"""Acceptatietests US-013 c2, c4 en c5 (workflow-bestand, geheimenscan en README-stappen). Geen internet.

Buiten scope van deze iteratie en dus NIET hier getest: US-013 c1 (site bereikbaar op github.io) en c3
(Laatst bijgewerkt op de live site). Die wachten op het hosting-account van Stef.

- c2: dagelijkse cron rond 06:00 Nederlandse tijd en handmatig te starten (workflow_dispatch). De job draait
  het ophaal- en het bouwcommando (volgorde gecontroleerd).
- c4: geen wachtwoorden, tokens of sleutels in de repository (scan van alle tekstbestanden in de projectmap).
- c5: de README beschrijft hoe Stef feeds toevoegt/verwijdert en hoe hij de job handmatig start.
"""
import os
import re
import sys
import unittest

import hulp_statisch as h

sys.dont_write_bytecode = True
WORKFLOW = os.path.join(h.ROOT, ".github", "workflows", "nieuws.yml")
README = os.path.join(h.ROOT, "README.technisch.md")  # was README.md; nu de lokale technische README (feeds, job, online zetten)
ZELF = os.path.normcase(os.path.abspath(__file__))

# Patronen van echte geheimen. Regex-tekst staat zo opgeschreven dat hij zichzelf niet raakt.
GEHEIM_PATRONEN = {
    "GitHub-token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "GitHub fine-grained token": r"github" r"_pat_[A-Za-z0-9_]{20,}",  # gesplitst: zo staat het prefix niet letterlijk in dit bestand
    "AWS-sleutel": r"AKIA[0-9A-Z]{16}",
    # "sk-" alleen als los begin van een woord/token (niet midden in een slug zoals "amazon-msk-with-...")
    "OpenAI/Anthropic-achtige sleutel": r"(?<![A-Za-z0-9_/-])sk-[A-Za-z0-9_-]{20,}",
    "privesleutel": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Slack-token": r"xox[abprs]-[A-Za-z0-9-]{10,}",
    "Google API-sleutel": r"AIza[0-9A-Za-z_-]{35}",
    "wachtwoord/sleutel in toekenning": r"(?i)\b(password|passwd|wachtwoord|api[_-]?key|client_secret|access[_-]?token|auth[_-]?token|secret)\b\s*[:=]\s*['\"][^'\"\s]{6,}['\"]",
    "inloggegevens in URL": r"https?://[^/\s:@]+:[^/\s@]+@",
    "geheim in URL-parameter": r"[?&](token|apikey|api_key|sig|signature|auth|secret)=[^&\s\"']{8,}",
}
OVERSLAAN_MAPPEN = {".git", "__pycache__", ".venv", "node_modules"}


def tekstbestanden():
    for dirpad, mappen, bestanden in os.walk(h.ROOT):
        mappen[:] = [m for m in mappen if m not in OVERSLAAN_MAPPEN]
        for naam in bestanden:
            pad = os.path.join(dirpad, naam)
            if os.path.normcase(os.path.abspath(pad)) == ZELF:
                continue  # dit testbestand bevat de patronen zelf
            if os.path.getsize(pad) > 5 * 1024 * 1024:
                continue
            with open(pad, "rb") as f:
                ruw = f.read()
            if b"\x00" in ruw:
                continue  # binair (bijv. favicon.ico, git-bestanden)
            yield pad, ruw.decode("utf-8", "replace")


class TestUS013Workflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(WORKFLOW, encoding="utf-8") as f:
            cls.yml = f.read()

    def test_US013_c2_cron_dagelijks_rond_zes_uur_nederlandse_tijd(self):
        m = re.search(r'^\s*-\s*cron:\s*"([^"]+)"', self.yml, re.M)
        self.assertIsNotNone(m, "geen cron-schema in het workflow-bestand")
        minuut, uur, dag, maand, weekdag = m.group(1).split()
        self.assertEqual((dag, maand, weekdag), ("*", "*", "*"), "moet dagelijks draaien")
        self.assertEqual(minuut, "0")
        # 04:00 UTC = 06:00 Nederlandse zomertijd (de cron is in UTC; in de winter is dat 05:00, zie workflow-commentaar).
        self.assertEqual(uur, "4", "uur in UTC moet 4 zijn (06:00 NL zomertijd)")

    def test_US013_c2_handmatig_te_starten(self):
        self.assertRegex(self.yml, r"(?m)^\s*workflow_dispatch:")

    def test_US013_c2_job_draait_ophalen_en_bouwen_in_die_volgorde(self):
        ophalen = self.yml.find("python src/ophalen.py")
        bouwen = self.yml.find("python src/bouw.py")
        self.assertGreater(ophalen, 0, "ophaalcommando ontbreekt in de job")
        self.assertGreater(bouwen, ophalen, "bouwcommando moet na het ophalen komen")

    def test_US013_c2_geen_geheimen_en_minimale_rechten(self):
        self.assertNotIn("secrets.", self.yml, "de job gebruikt een geheim; dat moet niet nodig zijn")
        self.assertNotIn("write-all", self.yml)
        self.assertRegex(self.yml, r"contents:\s*write", "schrijfrecht voor data/nieuws.json ontbreekt")

    def test_US013_c2_publiceren_pas_na_bouwen(self):
        self.assertRegex(self.yml, r"(?m)^\s*needs:\s*bouwen\s*$")

    def test_US013_c4_geen_wachtwoorden_tokens_of_sleutels_in_repository(self):
        gevonden = []
        bestanden = 0
        for pad, tekst in tekstbestanden():
            bestanden += 1
            for naam, patroon in GEHEIM_PATRONEN.items():
                for m in re.finditer(patroon, tekst):
                    regel = tekst.count("\n", 0, m.start()) + 1
                    gevonden.append("%s:%d (%s)" % (os.path.relpath(pad, h.ROOT), regel, naam))
        self.assertGreater(bestanden, 10, "scan heeft te weinig bestanden gezien")
        self.assertEqual(gevonden, [], "mogelijke geheimen gevonden")

    def test_US013_c4_mutatie_sleutelpatroon_vangt_echte_sleutels_en_negeert_slug(self):
        # Mutatietest (it. 4 fixronde 2): het sk-patroon moet realistische sleutels vangen
        # en mag de URL-slug "amazon-msk-with-next-generation-protocol" niet meer als vals alarm geven.
        patroon = GEHEIM_PATRONEN["OpenAI/Anthropic-achtige sleutel"]
        echte = [
            "OPENAI_API_KEY=sk-proj-AbC123xyZ987qwerTYuiop_-56",
            '"sk-ant-api03-Qw3rTy7UiOp9AsDf2GhJkL4zXcVbNm"',
            "Authorization: Bearer sk-proj-9fK2mP7qR4tZ8vB1nC6xW0",
            "key: sk-Lm4Nb7Vc2Xz9Qw1Er6Ty8Ui",
            "(sk-XyZ1234567890abcdefGHIJ)",
        ]
        slugs = [
            "https://aws.amazon.com/blogs/big-data/optimize-consumer-rebalancing-on-amazon-msk-with-next-generation-protocol/",
            "risk-management-platform-for-sk-hynix-chips-overview-2026",
        ]
        for s in echte:
            self.assertRegex(s, patroon, "echte sleutel wordt niet meer gevangen: %s" % s)
        for s in slugs:
            self.assertNotRegex(s, patroon, "vals alarm op URL-slug: %s" % s)

    def test_US013_c4_geen_geheim_in_configuratie_of_data_urls(self):
        import json
        with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
            cfg = json.load(f)
        for feed in cfg["feeds"]:
            self.assertNotRegex(feed["url"], r"[?&](token|key|apikey|sig|auth)=", feed["naam"])


class TestUS013Readme(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(README, encoding="utf-8") as f:
            cls.readme = f.read()

    def test_US013_c5_readme_feeds_toevoegen_en_verwijderen(self):
        self.assertIn("Feeds beheren", self.readme)
        self.assertIn("config/feeds.json", self.readme)
        blok = self.readme.split("Feeds beheren", 1)[1].split("Tests draaien", 1)[0].lower()
        # Toevoegen gebeurt door de lijst 'feeds' aan te passen met naam, url en taal (zo staat het in de README).
        # Het woord 'toevoegen' ontbreekt; dat is een KLEIN verbeterpunt, geen criteriumfout.
        for woord in ["naam", "url", "taal", "pas de lijst", "verwijderen"]:
            self.assertIn(woord, blok, woord)

    def test_US013_c5_readme_job_handmatig_starten(self):
        self.assertIn("Job handmatig starten", self.readme)
        regel = [r for r in self.readme.splitlines() if "Job handmatig starten" in r][0]
        self.assertIn("Actions", regel)
        self.assertIn("Run workflow", regel)

    def test_US013_c5_readme_stappen_online_zetten(self):
        for stap in ["Pages", "Source: GitHub Actions", "Workflow permissions", "Read and write permissions",
                     "openbaar", "git push"]:  # it. 7: README-zin "De repo moet openbaar zijn" (predicatief); was "openbare"
            self.assertIn(stap, self.readme, stap)


if __name__ == "__main__":
    unittest.main()
