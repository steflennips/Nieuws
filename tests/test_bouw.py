"""Eigen tests voor het bouwcommando (US-012) en het workflow-bestand (US-013 c2/c4/c5). Geen internet nodig."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "src"))
import bouw  # noqa: E402


def item(n, cat, titel, samen="Korte samenvatting"):
    return {"id": "id%d" % n, "titel": titel, "categorie": cat, "bron": "Testbron %s" % ("NL" if n % 2 else "EN"),
            "taal": "nl", "datum": "2026-10-0%d" % (n % 9 + 1), "samenvatting": samen,
            "url": "https://voorbeeld.test/a%d" % n}


ITEMS = [item(1, "AI", "Nieuwe chatbot <b>live</b> & klaar", "Over een chatbot"),
         item(2, "AI", "AI in de zorg", "x" * 400),
         item(3, "Data", "Dashboard met open data", "Met een dataset"),
         item(4, "Automatisering", "RPA bij de gemeente", "Workflow en RPA"),
         item(5, "Data", "Datakwaliteit", "Gegevens op orde"),
         item(6, "Data", "Machine learning basics", "Leer het"),
         item(7, "BI", "Nog een BI-bericht", "Meer BI")]
DATA = {"bijgewerkt": "2026-07-01T04:05:06+00:00", "feeds": [], "items": ITEMS}
CONFIG = {"feeds": [{"naam": "Testbron NL", "url": "https://nl.voorbeeld.test/feed/", "taal": "nl", "headnieuws": True},
                    {"naam": "Testbron EN", "url": "https://en.voorbeeld.test/rss", "taal": "en"}]}


class BouwTestBasis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        t = Path(cls.tmp.name)
        (t / "nieuws.json").write_text(json.dumps(DATA), encoding="utf-8")
        (t / "feeds.json").write_text(json.dumps(CONFIG), encoding="utf-8")
        cls.uit = t / "site"
        r = subprocess.run([sys.executable, str(BASIS / "src" / "bouw.py"), "--data", str(t / "nieuws.json"),
                            "--config", str(t / "feeds.json"), "--uit", str(cls.uit), "--vandaag", "2026-10-08"], capture_output=True, text=True)
        cls.rc, cls.out = r.returncode, r.stdout + r.stderr

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def lees(self, naam):
        return (self.uit / naam).read_text(encoding="utf-8")


class TestBouw(BouwTestBasis):
    def test_bouwt_statische_bestanden(self):
        self.assertEqual(self.rc, 0, self.out)
        for n in ("index.html", "nieuws.html", "bronnen.html", "style.css", "app.js", "favicon.ico", "favicon.svg"):
            self.assertTrue((self.uit / n).is_file(), n)

    def test_navigatie_precies_overzicht_en_nieuws(self):
        for n in ("index.html", "nieuws.html", "bronnen.html"):
            nav = re.search(r"<nav[^>]*>(.*?)</nav>", self.lees(n), re.S).group(1)
            self.assertEqual(re.findall(r">([^<]+)</a>", nav), ["Overzicht", "Nieuws"], n)
        self.assertIn('href="nieuws.html" aria-current="page"', self.lees("nieuws.html"))

    def test_geen_externe_bestanden(self):
        alles = " ".join(self.lees(n) for n in ("index.html", "nieuws.html", "bronnen.html", "app.js", "style.css")).lower()
        for woord in ("<img", "@import", "<iframe"):
            self.assertNotIn(woord, alles)
        for n in ("index.html", "nieuws.html", "bronnen.html"):
            for href in re.findall(r'(?:href|src)="([^"]+)"', self.lees(n)):
                self.assertFalse(href.startswith("/"), href)  # relatief, werkt onder /<repo>/
                if href.startswith("http"):  # alleen bronlinks (nieuws en bronnenlijst)
                    self.assertIn("voorbeeld.test", href)

    def test_item_met_bron_datum_link_en_samenvatting(self):
        h = self.lees("nieuws.html")
        self.assertIn("Bron: Testbron NL", h)
        self.assertIn('href="https://voorbeeld.test/a1" target="_blank" rel="noopener noreferrer"', h)
        self.assertIn("Nieuwe chatbot &lt;b&gt;live&lt;/b&gt; &amp; klaar", h)  # geescapet
        samenvattingen = re.findall(r"<p>([^<]*)</p></article>", h)
        self.assertEqual(len(samenvattingen), 7)
        for s in samenvattingen:
            self.assertLessEqual(len(s), 300)

    def test_nieuwste_eerst(self):
        h = self.lees("nieuws.html")
        datums = [int(m) for m in re.findall(r"<span>(\d+) okt 2026</span>", h)]
        self.assertEqual(len(datums), 7)
        self.assertEqual(datums, sorted(datums, reverse=True))

    def test_voet_op_elke_pagina(self):
        for n in ("index.html", "nieuws.html", "bronnen.html"):
            h = self.lees(n)
            self.assertIn("Laatst bijgewerkt: <time", h)
            self.assertIn("1 jul 2026 06:05", h)  # 04:05 UTC = 06:05 zomertijd
            self.assertIn("afkomstig van de genoemde bronnen", h)
            self.assertIn('<a href="bronnen.html">alle bronnen</a>', h)

    def test_bronnenlijst(self):
        h = self.lees("bronnen.html")
        self.assertIn("Testbron NL", h)
        self.assertIn("https://en.voorbeeld.test/", h)

    def test_bronnenlijst_bevat_ook_bron_buiten_config(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            data = dict(DATA, items=ITEMS + [dict(item(8, "AI", "Oud bericht"), bron="Verdwenen Blog <x>")])
            (t / "n.json").write_text(json.dumps(data), encoding="utf-8")
            (t / "f.json").write_text(json.dumps(CONFIG), encoding="utf-8")
            bouw.bouw(str(t / "n.json"), str(t / "f.json"), str(t / "s"))
            h = (t / "s" / "bronnen.html").read_text(encoding="utf-8")
        self.assertEqual(h.count("Verdwenen Blog &lt;x&gt;"), 1)
        self.assertEqual(h.count("Testbron NL"), 1)  # geen dubbelen
        # alle artikelen van deze bron staan op https://voorbeeld.test/, dus die link is afleidbaar
        regel = re.search(r'<li><a href="https://voorbeeld.test/"[^>]*>Verdwenen Blog &lt;x&gt;</a></li>', h)
        self.assertIsNotNone(regel)

    def test_tellers_en_vijf_nieuwste(self):
        h = self.lees("index.html")
        for cat, n in (("bi", 1), ("data", 3), ("automatisering", 1), ("ai", 2)):
            self.assertIn('id="teller-%s">%d<' % (cat, n), h)
        uit = re.search(r'id="blok-uitgelicht".*?</section>', h, re.S).group(0)
        vak = re.search(r'id="blok-nieuws".*?</section>', h, re.S).group(0)
        self.assertEqual(uit.count("<li>"), 2)  # alleen headnieuws-feed (Testbron NL), laatste 3 dagen: items 5 en 7
        self.assertEqual(vak.count("<li>"), 5)  # de 5 nieuwste overige items
        self.assertNotIn("in totaal", h)
        self.assertIn("Alle 7 berichten bekijken", h)

    def test_nl_tijd_zomer_en_winter(self):
        self.assertEqual(bouw.nl_tijd(datetime(2026, 7, 1, 4, 0, tzinfo=timezone.utc)).hour, 6)
        self.assertEqual(bouw.nl_tijd(datetime(2026, 12, 1, 5, 0, tzinfo=timezone.utc)).hour, 6)
        self.assertEqual(bouw.nl_tijd(datetime(2026, 3, 29, 0, 59, tzinfo=timezone.utc)).hour, 1)
        self.assertEqual(bouw.nl_tijd(datetime(2026, 3, 29, 1, 0, tzinfo=timezone.utc)).hour, 3)
        self.assertEqual(bouw.nl_tijd(datetime(2026, 10, 25, 0, 59, tzinfo=timezone.utc)).hour, 2)
        self.assertEqual(bouw.nl_tijd(datetime(2026, 10, 25, 1, 0, tzinfo=timezone.utc)).hour, 2)

    def test_favicon_is_geldige_ico(self):
        d = (self.uit / "favicon.ico").read_bytes()
        self.assertEqual(d[:4], b"\x00\x00\x01\x00")

    def test_zonder_data_foutmelding_en_niets_gebouwd(self):
        with tempfile.TemporaryDirectory() as t:
            r = subprocess.run([sys.executable, str(BASIS / "src" / "bouw.py"), "--data", os.path.join(t, "weg.json"),
                                "--uit", os.path.join(t, "site")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("FOUT", r.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "site")))


class TestWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wf = (BASIS / ".github" / "workflows" / "nieuws.yml").read_text(encoding="utf-8")

    def test_dagelijks_rond_zes_uur_nl_en_handmatig(self):
        m = re.search(r'cron:\s*"(\d+) (\d+) \* \* \*"', self.wf)
        self.assertIsNotNone(m)
        self.assertIn(int(m.group(2)), (4, 5))  # 04:00 UTC = 06:00 zomertijd, 05:00 UTC = 06:00 wintertijd
        self.assertIn("workflow_dispatch", self.wf)

    def test_job_haalt_op_bouwt_en_publiceert(self):
        i1, i2, i3 = (self.wf.index(x) for x in ("src/ophalen.py", "src/bouw.py", "deploy-pages"))
        self.assertTrue(i1 < i2 < i3)
        self.assertIn("upload-pages-artifact", self.wf)

    def test_geen_eigen_geheimen(self):
        self.assertNotIn("secrets.", self.wf)  # alleen de automatische GITHUB_TOKEN wordt gebruikt


class TestGeenGeheimen(unittest.TestCase):
    def test_repo_bevat_geen_sleutels(self):
        patroon = re.compile("ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|"
                             "(?i:(password|passwd|secret|api[_-]?key|token)\\s*[:=]\\s*[\"'][^\"']{6,})")
        for pad in BASIS.rglob("*"):
            if not pad.is_file() or any(d in pad.parts for d in (".git", "__pycache__", "site", "node_modules")):
                continue
            if pad.suffix not in (".py", ".json", ".yml", ".yaml", ".md", ".txt", ".html", ".js", ".css"):
                continue
            if pad.name == "test_bouw.py":
                continue  # bevat het zoekpatroon zelf
            self.assertIsNone(patroon.search(pad.read_text(encoding="utf-8", errors="ignore")), str(pad))


if __name__ == "__main__":
    unittest.main()
