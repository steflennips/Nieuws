"""Mix en selectie voor de weergave (alleen Python-standaardbibliotheek).

- beperk_ai: AI hooguit 40% van alle getoonde items (US-016 c4).
- uitgelicht / vaknieuws: blok "Uitgelicht" op het Overzicht (US-018).
- Gebruikt door de statische site (bouw.py).
"""
import json
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ophalen import _patroon  # noqa: E402

CATEGORIEEN = ["BI", "Data", "Automatisering", "AI"]
MAX_AI_AANDEEL = 0.4
UITGELICHT_MAX = 5
UITGELICHT_MAX_AI = 2
UITGELICHT_DAGEN = 3
VAKNIEUWS_MAX = 5
VAKNIEUWS_MAX_AI = 2


def laad_config(pad):
    """Config als dict; bij een fout een lege dict (de site blijft werken, zonder headnieuws-score)."""
    try:
        with open(pad, encoding="utf-8") as f:
            c = json.load(f)
        return c if isinstance(c, dict) else {}
    except (OSError, ValueError):
        return {}


def _sorteer_nieuwste(items):
    """Nieuwste eerst; bij gelijke datum blijft de oorspronkelijke volgorde (stabiel)."""
    return sorted(items, key=lambda i: i["datum"], reverse=True)


def beperk_ai(items, max_aandeel=MAX_AI_AANDEEL):
    """Alle niet-AI items blijven; van AI de nieuwste zodat AI hooguit max_aandeel van het totaal is
    (naar beneden afgerond). 20 niet-AI -> 13 AI (13 van 33 = 39%; 14 van 34 = 41%)."""
    niet_ai = [i for i in items if i["categorie"] != "AI"]
    ai = _sorteer_nieuwste([i for i in items if i["categorie"] == "AI"])
    # ai_toegestaan = grootste a met a <= max_aandeel * (n + a)  ->  a <= n * p / (1 - p)
    p = max_aandeel
    a = int((len(niet_ai) * p / (1 - p)) + 1e-9) if p < 1 else len(ai)
    keep = {id(i) for i in ai[:a]}
    return [i for i in items if i["categorie"] != "AI" or id(i) in keep]


def headnieuws_bronnen(config):
    return {f["naam"] for f in config.get("feeds", []) if isinstance(f, dict) and f.get("headnieuws")}


def nl_bronnen(config):
    return {f["naam"] for f in config.get("feeds", []) if isinstance(f, dict) and f.get("taal") == "nl"}


def score(item, bronnen_head, patronen, bronnen_nl=()):
    """2 punten voor een headnieuws-feed, 1 punt voor een Nederlandse feed, plus 1 punt per verschillende
    relevantieterm in titel of samenvatting (US-018 c3, US-021 c2)."""
    tekst = ("%s %s" % (item.get("titel", ""), item.get("samenvatting", ""))).casefold()
    punten = (2 if item.get("bron") in bronnen_head else 0) + (1 if item.get("bron") in bronnen_nl else 0)
    return punten + sum(1 for p in patronen if p.search(tekst))


def _evenement_patronen(config):
    return [_patroon(t) for t in (config or {}).get("evenement_termen", [])]


def blok_geschikt(item, evenement_patronen):
    """Mag het item in Uitgelicht of Vaknieuws? Niet bij een titel die met "Kort:" begint (digest) of een
    evenementterm in titel of samenvatting (US-018 c7/c8). Op Nieuws blijft het item staan."""
    titel = item.get("titel", "")
    if titel.strip().casefold().startswith("kort:"):
        return False
    tekst = ("%s %s" % (titel, item.get("samenvatting", ""))).casefold()
    return not any(p.search(tekst) for p in evenement_patronen)


def uitgelicht(items, config, vandaag=None):
    """Max. 5 items uit de laatste 3 dagen, hooguit 2 AI, alleen uit headnieuws-feeds (geen aanvulling met
    andere bronnen). Hoogste score eerst, bij gelijke score nieuwste eerst."""
    vandaag = vandaag or date.today()
    grens = (vandaag - timedelta(days=UITGELICHT_DAGEN)).isoformat()
    head = headnieuws_bronnen(config)
    nl = nl_bronnen(config)
    patronen = [_patroon(t) for t in config.get("deux_relevantie", [])]
    ev = _evenement_patronen(config)
    kand = [i for i in items if i["datum"] >= grens and i.get("bron") in head and blok_geschikt(i, ev)]
    gesorteerd = sorted(_sorteer_nieuwste(kand), key=lambda i: -score(i, head, patronen, nl))  # stabiel: nieuwste eerst
    gekozen, ai = [], 0
    for i in gesorteerd:
        if len(gekozen) >= UITGELICHT_MAX:
            break
        if i["categorie"] == "AI":
            if ai >= UITGELICHT_MAX_AI:
                continue
            ai += 1
        gekozen.append(i)
    return gekozen


def vaknieuws(items, uitgelicht_items, config=None):
    """De 5 nieuwste items die niet in Uitgelicht staan, hooguit 2 AI (aangevuld met niet-AI, anders minder dan 5);
    zonder "Kort:"-titels en evenementaankondigingen."""
    ids = {id(i) for i in uitgelicht_items}
    ev = _evenement_patronen(config)
    gekozen, ai = [], 0
    for i in _sorteer_nieuwste(items):
        if len(gekozen) >= VAKNIEUWS_MAX:
            break
        if id(i) in ids or not blok_geschikt(i, ev):
            continue
        if i["categorie"] == "AI":
            if ai >= VAKNIEUWS_MAX_AI:
                continue
            ai += 1
        gekozen.append(i)
    return gekozen
