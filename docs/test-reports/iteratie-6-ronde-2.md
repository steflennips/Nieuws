ITERATIE: 6 | RONDE: 2 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD

Reden: 1 BLOKKEREND (US-017 c5, deel "unieke links per feed" faalt) en 2 BELANGRIJKE bevindingen open (promotie in Uitgelicht; meldpunt US-016 c6 niet gehaald). De eerdere vier falende tests zijn opgelost (drie tests aangepast met reden, een lokaal pad uit mijn ronde-1 rapport gehaald).

PER CRITERIUM:
- US-008-c8: OK. 375 px: tegels Overzicht in 1 kolom (test_US008_c8_statisch_375_px_kaarten_onder_elkaar, test_US008_c8_375_px_kaarten_onder_elkaar_en_leesbaar lokaal; screenshot 375 px bekeken). 1280 px: 4 tegels naast elkaar (test_US004_c2_statisch_1280_px_tegels_naast_elkaar; screenshot).
- US-008-c1 t/m c7: OK (regressie suite, test_US008_c1..c7 en test_US008_c3_focusrand_*).
- US-016-c1: OK. Vier categorieen BI, Data, Automatisering, AI, elk >= 15 trefwoorden (test_US016_c1_*).
- US-016-c2: OK. Gelijkspel BI/AI -> BI, 6 titels (test_US016_c2_*).
- US-016-c3: OK. AI alleen in samenvatting telt niet mee (test_US016_c3_*).
- US-016-c4: OK. 80 AI + 20 overig -> 13 AI, 33 getoond; echte ronde: AI 31 van 96 = 32% (test_US016_c4_*).
- US-016-c5: OK. 10 feeds, 6 EN, 4 NL, 3 BI-feeds; elke feed in feedbesluit en op bronnen.html (test_US016_c5_*).
- US-016-c6: OPEN PUNT (meldpunt, niet hard getoetst). Gemeten op echte ronde: BI+Data 51,0% (doel >= 30%: gehaald); Automatisering 16,7% (doel >= 20%: niet gehaald); AWS Big Data Blog 73% van Data (doel <= 60%: niet gehaald). Zie BEVINDING 3.
- US-016-c7: OK. Tegels BI/Data/Automatisering/AI op Overzicht, filterknoppen Alle/BI/Data/Automatisering/AI op Nieuws, categorie=bi werkt; 375 en 1280 px zonder horizontaal scrollen (test_US016_c7_*, browser). Lokale app: zie BEVINDING 6.
- US-016-c8: OK (fixronde 1). "gegevens" los is geen Data-trefwoord (test_US016_c8_los_gegevens_is_geen_data_trefwoord). De drie NOS-titels met hun opgeslagen samenvatting krijgen geen Data (test_US016_c8_drie_nos_titels_met_echte_samenvatting_krijgen_geen_data).
- US-016-c9: OK (fixronde 1). Item met datum "garbage": waarschuwing met titel en link, goede items getoond, exitcode 0 (test_US016_c9_*; ook handmatig gecontroleerd).
- US-016-c10: OK (fixronde 1). Alleen AI-items: exitcode 1, melding "... door het AI-plafond (maximaal 40% AI) blijft niets over" (test_US016_c10_*; handmatig gecontroleerd).
- US-017-c1: OK. Weigerlijst bevat alle verplichte termen; promotietermen in samenvatting-lijst (test_US017_c1_*).
- US-017-c2: OK. Weigerterm in titel, ook met trefwoordtreffer en in hoofdletters, wordt niet opgeslagen (test_US017_c2_*).
- US-017-c3: OK. sponsored/gesponsord/partnerbijdrage/advertorial alleen in samenvatting: geweigerd (test_US017_c3_*).
- US-017-c4: OK. Vaste testset 12 titels: 5 geweigerd, 7 toegelaten, incl. overname met "deal" en "Dealer-netwerk" (test_US017_c4_*; testset aangepast, zie AANGEPASTE TESTS).
- US-017-c5: FAALT. Formaat OK (test_US017_c5_ophaaluitvoer_*), maar dubbele geweigerde link in een feed telt twee keer (test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer). Zie BEVINDING 1. Echte aantallen per feed: Camunda 2, n8n 1, Emerce 1, overige 7 feeds 0 (voorbeelden in de uitvoer).
- US-017-c6: OK. Config bevat evenement- en vendor-PR-patronen incl. regex "nog <getal> ... tot" (test_US017_c6_configuratie_*). Geweigerd: "Nog vier weken tot Emerce EDAY", "Camunda Named a Leader ... Forrester Wave ...", "Camunda Recognized as a Visionary ... Magic Quadrant 2026", "You can now top up your n8n Assistant credits" (test_US017_c6_evenementpromo_*). Toegelaten: "Salesforce neemt Informatica over", "Power BI September 2026 Feature Summary", Fabric-release "... generally available", "Gartner ziet BI-markt groeien" (test_US017_c6_overname_*).
- US-017-c7: OK. Uitzonderingslijst bevat alle termen (test_US017_c7_uitzonderingslijst_*); "Run an automated operational review ..." en "Gemini, metadata and the analogy game" toegelaten; "Review: Samsung Galaxy S26", "Nieuwe games met AI-personages", "Analogy game: nieuwe game voor AI" geweigerd (test_US017_c7_*).
- US-018-c1: OK. 4 algemene NL-feeds headnieuws (Computable, Emerce, Techzine, NOS Tech); deux_relevantie compleet (test_US018_c1_*).
- US-018-c2: OK. Uitgelicht boven de tellers, max 5, laatste 3 dagen, 2 AI in de echte ronde (test_US018_c2_*; browser en lokaal).
- US-018-c3: OK. Scoreregel in README; vaste volgorde van 6 titels (test_US018_c3_*).
- US-018-c4: OK. Minder dan 5 toont beschikbare items; 0 items "Nog geen uitgelicht nieuws" (test_US018_c4_*).
- US-018-c5: OK. Vaknieuws = 5 nieuwste die niet in Uitgelicht staan, geen overlap (test_US018_c5_*).
- US-018-c6: OK. Startpagina 375 en 1280 px zonder horizontaal scrollen; geen console-fouten (test_US018_c6_*; screenshot Overzicht 375 en 1280 px bekeken).
- US-010-c1: OK (aangepast, zie AANGEPASTE TESTS, punt 1).
- US-011-c5: OK (fixture aangepast, zie AANGEPASTE TESTS, punt 2).
- US-013-c1: NIET GETEST. Vereist de live site op github.io (geen toegang).
- US-013-c2: OK. Cron 0 4 * * *, workflow_dispatch, minimale rechten (test_US013_c2_*, test_IT5_*).
- US-013-c3: NIET GETEST. Vereist een run op GitHub en de live site.
- US-013-c4: OK. Geen secrets in workflow; geheimenscan OK; veilig_check exitcode 0 (test_US013_c4_*, test_IT5_veilig_check_eindigt_met_exitcode_0).
- US-013-c5: OK. README: feed toevoegen met letterlijke regel uit config, handmatig starten (test_US013_c5_*).
- US-015-c12: VERVALLEN (vervangen door US-016 c6 volgens BACKLOG; test_US015_c12_is_vervangen_door_US016_c6_in_backlog).
- REGRESSIE US-001 (c2, c3, c5, c6 statisch), US-002, US-004, US-007, US-009, US-010 c2-c5, US-011 c1-c4, US-012, US-015 c1-c11: OK (volledige suite, zie REGRESSIE).

SUITE: 264 tests, 263 geslaagd, 1 FAALT (test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer). Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v` (137 s). Bouwer-suite: `python -B -m unittest discover -s tests -v`: 131 OK.

REGRESSIE: NIET OK. Wat faalt: alleen US-017 c5 (dubbele link, BEVINDING 1). Verder OK: de vier falende tests van ronde 1 (US-010 c1, US-011 c5, US-017 c4 na aanpassing; veilig_check na het verwijderen van de lokale paden); US-008 c8 op 375 px (1 kolom) en 1280 px (4 naast elkaar) in browser en op schermafbeelding; de lokale app (statische site en lokale app met echte data); veilig_check exitcode 0.

VERDELING ECHTE OPHAALRONDE (1 ronde naar een tijdelijke map, 9 okt 2026, 10 feeds OK, 96 items opgeslagen; AI-plafond niet actief, want AI 31 <= 43):
- Per categorie (getoond 96): BI 34 (35,4%), Data 15 (15,6%), Automatisering 16 (16,7%), AI 31 (32,3%). AI-aandeel 32,3% (<= 40%: gehaald). BI+Data 51,0%.
- Per feed in BI (34): Microsoft Fabric 17 (50%), Power BI 12 (35%), SQLBI 2 (6%), AWS Big Data 2 (6%), Camunda 1 (3%).
- Per feed in Data (15): AWS Big Data 11 (73%, boven 60%), Microsoft Fabric 3 (20%), Power BI 1 (7%).
- Per feed in Automatisering (16): n8n 7 (44%), Camunda 5 (31%), Techzine 2 (12%), Emerce 1 (6%), AWS 1 (6%).
- Per feed in AI (31): NOS Tech 10 (32%), Camunda 7 (23%), n8n 5 (16%), Computable 4 (13%), Techzine 2 (6%), AWS 2 (6%), Emerce 1 (3%).
- Geweigerd door kwaliteitsfilter (per feed): Camunda 2, n8n 1, Emerce 1; 7 feeds 0.
- Ter vergelijking ronde 1 (8 okt, 103 items): AWS Big Data 61% van Data. Nu 73%: het feedprobleem is niet opgelost.

KWALITEIT UITGELICHT EN VAKNIEUWS (ernst; PO beslist):
Uitgelicht (5 items, peildatum 8 okt 2026):
- "Ai jaagt cyberdreigingen aan, organisaties moeten veerkrachtig worden" (Computable, AI): matig; zakelijk relevant, bronschrijfwijze "Ai" overgenomen (KLEIN).
- "Power BI September 2026 Feature Summary" (Power BI Blog, BI): goed voor Deux; Engelstalig (KLEIN, zie BEVINDING 5).
- "Microsoft introduceert hybride ai voor Windows 11: slimmer en goedkoper" (Computable, AI): matig; OS-nieuws, weinig MKB-relevantie.
- "Begin bij het einde: zo maak je agentic remediation mogelijk" (Techzine, Automatisering): slecht; het is een aankondiging van een evenement (ServiceNow World Forum, 28 oktober, Amsterdam), dus promotietekst. Zie BEVINDING 2.
- "OutSystems Agent Experience opent platform voor Claude Code en Cursor" (Techzine, Automatisering): matig; vendor-productnieuws.
Vaknieuws (5 items): "Kort: Google-detector ..." (digest, bekend open punt, KLEIN); "IT Automation Software: 6 Tools for Different IT Jobs" (n8n Blog, generiek Engels listicle, weinig Deux-waarde, KLEIN); "Kleine groepje klanten levert AI-reuzen meeste omzet" (Emerce, AI; redelijk); "Compacte en snelle Claude Haiku 5.5 vervangt eindelijk 4.5" (Techzine, productnieuws; redelijk); "Ai in het soc: humans in de lead en in de loop" (Computable; redelijk).
Oordeel: Uitgelicht is bruikbaar voor Deux (2 van 5 sterk, 2 matig, 1 promo). Vaknieuws bevat 4 van 5 AI-items: het AI-plafond geldt voor de hele lijst, maar het blok zelf is AI-zwaar (KLEIN, zie BEVINDING 4).

BEVINDINGEN:
1. BLOKKEREND, US-017 c5 (deel): dubbele geweigerde link telt dubbel in het ophaallog. Stappen: feed (RSS) met twee identieke items met dezelfde link en titel "Webinar: Power BI voor het mkb"; `python src/ophalen.py --config <tmp>/cfg.json --uitvoer <tmp>/nieuws.json`. Verwacht: "1 geweigerd (kwaliteit)". Werkelijk: "2 geweigerd (kwaliteit)". Oorzaak: in src/ophalen.py (functie draai) telt len(geweigerd) per item; de dedupe op link gebeurt pas na verwerk_items, dus voor bewaarde items wel en voor geweigerde niet. Test: test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer. Let op: in besluit 2026-10-09-fixronde1-it6 (punt 10) is dit als KLEIN geclassificeerd; volgens de ernstregels is het een deel van een acceptatiecriterium dat faalt, dus BLOKKEREND. De impact is klein (alleen het telgetal in het log).
2. BELANGRIJK, promotie in Uitgelicht: "Begin bij het einde: zo maak je agentic remediation mogelijk" (Techzine) staat op de startpagina als 4e item. Het is een vooraankondiging van een evenement. Verwacht (doel US-017 en besluit punt 2): geen evenementpromo in Uitgelicht. Werkelijk: aanwezig, want er is geen weigerpatroon dat hem vangt. Besluit PO: een patroon toevoegen, bronkeuze, of accepteren. Ik stel geen generieke term voor.
3. BELANGRIJK, meldpunt US-016 c6 niet gehaald (open punt, niet blokkerend volgens criterium): Automatisering 16,7% (doel >= 20%); AWS Big Data Blog 73% van Data (doel <= 60%; in ronde 1 nog 61%). Data bestaat voor een groot deel uit AWS-diepteartikelen (MSK, EMR, Glue, MWAA) met weinig MKB-relevantie (open punt Stef uit ronde 1). Besluit PO: feed vervangen of accepteren.
4. KLEIN, Vaknieuws: 4 van 5 items zijn AI; een digest ("Kort: ...") en een generiek Engels listicle staan erin. Besluit PO.
5. KLEIN, taal: Engelstalige titels in Uitgelicht en Vaknieuws op een Nederlandse site (bijv. "Power BI September 2026 Feature Summary", "IT Automation Software: 6 Tools ..."). Taalfilter is US-014 (COULD).
6. KLEIN, lokale app: Overzicht toont nog de tellers nieuwsitems, leads en nieuwe leads, zonder BI-tegel. Of US-016 c7 ook voor de lokale app geldt, is niet duidelijk uit BACKLOG (US-012 zegt dat de lokale app buiten de regressie valt). Bevestiging PO.
7. KLEIN, foutmelding bij een ongeldige peildatum: `python src/bouw.py --vandaag 2026-13-45` geeft "FOUT: month must be in 1..12" (Engelse Python-tekst, exitcode 1, geen traceback). Verwacht: Nederlandse melding over het datumformaat.
8. Status eerdere ronde-1-bevindingen: 1 (375 px) OPGELOST, 2 (Emerce-promo) OPGELOST (geweigerd), 3 (Camunda/n8n-PR) OPGELOST (geweigerd), 4 (NOS-categoriefout) OPGELOST (geen Data), 5 (review/game-valse positieven) OPGELOST (uitzonderingslijst), 6 (ongeldige datum) OPGELOST, 7 (alleen-AI-melding) OPGELOST, 8 (BACKLOG-tegenstrijdigheid) OPGELOST (c7 verduidelijkt), 9 (AWS-diepteartikelen, Kort-digests) OPEN (zie 3 en 4), 10 (meetlog unieke links) DEELS: bewaard-tellingen kloppen nu, geweigerd-telling niet (zie 1).

AANGEPASTE TESTS (was -> nu, waarom; geen criterium verzwakt):
1. test_US010_c1_config_heeft_trefwoorden_nl_en_per_categorie (test_US010_categorie.py): Data-eis "gegevens" -> "gegevensanalyse". Reden: los "gegevens" is geen Data-trefwoord meer (US-016 c8, besluit punt 4). De samenstelling blijft Data.
2. test_US011_c5_item_zonder_titel_overgeslagen_zonder_datum_krijgt_ophaaldatum (test_US011_foutafhandeling.py): fixture-beschrijving "Gegevens" -> "SQL" bij het item "Met datum over data". Reden: met "gegevens" los zonder categorie werd het item weggefilterd, waardoor de test de controle op het item met datum niet kon doen. Het criterium (titel leeg overslaan, datum krijgt ophaaldatum, het ophalen stopt niet) is ongewijzigd.
3. test_US017_c4_vaste_testset_klopt_voor_elke_titel (test_US017_weigerlijst.py): "Gemini, metadata and the analogy game" was te weigeren (True) -> toegelaten (False). Reden: US-017 c7 zet 'analogy game' op de uitzonderingslijst en noemt deze titel uitdrukkelijk als toegelaten.
4. test_iteratie5 (veilig_check, geen testwijziging): twee lokale-padregels in mijn eigen rapport docs/test-reports/iteratie-6-ronde-1.md verwijderd (regel 37 en 99). Nieuwe rapporten bevatten geen lokale paden.
Nieuwe tests (11): test_US016_c8_los_gegevens_is_geen_data_trefwoord, test_US016_c8_drie_nos_titels_met_echte_samenvatting_krijgen_geen_data, test_US016_c9_ongeldige_datum_wordt_overgeslagen_met_melding_bouw_gaat_door, test_US016_c10_alleen_ai_items_geeft_exitcode_1_en_melding_ai_plafond, test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer, test_US017_c6_configuratie_bevat_evenement_en_vendor_pr_patronen, test_US017_c6_evenementpromo_en_vendor_pr_worden_geweigerd, test_US017_c6_overname_productrelease_en_gartner_titel_worden_toegelaten, test_US017_c7_uitzonderingslijst_bevat_zakelijke_combinaties, test_US017_c7_vaste_testset_laat_zakelijke_combinaties_toe, test_US017_c7_review_en_games_blijven_geweigerd. De drie NOS-titels gebruiken de opgeslagen samenvattingen (ingekort tot 300 tekens, zoals in het bestand) uit de ronde van 8 okt, omdat de titels in de feed van 9 okt niet meer staan. De test is dus deterministisch.
Het overzicht in tests/acceptance/README.md is bijgewerkt (criterium -> testnaam).

BASISCHECKS (VOLLEDIG):
- Lokale app (achtergrond, PORT=8791, GEEN_BROWSER=1): /, /nieuws, /leads, /nieuws?categorie=bi, /nieuws?categorie=BI&q=power: 200; /favicon.ico 204; /nietbestaand 404; serverlog leeg. Gestopt.
- Statische site (achtergrond, lokale server): alle pagina's en assets 200; serverlog alleen 200-regels. Gestopt.
- Console-fouten: geen op index.html en nieuws.html (browsertests, Edge headless, met meetscript). Echte browser-sessie op de lokale app: niet gedaan.
- README: klopt op de punten die ik heb gecontroleerd (10 feeds, vier categorieen, AI-plafond 40%, Uitgelicht-scoreregel, weigerlijst en uitzonderingen, bouwopties, stappen online zetten A-E). Geen lokaal pad of persoonlijk account in de README.
- Foutpaden bouw: kapot JSON -> FOUT, exitcode 1, geen traceback; leeg items -> FOUT, exitcode 1; ontbrekend bestand -> FOUT met "Draai eerst: python src/ophalen.py", exitcode 1; ongeldige --vandaag -> zie BEVINDING 7.
- Ophaalronde: alle 10 feeds OK, geen FOUT, geen traceback.

UITERLIJK (headless Edge, schermafbeeldingen in de tijdelijke map, bekeken):
- Overzicht 1280 px: donkerblauwe kop, grijze achtergrond, witte kaarten, accent teal op links en actieve menu-items; Uitgelicht boven, daarna 4 tegels naast elkaar (BI, Data, Automatisering, AI), daarna Vaknieuws. Netjes.
- Overzicht 375 px (iframe): tegels onder elkaar, Uitgelicht leesbaar, navigatie in beeld, geen horizontaal scrollen. Netjes.
- Het totaalbeeld en de smaak beoordeelt Stef; ik beoordeel de techniek.
- Nieuws 375 en 1280 px: schermafbeelding niet gelukt (Edge leverde geen bestand); beoordeeld via geautomatiseerde metingen (geen horizontale overloop, navigatie in beeld, filterknoppen en kaarten, test_US016_c7_browser_* en test_US012_*). Visueel: NIET GETEST.

NIET GETEST:
- US-013 c1 en c3: live site op github.io en een run op GitHub (geen toegang).
- Echte browser-interactie: klikken, terugknop, herladen, snel klikken, toetsenbord (Tab), echt toestel, browser die zich automatisch opent.
- Visuele beoordeling van Nieuws op 375 en 1280 px (zie UITERLIJK).
- De drie NOS-hacktitels zijn in de feed van 9 okt niet meer aanwezig; de test gebruikt de opgeslagen samenvattingen uit een eerdere ronde (zie AANGEPASTE TESTS).

BENODIGD VAN BOUWER:
1. BLOKKEREND, US-017 c5: tel geweigerde items per feed unieke link (src/ophalen.py, functie draai). Daarna test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer draaien. Geen andere tests aanpassen.
2. KLEIN: ongeldige --vandaag geeft een Engelse Python-melding (src/bouw.py), met Nederlandse tekst.
3. PO-besluiten nodig: BEVINDING 2 (promo in Uitgelicht), 3 (feed-aandeel Automatisering/AWS, open punt), 4 (AI-zwaar Vaknieuws, digests), 5 (Engelse titels), 6 (lokale app: BI-tegel of niet).

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US010_categorie.py
- tests/acceptance/test_US011_foutafhandeling.py
- tests/acceptance/test_US016_mix.py
- tests/acceptance/test_US017_weigerlijst.py
- tests/acceptance/README.md
- docs/test-reports/iteratie-6-ronde-1.md (alleen twee lokale-padregels, op verzoek van de orchestrator)
- docs/test-reports/iteratie-6-ronde-2.md (nieuw)
Tijdelijke bestanden (ophaalrondes, gebouwde sites, schermafbeeldingen, Edge-profielen): alleen in de tijdelijke map van het systeem. Servers gestopt (geen processen achtergelaten).
Opmerking: data/nieuws.json en site/ zijn om 00:08-00:09 gewijzigd (door de Bouwer), vóór mijn eerste wijziging; ik heb in de projectmap niets anders geschreven.
