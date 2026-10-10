"""Acceptatietests README-splitsing (iteratie 8, ronde 1, op verzoek van Stef). Geen internet.

- c1 publieke README.md: geen lokale paden (letter-schijf, /Users/, cloudmap van de gebruiker, bureaubladmap).
- c2 publieke README.md: geen werkafspraken, geen rollen (Claude, Bouwer, Tester, PO), geen testcommando's.
- c3 publieke README.md: bevat de site-link https://steflennips.github.io/Nieuws/ en de onderdelen Overzicht, Nieuws, Bronnen.
- c4 publieke README.md: geen persoonlijk account buiten de site-link en de bedrijfsnaam in de titel (exact toegestaan).
- c5 README.technisch.md staat in .gitignore (lokaal, niet naar GitHub).
- c6 python src/veilig_check.py geeft exitcode 0 en de OK-regel.

Bron: opdracht Stef/PO (readme-splitsing), niet als apart criterium in docs/BACKLOG.md.
"""
import os
import re
import subprocess
import sys
import unittest

import hulp_statisch as h
import hulp_feeds as hf

sys.dont_write_bytecode = True
PUBLIEK = os.path.join(h.ROOT, "README.md")
TECHNISCH = os.path.join(h.ROOT, "README.technisch.md")
GITIGNORE = os.path.join(h.ROOT, ".gitignore")
VEILIG = os.path.join(h.ROOT, "src", "veilig_check.py")
SITE_LINK = "https://steflennips.github.io/Nieuws/"
BEDRIJFSNAAM = "Deux2qonnect"


def lees(pad):
    with open(pad, encoding="utf-8") as f:
        return f.read()


PUBLIEKE_TEKST = lees(PUBLIEK)


class TestPubliekeReadme(unittest.TestCase):
    def test_README_splitsing_c1_publieke_readme_geen_lokale_paden(self):
        verboden = [r"(?<![A-Za-z])[A-Za-z]:\\", r"(?<![A-Za-z])[A-Za-z]:/(?!/)", r"/Users/", r"\\Users\\",
                    r"One" r"Drive", r"Desk" r"top", r"Bureau" r"blad"]  # gesplitst: veilig_check meldt de letterlijke tekst
        gevonden = [v for v in verboden if re.search(v, PUBLIEKE_TEKST, re.I)]
        self.assertEqual(gevonden, [], "publieke README bevat een lokaal pad of map-naam")

    def test_README_splitsing_c2_publieke_readme_geen_werkafspraken_of_rollen(self):
        verboden = [r"claude", r"bouwer", r"tester", r"product owner", r"orkestrator", r"subagent", r"\brollen?\b",
                    r"unittest", r"pytest", r"python -m", r"python src/", r"tests/", r"docs/", r"iteratie",
                    r"backlog", r"status\.md", r"claude\.md", r"veilig_check", r"\bsrc/"]
        gevonden = [v for v in verboden if re.search(v, PUBLIEKE_TEKST, re.I)]
        self.assertEqual(gevonden, [], "publieke README bevat een werkafspraak, rol of testcommando")

    def test_README_splitsing_c3_publieke_readme_bevat_site_link_en_onderdelen(self):
        self.assertIn(SITE_LINK, PUBLIEKE_TEKST, "site-link ontbreekt in de publieke README")
        for onderdeel in ["Overzicht", "Nieuws", "Bronnen"]:
            self.assertIn(onderdeel, PUBLIEKE_TEKST, "onderdeel %s ontbreekt in de publieke README" % onderdeel)

    def test_README_splitsing_c4_geen_persoonlijk_account_buiten_toegestane_tekst(self):
        # Alleen de exacte site-link en de bedrijfsnaam mogen voorkomen; de rest van het accountspoor is verboden.
        rest = PUBLIEKE_TEKST.replace(SITE_LINK, "").replace(BEDRIJFSNAAM, "")
        gevonden = [v for v in ["steflennips", "deux2qonnect"] if re.search(v, rest, re.I)]
        self.assertEqual(gevonden, [], "publieke README noemt een persoonlijk account buiten de site-link")


class TestTechnischeReadme(unittest.TestCase):
    def test_README_splitsing_c5_technische_readme_staat_in_gitignore(self):
        regels = [r.strip() for r in lees(GITIGNORE).splitlines()]
        self.assertIn("README.technisch.md", regels, "README.technisch.md staat niet in .gitignore")

    def test_README_splitsing_c5_technische_readme_bestaat_lokaal(self):
        self.assertTrue(os.path.isfile(TECHNISCH), "README.technisch.md ontbreekt lokaal (nodig voor de technische tests)")


class TestVeiligheidscontrole(unittest.TestCase):
    def test_README_splitsing_c6_veilig_check_exitcode_0(self):
        r = subprocess.run([sys.executable, "-B", VEILIG], cwd=h.ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=hf.omgeving(), timeout=180)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("OK: geen geheimen, e-mailadressen, lokale paden of verdachte bestanden gevonden.", r.stdout)


if __name__ == "__main__":
    unittest.main()
