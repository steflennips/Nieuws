# Testrapport iteratie 3, ronde 2 (Tester)

ITERATIE: 3 | RONDE: 2 | MODUS: VOLLEDIG
RESULTAAT: GESLAAGD (geen BLOKKEREND of BELANGRIJK open; 3 KLEIN open, zie bevindingen 2, 3, 6)

PER CRITERIUM:
- US-009-c1 (9 feeds, 4 NL en 5 EN, naam/url/taal, timeout 15 s): OK. config/feeds.json; test_US009_c1_...; Tweakers-URL is nu https://tweakers.net/feeds/mixed.xml.
- US-009-c2 (RSS 2.0 en Atom, alle velden): OK. test_US009_c2_...; echte ronde: 78 items met alle velden.
- US-009-c3 (platte tekst, max 300, geen afbeeldingen): OK. test_US009_c3_... en echte data: max 300 tekens, 0 tags in titel/samenvatting. Dubbele escape: zie bevinding 3 (KLEIN).
- US-009-c4 (geen dubbele links): OK. test_US009_c4_...; echte data: 0 dubbele links.
- US-009-c5 (ouder dan 60 dagen weg): OK. test_US009_c5_...; echte data: 0 items ouder dan 60 dagen.
- US-009-c6 (app toont echte items, nieuwste eerst, link): OK. test_US009_c6_...; app op 1280 px met 78 items, teller klopt (zie REGRESSIE).
- US-009-c7 (per feed aantal in uitvoer; echte ronde minimaal 6 feeds): OK. Echte ronde (eigen run naar tijdelijke map): 9 van 9 feeds OK met aantallen. Bevinding 1 opgelost: test_US009_c7_bewaard_na_leeftijdsfilter_... en test_US009_c7_feed_met_alleen_verouderde_items_... (nieuw, ronde 2).
- US-010-c1 t/m c5 (trefwoorden, hele woorden, meeste treffers/gelijkspel, geen treffer weg, vaste testset van 12): OK. Suite test_US010_c1..c5; echte ronde: 0 items zonder categorie in opslag. Kwaliteit van de categorie: zie bevinding 2 (KLEIN).
- US-011-c1 t/m c5 (uitgevallen/trage/kapotte feed, eerdere items blijven, OK/FOUT per feed, alle mislukt = bestand ongewijzigd en exitcode niet 0, item zonder datum/titel): OK. Suite test_US011_c1..c5 (6 tests); echte ronde: 9 van 9 OK, geen FOUT.
- US-001-c1 (start volgens README): OK voor het starten (server antwoordt op de README-poort en met PORT-variant). Automatisch openen van de browser: NIET GETEST (zie NIET GETEST).
- US-001-c2, c3, c5, c6: OK. Suite (voorbeeld en echte data); 375 en 1280 px via suite (headless Edge).
- US-001-c4 (leadsdeel): OK. Nieuwsdeel vervallen na US-009; leads 12, 4 nieuw, 2 per status in voorbeelddata (suite).
- US-002-c1 t/m c6: OK. Suite voorbeeld en echte data; zoek en filter met echte data (zie VERKENNEND).
- US-004-c1 t/m c4: OK. Overzicht toont 78 / 12 / 4, 5 nieuwste nieuws en 5 nieuwste leads; suite en screenshot.
- US-007-c1 t/m c3: OK. favicon 204, kleine letters en onbekende waarde getest met curl op echte data (AI = 66 items, onbekend = alles).
- US-008-c1 t/m c8: OK. Stylesheet ongewijzigd (suite c1-c5, c7, c8); layout op 1280 px en 375 px (suite en screenshots). Visueel totaalbeeld: zie NIET GETEST.
- US-003 en lead-delen US-001/US-004: OK (regressie tot US-012; suite).

SUITE: 75 tests, 75 geslaagd. Commando: `python -m unittest discover -s tests/acceptance -t tests/acceptance -v`. Zelfde suite met `NIEUWS_BRON=voorbeeld`: 75 geslaagd. Bouwer-unittests (`python -m unittest discover -s tests -v`): 51 geslaagd. Nieuw in ronde 2: `tests/acceptance/test_US009_ronde2.py` (4 tests).

REGRESSIE: OK. Hele suite (incl. 375 px en 1280 px headless Edge) met echte data en met voorbeelddata, geen fouten. Aanvullend visueel (headless Edge, screenshots in tijdelijke map): 1280 px Overzicht en Nieuws: strak, donkerblauwe kop, grijze achtergrond, witte kaarten, teal accent alleen op actief menu, actief filter, links en knop. 375 px: beoordeeld via een iframe van 375 px in een 1280 px venster (zelfde methode als de suite): navigatie volledig in beeld, tellers en kaarten onder elkaar, geen horizontaal scrollen. Een directe 375 px-venster-screenshot liet afgesneden tekst zien; dat komt waarschijnlijk door de minimale vensterbreedte van Edge (de iframe-meting toont een correcte layout), niet door de app.

BEVINDINGEN:
1. OPGELOST (was BELANGRIJK). Tweakers: nu `40 items in feed, 6 bewaard (6 nieuw), 0 verouderd`, en JSON-feeds-status (bewaard 6) klopt met het aantal Tweakers-items in het bestand (6). Totaal in de uitvoer (78) = som van bewaard (78) = aantal items in het JSON-bestand. Geen dubbele links, geen items ouder dan 60 dagen, alle velden aanwezig, samenvatting max 300 tekens. Verouderd-pad apart getest (feed met alleen oude items: OK, 0 bewaard, geen items opgeslagen).

2. KLEIN (open, verbeterpunt voor PO). Categorieverdeling echte data: AI 66, Data 9, Automatisering 3 (van 78). Voorbeeld: "Firmware-update - Asustor ADM 5.1.4.RM62" krijgt "Data" door de productnaam "Asustor Data Master". Stappen: start met `python src/ophalen.py --uitvoer <tmp>`, kijk naar categorie en filter Automatisering. Verwacht: categorie volgt het onderwerp; werkelijk: filter Automatisering bijna leeg.

3. KLEIN (deels open; ronde 1 bevinding 3). De functie is goed: `platte_tekst("Tom &amp;amp; Jerry")` geeft nu "Tom &amp; Jerry" (nieuwe test, OK). In de volledige pijplijn blijft het anders: een feed met titel `Tom &amp;amp; Jerry` (XML) wordt opgeslagen als "Tom & Jerry" (XML-parser decodeert eenmaal, platte_tekst nog eens). Ook een dubbel ge-escapete samenvatting met `&amp;lt;b&amp;gt;` wordt opgeslagen als letterlijk "<b>" in de tekst. De app escapet de uitvoer wel (geen script-risico gevonden), maar de samenvatting is dan geen platte tekst. Verwacht (ronde 1): "Tom &amp; Jerry" in de opgeslagen titel; werkelijk: "Tom & Jerry". Reproduceer: feed met `<title>Tom &amp;amp; Jerry</title>`, ophaalronde, kijk in JSON.

4. OPGELOST (ronde 1 bevinding 4, KLEIN). `--config bestaat-niet.json`, kapotte JSON en een config zonder `feeds` geven exitcode 2, een `FOUT:`-regel op stderr en geen traceback. Er ontstaat geen uitvoerbestand. Getest in de suite (test_US009_extra_ongeldige_config_...) en met de hand (ook een map als config: exitcode 2).

5. OPGELOST (ronde 1 bevinding 5, KLEIN). README-zin over NIEUWS_BRON klopt nu (de tests forceren zelf de voorbeelddata).

6. KLEIN (open, PO). `docs/decisions/2026-10-08-nieuwsfeeds.md` noemt nog de oude Tweakers-feedburner-URL en de Computable-URL /rss; de wijzigingen staan in `2026-10-08-feedwijzigingen-it3.md`. PO moet de lijst bijwerken en de vervangers bevestigen (ronde 1 bevinding 6). De config zelf is consistent met de wijzigingsnotitie.

7. OMGEVING (geen productfout). Op poort 8000 draait nog een `python src/app.py` (PID 34772, gestart 18:32, dus niet door mij gestart). Ik heb het niet gestopt omdat het niet van mij is; zie BENODIGD VAN BOUWER.

VERKENNEND (VOLLEDIG, met curl en de app op echte data, 78 items):
- Lege zoekterm en lege categorie, onbekende categorie, dubbele categorie-parameter, hoofdletters (AI): 200, filter klopt.
- Zoekterm van 3000 tekens: 200, geen fout. Zoekterm `<script>`: 200, waarde wordt geescapet.
- Snel achter elkaar klikken en grote aantallen requests: in deze ronde NIET GETEST (alleen ronde 1: 200 requests in 2,5 s, geen fouten).
- Serverlog (stderr) bleef leeg tijdens alle requests en de suite.
- Herladen en terugnavigeren: NIET GETEST (geen browserbediening zonder installatie).

BASISCHECKS:
- Foutmeldingen in serverlog: geen (stderr leeg). Browserconsole: NIET GETEST (headless Edge zonder devtools-uitlezing).
- README: klopt met het gedrag voor starten (PORT), ophalen (uitvoer per feed, exitcodes 0/1/2), feeds, tests en het aantal voorbeeldartikelen (18 nieuws, 12 leads). Automatisch openen van de browser is niet gecontroleerd.

NIET GETEST:
- Browser opent automatisch (README): NIET GETEST, omdat de suite met GEEN_BROWSER=1 start. Handmatig door Stef.
- Terugknop, snel klikken, herladen, toetsenbord: NIET GETEST, geen browserbediening zonder installatie. Handmatig door Stef.
- Time-out op het echte netwerk: alleen met lokale trage server (1 s), het 15 s-maximum staat in de config. Geen echte feed was uitgevallen tijdens deze ronde.
- Grote hoeveelheden: maximaal 78 echte items; geen test met duizenden items.
- Leads visueel: niet beoordeeld in deze ronde (alleen functioneel via de suite). Totaalbeeld "Stijl en uitstraling": alleen eigen beoordeling van schermen; Stef beoordeelt het totaal.
- US-013 (online site): buiten scope van deze iteratie.

NETWERKGEBRUIK (eerlijk): één echte ophaalronde naar een tijdelijke map (`--uitvoer` in de scratch-map; `data/nieuws.json` is niet aangepast). Verder alleen lokale servers op 127.0.0.1 en de suite.

BENODIGD VAN BOUWER:
- Geen blokkerende punten. Optioneel (KLEIN): bevinding 3 volledig oplossen (titel en samenvatting één keer decoderen) en bevinding 2 (categorie) bespreken met PO.
- PO: bevinding 2 (trefwoorden, o.a. "Data Master"), bevinding 6 (decisions bijwerken).
- Orkestrator: python-proces `src/app.py` op 127.0.0.1:8000 (PID 34772, gestart 18:32, niet door de Tester) draait nog. Graag controleren of Stef of de Bouwer dat wil laten draaien; ik heb het niet gestopt.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US009_ronde2.py (nieuw)
- tests/acceptance/README.md (overzicht uitgebreid met de ronde-2 tests)
- docs/test-reports/iteratie-3-ronde-2.md (dit rapport)
- Tijdelijk (buiten de projectmap, in de temp-map): ophaaluitvoer, screenshots, Edge-profielen. Alle servers die ik startte zijn gestopt; de `__pycache__` in src/ kwam van de builder-tests en staat in .gitignore.
