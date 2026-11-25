from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from barometre.storage import (
    attach_article,
    connect,
    create_event,
    database_summary,
    detach_article,
    export_events,
    import_collection,
    infer_role,
    set_article_role,
    update_event,
)


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.database = root / "barometre.sqlite"
        self.collection = root / "collection.json"
        articles = [
            {
                "title": "Coco Gauff visée par des insultes racistes, les Nations unies réagissent",
                "google_url": "https://news.google.test/1",
                "published_at": "Sun, 11 Oct 2026 16:09:43 GMT",
                "media": "Média A",
                "query_origins": ["insultes racistes"],
            },
            {
                "title": "Coco Gauff visée par des insultes racistes, les Nations unies réagissent",
                "google_url": "https://news.google.test/2",
                "published_at": "Sun, 11 Oct 2026 16:09:43 GMT",
                "media": "Média A",
                "query_origins": ["racisme sport"],
            },
            {
                "title": "L'ONU condamne les insultes racistes visant Coco Gauff",
                "google_url": "https://news.google.test/3",
                "published_at": "Sun, 11 Oct 2026 17:09:43 GMT",
                "media": "Média B",
                "query_origins": ["insultes racistes"],
            },
        ]
        payload = {
            "collector": "google-news-rss",
            "window": {"start": "2026-10-10", "end": "2026-10-14"},
            "articles": articles,
        }
        self.collection.write_text(json.dumps(payload), encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_import_is_idempotent_and_preserves_queries(self) -> None:
        with closing(connect(self.database)) as connection:
            first = import_collection(connection, self.collection)
            second = import_collection(connection, self.collection)
            query_count = connection.execute("SELECT COUNT(*) FROM article_queries").fetchone()[0]
        self.assertEqual(first["article_count"], 3)
        self.assertEqual(first["new_article_count"], 3)
        self.assertEqual(second["new_article_count"], 0)
        self.assertEqual(query_count, 3)

    def test_exact_duplicate_is_marked_without_deleting_articles(self) -> None:
        with closing(connect(self.database)) as connection:
            result = import_collection(connection, self.collection)
            rows = connection.execute("SELECT id, duplicate_of FROM articles ORDER BY id").fetchall()
        self.assertEqual(result["exact_duplicate_count"], 1)
        self.assertIsNone(rows[0]["duplicate_of"])
        self.assertEqual(rows[1]["duplicate_of"], rows[0]["id"])

    def test_roles_are_only_suggestions_until_reviewed(self) -> None:
        role, reason = infer_role("Aphatie dénonce le business de la haine dans les médias")
        self.assertEqual(role, "analyse")
        self.assertIn("business de la haine", reason)
        with closing(connect(self.database)) as connection:
            import_collection(connection, self.collection)
            self.assertEqual(database_summary(connection)["roles_valides"], 0)
            set_article_role(connection, 1, "reaction", "Réaction à rattacher")
            self.assertEqual(database_summary(connection)["roles_valides"], 1)

    def test_generic_racist_wording_does_not_merge_distinct_places(self) -> None:
        from barometre.storage import titles_are_related

        self.assertFalse(
            titles_are_related(
                "Agression raciste à Cergy, le suspect arrêté - Orange Actualités",
                "Agression raciste à Dole : le procès s'ouvre - Orange Actualités",
            )
        )

    def test_event_links_can_be_corrected_without_touching_raw_json(self) -> None:
        original = self.collection.read_bytes()
        with closing(connect(self.database)) as connection:
            import_collection(connection, self.collection)
            public_id = create_event(connection, "Insultes racistes visant Coco Gauff", [1])
            attach_article(connection, public_id, 3, "reaction")
            linked = connection.execute("SELECT COUNT(*) FROM event_articles").fetchone()[0]
            detach_article(connection, public_id, 3)
            corrected = connection.execute("SELECT COUNT(*) FROM event_articles").fetchone()[0]
        self.assertEqual(public_id, "E000001")
        self.assertEqual(linked, 2)
        self.assertEqual(corrected, 1)
        self.assertEqual(self.collection.read_bytes(), original)

    def test_event_keeps_fact_and_news_episode_dates_separate(self) -> None:
        with closing(connect(self.database)) as connection:
            import_collection(connection, self.collection)
            public_id = create_event(connection, "Un fait ancien connaît une nouvelle actualité")
            update_event(
                connection,
                public_id,
                date_start="2018",
                date_precision="année",
                episode_date_start="2026-10-09",
                episode_date_precision="jour",
            )
            row = connection.execute(
                "SELECT date_start, episode_date_start FROM events WHERE public_id = ?",
                (public_id,),
            ).fetchone()
        self.assertEqual(row["date_start"], "2018")
        self.assertEqual(row["episode_date_start"], "2026-10-09")

    def test_export_contains_event_and_source_roles(self) -> None:
        output = Path(self.temporary_directory.name) / "events.json"
        with closing(connect(self.database)) as connection:
            import_collection(connection, self.collection)
            public_id = create_event(connection, "Insultes visant Coco Gauff", [1])
            attach_article(connection, public_id, 3, "reaction")
            update_event(connection, public_id, target_dimension="Personnes visées : personnes noires")
            result = export_events(connection, output)
        self.assertEqual(len(result["events"]), 1)
        self.assertEqual(result["events"][0]["articles"][0]["role"], "source")
        self.assertEqual(result["events"][0]["articles"][1]["role"], "reaction")
        self.assertFalse(result["events"][0]["counted_in_barometer"])
        self.assertEqual(result["events"][0]["status_label"], "brouillon")
        self.assertEqual(
            result["events"][0]["persons_targeted"],
            "Personnes visées : personnes noires",
        )
        self.assertNotIn("target_dimension", result["events"][0])
        self.assertEqual(len(result["candidates_to_review"]), 2)
        self.assertEqual(result["reviewed_articles_without_event"], [])
        self.assertTrue(output.exists())

    def test_export_keeps_review_questions_source_urls_and_event_relations(self) -> None:
        output = Path(self.temporary_directory.name) / "events.json"
        with closing(connect(self.database)) as connection:
            import_collection(connection, self.collection)
            parent = create_event(connection, "Fait initial", [1], status="admis")
            child = create_event(connection, "Nouveau propos en réaction", [3], status="incertain")
            connection.execute(
                "INSERT INTO event_relations VALUES (2, 1, ?)", ("réaction autonome",)
            )
            connection.execute(
                "UPDATE articles SET original_url=?, role_note=? WHERE id=3",
                ("https://media.test/article", "Confirmer la date des propos"),
            )
            result = export_events(connection, output)
        self.assertEqual(result["events"][1]["public_id"], child)
        self.assertFalse(result["events"][1]["counted_in_barometer"])
        self.assertEqual(result["events"][1]["relations"], [
            {"related_event": parent, "relation": "réaction autonome"}
        ])
        self.assertEqual(result["events"][1]["articles"][0]["source_url"], "https://media.test/article")
        self.assertEqual(result["events"][0]["articles"][0]["source_url"], "https://news.google.test/1")
        pending = {item["article_id"]: item for item in result["candidates_to_review"]}
        self.assertEqual(pending[3]["review_question"], "Confirmer la date des propos")


if __name__ == "__main__":
    unittest.main()
