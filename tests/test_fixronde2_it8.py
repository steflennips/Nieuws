"""Fixronde 2 iteratie 8 (US-022 c3, c4, c5): configvalidatie en vangnet tegen het wissen van opgeslagen nieuws.
Geen internet: een lokale testfeed op 127.0.0.1."""
import io
import json
import os
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import ophalen  # noqa: E402

NU = datetime(2026, 10, 8, 12, 0, tzinfo=timezone.utc)
RSS = ('<?xml version="1.0"?><rss version="2.0"><channel><item><title>Nieuwe AI-assistent</title>'
       '<link>http://x.test/nieuw1</link><description>x</description>'
       '<pubDate>Wed, 07 Oct 2026 09:00:00 +0200</pubDate></item></channel></rss>')
TW = {"BI": ["power bi"], "Data": ["data"], "Automatisering": ["workflow*"], "AI": ["ai"]}


class _H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(RSS.encode())

    def log_message(self, *a):
        pass


def item(n, bron, goed):
    return {"id": "i%s%d" % (bron, n), "titel": ("AI-nieuws %d" % n) if goed else ("Recept %d" % n),
            "samenvatting": "x", "datum": "2026-10-05", "bron": bron, "taal": "nl",
            "url": "http://x.test/%s/%d" % (bron, n), "categorie": "AI"}


class Basis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), _H)
        cls.base = "http://127.0.0.1:%d/rss" % cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.uitvoer = os.path.join(self.tmp.name, "nieuws.json")

    def tearDown(self):
        self.tmp.cleanup()

    def cfg(self, **extra):
        c = {"user_agent": "T/1", "trefwoorden": json.loads(json.dumps(TW)),
             "feeds": [{"naam": "R", "url": self.base, "taal": "nl"}]}
        c.update(extra)
        return c

    def bewaar(self, items):
        with open(self.uitvoer, "w", encoding="utf-8") as f:
            json.dump({"bijgewerkt": "x", "feeds": [], "items": items}, f)

    def bytes_uitvoer(self):
        with open(self.uitvoer, "rb") as f:
            return f.read()

    def main(self, cfg, extra=(), ruw=None):
        pad = os.path.join(self.tmp.name, "c.json")
        with open(pad, "wb") as f:
            f.write(ruw if ruw is not None else json.dumps(cfg).encode("utf-8"))
        err, out = io.StringIO(), io.StringIO()
        with redirect_stderr(err), redirect_stdout(out):
            code = ophalen.main(["--config", pad, "--uitvoer", self.uitvoer, "--geen-robots"] + list(extra))
        return code, err.getvalue() + out.getvalue()


class TestTrefwoordCategorieen(Basis):
    def test_ongeldige_trefwoorden_geven_exit_2_en_laten_bestand_intact(self):
        self.bewaar([item(i, "R", True) for i in range(5)])
        voor = self.bytes_uitvoer()
        gevallen = [
            ({}, None),
            ({"BI": ["power bi"], "Data": ["data"], "Automatisering": ["workflow*"], "Ai": ["ai"]}, "AI"),
            ({**TW, "Data": []}, "Data"),
            ({**TW, "BI": ["power bi", ""]}, "BI"),
            ({**TW, "Automatisering": ["  "]}, "Automatisering"),
        ]
        for tw, cat in gevallen:
            code, uit = self.main(self.cfg(trefwoorden=tw))
            self.assertEqual(code, 2, tw)
            self.assertNotIn("Traceback", uit)
            self.assertIn("categorie", uit)
            if cat:
                self.assertIn('"%s"' % cat, uit)
            self.assertEqual(self.bytes_uitvoer(), voor)

    def test_geldige_config_blijft_werken(self):
        code, _ = self.main(self.cfg())
        self.assertEqual(code, 0)


class TestVangnet(Basis):
    def _run(self, weg, totaal=100, extra=(), vreemd=0):
        items = [item(i, "R", i >= weg) for i in range(totaal)] + [item(i, "Onbekend", False) for i in range(vreemd)]
        self.bewaar(items)
        voor = self.bytes_uitvoer()
        code, uit = self.main(self.cfg(), extra)
        return code, uit, voor

    def test_precies_50_procent_wordt_geschreven(self):
        code, uit, voor = self._run(50)
        self.assertEqual(code, 0, uit)
        namen = [i["titel"] for i in json.loads(self.bytes_uitvoer())["items"]]
        self.assertFalse(any(t.startswith("Recept") for t in namen))

    def test_51_procent_wordt_geweigerd(self):
        code, uit, voor = self._run(51)
        self.assertEqual(code, 1)
        self.assertIn("51 van de 100", uit)
        self.assertIn("--forceer-opruimen", uit)
        self.assertNotIn("Traceback", uit)
        self.assertEqual(self.bytes_uitvoer(), voor)

    def test_forceer_opruimen_schrijft_wel(self):
        code, uit, voor = self._run(51, extra=["--forceer-opruimen"])
        self.assertEqual(code, 0, uit)
        self.assertNotEqual(self.bytes_uitvoer(), voor)

    def test_items_van_niet_geconfigureerde_bron_tellen_niet_mee(self):
        # 100 items van R (alle goed) + 300 van een bron die niet in de config staat: wordt verwijderd, geen vangnet.
        code, uit, _ = self._run(0, vreemd=300)
        self.assertEqual(code, 0, uit)
        bronnen = {i["bron"] for i in json.loads(self.bytes_uitvoer())["items"]}
        self.assertEqual(bronnen, {"R"})

    def test_gewone_ronde_zonder_verwijderingen(self):
        code, uit, _ = self._run(0)
        self.assertEqual(code, 0, uit)

    def test_leeg_bestand_geen_vangnet(self):
        code, uit = self.main(self.cfg())
        self.assertEqual(code, 0, uit)


class TestConfigOverig(Basis):
    def _fout(self, cfg, melding):
        self.bewaar([item(1, "R", True)])
        voor = self.bytes_uitvoer()
        code, uit = self.main(cfg)
        self.assertEqual(code, 2, uit)
        self.assertIn(melding, uit)
        self.assertNotIn("Traceback", uit)
        self.assertEqual(self.bytes_uitvoer(), voor)

    def test_bom_wordt_gelezen(self):
        ruw = b"\xef\xbb\xbf" + json.dumps(self.cfg()).encode("utf-8")
        code, uit = self.main(None, ruw=ruw)
        self.assertEqual(code, 0, uit)

    def test_lijstvelden_moeten_lijst_van_tekst_zijn(self):
        for veld in ("uitsluitingen", "weigertermen", "weiger_uitzonderingen", "weigertermen_samenvatting"):
            for waarde in ("tekst", [1], {"a": "b"}, 5):
                self._fout(self.cfg(**{veld: waarde}), veld)

    def test_url_moet_http_of_https_zijn(self):
        for url in ("file:///c:/x.xml", "ftp://x.test/a", "x.test/feed"):
            c = self.cfg()
            c["feeds"][0]["url"] = url
            self._fout(c, "http://")

    def test_lege_feedlijst(self):
        self._fout(self.cfg(feeds=[]), "geen feeds ingesteld")


class TestWorkflow(unittest.TestCase):
    def test_workflow_gebruikt_forceer_opruimen_niet(self):
        pad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".github", "workflows")
        for naam in os.listdir(pad):
            with open(os.path.join(pad, naam), encoding="utf-8") as f:
                self.assertNotIn("forceer-opruimen", f.read(), naam)


if __name__ == "__main__":
    unittest.main()
