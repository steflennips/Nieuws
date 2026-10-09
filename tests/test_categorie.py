"""Eigen tests US-015: uitsluitingstermen, trefwoordenaantallen en een vaste testset (zonder internet)."""
import json
import os
import sys
import unittest

BASIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(BASIS, "src"))
import ophalen  # noqa: E402

with open(os.path.join(BASIS, "config", "feeds.json"), encoding="utf-8") as f:
    CFG = json.load(f)
M = ophalen.maak_matchers(CFG["trefwoorden"], CFG.get("uitsluitingen"))

# (titel, verwachte categorie); None = niet relevant, wordt niet getoond.
# De eerste 6 zijn echte titels uit een ophaalronde van 2026-10-08.
TESTSET = [
    ("Automate remediation post AWS DevOps Agent investigation", "Automatisering"),
    ("AWS Launches Aurora Capability to Query Data Lakes Without Moving the Data", "Data"),
    ("Compacte en snelle Claude Haiku 5.5 vervangt eindelijk 4.5", "AI"),
    ("How Cornerstone OnDemand cut database diagnosis by 78% with Amazon Bedrock", "Data"),
    ("Who Pays for AI Data Centers?", "AI"),
    ("Firmware-update - Asustor ADM 5.1.4.RM62", None),
    ("Zo automatiseer je je facturatie met Power Automate", "Automatisering"),
    ("Low-code platform versnelt bedrijfsprocessen", "Automatisering"),
    ("Terraform en Ansible voor infrastructure as code", "Automatisering"),
    ("RPA-bot neemt administratie over bij zorginstelling", "Automatisering"),
    ("n8n en Zapier: workflows zonder code", "Automatisering"),
    ("Snowflake lanceert nieuw dataplatform", "Data"),
    ("Databricks en de lakehouse: wat verandert er", "Data"),
    ("Power BI dashboard voor het mkb", "BI"),
    ("Datakwaliteit blijft een probleem voor gemeenten", "Data"),
    ("Nieuwe SQL-database met sneller ETL", "Data"),
    ("Nieuwe dataset voor onderzoek vrijgegeven", "Data"),
    ("Data engineering in de praktijk bij gemeenten", "Data"),
    ("Pandas 3.0 maakt dataframes sneller", "Data"),
    ("Een datamodel opzetten voor je webshop", "Data"),
    ("Data governance wordt verplicht voor ziekenhuizen", "Data"),
    ("Data lake of data warehouse: wat past bij jou", "Data"),
    ("Business intelligence voor het mkb", "BI"),
    ("Goedkoper datawarehouse in de cloud", "Data"),
    ("Webanalytics met een nieuw dbt-pakket", "Data"),
    ("Workflow automation met open source tools", "Automatisering"),
    ("Workflowautomatisering bespaart uren per week", "Automatisering"),
    ("Workflow-automatisering voor de administratie", "Automatisering"),
    ("Nieuwe workflows in ons team besproken", None),
    ("Mistral lanceert nieuw taalmodel", "AI"),
    ("Generatieve AI in het onderwijs", "AI"),
    ("OpenAI en Anthropic strijden om de enterprise-markt", "AI"),
    ("Kunstmatige intelligentie in de zorg", "AI"),
    ("Je mail en je maintenance", None),
    ("Nieuwe telefoon met grote batterij", None),
]


# Echte titels met samenvatting uit de ophaalronde van 2026-10-08 (US-015 c6): (titel, samenvatting, verwacht)
# verwacht: ("niet", categorie) = mag die categorie niet krijgen; ("is", categorie) = moet die krijgen.
ECHT = [
    ("Laptops met Nvidia RTX Spark-processor kosten in Nederland minstens 2999 euro",
     "Laptops met Nvidia RTX Spark-processors zijn in Nederland te koop vanaf 2999 euro. Dat blijkt uit listings van Megekko en Coolblue. De versies met het meeste geheugen en de krachtigste chip kosten meer dan 6000 euro. Ze worden later deze maand geleverd.",
     ("niet", "Data")),
    ("Instapversie Microsoft Surface-laptop met Nvidia RTX Spark-cpu kost 2600 dollar",
     "Microsoft en Nvidia deelden op woensdagavond meer details over de aanstaande Nvidia RTX Spark-processor. Laptops met deze chip zijn vanaf nu vooruit te bestellen en worden vanaf volgende week vrijdag geleverd. Microsofts goedkoopste variant kost 2600 dollar.",
     ("niet", "Data")),
    ("Colt brengt SCION als managed netwerkdienst naar Europa",
     "Colt Technology Services brengt SCION op de markt als volledig beheerde netwerkdienst in Europa, Noord-Amerika en Azië. Met de technologie van het Zwitserse Anapaya bepalen organisaties zelf welke route hun data aflegt. Colt richt zich op sectoren met gevoelige, gereguleerde of bedrijfskritische...",
     ("niet", "Data")),
    ("Uber Eats Rebuilds Search Pipeline to Cut End-to-End Latency by 50%",
     "Uber has rebuilt major parts of the Uber Eats search pipeline, reporting a 50% reduction in end-to-end latency. Changes include Above-the-Fold measurement, reduced retrieval work, parallel hydration, advertising data redesign, infrastructure optimizations, and an agentic coding workflow. Uber is...",
     ("niet", "Automatisering")),
    ("New Archestra's OpenAPPA Saturates Two Major Security Benchmarks with a 0% Attack Success Rate",
     "Archestra released OpenAPPA, an open-source security engine designed to stop data exfiltration caused by prompt injection or model hallucination. The team reports zero successful attacks when running security benchmarks Bench-Corp (20 multi-step enterprise workflows) and AgentThreatBench, versus...",
     ("niet", "Automatisering")),
    ("Manage Amazon SageMaker HyperPod Spaces directly from SageMaker Studio",
     "Data scientists and ML engineers can now create, configure, start, stop, and open Amazon SageMaker Spaces on SageMaker HyperPod EKS clusters directly from SageMaker Studio. Launch JupyterLab and Code Editor environments in a few clicks, without using command-line tools.",
     ("is", "AI")),
]


class TestEchteTitels(unittest.TestCase):
    def test_echte_titels_met_samenvatting(self):
        for titel, samenv, (soort, cat) in ECHT:
            res = ophalen.categoriseer(titel, samenv, M)
            if soort == "niet":
                self.assertNotEqual(res, cat, titel)
            else:
                self.assertEqual(res, cat, titel)

    def test_losse_generieke_woorden_niet_in_config(self):
        for cat, woorden in CFG["trefwoorden"].items():
            low = [w.casefold() for w in woorden]
            for verboden in ("data", "spark", "pipeline*", "pipeline"):
                self.assertNotIn(verboden, low, cat)

    def test_specifieke_vormen_werken(self):
        self.assertEqual(ophalen.categoriseer("Apache Spark 5 is uit", "", M), "Data")
        self.assertEqual(ophalen.categoriseer("Bouw een CI/CD-pipeline in een uur", "", M), "Automatisering")
        self.assertEqual(ophalen.categoriseer("Een data pipeline bouwen", "", M), "Data")

    def test_false_positives_data_termen(self):
        for t in ("Mensen met een etlen-naam", "Elk sqlite-item", "Een pandastaal studie", "Metaldehyde dbtx"):
            self.assertNotEqual(ophalen.categoriseer(t, "", M), "Data", t)

    def test_minstens_10_specifieke_data_termen(self):
        woorden = " | ".join(CFG["trefwoorden"]["Data"]).casefold()
        # business intelligence en power bi zijn sinds iteratie 6 BI (eigen categorie)
        termen = ["dataset", "data engineering", "data lake", "data warehouse", "sql", "analytics", "etl",
                  "databricks", "snowflake", "dbt", "pandas",
                  "datakwaliteit", "data governance", "datamodel"]
        self.assertGreaterEqual(len([t for t in termen if t in woorden]), 10)

    def test_rtx_spark_uitgesloten(self):
        uitsl = [u.casefold() for u in CFG["uitsluitingen"]]
        self.assertIn("rtx spark", uitsl)


# Eigen mini-trefwoordenlijst voor de uitsluitingsmechaniek: de echte config heeft sinds fixronde it. 4 geen los woord "data" meer.
MECHANIEK = {"Data": ["data"], "AI": ["chatbot*"]}
MM = ophalen.maak_matchers(MECHANIEK, CFG["uitsluitingen"])


class TestUitsluiting(unittest.TestCase):
    def test_config_heeft_uitsluitingen(self):
        self.assertIn("data master", [u.casefold() for u in CFG["uitsluitingen"]])

    def test_asustor_niet_data(self):
        cat = ophalen.categoriseer("Firmware-update - Asustor ADM 5.1.4.RM62", "Asustor Data Master krijgt nieuwe functies", M)
        self.assertNotEqual(cat, "Data")

    def test_zonder_uitsluiting_wel_data(self):
        zonder = ophalen.maak_matchers(MECHANIEK)
        self.assertEqual(ophalen.categoriseer("Asustor Data Master", "", zonder), "Data")

    def test_uitsluiting_laat_rest_van_tekst_meetellen(self):
        self.assertEqual(ophalen.categoriseer("Data Master krijgt een chatbot", "", MM), "AI")

    def test_uitsluiting_hele_woorden_en_hoofdletterongevoelig(self):
        self.assertIsNone(ophalen.categoriseer("DATA MASTER 5.1", "", MM))
        self.assertEqual(ophalen.categoriseer("Data Mastery cursus", "", MM), "Data")


class TestTrefwoorden(unittest.TestCase):
    def test_minstens_15_per_categorie(self):
        for cat in ("BI", "Data", "Automatisering", "AI"):
            self.assertGreaterEqual(len(CFG["trefwoorden"][cat]), 15, cat)

    def test_nl_en_aanwezig(self):
        for cat, nl, en in (("AI", "kunstmatige intelligentie", "machine learning"),
                            ("Automatisering", "bedrijfsprocessen", "workflow automation"),
                            ("Data", "datakwaliteit", "data engineering")):
            woorden = [w.casefold() for w in CFG["trefwoorden"][cat]]
            self.assertIn(nl, woorden)
            self.assertIn(en, woorden)


class TestTestset(unittest.TestCase):
    def test_omvang(self):
        self.assertGreaterEqual(len(TESTSET), 20)
        for cat in ("Data", "Automatisering", "AI"):  # BI: zie tests/test_mix.py
            self.assertGreaterEqual(len([1 for _, c in TESTSET if c == cat]), 5, cat)

    def test_vaste_testset(self):
        for titel, verwacht in TESTSET:
            self.assertEqual(ophalen.categoriseer(titel, "", M), verwacht, titel)


if __name__ == "__main__":
    unittest.main()
