"""Stockage de travail pour passer des articles collectés aux événements."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import unicodedata
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ARTICLE_ROLES = ("source_evenement", "reaction", "analyse", "hors_sujet")
EVENT_ARTICLE_ROLES = ("source", "reaction", "analyse")
EVENT_STATUSES = ("brouillon", "admis", "refuse", "incertain")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS collection_imports (
    id INTEGER PRIMARY KEY,
    source_path TEXT NOT NULL,
    source_digest TEXT NOT NULL UNIQUE,
    collector TEXT NOT NULL,
    window_start TEXT NOT NULL,
    window_end TEXT NOT NULL,
    imported_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    source_key TEXT NOT NULL UNIQUE,
    google_url TEXT,
    original_url TEXT,
    title TEXT NOT NULL,
    normalized_title TEXT NOT NULL,
    published_at TEXT,
    published_at_raw TEXT,
    media TEXT,
    media_url TEXT,
    first_seen_at_utc TEXT,
    last_seen_at_utc TEXT,
    suggested_role TEXT CHECK (suggested_role IN ('source_evenement', 'reaction', 'analyse', 'hors_sujet')),
    suggestion_reason TEXT,
    role TEXT CHECK (role IN ('source_evenement', 'reaction', 'analyse', 'hors_sujet')),
    role_note TEXT,
    reviewed_at_utc TEXT,
    duplicate_of INTEGER REFERENCES articles(id)
);

CREATE TABLE IF NOT EXISTS article_queries (
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    PRIMARY KEY (article_id, query)
);

CREATE TABLE IF NOT EXISTS grouping_proposals (
    id INTEGER PRIMARY KEY,
    signature TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'propose' CHECK (status IN ('propose', 'accepte', 'rejete')),
    created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS grouping_proposal_articles (
    proposal_id INTEGER NOT NULL REFERENCES grouping_proposals(id) ON DELETE CASCADE,
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    PRIMARY KEY (proposal_id, article_id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    public_id TEXT UNIQUE,
    date_start TEXT,
    date_end TEXT,
    date_precision TEXT,
    episode_date_start TEXT,
    episode_date_end TEXT,
    episode_date_precision TEXT,
    location TEXT,
    summary TEXT NOT NULL,
    nature TEXT,
    target_dimension TEXT,
    context TEXT,
    editorial_status TEXT NOT NULL DEFAULT 'brouillon'
        CHECK (editorial_status IN ('brouillon', 'admis', 'refuse', 'incertain')),
    notes TEXT,
    created_at_utc TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS event_articles (
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('source', 'reaction', 'analyse')),
    PRIMARY KEY (event_id, article_id)
);

CREATE TABLE IF NOT EXISTS event_relations (
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    related_event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    relation TEXT NOT NULL,
    PRIMARY KEY (event_id, related_event_id, relation),
    CHECK (event_id <> related_event_id)
);

CREATE INDEX IF NOT EXISTS idx_articles_role ON articles(role);
CREATE INDEX IF NOT EXISTS idx_articles_normalized_title ON articles(normalized_title);
CREATE INDEX IF NOT EXISTS idx_articles_duplicate_of ON articles(duplicate_of);
CREATE INDEX IF NOT EXISTS idx_event_articles_article ON event_articles(article_id);
"""

STOPWORDS = {
    "a", "acte", "actes", "actualite", "actualites", "agression", "apres", "au",
    "aux", "avec", "ce", "ces", "cette", "contre", "dans", "de", "des", "du",
    "en", "est", "et", "etre", "fait", "faits", "il", "injure", "injures", "insulte",
    "insultes", "la",
    "le", "les", "leur", "leurs", "lors", "mais", "ne", "nouveau", "nouvelle",
    "orange", "ou", "par", "pas", "plus", "pour", "presume", "presumes", "propos",
    "qui", "racisme", "raciste", "racistes", "sa", "se", "ses", "son", "sur", "un",
    "une", "vers",
}

REACTION_MARKERS = (
    "condamne", "denonce", "reagit", "reaction", "soutien", "defend", "estime",
    "ne croit", "vole au secours", "au secours de", "juge les sanctions",
)
ANALYSIS_MARKERS = (
    "analyse", "edito", "retour sur", "ce que revele", "ce que l on sait",
    "revue de presse", "entretien", "business de la haine",
)
EVENT_MARKERS = (
    "agression raciste", "acte raciste", "actes racistes", "injure raciste",
    "injures racistes", "insulte raciste", "insultes racistes", "propos racistes",
    "message raciste", "messages racistes", "publication raciste", "publications racistes",
    "ecrit antisemite", "ecrits antisemites", "acte antisemite", "actes antisemites",
    "propos antisemites", "haine raciale", "symbole nazi", "symboles nazis",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(character for character in value if not unicodedata.combining(character))
    return " ".join(re.findall(r"[a-z0-9]+", value))


def headline_tokens(title: str) -> set[str]:
    return {
        token
        for token in normalize_text(title).split()
        if len(token) >= 3 and token not in STOPWORDS
    }


def infer_role(title: str) -> tuple[str | None, str | None]:
    """Propose un rôle depuis le titre, sans prendre de décision éditoriale."""
    normalized = normalize_text(title)
    for marker in ANALYSIS_MARKERS:
        if marker in normalized:
            return "analyse", f"marqueur de titre : {marker}"
    for marker in REACTION_MARKERS:
        if marker in normalized:
            return "reaction", f"marqueur de titre : {marker}"
    for marker in EVENT_MARKERS:
        if marker in normalized:
            return "source_evenement", f"marqueur de titre : {marker}"
    return None, None


def source_key(article: dict) -> str:
    if article.get("google_url"):
        return f"gnews:{article['google_url']}"
    material = "\n".join(
        str(article.get(field) or "") for field in ("title", "media", "published_at")
    )
    return f"fallback:{hashlib.sha256(material.encode('utf-8')).hexdigest()}"


def parse_published_at(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).isoformat()
    except (TypeError, ValueError):
        return None


def connect(database: Path) -> sqlite3.Connection:
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    initialize_database(connection)
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA)
    article_columns = {row[1] for row in connection.execute("PRAGMA table_info(articles)")}
    if "original_url" not in article_columns:
        connection.execute("ALTER TABLE articles ADD COLUMN original_url TEXT")
    columns = {
        row[1] for row in connection.execute("PRAGMA table_info(events)").fetchall()
    }
    for name in ("episode_date_start", "episode_date_end", "episode_date_precision"):
        if name not in columns:
            connection.execute(f"ALTER TABLE events ADD COLUMN {name} TEXT")
    if "publication_validated_at" not in columns:
        connection.execute("ALTER TABLE events ADD COLUMN publication_validated_at TEXT")
    if "origin" not in columns:
        connection.execute("ALTER TABLE events ADD COLUMN origin TEXT NOT NULL DEFAULT 'collecte'")
    connection.executescript("""
        CREATE TRIGGER IF NOT EXISTS event_recheck_after_edit
        AFTER UPDATE OF summary, date_start, date_end, date_precision, episode_date_start,
            episode_date_end, episode_date_precision, location, nature, target_dimension,
            context, editorial_status ON events
        WHEN OLD.publication_validated_at IS NOT NULL AND (
            OLD.summary IS NOT NEW.summary OR OLD.date_start IS NOT NEW.date_start OR
            OLD.date_end IS NOT NEW.date_end OR OLD.date_precision IS NOT NEW.date_precision OR
            OLD.episode_date_start IS NOT NEW.episode_date_start OR
            OLD.episode_date_end IS NOT NEW.episode_date_end OR
            OLD.episode_date_precision IS NOT NEW.episode_date_precision OR
            OLD.location IS NOT NEW.location OR OLD.nature IS NOT NEW.nature OR
            OLD.target_dimension IS NOT NEW.target_dimension OR OLD.context IS NOT NEW.context OR
            OLD.editorial_status IS NOT NEW.editorial_status)
        BEGIN
            UPDATE events SET publication_validated_at=NULL WHERE id=NEW.id;
        END;
        CREATE TRIGGER IF NOT EXISTS event_recheck_after_source_added
        AFTER INSERT ON event_articles
        BEGIN
            UPDATE events SET publication_validated_at=NULL WHERE id=NEW.event_id;
        END;
        CREATE TRIGGER IF NOT EXISTS event_recheck_after_source_removed
        AFTER DELETE ON event_articles
        BEGIN
            UPDATE events SET publication_validated_at=NULL WHERE id=OLD.event_id;
        END;
        CREATE TRIGGER IF NOT EXISTS event_recheck_after_source_role
        AFTER UPDATE OF role ON event_articles WHEN OLD.role IS NOT NEW.role
        BEGIN
            UPDATE events SET publication_validated_at=NULL WHERE id=NEW.event_id;
        END;
    """)


def load_collection(path: Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    try:
        collection = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"collecte JSON illisible : {path}") from exc
    if collection.get("collector") != "google-news-rss":
        raise ValueError("le fichier n'est pas une collecte Google News RSS du baromètre")
    window = collection.get("window") or {}
    if not window.get("start") or not window.get("end"):
        raise ValueError("la fenêtre de collecte est absente")
    if not isinstance(collection.get("articles"), list):
        raise ValueError("la liste des articles est absente")
    return collection, hashlib.sha256(raw).hexdigest()


def import_collection(connection: sqlite3.Connection, path: Path) -> dict[str, int]:
    collection, digest = load_collection(path)
    initialize_database(connection)
    before = connection.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    now = utc_now()
    window = collection["window"]

    with connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO collection_imports
                (source_path, source_digest, collector, window_start, window_end, imported_at_utc)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (str(path), digest, collection["collector"], window["start"], window["end"], now),
        )
        for article in collection["articles"]:
            title = str(article.get("title") or "").strip()
            if not title:
                continue
            suggested_role, reason = infer_role(title)
            key = source_key(article)
            connection.execute(
                """
                INSERT INTO articles (
                    source_key, google_url, title, normalized_title, published_at,
                    published_at_raw, media, media_url, first_seen_at_utc, last_seen_at_utc,
                    suggested_role, suggestion_reason
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_key) DO UPDATE SET
                    title = excluded.title,
                    normalized_title = excluded.normalized_title,
                    media = COALESCE(excluded.media, articles.media),
                    media_url = COALESCE(excluded.media_url, articles.media_url),
                    first_seen_at_utc = MIN(articles.first_seen_at_utc, excluded.first_seen_at_utc),
                    last_seen_at_utc = MAX(articles.last_seen_at_utc, excluded.last_seen_at_utc),
                    suggested_role = COALESCE(articles.suggested_role, excluded.suggested_role),
                    suggestion_reason = COALESCE(articles.suggestion_reason, excluded.suggestion_reason)
                """,
                (
                    key,
                    article.get("google_url"),
                    title,
                    normalize_text(title),
                    parse_published_at(article.get("published_at")),
                    article.get("published_at"),
                    article.get("media"),
                    article.get("media_url"),
                    article.get("first_seen_at_utc"),
                    article.get("last_seen_at_utc"),
                    suggested_role,
                    reason,
                ),
            )
            article_id = connection.execute(
                "SELECT id FROM articles WHERE source_key = ?", (key,)
            ).fetchone()[0]
            for query in article.get("query_origins") or []:
                connection.execute(
                    "INSERT OR IGNORE INTO article_queries (article_id, query) VALUES (?, ?)",
                    (article_id, query),
                )

        mark_exact_duplicates(connection)
        proposal_count = rebuild_grouping_proposals(connection)

    after = connection.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    duplicates = connection.execute(
        "SELECT COUNT(*) FROM articles WHERE duplicate_of IS NOT NULL"
    ).fetchone()[0]
    suggestions = connection.execute(
        "SELECT COUNT(*) FROM articles WHERE suggested_role IS NOT NULL"
    ).fetchone()[0]
    return {
        "article_count": after,
        "new_article_count": after - before,
        "exact_duplicate_count": duplicates,
        "suggested_role_count": suggestions,
        "grouping_proposal_count": proposal_count,
    }


def mark_exact_duplicates(connection: sqlite3.Connection) -> None:
    connection.execute("UPDATE articles SET duplicate_of = NULL")
    groups = connection.execute(
        """
        SELECT normalized_title, MIN(id) AS canonical_id
        FROM articles
        GROUP BY normalized_title
        HAVING COUNT(*) > 1
        """
    ).fetchall()
    for group in groups:
        connection.execute(
            """
            UPDATE articles SET duplicate_of = ?
            WHERE normalized_title = ? AND id <> ?
            """,
            (group["canonical_id"], group["normalized_title"], group["canonical_id"]),
        )


def titles_are_related(left: str, right: str) -> bool:
    left_tokens = headline_tokens(left)
    right_tokens = headline_tokens(right)
    shared = left_tokens & right_tokens
    if len(shared) < 3:
        return False
    union = left_tokens | right_tokens
    return bool(union) and len(shared) / len(union) >= 0.34


def rebuild_grouping_proposals(connection: sqlite3.Connection) -> int:
    """Reconstruit seulement les propositions non arbitrées."""
    connection.execute("DELETE FROM grouping_proposals WHERE status = 'propose'")
    articles = connection.execute(
        "SELECT id, source_key, title FROM articles WHERE duplicate_of IS NULL ORDER BY id"
    ).fetchall()
    parent = {row["id"]: row["id"] for row in articles}

    def find(item: int) -> int:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for index, left in enumerate(articles):
        for right in articles[index + 1 :]:
            if titles_are_related(left["title"], right["title"]):
                union(left["id"], right["id"])

    groups: dict[int, list[sqlite3.Row]] = {}
    for article in articles:
        groups.setdefault(find(article["id"]), []).append(article)

    now = utc_now()
    count = 0
    for group in groups.values():
        if len(group) < 2:
            continue
        keys = sorted(article["source_key"] for article in group)
        signature = hashlib.sha256("\n".join(keys).encode("utf-8")).hexdigest()
        label = min((article["title"] for article in group), key=len)
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO grouping_proposals (signature, label, created_at_utc)
            VALUES (?, ?, ?)
            """,
            (signature, label, now),
        )
        proposal_id = cursor.lastrowid
        if not proposal_id:
            proposal_id = connection.execute(
                "SELECT id FROM grouping_proposals WHERE signature = ?", (signature,)
            ).fetchone()[0]
        for article in group:
            connection.execute(
                """
                INSERT OR IGNORE INTO grouping_proposal_articles (proposal_id, article_id)
                VALUES (?, ?)
                """,
                (proposal_id, article["id"]),
            )
        count += 1
    return count


def set_article_role(
    connection: sqlite3.Connection, article_id: int, role: str, note: str | None = None
) -> None:
    if role not in ARTICLE_ROLES:
        raise ValueError(f"rôle invalide : {role}")
    with connection:
        cursor = connection.execute(
            """
            UPDATE articles SET role = ?, role_note = ?, reviewed_at_utc = ? WHERE id = ?
            """,
            (role, note, utc_now(), article_id),
        )
        if cursor.rowcount != 1:
            raise ValueError(f"article introuvable : {article_id}")


def create_event(
    connection: sqlite3.Connection,
    summary: str,
    article_ids: list[int] | None = None,
    status: str = "brouillon",
) -> str:
    if status not in EVENT_STATUSES:
        raise ValueError(f"statut invalide : {status}")
    if not summary.strip():
        raise ValueError("le résumé de l'événement est obligatoire")
    now = utc_now()
    with connection:
        cursor = connection.execute(
            """
            INSERT INTO events (summary, editorial_status, created_at_utc, updated_at_utc)
            VALUES (?, ?, ?, ?)
            """,
            (summary.strip(), status, now, now),
        )
        event_id = cursor.lastrowid
        public_id = f"E{event_id:06d}"
        connection.execute(
            "UPDATE events SET public_id = ? WHERE id = ?", (public_id, event_id)
        )
        for article_id in article_ids or []:
            attach_article(connection, public_id, article_id, "source", commit=False)
    return public_id


def event_database_id(connection: sqlite3.Connection, public_id: str) -> int:
    row = connection.execute(
        "SELECT id FROM events WHERE public_id = ?", (public_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"événement introuvable : {public_id}")
    return row[0]


def attach_article(
    connection: sqlite3.Connection,
    public_id: str,
    article_id: int,
    role: str,
    *,
    commit: bool = True,
) -> None:
    if role not in EVENT_ARTICLE_ROLES:
        raise ValueError(f"rôle de rattachement invalide : {role}")
    event_id = event_database_id(connection, public_id)
    if connection.execute("SELECT 1 FROM articles WHERE id = ?", (article_id,)).fetchone() is None:
        raise ValueError(f"article introuvable : {article_id}")
    connection.execute(
        """
        INSERT INTO event_articles (event_id, article_id, role) VALUES (?, ?, ?)
        ON CONFLICT(event_id, article_id) DO UPDATE SET role = excluded.role
        """,
        (event_id, article_id, role),
    )
    if commit:
        connection.commit()


def detach_article(connection: sqlite3.Connection, public_id: str, article_id: int) -> None:
    event_id = event_database_id(connection, public_id)
    with connection:
        cursor = connection.execute(
            "DELETE FROM event_articles WHERE event_id = ? AND article_id = ?",
            (event_id, article_id),
        )
        if cursor.rowcount != 1:
            raise ValueError("ce rattachement n'existe pas")


def update_event(connection: sqlite3.Connection, public_id: str, **changes: str | None) -> None:
    allowed = {
        "date_start",
        "date_end",
        "date_precision",
        "episode_date_start",
        "episode_date_end",
        "episode_date_precision",
        "location",
        "summary",
        "nature",
        "target_dimension",
        "context",
        "editorial_status",
        "notes",
    }
    unexpected = set(changes) - allowed
    if unexpected:
        raise ValueError(f"champ(s) d'événement invalide(s) : {', '.join(sorted(unexpected))}")
    if changes.get("editorial_status") not in (None, *EVENT_STATUSES):
        raise ValueError(f"statut invalide : {changes['editorial_status']}")
    effective = {name: value for name, value in changes.items() if value is not None}
    if not effective:
        raise ValueError("aucune modification fournie")
    if "summary" in effective and not str(effective["summary"]).strip():
        raise ValueError("le résumé ne peut pas être vide")
    event_id = event_database_id(connection, public_id)
    effective["updated_at_utc"] = utc_now()
    assignments = ", ".join(f"{name} = ?" for name in effective)
    with connection:
        connection.execute(
            f"UPDATE events SET {assignments} WHERE id = ?",
            (*effective.values(), event_id),
        )


def database_summary(connection: sqlite3.Connection) -> dict[str, int]:
    initialize_database(connection)
    queries = {
        "articles": "SELECT COUNT(*) FROM articles",
        "doublons_exacts": "SELECT COUNT(*) FROM articles WHERE duplicate_of IS NOT NULL",
        "roles_proposes": "SELECT COUNT(*) FROM articles WHERE suggested_role IS NOT NULL",
        "roles_valides": "SELECT COUNT(*) FROM articles WHERE role IS NOT NULL",
        "articles_a_verifier": (
            "SELECT COUNT(*) FROM articles "
            "WHERE role IS NULL AND duplicate_of IS NULL"
        ),
        "regroupements_proposes": "SELECT COUNT(*) FROM grouping_proposals WHERE status = 'propose'",
        "evenements": "SELECT COUNT(*) FROM events",
    }
    return {name: connection.execute(sql).fetchone()[0] for name, sql in queries.items()}


def export_events(connection: sqlite3.Connection, output: Path) -> dict:
    """Exporte les événements qualifiés dans un format lisible hors de SQLite."""
    initialize_database(connection)
    events = []
    event_rows = connection.execute("SELECT * FROM events ORDER BY id").fetchall()
    event_fields = (
        "public_id",
        "date_start",
        "date_end",
        "date_precision",
        "episode_date_start",
        "episode_date_end",
        "episode_date_precision",
        "location",
        "summary",
        "nature",
        "context",
        "editorial_status",
        "notes",
        "origin",
        "publication_validated_at",
    )
    for event in event_rows:
        item = {field: event[field] for field in event_fields}
        # Le stockage conserve provisoirement l'ancien nom technique, mais la
        # sortie publique décrit les personnes visées sans créer des
        # catégories de type « racisme anti-X ».
        item["persons_targeted"] = event["target_dimension"]
        item["counted_in_barometer"] = event["editorial_status"] == "admis"
        item["publishable"] = item["counted_in_barometer"] and bool(event["publication_validated_at"])
        item["status_label"] = {
            "brouillon": "brouillon",
            "admis": "admis au comptage",
            "refuse": "hors comptage, conservé pour contexte",
            "incertain": "à vérifier",
        }[event["editorial_status"]]
        sources = connection.execute(
            """
            SELECT a.id AS article_id, ea.role, a.title, a.media, a.published_at,
                   a.google_url, COALESCE(a.original_url, a.google_url) AS source_url,
                   a.role AS reviewed_role, a.role_note
            FROM event_articles ea
            JOIN articles a ON a.id = ea.article_id
            WHERE ea.event_id = ?
            ORDER BY a.published_at, a.id
            """,
            (event["id"],),
        ).fetchall()
        item["articles"] = [dict(source) for source in sources]
        item["relations"] = [
            dict(row) for row in connection.execute(
                """SELECT e.public_id AS related_event, er.relation
                   FROM event_relations er JOIN events e ON e.id=er.related_event_id
                   WHERE er.event_id=? ORDER BY e.id, er.relation""", (event["id"],)
            ).fetchall()
        ]
        events.append(item)

    windows = [
        dict(row)
        for row in connection.execute(
            """
            SELECT DISTINCT window_start AS start, window_end AS end
            FROM collection_imports ORDER BY window_start, window_end
            """
        ).fetchall()
    ]
    candidates = [
        dict(row)
        for row in connection.execute(
            """
            SELECT id AS article_id, title, media, published_at, google_url,
                   suggested_role, suggestion_reason, role_note AS review_question
            FROM articles
            WHERE role IS NULL AND duplicate_of IS NULL
            ORDER BY published_at, id
            """
        ).fetchall()
    ]
    reviewed_articles = [
        dict(row)
        for row in connection.execute(
            """
            SELECT a.id AS article_id, a.title, a.media, a.published_at,
                   a.google_url, a.role AS reviewed_role, a.role_note
            FROM articles a
            WHERE a.role IS NOT NULL
              AND a.duplicate_of IS NULL
              AND NOT EXISTS (
                  SELECT 1 FROM event_articles ea WHERE ea.article_id = a.id
              )
            ORDER BY a.published_at, a.id
            """
        ).fetchall()
    ]
    result = {
        "exported_at_utc": utc_now(),
        "collection_windows": windows,
        "review_progress": database_summary(connection),
        "events": events,
        "reviewed_articles_without_event": reviewed_articles,
        "candidates_to_review": candidates,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
