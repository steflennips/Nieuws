ITERATIE: 4 | RONDE: 2 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD (alle geautomatiseerde criteria groen; open BELANGRIJK 1 en 2, zie BEVINDINGEN)
PER CRITERIUM:
- US-015-c1 (uitsluitingen, "Data Master"): OK. Config bevat "Data Master", "RTX Spark", "Nvidia Spark" en data center*-varianten (test_US015_c1_*). Aangepast: zie WIJZIGINGEN 3.
- US-015-c2 (Asustor-voorbeeld niet Data): OK (test_US015_c2_*).
- US-015-c3 (min. 15 trefwoorden per categorie, NL en EN): OK (test_US015_c3_*).
- US-015-c4 (vaste testset min. 20, min. 5 per categorie, min. 3 echt): OK, 26 titels ongewijzigd, alle goed (test_US015_c4_*).
- US-015-c5 (aantallen per categorie na echte ronde, geen minimum): informatief. Eigen ronde (84 opgeslagen): AI 68 (81%), Automatisering 12 (14%), Data 4 (5%). data/nieuws.json (95 items): AI 79, Automatisering 12, Data 4. Oordeel: zie BEVINDING 1.
- US-015-c6 (echte titels niet in de genoemde categorie): OK. Vier titels plus Manage Amazon SageMaker HyperPod Spaces (AI, niet Data) groen (TestUS015Fixronde, 3 tests). Samenvattingen: Tweakers en Colt uit de live feed op 8 okt 2026 (platte tekst zoals ophalen.py opslaat; Colt-tekst "Azië" zonder het ontbrekende teken); Uber en SageMaker letterlijk uit data/nieuws.json. De vier titels staan niet meer in data/nieuws.json.
- US-015-c7 (extra automatisering-feed in config, bronnenlijst, feedbesluit): OK. n8n Blog (https://blog.n8n.io/rss/, taal en) staat in config/feeds.json (10 feeds: NL 4, EN 6), in docs/decisions/2026-10-08-nieuwsfeeds.md en op bronnen.html (naam en https://blog.n8n.io/). Test: test_US015_c7_feeds.py (4 tests). Feed-URL zelf niet op bronnen.html; dat is het bronnenlijst-formaat (homepage-link).
- US-015-c8 (Automatisering min. 8 items en filter niet leeg, na echte ronde): OK voor deze ronde, handmatig (niet automatisch). Ophaalronde naar tijdelijke map: 84 items, Automatisering 12, filter niet leeg. Let op: 9 van de 12 komen van n8n Blog (zie BEVINDING 3). Live feeds zijn niet deterministisch; daarom geen automatische test.
- US-012-c1 t/m c7 (statische site, zie ronde 1): OK. Alle tests groen, inclusief browsertests (Edge) op de gebouwde site met echte data.
- US-012-c8 (placeholder 375 px volledig zichtbaar): OK. Automatisch (test_US012_c8_placeholder.py, Edge, iframe 375 px, canvas-meting): placeholder "Zoek in nieuws" 105 px tekst in 209 px beschikbaar, geen overloop. Controle van de meting: bij 150 px faalt dezelfde meting correct. Screenshot 375 px (zie hieronder): placeholder volledig zichtbaar.
- US-013-c2 en c4 (workflow, geen geheimen): OK (ongewijzigd, ronde 1; suite groen).
- US-013-c5 (README: feeds beheren, letterlijke voorbeeldregel, handmatig starten): OK. De voorbeeldregel uit README.md is geldige JSON en komt exact overeen met de n8n-feed in config/feeds.json (test_US013_c5_readme.py, 2 tests). Beschrijving toevoegen/verwijderen en "Run workflow" aanwezig.
- US-013-c1 en c3 (live site): NIET GETEST, wacht op hosting-account van Stef.
- US-009-c1 (8-10 feeds, min. 3 NL en 3 EN): OK, 10 feeds (NL 4, EN 6).
- US-011 (foutafhandeling): OK (suite groen). Live ophaalronde: KDnuggets gaf eenmalig HTTP 403 (FOUT met reden, overige 8 OK), zie BEVINDING 4.
- US-010-c1 t/m c5: OK. c2 en c3 aangepast aan het besluit (zie WIJZIGINGEN 1 en 2), c4 en c5 ongewijzigd groen.
- KLEIN 4 (README voorbeeldregel): OK (US-013-c5 hierboven).
- KLEIN 5 (placeholder 375 px): OK (US-012-c8 hierboven).
- KLEIN 6 (eigen 404.html): OK in de gebouwde map. Automatisch aanvullend (test_US012_extra_404.py, 2 tests): Nederlands, eigen tekst, links naar Overzicht en Nieuws, geen externe bestanden. Het gedrag van GitHub Pages op de live site is NIET GETEST.
SUITE: 170 tests, 170 geslaagd, 0 overgeslagen. Commando: python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v (158 bestaande na wijziging + 12 nieuw). Bouwer-tests: python -B -m unittest discover -s tests -p "test_*.py": 81 OK.
REGRESSIE: OK. Alle 158 tests van ronde 1 groen (drie aangepast, zie WIJZIGINGEN). Browsertests op 375 px (iframe) en 1280 px draaiden in Edge, niet overgeslagen. Geen regressie in US-001 t/m US-011.
BEVINDINGEN:
1. BELANGRIJK (US-015, doel "Automatisering zinvol gevuld" en "filteren echt helpt"; oordeel Tester, PO beslist): het Data-filter is praktisch leeg: 4 van 84 items in deze ronde (5%), 4 van 95 in data/nieuws.json. AI blijft 81-83%. c5 heeft geen minimum, dus geen criterium faalt, maar het doel "Data" is met de huidige feeds en trefwoorden niet gehaald.
   - Stappen: python src/ophalen.py --uitvoer <tijdelijke map>/nieuws.json, dan categorieen tellen.
   - Verwacht: de drie categorieen zijn bruikbaar voor filteren (doel US-015).
   - Werkelijk: Data 4, Automatisering 12, AI 68 van 84.
   - Oorzaak (vermoeden): losse "data" is vervallen zonder dat de specifieke Data-termen in deze feedmix vaak voorkomen; de feeds zijn AI-zwaar (MIT, AWS ML, InfoQ AI). Het besluit verbiedt het verruimen van trefwoorden om c8 te halen; de PO moet kiezen tussen accepteren met open punt, of een andere feedkeuze.
2. BELANGRIJK (categorie, echte titel in verkeerde categorie; zelfde soort fout als ronde 1 BELANGRIJK 1):
   - Titel: "New Archestra's OpenAPPA Saturates Two Major Security Benchmarks with a 0% Attack Success Rate" (InfoQ AI, ML & Data Engineering), staat in data/nieuws.json en in mijn ronde.
   - Stappen: categoriseer(titel, samenvatting) met de echte samenvatting; de samenvatting bevat "20 multi-step enterprise workflows".
   - Verwacht: niet Automatisering (het is een AI-beveiligingsonderwerp).
   - Werkelijk: Automatisering, door het generieke trefwoord "workflow*" in de samenvatting.
   - Benodigd: Bouwer en PO moeten bepalen hoe generieke woorden als "workflow*" worden behandeld.
3. KLEIN (Automatisering afhankelijk van een bron): in mijn ronde komen 9 van de 12 Automatisering-items van n8n Blog. c8 is gehaald, maar het filter hangt sterk aan een enkele feed. Ter informatie voor de PO.
4. KLEIN (bronstabiliteit): KDnuggets gaf in de ophaalronde HTTP 403 (FOUT met reden; overige 8 feeds OK; US-011 werkt zoals bedoeld). Direct daarna gaf dezelfde URL met dezelfde User-Agent HTTP 200. Vraagt aandacht bij volgende rondes, geen fout in de app.
5. INFO (verkennend, beperkt tot de fixronde-punten): lege en rare zoekinvoer en het filter zijn niet opnieuw uitgebreid verkend in deze ronde; de suite dekt de eerdere verkenning (ronde 1). Consolefouten: niet apart gecontroleerd in deze ronde (de browsertests van de suite zijn groen; ronde 1 vond geen consolefouten). Het gedrag van de statische site op de live URL is niet getest.
6. INFO (uiterlijk, screenshot): Nieuws op 375 px in headless Edge: koptekst en navigatie in beeld, zoekveld met "Zoek in nieuws" volledig zichtbaar, chips en kaarten onder elkaar, teal accent op links, knoppen en de actieve chip. Oordeel Tester: passend bij "Stijl en uitstraling"; het totaalbeeld beoordeelt Stef.
WIJZIGINGEN AAN TESTS (criterium gewijzigd door het besluit 2026-10-08; niets verzwakt, verwachte categorieen gelijk):
1. test_US010_c2: "DATA-opslag" is "DATABASE-opslag" (verwacht Data).
2. test_US010_c3: "data data data AI" is "database database database AI" (verwacht Data). De gelijkspelregels Automatisering/Data gebruiken nu "databases" en "database"; met het losse "data" zou het gelijkspel stil zijn weggevallen.
3. test_US015_c1: "data" in de samenvatting is "database" (verwacht Data).
Nieuw: test_US012_c8_placeholder.py, test_US013_c5_readme.py, test_US015_c7_feeds.py, test_US012_extra_404.py, en in test_US015_categorie.py de klasse TestUS015Fixronde (US-015 c6). README.md van de suite bijgewerkt.
BENODIGD VAN BOUWER: geen installatie nodig. Voor de volgende fixronde: BELANGRIJK 2 (generiek trefwoord "workflow*" geeft een AI-beveiligingstitel de categorie Automatisering; een gerichte oplossing volgens het besluit). BELANGRIJK 1 is een PO-beslissing (accepteren of verdere feedkeuze).
NIET GETEST: US-013 c1 en c3 (live site, hosting-account); het gedrag van GitHub Pages met site/404.html op de live site; US-015 c8 als automatische test (live feeds); snel klikken, terugknop, herladen, toetsenbordnavigatie, echt toestel, grotere datasets dan 84 items (zoals in ronde 1).
BESTANDEN GEWIJZIGD DOOR MIJ: tests/acceptance/test_US010_categorie.py (gewijzigd), tests/acceptance/test_US015_categorie.py (gewijzigd), tests/acceptance/test_US012_c8_placeholder.py (nieuw), tests/acceptance/test_US013_c5_readme.py (nieuw), tests/acceptance/test_US015_c7_feeds.py (nieuw), tests/acceptance/test_US012_extra_404.py (nieuw), tests/acceptance/README.md (gewijzigd), docs/test-reports/iteratie-4-ronde-2.md (nieuw). Tijdelijke bestanden (ophaalronde, gebouwde site, screenshot) staan alleen in de tijdelijke map van het systeem. Servers: geen achtergronddiensten gestart; alle Edge-processen van de tests zijn gestopt.
