"""Acceptatietests US-017 (kwaliteitsfilter tegen gadget-, deal- en promotieberichten), iteratie 6.

- c1 configuratie: aanpasbare weigerlijst met de verplichte termen (titel) en de promotietermen (samenvatting).
- c2 weigerterm in de titel (hele woorden, hoofdletterongevoelig) -> niet opgeslagen, ook met trefwoordtreffers.
- c3 "sponsored", "gesponsord", "partnerbijdrage", "advertorial" alleen in de samenvatting -> geweigerd.
- c4 vaste testset van echte en voorbeeldtitels: 6 te weigeren, 6 toe te laten (incl. overname met "deal", en "dealer").
- c5 per feed het aantal geweigerde items met voorbeeldtitels in de uitvoer (formaat, automatisch); de meting van de
  echte ophaalronde staat in het testrapport.

Geen internet. config/feeds.json wordt alleen gelezen; de ophaal-test gebruikt een lokale testserver.
"""
import sys
sys.dont_write_bytecode = True  # vóór de imports hieronder: geen __pycache__ in src/ (iteratie 8)

import datetime
import json
import os
import unittest

import hulp_statisch as h  # noqa: F401  (ROOT/paden)
import hulp_feeds as hf
sys.path.insert(0, os.path.join(h.ROOT, "src"))
import ophalen as o  # noqa: E402

with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
    CFG = json.load(f)
MATCHERS = o.maak_matchers(CFG["trefwoorden"], CFG.get("uitsluitingen"))
WEIGER = o.maak_weigerlijst(CFG)
VANDAAG = datetime.date(2026, 10, 8)
FEED = {"naam": "Fixture", "taal": "nl"}


def norm(woord):
    return woord.rstrip("*").casefold()


def verwerk(titel, samenvatting=""):
    """Geeft (opgeslagen titels, geweigerde titels) voor een enkel ruw item."""
    geweigerd = []
    ruw = [{"titel": titel, "link": "https://voorbeeld-bron.example/w-%d" % abs(hash(titel)),
            "samenvatting_html": samenvatting, "datum": VANDAAG}]
    uit, _, _ = o.verwerk_items(ruw, FEED, MATCHERS, VANDAAG, 300, WEIGER, geweigerd)
    return [i["titel"] for i in uit], geweigerd


# c4: vaste testset (titel, samenvatting, verwacht geweigerd?). Titels 'Gemini, metadata...' en 'Power BI September...'
# zijn echte titels uit de ophaalronde van 8 okt 2026; de overige zijn verzonnen voor deze test.
TESTSET = [
    # it. 6 fixronde 1 (US-017 c7): 'analogy game' staat op de uitzonderingslijst; deze titel is nu toegelaten (was: True).
    ("Gemini, metadata and the analogy game", "", False),                        # echt (uitzondering analogy game)
    ("Webinar: dashboards voor het mkb", "", True),
    ("Black Friday-deals op laptops", "", True),
    ("Review: de nieuwe smartphone van Samsung", "", True),
    ("Kortingscode voor de AI-cursus", "", True),
    ("Unboxing van de nieuwe Surface", "", True),
    ("Power BI September 2026 Feature Summary", "", False),                       # echt
    ("Microsoft introduceert hybride ai voor Windows 11: slimmer en goedkoper", "", False),  # echt
    ("Begin bij het einde: zo maak je agentic remediation mogelijk", "", False),  # echt
    ("Snowflake neemt Acme over: deal van 1 miljard dollar", "", False),        # overname met 'deal'
    ("Dealer-netwerk van Acme gaat naar Bolt", "", False),                      # 'dealer'
    ("Nieuwe Fabric-update voor de gemeente", "", False),
]


class TestUS017(unittest.TestCase):
    def test_US017_c1_weigerlijst_bevat_verplichte_termen(self):
        titel = {norm(w) for w in CFG["weigertermen"]}
        samen = {norm(w) for w in CFG["weigertermen_samenvatting"]}
        for t in ["webinar", "webcast", "aanbieding", "korting", "kortingscode", "deals", "prijsverlaging",
                  "black friday", "review", "unboxing", "hands-on", "smartphone", "game", "console"]:
            self.assertIn(t, titel, "weigerlijst (titel) mist: %s" % t)
        for t in ["sponsored", "gesponsord", "partnerbijdrage", "advertorial"]:
            self.assertIn(t, samen, "promotieterm (samenvatting) mist: %s" % t)
        self.assertIsInstance(CFG["weigertermen"], list, "weigerlijst moet een aanpasbare lijst in de config zijn")

    def test_US017_c2_weigerterm_in_titel_wordt_niet_opgeslagen_ook_met_trefwoord(self):
        for titel in ["Webinar: AI en dataplatformen voor het mkb", "WEBINAR over Power BI", "Unboxing van de nieuwe AI-bril",
                      "Dashboards: review van Tableau", "Kortingscode voor Snowflake-cursus", "Game-AI in de cloud"]:
            opgeslagen, geweigerd = verwerk(titel)
            self.assertEqual(opgeslagen, [], "%r is toch opgeslagen" % titel)
            self.assertEqual(geweigerd, [titel], "%r moet als geweigerd gemeld worden" % titel)

    def test_US017_c2_hele_woorden_en_geen_valse_weigering(self):
        opgeslagen, _ = verwerk("Power BI krijgt nieuwe functies")
        self.assertEqual(opgeslagen, ["Power BI krijgt nieuwe functies"], "gewone BI-titel moet blijven staan")
        self.assertIsNone(WEIGER.reden("Consolidatie van dataplatformen", ""), "'console*' mag niet in 'consolidatie' matchen")

    def test_US017_c3_promotieterm_alleen_in_samenvatting_wordt_geweigerd(self):
        for term in ["sponsored", "gesponsord", "partnerbijdrage", "advertorial"]:
            opgeslagen, geweigerd = verwerk("Nieuwe Power BI-functies", "Dit artikel is %s door een partner." % term)
            self.assertEqual(opgeslagen, [], "promotieterm '%s' in samenvatting is toch opgeslagen" % term)
            self.assertEqual(len(geweigerd), 1)
        opgeslagen, _ = verwerk("Nieuwe Power BI-functies", "Microsoft toont nieuwe functies voor rapportages.")
        self.assertEqual(opgeslagen, ["Nieuwe Power BI-functies"], "controle: gewone samenvatting blijft staan")

    def test_US017_c4_vaste_testset_klopt_voor_elke_titel(self):
        self.assertGreaterEqual(len(TESTSET), 10)
        self.assertGreaterEqual(len([t for t in TESTSET if t[2]]), 5, "minstens 5 te weigeren")
        self.assertGreaterEqual(len([t for t in TESTSET if not t[2]]), 5, "minstens 5 toe te laten")
        fouten = []
        for titel, samen, verwacht_geweigerd in TESTSET:
            opgeslagen, geweigerd = verwerk(titel, samen)
            if verwacht_geweigerd != bool(geweigerd):
                fouten.append("%r: verwacht geweigerd=%s, kreeg %s" % (titel, verwacht_geweigerd, bool(geweigerd)))
        self.assertEqual(fouten, [], "\n".join(fouten))

    def test_US017_c4_overnametitel_met_deal_en_dealer_worden_toegelaten(self):
        for titel in ["Snowflake neemt Acme over: deal van 1 miljard dollar", "Dealer-netwerk van Acme gaat naar Bolt"]:
            self.assertIsNone(WEIGER.reden(titel, ""), "'%s' ten onrechte geweigerd" % titel)

    def test_US017_c5_ophaaluitvoer_meldt_geweigerd_per_feed_met_voorbeeldtitels(self):
        """Formaat van de uitvoer (automatisch). De echte aantallen per feed staan in het testrapport."""
        tmp = hf.tmp_map()
        try:
            def rss(base):
                return ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Fixture</title>'
                        '<item><title>Webinar: Power BI voor het mkb</title><link>%(b)s/a1</link>'
                        '<description>Test</description><pubDate>%(d)s</pubDate></item>'
                        '<item><title>Black Friday-deals op laptops</title><link>%(b)s/a2</link>'
                        '<description>Test</description><pubDate>%(d)s</pubDate></item>'
                        '<item><title>Power BI krijgt nieuwe functies</title><link>%(b)s/a3</link>'
                        '<description>Test</description><pubDate>%(d)s</pubDate></item>'
                        '</channel></rss>' % {"b": base, "d": hf.rfc(1)}).encode("utf-8")
            with hf.FeedServer({"/feed.xml": {"body": rss}}) as srv:
                cfg = hf.schrijf_config(os.path.join(tmp, "cfg.json"),
                                        [{"naam": "Fixture Feed", "url": srv.base + "/feed.xml", "taal": "nl"}])
                res = hf.run_ophalen(cfg, os.path.join(tmp, "nieuws.json"))
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            regel = [r for r in res.stdout.splitlines() if r.startswith("OK") and "Fixture Feed" in r]
            self.assertTrue(regel, res.stdout)
            self.assertIn("2 geweigerd (kwaliteit)", regel[0])
            self.assertIn("Webinar: Power BI voor het mkb", res.stdout, "voorbeeldtitel ontbreekt in de uitvoer")
            self.assertIn("Black Friday-deals op laptops", res.stdout)
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    def test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer(self):
        """US-017 c5 (fixronde 1): het ophaallog telt per feed unieke nieuwe links; dubbele links tellen een keer."""
        tmp = hf.tmp_map()
        try:
            def rss(base):
                blok = ('<item><title>Webinar: Power BI voor het mkb</title><link>%(b)s/dubbel</link>'
                        '<description>Test</description><pubDate>%(d)s</pubDate></item>') % {"b": base, "d": hf.rfc(1)}
                return ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Fixture</title>'
                        + blok + blok +
                        '</channel></rss>').encode("utf-8")
            with hf.FeedServer({"/feed.xml": {"body": rss}}) as srv:
                cfg = hf.schrijf_config(os.path.join(tmp, "cfg.json"),
                                        [{"naam": "Fixture Feed", "url": srv.base + "/feed.xml", "taal": "nl"}])
                res = hf.run_ophalen(cfg, os.path.join(tmp, "nieuws.json"))
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            regel = [r for r in res.stdout.splitlines() if r.startswith("OK") and "Fixture Feed" in r]
            self.assertTrue(regel, res.stdout)
            self.assertIn("1 geweigerd (kwaliteit)", regel[0], "dubbele link telt meer dan een keer: %s" % regel[0])
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    # c6: evenement- en vendor-PR-patronen in de weigerlijst (titel, hoofdletterongevoelig)
    def test_US017_c6_configuratie_bevat_evenement_en_vendor_pr_patronen(self):
        titel = CFG["weigertermen"]
        verplicht_woorden = ["save the date", "early bird", "tickets", "named a leader", "named a visionary",
                             "recognized as a", "recognised as a", "magic quadrant", "forrester wave", "credits"]
        for w in verplicht_woorden:
            self.assertIn(w, titel, "weigerlijst mist: %s" % w)
        regex = [t for t in titel if t.startswith("re:") and "nog" in t and "tot" in t and "dagen" in t and "weken" in t]
        self.assertTrue(regex, "weigerlijst mist de regex 'nog <getal> (dagen|weken|maanden) tot'")

    def test_US017_c6_evenementpromo_en_vendor_pr_worden_geweigerd(self):
        for titel in ["Nog vier weken tot Emerce EDAY",
                      "Camunda Named a Leader in The Forrester Wave: Adaptive Process Orchestration Software, Q3 2026",
                      "Camunda Recognized as a Visionary in Gartner BOAT Magic Quadrant 2026",
                      "You can now top up your n8n Assistant credits"]:
            self.assertIsNotNone(WEIGER.reden(titel, ""), "%r is ten onrechte toegelaten" % titel)
            opgeslagen, geweigerd = verwerk(titel)
            self.assertEqual(opgeslagen, [], "%r is toch opgeslagen" % titel)

    def test_US017_c6_overname_productrelease_en_gartner_titel_worden_toegelaten(self):
        for titel in ["Salesforce neemt Informatica over",
                      "Power BI September 2026 Feature Summary",
                      "Microsoft Fabric: Materialized views now generally available",
                      "Gartner ziet BI-markt groeien"]:
            self.assertIsNone(WEIGER.reden(titel, ""), "%r ten onrechte geweigerd" % titel)

    # c7: uitzonderingslijst voor zakelijke combinaties; tekst onder een uitzondering telt niet als weigerterm
    def test_US017_c7_uitzonderingslijst_bevat_zakelijke_combinaties(self):
        uitz = {norm(w) for w in CFG["weiger_uitzonderingen"]}
        for w in ["operational review", "code review", "peer review", "security review", "analogy game", "game theory",
                  "gamechanger", "game changer"]:
            self.assertIn(w, uitz, "uitzonderingslijst mist: %s" % w)

    def test_US017_c7_vaste_testset_laat_zakelijke_combinaties_toe(self):
        for titel in ["Run an automated operational review with the Amazon Redshift MCP server",
                      "Gemini, metadata and the analogy game"]:
            self.assertIsNone(WEIGER.reden(titel, ""), "%r ten onrechte geweigerd" % titel)

    def test_US017_c7_review_en_games_blijven_geweigerd(self):
        for titel in ["Review: Samsung Galaxy S26", "Nieuwe games met AI-personages",
                      "Analogy game: nieuwe game voor AI", "Gemini, metadata and the analogy game (zie ook de review)"]:
            self.assertIsNotNone(WEIGER.reden(titel, ""), "%r ten onrechte toegelaten" % titel)


if __name__ == "__main__":
    unittest.main()
