"""Acceptatietests US-010 (categorie automatisch toewijzen op trefwoorden), zonder internet.

De tests gebruiken de trefwoorden uit config/feeds.json (alleen-lezen) en de functies van src/ophalen.py.
"""
import sys
sys.dont_write_bytecode = True  # vóór de imports hieronder: geen __pycache__ in src/ (iteratie 8)

import os
import unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "src"))
from hulp_feeds import FeedServer, project_config, run_ophalen, schrijf_config, tmp_map, lees_json  # noqa: E402
import ophalen  # noqa: E402
import shutil  # noqa: E402

CFG = project_config()
MATCHERS = ophalen.maak_matchers(CFG["trefwoorden"])

# Vaste testset: (titel, verwachte categorie). Minimaal 10 (criterium c5).
TESTSET = [
    ("Nieuwe machine learning-tool voor kleine teams", "AI"),
    ("Kunstmatige intelligentie helpt bij de triage in ziekenhuizen", "AI"),
    ("OpenAI lanceert een nieuwe API voor bedrijven", "AI"),
    ("Taalmodellen worden kleiner en zuiniger", "AI"),
    ("Chatbots in de klantenservice worden slimmer", "AI"),
    ("Automatisering van factuurverwerking bespaart uren", "Automatisering"),
    ("Low-code platforms groeien snel", "Automatisering"),
    # it. 4 fixronde 2 (besluit 2026-10-08): los "workflow" vervalt; de titel gebruikt nu de specifieke vorm "workflow automation"
    ("Workflow automation-tools maken processen voorspelbaar", "Automatisering"),
    ("Datawarehouse in de cloud wordt goedkoper", "Data"),
    ("Big data-analyse bij retailers", "Data"),
    # it. 6 (US-016 c1): dashboard en rapportage zijn BI-trefwoorden (was: Data)
    ("Dashboards voor betere bedrijfsrapportage", "BI"),
    ("Gegevens opschonen met SQL-scripts", "Data"),
]


class TestUS010(unittest.TestCase):
    # c1: trefwoorden per categorie, Nederlands en Engels
    def test_US010_c1_config_heeft_trefwoorden_nl_en_per_categorie(self):
        kw = CFG["trefwoorden"]
        # it. 6 (US-016 c1): vier categorieen, BI erbij (was: drie)
        self.assertEqual(set(kw.keys()), {"BI", "Data", "Automatisering", "AI"})
        eisen = {
            "AI": (["kunstmatige intelligentie", "machinaal leren", "taalmodel*"], ["artificial intelligence", "machine learning"]),
            "Automatisering": (["procesoptimalisatie", "bedrijfsprocessen", "geautomati*"], ["business process*", "orchestrat*", "robotic process"]),
            # it. 6 fixronde 1 (US-016 c8): los "gegevens" vervalt als Data-trefwoord; samenstelling "gegevensanalyse" blijft
            "Data": (["gegevensanalyse", "datawetenschap", "datakwaliteit"], ["data science", "big data", "analytics"]),
        }
        for cat, (nl, en) in eisen.items():
            for w in nl + en:
                self.assertIn(w, kw[cat], "%s: trefwoord ontbreekt: %s" % (cat, w))

    # c2: hele woorden, hoofdletterongevoelig
    def test_US010_c2_een_categorie_hoofdletterongevoelig_hele_woorden(self):
        self.assertEqual(ophalen.categoriseer("Nieuwe AI-tool voor kantoren", "", MATCHERS), "AI")
        self.assertEqual(ophalen.categoriseer("Nieuwe ai-tool", "", MATCHERS), "AI")
        # it. 6 (US-016 c3): een AI-woord alleen in de samenvatting telt niet mee (was: AI)
        self.assertIsNone(ophalen.categoriseer("Kleine tekst", "de ai hype groeit", MATCHERS), "AI alleen in samenvatting")
        self.assertEqual(ophalen.categoriseer("Nieuwe AI-tool", "de ai hype groeit", MATCHERS), "AI", "AI in de titel telt")
        self.assertEqual(ophalen.categoriseer("DATABASE-opslag", "", MATCHERS), "Data")  # fixronde it4: "data" los vervalt, specifieke vorm
        self.assertIsNone(ophalen.categoriseer("Mail vanuit de nieuwe Waaier-app", "", MATCHERS), "'AI' matcht ten onrechte in 'mail' of 'Waaier'")
        self.assertIsNone(ophalen.categoriseer("Gmail-filter voor Waaier", "", MATCHERS))

    # c3: meeste treffers wint; gelijkspel volgorde BI, Data, Automatisering, AI (it. 6, US-016 c2; was AI, Automatisering, Data)
    def test_US010_c3_meeste_treffers_wint_en_gelijkspel_volgorde_ai_automatisering_data(self):
        cat = ophalen.categoriseer
        # "Data en AI" is geen gelijkspel meer (los "data" telt sinds it. 4 niet); de gelijkspel-invoer is "dataset".
        self.assertEqual(cat("Dataset en AI", "", MATCHERS), "Data", "gelijkspel Data/AI: Data wint (it. 6)")
        self.assertEqual(cat("Automatisering van databases", "", MATCHERS), "Data", "gelijkspel Automatisering/Data: Data wint (it. 6)")
        self.assertEqual(cat("Automatisering, automatisering, database, database", "", MATCHERS), "Data",
                         "gelijkspel 2-2 Automatisering/Data: Data wint (it. 6)")
        self.assertEqual(cat("database database database AI", "", MATCHERS), "Data", "3 Data-treffers wint van 1 AI-treffer")
        self.assertEqual(cat("AI AI Automatisering", "", MATCHERS), "AI")

    # c4: geen enkele treffer -> niet opgeslagen (en dus niet getoond)
    def test_US010_c4_item_zonder_treffer_wordt_niet_opgeslagen(self):
        self.assertIsNone(ophalen.categoriseer("Nieuwe telefoon met grote batterij", "Lichter en dunner", MATCHERS))
        tmp = tmp_map()
        try:
            uit = os.path.join(tmp, "nieuws.json")
            def feed(base):
                return ('<?xml version="1.0"?><rss version="2.0"><channel>'
                        '<item><title>Nieuwe telefoon met grote batterij</title><link>%s/geen</link>'
                        '<description>Lichter en dunner</description></item>'
                        '<item><title>AI-assistent voor het mkb</title><link>%s/wel</link>'
                        '<description>Test</description></item></channel></rss>' % (base, base)).encode("utf-8")
            with FeedServer({"/feed.xml": {"body": feed}}) as srv:
                cfg = schrijf_config(os.path.join(tmp, "cfg.json"), [{"naam": "Testfeed", "url": srv.base + "/feed.xml", "taal": "nl"}])
                res = run_ophalen(cfg, uit)
                self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
                urls = [i["url"] for i in lees_json(uit)["items"]]
            self.assertEqual(len(urls), 1, urls)
            self.assertTrue(urls[0].endswith("/wel"))
            self.assertIn("1 zonder categorie", res.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # c5: vaste testset van minimaal 10 titels met verwachte categorie
    def test_US010_c5_testset_titels_krijgen_verwachte_categorie(self):
        self.assertGreaterEqual(len(TESTSET), 10)
        fouten = []
        for titel, verwacht in TESTSET:
            gevonden = ophalen.categoriseer(titel, "", MATCHERS)
            if gevonden != verwacht:
                fouten.append("%r: verwacht %s, kreeg %s" % (titel, verwacht, gevonden))
        self.assertEqual(fouten, [], "\n".join(fouten))


if __name__ == "__main__":
    unittest.main()
