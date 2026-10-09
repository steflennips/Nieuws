"""Acceptatietests US-015 (betere categorie-indeling) met de echte configuratie config/feeds.json (alleen gelezen).

- c1: uitsluitingstermen staan in de configuratie (minstens "Data Master"); uitgesloten tekst telt niet mee.
- c2: het voorbeeld uit de story (Asustor Data Master) krijgt niet de categorie Data.
- c3: per categorie minstens 15 trefwoorden, in het Nederlands en Engels.
- c4: vaste testset van 26 voorbeeldtitels: 25 met verwachte categorie (minstens 5 per categorie, waarvan minstens 3 echte titels uit de
  ophaalronde van 8 oktober 2026). Verwachte categorieen zijn door de Tester bepaald vóór het draaien van de
  test, op basis van de titel en samenvatting; niet afgeleid van de uitkomst van de code.
- c5 (aantallen per categorie na een echte ophaalronde) is geen automatische test; zie tests/acceptance/README.md.
"""
import sys
sys.dont_write_bytecode = True  # vóór de imports hieronder: geen __pycache__ in src/ (iteratie 8)

import datetime
import json
import os
import unittest

import hulp_statisch as h
SRC = os.path.join(h.ROOT, "src")
sys.path.insert(0, SRC)
import ophalen as o  # noqa: E402

with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
    CFG = json.load(f)
MATCHERS = o.maak_matchers(CFG["trefwoorden"], CFG.get("uitsluitingen"))

ECHT = True
# (titel, samenvatting, verwachte categorie, echte titel uit de ophaalronde?)
# Synthetische titels: verzonnen voor deze test. Echte titels: exact overgenomen uit data/nieuws.json (8 okt 2026).
TESTSET = [
    ("Chatbot helpt klanten met vragen over hun polis", "", "AI", False),
    ("Nieuwe LLM-release verbetert codering", "", "AI", False),
    ("Kunstmatige intelligentie in de zorg groeit snel", "", "AI", False),
    ("Machine learning-model voorspelt uitval van machines", "", "AI", False),
    ("Generative tools veranderen het ontwerpwerk", "", "AI", False),
    ("ChatGPT schrijft nu ook code voor bedrijven", "", "AI", False),
    ("Low-code platform versnelt de bouw van interne apps", "", "Automatisering", False),
    ("Mkb automatiseert facturatie met workflow-tools", "", "Automatisering", False),
    ("RPA-robots nemen repetitief werk over", "", "Automatisering", False),
    ("Robotic process automation groeit in de bank", "", "Automatisering", False),
    ("Terraform en Ansible voor infrastructure as code", "", "Automatisering", False),
    ("Datakwaliteit wordt een prioriteit voor bestuurders", "", "Data", False),
    ("Nieuw dashboard toont rapportages in realtime", "", "BI", False),  # it. 6: BI-trefwoorden (was Data)
    ("Databases in de cloud: wat moet je weten", "", "Data", False),
    ("Big data-analyse helpt retailers met voorraad", "", "Data", False),
    ("Open data van de gemeente wordt gratis beschikbaar", "", "Data", False),
    ("Snowflake breidt datawarehouse-functies uit", "", "Data", False),
    ("Statistiek en metadata maken rapportages beter", "", "Data", False),
    ("Workflow met ChatGPT", "", "AI", False),
    ("Introducing Claude Haiku 5.5 on AWS",
     "Claude Haiku 5.5 is now available on Amazon Bedrock and Claude Platform on AWS. According to Anthropic, it is the fastest, most efficient model in the Claude 5.5 family, built for subagents and high-volume, cost-sensitive work, and costs around 75% less than Claude Haiku 4.5 for most tasks. This...",
     "AI", ECHT),
    ("Compacte en snelle Claude Haiku 5.5 vervangt eindelijk 4.5",
     "Op een week na een jaar geleden bracht Anthropic Claude Haiku 4.5 uit, een compact, goedkoop en snel alternatief voor Sonnet en Opus. Nu is er eindelijk weer een volledig geüpdatete optelsom in de Claude-reeks: Opus 5.5 voor ambitieuze taken, Sonnet 5.5 voor net wat minder complex werk en Haiku 5...",
     "AI", ECHT),
    ("Building AI Agents with Docker Agent",
     "Docker Agent is an open-source, Apache 2.0-licensed CLI plugin built by Docker Engineering, installed and run as docker agent. Its own tagline states the goal plainly: run AI agents like containers.",
     "AI", ECHT),
    ("Automate remediation post AWS DevOps Agent investigation",
     "AWS DevOps Agent can diagnose production incidents but is kept in observe-and-report mode so it does not change resources directly. This post shows how to use AWS Lambda Durable Functions, Amazon EventBridge, and Amazon Bedrock to turn its investigation summaries into pre-validated fixes an on-ca...",
     "Automatisering", ECHT),
    ("How Cornerstone OnDemand cut database diagnosis by 78% with Amazon Bedrock",
     "Cornerstone OnDemand built Orion AI, a multi-agent system on Amazon Bedrock and Strands Agents, to turn database operations from reactive firefighting into proactive automation. A three-person team cut database diagnosis from 45 minutes to 10, a 78% reduction, in six months. See the design decisi...",
     "Data", ECHT),
    ("AWS Launches Aurora Capability to Query Data Lakes Without Moving the Data",
     "Moving enterprise data around is one of the less glamorous parts of the running modern data stack. Nevertheless, it is critical to getting the right data to the right applications when they need it. Companies build their data pipelines to shuttle information between databases and data lakes. This...",
     "Data", ECHT),
    # Fixronde 2 it. 4 (US-015 c10): extra titels, elk via een andere specifieke Data-term (zie C10_EXTRA hieronder)
    ("Een nieuwe dataset voor weerdata is gratis beschikbaar", "", "Data", False),
    ("Data engineering-teams krijgen een eigen platform", "", "Data", False),
    ("Hoe een data lake bij een bank wordt opgezet", "", "Data", False),
    ("SQL-cursus voor beginners", "", "Data", False),
    ("ETL-pijplijnen vereenvoudigen met een nieuwe tool", "", "Data", False),
    ("Databricks brengt een nieuwe versie van zijn dataplatform uit", "", "Data", False),  # it. 6: was "Power BI ..." (Power BI is nu BI)
    ("Asustor Data Master krijgt nieuwe functies", "", None, False),
]


def categorie_van(titel, samenvatting):
    return o.categoriseer(titel, samenvatting, MATCHERS)


class TestUS015(unittest.TestCase):
    def test_US015_c1_uitsluitingstermen_in_config_met_data_master(self):
        uitsluitingen = [u.casefold() for u in CFG.get("uitsluitingen", [])]
        self.assertIn("data master", uitsluitingen)
        self.assertGreaterEqual(len(uitsluitingen), 1)

    def test_US015_c1_uitgesloten_tekst_telt_niet_mee_als_treffer(self):
        self.assertIsNone(categorie_van("Asustor Data Master", ""))
        self.assertEqual(categorie_van("Nieuwe Data Master-firmware", "database"), "Data",
                         "losse 'data' buiten de uitsluiting moet nog wel tellen")

    def test_US015_c2_firmware_met_data_master_krijgt_niet_categorie_data(self):
        ruw = [{"titel": "Firmware-update - Asustor ADM 5.1.4.RM62",
                "link": "https://voorbeeld-bron.example/firmware-adm-5-1-4",
                "samenvatting_html": "Asustor Data Master krijgt nieuwe functies",
                "datum": datetime.date(2026, 10, 8)}]
        feed = {"naam": "Fixture", "taal": "nl"}
        uit, zonder_titel, zonder_cat = o.verwerk_items(ruw, feed, MATCHERS, datetime.date(2026, 10, 8))
        self.assertTrue(all(i["categorie"] != "Data" for i in uit), "item kreeg categorie Data: %s" % uit)
        self.assertEqual(len(uit) + zonder_cat, 1)

    def test_US015_c3_minstens_15_trefwoorden_per_categorie_nl_en(self):
        nl_markers = {
            "AI": {"kunstmatige intelligentie", "generatieve", "neurale", "machinaal leren", "taalmodel*", "chatbot*"},
            "Automatisering": {"geautomati*", "robotisering", "procesoptimalisatie", "bedrijfsprocessen", "automati*"},
            "Data": {"gegevens", "datagedreven", "datakwaliteit", "databeheer", "statistiek", "rapportage*"},
        }
        en_markers = {
            "AI": {"machine learning", "large language model*", "generative", "neural", "agentic"},
            "Automatisering": {"workflow*", "robotic process", "orchestrat*", "business process*", "low-code"},
            "Data": {"analytics", "database*", "data warehouse*", "big data", "data science"},
        }
        for cat in ["Data", "Automatisering", "AI"]:
            woorden = CFG["trefwoorden"][cat]
            self.assertGreaterEqual(len(woorden), 15, "%s heeft %d trefwoorden" % (cat, len(woorden)))
            self.assertTrue(nl_markers[cat] & set(woorden), "%s: geen Nederlands trefwoord" % cat)
            self.assertTrue(en_markers[cat] & set(woorden), "%s: geen Engels trefwoord" % cat)

    def test_US015_c4_vaste_testset_minstens_20_titels_min_5_per_categorie_en_3_echte(self):
        per_cat = {}
        for _, _, cat, echt in TESTSET:
            if cat is not None:
                per_cat[cat] = per_cat.get(cat, 0) + 1
        self.assertGreaterEqual(len([t for t in TESTSET if t[2] is not None]), 20)
        for cat in ["Data", "Automatisering", "AI"]:
            self.assertGreaterEqual(per_cat.get(cat, 0), 5, "te weinig testtitels voor %s" % cat)
        self.assertGreaterEqual(len([t for t in TESTSET if t[3]]), 3, "minstens 3 echte titels nodig")

    def test_US015_c4_elke_testtitel_krijgt_de_verwachte_categorie(self):
        fouten = []
        for titel, sam, verwacht, _ in TESTSET:
            gevonden = categorie_van(titel, sam)
            if gevonden != verwacht:
                fouten.append("%r: verwacht %s, kreeg %s" % (titel[:70], verwacht, gevonden))
        self.assertEqual(fouten, [], "\n".join(fouten))



# Fixronde iteratie 4 (US-015 c6): echte titels uit de ronde van 8 okt 2026 die NIET in de genoemde categorie mogen.
# Samenvattingen: de Tweakers- en Colt-tekst is de platte tekst (max 300 tekens) zoals ophalen.py die opslaat, uit de
# feed op 8 okt 2026 (in de testtekst is de samenvatting ongewijzigd overgenomen); de Uber- en SageMaker-samenvatting
# staan letterlijk in data/nieuws.json.
ECHTE_TITELS_NIET = [
    ("Laptops met Nvidia RTX Spark-processor kosten in Nederland minstens 2999 euro",
     "Laptops met Nvidia RTX Spark-processors zijn in Nederland te koop vanaf 2999 euro. Dat blijkt uit listings van "
     "Megekko en Coolblue. De versies met het meeste geheugen en de krachtigste chip kosten meer dan 6000 euro. Ze "
     "worden later deze maand geleverd.", "Data"),
    ("Instapversie Microsoft Surface-laptop met Nvidia RTX Spark-cpu kost 2600 dollar",
     "Microsoft en Nvidia deelden op woensdagavond meer details over de aanstaande Nvidia RTX Spark-processor. Laptops "
     "met deze chip zijn vanaf nu vooruit te bestellen en worden vanaf volgende week vrijdag geleverd. Microsofts "
     "goedkoopste variant kost 2600 dollar.", "Data"),
    ("Colt brengt SCION als managed netwerkdienst naar Europa",
     "Colt Technology Services brengt SCION op de markt als volledig beheerde netwerkdienst in Europa, Noord-Amerika en "
     "Azië. Met de technologie van het Zwitserse Anapaya bepalen organisaties zelf welke route hun data aflegt. Colt "
     "richt zich op sectoren met gevoelige, gereguleerde of bedrijfskritische...", "Data"),
    ("Uber Eats Rebuilds Search Pipeline to Cut End-to-End Latency by 50%",
     "Uber has rebuilt major parts of the Uber Eats search pipeline, reporting a 50% reduction in end-to-end latency. "
     "Changes include Above-the-Fold measurement, reduced retrieval work, parallel hydration, advertising data redesign, "
     "infrastructure optimizations, and an agentic coding workflow. Uber is...", "Automatisering"),
]
ECHTE_TITEL_AI = (
    "Manage Amazon SageMaker HyperPod Spaces directly from SageMaker Studio",
    "Data scientists and ML engineers can now create, configure, start, stop, and open Amazon SageMaker Spaces on "
    "SageMaker HyperPod EKS clusters directly from SageMaker Studio. Launch JupyterLab and Code Editor environments in a "
    "few clicks, without using command-line tools.",
)


# Fixronde 2 iteratie 4 (US-015 c9): de Archestra-titel met de echte samenvatting uit de ophaalronde van 8 okt 2026
# (uit een tijdelijke snapshot, letterlijk). Die krijgt NIET Automatisering; het losse "workflow(s)" telt niet.
ARCHESTRA_TITEL = "New Archestra's OpenAPPA Saturates Two Major Security Benchmarks with a 0% Attack Success Rate"
ARCHESTRA_SAMENVATTING = (
    "Archestra released OpenAPPA, an open-source security engine designed to stop data exfiltration caused by prompt "
    "injection or model hallucination. The team reports zero successful attacks when running security benchmarks "
    "Bench-Corp (20 multi-step enterprise workflows) and AgentThreatBench, versus..."
)

# Fixronde 2 iteratie 4 (US-015 c10): specifieke Data-termen uit de criteriumlijst; per term de varianten in de config.
C10_TERMEN = [
    ("dataset", ["dataset*"]),
    ("data engineering", ["data engineering"]),
    ("data lake", ["data lake*", "datalake*"]),
    ("data warehouse / datawarehouse", ["data warehouse*", "datawarehouse*"]),
    ("SQL", ["sql"]),
    ("analytics / data-analyse", ["analytics", "data-analyse"]),
    ("ETL", ["etl"]),
    # it. 6 (BACKLOG US-015, notitie): "business intelligence" en "Power BI" zijn BI-termen en tellen hier niet meer mee.
    ("Databricks", ["databricks"]),
    ("Snowflake", ["snowflake"]),
    ("dbt", ["dbt"]),
    ("pandas", ["pandas"]),
    ("datakwaliteit", ["datakwaliteit"]),
    ("data governance", ["data governance", "datagovernance"]),
    ("datamodel", ["datamodel*", "data model*"]),
]
# Extra testtitels: elk via een andere specifieke Data-term (staan ook in TESTSET).
C10_EXTRA = [
    ("Een nieuwe dataset voor weerdata is gratis beschikbaar", "dataset"),
    ("Data engineering-teams krijgen een eigen platform", "data engineering"),
    ("Hoe een data lake bij een bank wordt opgezet", "data lake"),
    ("SQL-cursus voor beginners", "sql"),
    ("ETL-pijplijnen vereenvoudigen met een nieuwe tool", "etl"),
    ("Databricks brengt een nieuwe versie van zijn dataplatform uit", "Databricks"),
]


class TestUS015C9C10(unittest.TestCase):
    # c9: Archestra-titel niet Automatisering; los "workflow" telt niet; specifieke vormen wel (elk een testtitel)
    def test_US015_c9_archestra_titel_met_echte_samenvatting_is_niet_automatisering(self):
        self.assertNotEqual(categorie_van(ARCHESTRA_TITEL, ARCHESTRA_SAMENVATTING), "Automatisering")

    def test_US015_c9_los_workflow_of_workflows_telt_niet_als_automatisering(self):
        for titel in ["Workflows worden steeds slimmer", "Een workflow voor de redactie", "Multi-step workflows in de cloud"]:
            self.assertNotEqual(categorie_van(titel, ""), "Automatisering", titel)

    def test_US015_c9_workflow_automation_telt_als_automatisering(self):
        self.assertEqual(categorie_van("Workflow automation voor de finance-afdeling", ""), "Automatisering")

    def test_US015_c9_workflowautomatisering_telt_als_automatisering(self):
        self.assertEqual(categorie_van("Workflowautomatisering wint terrein bij mkb", ""), "Automatisering")

    def test_US015_c9_workflow_automatisering_met_koppelteken_telt_als_automatisering(self):
        self.assertEqual(categorie_van("Workflow-automatisering kost minder tijd", ""), "Automatisering")

    # c10: config bevat minstens 10 van de specifieke Data-termen; extra testtitels via andere termen
    def test_US015_c10_config_bevat_minstens_10_specifieke_data_termen(self):
        data_kw = [w.casefold() for w in CFG["trefwoorden"]["Data"]]
        aanwezig = [naam for naam, varianten in C10_TERMEN if any(v.casefold() in data_kw for v in varianten)]
        self.assertGreaterEqual(len(aanwezig), 10, "alleen aanwezig: %s" % aanwezig)

    def test_US015_c10_losse_data_is_niet_in_config_als_data_term(self):
        self.assertNotIn("data", [w.casefold() for w in CFG["trefwoorden"]["Data"]])

    def test_US015_c10_minstens_5_extra_titels_elk_via_andere_specifieke_term_data(self):
        self.assertGreaterEqual(len(C10_EXTRA), 5)
        termen = [t for _, t in C10_EXTRA]
        self.assertEqual(len(set(termen)), len(termen), "elke extra titel moet via een andere term Data krijgen")
        testtitels = {t[0] for t in TESTSET}
        data_kw = [w.casefold() for w in CFG["trefwoorden"]["Data"]]
        for titel, term in C10_EXTRA:
            self.assertIn(titel, testtitels, "extra titel staat niet in de vaste testset")
            varianten = [v for naam, vs in C10_TERMEN if naam.split(" / ")[0].casefold() == term.casefold() for v in vs]
            self.assertTrue(any(v.casefold() in data_kw for v in varianten), "term ontbreekt in config: %s" % term)
            self.assertEqual(categorie_van(titel, ""), "Data", titel)


class TestUS015Fixronde(unittest.TestCase):
    # c6: echte titels krijgen NIET de genoemde categorie (ook in de eigen testset van de Tester)
    def test_US015_c6_echte_titels_niet_in_de_verkeerde_categorie(self):
        fouten = []
        for titel, sam, verkeerd in ECHTE_TITELS_NIET:
            gevonden = categorie_van(titel, sam)
            if gevonden == verkeerd:
                fouten.append("%r: mag niet %s zijn, is wel %s" % (titel[:70], verkeerd, gevonden))
        self.assertEqual(fouten, [], "\n".join(fouten))

    def test_US015_c6_manage_sagemaker_hyperpod_spaces_is_ai_en_niet_data(self):
        titel, sam = ECHTE_TITEL_AI
        self.assertEqual(categorie_van(titel, sam), "AI")

    def test_US015_c6_losse_data_telt_niet_meer_als_categorie(self):
        self.assertIsNone(categorie_van("Data van de week", ""), "losse 'data' mag geen categorie Data geven (besluit it4)")
        self.assertIsNone(categorie_van("Nieuwe data-regels in de app", ""))


if __name__ == "__main__":
    unittest.main()
