"""Extra acceptatietests dataverlies en configcontrole, iteratie 8, Tester ronde 4.

Geen geschreven criteria: afgeleid van US-022 c4 (vangnet) en c5 (configcontrole) en van de dagelijkse job die
data/nieuws.json commit. Alle tests draaien tegen lokale testfeeds (127.0.0.1) en tijdelijke bestanden; de echte
data/nieuws.json en config/feeds.json worden alleen gelezen.

- R4-a (BLOKKEREND-kandidaat): een config met bewaar_dagen 6 (typo voor 60) mag 90% van de opgeslagen items niet
  stil wegschrijven (geen vangnet voor de leeftijdsopruiming). Verwacht: exitcode != 0 en het bestand ongewijzigd,
  of minstens de helft blijft staan.
- R4-b (BELANGRIJK): bewaar_dagen 0 of tekst: exitcode 2, Nederlandse melding, geen traceback, data ongewijzigd.
- R4-c (BELANGRIJK): een opgeslagen item zonder datum of id (geldige JSON) geeft geen traceback.
- R4-d (positief): een mislukte schrijfactie (surrogaat in een opgeslagen item) laat het oorspronkelijke bestand
  byte-gelijk; atomair schrijven via .tmp en os.replace.
"""
import sys
sys.dont_write_bytecode = True  # geen __pycache__ in src/ of tests/

import copy
import hashlib
import json
import os
import shutil
import tempfile
import unittest

import hulp_feeds as hf

FEED_NAAM = "Lokale testfeed R4"
TW_GOED = {"BI": ["bikern"], "Data": ["datakern"], "Automatisering": ["autokern"], "AI": ["aikern"]}
RSS = ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>T</title>'
       '<item><title>bikern nieuw item van vandaag</title><link>%s/nieuw/1</link>'
       '<description>Nieuw item met een treffer.</description></item></channel></rss>')
ROUTES = {"/feed.xml": {"body": lambda base: (RSS % base).encode("utf-8")}}


def _item(i, dagen, titel="bikern nummer"):
    return {"id": "r%05d" % i, "titel": "%s %d" % (titel, i), "categorie": "BI", "bron": FEED_NAAM, "taal": "nl",
            "datum": hf.iso_dag(dagen), "samenvatting": "Testsamenvatting %d." % i,
            "url": "https://voorbeeld.example/r4/%05d" % i}


def _sha(pad):
    with open(pad, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _config(feeds, **wijzigingen):
    cfg = copy.deepcopy(hf.project_config())
    cfg["feeds"] = feeds
    cfg["trefwoorden"] = copy.deepcopy(TW_GOED)
    cfg["uitsluitingen"] = []
    cfg["weigertermen"] = []
    cfg["weigertermen_samenvatting"] = []
    cfg["weiger_uitzonderingen"] = []
    cfg.update(wijzigingen)
    return cfg


class _Basis(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="t8-r4-")
        self.data = os.path.join(self.tmp, "nieuws.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _schrijf_config(self, cfg):
        pad = os.path.join(self.tmp, "config.json")
        with open(pad, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        return pad

    def _schrijf_items(self, items):
        with open(self.data, "w", encoding="utf-8") as f:
            json.dump({"bijgewerkt": "2026-10-08T18:00:00+00:00", "feeds": [], "items": items}, f, ensure_ascii=False)

    def _draai(self, cfg):
        with hf.FeedServer(ROUTES) as srv:
            feeds = [{"naam": FEED_NAAM, "url": srv.url("/feed.xml"), "taal": "nl"}]
            return hf.run_ophalen(self._schrijf_config(_config(feeds, **cfg)), self.data)


class TestR4BewaarDagen(_Basis):
    def setUp(self):
        super().setUp()
        self.items = [_item(i, 1) for i in range(10)] + [_item(100 + i, 30) for i in range(90)]
        self._schrijf_items(self.items)
        self.hash_voor = _sha(self.data)

    def test_US022_extra_r4a_bewaar_dagen_typo_wist_niet_stil_90_procent(self):
        """Extra (Tester it. 8 ronde 4, dataverlies, BLOKKEREND-kandidaat): bewaar_dagen 6 i.p.v. 60 verwijdert
        90 van 100 opgeslagen items zonder vangnet en met exitcode 0; de dagelijkse job commit dat. Verwacht: geen
        stille wipe: exitcode != 0 en bestand ongewijzigd, of minstens de helft blijft staan."""
        res = self._draai({"bewaar_dagen": 6})
        uit = res.stdout + res.stderr
        self.assertNotIn("Traceback", uit, uit)
        with open(self.data, encoding="utf-8") as f:
            na = len(json.load(f)["items"])
        self.assertTrue((res.returncode != 0 and _sha(self.data) == self.hash_voor) or na >= 50,
                        "stil weggeschreven: exitcode %d, %d van 100 items over (bewaar_dagen 6)" % (res.returncode, na))

    def test_US022_extra_r4b_bewaar_dagen_nul_is_configfout(self):
        res = self._draai({"bewaar_dagen": 0})
        uit = res.stdout + res.stderr
        self.assertEqual(res.returncode, 2, uit)
        self.assertNotIn("Traceback", uit, uit)
        self.assertEqual(_sha(self.data), self.hash_voor, "data gewijzigd bij bewaar_dagen 0")

    def test_US022_extra_r4b_bewaar_dagen_tekst_is_configfout(self):
        res = self._draai({"bewaar_dagen": "60"})
        uit = res.stdout + res.stderr
        self.assertEqual(res.returncode, 2, uit)
        self.assertNotIn("Traceback", uit, uit)
        self.assertEqual(_sha(self.data), self.hash_voor, "data gewijzigd bij bewaar_dagen als tekst")


class TestR4OnvolledigOpgeslagenItem(_Basis):
    def test_US022_extra_r4c_item_zonder_datum_geen_traceback(self):
        """Extra (ronde 4, BELANGRIJK): geldige JSON met een opgeslagen item zonder datum geeft nu een traceback
        (KeyError/TypeError in draai). Verwacht: nette afhandeling, geen traceback."""
        items = [_item(i, 1) for i in range(5)]
        zonder = _item(50, 1, titel="bikern zonder datum")
        del zonder["datum"]
        items.append(zonder)
        self._schrijf_items(items)
        res = self._draai({})
        uit = res.stdout + res.stderr
        self.assertNotIn("Traceback", uit, uit)

    def test_US022_extra_r4c_item_zonder_id_geen_traceback(self):
        items = [_item(i, 1) for i in range(5)]
        zonder = _item(51, 1, titel="bikern zonder id")
        del zonder["id"]
        items.append(zonder)
        self._schrijf_items(items)
        res = self._draai({})
        uit = res.stdout + res.stderr
        self.assertNotIn("Traceback", uit, uit)


class TestR4AtomairSchrijven(_Basis):
    def test_US022_extra_r4d_mislukte_schrijfactie_laat_origineel_intact(self):
        """Positief (ronde 4): een opgeslagen item met een surrogaat (\\ud800 als JSON-escape) laat het schrijven
        halverwege mislukken; het oorspronkelijke bestand moet byte-gelijk blijven en exitcode != 0 zijn."""
        raw = ('{"items": [{"titel": "bikern rapportage \\ud800 test", "url": "https://voorbeeld.example/r4/s1", '
               '"bron": "%s", "datum": "%s", "categorie": "BI", "id": "sssssssssss1", '
               '"samenvatting": "bikern data."}]}' % (FEED_NAAM, hf.iso_dag(1)))
        with open(self.data, "wb") as f:
            f.write(raw.encode("ascii"))
        voor = _sha(self.data)
        res = self._draai({})
        self.assertNotEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertEqual(_sha(self.data), voor, "oorspronkelijk bestand gewijzigd bij mislukte schrijfactie")


if __name__ == "__main__":
    unittest.main()
