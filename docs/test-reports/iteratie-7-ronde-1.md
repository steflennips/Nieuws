ITERATIE: 7 | RONDE: 1 | MODUS: VOLLEDIG
RESULTAAT: GESLAAGD

PER CRITERIUM:
- US-019-c1: OK. Config: AWS Big Data weg; 10 feeds (4 NL, 6 EN); 3 automatiseringsfeeds (Power Platform, Camunda, n8n); 3 BI-feeds; 4 NL-headnieuws (test_US019_c1_* 4x, geslaagd).
- US-019-c2: OK. Besluit-sectie "Wijzigingen iteratie 7": gratis, geen login, robots gecontroleerd, reden, afgevallen kandidaten; feed staat op bronnen.html (test_US019_c2_* 2x).
- US-019-c3: OK. Lokale testfeed: item van een bron niet in config weg; item van falende feed die wel in config staat blijft (test_US019_c3_items_van_bron_niet_in_config_*, geslaagd).
- US-019-c4: OK (meting, zie ECHTE OPHAALRONDE). Automatisering 22,1% (>=20%), BI+Data 43,0% (>=30%), geen feed >60% van een categorie. Nieuwe feed: 6 items.
- US-020-c1: OK voor product. src/app.py en src/data.py bestaan niet; geen leadwoorden of leadstatussen in src/, config/, README.md (test_US020_c1_* geslaagd). Verzonnen bedrijfsnamen: NIET GETEST (lijst zat in het verwijderde src/data.py). Uitzondering in tests/: zie BEVINDING 2.
- US-020-c2: OK. Geen bestand in src/ importeert http.server, app, data of logica; src/ bevat bouw.py, mix.py, ophalen.py, veilig_check.py.
- US-020-c3: OK. Verse kopie (zonder site/): ophalen met lokale testfeeds exitcode 0; bouwen exitcode 0; veilig_check exitcode 0; Bouwer-unittests 112 OK, geen ImportError.
- US-020-c4: OK. README: geen src/app.py, geen GEEN_BROWSER; wel ophalen, bouwen, http.server, feeds beheren, online zetten.
- US-021-c1: OK. Test: productblog met hoogste score niet in Uitgelicht, wel op Nieuws en in Vaknieuws. Echte data: Power BI-productnieuws staat in Vaknieuws, niet in Uitgelicht.
- US-021-c2: OK. Testconfig: exacte volgorde [6, 5 (NL-punt), 5, 4 nieuwer, 4]; productblog (Looker/Qlik) niet in Uitgelicht. README beschrijft het NL-punt.
- US-021-c3: OK. 2 geschikte items geven precies 2 (geen aanvulling); 0 items geeft "Nog geen uitgelicht nieuws", Vaknieuws blijft 5 items.
- US-021-c4: OK. Vaknieuws = 5 nieuwste niet in Uitgelicht, ongeacht taal (test geslaagd).
- US-001 c1-c6, US-002 c1-c6, US-004 c2, US-007 c1-c3, US-008 c1-c8, US-009 c6 (statische site): OK. Overzicht/Nieuws/Bronnen in headless Edge op 375 px (iframe) en 1280 px zonder horizontale overloop; stylesheet-tests op de gebouwde site; US-009 c6 getest op de gebouwde site (test_US012_browser, test_statisch_regressie, test_US008_c3_focusrand, test_US009_c6_site_*).
- US-012 c1-c8, US-015 c1-c12 (behalve de meldpunten), US-016 c1-c11, US-017 c1-c7, US-018 c1-c8: OK in de geautomatiseerde suite (geslaagd). US-016 c6 (meldpunt): zie ECHTE OPHAALRONDE.
- US-013 c2, c4, c5: OK (suite). US-013 c1 en c3: NIET GETEST (live site op github.io en run op GitHub; geen toegang).

SUITE: 264 tests, 256 geslaagd, 0 gefaald, 8 geskipt (vervallen lokale-app-tests, zie BEVINDING 2). Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v` (133 s). Ter vergelijking: vóór mijn aanpassingen 205 tests met 18 fouten (6 FAIL, 12 ERROR; de drie modules die de lokale app importeerden gaven een importfout). Bouwer-suite: `python -B -m unittest discover -s tests -v`: 112 OK (it. 6: 137; het verschil is de verwijderde lokale-app-tests; een baseline-commit ontbreekt, dus niet verifieerbaar).

REGRESSIE: OK. Statische site 375 px (iframe) en 1280 px in headless Edge; `python src/veilig_check.py` exitcode 0; workflow- en verse-checkouttests van iteratie 5 (test_IT5_*, test_US013_*) groen; alle criteria van it. 1-6 in de suite groen.

BEVINDINGEN:
1. KLEIN (PO beslist): Uitgelicht bevat vendor-productnieuws uit een headnieuws-nieuwssite: "OutSystems Agent Experience opent platform voor Claude Code en Cursor" (Techzine). Voldoet aan US-021 c2 (headnieuws). Stappen: bouw een ronde, lees index.html. Verwacht (doel Stef): nuttig nieuws voor MKB/ZZP. Werkelijk: 1 van 4 items is productnieuws (it. 6: 5 van 10).
2. KLEIN (housekeeping, actie nodig): test_acceptance.py, test_browser_layout.py en test_echte_data_app.py staan nog in tests/acceptance/ als geskipte modules (raise SkipTest, met reden). Verwijderen weigerde de auto-classifier (irreversible local destruction); ik heb niets omzeild. Deze drie bestanden bevatten nog 43 regels met het woord lead/leads, wat US-020 c1 letterlijk raakt voor tests/. Daarom staan ze in EXEMPT_TESTBESTANDEN (test_US020_lokale_app_weg.py), samen met test_US012_statische_site.py (zoektermen), dit README en de controle zelf; alles is gedocumenteerd in tests/acceptance/README.md ("Iteratie 7"). Oplossing: Stef of de orchestrator verwijdert de drie bestanden; daarna haal ik de uitzonderingen weg en draai ik de suite opnieuw.
3. KLEIN (meldpunt, PO/Stef): Data is klein: 5 van 86 items (5,8%). Het Data-filter is bijna leeg. Geen criterium geschonden (US-016 c6 en US-019 c4 zijn meldpunten). Feed-aandeel: Microsoft Fabric is precies 60% van Data (de grens, niet erboven).
4. KLEIN: "AI helpt verpleegkundigen wonden sneller vast te leggen bij LUMC" (Emerce) staat in Uitgelicht als Automatisering, terwijl de titel over AI gaat (bekend van it. 6, BEVINDING 3).
5. KLEIN (US-014, COULD): Engelse titels en samenvattingen op de site. Vaknieuws: 3 van 5 items Engels (n8n-listicle, Power BI-featuresummary, Power Pages). Nieuws: veel Engelse boilerplate-samenvattingen (bijv. "If you haven't already, check out FabCon ...").
6. KLEIN: de kop van Vaknieuws toont "86 in totaal"; dat is het aantal van alle items, niet van dit blok. Verwarrend voor de lezer.
7. KLEIN: `python src/ophalen.py --config <bestaat niet>` geeft exitcode 2 en een Nederlandse melding, met Engelse OS-tekst achter de dubbele punt (bekend, it. 6 BEVINDING 4). `bouw.py --vandaag 2026-02-30` geeft exitcode 1 en een Nederlandse melding, geen traceback.
8. KLEIN: src/__pycache__/ophalen.cpython-312.pyc is ontstaan door een import in de acceptatietests (zonder -B). Map staat in .gitignore. Niet verwijderd (rechten). Niet gecorrigeerd in deze ronde: de importeurs in test_US010/US015/US016/US017/US018 zetten het bytecode-verbod pas na de import; dat wordt in de volgende ronde rechtgezet.
9. OPERATIONEEL (geen productfout): een proces `python src/app.py` (PID 34772, gestart 8 okt 2026 om 18:32, niet door mij gestart) luistert nog op 127.0.0.1:8000. Ik heb het niet gestopt: het is niet mijn proces en het kan van Stef zijn. Stef of de orchestrator stopt het. Eigen servers (statische server voor de checks, Edge-processen) zijn gestopt. Let op: bij het zoeken naar dat proces heb ik per ongeluk `taskkill` op PID 0 geprobeerd; Windows weigerde dat (systeemproces). Er is niets gestopt behalve mijn eigen server.
10. Verkennend (VOLLEDIG): rare invoer op de statische site: `/nieuws.html?q=<script>`, `?q=%%'"` en `?categorie=onbekend` geven 200 en tonen geen ruwe script; app.js gebruikt textContent (geen innerHTML). Synthetische dataset van 5000 items bouwt zonder fout (exitcode 0). Snel klikken, terugnavigeren, herladen en toetsenbord in een echte browser: NIET GETEST (alleen headless laden en metingen).
11. Basischecks: console-fouten: de browsertests met assertGeenConsoleFouten slagen bij het laden van de statische pagina's; 404 voor onbekende paden (lokale static server; GitHub Pages toont 404.html). README klopt met code en uitvoer: 10 feeds, exitcodes 0/1/2, scoreregel, --vandaag-formaat, online-zetten-stappen, lokaal bekijken met http.server (proef gedaan op de tijdelijke site: 200 voor index, nieuws, bronnen, favicon).
12. Uiterlijk (headless Edge, screenshots in tijdelijke map, bekeken): 1280 px Overzicht en Nieuws (filter BI): donkerblauwe kop, grijze achtergrond, witte kaarten, teal alleen op links, actief menu, actief filter en knop; netjes. 375 px Overzicht: menu volledig in beeld, tegels onder elkaar, geen horizontale overloop. Totaalbeeld en smaak beoordeelt Stef.

ECHTE OPHAALRONDE (9 okt 2026, lege tijdelijke map <tmp>, standaard robots-controle aan; 10 feeds OK; 86 items opgeslagen; bouw naar <tmp>/site, zonder --vandaag):
- Per feed (items in feed / bewaard): Power BI Blog 20/13; Microsoft Fabric Blog 20/20; SQLBI 30/2; Microsoft Power Platform Blog 10/6 (nieuw); Camunda 50/13 (2 geweigerd); n8n 15/12 (1 geweigerd); Computable 10/4; Emerce 10/2 (1 geweigerd); Techzine 10/4; NOS Tech 20/10.
- Per categorie (van 86; AI-plafond niet actief, AI 34,9%): BI 32 (37,2%); Data 5 (5,8%); Automatisering 19 (22,1%); AI 30 (34,9%). Tellers op de site komen overeen.
- Per feed in BI (32): Fabric 17 (53%), Power BI 12 (38%), SQLBI 2, Camunda 1.
- Per feed in Data (5): Fabric 3 (60%), Power BI 1, Power Platform 1.
- Per feed in Automatisering (19): n8n 7 (37%), Camunda 5 (26%), Power Platform 4 (21%), Techzine 2, Emerce 1.
- Per feed in AI (30): NOS Tech 10 (33%), Camunda 7, n8n 5, Computable 4, Techzine 2, Emerce 1, Power Platform 1.
- Meetpunten: Automatisering >=20%: gehaald (22,1%). BI+Data >=30%: gehaald (43,0%). Geen feed >60% van een categorie: gehaald, net (Fabric 60% van Data; hoogste in BI 53%). Data blijft klein (BEVINDING 3).
- Uitgelicht (4 items, 2 AI): (1) "Ai jaagt cyberdreigingen aan, organisaties moeten veerkrachtig worden" (Computable, AI): matig, zakelijk relevant. (2) "Microsoft introduceert hybride ai voor Windows 11: slimmer en goedkoper" (Computable, AI): matig, OS-nieuws. (3) "OutSystems Agent Experience opent platform voor Claude Code en Cursor" (Techzine, Automatisering): vendor-productnieuws (BEVINDING 1). (4) "AI helpt verpleegkundigen wonden sneller vast te leggen bij LUMC" (Emerce, Automatisering): NL, relevant (BEVINDING 4). Correct uitgesloten: "Kort: ..." (digest), "Begin bij het einde: ..." (evenement), AI-items boven het plafond van 2. Oordeel: alle vier titels in het Nederlands (de OutSystems-titel bevat wel Engelse productnamen; it. 6: 4 van 10 Engelstalig), 1 productitem (it. 6: 5 van 10). Verbeterd; de NL-voorkeur werkt.
- Vaknieuws (5): "IT Automation Software: 6 Tools for Different IT Jobs" (n8n, EN listicle, KLEIN); "Kleine groepje klanten levert AI-reuzen meeste omzet" (Emerce, AI, redelijk); "Power BI September 2026 Feature Summary" (EN productrelease, KLEIN); "Microsoft Power Pages is now available in Sweden Central and Italy North" (EN productnieuws, KLEIN); "Compacte en snelle Claude Haiku 5.5 vervangt eindelijk 4.5" (Techzine, AI, productnieuws, redelijk). Maximaal 2 AI: gehaald.

NIET GETEST:
- US-013 c1 en c3: live site op github.io en een run op GitHub (geen toegang).
- Interactie in een echte browser (klikken, terugknop, herladen, snel klikken, Tab): niet in deze ronde.
- US-020 c1 verzonnen bedrijfsnamen: de lijst zat in het verwijderde src/data.py; alleen de generieke controles zijn gedaan.
- Visueel 375 px en 1280 px van Nieuws met alle filters en tellers: alleen steekproef (zie BEVINDING 12).

BENODIGD VAN BOUWER:
- Geen blokkerend werk; geen fixronde nodig.
- Stef of de orchestrator: (a) verwijder test_acceptance.py, test_browser_layout.py en test_echte_data_app.py uit tests/acceptance/ (de auto-classifier weigerde dat voor de Tester; BEVINDING 2); (b) stop het proces op poort 8000 (python src/app.py, PID 34772) als dat van jou is (BEVINDING 9); (c) PO: Uitgelicht-productitem (BEVINDING 1) en de kleine Data-categorie (BEVINDING 3) beoordelen; (d) US-013 c1/c3 blijft open tot na publicatie.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/hulp_stijl.py (nieuw)
- tests/acceptance/test_US019_automatiseringsfeed.py (nieuw)
- tests/acceptance/test_US020_lokale_app_weg.py (nieuw)
- tests/acceptance/test_US021_uitgelicht.py (nieuw)
- tests/acceptance/test_statisch_regressie.py (importbron naar hulp_stijl.py)
- tests/acceptance/test_US008_c3_focusrand.py (stylesheet uit de gebouwde site)
- tests/acceptance/test_US009_feeds.py (c6 op de gebouwde site; app-helpers verwijderd)
- tests/acceptance/test_US012_statische_site.py (c3 generiek, leadlijst niet meer beschikbaar)
- tests/acceptance/test_US013_workflow.py ("openbare" -> "openbaar")
- tests/acceptance/test_US015_c7_feeds.py (herschreven naar de nieuwe criteriumtekst, op naam)
- tests/acceptance/test_US015_c11_datafeed.py (herschreven naar de nieuwe criteriumtekst, geen AWS)
- tests/acceptance/test_US016_mix.py (BI-regel op naam; c4 lokale app geskipt)
- tests/acceptance/test_US018_c7_c8_evenement_kort_ai.py (fixture: AI A/B uit Computable)
- tests/acceptance/test_US018_uitgelicht.py (fixture-standaardbron Computable; c3 volgens US-021; TestUS018Lokaal geskipt)
- tests/acceptance/test_iteratie5_online.py (voorbeelddata-controle generiek)
- tests/acceptance/test_acceptance.py (geskipt: VERVALLEN, lokale app)
- tests/acceptance/test_browser_layout.py (geskipt: VERVALLEN, lokale app)
- tests/acceptance/test_echte_data_app.py (geskipt: VERVALLEN, lokale app)
- tests/acceptance/README.md (draaien bijgewerkt; sectie "Iteratie 7" met nieuwe tests, regressie-dekking en vervallen tests per test)
- docs/test-reports/iteratie-7-ronde-1.md (dit rapport)
Tijdelijke bestanden (ophaalronde, gebouwde sites, screenshots, Edge-profielen, testkopie): alleen in de tijdelijke map van het systeem.
