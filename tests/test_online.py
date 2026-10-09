"""Voorbereiding online zetten (US-013): verse checkout, subpad /<repo>/, veiligheidscontrole. Geen internet nodig."""
import json
import os
import re
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "src"))
import bouw  # noqa: E402
import ophalen  # noqa: E402
import veilig_check  # noqa: E402

RSS = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>T</title>
<item><title>Nieuwe AI chatbot</title><link>https://bron.test/a1</link><description>Over AI en data</description>
<pubDate>Wed, 07 Oct 2026 10:00:00 GMT</pubDate></item></channel></rss>"""
CFG = {"user_agent": "Test/1.0", "bewaar_dagen": 60, "feeds": [{"naam": "Bron", "url": "https://bron.test/feed", "taal": "en"}],
       "trefwoorden": {"AI": ["AI"], "Data": ["data"], "Automatisering": ["automatisering"]}}
NU = datetime(2026, 10, 8, 4, 0, tzinfo=timezone.utc)


class TestVerseCheckout(unittest.TestCase):
    """De workflow-stappen ophalen -> bouwen op een checkout zonder (of met leeg) data/nieuws.json."""

    def _run(self, voorbereiding):
        with tempfile.TemporaryDirectory() as t:
            data = os.path.join(t, "data", "nieuws.json")
            voorbereiding(t, data)
            self.assertEqual(ophalen.draai(CFG, data, controleer_robots=False, lees=lambda u, a, to: RSS, nu=NU, log=lambda *_: None), 0)
            cfgp = os.path.join(t, "feeds.json")
            Path(cfgp).write_text(json.dumps(CFG), encoding="utf-8")
            uit = os.path.join(t, "site")
            n, _ = bouw.bouw(data, cfgp, uit)
            self.assertEqual(n, 1)
            html = Path(uit, "index.html").read_text(encoding="utf-8")
            self.assertIn("Nieuwe AI chatbot", html)
            self.assertNotIn("voorbeeld", html.lower().replace("voorbeeldcode", ""))

    def test_zonder_data_map(self):
        self._run(lambda t, d: None)

    def test_met_leeg_bestand(self):
        def v(t, d):
            os.makedirs(os.path.dirname(d))
            open(d, "w").close()
        self._run(v)

    def test_geen_data_en_geen_feeds_publiceert_niets(self):
        with tempfile.TemporaryDirectory() as t:
            data = os.path.join(t, "data", "nieuws.json")
            def kapot(u, a, to):
                raise OSError("geen internet")
            self.assertEqual(ophalen.draai(CFG, data, controleer_robots=False, lees=kapot, nu=NU, log=lambda *_: None), 1)
            with self.assertRaises(ValueError):
                bouw.bouw(data, str(BASIS / "config" / "feeds.json"), os.path.join(t, "site"))
            self.assertFalse(os.path.exists(os.path.join(t, "site", "index.html")))


class TestSubpad(unittest.TestCase):
    PREFIX = "/mijn-repo/"

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        t = cls.tmp.name
        items = [{"id": "1", "titel": "AI nieuws", "url": "https://bron.test/a", "categorie": "AI", "bron": "Bron",
                  "taal": "en", "datum": "2026-10-07", "samenvatting": "x"},
                 {"id": "2", "titel": "Data nieuws", "url": "https://bron.test/b", "categorie": "Data", "bron": "Bron",
                  "taal": "en", "datum": "2026-10-07", "samenvatting": "x"}]
        Path(t, "d.json").write_text(json.dumps({"bijgewerkt": "2026-10-08T04:00:00+00:00", "items": items}), encoding="utf-8")
        Path(t, "c.json").write_text(json.dumps({"feeds": [{"naam": "Bron", "url": "https://bron.test/feed", "taal": "en"}]}), encoding="utf-8")
        cls.site = os.path.join(t, "site")
        bouw.bouw(os.path.join(t, "d.json"), os.path.join(t, "c.json"), cls.site)
        prefix, site = cls.PREFIX, cls.site

        class H(SimpleHTTPRequestHandler):
            def translate_path(self, path):
                if not path.startswith(prefix):
                    return os.path.join(site, "__bestaat_niet__")
                return super().translate_path("/" + path[len(prefix):])
            def log_message(self, *a):
                pass
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(H, directory=site))
        cls.poort = cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        cls.tmp.cleanup()

    def url(self, pad):
        return "http://127.0.0.1:%d%s" % (self.poort, pad)

    def test_alle_interne_links_en_bronnen_werken_onder_subpad(self):
        gezien, todo = set(), [self.url(self.PREFIX)]
        while todo:
            u = todo.pop()
            if u in gezien:
                continue
            gezien.add(u)
            with urlopen(u) as r:
                self.assertEqual(r.status, 200, u)
                tekst = r.read().decode("utf-8", "ignore") if u.endswith(("/", ".html", ".css", ".js")) else ""
            for m in re.finditer(r'(?:href|src)="([^"#]+)', tekst):
                ref = m.group(1)
                if ref.startswith(("http:", "https:", "mailto:", "javascript:")):
                    continue
                self.assertFalse(ref.startswith("/"), "absolute link %s in %s" % (ref, u))
                todo.append(urljoin(u, ref.split("?")[0]))
        namen = {urlparse(u).path.rsplit("/", 1)[-1] for u in gezien}
        for n in ("index.html", "nieuws.html", "bronnen.html", "style.css", "app.js", "favicon.svg"):
            self.assertIn(n, namen)

    def test_favicon_ico_en_404(self):
        with urlopen(self.url(self.PREFIX + "favicon.ico")) as r:
            self.assertEqual(r.status, 200)
        html = Path(self.site, "404.html").read_text(encoding="utf-8")
        self.assertIn("github[.]io", html)  # <base> voor diepe 404-paden op GitHub Pages
        with self.assertRaises(HTTPError) as c:
            urlopen(self.url(self.PREFIX + "bestaat-niet.html"))
        self.assertEqual(c.exception.code, 404)


class TestBronnenLink(unittest.TestCase):
    def test_link_alleen_bij_eenduidige_site(self):
        def it(n, bron, url):
            return {"id": str(n), "titel": "t%d" % n, "url": url, "categorie": "Data", "bron": bron, "datum": "2026-10-07"}
        items = [it(1, "Eén", "https://een.test/a"), it(2, "Eén", "https://een.test/b"),
                 it(3, "Twee", "https://x.test/a"), it(4, "Twee", "https://y.test/a"), it(5, "Drie", "http://drie.test/a")]
        with tempfile.TemporaryDirectory() as t:
            Path(t, "d.json").write_text(json.dumps({"items": items}), encoding="utf-8")
            Path(t, "c.json").write_text(json.dumps({"feeds": []}), encoding="utf-8")
            bouw.bouw(os.path.join(t, "d.json"), os.path.join(t, "c.json"), os.path.join(t, "s"))
            html = Path(t, "s", "bronnen.html").read_text(encoding="utf-8")
        self.assertIn('<a href="https://een.test/"', html)
        self.assertIn("<li>Twee</li>", html)
        self.assertIn("<li>Drie</li>", html)


class TestVeiligCheck(unittest.TestCase):
    def test_vangt_pad_mail_en_sleutel(self):
        soorten = {s for _, s in veilig_check.scan_tekst(
            "pad C:" + chr(92) + "Users" + chr(92) + "x en mail a.b@voorbeeld.nl en password=abcdefgh1234 en ghp_" + "A" * 36)}
        for s in ("lokaal pad (Windows-gebruikersmap)", "e-mailadres", "wachtwoord/sleutel in toekenning", "GitHub-token"):
            self.assertIn(s, soorten)

    def test_bot_noreply_en_gewone_tekst_ok(self):
        self.assertEqual(veilig_check.scan_tekst("41898282+github-actions[bot]@users.noreply.github.com, token prices, https://a.nl/x/y"), [])

    def test_verdachte_namen(self):
        r = veilig_check.controleer(["NTUSER.DAT", ".claude.json", "sub/.env"])
        self.assertEqual(len(r), 3)

    def test_gitignore_sluit_site_en_ntuser_uit(self):
        pats = veilig_check._lees_gitignore()
        for rel in ("site/index.html", "NTUSER.DAT", "src/__pycache__/x.pyc"):
            self.assertTrue(veilig_check.genegeerd(rel, pats), rel)
        self.assertFalse(veilig_check.genegeerd("data/nieuws.json", pats))
        self.assertFalse(veilig_check.genegeerd("docs/STATUS.md", pats))


if __name__ == "__main__":
    unittest.main()
