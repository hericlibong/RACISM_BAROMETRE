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
# Le périmètre éditorial est fixe : France et espace médiatique francophone.
# Ce n'est pas une option utilisateur du collecteur.
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
    # Les opérateurs Google `after:` et `before:` sont traités comme exclusifs.
    # On décale donc les deux bornes pour couvrir entièrement les jours demandés.
    after = start - timedelta(days=1)
    before = end + timedelta(days=1)
    windowed_query = f"{query} after:{after.isoformat()} before:{before.isoformat()}"
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
                "query_origins": [query],
                "first_seen_at_utc": collected_at,
                "last_seen_at_utc": collected_at,
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


def merge_article(existing: dict, incoming: dict) -> dict:
    """Fusionne deux occurrences du même article sans perdre leur provenance."""
    merged = dict(existing)
    for field in ("title", "google_url", "published_at", "media", "media_url"):
        if not merged.get(field) and incoming.get(field):
            merged[field] = incoming[field]

    origins = list(existing.get("query_origins") or [])
    legacy_origin = existing.get("query_origin")
    if legacy_origin and legacy_origin not in origins:
        origins.append(legacy_origin)
    for origin in incoming.get("query_origins") or []:
        if origin not in origins:
            origins.append(origin)
    merged["query_origins"] = origins
    merged.pop("query_origin", None)

    first_seen = [
        value
        for value in (
            existing.get("first_seen_at_utc") or existing.get("collected_at_utc"),
            incoming.get("first_seen_at_utc") or incoming.get("collected_at_utc"),
        )
        if value
    ]
    last_seen = [
        value
        for value in (
            existing.get("last_seen_at_utc") or existing.get("collected_at_utc"),
            incoming.get("last_seen_at_utc") or incoming.get("collected_at_utc"),
        )
        if value
    ]
    merged["first_seen_at_utc"] = min(first_seen) if first_seen else None
    merged["last_seen_at_utc"] = max(last_seen) if last_seen else None
    merged.pop("collected_at_utc", None)
    return merged


def load_existing(output: Path, plan: CollectionPlan) -> dict | None:
    if not output.exists():
        return None
    try:
        existing = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"sortie existante illisible : {output}") from exc

    expected_window = {"start": plan.start.isoformat(), "end": plan.end.isoformat()}
    if existing.get("collector") != "google-news-rss":
        raise ValueError(f"la sortie existante ne vient pas du collecteur Google News RSS : {output}")
    if existing.get("window") != expected_window:
        raise ValueError(
            f"la sortie existante porte sur une autre fenêtre : {existing.get('window')}"
        )
    return existing


def default_output_path(start: date, end: date) -> Path:
    return Path("data") / "raw" / f"gnews-{start.isoformat()}-{end.isoformat()}.json"


def collect_google_news(
    plan: CollectionPlan,
    output: Path,
    pause_seconds: float = 2.0,
) -> dict:
    existing_result = load_existing(output, plan)
    traces = []
    unique_articles: dict[tuple[str, ...], dict] = {}
    for article in (existing_result or {}).get("articles", []):
        unique_articles[article_key(article)] = article
    existing_article_count = len(unique_articles)

    for index, (query, url) in enumerate(plan.urls):
        started = datetime.now(timezone.utc)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
            status = response.status
        collected_at = datetime.now(timezone.utc).isoformat()
        articles = parse_feed(content, query=query, collected_at=collected_at)
        for article in articles:
            key = article_key(article)
            if key in unique_articles:
                unique_articles[key] = merge_article(unique_articles[key], article)
            else:
                unique_articles[key] = article
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
    collected_at = datetime.now(timezone.utc).isoformat()
    previous_runs = list((existing_result or {}).get("runs") or [])
    previous_runs.append({"collected_at_utc": collected_at, "traces": traces})
    result = {
        "collector": "google-news-rss",
        "edition": EDITION,
        "window": {"start": plan.start.isoformat(), "end": plan.end.isoformat()},
        "collected_at_utc": collected_at,
        "queries": list(plan.queries),
        "query_count": len(plan.queries),
        "article_count": len(articles),
        "existing_article_count": existing_article_count,
        "new_article_count": len(articles) - existing_article_count,
        "media_count": len(medias),
        "saturated_query_count": sum(1 for trace in traces if trace["saturated"]),
        "runs": previous_runs,
        "articles": articles,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
