"""Eigen tests fixronde 2 iteratie 6: evenementen, Vaknieuws max 2 AI, "Kort:", ongeldige --vandaag, geweigerd-telling."""
import json
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "src"))
import mix  # noqa: E402

CFG = json.loads((BASIS / "config" / "feeds.json").read_text(encoding="utf-8"))
VANDAAG = date(2026, 10, 9)


def item(titel, cat="BI", datum="2026-10-08", bron="Techzine", sam=""):
    return {"titel": titel, "categorie": cat, "bron": bron, "datum": datum, "samenvatting": sam, "url": "https://x.nl/" + titel[:10]}


class TestEvenementen(unittest.TestCase):
    def test_config_termen(self):
        t = [x.casefold() for x in CFG["evenement_termen"]]
        for w in ["evenement", "conferentie", "congres", "summit", "world forum", "meld je aan", "aanmelden", "inschrijven"]:
            self.assertIn(w, t)
        self.assertNotIn("event", t)

    def test_techzine_titel_niet_in_blokken(self):
        data = json.loads((BASIS / "data" / "nieuws.json").read_text(encoding="utf-8"))
        echt = [i for i in data["items"] if i["titel"].startswith("Begin bij het einde")]
        if not echt:
            self.skipTest("titel niet meer in data/nieuws.json")
        e = echt[0]
        normaal = item("Power BI nieuws voor het MKB", bron="Techzine")
        items = [e, normaal]
        u = mix.uitgelicht(items, CFG, VANDAAG)
        self.assertNotIn(e, u)
        self.assertIn(normaal, u)
        self.assertNotIn(e, mix.vaknieuws(items, u, CFG))

    def test_term_in_samenvatting_en_hele_woorden(self):
        ev = item("Iets", sam="Meld je aan voor ons Summit")
        ok = item("Eventueel nieuws over Power BI")
        u = mix.uitgelicht([ev, ok], CFG, VANDAAG)
        self.assertEqual(u, [ok])


class TestVaknieuws(unittest.TestCase):
    def test_max_2_ai_aanvullen_en_kort(self):
        ai = [item("AI nieuws %d" % n, "AI", "2026-10-0%d" % (9 - n % 3)) for n in range(6)]
        kort = item("Kort: allerlei", "BI", "2026-10-09")
        rest = [item("Data bericht %d" % n, "Data", "2026-09-%02d" % (10 + n)) for n in range(4)]
        items = ai + [kort] + rest
        v = mix.vaknieuws(items, [], CFG)
        self.assertEqual(len(v), 5)
        self.assertEqual(sum(1 for i in v if i["categorie"] == "AI"), 2)
        self.assertNotIn(kort, v)
        self.assertNotIn(kort, mix.uitgelicht(items, CFG, VANDAAG))

    def test_minder_dan_5(self):
        items = [item("AI %d" % n, "AI") for n in range(4)]
        self.assertEqual(len(mix.vaknieuws(items, [], CFG)), 2)


class TestVandaag(unittest.TestCase):
    def test_ongeldige_datum(self):
        r = subprocess.run([sys.executable, str(BASIS / "src" / "bouw.py"), "--vandaag", "2026-13-45"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("JJJJ-MM-DD", r.stderr)
        self.assertNotIn("Traceback", r.stderr)


if __name__ == "__main__":
    unittest.main()
