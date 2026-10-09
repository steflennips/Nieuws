# Testrapport iteratie 3, ronde 1 (Tester)

ITERATIE: 3 | RONDE: 1 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD (1 BELANGRIJK open: bevinding 1)

PER CRITERIUM:
- US-009-c1 (8-10 feeds, min. 3 NL/3 EN, naam/url/taal): OK. config/feeds.json: 9 feeds (4 NL, 5 EN), naam/url/taal, timeout 15 s. Test: test_US009_c1_...
- US-009-c2 (RSS 2.0 en Atom opgeslagen met alle velden): OK. Test: test_US009_c2_...; echte ronde: 72 items met alle velden.
- US-009-c3 (HTML weg, max 300 tekens, geen afbeeldingen/volle tekst): OK. Test: test_US009_c3_...; echte data: max 300 tekens, 0 tags, geen image-verwijzingen.
- US-009-c4 (zelfde link een keer): OK. Test: test_US009_c4_...; echte data: 0 dubbele links.
- US-009-c5 (items ouder dan 60 dagen weg): OK. Test: test_US009_c5_... (61 dagen weg, 59 dagen blijft). Zie bevinding 1 voor de melding.
- US-009-c6 (app toont echte items, nieuwste eerst, werkende link): OK. Test: test_US009_c6_... (end-to-end, zonder herstart); echte data in app: test_echte_data_*.
- US-009-c7 (per feed aantal items in uitvoer; echte ronde minimaal 6 feeds): OK. Echte ronde: 9 van 9 feeds OK met aantallen (zie bevinding 1 voor het "bewaard"-cijfer van Tweakers).
- US-010-c1 (trefwoorden NL en EN per categorie): OK. Test: test_US010_c1_...
- US-010-c2 (hele woorden, hoofdletterongevoelig; "AI" niet in "mail"): OK. Test: test_US010_c2_...
- US-010-c3 (meeste treffers; gelijkspel AI, Automatisering, Data): OK. Test: test_US010_c3_...
- US-010-c4 (zonder treffer niet opgeslagen): OK. Test: test_US010_c4_...
- US-010-c5 (vaste testset van 12 titels, verwachte categorie): OK. Test: test_US010_c5_...
- US-011-c1 (onbereikbare, trage (time-out) en kapotte feed laten de rest doorgaan): OK. Test: test_US011_c1_...
- US-011-c2 (eerder opgeslagen items van mislukte feed blijven staan): OK. Test: test_US011_c2_...
- US-011-c3 (per feed OK of FOUT met reden): OK. Test: test_US011_c3_...
- US-011-c4 (alle feeds mislukt: bestand ongewijzigd, foutcode; minstens 1 OK: code 0): OK. Tests: test_US011_c4_... (3 tests).
- US-011-c5 (item zonder titel overgeslagen; zonder datum krijgt ophaaldatum): OK. Test: test_US011_c5_...
- US-001-c1, c2, c3: OK (suite, voorbeeld- en echte data).
- US-001-c4 (leadsdeel): OK. Nieuwsdeel vervallen na US-009 (backlog), niet meer getoetst.
- US-001-c5 (labels Nederlands): OK. Scope gewijzigd naar interfaceteksten (zie wijzigingen).
- US-001-c6 (375 en 1280 px zonder horizontaal scrollen): OK. Headless Edge, met voorbeelddata én met echte data.
- US-002-c1 t/m c6 (nieuws, filter, alle, zoeken, geen resultaat, bronlink): OK. Suite met voorbeelddata; met echte data: test_echte_data_* (volgorde, filter, zoeken, leeg) en een in-proces controle tegen het echte bestand.
- US-004-c1 t/m c4 (startpagina, leadsdeel nog van kracht): OK. Suite (voorbeeld) en test_echte_data_overzicht_* (echte data).
- US-007-c1 t/m c3 (favicon, kleine letters, onbekend filter): OK. Suite (voorbeeld); c2/c3 ook met echte data (AI = ai = 61 items; onbekend = 72 items, Alle actief).
- US-008-c1 t/m c8 (stijl, kleuren, contrast, je/jij, breedte, responsief): OK. Stylesheet ongewijzigd; layout met voorbeelddata en echte data. Visueel: zie NIET GETEST.

SUITE: 71 tests, 71 geslaagd (standaard, met echte data aanwezig). Commando: `python -m unittest discover -s tests/acceptance -t tests/acceptance -v`. Aanvullend: met `NIEUWS_BRON=voorbeeld` 71 geslaagd; in een kopie van de projectmap zonder data/ 71 geslaagd, 2 overgeslagen (NIET GETEST: echt bestand ontbreekt). Bouwer-unittests (`python -m unittest discover -s tests -v`): 48 geslaagd.
Mutatiecontrole (in kopie): geen escaping van links, omgekeerde gelijkspelvolgorde en genegeerde robots.txt werden elk door minstens één test gevangen.

REGRESSIE: OK. Hele suite (71 tests), 375 en 1280 px in headless Edge, met voorbeelddata en met echte data. Geen regressie gevonden in US-002, US-007, US-008.

BEVINDINGEN:
1. BELANGRIJK. Tweakers-feed: uitvoer en opslag spreken elkaar tegen. Stappen: `python src/ophalen.py --uitvoer <tijdelijke map>/nieuws.json`. Verwacht: Tweakers-regel met het werkelijk bewaarde aantal, en feeds-status in het JSON-bestand die klopt met de items. Werkelijk: "OK Tweakers: 40 items in feed, 8 bewaard (8 nieuw)" en in dezelfde run "Totaal opgeslagen: 72 items (8 ouder dan 60 dagen verwijderd)". Er staat geen enkel Tweakers-item in het bestand, terwijl de feeds-status "bewaard": 8 zegt. Oorzaak (alleen-lezen onderzocht): de feed levert alleen items met een datum van april 2025; de parser doet het goed, de bron is verouderd. Gevolg: Tweakers draagt niets zichtbaar bij en de telling in de uitvoer is misleidend. Advies: tel "bewaard" na de leeftijdsfilter en meld verouderde items apart; PO beslist of deze feed blijft.
2. KLEIN. Categorieverdeling in echte data is scheef: AI 61 van 72, Data 8, Automatisering 3. Het filter Automatisering is bijna leeg. Oorzaak deels de gelijkspelregel (AI wint) en brede AI-trefwoorden ("claude", "gemini", "generative", "neural"). Verbeterpunt voor PO.
3. KLEIN. platte_tekst decodeert HTML-entiteiten dubbel. Reproduceer: `platte_tekst("Tom &amp;amp; Jerry")` geeft "Tom & Jerry" (verwacht "Tom &amp; Jerry"). Alleen bij dubbel ge-escapete feeds.
4. KLEIN. `python src/ophalen.py --config bestaat-niet.json` (of ongeldige JSON) geeft een Python-traceback in plaats van een nette melding. Er wordt niets beschadigd.
5. KLEIN. README: de zin "anders falen ze" over NIEUWS_BRON=voorbeeld klopt niet meer; de suite forceert dit nu zelf. Bouwer past README aan.
6. KLEIN. docs/decisions/2026-10-08-nieuwsfeeds.md wijkt af van config/feeds.json: toegevoegd AWS Machine Learning Blog, BigDATAwire (Datanami), Techzine; verdwenen VentureBeat AI, AI News, AG Connect, Frankwatching. US-009-c1 staat vervangers toe ("gemelde vervanger"), maar de melding van de Bouwer was niet in mijn opdracht; zie BENODIGD.

WIJZIGINGEN AAN BESTAANDE TESTS (iteratie 3, ronde 1; geen criterium verzwakt):
- test_acceptance.py: alle tests van US-001 t/m US-008 forceren NIEUWS_BRON=voorbeeld (setUpModule). Verwachte waarden ongewijzigd.
- US-001-c4: nieuwsdeel verwijderd (backlog: vervalt na US-009). Leadsdeel blijft.
- US-001-c5 en US-008-c7: controle op Engelse woorden en u/uw gaat nu over interfaceteksten (labels, knoppen, menu's), niet over nieuwstitels uit bronnen. Backlog zegt "labels en knoppen"; zonder deze scope faalde c5 op een Engels woord in een echte nieuwstitel.
- US-004-c4: href wordt ontgeescapet voor de vergelijking (testfout, zichtbaar alleen bij echte data).
- Nieuwe tests: test_US009_feeds.py, test_US010_categorie.py, test_US011_foutafhandeling.py, test_echte_data_app.py, hulp_feeds.py.

NIET GETEST:
- Terugknop, snel klikken, herladen met state, toetsenbord: NIET GETEST, omdat er geen browserbediening beschikbaar is zonder installatie. Handmatig door Stef.
- Browser opent automatisch (README): NIET GETEST, de suite start met GEEN_BROWSER=1. Handmatig door Stef.
- Time-out op het echte netwerk: alleen getest met een lokale trage server (time-out 1 s). Het project-maximum van 15 s staat in de config.
- Grote hoeveelheden: maximaal 72 echte items en 41 fixture-items; 200 snelle requests in 2,5 s; 200 000 tekens in de zoekterm geeft 414 (geen serverfout). Geen test met duizenden items.
- Visueel totaalbeeld (Stijl en uitstraling): alleen een zelf-beoordeling van schermen op 375 px (nieuws, overzicht) en 1280 px (overzicht); leads niet visueel beoordeeld. Stef beoordeelt het totaalbeeld.
- Echte feeds: vervangers niet geverifieerd (of de vervangen feeds echt dood waren). Robots.txt van de 9 hosts is gecontroleerd: alle toegestaan (InfoQ heeft geen robots.txt, dus toegestaan).
- US-013 (online site): niet in scope van deze iteratie.

NETWERKGEBRUIK (eerlijk): één echte ophaalronde naar een tijdelijke map (buiten de projectmap; data/nieuws.json is niet aangepast, met 72 items dezelfde telling als het bestaande bestand); plus alleen-lezen robots.txt-controle van de 9 hosts en één losse GET van de Tweakers-feed voor de diagnose van bevinding 1.

BENODIGD VAN BOUWER:
- Bevinding 1 oplossen (BELANGRIJK), daarna een SNEL-fixronde. Eventueel bevinding 3-5 meenemen.
- Melding van vervangers in de feedlijst bevestigen (welke feeds dood waren en door welke vervangen) zodat docs/decisions bijgewerkt kan worden (PO).
- README-zin over NIEUWS_BRON bijwerken (bevinding 5).
- Geen tools of rechten ontbreken.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/README.md (gewijzigd)
- tests/acceptance/test_acceptance.py (gewijzigd)
- tests/acceptance/hulp_feeds.py (nieuw)
- tests/acceptance/test_US009_feeds.py (nieuw)
- tests/acceptance/test_US010_categorie.py (nieuw)
- tests/acceptance/test_US011_foutafhandeling.py (nieuw)
- tests/acceptance/test_echte_data_app.py (nieuw)
- docs/test-reports/iteratie-3-ronde-1.md (nieuw, dit rapport)
- Servers: app gestart op poort 8765 en na afloop gestopt (PID gecontroleerd, niet meer bereikbaar). Tijdelijke bestanden (scratchpad, screenshots, kopie) buiten de projectmap.
