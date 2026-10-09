"""Gedeelde browserhulp (headless Microsoft Edge) voor de acceptatietests van iteratie 6 (US-016 c7, US-018 c6).

Hergebruikt de proxy- en meetmechanik uit test_US012_browser.py (die werkt in deze omgeving):
- Site: een statische map wordt geserveerd op 127.0.0.1; een proxy voegt een meetscript toe dat de DOM
  (na JavaScript) en console-fouten terugmeldt.
- meting(pad, w): laadt de pagina in een iframe van w px en meet overloop en navigatie.
Zonder Edge: de aanroepende tests worden overgeslagen (NIET GETEST).

Dit bestand heet niet test*.py, dus unittest verzamelt het niet als testmodule.
"""
import shutil
import sys
import threading
import time
import urllib.parse
from http.server import ThreadingHTTPServer

import hulp_statisch as h
import test_US012_browser as tb

sys.dont_write_bytecode = True
EDGE = tb.EDGE
SLA_OVER = tb.SLA_OVER


class Site:
    def __init__(self, map):
        self.map = map
        self.srv = h.StatischeServer(map).__enter__()
        self.rapporten = []
        self.proxy = ThreadingHTTPServer(("127.0.0.1", 0), tb.maak_proxy(self.srv.base, self.rapporten))
        threading.Thread(target=self.proxy.serve_forever, daemon=True).start()
        self.base = "http://127.0.0.1:%d" % self.proxy.server_address[1]
        self.cache = {}

    def stop(self):
        self.proxy.shutdown()
        self.proxy.server_close()
        self.srv.__exit__(None, None, None)

    def _wacht(self, url, pad, kind, w=None, timeout=90):
        proc, profiel = tb.start_edge(url)
        try:
            eind = time.time() + timeout
            while time.time() < eind:
                for r in list(self.rapporten):
                    if r.get("url") == pad and r.get("kind") == kind and (w is None or r.get("viewport") == w):
                        return r
                time.sleep(0.3)
            raise AssertionError("Edge meldde geen %s-rapport voor %s binnen %d s" % (kind, pad, timeout))
        finally:
            h.stop_proces(proc)
            h.stop_edge_profiel(profiel)
            shutil.rmtree(profiel, ignore_errors=True)

    def laad(self, pad):
        """(DOM na JavaScript, lijst console-fouten) voor een pad inclusief ?parameters."""
        if pad not in self.cache:
            r = self._wacht(self.base + pad, pad, "dom")
            self.cache[pad] = (r["dom"], r.get("errs", []))
        return self.cache[pad]

    def meting(self, pad, w):
        key = ("layout", pad, w)
        if key not in self.cache:
            url = "%s/__h?w=%d&p=%s" % (self.base, w, urllib.parse.quote(pad, safe=""))
            self.cache[key] = self._wacht(url, pad, "layout", w)
        return self.cache[key]
