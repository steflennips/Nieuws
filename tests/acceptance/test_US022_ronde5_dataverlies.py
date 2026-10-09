"""Extra acceptatietests dataverlies en robuustheid, iteratie 8, Tester ronde 5.

Geen geschreven criteria: afgeleid van US-022 c4 (vangnet), c5 (configcontrole) en de dagelijkse job die
data/nieuws.json commit. Alle tests draaien tegen lokale testfeeds (127.0.0.1) en tijdelijke bestanden; de echte
data/nieuws.json en config/feeds.json worden alleen gelezen.

- R5-a (BLOKKEREND): items met een datum in een andere notatie (bijv. "2026-10-08T00:00:00") worden overgeslagen
  en vallen buiten het vangnet. Zo verdwijnt 86 van 87 items met exitcode 0. Verwacht: geen stille wipe.
- R5-b (BELANGRIJK): alle opgeslagen items van een naam die niet meer in de config staat (bijv. een spatie in de
  feednaam) verdwijnen zonder vangnet en zonder melding. Verwacht: geen stille wipe.
- R5-c..f (BELANGRIJK): configwaarden of opgeslagen items die de validatie passeren, geven een traceback:
  bewaar_dagen extreem groot, samenvatting als getal, bron als lijst, ongeldige re:-regex in weigertermen.
  Verwacht: geen traceback.
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

FEED_NAAM = "Lokale testfeed R5"
TW_GOED = {"BI": ["bikern"], "Data": ["datakern"], "Automatisering": ["autokern"], "AI": ["aikern"]}
RSS = ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>T</title>'
       '<item><title>bikern nieuw item van vandaag</title><link>%s/nieuw/1</link>'
       '<description>Nieuw item met een treffer.</description></item></channel></rss>')
ROUTES = {"/feed.xml": {"body": lambda base: (RSS % base).encode("utf-8")}}


def _item(i, dagen=1, **wijzig):
    x = {"id": "q%05d" % i, "titel": "bikern nummer %d" % i, "categorie": "BI", "bron": FEED_NAAM, "taal": "nl",
         "datum": hf.iso_dag(dagen), "samenvatting": "Testsamenvatting %d." % i,
         "url": "https://voorbeeld.example/r5/%05d" % i}
    x.update(wijzig)
    return x


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
        self.tmp = tempfile.mkdtemp(prefix="t8-r5-")
        self.data = os.path.join(self.tmp, "nieuws.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _schrijf_items(self, items):
        with open(self.data, "w", encoding="utf-8") as f:
            json.dump({"bijgewerkt": "2026-10-08T18:00:00+00:00", "feeds": [], "items": items}, f, ensure_ascii=False)

    def _aantal_na(self):
        with open(self.data, encoding="utf-8") as f:
            return len(json.load(f)["items"])

    def _draai(self, cfg, feed_naam=FEED_NAAM):
        pad = os.path.join(self.tmp, "config.json")
        with hf.FeedServer(ROUTES) as srv:
            feeds = [{"naam": feed_naam, "url": srv.url("/feed.xml"), "taal": "nl"}]
            with open(pad, "w", encoding="utf-8") as f:
                json.dump(_config(feeds, **cfg), f, ensure_ascii=False)
            return hf.run_ophalen(pad, self.data)


class TestR5DatumEnBronWegvallen(_Basis):
    def test_US022_extra_r5a_andere_datumnotatie_wist_niet_stil_86_van_87(self):
        """Extra (Tester it. 8 ronde 5, dataverlies, BLOKKEREND): 87 opgeslagen items met datum
        "JJJJ-MM-DDT00:00:00" worden allemaal overgeslagen (met waarschuwing) en vallen buiten het vangnet;
        het bestand wordt geschreven met 1 item en exitcode 0. Verwacht: exitcode != 0 en bestand ongewijzigd,
        of minstens de helft blijft staan."""
        items = [_item(i, 1, datum=hf.iso_dag(1) + "T00:00:00") for i in range(87)]
        self._schrijf_items(items)
        voor = _sha(self.data)
        res = self._draai({})
        uit = res.stdout + res.stderr
        self.assertNotIn("Traceback", uit, uit)
        na = self._aantal_na()
        self.assertTrue((res.returncode != 0 and _sha(self.data) == voor) or na >= 44,
                        "stil weggeschreven: exitcode %d, %d van 87 items over" % (res.returncode, na))

    def test_US022_extra_r5b_bronnaam_van_alle_items_gewijzigd_wist_niet_stil(self):
        """Extra (ronde 5, BELANGRIJK; ontwerpvraag PO): alle 87 opgeslagen items hebben een bronnaam die niet
        (exact) in de config staat, bijv. door een spatie in de feednaam. Ze verdwijnen zonder vangnet (niet
        geteld) en de log meldt "0 ouder dan ... verwijderd". Verwacht: exitcode != 0 en bestand ongewijzigd,
        of minstens de helft blijft staan."""
        items = [_item(i, 1, bron="Testfeed R5 oud") for i in range(87)]
        self._schrijf_items(items)
        voor = _sha(self.data)
        res = self._draai({})
        uit = res.stdout + res.stderr
        self.assertNotIn("Traceback", uit, uit)
        na = self._aantal_na()
        self.assertTrue((res.returncode != 0 and _sha(self.data) == voor) or na >= 44,
                        "stil weggeschreven: exitcode %d, %d van 87 items over (log: %s)"
                        % (res.returncode, na, res.stdout.strip()[-200:]))


class TestR5TracebackOpConfigEnOpslag(_Basis):
    def _geen_traceback(self, res, naam):
        uit = res.stdout + res.stderr
        self.assertNotIn("Traceback", uit, "%s geeft een traceback:\n%s" % (naam, uit[-800:]))

    def test_US022_extra_r5c_bewaar_dagen_extreem_groot_geen_traceback(self):
        """Extra (ronde 5, BELANGRIJK): bewaar_dagen 1000000 passeert de validatie (geheel getal >= 1) maar geeft
        een OverflowError in de datumberekening (traceback, exitcode 1). Verwacht: geen traceback."""
        self._schrijf_items([_item(i, 1) for i in range(5)])
        res = self._draai({"bewaar_dagen": 1000000})
        self._geen_traceback(res, "bewaar_dagen 1000000")

    def test_US022_extra_r5d_samenvatting_als_getal_geen_traceback(self):
        """Extra (ronde 5, BELANGRIJK): opgeslagen item met samenvatting 5 (geen tekst) geeft een AttributeError
        (traceback). Verwacht: geen traceback (overslaan met waarschuwing of tekst maken)."""
        items = [_item(i, 1) for i in range(5)] + [_item(50, 1, samenvatting=5)]
        self._schrijf_items(items)
        res = self._draai({})
        self._geen_traceback(res, "samenvatting als getal")

    def test_US022_extra_r5e_bron_als_lijst_geen_traceback(self):
        """Extra (ronde 5, BELANGRIJK): opgeslagen item met bron als lijst geeft een TypeError (traceback) bij de
        controle op bekende bronnen. Verwacht: geen traceback."""
        items = [_item(i, 1) for i in range(5)] + [_item(51, 1, bron=["Testfeed R5"])]
        self._schrijf_items(items)
        res = self._draai({})
        self._geen_traceback(res, "bron als lijst")

    def test_US022_extra_r5f_ongeldige_regex_in_weigertermen_geen_traceback(self):
        """Extra (ronde 5, BELANGRIJK): een ongeldige re:-regex in weigertermen (bijv. "re:([") passeert de
        configcontrole en geeft een traceback (re.error) bij het ophalen. Verwacht: exitcode 2 met Nederlandse
        melding of geen traceback; bestand ongewijzigd."""
        self._schrijf_items([_item(i, 1) for i in range(5)])
        voor = _sha(self.data)
        res = self._draai({"weigertermen": ["re:(["]})
        self._geen_traceback(res, "ongeldige regex in weigertermen")
        self.assertEqual(_sha(self.data), voor, "data gewijzigd bij een ongeldige regex")


if __name__ == "__main__":
    unittest.main()
