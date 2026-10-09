ITERATIE: 8 | RONDE: 2 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD (BLOKKEREND: dataverlies bij een foutieve trefwoordenconfig, bevinding 1)

PER CRITERIUM:
- US-020-c1: NIET GETEST (deel). Bestanden app.py en data.py weg; geen leadwoord of leadstatus in src/, config/, README.md (test_US020_c1_* OK). Verzonnen bedrijfsnamen: NIET TESTBAAR, de lijst bestaat nergens meer (zie bevinding 6).
- US-020-c2: OK via suite (test_US020_c2_*): src/ bevat bouw.py, mix.py, ophalen.py, veilig_check.py; geen http.server of verwijderde module.
- US-020-c3: OK via suite (test_US020_c3_*). Echte ophaalronde: 10 van 10 feeds OK, exitcode 0 (zie REGRESSIE).
- US-020-c4: OK via suite (test_US020_c4_*): README zonder startinstructie lokale app.
- US-022-c1: OK via suite (test_US022_c1_fixture_* en test_US022_c1_echte_data_*): geen totaal in de kop van Vaknieuws, link "Alle <n> berichten bekijken".
- US-022-c2: OK voor de gevraagde gevallen: ontbrekend bestand, geen JSON, geen tekst (UTF-8), map; plus de ronde-1-bevindingen 1 en 2 (zie hieronder) en feeds als object, leeg object, user_agent ontbreekt (alle exitcode 2, Nederlands, geen traceback, geen uitvoerbestand). Lege of verkeerd gespelde trefwoorden worden NIET geweigerd (bevinding 1).
- US-013-c1 en c3: NIET GETEST (live site en GitHub-run; geen toegang).
- US-001 t/m US-021 (regressie): OK in de suite, zie REGRESSIE.

RONDE-1-BEVINDINGEN:
- 1 (feed-item als tekst, traceback, exit 1): OPGELOST. Nu exitcode 2 met "FOUT: ongeldig configuratiebestand ...: feed 1 is geen object", geen traceback. Test: test_US022_c2_extra_feed_item_dat_geen_object_is_geeft_geen_traceback (OK).
- 2 (feed zonder url): OPGELOST. Nu exitcode 2 met "feed \"A\" mist url (tekst)". Nieuwe test: test_US022_c2_extra_feed_zonder_url_nederlandse_melding_exitcode_2 (OK).
- 3 (bedrijfsnamen-controle US-020 c1): OPEN, besluit PO/Stef, zie hieronder.
- 4 (src/__pycache__ aanwezig): OPGELOST. Geen __pycache__ meer in src/ of tests/.
- 5 (Uitgelicht met vendor-productitem, Engelse titels in Vaknieuws): ongewijzigd, bekend KLEIN.
- 6 (oude python-processen op poort 8000 en 8080): NOG OPEN, zie hieronder.

SUITE: 270 tests, 265 geslaagd, 0 gefaald, 5 geskipt (vervallen lokale-app-tests, met reden). Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v` (met PYTHONDONTWRITEBYTECODE=1). Bouwer-suite: `python -B -m unittest discover -s tests -v`: 118 geslaagd, 0 gefaald.

REGRESSIE: NIET GESLAAGD door bevinding 1 (BLOKKEREND). Overig OK:
- Statische site op 375 px (iframe) en 1280 px: via de browsertests in de suite (headless Edge: test_US012_browser, test_US001_c6, test_US008_c8, test_US012_c8 e.a.), alle OK. Ik heb geen eigen screenshots gemaakt in deze ronde; het totaalbeeld is aan Stef.
- `python src/veilig_check.py`: exitcode 0 (92 bestanden, geen geheimen, geen lokale paden).
- Geen __pycache__ in src/ of tests/ na alle runs.
- Echte ophaalronde (eenmalig, met robots.txt-controle, naar een tijdelijke map, geen bestaande data): 10 van 10 feeds OK, exitcode 0, 86 items bewaard.
  Per feed (bewaard, geweigerd): Power BI Blog (Microsoft) 13 | Microsoft Fabric Blog 20 | SQLBI 2 | Microsoft Power Platform Blog 6 | Camunda Blog 13 (2 geweigerd) | n8n Blog 12 (1 geweigerd) | Computable 4 | Emerce 2 | Techzine 4 | NOS Tech 10.
  Per categorie na bouwen (86 items): BI 32 (37,2%), Data 5 (5,8%), Automatisering 16 (18,6%), AI 33 (38,4%; het AI-plafond van 40% is niet aan de orde).
  Per feed binnen categorie: BI: Fabric 17 van 32 (53%), Power BI 12, SQLBI 2, Camunda 1. Data: Fabric 3 van 5 (60%, niet boven 60%), Power BI 1, Power Platform 1. Automatisering: n8n 7 van 16 (44%), Power Platform 4, Camunda 5. AI: NOS Tech 10, Computable 4, Techzine 4, n8n 5, Camunda 7, Emerce 2, Power Platform 1.
  Meetpunten US-016 c6 / US-019 c4 (melden, niet hard getoetst): BI+Data 43,0% (>= 30%) OK; Automatisering 18,6% (< 20%) NIET gehaald, bekend open punt; geen feed boven 60% van een categorie OK.
  Geweigerde titels (ter info): "Camunda Named a Leader in The Forrester Wave: ...", "Camunda Recognized as a Visionary in Gartner BOAT Magic Quadrant 2026", "You can now top up your n8n Assistant credits".

BEVINDINGEN:
1. BLOKKEREND (dataverlies, nieuw in ronde 2). Een config die volgens controleer_config geldig is, maar met lege of verkeerd gespelde trefwoorden, wist alle opgeslagen nieuws zodra er een feed lukt.
   Reproduceren: (a) kopieer data/nieuws.json (87 items) naar een tijdelijke map; (b) maak een config met de echte inhoud van config/feeds.json, maar met `"trefwoorden": {}` en als `feeds` een bereikbare feed (of met de categoriesleutel "Ai" i.p.v. "AI"); (c) `python src/ophalen.py --config <config> --uitvoer <kopie> --geen-robots`.
   Verwacht: nette Nederlandse melding met exitcode 2, of op zijn minst het bestand intact.
   Werkelijk: exitcode 0; bij lege trefwoorden 87 -> 0 items; bij de typo "Ai" 87 -> 2 items. Bij alle feeds mislukt: bestand ongewijzigd (goed).
   Oorzaak: draai() categoriseert opgeslagen items opnieuw en verwijdert items zonder categorie. controleer_config controleert alleen dat trefwoorden een object is met lijsten van tekst; niet dat BI, Data, Automatisering en AI aanwezig en niet leeg zijn.
   Impact: de dagelijkse job commit data/nieuws.json. Eén spelfout in config/feeds.json maakt de publieke site bij de eerstvolgende run vrijwel leeg.
   Voorstel Bouwer: (a) controleer dat de vier categorieen aanwezig en niet leeg zijn, exitcode 2 met Nederlandse melding; (b) schrijf niets weg als de indeling bijna alle opgeslagen items zou verwijderen, met melding en exitcode 1 (drempel te bepalen door de PO). Er is nog geen automatische test: dit is geen geschreven criterium. PO bepaalt of het er een wordt (bijvoorbeeld uitbreiding van US-022 c2).
2. KLEIN. Een config als UTF-8 met BOM (bijv. opgeslagen met Kladblok) geeft "geen geldige JSON" (exitcode 2, geen traceback), terwijl de JSON geldig is. Lezen met encoding utf-8-sig zou dit oplossen.
3. KLEIN. uitsluitingen, weigertermen en weiger_uitzonderingen als tekst i.p.v. lijst worden stil geaccepteerd (exitcode 0, geen melding; het effect is niet onderzocht). Een lege trefwoordterm "" wordt zonder melding geaccepteerd.
4. KLEIN. Een feed-url met file:/// wordt door urllib als lokaal bestand gelezen (de fout was "ongeldige XML", exitcode 1). De config is van de repo, maar alleen http(s) is verwacht.
5. KLEIN. `"feeds": []` geeft "Alle feeds mislukt: ... blijft ongewijzigd" (exitcode 1). De melding is misleidend: er zijn geen feeds ingesteld.
6. OPERATIONEEL (zelfde als ronde 1, nog niet opgelost). Twee python-processen draaien nog: PID 34772 (127.0.0.1:8000) en PID 43088 (0.0.0.0:8080). Niet door mij gestart; niet gestopt. Stef of orchestrator controleert ze. Mijn eigen testserver (poort 8765) is gestopt; er draait niets meer van mij.
7. Verkennend: lege, rare en ontbrekende configs zijn hierboven nagelopen (zie bevindingen 1-5 en US-022 c2). Snel klikken, terugnavigeren en herladen in een echte browser: NIET GETEST.
8. Correctie op ronde 1 (bevinding 3): `git ls-tree -r 66e4d21` telt 0 bestanden, maar `git show --stat 66e4d21` toont een regel voor README.md (28 bytes). Beide zeggen dat er geen src/data.py in die commit zit. `git log --all -S "Niet interessant"` vindt geen enkele commit met leadstatus. De lijst met bedrijfsnamen staat dus niet in de git-historie.

NIET GETEST:
- US-020-c1 verzonnen bedrijfsnamen: de lijst bestaat niet meer in de projectmap of in git (bevinding 3 ronde 1 en 8 hierboven). Besluit PO/Stef nodig.
- US-013 c1 en c3: live site en GitHub-run (geen toegang).
- Interactie in een echte browser (klikken, toetsenbord, terugknop, herladen, snel klikken): niet in deze ronde.
- Visueel totaalbeeld 375 en 1280 px: alleen via de automatische browsertests; smaak en totaalbeeld aan Stef.
- Inhoudelijke beoordeling van de Uitgelicht- en Vaknieuws-selectie uit de echte ronde: niet beoordeeld.
- Verse checkout (kloon): niet opnieuw gedaan; US-020 c3 is via de suite gedekt.

BENODIGD VAN BOUWER:
- BLOKKEREND (bevinding 1): validatie van de vier trefwoordcategorieen (aanwezig, niet leeg) en een vangnet tegen het wissen van opgeslagen items. Daarna opnieuw SNEL, plus de regressie.
- KLEIN (bevindingen 2-5): BOM, niet-gevalideerde velden, file://-url, melding bij lege feeds.
- BESLUIT PO (en Stef): US-020 c1 bedrijfsnamen-controle. Die lijst bestaat nergens meer en stond ook nooit in git. Vervalt dit deel, of levert Stef de lijst opnieuw aan? Zonder besluit blijft c1 deels NIET GETEST.
- Stef of orchestrator: bevinding 6, de processen op poort 8000 en 8080 stoppen als ze van jullie zijn.
- Stef: US-013 c1 en c3 blijven open tot na publicatie.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US022_afwerking.py (2 nieuwe tests: feed zonder url; feeds als object, leeg object en user_agent ontbreekt)
- tests/acceptance/README.md (2 regels in de tabel van iteratie 8)
- docs/test-reports/iteratie-8-ronde-2.md (dit rapport)
Tijdelijke bestanden (configs, kopieen van de data, testfeed, ophaalresultaat en site): alleen in de tijdelijke map van het systeem, buiten de projectmap.
