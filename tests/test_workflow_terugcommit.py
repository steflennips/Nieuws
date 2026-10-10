"""Eigen tests voor de terugcommit-stap in .github/workflows/nieuws.yml (conflictvrij, herhaalpogingen, geen force)."""
import re
import unittest
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
WF = (BASIS / ".github" / "workflows" / "nieuws.yml").read_text(encoding="utf-8")


class TestTerugcommit(unittest.TestCase):
    def test_yaml_geldig(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML niet beschikbaar")
        data = yaml.safe_load(WF)
        self.assertIn("bouwen", data["jobs"])
        self.assertEqual(data["jobs"]["publiceren"]["needs"], "bouwen")

    def test_geen_force_en_geen_rebase(self):
        self.assertNotRegex(WF, r"--force|--force-with-lease|push\s+-f\b|\+HEAD")
        self.assertNotIn("pull --rebase", WF)
        self.assertNotIn("git pull", WF)

    def test_herhaalpogingen(self):
        self.assertRegex(WF, r"for poging in 1 2 3")

    def test_job_versie_wint_zonder_conflict(self):
        i_cp = WF.index('cp data/nieuws.json "$RUNNER_TEMP/nieuws.json"')
        i_reset = WF.index('git reset --hard "origin/$BRANCH"')
        i_terug = WF.index('cp "$RUNNER_TEMP/nieuws.json" data/nieuws.json')
        i_commit = WF.index('git commit -m "Nieuws bijgewerkt"')
        i_push = WF.index('git push origin "HEAD:$BRANCH"')
        self.assertTrue(i_cp < i_reset < i_terug < i_commit < i_push)
        self.assertIn("git fetch origin", WF)

    def test_mislukte_push_blokkeert_publicatie_niet_maar_waarschuwt(self):
        self.assertIn("::warning", WF)
        self.assertIn("GITHUB_STEP_SUMMARY", WF)
        stap = WF[WF.index("Nieuwe data bewaren"):WF.index("upload-pages-artifact")]
        self.assertNotRegex(stap, r"^\s*exit 1", re.M)
        # bouwen en uploaden van site/ staan los van het slagen van de push
        self.assertLess(WF.index("python src/bouw.py"), WF.index("Nieuwe data bewaren"))

    def test_geen_secrets_en_minimale_rechten(self):
        self.assertNotIn("secrets.", WF)
        self.assertIn("contents: write", WF)
        self.assertNotIn("write-all", WF)


if __name__ == "__main__":
    unittest.main()
