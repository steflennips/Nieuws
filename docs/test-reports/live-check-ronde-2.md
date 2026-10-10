ITERATIE: 8 (live-check na workflow-fix, US-013 c1/c3) | RONDE: 2 | MODUS: SNEL
RESULTAAT: NIET GESLAAGD (BELANGRIJK open: de conflictvrije workflow-stap en de korte publieke README staan NIET op main; de site is wel bijgewerkt)

PER CRITERIUM:
- US-013-c1: OK. Bewijs: https://steflennips.github.io/Nieuws/ 200 (text/html); /nieuws.html 200; /bronnen.html 200; /zz-onbekend.html 404 met eigen pagina; style.css, app.js, favicon.svg, favicon.ico 200. Last-Modified nu 10 okt 2026 04:57:09 GMT (vorige check: 9 okt 18:49:08 GMT). KLEIN, bekend: /404 (zonder extensie) geeft 200 (soft 404).
- US-013-c2: NIET GETEST (volledig). Bewijs: publieke workflow op main heeft cron "0 4 * * *" en workflow_dispatch. Een geplande run (event schedule) staat nog niet in de API (0 runs); de run van 10 okt 04:00 UTC was er bij de check (ongeveer 05:10 UTC) nog niet. Dat is geen fout, maar de geplande start is nog niet bewezen.
- US-013-c3: OK (met voorbehoud). Bewijs: "Laatst bijgewerkt: 10 okt 2026 06:56" (= 04:56 UTC) ligt na 9 okt 20:48. Komt overeen met run 38025801943 (conclusie success, attempt 1, aangemaakt 04:56:36Z, klaar 04:57:16Z). Ook de bot-commit "Nieuws bijgewerkt" (ecae95a, 04:56:55Z) staat op main. Last-Modified is veranderd. Voorbehoud: de geplande run is nog niet gezien.
- US-013-c4: OK. Bewijs: 104 bestanden in de publieke main (raw) gescand op lokale paden, e-mail en sleutel-/wachtwoordpatronen. Geen echte gegevens. Treffers zijn detectiepatronen en testvoorbeelden: fictieve "sk-..."-strings in tests/acceptance/test_US013_workflow.py, het voorbeeldadres a.b@voorbeeld.nl in tests/test_online.py. Geen README.technisch.md in de repo (404).
- US-013-c5: OK op de huidige publieke README, maar NIET de gewenste versie (zie bevinding 2). Bewijs: publieke README (124 regels) bevat een letterlijk feedvoorbeeld (regel 106) en de handmatige startinstructie (Actions > Run workflow, regel 102). De korte lokale README (21 regels) bevat die niet: publiceren daarvan zou c5 breken.

SUITE: n.v.t. (live-check; geen geautomatiseerde acceptatietests gedraaid of toegevoegd)
REGRESSIE: n.v.t. in modus SNEL

BEVINDINGEN:
1. BELANGRIJK: de workflow-fix is niet gepubliceerd. Reproduceren: GET https://api.github.com/repos/steflennips/Nieuws/contents/.github/workflows/nieuws.yml. Verwacht: de conflictvrije terugcommit-stap (3 pogingen, geen pull --rebase). Werkelijk: de oude stap met "git pull --rebase" en "git push" zonder retry; dit is dezelfde versie als op commit 01510da, waarmee de run van 9 okt draaide. Branches: alleen "main" (head ecae95a). Het verschil met de lokale versie is er. Gevolg: een volgende run kan op dezelfde plek falen (de oorzaak van de mislukte attempt 2 is niet vastgesteld, want de logs vragen inloggen). Wordt BLOKKEREND als de geplande run van morgen faalt.
2. BELANGRIJK: de publieke README is niet bijgewerkt. Reproduceren: GET https://raw.githubusercontent.com/steflennips/Nieuws/main/README.md. Verwacht: de nieuwe korte site-tekst. Werkelijk: de oude 124-regelige versie (blob cbf874d), met de tekst "team van drie AI-rollen", /iteratie-commando's en de projectstructuur. Dat is interne projectinformatie op een openbare repo; de keuze hoort bij de PO/Stef (zie bevinding 3).
3. BELANGRIJK (PO-beslissing): de korte lokale README bevat geen feedvoorbeeld en geen handmatige startinstructie. Publiceren daarvan breekt US-013 c5. Keuze nodig: de korte README met c5-tekst erin, of README.technisch.md die dan wel in de repo komt (dan opnieuw toetsen op de c5-regel).
4. Stef meldde dat de README en nieuws.yml gepusht zijn. Op main is dat niet te zien: de laatste commit is de bot-commit van 10 okt 04:56:55Z, er is geen commit van Stef. Mogelijk is er nog niet gepusht, of is dat lokaal gebeurd zonder push. Ter controle: lokaal `git log origin/main` (alleen-lezen).
5. VERSCHIL MET VORIGE CHECK (informatief, geen fout): tellers 93 -> 90 berichten. BI 32 -> 30, Data 5 -> 5, Automatisering 19 -> 19, AI 37 -> 36. AI is 36 van 90 = 40%, dus het AI-plafond klopt. Oorzaak van de daling van 3 items is niet vastgesteld (de feeds en de 60-daagse bewaartermijn zijn niet opnieuw gecontroleerd). Het aantal op Nieuws (90 article-elementen) klopt met de teller en met "Alle 90 berichten".
6. Nieuwste artikeldatum: 10 okt 2026 (vandaag); oudste 18 aug 2026 (binnen de 60 dagen). Plausibel: de run was om 06:56 lokale tijd en het artikel kan vóór die tijd zijn verschenen. Het tijdstip van artikelen staat niet op de site, dus niet te verifiëren.
7. KLEIN (bekend, Stef oordeelt): Uitgelicht toont nog het vendor-productitem (OutSystems Agent Experience, Techzine); het LUMC-item staat nog bij Automatisering. Data is 5 van 90 items (5,6%). Soft 404 op /404 (zie c1).
8. KLEIN: docs/test-reports van de publieke repo bevat operationele notities (procesnummers, lokale poort). Geen geheim.

NIET GETEST:
- US-013-c2 geplande run (cron 04:00 UTC): nog geen geplande run zichtbaar; controle later nodig (zie voorstel).
- GitHub Actions-logs van attempt 2 (oorzaak mislukking): vereist inloggen; niet gelezen.
- Visuele beoordeling van 375 px en 1280 px: niet opnieuw gedaan in deze ronde (ronde 1 had een screenshot-beoordeling; die is niet herhaald). Geen browser-inspectie uitgevoerd, alleen HTTP-checks.
- Geen push, geen login, geen workflow gestart (conform opdracht).

VOORSTEL CONTROLE VOLGENDE RONDE:
(a) Na de push van de nieuwe nieuws.yml en README: GET api.github.com/repos/steflennips/Nieuws/contents/.github/workflows/nieuws.yml en de README; controleer de conflictvrije stap en de korte site-tekst met c5-regels (of de bewuste keuze van de PO).
(b) Na de geplande run van 11 okt (of later): GET .../actions/runs?event=schedule, conclusie success en tijdstip rond 04:00-06:00 UTC; en "Laatst bijgewerkt" op de startpagina.

BENODIGD VAN BOUWER:
(1) Stef: bevestig de push van nieuws.yml en README naar main (lokaal `git log origin/main`), of push ze alsnog nadat jij ze hebt gecontroleerd. Dit is door mij niet gedaan.
(2) PO-beslissing: korte README (c5 opnieuw toetsen) of README.technisch.md (dan geen c5 in de publieke repo), en de interne projectbeschrijving uit de publieke README (bevinding 2).
(3) Stef: de oorzaak van de mislukte attempt 2 in het logboek van de Actions-run bekijken (inloggen vereist) en de foutregel doorgeven.

BESTANDEN GEWIJZIGD DOOR MIJ: docs/test-reports/live-check-ronde-2.md (dit rapport). Geen bestanden in tests/acceptance/ of elders gewijzigd. Tijdelijke downloads (HTML, YAML, JSON) staan in de tijdelijke map van het systeem en zijn buiten de projectmap gebleven.
