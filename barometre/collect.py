"""Collecteur Google News RSS du baromètre."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from importlib.resources import files
from pathlib import Path

ENDPOINT = "https://news.google.com/rss/search"
EDITION = {"hl": "fr", "gl": "FR", "ceid": "FR:fr"}
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)


@dataclass(frozen=True)
class CollectionPlan:
    start: date
    end: date
    queries: tuple[str, ...]
    urls: tuple[tuple[str, str], ...]


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"date invalide « {value} » ; format attendu AAAA-MM-JJ") from exc


def load_queries(path: Path | None = None) -> tuple[str, ...]:
    if path is None:
        content = files("barometre").joinpath("queries.txt").read_text(encoding="utf-8")
    else:
        content = path.read_text(encoding="utf-8")

    queries = tuple(
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )
    if not queries:
        raise ValueError("le fichier de requêtes ne contient aucune requête")
    return queries


def build_url(query: str, start: date, end: date) -> str:
    before = end + timedelta(days=1)
    windowed_query = f"{query} after:{start.isoformat()} before:{before.isoformat()}"
    parameters = urllib.parse.urlencode({"q": windowed_query, **EDITION})
    return f"{ENDPOINT}?{parameters}"


def prepare_collection(
    start: str,
    end: str,
    queries_file: Path | None = None,
    limit_queries: int | None = None,
) -> CollectionPlan:
    start_date = parse_date(start)
    end_date = parse_date(end)
    if end_date < start_date:
        raise ValueError("la date de fin doit être postérieure ou égale à la date de début")

    queries = load_queries(queries_file)
    if limit_queries is not None:
        if limit_queries < 1:
            raise ValueError("--limit-queries doit être supérieur ou égal à 1")
        queries = queries[:limit_queries]

    urls = tuple((query, build_url(query, start_date, end_date)) for query in queries)
    return CollectionPlan(start=start_date, end=end_date, queries=queries, urls=urls)


def parse_feed(content: bytes, query: str, collected_at: str) -> list[dict]:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise ValueError(f"flux XML illisible pour la requête {query!r}: {exc}") from exc

    articles = []
    for item in root.iterfind(".//item"):
        source = item.find("source")
        articles.append(
            {
                "title": (item.findtext("title") or "").strip(),
                "google_url": (item.findtext("link") or "").strip(),
                "published_at": (item.findtext("pubDate") or "").strip(),
                "media": (source.text or "").strip() if source is not None else None,
                "media_url": source.get("url") if source is not None else None,
                "query_origin": query,
                "collected_at_utc": collected_at,
            }
        )
    return articles


def article_key(article: dict) -> tuple[str, ...]:
    if article.get("google_url"):
        return (article["google_url"],)
    return (
        article.get("title") or "",
        article.get("media") or "",
        article.get("published_at") or "",
    )


def default_output_path(start: date, end: date) -> Path:
    return Path("data") / "raw" / f"gnews-{start.isoformat()}-{end.isoformat()}.json"


def collect_google_news(
    plan: CollectionPlan,
    output: Path,
    pause_seconds: float = 2.0,
) -> dict:
    traces = []
    unique_articles: dict[tuple[str, ...], dict] = {}

    for index, (query, url) in enumerate(plan.urls):
        started = datetime.now(timezone.utc)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
            status = response.status
        collected_at = datetime.now(timezone.utc).isoformat()
        articles = parse_feed(content, query=query, collected_at=collected_at)
        for article in articles:
            unique_articles.setdefault(article_key(article), article)
        traces.append(
            {
                "query": query,
                "url": url,
                "started_at_utc": started.isoformat(),
                "duration_seconds": round(
                    (datetime.now(timezone.utc) - started).total_seconds(), 2
                ),
                "http_status": status,
                "article_count": len(articles),
                "saturated": len(articles) >= 100,
            }
        )
        if index < len(plan.urls) - 1 and pause_seconds:
            time.sleep(pause_seconds)

    articles = list(unique_articles.values())
    medias = sorted({article["media"] for article in articles if article.get("media")})
    result = {
        "collector": "google-news-rss",
        "edition": EDITION,
        "window": {"start": plan.start.isoformat(), "end": plan.end.isoformat()},
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "queries": list(plan.queries),
        "query_count": len(plan.queries),
        "article_count": len(articles),
        "media_count": len(medias),
        "traces": traces,
        "articles": articles,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
