ITERATIE: 6 (gecombineerd met iteratie 5: online zetten voorbereiden) | RONDE: 1 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD

BEVINDING 1 is BLOKKEREND (regressie US-008 c8 op 375 px). Daarnaast staan er drie BELANGRIJKE bevindingen open (2, 3, 4).
Tester-oordeel: de functionele criteria van US-016, US-017 en US-018 zijn met de suite aangetoond. De openbare site is nog niet klaar voor publicatie: de promotie in Uitgelicht, de categoriefout NOS -> Data en de 375 px-regressie moeten eerst opgelost of door de PO beslist worden.

PER CRITERIUM:
- US-016-c1: OK. Vier categorieen BI, Data, Automatisering, AI; BI 32, Data 51, Automatisering 42, AI 29 trefwoorden (alle >= 15); verplichte termen aanwezig (test_US016_c1_*).
- US-016-c2: OK. Gelijkspel BI/AI -> BI, BI/Data -> BI, Data/Automatisering -> Data, Automatisering/AI -> Automatisering, 6 titels (test_US016_c2_*).
- US-016-c3: OK. AI-woord alleen in samenvatting: geen categorie, item niet opgeslagen; AI in titel telt (test_US016_c3_*, 3 tests).
- US-016-c4: OK. Mix 80 AI + 20 overig: 33 items, 13 AI = de 13 nieuwste; site, tellers en Overzicht tonen 33 (fixture); plafond geverifieerd voor 0-200 overige items (exact gerekend); echte data: AI 31 van 103 = 30%.
- US-016-c5: OK (automatisch). 10 feeds, 6 EN, 4 NL; 3 BI-feeds (Power BI, Fabric, SQLBI); 4 algemene NL-bronnen; elke feed in nieuwsfeeds.md (robots/gratis/geen login) en op bronnen.html.
- US-016-c6: NIET AUTOMATISCH (meldpunt, echte ronde, zie hieronder): BI+Data 50% (>= 30%, gehaald); Automatisering 19,4% (net onder 20%, gemeld); AWS Big Data 61% van Data (> 60%, gemeld). Niet blokkerend.
- US-016-c7: OK (browser 375 en 1280 px; statisch en lokaal). Filterknoppen Alle, BI, Data, Automatisering, AI op Nieuws; tegels BI, Data, Automatisering, AI op Overzicht; categorie=bi werkt (3 kaarten); geen horizontaal scrollen; geen console-fouten. Zie BACKLOG-tegenstrijdigheid (bevinding 8).
- US-017-c1: OK. Weigerlijst bevat alle verplichte termen; promotietermen in samenvatting-lijst (test_US017_c1).
- US-017-c2: OK. Weigerterm in titel, ook met trefwoordtreffer en in hoofdletters, niet opgeslagen; "consolidatie" niet geweigerd (test_US017_c2_*).
- US-017-c3: OK. sponsored, gesponsord, partnerbijdrage, advertorial alleen in samenvatting: geweigerd; gewone samenvatting blijft (test_US017_c3).
- US-017-c4: OK. Testset 12 titels (6 geweigerd, 6 toegelaten); overnametitel met "deal" en "Dealer-netwerk" toegelaten (test_US017_c4_*).
- US-017-c5: OK (formaat, automatisch); echte aantallen gemeld: SQLBI 1 (zie bevinding 5), AWS Big Data 1 (zie bevinding 5), 8 feeds 0. Voorbeeldtitels worden per feed getoond.
- US-018-c1: OK. 4 algemene NL-feeds met headnieuws; deux_relevantie bevat alle 19 verplichte termen (test_US018_c1_*).
- US-018-c2: OK. Uitgelicht staat boven de tellertegels; max 5; alleen laatste 3 dagen; hooguit 2 AI; velden titel, link, bron, datum, categorie. Statisch en lokaal (test_US018_c2_*). Echte data: 5 items, 2 AI.
- US-018-c3: OK. Scoreregel (2 punten headnieuws + 1 punt per verschillende term) in README; vaste volgorde van 6 titels; term telt een keer; hele woorden (test_US018_c3_*).
- US-018-c4: OK. Minder dan 5: alleen beschikbare items; 0 items: "Nog geen uitgelicht nieuws", exitcode 0; statisch en lokaal (test_US018_c4_*).
- US-018-c5: OK. Vaknieuws = 5 nieuwste items die niet in Uitgelicht staan; statisch en lokaal; geen overlap (test_US018_c5_*).
- US-018-c6: OK voor overloop (375 en 1280 px, browser, geen console-fouten). De accentkleur en de 2x2-tegels: zie BEVINDING 1 (US-008 c8).
- US-015-c12: VERVALLEN, vervangen door US-016 c6 (BACKLOG-tekst gecontroleerd, test_US015_c12_is_vervangen_door_US016_c6_in_backlog). Geen harde test meer.
- US-013-c1: NIET GETEST: vereist de live site op github.io (hosting-account Stef).
- US-013-c2: OK. Cron "0 4 * * *" (04:00 UTC = 06:00 CEST), workflow_dispatch, rechten contents/pages/id-token write (test_IT5_c2_*, test_IT5_rechten_*).
- US-013-c3: NIET GETEST: vereist een run op GitHub en de live site.
- US-013-c4: OK. Geen secrets in de workflow; veilig_check exitcode 0; geheimenscan in de suite (test_IT5_c4_*, veilig_check).
- US-013-c5: OK. README: feed toevoegen met letterlijke regel uit config, handmatig starten (suite US-013 c5).
- Iteratie 5, .gitignore: OK. Alle veiligheidsregels aanwezig (test_IT5_gitignore_bevat_veiligheidsregels).
- Iteratie 5, veilig_check: OK. `python src/veilig_check.py` eindigt met exitcode 0 en de OK-regel (alleen-lezen controle).
- Iteratie 5, workflow: OK. YAML-tekstcontrole: cron, dispatch, minimale rechten, geen eigen sleutels, volgorde ophalen -> bouwen -> artefact -> publiceren, needs bouwen, geen if: always(), geen continue-on-error, data alleen committen bij wijziging (test_IT5_*).
- Iteratie 5, verse checkout: OK. Zonder data/nieuws.json en met een leeg bestand, alle feeds down: ophalen exitcode 1, geen bestand aangemaakt of aangepast, bouw exitcode 1, geen site, geen traceback. Met een werkende feed: publicatie zonder voorbeelddata (test_IT5_verse_checkout_*, test_IT5_leeg_*, test_IT5_ontbrekend_*).
- Iteratie 5, subpad /<repo>/: OK. Alle interne links (pagina's, css, js, favicons, zoekfilter) blijven onder het repo-pad en geven 200 (test_IT5_subpad_*).
- Iteratie 5, README stappen A-E: OK. Alle commando's en namen staan er; de stopinstructie bij het toplevel-pad staat erin; geen lokaal pad of persoonlijk account in README (test_IT5_readme_*). Handmatige controle (read-only): `git rev-parse --show-toplevel` geeft de gebruikersmap boven de projectmap (<gebruikersmap>, het pad eindigt op de gebruikersnaam), dus de README-stop van stap C geldt nu. Ik heb geen git init, commit of push uitgevoerd.
- US-001 c2/c3/c5/c6 (statisch), US-002, US-004, US-007, US-008 c1-c7, US-009 t/m US-012, US-015 (behalve c12): OK, behalve US-008 c8 (BEVINDING 1). Zie REGRESSIE.

SUITE: 253 tests, 252 geslaagd, 1 FAALT (test_US008_c8_statisch_375_px_kaarten_onder_elkaar), 0 overgeslagen (headless Edge aanwezig). Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v`. Bouwer-suite (README): `python -B -m unittest discover -s tests -v`: 121 OK.

REGRESSIE: NIET OK. Wat faalt: US-008 c8 op 375 px (BEVINDING 1). Verder OK: de volledige suite (iteratie 1 t/m 5), de lokale app met echte data (en voorbeelddata via test), statische site 375 en 1280 px (iframe-methode, headless Edge), echte-data tests (AI-plafond, tellers, bronnenlijst).

BEVINDINGEN:
1. BLOKKEREND, regressie US-008 c8 (375 px). De vierde tellertegel (BI, it. 6) zet de tellertegels op Overzicht in 2 kolommen naast elkaar op 375 px. Criterium: "staan kaarten onder elkaar". Test: test_US012_browser.test_US008_c8_statisch_375_px_kaarten_onder_elkaar, assert 2 != 1. Reproduceer: `python src/bouw.py --uit <tmp>` met data, open index.html in iframe 375 px. Verwacht: 1 kolom. Werkelijk: 2x2 (screenshot leesbaar, maar het criterium is letterlijk niet gehaald). Ik heb de test NIET verzwakt. Oplossing of besluit PO: tegels onder elkaar bij 375 px, of criterium aanpassen.
2. BELANGRIJK, promotie in Uitgelicht en Automatisering. "Nog vier weken tot Emerce EDAY" (Emerce, 8 okt 2026) staat in Uitgelicht (5e item) en in Automatisering. Dat is een evenementpromo; het doel van US-017 (geen marketing) is niet gehaald. Verwacht: uitgefilterd. Werkelijk: opgenomen. Besluit PO: weigerterm of regel voor evenementen.
3. BELANGRIJK, vendor-PR in de mix (US-017 doel). Automatisering bevat "Camunda Named a Leader in The Forrester Wave: Adaptive Process Orchestration Software, Q3 2026", "Camunda Recognized as a Visionary in Gartner BOAT Magic Quadrant 2026" en "You can now top up your n8n Assistant credits" (n8n-productmarketing). Verwacht: productnieuws en marketing gefilterd (US-017 intentie). Werkelijk: aanwezig. Besluit PO (weigerlijst of bronkeuze).
4. BELANGRIJK, categoriefout. Drie NOS Tech-items over hacks en datalekken staan in Data: "Amsterdammer opgepakt in onderzoek naar hackerscollectief ShinyHunters", "Hackers persen klanten boodschappendienst Flink af: betalen of data gepubliceerd", "Datalek bij reisapp Polarsteps: iedereen kon meekijken, ook met afgeschermde reizen". Oorzaak: het trefwoord "gegevens" (Data, te breed) matcht in de samenvatting. Verwacht: niet Data. Werkelijk: Data. Reproduceer: categoriseer(titel, samenvatting) met config/feeds.json.
5. KLEIN, weigerlijst met valse positieven. "Run an automated operational review with the Amazon Redshift MCP server" (AWS Big Data, geweigerd door "review*") en "Gemini, metadata and the analogy game" (SQLBI, geweigerd door "game*"). Dit volgt de letterlijke lijst, maar "review" is hier geen productrecensie. Besluit PO/Bouwer.
6. KLEIN, ongeldige datum laat de bouw falen. Een item met datum "garbage" in data/nieuws.json geeft `FOUT: not enough values to unpack (expected 3, got 1)`, exitcode 1 (geen traceback). Het ophaalcommando schrijft altijd ISO-datums, dus het risico is laag. Verwacht: het item overslaan (zoals US-011 c5).
7. KLEIN, alleen AI-items. Een databestand met uitsluitend AI-items (10 stuks) geeft "bevat geen nieuwsitems; er wordt niets gebouwd" (exitcode 1). Het AI-plafond snijdt alles weg, en de melding is misleidend. Gevolg: de publicatie blijft oud. Met vier categorieen is dit onwaarschijnlijk. Besluit PO.
8. KLEIN, BACKLOG-tegenstrijdigheid. US-016 c7 vraagt "tellertegels en filterknoppen" op Overzicht EN Nieuws; US-008 c6 verbiedt tellertegels op Nieuws. Ik heb de tellertegels op Overzicht en de filterknoppen op Nieuws getoetst. Bevestiging PO.
9. KLEIN, relevantie (PO beslist). In Data staan veel technische AWS-diepteartikelen (MSK, EMR, MWAA, Glue), weinig relevant voor MKB/ZZP. Vaknieuws bevat digest- en listicle-items ("Kort: ..."). Kwaliteit, geen criterium.
10. KLEIN, meetlog. ophalen meldt voor Camunda "19 nieuw", maar er staan 15 unieke items in het bestand; de log telt dubbele links binnen een feed dubbel. Niet nader onderzocht.

UITGELICHT (kwaliteit, site van de echte ronde 8 okt 2026, 5 items): 4 van 5 zakelijk relevant (Computable AI-cyber; Power BI September Feature Summary; Computable hybride AI Windows 11; Techzine agentic remediation, technisch). 1 evenementpromo (bevinding 2). Vaknieuws (5): 3 relevant, 1 digest ("Kort: ..."), 1 product-launch (Claude Haiku 5.5, Techzine).

MEETPUNTEN ECHTE OPHAALRONDE (1 ronde naar tijdelijke map, 8 okt 2026; alle 10 feeds OK; 103 items getoond, AI-plafond niet actief):
- Per categorie: BI 34 (33%), Data 18 (17%), Automatisering 20 (19%), AI 31 (30%). AI-aandeel 30% (<= 40%: gehaald). BI+Data 50% (>= 30%: gehaald). Automatisering 19,4% (< 20%: gemeld).
- Per feed in BI: Microsoft Fabric 17 (50%), Power BI 12 (35%), SQLBI 2, AWS Big Data 2, Camunda 1.
- Per feed in Data: AWS Big Data 11 (61%, > 60%: gemeld), Fabric 3, NOS Tech 3, Power BI 1.
- Per feed in Automatisering: n8n 8 (40%), Camunda 7 (35%), Techzine 2, Emerce 2, AWS 1.
- Per feed in AI: NOS Tech 10 (32%), Camunda 7 (23%), n8n 5, Computable 4, Techzine 2, AWS 2, Emerce 1.
- Weigeringen per feed: SQLBI 1, AWS Big Data 1 (voorbeelden in bevinding 5); overige feeds 0.

BASISCHECKS (VOLLEDIG): lokale app gestart (`PORT=8765 GEEN_BROWSER=1 python src/app.py`, achtergrond): /, /nieuws, /leads, /nieuws?categorie=bi, ?q=<script>, lange zoekterm: 200; /favicon.ico 204; /nietbestaand 404; serverlog alleen "App draait op ..."; gestopt. Statische site: geen console-fouten op index en nieuws (browser-proxy). README klopt op de punten die ik heb gecontroleerd (feeds, categorieen, AI-plafond, Uitgelicht, bouwopties, online-stappen A-E); geen lokaal pad.

VERKENNEND (tijdelijke map): alleen-AI-data (bevinding 7); ongeldige URL (javascript:) wordt geweigerd; HTML en onerror in titel en bron worden ge-escaped; ampersand in titel correct; 3000 items (1000 AI) bouwen in 0,3 s met AI 33%; datum in de toekomst (2026-12-31) wordt getoond; ongeldige datum (bevinding 6).

UITERLIJK (headless Edge, screenshots in de tijdelijke map, 375 px via iframe, 1280 px direct): Overzicht en Nieuws: donkerblauwe kop, grijze achtergrond, witte kaarten, teal accent op links, actief menu en actief filter; geen horizontaal scrollen; Uitgelicht leesbaar; filterknoppen wrappen netjes. Afwijking: tellertegels 2x2 op 375 px (bevinding 1). Het totaalbeeld beoordeelt Stef.

NIET GETEST:
- GitHub-uitvoering van de workflow, Pages en de live site (US-013 c1, c3; /nieuws zonder .html op Pages): geen toegang tot GitHub.
- Console-fouten op de live site en in de lokale app in een echte browser; alleen via de browser-proxy (statisch) en serverlog (lokaal).
- Interactie in een echte browser: klikken, terugknop, herladen, snel klikken, toetsenbord (Tab), echt toestel, browser die zich automatisch opent.
- Grote datasets met echte browser (wel gebouwd en gemeten zonder browser).

BENODIGD VAN BOUWER: (1) bevinding 1: tegels op 375 px onder elkaar, of PO-besluit over het criterium. (2) bevinding 4: term "gegevens" beperken (en bevinding 2/3 na PO-besluit over weigerlijst). PO: besluiten over bevindingen 2, 3, 5, 7, 8, 9.

REGEL PER AANGEPASTE TEST (was -> nu, waarom; geen criterium verzwakt):
1. test_US010_c1: categorieset {Data, Automatisering, AI} -> + BI (US-016 c1).
2. test_US010_c2: AI in samenvatting "is AI" -> None; AI in titel telt (US-016 c3).
3. test_US010_c3: gelijkspel-volgorde AI/Auto/Data -> BI/Data/Auto/AI (US-016 c2); "Data en AI" -> "Dataset en AI" (los "data" telt sinds it. 4 niet).
4. test_US010_c5: "Dashboards voor betere bedrijfsrapportage" Data -> BI (US-016 c1).
5. test_US015_c4: "Nieuw dashboard ... rapportages ..." Data -> BI (US-016 c1).
6. test_US015_c10: "business intelligence" en "Power BI" uit de Data-termen (BACKLOG US-015 notitie); extra titel "Power BI krijgt ..." -> "Databricks brengt ... dataplatform uit".
7. hulp_statisch fixture item 7: AI -> BI (AI-plafond met 4 AI en 4 overig liet een AI-item weg); AI-tellingen in fixture-tests 4 -> 3, total 8 blijft.
8. hulp_statisch.bouw(): parameter vandaag (vaste peildatum 2026-10-08 voor Uitgelicht; was klokdatum).
9. test_US012_c4 (statisch): zip-volgorde -> koppelen op link (robuust bij gelijke datums).
10. test_US012_c6 vijf nieuwste: -> vaknieuws = 5 nieuwste niet in Uitgelicht (US-018 c5).
11. test_US012_c6 tellers: BI toegevoegd (US-016 c7).
12. TestSiteEchteData: items zonder BI (70 van 104) -> incl. BI en AI-plafond (verwacht_getoond).
13. test_US012_c5_bronnenlijst fixture: AI -> Data (AI-plafond verwijderde alle items).
14. test_US012_browser fixture AI 4 -> 3; test_US004_c2 statisch 1280 px "3 kolommen" -> "4 tegels naast elkaar" (4 categorietellers). De 375 px-test (test_US008_c8) is NIET aangepast (bevinding 1).
15. test_statisch_regressie: tegels 3 -> 4; categorielijst incl. BI.
16. test_acceptance US-004 c1/c4 (lokale app): vijf nieuwste -> vaknieuws (US-018 c5); regex accepteert bron-element (US-018 c2).
17. test_echte_data_app: samenvatting-test AI -> Data (los AI-item valt weg door het plafond); overzichtstest: nieuwste item in Uitgelicht of vaknieuws (US-018).
18. test_US009_c6: verwachte aantallen en links na het AI-plafond (verwacht_getoond).
Twee tests gecorrigeerd op eigen fout (geen criterium): test_US016 (testzin) en test_iteratie5 (regex die "https://" als pad zag, en mijn eigen tekst met de naam van een cloudmap die de veiligheidscontrole terecht aansloeg).

NIEUWE TESTBESTANDEN: tests/acceptance/test_US016_mix.py, test_US017_weigerlijst.py, test_US018_uitgelicht.py, test_iteratie5_online.py, hulp_browser.py. Overzicht criterium -> testnaam in tests/acceptance/README.md.

BESTANDEN GEWIJZIGD DOOR MIJ: tests/acceptance/README.md, tests/acceptance/hulp_statisch.py, tests/acceptance/hulp_browser.py (nieuw), tests/acceptance/test_US009_feeds.py, test_US010_categorie.py, test_US012_browser.py, test_US012_c5_bronnenlijst.py, test_US012_statische_site.py, test_US015_categorie.py, test_acceptance.py, test_echte_data_app.py, test_statisch_regressie.py, test_US016_mix.py (nieuw), test_US017_weigerlijst.py (nieuw), test_US018_uitgelicht.py (nieuw), test_iteratie5_online.py (nieuw), docs/test-reports/iteratie-6-ronde-1.md (dit rapport). Tijdelijke bestanden (ophaalronde, gebouwde sites, screenshots, Edge-profielen) alleen in de systeem-tijdelijke map. Geen wijzigingen in src/, config/, data/, site/, docs/ buiten dit rapport, of de hoofdmap. Servers: mijn app-proces (poort 8765) is gestopt. Niet van mij en niet aangeraakt: app.py op poort 8000 (PID 34772, gestart 18:32) en een proces op poort 8080 (PID 43088).
