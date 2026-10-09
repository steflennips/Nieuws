ITERATIE: 8 | RONDE: 1 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD

PER CRITERIUM:
- US-020-c1: NIET GETEST (deel verzonnen bedrijfsnamen); rest OK. Bestanden app.py/data.py weg; geen leadwoord of leadstatus in src/, config/, README.md (test_US020_c1_* OK). Geen "lead" buiten de vaste uitzonderingslijst (test_US020_c1_geen_leadwoorden_in_tests OK). Bedrijfsnamen: zie BEVINDING 2.
- US-020-c2: OK. Geen http.server of verwijderde module in src/; src/ = bouw.py, mix.py, ophalen.py, veilig_check.py (test_US020_c2_* OK).
- US-020-c3: OK. Verse kopie zonder site/: ophalen (lokale testfeeds) exit 0, bouwen exit 0, veilig_check exit 0, unittests 117 OK, geen ImportError (test_US020_c3_* OK).
- US-020-c4: OK. README zonder startinstructie lokale app; wel ophalen, bouwen, statische server, feeds, publiceren (test_US020_c4_* OK).
- US-022-c1: OK. Fixture-site en site uit data/nieuws.json (87 items): kop Vaknieuws is alleen "Vaknieuws", geen "in totaal" op de startpagina, link "Alle 87 berichten bekijken" = 87 kaarten op Nieuws. Screenshots 1280 px en 375 px (iframe) bekeken: kop zonder teller, geen overloop.
- US-022-c2: OK voor de gevraagde gevallen: ontbrekend bestand, geen JSON (ook: niet-UTF-8 en map): Nederlandse melding met pad, exitcode 2, geen traceback, geen uitvoerbestand. Wel BELANGRIJK, zie BEVINDING 1 (extra geval).
- US-001-c5 (regressie na US-022 c1): OK, "Alle <n> berichten bekijken" in plaats van "Alles bekijken".
- US-013-c1 en c3: NIET GETEST (live site op github.io en run op GitHub; geen toegang), ongewijzigd.
- Overige criteria it. 1-7 (US-001 t/m US-021): OK in de suite, zie REGRESSIE.

SUITE: 268 tests, 262 geslaagd, 1 gefaald (BEVINDING 1), 5 geskipt (vervallen lokale-app-tests, geskipt met reden). Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v` (twee volledige runs; de eerste had 1 falende test door een README-volgorde, die ik daarna oploste; de tweede run is hierboven bedoeld). Bouwer-suite: `python -B -m unittest discover -s tests -v`: 117 OK.

REGRESSIE: NIET GESLAAGD door 1 nieuwe BELANGRIJK-test (BEVINDING 1). Geen regressie van eerder geaccepteerde criteria: statische site 375 px (iframe) en 1280 px in headless Edge OK; `python src/veilig_check.py` exitcode 0 (91 bestanden, geen geheimen); console- en 404-controles OK; README-controles OK. Bytecode: er ontstond geen nieuwe __pycache__ in src/ tijdens de runs.

BEVINDINGEN:
1. BELANGRIJK (blokkeert GESLAAGD): `python src/ophalen.py --config <config>` met geldige JSON maar een feed-item als tekst, bijvoorbeeld `{"user_agent": "test", "trefwoorden": {"AI": ["ai"]}, "feeds": ["tekst"]}`, geeft een traceback (TypeError: string indices must be integers, not 'str', in draai bij feed["naam"]) en exitcode 1. Verwacht: Nederlandse melding die het probleem noemt, exitcode 2, geen traceback (de geest van US-022 c2). Werkelijk: traceback, exitcode 1. Test: test_US022_c2_extra_feed_item_dat_geen_object_is_geeft_geen_traceback (FAALT). Reproduceer: maak een configbestand zoals hierboven en draai het commando.
2. KLEIN: feed-item zonder "url" (bijvoorbeeld `{"naam": "A", "taal": "nl"}`) geeft geen traceback, maar de melding "FOUT  A: niet bereikbaar of time-out ('url')" en "Alle feeds mislukt", exitcode 1. Verwacht: melding dat de url ontbreekt, bij voorkeur exitcode 2. Niet geautomatiseerd.
3. NIET UITGEVOERD / PO-AANNAME ONJUIST (BELANGRIJK voor US-020 c1): de PO-opdracht zei dat de lijst met verzonnen bedrijfsnamen in git staat (commit 66e4d21, src/data.py). Dat klopt niet: commit 66e4d21 bevat geen bestanden (lege commit), src/data.py staat niet in de git-historie en ook niet elders in de projectmap. De bedrijfsnamen-controle kan dus niet worden gedaan. Vraag aan Stef: de 12 voorbeeldbedrijven aanleveren (of bevestigen dat ze nergens meer nodig zijn), dan voeg ik de test toe.
4. KLEIN (operationeel, niet van de bouw): src/__pycache__/ophalen.cpython-312.pyc (van 16:00, niet door mijn runs) staat nog in de projectmap; het is in .gitignore. Ik kan het niet verwijderen. Bouwer of orchestrator verwijdert het.
5. KLEIN (bekend, PO): Uitgelicht toont nog het OutSystems-productitem (Techzine) en het LUMC-item in Automatisering (zie it. 7 BEVINDING 1 en 4). Vaknieuws toont Engelse titels (US-014). Niet nieuw in deze ronde; niet in US-022.
6. OPERATIONEEL (niet door mij gestart, niet gestopt): een python.exe-proces (PID 34772) luistert op 127.0.0.1:8000 en stamt waarschijnlijk van de lokale app van iteratie 6/7 (src/app.py bestaat niet meer). Een tweede python.exe-proces (PID 43088) luistert op poort 8080. Ik heb ze niet gestopt, omdat ik niet weet van wie ze zijn. Stef of orchestrator controleert en stopt ze. Alle servers die ik zelf startte (testservers, headless Edge) zijn gestopt; er draait niets van mij meer.
7. Verkennend (VOLLEDIG): lege en rare invoer in het configbestand (leeg bestand, binair, map, ontbrekend) gaf nette meldingen (behalve BEVINDING 1 en 2). Snel klikken, terugnavigeren en herladen in een echte browser: NIET GETEST (alleen headless laden en screenshots).

NIET GETEST:
- US-020-c1 verzonnen bedrijfsnamen: de lijst bestaat niet meer in de projectmap of git (zie BEVINDING 3).
- US-013 c1 en c3: live site en GitHub-run (geen toegang).
- Interactie in een echte browser (klikken, toetsenbord, terugknop, herladen, snel klikken): niet in deze ronde.
- Visuele beoordeling van de Nieuws-pagina en het volledige Overzicht op 375 en 1280 px: alleen steekproef (Overzicht op beide breedtes bekeken). Smaak en totaalbeeld: Stef.
- Uitgelichte selectie en Vaknieuws-inhoud van de echte ronde: niet opnieuw beoordeeld (geen nieuwe ophaalronde, zoals opgedragen).
- Beslissing over de lead-regel: vastgelegd in tests/acceptance/README.md (sectie "Regel: het woord lead"). Een besluit in docs/decisions/ hoort de PO te schrijven; ik heb dat bestand niet aangeraakt.

BENODIGD VAN BOUWER:
- BELANGRIJK, blokkerend voor GESLAAGD: BEVINDING 1 oplossen in src/ophalen.py (configuratie-items valideren; nette melding; exitcode 2). Daarna opnieuw SNEL draaien (de test test_US022_c2_extra_* moet groen worden).
- KLEIN: BEVINDING 2 (melding bij ontbrekende url).
- Stef of PO: BEVINDING 3 (lijst van de 12 voorbeeldbedrijven of een besluit dat die controle vervalt). Zonder lijst blijft US-020 c1 deels NIET GETEST.
- Stef of orchestrator: BEVINDING 6 (stoppen van de oude python-processen op 8000 en 8080 als die van jullie zijn).
- Stef: US-013 c1/c3 blijven open tot na publicatie.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US022_afwerking.py (nieuw: US-022 c1 en c2, plus de extra test voor BEVINDING 1)
- tests/acceptance/test_US020_lokale_app_weg.py (EXEMPT-lijst sluitend: 3 paden; uitzonderingscontrole op de nieuwe regel)
- tests/acceptance/test_US012_statische_site.py (c6: "in totaal" -> "Alle <n> berichten bekijken")
- tests/acceptance/test_US016_mix.py (c4: idem; bytecode-verbod vóór de imports)
- tests/acceptance/test_statisch_regressie.py (US-001 c5: "Alles bekijken" -> "Alle <n> berichten bekijken")
- tests/acceptance/test_US010_categorie.py, test_US015_categorie.py, test_US017_weigerlijst.py, test_US018_uitgelicht.py (bytecode-verbod vóór de imports)
- tests/acceptance/test_US009_ronde2.py (subproces met -B)
- tests/acceptance/README.md (regel over het woord lead, iteratie 8, wijzigingen was -> nu)
- docs/test-reports/iteratie-8-ronde-1.md (dit rapport)
Verwijderd (niet door mij): test_acceptance.py, test_browser_layout.py, test_echte_data_app.py (door de Bouwer, met akkoord Stef).
Tijdelijke bestanden (site, screenshots, configs, Edge-profiel): alleen in de tijdelijke map van het systeem.
