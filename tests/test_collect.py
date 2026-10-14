from __future__ import annotations

import unittest
from datetime import date

from barometre.collect import (
    article_key,
    build_url,
    merge_article,
    parse_feed,
    prepare_collection,
)


SAMPLE_FEED = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss><channel><item>
  <title>Un titre</title>
  <link>https://news.google.com/articles/example</link>
  <pubDate>Wed, 14 Oct 2026 08:00:00 GMT</pubDate>
  <source url="https://example.test">M\xc3\xa9dia test</source>
</item></channel></rss>
"""


class CollectionTests(unittest.TestCase):
    def test_requested_days_are_inside_exclusive_google_bounds(self) -> None:
        url = build_url("racisme", date(2026, 10, 1), date(2026, 10, 14))
        self.assertIn("before%3A2026-10-15", url)
        self.assertIn("after%3A2026-09-30", url)

    def test_prepare_collection_rejects_reversed_window(self) -> None:
        with self.assertRaises(ValueError):
            prepare_collection("2026-10-14", "2026-10-01")

    def test_parse_feed_preserves_source_metadata(self) -> None:
        articles = parse_feed(SAMPLE_FEED, "racisme", "2026-10-14T10:00:00+00:00")
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["media"], "Média test")
        self.assertEqual(articles[0]["media_url"], "https://example.test")
        self.assertEqual(articles[0]["query_origins"], ["racisme"])

    def test_article_key_prefers_google_url(self) -> None:
        self.assertEqual(article_key({"google_url": "https://example.test/a"}), ("https://example.test/a",))

    def test_merge_article_keeps_every_query_origin(self) -> None:
        first = {
            "google_url": "https://example.test/a",
            "query_origins": ["acte raciste"],
            "first_seen_at_utc": "2026-10-14T10:00:00+00:00",
            "last_seen_at_utc": "2026-10-14T10:00:00+00:00",
        }
        second = {
            "google_url": "https://example.test/a",
            "query_origins": ["agression raciste"],
            "first_seen_at_utc": "2026-10-14T11:00:00+00:00",
            "last_seen_at_utc": "2026-10-14T11:00:00+00:00",
        }
        merged = merge_article(first, second)
        self.assertEqual(merged["query_origins"], ["acte raciste", "agression raciste"])
        self.assertEqual(merged["first_seen_at_utc"], "2026-10-14T10:00:00+00:00")
        self.assertEqual(merged["last_seen_at_utc"], "2026-10-14T11:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
