ITERATIE: 4 | RONDE: 3 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD (2 BLOKKEREND: US-012-c5 bronnenlijst onvolledig; US-015-c12 feed-aandeel niet gehaald)

PER CRITERIUM:
- US-010-c1 t/m c4: OK (test_US010_c1 t/m c4).
- US-010-c5: OK. Testtitel aangepast (zie WIJZIGINGEN 1), 12 titels groen.
- US-009-c1: OK. 10 feeds, NL 4, EN 6 (test_US009_c1). Echte ronde: 10 van 10 feeds OK.
- US-011-c1 t/m c5: OK (test_US011_*, suite groen). Echte ronde: geen FOUT.
- US-012-c1, c2, c3, c4, c6, c7, c8: OK (suite; browsertests 375/1280 px in Edge groen; placeholder-test groen).
- US-012-c5: FAALT (BLOKKEREND, zie BEVINDING 1). Voet "Laatst bijgewerkt" en link naar bronnen: OK. Bronnenlijst mist 2 van de bronnen die op de site getoond worden: "AWS Machine Learning Blog" (16 items) en "MIT Technology Review (AI)" (10 items) in data/nieuws.json (test_US012_c5_echte_data_elke_getoonde_bron_staat_op_bronnenlijst en test_US012_c5_fixture_bron_die_niet_in_config_staat_staat_toch_op_bronnenlijst: FAIL).
- US-013-c2: OK (test_US013_c2_*, 4 tests).
- US-013-c4: OK. Geheimenscan groen na aanscherping patroon; mutatietest groen (5 van 5 realistische sleutels gevangen, 0 van 2 slugs vals alarm).
- US-013-c5: OK (test_US013_c5_readme_*; de voorbeeldregel staat letterlijk in config/feeds.json).
- US-013-c1, c3: NIET GETEST, wacht op hosting-account van Stef.
- US-015-c1 t/m c4: OK (suite).
- US-015-c5: informatief. Ronde 3 (97 items, fris opgehaald): AI 72 (74%), Automatisering 12 (12%), Data 13 (13%).
- US-015-c6: OK (test_US015_c6_*, 3 tests; Tweakers, Colt, Uber, SageMaker-titel).
- US-015-c7: OK (test_US015_c7_*, 4 tests).
- US-015-c8: OK voor deze ronde, handmatig: Automatisering 12 (>= 8), filter niet leeg. Niet automatisch.
- US-015-c9: OK. 5 tests groen. Archestra-titel met echte samenvatting krijgt geen categorie (niet Automatisering). Mutatie: "workflow*" terug in de config laat de Archestra-titel wel Automatisering worden, dus de test vangt die regressie.
- US-015-c10: OK. Config bevat alle 16 genoemde Data-termen (min. 10 vereist). Vaste testset: 6 extra titels, elk via een andere term, allen Data (3 tests).
- US-015-c11: OK. "AWS Big Data Blog" staat in config (gratis, geen login, en), in docs/decisions/2026-10-08-nieuwsfeeds.md en op bronnen.html (4 tests). Robots.txt handmatig gecontroleerd: aws.amazon.com blokkeert voor "*" alleen /blogs/*/tag/ en een vast pad, niet /blogs/big-data/feed/. Voorwaarden van de site niet gecontroleerd.
- US-015-c12: FAALT (BLOKKEREND, zie BEVINDING 2). Data 13 (>= 8: OK). Automatisering 12 (>= 8: OK). Feed-grens niet gehaald: AWS Big Data Blog 10 van 13 Data (77%), n8n Blog 8 van 12 Automatisering (67%).
- US-014, US-005, US-006: niet in deze iteratie.

SUITE: 185 tests, 183 geslaagd, 2 faalt (beide US-012-c5 bronnenlijst). Commando: python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v. Bouwer-suite (zelfde ronde, src ongewijzigd): python -B -m unittest discover -s tests -p "test_*.py": 83 OK. Geen tests overgeslagen; Edge aanwezig, dus de browsertests draaiden.

REGRESSIE: NIET OK: US-012-c5 (bronnenlijst). Verder groen: alle overige 183 tests, inclusief US-001 t/m US-011 (statisch en lokale app), browsertests op 375 px (iframe) en 1280 px in Edge.

BEVINDINGEN:
1. BLOKKEREND, US-012-c5 bronnenlijst mist bronnen die op de site staan.
   - Stappen: python src/bouw.py --uit <tijdelijke map>; open bronnen.html en vergelijk met de bronnen in data/nieuws.json (test_US012_c5_echte_data_elke_getoonde_bron_staat_op_bronnenlijst).
   - Verwacht: elke bronnaam van een getoond item staat op bronnen.html ("alle bronnen", US-012 c5).
   - Werkelijk: bronnen.html toont 10 bronnen. De site toont 26 items van "AWS Machine Learning Blog" en "MIT Technology Review (AI)" die daar niet op staan. Oorzaak: src/bouw.py bouwt bronnen.html uit config/feeds.json (regels ~295-298), terwijl items 60 dagen blijven staan na het verwijderen van hun feed. Bij dagelijkse publicatie blijft dat tot 60 dagen zo. De tekst op bronnen.html ("alle koppen en samenvattingen ... komen uit de openbare feeds van onderstaande bronnen") klopt dan niet.
   - Dit is een nieuwe bevinding en geen onderdeel van het besluit 2026-10-08. Het is fixronde 3 van 3 van deze iteratie.
2. BLOKKEREND, US-015-c12 feed-aandeel niet gehaald (met eerlijke feeds en termen).
   - Stappen: python src/ophalen.py --uitvoer <tijdelijke map>/nieuws.json, daarna per categorie en per feed tellen.
   - Verwacht: Data >= 8, Automatisering >= 8, geen feed > 60% van Data of Automatisering.
   - Werkelijk: Data 13 = AWS Big Data Blog 10 (77%), InfoQ AI/ML/Data 2 (15%), BigDATAwire 1 (8%). Automatisering 12 = n8n Blog 8 (67%), Camunda Blog 4 (33%). Aantallen en termen zijn gemeten, niet geraden.
   - Bijkomend: het losse productnaam-trefwoord "n8n" geeft 6 van de 12 Automatisering-items (o.a. "You can now top up your n8n Assistant credits"). Dat is productnieuws van n8n zelf en valt onder de feed-grens.
   - Volgens het besluit kan de PO c12 accepteren als open punt met deze aantallen. Er is geen derde inhoudelijke fixronde voor c12.
3. KLEIN, README.md (hoofdmap): "vaste testset van 22 titels plus 5 echte titels" voor tests/test_categorie.py. Het bestand bevat 35 titels plus 6 echte. Documentatie loopt achter op de code (Bouwer).
4. KLEIN, geheimenscan: het sk-patroon mist een sleutel die direct na een letter, cijfer, "_", "/" of "-" staat (bijv. "KEY-sk-..."). Bewust gekozen om het vals alarm op de slug op te lossen; in tests/acceptance/README.md vermeld. Geen echte sleutel gevonden in de projectmap.
5. KLEIN, brede trefwoorden: "integratie*"/"integration*" (Automatisering), "analyse", "gegevens", "statistiek" (Data) zijn breed. In deze ronde geen aantoonbaar fout item door deze termen (1 item via "integration*": "Three Ways Camunda Speaks MCP"). Ter overweging voor de PO.
6. INFO, console-fouten: NIET GETEST. De methode (Edge met logging naar stderr) legde ook een bewust console.error niet vast; de controle is dus niet betrouwbaar. Geen bewijs van fouten, maar ook niet als geslaagd geteld.
7. INFO, verkennend (lokale app en statische site, via URL en curl): lege zoekterm en lege categorie tonen alles; onbekende categorie toont alles; zoekterm van 5000 tekens geeft 200; zoekterm zonder resultaat toont "Geen nieuws gevonden"; <script> in zoekterm wordt geescapet in het invoerveld; de statische site zet de zoekterm via textContent en niet via innerHTML; /favicon.ico geeft 204; onbekende route 404. NIET GETEST: snel klikken, terugknop, herladen in de browser, toetsenbord, echt toestel, grotere datasets.
8. INFO, uiterlijk (headless Edge, screenshots in de tijdelijke map): 375 px (Nieuws, filter Automatisering, in een iframe van 375 px): navigatie in beeld, zoekveld en chips volledig, kaarten onder elkaar, teal alleen op actieve chip en links. 1280 px (Overzicht): donkerblauwe kop, grijze achtergrond, witte tegels, teal voor het actieve menu-item. Een schermopname van 375 px zonder iframe was vertekend (Edge houdt een minimumvensterbreedte aan); dat is dus niet als bevinding gerekend. Het totaalbeeld beoordeelt Stef.

BENODIGD VAN BOUWER:
- Bevinding 1: bronnenlijst uit config en uit de getoonde items samen bouwen, of items van verwijderde feeds niet tonen. Daarna fixronde 3 (laatste toegestane).
- Bevinding 3: README-getallen voor tests/test_categorie.py bijwerken.
- Bevinding 2: PO-beslissing (accepteren als open punt, of een andere feedkeuze). Geen Bouwer-actie zonder die beslissing.
- Niet automatisch te testen: US-013-c1 en c3 wachten op het hosting-account van Stef.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US013_workflow.py (gewijzigd: sk-patroon met grens; nieuwe mutatietest)
- tests/acceptance/test_US010_categorie.py (gewijzigd: testtitel "Workflow automation-tools ...")
- tests/acceptance/test_US015_categorie.py (gewijzigd: 6 extra Data-testtitels; nieuwe klassen voor c9 en c10)
- tests/acceptance/test_US015_c11_datafeed.py (nieuw)
- tests/acceptance/test_US012_c5_bronnenlijst.py (nieuw)
- tests/acceptance/README.md (gewijzigd)
- docs/test-reports/iteratie-4-ronde-3.md (nieuw, dit rapport)
Tijdelijke bestanden (ophaalronde, gebouwde site, screenshots, wrapper-pagina's) staan alleen in de scratchpad buiten de projectmap. Servers gestopt (poorten 8765 en 8766 vrij). Een ander Python-proces (PID 4229076, gestart 18:32, niet door mij) is niet aangeraakt.

WIJZIGINGEN AAN TESTS (niets verzwakt; verwachte categorieen gelijk):
1. test_US010_c5: "Workflow-tools maken processen voorspelbaar" is "Workflow automation-tools maken processen voorspelbaar" (verwacht Automatisering; los "workflow" vervalt volgens US-015 c9).
2. test_US013_c4: patroon voor "sk-" krijgt een grens `(?<![A-Za-z0-9_/-])`. De slug "...amazon-msk-with-next-generation-protocol" is geen vals alarm meer. Mutatietest bewijst dat realistische sleutels nog gevangen worden.
3. Nieuwe tests: US-015 c9 (5), c10 (3), c11 (4), US-012 c5 bronnenlijst (2; beide FAIL, zie bevinding 1). US-015 c12 blijft handmatig (live feeds).
