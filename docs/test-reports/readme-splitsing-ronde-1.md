ITERATIE: 8 (README-splitsing, buiten de iteratieloop, verzoek Stef) | RONDE: 1 | MODUS: SNEL
RESULTAAT: NIET GESLAAGD (de README-controles zijn OK; de suite bevat 6 open rode tests uit US-022 ronde 5, zie BEVINDINGEN 1-5)

PER CRITERIUM:
- README-splitsing c1 (publieke README: geen lokale paden): OK. `test_README_splitsing_c1_publieke_readme_geen_lokale_paden` geslaagd.
- README-splitsing c2 (publieke README: geen werkafspraken, rollen, testcommando's): OK. `test_README_splitsing_c2_...` geslaagd.
- README-splitsing c3 (publieke README: site-link en Overzicht/Nieuws/Bronnen): OK. `test_README_splitsing_c3_...` geslaagd.
- README-splitsing c4 (geen persoonlijk account buiten exacte site-link en bedrijfsnaam): OK. `test_README_splitsing_c4_...` geslaagd.
- README-splitsing c5 (README.technisch.md in .gitignore, lokaal aanwezig): OK. Regel staat in .gitignore; `git check-ignore` (alleen-lezen) geeft de regel als treffer; beide tests geslaagd.
- README-splitsing c6 (`python src/veilig_check.py` exitcode 0): OK. Exitcode 0 en OK-regel aanwezig; testen geslaagd.
- US-013-c5 (feeds beheren, voorbeeldregel, job handmatig, online zetten): OK. 5 tests geslaagd op README.technisch.md.
- US-018-c3 (scoreregel in README): OK. Geslaagd op README.technisch.md.
- US-020-c1 (geen leadwoorden in README.md en README.technisch.md): OK. Geslaagd; beide bestanden gecontroleerd.
- US-020-c4 (geen startinstructie lokale app; ophalen/bouwen/feeds/publiceren): OK. Geslaagd op beide README's.
- US-021-c2 (headnieuws, NL-punt, "niet aangevuld"): OK. Geslaagd op README.technisch.md.
- It.5 README-stappen A-E, stopinstructie, veilig_check-eindregel, workflow-naam: OK. Geslaagd op README.technisch.md.
- It.5 geen lokaal pad of persoonlijk account (publieke README): OK. Geslaagd met de exacte uitzondering van de site-link en bedrijfsnaam.
- US-022 extra ronde 5 (dataverlies en tracebacks, buiten deze wijziging): FAALT. Zie BEVINDINGEN 1-5.

SUITE:
- Acceptatiesuite: 312 tests, 301 geslaagd, 6 gefaald (alle US-022 ronde 5), 5 overgeslagen (niet uitgevoerd). Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance`
- Unittests (tests/): 150 tests, alle geslaagd. Commando: `python -B -m unittest discover -s tests`
- Ter vergelijking, vóór de wijziging: acceptatiesuite 305 tests, 19 gefaald (13 README-tests en de 6 US-022 ronde 5-tests).
- Nieuwe tests: 7 in `test_README_splitsing.py`. Alle 7 geslaagd.

REGRESSIE: 6 regressies open, niet door deze wijziging: de 6 US-022 ronde 5-tests waren al rood vóór de wijziging en zijn niet aangepast. De 13 README-tests die door de splitsing rood werden, zijn nu groen.

BEVINDINGEN:
1. BLOKKEREND (bestaand, open): dataverlies bij handmatig gewijzigde opslag. `test_US022_extra_r5a_andere_datumnotatie_wist_niet_stil_86_van_87`.
   - Stappen: `python -B -m unittest test_US022_ronde5_dataverlies` (vanuit tests/acceptance); de test bouwt een opgeslagen bestand met 87 items en een andere datumnotatie, en draait ophalen.
   - Verwacht: items blijven behouden of er komt een melding met reden.
   - Werkelijk: exitcode 0, 86 van 87 items verdwijnen zonder melding (1 van 87 blijft over).
2. BELANGRIJK (bestaand, open): `test_US022_extra_r5b_bronnaam_van_alle_items_gewijzigd_wist_niet_stil`. Zelfde patroon bij een gewijzigde bronnaam: exitcode 0, 86 van 87 items stil weg.
3. BELANGRIJK (bestaand, open): `test_US022_extra_r5c_bewaar_dagen_extreem_groot_geen_traceback`. bewaar_dagen 1000000 passeert de validatie en geeft een traceback (OverflowError in src/ophalen.py). Verwacht: nette foutmelding, exitcode 2 of 1. Werkelijk: traceback.
4. BELANGRIJK (bestaand, open): `test_US022_extra_r5d_samenvatting_als_getal_geen_traceback`. Samenvatting als getal geeft een traceback (AttributeError). Verwacht: geen traceback.
5. BELANGRIJK (bestaand, open): `test_US022_extra_r5e_bron_als_lijst_geen_traceback` en `test_US022_extra_r5f_ongeldige_regex_in_weigertermen_geen_traceback`. Bron als lijst geeft een traceback (TypeError); een ongeldige re:-regex in weigertermen ook (regex-fout). Verwacht: nette melding, geen traceback.
6. KLEIN (besluit ter bevestiging): de publieke README noemt de bedrijfsnaam in de titel en in de intro. De test staat die exacte tekst toe; elke andere treffer van het accountspoor blijft verboden. Bevestig dat de bedrijfsnaam mag blijven staan.
7. KLEIN (niet onderzocht): tijdens de acceptatiesuite verscheen een `ConnectionResetError (WinError 10054)` in de uitvoer. Geen test faalde erdoor; waarschijnlijk een afgebroken verbinding in een testserver.

NIET GETEST:
- Weergave van de publieke README op GitHub en de live site-link: NIET GETEST, geen internet; de link is alleen als tekst gecontroleerd.
- US-013 c1 en c3 (live site, Laatst bijgewerkt): NIET GETEST, wachten op het hosting-account van Stef (ongewijzigd).
- De technische tests lezen README.technisch.md, dat alleen lokaal bestaat (bewust, in .gitignore). In een verse clone zonder dit bestand falen die tests (ze worden niet overgeslagen). Dat is ontwerp, geen fout.
- Visuele beoordeling: niet van toepassing in modus SNEL.

BENODIGD VAN BOUWER: de 6 US-022 ronde 5-bevindingen (BEVINDINGEN 1-5) oplossen in src/ophalen.py en/of src/bouw.py. De tests zelf zijn niet aangepast. Verder geen wijziging nodig voor de README-splitsing.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_README_splitsing.py (nieuw)
- tests/acceptance/test_iteratie5_online.py
- tests/acceptance/test_US013_c5_readme.py
- tests/acceptance/test_US013_workflow.py
- tests/acceptance/test_US018_uitgelicht.py
- tests/acceptance/test_US021_uitgelicht.py
- tests/acceptance/test_US020_lokale_app_weg.py
- tests/acceptance/README.md
- docs/test-reports/readme-splitsing-ronde-1.md (dit rapport)
