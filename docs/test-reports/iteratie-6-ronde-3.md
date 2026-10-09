ITERATIE: 6 | RONDE: 3 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD

Reden: geen BLOKKEREND meer open (US-017 c5 is opgelost, de falende test US-012 c6 is aangepast op het gewijzigde criterium). Wel 1 BELANGRIJK open, dat volgens de ernstregels de test NIET GESLAAGD maakt: het meldpunt US-016 c6 (feedverdeling) en de inhoud van Uitgelicht/Vaknieuws (zie BEVINDINGEN 1 en 2). Die oplossing ligt bij de PO en Stef (feedkeuze), niet bij de Bouwer met generieke trefwoorden.

PER CRITERIUM:
- US-016-c1: OK. Vier categorieen, >= 15 trefwoorden, verplichte termen (test_US016_c1_*).
- US-016-c2: OK. Gelijkspel BI/AI -> BI (test_US016_c2_*).
- US-016-c3: OK. AI alleen in samenvatting telt niet (test_US016_c3_*).
- US-016-c4: OK. Fixture 80 AI + 20 overig -> 13 AI; echte ronde AI 31 van 96 = 32,3% (test_US016_c4_*).
- US-016-c5: OK. 10 feeds, 4 NL, 6 EN; 3 BI-feeds; elke feed in feedbesluit en op bronnenlijst (test_US016_c5_*).
- US-016-c6: NIET GESLAAGD (meldpunt, BELANGRIJK open). Echte ronde 9 okt (96 items, 10 feeds OK): BI+Data 51,0% (doel >= 30%: gehaald); Automatisering 16,7% (doel >= 20%: niet gehaald); AWS Big Data Blog 73% van Data (doel <= 60%: niet gehaald). Zie BEVINDING 1.
- US-016-c7: OK. Filterknoppen en tegels; categorie=bi; 375 en 1280 px zonder horizontaal scrollen (browsertests test_US016_c7_browser_*). Visueel 375 px: zie NIET GETEST.
- US-016-c8: OK. "gegevens" los geen Data; drie NOS-titels geen Data (test_US016_c8_*).
- US-016-c9: OK. Ongeldige datum "garbage": waarschuwing met titel, bouw exitcode 0 (test_US016_c9_*).
- US-016-c10: OK. Alleen AI: exitcode 1, melding over het AI-plafond (test_US016_c10_*).
- US-016-c11: OK. `python src/bouw.py --vandaag 2026-13-45`: "FOUT: ongeldige peildatum '2026-13-45' bij --vandaag; gebruik het formaat JJJJ-MM-DD (bijvoorbeeld 2026-10-09)", exitcode 1, geen traceback. Ook 2026-02-30 zelfde melding. Geldige datum bouwt exitcode 0 (test_US016_c11_* en handmatig).
- US-017-c1: OK. Weigerlijst en promotietermen compleet (test_US017_c1_*).
- US-017-c2: OK (test_US017_c2_*).
- US-017-c3: OK (test_US017_c3_*).
- US-017-c4: OK. Vaste testset 12 titels (test_US017_c4_*).
- US-017-c5: OK (BLOKKEREND uit ronde 2 is opgelost). Dubbele geweigerde link telt 1 (test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer, geslaagd). Echte ronde per feed geweigerd: Camunda 2 (twee verschillende titels, met voorbeelden), n8n 1, Emerce 1; overige 7 feeds 0.
- US-017-c6: OK (test_US017_c6_*).
- US-017-c7: OK (test_US017_c7_*).
- US-018-c1: OK. 4 algemene NL-headnieuws-feeds (Computable, Emerce, Techzine, NOS Tech); deux_relevantie compleet (test_US018_c1_*).
- US-018-c2: OK. Uitgelicht boven de tellers, max 5, laatste 3 dagen, hooguit 2 AI; echte ronde: 5 items, 2 AI.
- US-018-c3: OK. Scoreregel in README, vaste volgorde (test_US018_c3_*).
- US-018-c4: OK (test_US018_c4_*).
- US-018-c5: OK (test_US018_c5_*; ook test_US012_c6_* aangepast, zie hieronder).
- US-018-c6: OK (browser 375/1280 px, test_US018_c6_*). Visueel: zie NIET GETEST.
- US-018-c7: OK. Fixture: evenementaankondiging ("Begin bij het einde..." met "World Forum"/"Meld je aan" in de samenvatting) niet in Uitgelicht/Vaknieuws, wel op Nieuws; gewoon nieuws ("Nederlandse gemeenten kiezen Power BI...") blijft in Uitgelicht; "Eventueel" geen vals-positief (test_US018_c7_*). Echte data: de echte Techzine-titel stond in de projectdata en is getest (niet geskipt): niet in Uitgelicht/Vaknieuws, wel op Nieuws; ook in de schone ronde-build zo (test_US018_c7_echte_techzine_titel_*).
- US-018-c8: OK. Fixture 6 AI + 1 "Kort:"-titel + 10 niet-AI: Uitgelicht = AI A, AI B; Vaknieuws = AI C, AI D, Overig-0, -1, -2 (exacte volgorde, test_US018_c8_*). "Kort:"-titel niet in blokken, wel op Nieuws. Echte ronde: Vaknieuws 2 AI, "Kort:"-digest uitgesloten.
- US-012-c6 (vaknieuws, US-018 c5/c8): OK na aanpassing van de test (zie AANGEPASTE TESTS). Vaknieuws = nieuwste getoonde items, hooguit 2 AI, weggelaten nieuwere items alleen met reden (AI-max, "Kort:" of evenement); positief en negatief getoetst.
- US-013-c1 en c3: NIET GETEST (vereist live site op github.io en een run op GitHub; geen toegang).
- US-013-c2/c4/c5, US-001, US-002, US-004, US-007, US-008, US-009 t/m US-012, US-015: regressie OK (zie REGRESSIE).

SUITE: 279 tests, 279 geslaagd, 0 geskipt. Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v` (140 s). Bouwer-suite: `python -B -m unittest discover -s tests -v`: 137 OK. Baseline aan het begin van deze ronde: 264 tests (1 FAALT, US-012 c6). Nu 279: 15 nieuw (10 US-018 c7/c8, 3 US-016 c11, en de positief/negatief-test van US-012 c6 die in 2 klassen draait); de c6-test zelf is aangepast.

REGRESSIE: OK voor de geautomatiseerde suite (279/279, beide suites, 375 en 1280 px in headless Edge, statische site, echte data alleen-lezen, fixtures). Lokale app valt volgens PO-besluit buiten de regressie; toch meegedraaid, geslaagd. `python src/veilig_check.py`: exitcode 0. Let op: de regressie is NIET GESLAAGD door de open BELANGRIJK-bevindingen hieronder, niet door tests.

VERDELING ECHTE OPHAALRONDE (schone ronde: nieuwe lege tijdelijke map <tmp>, 9 okt 2026, 10 feeds OK, 96 items opgeslagen; AI-plafond niet actief, AI 31 <= 43):
- Per categorie (getoond 96): BI 34 (35,4%), Data 15 (15,6%), Automatisering 16 (16,7%), AI 31 (32,3%). BI+Data 51,0%.
- Per feed in BI (34): Microsoft Fabric Blog 17 (50%), Power BI Blog 12 (35%), SQLBI 2, AWS Big Data 2, Camunda 1.
- Per feed in Data (15): AWS Big Data Blog 11 (73%, boven 60%), Microsoft Fabric 3 (20%), Power BI 1.
- Per feed in Automatisering (16): n8n 7 (44%), Camunda 5 (31%), Techzine 2, Emerce 1, AWS 1.
- Per feed in AI (31): NOS Tech 10 (32%), Camunda 7, n8n 5, Computable 4, Techzine 2, AWS 2, Emerce 1.
- Geweigerd door kwaliteitsfilter: Camunda 2, n8n 1, Emerce 1.
- Vergelijking ronde 2 (9 okt, 96 items): dezelfde cijfers. Het feedprobleem is niet opgelost.
- Noot: een eerste ophaalpoging naar een bestaande testmap gaf een uitvoer met items van vier feeds die niet meer in de config staan (bewaard volgens het 60-dagenbeleid). Die uitvoer is niet gebruikt; alle cijfers hierboven komen uit de schone run. Fabric Blog gaf in die eerste poging een time-out (15 s), in de schone run OK.

KWALITEIT UITGELICHT EN VAKNIEUWS (peildatum 9 okt 2026, ernst; PO beslist):
Uitgelicht (5):
- "Ai jaagt cyberdreigingen aan, organisaties moeten veerkrachtig worden" (Computable, AI): matig, zakelijk relevant.
- "Power BI September 2026 Feature Summary" (Power BI Blog, BI): goed voor Deux, maar Engelstalig (KLEIN, US-014).
- "Microsoft introduceert hybride ai voor Windows 11: slimmer en goedkoper" (Computable, AI): matig, OS-nieuws.
- "OutSystems Agent Experience opent platform voor Claude Code en Cursor" (Techzine, Automatisering): matig, vendor-productnieuws.
- "Planning in Microsoft Fabric: From insight to action" (Fabric Blog, BI): matig, Engelstalige productblog.
Vaknieuws (5):
- "IT Automation Software: 6 Tools for Different IT Jobs" (n8n Blog): generiek Engels listicle, weinig Deux-waarde (KLEIN, bekend).
- "Kleine groepje klanten levert AI-reuzen meeste omzet" (Emerce, AI): redelijk.
- "Compacte en snelle Claude Haiku 5.5 vervangt eindelijk 4.5" (Techzine, AI): productnieuws, redelijk.
- "Fabric September 2026 Feature Summary" (Fabric Blog, BI): Engelstalige productrelease (KLEIN).
- "AI helpt verpleegkundigen wonden sneller vast te leggen bij LUMC" (Emerce): titel is AI, categorie Automatisering (KLEIN; volgt de treffer-regel, PO beoordeelt).
Oordeel: Uitgelicht en Vaknieuws zijn bruikbaar, maar 4 van de 10 blokitems zijn Engelstalig en 5 van de 10 zijn vendor-productnieuws (Fabric, Power BI, OutSystems, Claude-release). Dat past slecht bij het doel "nuttige info voor Deux (MKB/ZZP)". Zie BEVINDING 2.

BEVINDINGEN:
1. BELANGRIJK (open, PO beslist; feedkeuze voor Stef): US-016 c6 meldpunt niet gehaald. Automatisering 16,7% (doel >= 20%), AWS Big Data Blog 73% van Data (doel <= 60%). Reproduceer: schone ophaalronde naar een lege tijdelijke map, daarna `python src/bouw.py --data <tmp>/nieuws.json --uit <tmp>/site`; zie de verdeling. Verwacht: Automatisering >= 20%, geen feed > 60% van een categorie. Werkelijk: 16,7% en 73%. Dit is een criterium dat de PO als meldpunt en open punt heeft gemarkeerd; ik tel het mee als BELANGRIJK zodat het zichtbaar blijft en niet stilzwijgend verdwijnt. De Bouwer kan dit niet oplossen met generieke trefwoorden (criterium verbiedt het).
2. BELANGRIJK (open, PO beslist): Uitgelicht/Vaknieuws bevat veel Engelstalig vendor-productnieuws en een generiek listicle (zie kwaliteit hierboven: 4/10 EN, 5/10 productnieuws). Reproduceer: bouw de schone ronde en lees index.html. Verwacht (doel van Stef): nuttig nieuws voor MKB/ZZP, Nederlands waar mogelijk. Werkelijk: zie boven. Oorzaak deels de feedkeuze (Fabric Blog levert 50% van BI).
3. KLEIN: categorie van "AI helpt verpleegkundigen ... LUMC" is Automatisering terwijl de titel over AI gaat (Emerce). Volgt de treffer-regel; PO beoordeelt of de weging moet veranderen.
4. KLEIN: ophalen bij een ontbrekend --config-bestand geeft "FOUT: configuratiebestand niet te lezen ... (No such file or directory)"; de tekst achter de dubbele punt is Engels (exitcode 2 klopt met README).
5. KLEIN: Fabric Blog gaf in een eerste poging een time-out (15 s); in de schone run OK. Geen actie, US-011 vangt dit op; wel meewegen bij de feedkeuze.
6. KLEIN: Engelse samenvattingen op de site (bijv. Fabric-blog "If you haven't already, check out FabCon...") en Engelse titels op een Nederlandse site (US-014, COULD).
7. Verkennend (klein): `--vandaag 2026-02-30` geeft dezelfde Nederlandse melding; `--vandaag` met geldige datum bouwt. Geen traceback gezien.

AANGEPASTE TESTS (was -> nu, waarom; geen criterium verzwakt):
1. test_US012_c6_startpagina_toont_vijf_nieuwste_items (test_US012_statische_site.py): was: elk weggelaten item moet ouder zijn dan het oudste getoonde, en het aantal is min(5, rest). Nu: het aantal volgt "max 5, max 2 AI" (verwacht_vaknieuws_aantal); hooguit 2 AI getoond; een weggelaten nieuwer item moet een geldige reden hebben: AI terwijl er al 2 AI getoond worden, titel begint met "Kort:", of een evenementterm (mag_weggelaten). Reden: US-018 c8 en c7 (besluit 2026-10-09-fixronde2-it6.md). De aangepaste test faalde in de baseline (1 FAALT, op de echte data).
2. Nieuwe test test_US012_c6_weggelaten_nieuwere_items_uitzonderingen_positief_en_negatief: positief (AI boven max, "Kort:", evenement "world forum"/"aanmelden") en negatief (gewoon Data-item, 1 AI getoond, "Kortom:", "Congresbezoekers" geen uitzondering). Geslaagd.

NIEUWE TESTBESTANDEN: tests/acceptance/test_US018_c7_c8_evenement_kort_ai.py (10 tests), tests/acceptance/test_US016_c11_peildatum.py (3 tests). tests/acceptance/README.md bijgewerkt (criterium -> testnaam, en de wijzigingslijst).

BASISCHECKS (VOLLEDIG):
- Geen servers gestart door mij; de suite start zijn eigen servers in-process en stopt die. Browser-processen met mijn tijdelijke profielen gestopt; nul achtergebleven.
- Console-fouten: niet opnieuw gemeten in deze ronde (in ronde 2 geen fouten op index.html en nieuws.html; de browsertests van US-018 c6 zijn geslaagd).
- README: de beschreven zaken (tien feeds, vier categorieen, AI-plafond 40%, scoreregel, weigerlijst, bouwopties, --vandaag-formaat) kloppen met de code en met de testuitvoer. Het foutbericht van --config wijkt af van "nette foutmelding" door het Engelse OS-deel (KLEIN 4).
- Geen lokale paden in dit rapport (tijdelijke mappen als <tmp>).

UITERLIJK:
- Overzicht 1280 px (headless Edge, screenshot in tijdelijke map, bekeken): donkerblauwe kop, grijze achtergrond, witte kaarten, teal accent op links en actief menu. Uitgelicht boven, daarna 4 tellers naast elkaar, daarna Vaknieuws. Netjes.
- Overzicht 375 px: een screenshot is niet bruikbaar gebleken: Edge gaf een venster dat breder is dan 375 px, de pagina is afgekapt (Nieuws-link niet zichtbaar). Ik beoordeel 375 px dus NIET visueel. Dat laat de automatische browsermeting (geen horizontale overloop, US-016 c7/US-018 c6) wel zien.
- Nieuws 375/1280 px: visueel NIET GETEST in deze ronde.
- Totaalbeeld en smaak beoordeelt Stef.

NIET GETEST:
- US-013 c1 en c3: live site op github.io en een run op GitHub (geen toegang).
- Visueel 375 px (Overzicht en Nieuws): NIET GETEST, de screenshotmethode gaf geen bruikbaar beeld (zie UITERLIJK).
- Echte browser-interactie (klikken, terugknop, herladen, snel klikken, toetsenbord): niet in deze ronde gedaan.
- Console-fouten: niet opnieuw gemeten in deze ronde.

BENODIGD VAN BOUWER:
1. KLEIN: ophalen-foutmelding voor een ontbrekend --config-bestand in het Nederlands (BEVINDING 4).
2. Geen BLOKKEREND-werk meer. De twee BELANGRIJK-bevindingen (feedverdeling, inhoud) zijn PO/Stef-besluiten: feed vervangen of extra Automatisering-bron (zie open punt A in besluit 2026-10-09-fixronde2-it6.md) en beslissing over Engelstalig/productnieuws (open punt C).
3. Orchestrator: fixronde 3 is de laatste toegestane (max 3). Bij blijvend NIET GESLAAGD is noodrem vereist; de feedkeuze is een Stef-besluit en kan niet door een fix in de code worden opgelost.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US012_statische_site.py (test_US012_c6_startpagina_toont_vijf_nieuwste_items aangepast; nieuwe test test_US012_c6_weggelaten_nieuwere_items_uitzonderingen_positief_en_negatief)
- tests/acceptance/test_US018_c7_c8_evenement_kort_ai.py (nieuw)
- tests/acceptance/test_US016_c11_peildatum.py (nieuw)
- tests/acceptance/README.md (overzicht en wijzigingslijst bijgewerkt)
- docs/test-reports/iteratie-6-ronde-3.md (nieuw, dit rapport)
Tijdelijke bestanden (ophaalrondes, gebouwde sites, screenshots, Edge-profielen): alleen in de tijdelijke map van het systeem.
