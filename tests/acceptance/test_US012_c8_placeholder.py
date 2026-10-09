"""Acceptatietest US-012-c8: de placeholder van het lege zoekveld op Nieuws is op 375 px volledig zichtbaar.

Werkwijze (headless Microsoft Edge, zonder installatie): een meetpagina in een tijdelijke map (naast de
gebouwde site, niet in de site zelf) laadt nieuws.html in een iframe van 375 px. Daarna meet de pagina of de
placeholdertekst past in de inhoudsbreedte van het zoekveld (breedte minus padding), met de lettertypes en
de tekstmeting van de browser zelf (canvas measureText). Het resultaat wordt als DOM teruggegeven
(--dump-dom), zodat er geen proxy of extra poort nodig is.

Zonder Edge wordt de test overgeslagen en is het criterium NIET GETEST.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import html as htmllib

import hulp_statisch as h

sys.dont_write_bytecode = True

EDGE = h.vind_edge()
SLA_OVER = "NIET GETEST: geen headless Edge gevonden op de standaardlocaties (US-012-c8 placeholder)"

MEETPAGINA = """<!doctype html><html lang="nl"><head><meta charset="utf-8"><title>meting</title></head>
<body><iframe id="f" style="border:0;display:block"></iframe>
<script>
const f = document.getElementById('f');
f.style.width = '375px'; f.style.height = '1200px';
f.src = 'nieuws.html';
f.onload = () => {
  setTimeout(() => {
    const d = f.contentDocument, win = d.defaultView;
    const z = d.getElementById('zoekveld');
    const cs = win.getComputedStyle(z);
    const ctx = document.createElement('canvas').getContext('2d');
    ctx.font = cs.font;
    const tekst = ctx.measureText(z.placeholder).width;
    const beschikbaar = z.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const r = {placeholder: z.placeholder, font: cs.font, inputBreedte: z.clientWidth,
               beschikbaar: beschikbaar, tekstBreedte: tekst, past: tekst <= beschikbaar,
               horizontaalOverloop: d.documentElement.scrollWidth > d.documentElement.clientWidth};
    fetch('/__r', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(r)});
  }, 800);
};
</script></body></html>"""

from functools import partial
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import time

RAPPORT = []


class _Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        RAPPORT.append(self.rfile.read(n).decode("utf-8", "replace"))
        self.send_response(204)
        self.end_headers()

    def log_message(self, *a):
        pass


def start_edge(url, profiel):
    return subprocess.Popen([EDGE, "--headless", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                             "--user-data-dir=" + profiel, "--virtual-time-budget=8000",
                             "--window-size=1280,1000", url],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@unittest.skipUnless(EDGE, SLA_OVER)
class TestUS012C8Placeholder(unittest.TestCase):
    def test_US012_c8_placeholder_volledig_zichtbaar_op_375_px(self):
        tmp = h.nieuwe_tijdelijke_map()
        profiel = tempfile.mkdtemp(prefix="t4-edge-")
        proc = None
        try:
            site = os.path.join(tmp, "site")
            data = h.schrijf_fixture_data(tmp)
            rc, out, err = h.bouw(site, data=data)
            self.assertEqual(rc, 0, err)
            with open(os.path.join(site, "meting-placeholder.html"), "w", encoding="utf-8") as f:
                f.write(MEETPAGINA)
            srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(_Handler, directory=site))
            t = threading.Thread(target=srv.serve_forever, daemon=True)
            t.start()
            try:
                url = "http://127.0.0.1:%d/meting-placeholder.html" % srv.server_address[1]
                proc = start_edge(url, profiel)
                eind = time.time() + 90
                while not RAPPORT and time.time() < eind:
                    time.sleep(0.25)
            finally:
                srv.shutdown()
                srv.server_close()
            self.assertTrue(RAPPORT, "geen meetresultaat van de browser binnen 90 seconden (NIET GETEST)")
            r = json.loads(RAPPORT[-1])
            self.assertEqual(r["placeholder"], "Zoek in nieuws")
            self.assertTrue(r["past"], "placeholder past niet in het zoekveld op 375 px: %s" % r)
            self.assertFalse(r["horizontaalOverloop"], "horizontaal scrollen op 375 px: %s" % r)
        finally:
            if proc is not None:
                proc.kill()
            h.stop_edge_profiel(profiel)
            shutil.rmtree(tmp, ignore_errors=True)
            shutil.rmtree(profiel, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
