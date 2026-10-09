"""Eigen tests fixronde iteratie 4: 404-pagina, placeholder zoekveld, aantal feeds."""
import json
import os
import sys
import tempfile
import unittest

BASIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(BASIS, "src"))
import bouw  # noqa: E402


class TestFixronde(unittest.TestCase):
    def test_feeds_binnen_grenzen(self):
        with open(os.path.join(BASIS, "config", "feeds.json"), encoding="utf-8") as f:
            feeds = json.load(f)["feeds"]
        self.assertTrue(8 <= len(feeds) <= 10)
        self.assertTrue(all(fd["naam"] and fd["url"] and fd["taal"] in ("nl", "en") for fd in feeds))
        self.assertTrue(any("n8n" in fd["url"] for fd in feeds))

    def test_404_en_placeholder(self):
        with tempfile.TemporaryDirectory() as t:
            data = os.path.join(t, "n.json")
            with open(data, "w", encoding="utf-8") as f:
                json.dump({"bijgewerkt": "2026-10-08T04:00:00+00:00", "items": [
                    {"id": "1", "titel": "Een AI-test", "categorie": "AI", "bron": "X", "taal": "en",
                     "datum": "2026-10-08", "samenvatting": "s", "url": "https://example.com/a"},
                    {"id": "2", "titel": "Een data-test", "categorie": "Data", "bron": "X", "taal": "en",
                     "datum": "2026-10-08", "samenvatting": "s", "url": "https://example.com/b"}]}, f)
            uit = os.path.join(t, "site")
            bouw.bouw(data, os.path.join(BASIS, "config", "feeds.json"), uit)
            h404 = open(os.path.join(uit, "404.html"), encoding="utf-8").read()
            self.assertIn("Pagina niet gevonden", h404)
            self.assertIn('href="index.html"', h404)
            self.assertNotIn('href="style.css"', h404)
            nieuws = open(os.path.join(uit, "nieuws.html"), encoding="utf-8").read()
            self.assertIn('placeholder="Zoek in nieuws"', nieuws)


if __name__ == "__main__":
    unittest.main()
