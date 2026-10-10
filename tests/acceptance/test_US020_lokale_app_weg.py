"""Acceptatietests US-020 (lokale app verwijderd; de repo bevat alleen het nieuws), iteratie 7.

- c1 bestanden: src/app.py en src/data.py bestaan niet meer; in src/, tests/, config/ en README.md komen geen
  leadwoorden (hele woorden) voor. Lijst met verzonnen bedrijfsnamen: NIET GETEST (de oude data is verwijderd).
- c2 src: geen bestand importeert http.server of een verwijderde module (app, data, logica).
- c3 verse checkout: een kopie van de projectmap zonder site/ en zonder data/ draait ophalen (lokale testfeeds),
  bouwen, veilig_check en de unittests zonder ImportError en zonder internet.
- c4 README: geen startinstructie meer voor de lokale app; wel ophalen, bouwen, lokaal bekijken met een statische
  server, feeds aanpassen en publiceren.

Geen internet: de feeds zijn lokale testfeeds op 127.0.0.1. De kopie staat in de tijdelijke map van het systeem.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import hulp_statisch as h
import hulp_feeds as hf

sys.dont_write_bytecode = True
LEAD_WOORD = re.compile(r"\bleads?\b", re.I)
TEKST_SUFFIXEN = (".py", ".md", ".json", ".yml", ".yaml", ".txt", ".html", ".js", ".css")
ZELF = os.path.basename(__file__)
# Vaste uitzonderingslijst (regel vastgelegd in tests/acceptance/README.md, sectie "Regel: het woord lead"; besluit
# Stef, iteratie 8). Het woord 'lead' mag ALLEEN in deze drie bestanden voorkomen: de controle zelf, de zoektermen
# van de statische-site-tests en de documentatie. Sleutel = pad vanaf de projectmap. Alleen bestaande bestanden.
# Verwijderde bestanden (test_acceptance.py, test_browser_layout.py, test_echte_data_app.py) staan hier niet meer in.
EXEMPT_TESTBESTANDEN = {
    "tests/acceptance/test_US020_lokale_app_weg.py": "de controle zelf (zoekpatroon en uitzonderingslijst)",
    "tests/acceptance/test_US012_statische_site.py": "controles op afwezige leadlinks en -velden (zoektermen in strings)",
    "tests/acceptance/README.md": "documentatie van de testsuite (regel over het woord lead, testhistorie)",
}


def bestanden_in(mappen):
    """Alle tekstbestanden in de opgegeven mappen (relatief aan de projectmap), zonder caches."""
    gevonden = []
    for map_ in mappen:
        pad = os.path.join(h.ROOT, map_)
        if os.path.isfile(pad):
            gevonden.append(pad)
            continue
        for dirpad, dirnamen, bestandsnamen in os.walk(pad):
            dirnamen[:] = [d for d in dirnamen if d != "__pycache__"]
            for naam in bestandsnamen:
                if naam.endswith(TEKST_SUFFIXEN):
                    gevonden.append(os.path.join(dirpad, naam))
    return gevonden


def lees(pad):
    with open(pad, encoding="utf-8", errors="replace") as f:
        return f.read()


class TestUS020C1Bestanden(unittest.TestCase):
    def test_US020_c1_app_py_en_data_py_bestaan_niet(self):
        self.assertFalse(os.path.exists(os.path.join(h.ROOT, "src", "app.py")), "src/app.py bestaat nog")
        self.assertFalse(os.path.exists(os.path.join(h.ROOT, "src", "data.py")), "src/data.py bestaat nog")

    def test_US020_c1_geen_leadwoorden_in_src_config_en_readme(self):
        # README.md (publiek) EN README.technisch.md (lokaal) beide controleren (was: alleen README.md)
        for pad in bestanden_in(["src", "config", "README.md", "README.technisch.md"]):
            for regel_nr, regel in enumerate(lees(pad).splitlines(), 1):
                self.assertIsNone(LEAD_WOORD.search(regel),
                                  "leadwoord in %s regel %d" % (os.path.relpath(pad, h.ROOT), regel_nr))

    def test_US020_c1_geen_leadstatussen_in_src_config_en_readme(self):
        patroon = re.compile(r"in behandeling|niet interessant", re.I)
        for pad in bestanden_in(["src", "config", "README.md", "README.technisch.md"]):
            self.assertIsNone(patroon.search(lees(pad)), "leadstatus in %s" % os.path.relpath(pad, h.ROOT))

    def test_US020_c1_geen_leadwoorden_in_tests(self):
        """Tests: de hele woorden lead/leads worden gecontroleerd. Uitzonderingen (EXEMPT_TESTBESTANDEN) zijn
        bestanden die de afwezigheid van leadwoorden zelf controleren of vervallen zijn; die staan gedocumenteerd
        in tests/acceptance/README.md (zie test_US020_c1_uitzonderingen_zijn_gedocumenteerd)."""
        for pad in bestanden_in(["tests"]):
            rel = os.path.relpath(pad, h.ROOT).replace(os.sep, "/")
            if rel in EXEMPT_TESTBESTANDEN:
                continue
            for regel_nr, regel in enumerate(lees(pad).splitlines(), 1):
                self.assertIsNone(LEAD_WOORD.search(regel), "leadwoord in %s regel %d" % (rel, regel_nr))

    def test_US020_c1_uitzonderingen_zijn_gedocumenteerd(self):
        readme = lees(os.path.join(h.ROOT, "tests", "acceptance", "README.md"))
        self.assertIn("Regel: het woord lead", readme, "regel over het woord 'lead' ontbreekt in tests/acceptance/README.md")
        for rel in EXEMPT_TESTBESTANDEN:
            self.assertTrue(os.path.isfile(os.path.join(h.ROOT, *rel.split("/"))),
                            "uitzondering verwijst naar een bestand dat niet bestaat: %s" % rel)
            self.assertIn(os.path.basename(rel), readme,
                          "uitzondering niet gedocumenteerd in tests/acceptance/README.md: %s" % rel)


class TestUS020C2Src(unittest.TestCase):
    def test_US020_c2_geen_http_server_of_verwijderde_modules_in_src(self):
        for naam in sorted(os.listdir(os.path.join(h.ROOT, "src"))):
            if not naam.endswith(".py"):
                continue
            tekst = lees(os.path.join(h.ROOT, "src", naam))
            self.assertNotIn("http.server", tekst, "%s importeert http.server" % naam)
            self.assertIsNone(re.search(r"^\s*(import|from)\s+(app|data|logica)\b", tekst, re.M),
                              "%s importeert een verwijderde module" % naam)

    def test_US020_c2_src_bevat_alleen_ophalen_bouwen_mix_en_veilig_check(self):
        namen = sorted(n for n in os.listdir(os.path.join(h.ROOT, "src")) if n.endswith(".py"))
        self.assertEqual(namen, ["bouw.py", "mix.py", "ophalen.py", "veilig_check.py"], "onverwachte bestanden in src/")


class TestUS020C3VerseCheckout(unittest.TestCase):
    """Verse checkout = een kopie van de projectmap zonder site/ en zonder data/ (geen opgehaalde data).
    Alles draait tegen lokale testfeeds; geen internet."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="it7-verse-")
        cls.kopie = os.path.join(cls.tmp, "checkout")
        # data/nieuws.json hoort in git (README); de kopie bevat het dus. site/ en caches horen er niet bij.
        negeer = shutil.ignore_patterns("site", ".git", "__pycache__", "*.pyc")
        shutil.copytree(h.ROOT, cls.kopie, ignore=negeer)
        cls.resultaten = {}
        cls.uitvoer = {}
        cls._draai_alles()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def _run(cls, args, naam, timeout=180):
        res = subprocess.run([sys.executable, "-B"] + args, cwd=cls.kopie, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", env=h.omgeving(), timeout=timeout)
        cls.resultaten[naam] = res.returncode
        cls.uitvoer[naam] = res.stdout + res.stderr
        return res

    @classmethod
    def _draai_alles(cls):
        with hf.FeedServer({"/rss.xml": {"body": hf.rss_feed}, "/atom.xml": {"body": hf.atom_feed}}) as srv:
            feeds = [{"naam": "Testfeed RSS", "url": srv.base + "/rss.xml", "taal": "nl"},
                     {"naam": "Testfeed Atom", "url": srv.base + "/atom.xml", "taal": "en"}]
            cfg = hf.schrijf_config(os.path.join(cls.tmp, "cfg.json"), feeds)
            uit = os.path.join(cls.tmp, "nieuws.json")
            cls._run(["src/ophalen.py", "--config", cfg, "--uitvoer", uit, "--geen-robots"], "ophalen")
        cls.data_pad = uit
        cls._run(["src/bouw.py", "--data", uit, "--uit", os.path.join(cls.tmp, "site")], "bouwen")
        cls._run(["src/veilig_check.py"], "veilig_check")
        cls._run(["-m", "unittest", "discover", "-s", "tests"], "unittests", timeout=300)

    def test_US020_c3_ophalen_werkt_zonder_app_bestanden(self):
        self.assertEqual(self.resultaten["ophalen"], 0, self.uitvoer["ophalen"])
        self.assertNotIn("ImportError", self.uitvoer["ophalen"])
        self.assertTrue(os.path.exists(self.data_pad))

    def test_US020_c3_bouwen_werkt_zonder_app_bestanden(self):
        self.assertEqual(self.resultaten["bouwen"], 0, self.uitvoer["bouwen"])
        self.assertNotIn("ImportError", self.uitvoer["bouwen"])
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "site", "index.html")))

    def test_US020_c3_veilig_check_exitcode_0_in_verse_checkout(self):
        self.assertEqual(self.resultaten["veilig_check"], 0, self.uitvoer["veilig_check"])

    def test_US020_c3_unittests_draaien_in_verse_checkout_zonder_importfout(self):
        self.assertNotIn("ImportError", self.uitvoer["unittests"], self.uitvoer["unittests"][-2000:])
        self.assertEqual(self.resultaten["unittests"], 0, self.uitvoer["unittests"][-3000:])


class TestUS020C4Readme(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # was: README.md. Ophalen/bouwen/bekijken/feeds/publiceren staat in de lokale technische README.
        cls.readme = lees(os.path.join(h.ROOT, "README.technisch.md"))
        # De publieke README mag ook geen startinstructie voor de lokale app bevatten (extra controle).
        cls.publiek = lees(os.path.join(h.ROOT, "README.md"))

    def test_US020_c4_geen_startinstructie_voor_lokale_app(self):
        for naam, tekst in [("README.technisch.md", self.readme), ("README.md", self.publiek)]:
            self.assertIsNone(re.search(r"src/app\.py|src\\app\.py", tekst), "%s noemt nog src/app.py" % naam)
            self.assertNotIn("GEEN_BROWSER", tekst, naam)
            self.assertIsNone(re.search(r"python\s+src/app", tekst), naam)

    def test_US020_c4_readme_beschrijft_ophalen_bouwen_bekijken_feeds_en_publiceren(self):
        for tekst in ["python src/ophalen.py", "python src/bouw.py", "http.server", "config/feeds.json",
                      "Online zetten", "Feeds beheren"]:
            self.assertIn(tekst, self.readme, "README.technisch.md mist: %s" % tekst)


if __name__ == "__main__":
    unittest.main()
