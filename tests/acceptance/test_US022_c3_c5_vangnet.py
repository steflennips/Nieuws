"""Acceptatietests US-022 c3-c5 (configuratiecontrole en vangnet), iteratie 8, Tester ronde 3.

- c3: trefwoorden moeten de vier categorieen BI, Data, Automatisering, AI bevatten, elk een niet-lege lijst van
  niet-lege termen. Anders exitcode 2, Nederlandse melding, data/nieuws.json byte-gelijk. Het dataverlies uit
  ronde 2 (foutieve config + een bereikbare feed) wordt gereproduceerd.
- c4: vangnet. Verwijdert de herindeling meer dan 50% van de opgeslagen items van geconfigureerde bronnen, dan
  wordt niets weggeschreven, exitcode 1, melding met aantallen en --forceer-opruimen. 50% wordt geschreven,
  51% niet. Feedruil telt niet mee. Een gewone ronde wordt niet geblokkeerd. De workflow gebruikt de optie niet.
- c5: UTF-8 met BOM wordt gelezen; lijstvelden moeten lijsten van tekst zijn; feed-url alleen http(s);
  "feeds": [] geeft de melding "geen feeds ingesteld". Exitcode 2, Nederlands, geen traceback, data ongewijzigd.

Geen internet: de feeds zijn lokale testfeeds op 127.0.0.1 (hulp_feeds.FeedServer). Alle bestanden staan in een
tijdelijke map. De echte data (data/nieuws.json) en config/feeds.json worden alleen gelezen en gekopieerd.
Geen wijziging van criteria om te slagen: de criteria zijn de maatstaf.
"""
import sys
sys.dont_write_bytecode = True  # geen __pycache__ in src/ of tests/

import copy
import hashlib
import json
import os
import re
import shutil
import tempfile
import unittest

import hulp_feeds as hf

ROOT = hf.ROOT
ECHTE_DATA = hf.NIEUWS_JSON
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "nieuws.yml")
FEED_NAAM = "Lokale testfeed"
# Zelfde trefwoordenset in elke test (vaste, lokale matching); de echte trefwoorden staan in config/feeds.json.
TW_GOED = {"BI": ["bikern"], "Data": ["datakern"], "Automatisering": ["autokern"], "AI": ["aikern"]}
# Engelse OS-tekst of traceback die niet in een melding mag staan.
ENGELS_OF_TRACEBACK = re.compile(
    r"Traceback|Errno|No such file|Expecting|Invalid|decode|line \d+ column|Permission denied|not found|"
    r"Illegal|byte 0x", re.I)


def _rss_zonder_trefwoord(base):
    return ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>T</title>'
            '<item><title>Gewone tekst zonder woord uit de lijst</title><link>%s/leeg/1</link>'
            '<description>Niets bijzonders.</description></item></channel></rss>' % base)


def _rss_met_trefwoord(base):
    return ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>T</title>'
            '<item><title>bikern uit de feed van vandaag</title><link>%s/nieuw/1</link>'
            '<description>Nieuw item met een treffer.</description></item></channel></rss>' % base)


ROUTES = {
    "/feed.xml": {"body": _rss_zonder_trefwoord},
    "/nieuw.xml": {"body": _rss_met_trefwoord},
}


def _item(i, bron, titel):
    return {"id": "t%05d" % i, "titel": titel, "categorie": "BI", "bron": bron, "taal": "en",
            "datum": hf.iso_dag(1), "samenvatting": "Testsamenvatting nummer %d." % i,
            "url": "https://voorbeeld.example/us022/%05d" % i}


def _schrijf_data(pad, items):
    with open(pad, "w", encoding="utf-8") as f:
        json.dump({"bijgewerkt": "2026-10-08T18:00:00+00:00", "feeds": [], "items": items}, f, ensure_ascii=False)
    return pad


def _sha(pad):
    with open(pad, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _basis_config(feeds, **wijzigingen):
    """Projectconfig met lokale feeds en een vaste, lege weigerlijst (deterministisch)."""
    cfg = copy.deepcopy(hf.project_config())
    cfg["feeds"] = feeds
    cfg["trefwoorden"] = copy.deepcopy(TW_GOED)
    cfg["uitsluitingen"] = []
    cfg["weigertermen"] = []
    cfg["weigertermen_samenvatting"] = []
    cfg["weiger_uitzonderingen"] = []
    cfg.update(wijzigingen)
    return cfg


def _schrijf_json(pad, obj, enc="utf-8"):
    with open(pad, "w", encoding=enc) as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))
    return pad


def _lees_items(pad):
    with open(pad, encoding="utf-8") as f:
        return json.load(f)["items"]


class _Basis(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="t8-c3c5-")
        self.data = os.path.join(self.tmp, "nieuws.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _config(self, cfg, naam="config.json", enc="utf-8"):
        return _schrijf_json(os.path.join(self.tmp, naam), cfg, enc)

    def _draai(self, config, extra=()):
        return hf.run_ophalen(config, self.data, list(extra))

    def _uitkomst(self, res):
        return res.stdout + res.stderr


class TestUS022C3Trefwoorden(_Basis):
    def setUp(self):
        super().setUp()
        _schrijf_data(self.data, [_item(i, FEED_NAAM, "bikern nummer %d" % i) for i in range(87)])
        self.hash_voor = _sha(self.data)

    def _controleer_geweigerd(self, res, *verwacht):
        uit = self._uitkomst(res)
        self.assertEqual(res.returncode, 2, uit)
        self.assertNotIn("Traceback", uit, uit)
        self.assertIsNone(ENGELS_OF_TRACEBACK.search(uit), "Engelse OS-tekst of traceback: %r" % uit)
        self.assertIn("FOUT", res.stderr, res.stderr)
        for woord in verwacht:
            self.assertIn(woord, res.stderr, "melding noemt %r niet: %r" % (woord, res.stderr))
        self.assertEqual(_sha(self.data), self.hash_voor, "data/nieuws.json is gewijzigd bij een foute config")

    def _met_feed(self, trefwoorden, naam_config="config.json"):
        with hf.FeedServer(ROUTES) as srv:
            feeds = [{"naam": FEED_NAAM, "url": srv.url("/feed.xml"), "taal": "nl"}]
            cfg = _basis_config(feeds, trefwoorden=trefwoorden)
            return self._draai(self._config(cfg, naam_config))

    def test_US022_c3_lege_trefwoorden_object_exitcode_2_data_ongewijzigd(self):
        res = self._met_feed({})
        self._controleer_geweigerd(res, "BI")

    def test_US022_c3_typo_sleutel_Ai_noemt_categorie_AI_exitcode_2_data_ongewijzigd(self):
        res = self._met_feed({"BI": ["bikern"], "Data": ["datakern"], "Automatisering": ["autokern"],
                              "Ai": ["aikern"]})
        self._controleer_geweigerd(res, "AI")

    def test_US022_c3_lege_lijst_per_categorie_exitcode_2_data_ongewijzigd(self):
        tw = copy.deepcopy(TW_GOED)
        tw["AI"] = []
        res = self._met_feed(tw)
        self._controleer_geweigerd(res, "AI")

    def test_US022_c3_lege_term_exitcode_2_data_ongewijzigd(self):
        tw = copy.deepcopy(TW_GOED)
        tw["BI"] = ["", "dashboard"]
        res = self._met_feed(tw)
        self._controleer_geweigerd(res, "BI")

    def test_US022_c3_term_met_alleen_spaties_exitcode_2_data_ongewijzigd(self):
        tw = copy.deepcopy(TW_GOED)
        tw["Data"] = ["   "]
        res = self._met_feed(tw)
        self._controleer_geweigerd(res, "Data")

    def test_US022_c3_trefwoorden_als_tekst_i_p_v_lijst_exitcode_2_data_ongewijzigd(self):
        tw = copy.deepcopy(TW_GOED)
        tw["BI"] = "dashboard"
        res = self._met_feed(tw)
        self._controleer_geweigerd(res, "BI")

    def test_US022_c3_categorie_Data_ontbreekt_exitcode_2_data_ongewijzigd(self):
        tw = copy.deepcopy(TW_GOED)
        del tw["Data"]
        res = self._met_feed(tw)
        self._controleer_geweigerd(res, "Data")

    def test_US022_c3_repro_ronde2_dataverlies_met_bereikbare_feed_en_echte_feeds(self):
        """Reproductie van ronde 2 (bevinding 1): kopie van de opgeslagen data, de echte feedlijst met een
        bereikbare feed en 'trefwoorden': {}. Verwacht: exitcode 2 en het bestand intact (niet leeggemaakt)."""
        if os.path.isfile(ECHTE_DATA):
            shutil.copyfile(ECHTE_DATA, self.data)
        else:
            _schrijf_data(self.data, [_item(i, "Power BI Blog (Microsoft)", "bikern %d" % i) for i in range(87)])
        self.hash_voor = _sha(self.data)
        aantal_voor = len(_lees_items(self.data))
        with hf.FeedServer(ROUTES) as srv:
            feeds = [dict(f, url=srv.url("/feed.xml")) for f in hf.project_config()["feeds"]]
            cfg = hf.project_config()
            cfg["feeds"] = feeds
            cfg["trefwoorden"] = {}
            res = self._draai(self._config(cfg))
        self._controleer_geweigerd(res, "BI")
        self.assertEqual(_sha(self.data), self.hash_voor)
        self.assertEqual(len(_lees_items(self.data)), aantal_voor)


class TestUS022C4Vangnet(_Basis):
    def _scenario(self, aantal_bekend, weg, extra_vreemd=0, extra=(), feed="/feed.xml"):
        """aantal_bekend opgeslagen items van de geconfigureerde feed, waarvan 'weg' geen trefwoord meer hebben
        (het zijn de items die de herindeling zou verwijderen). Optioneel extra items van een niet-geconfigureerde
        bron. Draait ophalen met één lokale feed die geen trefwoord bevat (dus er komt niets bij)."""
        items = []
        for i in range(aantal_bekend):
            titel = ("zonder woord %d" if i < weg else "bikern %d") % i
            items.append(_item(i, FEED_NAAM, titel))
        for j in range(extra_vreemd):
            items.append(_item(100000 + j, "Verdwenen bron", "bikern verdwenen %d" % j))
        _schrijf_data(self.data, items)
        self.hash_voor = _sha(self.data)
        with hf.FeedServer(ROUTES) as srv:
            feeds = [{"naam": FEED_NAAM, "url": srv.url(feed), "taal": "nl"}]
            res = self._draai(self._config(_basis_config(feeds)), extra)
        return res

    def test_US022_c4_precies_50_procent_wordt_geschreven_exitcode_0(self):
        res = self._scenario(aantal_bekend=10, weg=5)
        self.assertEqual(res.returncode, 0, self._uitkomst(res))
        self.assertNotEqual(_sha(self.data), self.hash_voor, "bij 50% moet het bestand geschreven worden")
        self.assertEqual(len(_lees_items(self.data)), 5)

    def test_US022_c4_precies_50_van_100_wordt_geschreven_exitcode_0(self):
        res = self._scenario(aantal_bekend=100, weg=50)
        self.assertEqual(res.returncode, 0, self._uitkomst(res))
        self.assertEqual(len(_lees_items(self.data)), 50)

    def test_US022_c4_51_procent_wordt_geweigerd_exitcode_1_data_ongewijzigd(self):
        for aantal, weg in ((100, 51), (10, 6)):
            with self.subTest(aantal=aantal, weg=weg):
                res = self._scenario(aantal_bekend=aantal, weg=weg)
                uit = self._uitkomst(res)
                self.assertEqual(res.returncode, 1, uit)
                self.assertNotIn("Traceback", uit, uit)
                self.assertEqual(_sha(self.data), self.hash_voor, "bij >50% mag niets weggeschreven worden")
                self.assertIn("--forceer-opruimen", uit, "melding noemt de optie niet")
                self.assertIn("%d van de %d" % (weg, aantal), uit, "melding noemt de aantallen niet")
                self.assertIn("niets weggeschreven", uit, "melding zegt niet dat er niets is weggeschreven")
                self.assertIsNone(ENGELS_OF_TRACEBACK.search(uit), "Engelse tekst in melding: %r" % uit)

    def test_US022_c4_met_forceer_opruimen_wordt_wel_geschreven_exitcode_0(self):
        res = self._scenario(aantal_bekend=100, weg=51, extra=("--forceer-opruimen",))
        self.assertEqual(res.returncode, 0, self._uitkomst(res))
        self.assertNotEqual(_sha(self.data), self.hash_voor)
        self.assertEqual(len(_lees_items(self.data)), 49)

    def test_US022_c4_feedruil_telt_niet_mee_items_van_niet_geconfigureerde_bron_geven_geen_vangnet(self):
        """20 items van een bron die niet meer in de config staat verdwijnen (US-019 c3, bewust). De 10 items van
        de geconfigureerde feed blijven allemaal staan: exitcode 0, geen vangnet-melding."""
        res = self._scenario(aantal_bekend=10, weg=0, extra_vreemd=30)
        uit = self._uitkomst(res)
        self.assertEqual(res.returncode, 0, uit)
        self.assertNotIn("STOP", uit, uit)
        items = _lees_items(self.data)
        self.assertEqual(len(items), 10)
        self.assertTrue(all(i["bron"] == FEED_NAAM for i in items), "items van de verdwenen bron staan er nog")

    def test_US022_c4_feedruil_met_50_procent_eigen_items_geen_vangnet(self):
        """Verdwenen bron erbij telt niet mee: 5 van 10 eigen items weg (50%) met 30 vreemde items = exitcode 0."""
        res = self._scenario(aantal_bekend=10, weg=5, extra_vreemd=30)
        self.assertEqual(res.returncode, 0, self._uitkomst(res))
        self.assertEqual(len(_lees_items(self.data)), 5)

    def test_US022_c4_gewone_ronde_wordt_niet_geblokkeerd_nieuw_item_komt_erbij(self):
        """Een gewone ronde zonder verwijdering: alle 10 items blijven en het nieuwe item uit de feed komt erbij."""
        _schrijf_data(self.data, [_item(i, FEED_NAAM, "bikern %d" % i) for i in range(10)])
        self.hash_voor = _sha(self.data)
        with hf.FeedServer(ROUTES) as srv:
            feeds = [{"naam": FEED_NAAM, "url": srv.url("/nieuw.xml"), "taal": "nl"}]
            res = self._draai(self._config(_basis_config(feeds)))
        uit = self._uitkomst(res)
        self.assertEqual(res.returncode, 0, uit)
        self.assertNotIn("STOP", uit, uit)
        self.assertEqual(len(_lees_items(self.data)), 11)

    def test_US022_c4_echte_data_gewone_ronde_wordt_niet_geblokkeerd(self):
        """Met de echte data (kopie) en de echte trefwoorden, met lokale feeds: geen vangnet-stop."""
        if not os.path.isfile(ECHTE_DATA):
            self.skipTest("NIET GETEST: data/nieuws.json ontbreekt (geen ophaalronde)")
        shutil.copyfile(ECHTE_DATA, self.data)
        voor = len(_lees_items(self.data))
        with hf.FeedServer(ROUTES) as srv:
            feeds = [dict(f, url=srv.url("/feed.xml")) for f in hf.project_config()["feeds"]]
            cfg = hf.project_config()
            cfg["feeds"] = feeds
            res = self._draai(self._config(cfg))
        uit = self._uitkomst(res)
        self.assertEqual(res.returncode, 0, uit)
        self.assertNotIn("STOP", uit, uit)
        self.assertGreaterEqual(len(_lees_items(self.data)), voor // 2)

    def test_US022_c4_extra_onleesbaar_data_bestand_leegt_de_opslag_niet(self):
        """Extra (Tester it. 8 ronde 3, dataverlies, afgeleid van US-022 c4 en de geest van de vangnet-eis):
        als data/nieuws.json met 87 items niet als JSON gelezen kan worden (BOM van Kladblok, of een afgekapt
        bestand), telt ophalen 0 opgeslagen items, ziet het vangnet niets en schrijft het alleen de nieuwe feeditems
        weg. Verwacht: niet stil leeg schrijven: exitcode niet 0 (met melding), of de 87 items blijven staan."""
        items = [_item(i, FEED_NAAM, "bikern %d" % i) for i in range(87)]
        _schrijf_data(self.data, items)
        with open(self.data, "rb") as f:
            raw = f.read()
        varianten = {"met BOM": b"\xef\xbb\xbf" + raw, "afgekapt": raw[: len(raw) // 2]}
        for naam, inhoud in varianten.items():
            with self.subTest(variant=naam):
                with open(self.data, "wb") as f:
                    f.write(inhoud)
                with hf.FeedServer(ROUTES) as srv:
                    feeds = [{"naam": FEED_NAAM, "url": srv.url("/feed.xml"), "taal": "nl"}]
                    res = self._draai(self._config(_basis_config(feeds)))
                uit = self._uitkomst(res)
                self.assertNotIn("Traceback", uit, uit)
                with open(self.data, "rb") as f:
                    na = f.read()
                try:
                    aantal = len(json.loads(na.decode("utf-8-sig"))["items"])
                except ValueError:
                    aantal = -1  # niet leesbaar: het bestand is aangetast
                self.assertTrue(res.returncode != 0 or (aantal >= 87 and na == inhoud),
                                "stil leeggeschreven: exitcode %d, %d items (was 87 onleesbaar opgeslagen)"
                                % (res.returncode, aantal))

    def test_US022_c4_workflow_gebruikt_forceer_opruimen_niet(self):
        self.assertTrue(os.path.isfile(WORKFLOW), "workflow ontbreekt")
        with open(WORKFLOW, encoding="utf-8") as f:
            tekst = f.read()
        self.assertNotIn("forceer", tekst.lower(), "de workflow gebruikt --forceer-opruimen")
        self.assertIn("python src/ophalen.py", tekst)


class TestUS022C5Config(_Basis):
    def setUp(self):
        super().setUp()
        self.srv = hf.FeedServer(ROUTES)
        self.srv.__enter__()  # de lokale feed moet bereikbaar zijn voor de geldige-config-test (c5a)

    def tearDown(self):
        self.srv.__exit__(None, None, None)
        super().tearDown()

    def _feed_config(self, **wijzigingen):
        feeds = [{"naam": FEED_NAAM, "url": self.srv.url("/feed.xml"), "taal": "nl"}]
        return _basis_config(feeds, **wijzigingen)

    def _controleer_geweigerd(self, res, cfg_pad, *verwacht):
        uit = self._uitkomst(res)
        self.assertEqual(res.returncode, 2, uit)
        self.assertNotIn("Traceback", uit, uit)
        self.assertIsNone(ENGELS_OF_TRACEBACK.search(uit), "Engelse tekst of traceback: %r" % uit)
        self.assertIn("FOUT", res.stderr, res.stderr)
        for woord in verwacht:
            self.assertIn(woord, res.stderr, "melding noemt %r niet: %r" % (woord, res.stderr))

    def test_US022_c5a_utf8_met_bom_wordt_normaal_gelezen_exitcode_0(self):
        cfg_pad = self._config(self._feed_config(), naam="met-bom.json", enc="utf-8-sig")
        with open(cfg_pad, "rb") as f:
            self.assertEqual(f.read(3), b"\xef\xbb\xbf", "testbestand heeft geen BOM")
        res = self._draai(cfg_pad)
        self.assertEqual(res.returncode, 0, self._uitkomst(res))
        self.assertTrue(os.path.isfile(self.data), "bij een geldige config met BOM moet het bestand ontstaan")
        self.assertNotIn("geen geldige JSON", self._uitkomst(res))

    def test_US022_c5b_lijstvelden_geen_lijst_van_tekst_exitcode_2_data_ongewijzigd(self):
        _schrijf_data(self.data, [_item(1, FEED_NAAM, "bikern 1")])
        voor = _sha(self.data)
        waarden = ["Data Master", 5, {"a": 1}, [1, 2]]
        for veld in ("uitsluitingen", "weigertermen", "weigertermen_samenvatting", "weiger_uitzonderingen"):
            for waarde in waarden:
                with self.subTest(veld=veld, waarde=waarde):
                    cfg_pad = self._config(self._feed_config(**{veld: waarde}), naam="lijst.json")
                    res = self._draai(cfg_pad)
                    self._controleer_geweigerd(res, cfg_pad, veld)
                    self.assertEqual(_sha(self.data), voor, "data ongewijzigd verwacht")

    def test_US022_c5c_feed_url_zonder_http_of_https_exitcode_2_data_ongewijzigd(self):
        _schrijf_data(self.data, [_item(1, FEED_NAAM, "bikern 1")])
        voor = _sha(self.data)
        for url in ("file:///C:/geheim.xml", "FILE:///C:/geheim.xml", "ftp://voorbeeld.example/feed",
                    "voorbeeld.example/feed.xml", ""):
            with self.subTest(url=url):
                cfg = self._feed_config()
                cfg["feeds"][0]["url"] = url
                cfg_pad = self._config(cfg, naam="url.json")
                res = self._draai(cfg_pad)
                self._controleer_geweigerd(res, cfg_pad, FEED_NAAM)
                self.assertEqual(_sha(self.data), voor, "data ongewijzigd verwacht")

    def test_US022_c5d_lege_feeds_eigen_melding_exitcode_2_data_ongewijzigd(self):
        _schrijf_data(self.data, [_item(1, FEED_NAAM, "bikern 1")])
        voor = _sha(self.data)
        cfg_pad = self._config(_basis_config([]), naam="leeg.json")
        res = self._draai(cfg_pad)
        uit = self._uitkomst(res)
        self._controleer_geweigerd(res, cfg_pad, "geen feeds ingesteld")
        self.assertNotIn("mislukt", uit, "melding is nog de misleidende 'alle feeds mislukt'")
        self.assertEqual(_sha(self.data), voor, "data ongewijzigd verwacht")

    def test_US022_c5_geen_uitvoer_bij_configfout_zonder_bestaand_bestand(self):
        cfg_pad = self._config(_basis_config([]), naam="leeg2.json")
        res = self._draai(cfg_pad)
        self.assertEqual(res.returncode, 2, self._uitkomst(res))
        self.assertFalse(os.path.exists(self.data), "bij een configfout mag geen uitvoerbestand ontstaan")


if __name__ == "__main__":
    unittest.main()
