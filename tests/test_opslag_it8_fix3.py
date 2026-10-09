"""Fixronde 3 iteratie 8: een bestaand maar onleesbaar opslagbestand wordt nooit stil leeggeschreven."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

sys.dont_write_bytecode = True
BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "src"))
import bouw  # noqa: E402
import ophalen  # noqa: E402

DATA = json.dumps({"items": [{"url": "https://example.org/%d" % i, "titel": "t%d" % i, "bron": "B"}
                             for i in range(20)]}, ensure_ascii=False, indent=1).encode("utf-8")


class TestLaadOpslag(unittest.TestCase):
    def setUp(self):
        self.map = tempfile.TemporaryDirectory()
        self.pad = os.path.join(self.map.name, "nieuws.json")

    def tearDown(self):
        self.map.cleanup()

    def _schrijf(self, inhoud):
        with open(self.pad, "wb") as f:
            f.write(inhoud)

    def test_ontbrekend_is_leeg(self):
        self.assertEqual(ophalen.laad_opslag(self.pad), {"items": []})

    def test_bom_met_inhoud_wordt_geweigerd(self):
        self._schrijf(b"\xef\xbb\xbf" + DATA)
        with self.assertRaises(ophalen.OpslagFout):
            ophalen.laad_opslag(self.pad)

    def test_onleesbaar_geeft_fout_met_pad(self):
        for naam, inhoud in {"afgekapt": DATA[:len(DATA) // 2], "geen utf-8": b"\xff\xfe\x00{",
                             "lijst": b"[1, 2]", "zonder items": b"{}", "items geen lijst": b'{"items": 3}'}.items():
            with self.subTest(naam):
                self._schrijf(inhoud)
                with self.assertRaises(ophalen.OpslagFout) as c:
                    ophalen.laad_opslag(self.pad)
                self.assertIn(self.pad, str(c.exception))
                self.assertIn("niet overschreven", str(c.exception))

    def test_nul_bytes_telt_als_leeg(self):
        for inhoud in (b"", b"\n", bytes([0xEF, 0xBB, 0xBF])):
            self._schrijf(inhoud)
            self.assertEqual(ophalen.laad_opslag(self.pad), {"items": []})

    def test_map_geeft_fout(self):
        with self.assertRaises(ophalen.OpslagFout):
            ophalen.laad_opslag(self.map.name)

    def test_main_exitcode_2_bestand_ongewijzigd_geen_tmp(self):
        cfg = os.path.join(self.map.name, "feeds.json")
        with open(cfg, "w", encoding="utf-8") as f:
            json.dump({"user_agent": "test", "trefwoorden": {c: ["x"] for c in ophalen.VERPLICHTE_CATEGORIEEN},
                       "feeds": [{"naam": "B", "url": "http://127.0.0.1:9/feed.xml", "taal": "nl"}]}, f)
        for inhoud in (DATA[:100], b"\xef\xbb\xbf{"):
            self._schrijf(inhoud)
            err = io.StringIO()
            with redirect_stderr(err):
                code = ophalen.main(["--config", cfg, "--uitvoer", self.pad])
            self.assertEqual(code, 2)
            self.assertIn("FOUT", err.getvalue())
            self.assertIn(self.pad, err.getvalue())
            with open(self.pad, "rb") as f:
                self.assertEqual(f.read(), inhoud)
            self.assertFalse(os.path.exists(self.pad + ".tmp"))

    def test_uitvoer_is_map_nederlandse_melding_geen_tmp(self):
        cfg = os.path.join(self.map.name, "feeds.json")
        with open(cfg, "w", encoding="utf-8") as f:
            json.dump({"user_agent": "test", "trefwoorden": {c: ["x"] for c in ophalen.VERPLICHTE_CATEGORIEEN},
                       "feeds": [{"naam": "B", "url": "http://127.0.0.1:9/feed.xml", "taal": "nl"}]}, f)
        doel = os.path.join(self.map.name, "uitmap")
        os.mkdir(doel)
        err = io.StringIO()
        with redirect_stderr(err):
            code = ophalen.main(["--config", cfg, "--uitvoer", doel])
        self.assertEqual(code, 2)
        self.assertIn("map", err.getvalue())
        self.assertFalse(os.path.exists(doel + ".tmp"))


class TestBouwDataMelding(unittest.TestCase):
    def test_ontbrekend_volledig_nederlands(self):
        with self.assertRaises(ValueError) as c:
            bouw.bouw(os.path.join(tempfile.gettempdir(), "bestaat-echt-niet.json"), "x", "y")
        t = str(c.exception)
        self.assertIn("ontbreekt", t)
        for engels in ("No such file", "Errno", "Expecting"):
            self.assertNotIn(engels, t)


if __name__ == "__main__":
    unittest.main()
