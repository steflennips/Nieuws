"""US-022: geen verwarrende Vaknieuws-teller en volledig Nederlandse --config-melding."""
import io
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "src"))
import bouw  # noqa: E402
import ophalen  # noqa: E402

ENGELS = re.compile(r"No such file|Expecting|Errno|Permission denied|Invalid|decode|line \d+ column", re.I)


def draai(pad):
    f = io.StringIO()
    with redirect_stderr(f):
        code = ophalen.main(["--config", pad, "--uitvoer", os.devnull])
    return code, f.getvalue()


class TestVaknieuwsLink(unittest.TestCase):
    def test_geen_totaal_en_link_met_aantal(self):
        items = [{"titel": "T%d" % i, "samenvatting": "s", "datum": "2026-10-0%d" % (i % 9 + 1), "bron": "B",
                  "url": "https://example.org/%d" % i, "categorie": "AI"} for i in range(12)]
        html = bouw.view_overzicht(items, ("9 okt 2026 06:00", "2026-10-09T06:00:00+02:00"), [], items[:5])
        self.assertNotIn("in totaal", html)
        self.assertIn('<a class="alles" href="nieuws.html">Alle 12 berichten bekijken</a>', html)


class TestConfigMelding(unittest.TestCase):
    def test_ontbrekend_bestand(self):
        code, uit = draai("bestaat-niet.json")
        self.assertEqual(code, 2)
        self.assertIn("bestaat-niet.json", uit)
        self.assertIn("niet gevonden", uit)
        self.assertIsNone(ENGELS.search(uit), uit)
        self.assertNotIn("Traceback", uit)

    def test_geen_json(self):
        with tempfile.TemporaryDirectory() as t:
            pad = os.path.join(t, "kapot.json")
            with open(pad, "w") as f:
                f.write("dit is geen json")
            code, uit = draai(pad)
        self.assertEqual(code, 2)
        self.assertIn("kapot.json", uit)
        self.assertIsNone(ENGELS.search(uit), uit)

    def test_geen_utf8(self):
        with tempfile.TemporaryDirectory() as t:
            pad = os.path.join(t, "bin.json")
            with open(pad, "wb") as f:
                f.write(b"\xff\xfe\x00\x80")
            code, uit = draai(pad)
        self.assertEqual(code, 2)
        self.assertIsNone(ENGELS.search(uit), uit)

    def test_map_in_plaats_van_bestand(self):
        with tempfile.TemporaryDirectory() as t:
            code, uit = draai(t)
        self.assertEqual(code, 2)
        self.assertIsNone(ENGELS.search(uit), uit)

class TestConfigItems(unittest.TestCase):
    def _cfg(self, tekst):
        with tempfile.TemporaryDirectory() as t:
            pad = os.path.join(t, "c.json")
            with open(pad, "w", encoding="utf-8") as f:
                f.write(tekst)
            uit_pad = os.path.join(t, "uit.json")
            f2 = io.StringIO()
            with redirect_stderr(f2):
                code = ophalen.main(["--config", pad, "--uitvoer", uit_pad])
            return code, f2.getvalue(), os.path.exists(uit_pad)

    def test_ongeldige_items(self):
        basis = '"user_agent": "t", "trefwoorden": {"AI": ["ai"]}, '
        gevallen = [
            (basis + '"feeds": ["tekst"]', "feed 1 is geen object"),
            (basis + '"feeds": [{"naam": "A", "taal": "nl"}]', "mist url"),
            (basis + '"feeds": [{"naam": "A", "url": "http://x", "taal": "nl"}, 5]', "feed 2"),
            (basis + '"feeds": [{"url": "http://x", "taal": "nl"}]', "naam"),
            ('"user_agent": "t", "trefwoorden": {"AI": "ai"}, "feeds": []', "trefwoorden"),
        ]
        for tekst, melding in gevallen:
            code, uit, bestaat = self._cfg("{" + tekst + "}")
            self.assertEqual(code, 2, tekst)
            self.assertIn(melding, uit)
            self.assertNotIn("Traceback", uit)
            self.assertFalse(bestaat)


if __name__ == "__main__":
    unittest.main()
