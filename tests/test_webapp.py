from contextlib import closing
from datetime import date
from http.client import HTTPConnection
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import urlencode
import unittest

from barometre.storage import connect, create_event, update_event
from barometre.webapp import LocalApp, series


class WebAppTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        database = Path(temporary.name) / "test.sqlite"
        with closing(connect(database)) as db:
            self.existing = create_event(db, "Incident à Dijon", status="admis")
            update_event(db, self.existing, date_start="2026-10-24", location="Dijon")
        try:
            self.app = LocalApp(database, 0)
        except PermissionError:
            self.skipTest("Les sockets locales sont interdites dans cet environnement de test.")
        worker = Thread(target=self.app.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(self.app.server_close)
        self.addCleanup(worker.join, 5)
        self.addCleanup(self.app.shutdown)

    def request(self, path, form=None):
        with closing(HTTPConnection("127.0.0.1", self.app.server_port, timeout=5)) as http:
            if form is None:
                http.request("GET", path)
            else:
                http.request("POST", path, urlencode(form),
                             {"Content-Type": "application/x-www-form-urlencoded"})
            response = http.getresponse()
            return response.status, response.read().decode("utf-8"), response.getheader("Location")

    def test_human_review_and_source_change_through_http(self):
        status, body, _ = self.request("/?location=dijon&unite=day")
        self.assertEqual(status, 200)
        self.assertIn('data-count="1"', body)
        self.assertIn('24 octobre 2026', body)
        self.assertEqual(self.request(f"/public/{self.existing}")[0], 404)

        form = {"summary": "Signalement & source", "location": "Nantes",
                "source_url": "https://example.com/article", "media": "Journal",
                "date_start": "2026-10", "token": self.app.token}
        self.assertEqual(self.request("/relecture/ajouter", {**form, "token": ""})[0], 403)
        code, _, location = self.request("/relecture/ajouter", form)
        self.assertEqual(code, 303)
        route = location.split("?")[0]
        public = route.replace("/relecture/", "/public/")
        self.assertEqual(self.request(public)[0], 404)
        self.assertIn("Ajout manuel", self.request(route)[1])
        self.assertEqual(self.request(route, {"action": "approve", "token": self.app.token})[0], 303)
        self.assertEqual(self.request(public)[0], 200)
        self.assertIn("https://example.com/article", self.request(public)[1])
        self.assertIn('data-count="1"', self.request("/public?unite=month")[1])

        with closing(connect(self.app.database)) as db:
            article = db.execute("SELECT id FROM articles WHERE media='Journal'").fetchone()[0]
        review = self.request(route)[1]
        self.assertIn('href="#sources">Lire les articles</a>', review)
        self.assertIn(f'?deplacer={article}#article-{article}', review)
        self.assertNotIn('name="destination"', review)
        chooser = self.request(f"{route}?deplacer={article}")[1]
        self.assertIn('name="destination" required', chooser)
        self.assertIn(f'<option value="{self.existing}">24 octobre 2026 · Dijon · Incident à Dijon</option>', chooser)
        move = {"action": "move", "token": self.app.token, "article_id": article,
                "link_role": "source", "destination": self.existing}
        self.assertEqual(self.request(route, move)[0], 303)
        self.assertEqual(self.request(public)[0], 404)
        self.assertIn("Articles et réactions (1)", self.request(f"/evenements/{self.existing}")[1])
        self.assertEqual(self.request(route, {"action": "approve", "token": self.app.token})[0], 400)

    def test_preview_and_attach_article_by_url_in_existing_dossier(self):
        route = f"/relecture/{self.existing}"
        public = f"/public/{self.existing}"
        token = self.app.token
        code, _, _ = self.request(route, {"action": "save", "token": token, "notes": "À vérifier en interne",
                                          "episode_date_start": "2026-10-28", "episode_date_precision": "Annonce du parquet"})
        self.assertEqual(code, 303)
        preview_link = f"{route}?apercu=1"
        self.assertIn(preview_link, self.request(route)[1])
        code, preview, _ = self.request(preview_link)
        self.assertEqual(code, 200)
        self.assertIn("24 octobre 2026", preview)
        self.assertIn("28 octobre 2026", preview)
        self.assertNotIn("À vérifier en interne", preview)
        self.assertEqual(self.request(public)[0], 404)

        article = {"action": "link-url", "token": token, "source_url": "https://example.com/reaction",
                   "media": "Journal local", "article_title": "Une association réagit", "link_role": "reaction",
                   "published_at": "2026-10-25"}
        self.assertEqual(self.request(route, {**article, "published_at": "2026-10"})[0], 400)
        self.assertEqual(self.request(route, article)[0], 303)
        self.assertEqual(self.request(route, article)[0], 400)
        self.assertEqual(self.request(route, {"action": "approve", "token": token})[0], 400)
        self.assertIn("Réactions (1)", self.request(route)[1])
        preview = self.request(preview_link)[1]
        self.assertIn("https://example.com/reaction", preview)
        self.assertIn("25 octobre 2026", preview)
        self.assertIn("Incident à Dijon", preview)

        source = {**article, "source_url": "https://example.com/report", "link_role": "source"}
        self.assertEqual(self.request(route, source)[0], 303)
        self.assertEqual(self.request(route, {"action": "approve", "token": token})[0], 303)
        self.assertIn("Articles et réactions (2)", self.request(public)[1])
        self.assertIn('data-count="1"', self.request("/public?unite=day")[1])


class CountingTests(unittest.TestCase):
    def test_imprecise_dates_are_only_counted_in_a_defensible_period(self):
        events = [
            {"date_start": "2026-10", "date_end": None, "editorial_status": "admis"},
            {"date_start": None, "date_end": "2026-10-23", "editorial_status": "admis"},
            {"date_start": "2026-10-23", "date_end": "2026-10-23", "editorial_status": "incertain"},
        ]
        self.assertEqual(series(events, "day", None, None), ({}, 2))
        self.assertEqual(series(events, "month", None, None), ({date(2026, 10, 1): 1}, 1))
        self.assertEqual(series(events, "month", date(2026, 10, 15), None), ({}, 2))
