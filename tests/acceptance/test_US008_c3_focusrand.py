"""US-008-c3 (focusrand): stylesheet-controle van de focusrand (fixronde iteratie 2).

Focusrand donkerblauw (#1F2A44) buiten de koptekst, wit in de donkerblauwe koptekst, nooit accentkleur.
Controleert de stylesheet op contrast (WCAG 1.4.11: minimaal 3:1 voor UI-onderdelen). De zichtbaarheid
in een echte browser (focus op menu, zoekveld, knop en chips) is handmatig gecontroleerd met headless Edge.
"""
import os
import re
import sys
import unittest

sys.dont_write_bytecode = True
import hulp_statisch as h  # noqa: E402

# Iteratie 7: de lokale app (app.CSS) is verwijderd; de stylesheet komt nu uit de gebouwde statische site.
_CSS_TEKST = None


def _css_van_statische_site():
    global _CSS_TEKST
    if _CSS_TEKST is None:
        tmp = h.nieuwe_tijdelijke_map(prefix="it7-focusrand-")
        try:
            data = h.schrijf_fixture_data(tmp)
            rc, out, err = h.bouw(os.path.join(tmp, "site"), data=data, vandaag=h.FIXTURE_VANDAAG)
            if rc != 0:
                raise AssertionError("bouwen voor focusrand-controle faalde: " + err)
            _CSS_TEKST = h.lees(os.path.join(tmp, "site", "style.css"))
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)
    return _CSS_TEKST


def hex_rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(c):
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def variabelen(css):
    root = re.search(r":root\{([^}]*)\}", css).group(1)
    return {k: v.strip() for k, v in re.findall(r"--([\w-]+):([^;]+)", root)}


class TestFocusrand(unittest.TestCase):
    def setUp(self):
        self.css = _css_van_statische_site()
        self.v = variabelen(self.css)

    def regel(self, selector):
        m = re.search(re.escape(selector) + r"\{([^}]*)\}", self.css)
        return m.group(1).replace(" ", "") if m else None

    def kleur(self, naam):
        return hex_rgb(self.v[naam])

    def test_US008_c3_focusrand_in_koptekst_wit_op_donkerblauw_contrast(self):
        body = self.regel("header a:focus-visible")
        self.assertIsNotNone(body, "geen focusregel voor koptekstlinks")
        self.assertIn("outline-color:var(--wit)", body)
        self.assertGreaterEqual(contrast(self.kleur("wit"), self.kleur("donker")), 3.0)

    def test_US008_c3_focusrand_overig_donkerblauw_op_lichte_achtergrond_contrast(self):
        body = self.regel("a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible")
        self.assertIsNotNone(body, "geen algemene focusregel")
        self.assertIn("outline:2pxsolidvar(--donker)", body)
        self.assertGreaterEqual(contrast(self.kleur("donker"), self.kleur("achtergrond")), 3.0)

    def test_US008_c3_focusrand_gebruikt_geen_accentkleur(self):
        for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", self.css):
            if "focus" in sel:
                self.assertNotIn("var(--accent)", body, "accentkleur in focusregel: %s" % sel.strip())


if __name__ == "__main__":
    unittest.main()
