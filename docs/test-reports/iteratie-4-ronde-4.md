ITERATIE: 4 | RONDE: 4 | MODUS: VOLLEDIG
RESULTAAT: GESLAAGD (met OPEN PUNT US-015-c12, geaccepteerd door PO; niet blokkerend)

PER CRITERIUM:
- US-012-c1: OK. Bouwcommando naar tijdelijke map; statische site werkt via http.server (index, nieuws, bronnen 200). Suite: test_US012_statische_site, browsertests.
- US-012-c2: OK. Navigatie precies Overzicht en Nieuws; geen Leads-link (test_US001_c2_statisch, browser).
- US-012-c3: OK. Geen leads/leadstatussen/voorbeeldbedrijven in gegenereerde bestanden (suite, 6 tests). Handmatig: enige treffer op "leads" is artikeltekst ("Soc-teamleads"), geen leaddata.
- US-012-c4: OK. Bron, datum, samenvatting (max 300 tekens), link naar origineel; geen afbeeldingen (suite, 7 tests).
- US-012-c5: OK (blokkerende bevinding ronde 3 opgelost). Echte data: 125 items uit 12 bronnen; bronnen.html bevat alle 12, incl. "AWS Machine Learning Blog" (16 items) en "MIT Technology Review (AI)" (10 items) die niet in config staan. Fixture met bron buiten config: staat ook op de lijst. Voet "Laatst bijgewerkt: 8 okt 2026 21:08" (19:08 UTC, correct CEST), link "alle bronnen" werkt.
- US-012-c6: OK. Tellertegels Data/Automatisering/AI en 5 nieuwste items (browsertest, suite).
- US-012-c7: OK. Categoriefilter, zoeken, combinatie, speciale tekens, lege zoekterm (browsertests, 9 tests).
- US-012-c8: OK. Placeholder op 375 px volledig zichtbaar (browsertest in Edge).
- US-015-c1 t/m c4: OK (suite, 16 tests; "Data Master" uitsluiting, Asustor-titel niet Data, 15+ trefwoorden per categorie).
- US-015-c5: informatief. Ronde 4 (fris opgehaald, zie hieronder): Data 12, Automatisering 12, AI 63 (87 items).
- US-015-c6, c7: OK (suite: 3 + 4 tests).
- US-015-c8: OK voor deze ronde, handmatig. Automatisering 12 (>= 8), filter Automatisering op Nieuws niet leeg (12 items).
- US-015-c9 t/m c11: OK (suite: 5 + 3 + 4 tests). c11: AWS Big Data Blog in config, feedbesluit en bronnenlijst.
- US-015-c12: OPEN PUNT (geaccepteerd door PO). Eén echte ophaalronde naar tijdelijke map: Data 12 = AWS Big Data Blog 10 (83%), InfoQ AI/ML/Data Eng 2 (17%). Automatisering 12 = n8n Blog 8 (67%), Camunda Blog 4 (33%). Doel Data >= 8 en Automatisering >= 8 gehaald; grens 60% per feed NIET gehaald (2 feeds boven 60%). BigDATAwire gaf deze ronde FOUT (time-out), wat correct gemeld werd (US-011-c3).
- US-013-c2: OK (suite, 5 tests): cron "0 4 * * *" = 04:00 UTC = 06:00 CEST; workflow_dispatch aanwezig.
- US-013-c4: OK (suite, 3 tests, incl. mutatietest). Handmatige scan op sleutelpatronen (ghp_, github_pat_, AKIA, sk-, password=): alleen het patroon in tests/test_bouw.py, geen echte sleutel.
- US-013-c5: OK (suite, 5 tests): README bevat de feedregel, de voorbeeldregel staat letterlijk in config/feeds.json, handmatige start beschreven.
- US-013-c1, c3: NIET GETEST. Buiten scope iteratie 4 (wacht op hosting-account van Stef, iteratie 5).

SUITE: 185 tests, 185 geslaagd, 0 overgeslagen (Edge aanwezig, browsertests draaiden). Commando: python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v. Bouwer-suite (README-commando): python -B -m unittest discover -s tests -v: 84 OK.

REGRESSIE: OK. Gedekt: US-001 c3/c5/c6 op statische site; US-002, US-007, US-008 c1-c8 (statisch en lokale app); US-009, US-010, US-011 (suite en echte ophaalronde); lokale app met echte data en met voorbeelddata; browsertests op 375 px en 1280 px (statisch en app). Geen regressie gevonden.

BEVINDINGEN:
1. (ronde 3, nr. 1) BLOKKEREND, US-012-c5 bronnenlijst. OPGELOST: zie PER CRITERIUM. Geen nieuwe bevinding.
2. (ronde 3, nr. 2) US-015-c12 feed-aandeel. OPEN PUNT (geaccepteerd door PO), niet blokkerend. Actuele aantallen zie PER CRITERIUM. Ter info: de ronde-aantallen verschillen per ophaling (ronde 3: Data 13 met AWS 77%; ronde 4: Data 12 met AWS 83%); de conclusie blijft gelijk.
3. (ronde 3, nr. 3) KLEIN, README-aantallen tests/test_categorie.py. OPGELOST: README noemt nu 35 titels plus 6 echte titels (eerder 22 plus 5); dat klopt met het bestand tests/test_categorie.py.
4. (ronde 3, nr. 4-5) KLEIN, geheimenscan-patroon en brede trefwoorden: ongewijzigd, niet opnieuw beoordeeld in deze ronde.
5. (ronde 3, nr. 6) Console-fouten: NIET GETEST. Geen betrouwbare methode gevonden. Statische controle: app.js bevat geen console-aanroepen; alle element-ID's die app.js gebruikt bestaan in nieuws.html; HTML-tags zijn in index, nieuws, bronnen en 404 in balans. Serverlog van de statische site: alleen 200 en verwachte 404's, geen fouten.
6. KLEIN (nieuw): bronnen.html toont "AWS Machine Learning Blog" en "MIT Technology Review (AI)" als platte tekst zonder link (bron buiten config). Reproduceer: python src/bouw.py --uit <map>, open bronnen.html. US-012-c5 vraagt geen link per bron, dus geen blokkade; wel een verbeterpunt voor de PO (URL van de bron afleiden uit de items).
7. INFO (verkennend, statische site via HTTP): /nieuws.html?categorie=onbekend, ?categorie=AI&q=zzzzzz, ?q=%3Cscript%3E en een zoekterm van 5000 tekens geven 200 zonder serverfout. Onbekende routes /leads, /leads.html, /nieuws en /nietbestaand geven 404 (lokale server; of GitHub Pages /nieuws zonder .html zich zo gedraagt, is NIET GETEST). /favicon.ico (200) en /favicon.svg (200) aanwezig.
8. INFO, NIET GETEST in een echte browser: terugknop, herladen, snel klikken, toetsenbord (Tab), echt toestel, grote datasets (alleen 125 items gebouwd), browser auto-open van de lokale app. De filters werken via URL-parameters; die zijn met de browsertests gecontroleerd, niet de interactie.
9. INFO, uiterlijk: screenshots (headless Edge) van bronnen.html op 1280 px en 375 px (375 px via iframe in tijdelijke map). Donkerblauwe kop, grijze achtergrond, witte kaarten, teal voor links. Geen horizontaal scrollen zichtbaar; kaarten onder elkaar. Totaalbeeld beoordeelt Stef.

BENODIGD VAN BOUWER: geen voor iteratie 4. Ter info voor de PO: c12 (open punt) en het verbeterpunt uit bevinding 6. US-013-c1/c3 wachten op het hosting-account van Stef (iteratie 5).

BESTANDEN GEWIJZIGD DOOR MIJ: docs/test-reports/iteratie-4-ronde-4.md (dit rapport). Geen wijzigingen in tests/acceptance/. Tijdelijke bestanden (ophaalronde, gebouwde site, screenshots, wrapper) alleen in de systeem-tijdelijke map (%TEMP%\t4r4). Servers gestopt (poorten 8765 en 8766 vrij); de Edge-processen van mijn profiel zijn gestopt. Andere msedge-processen (niet van mij) zijn niet aangeraakt.
