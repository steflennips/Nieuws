ITERATIE: 8 (live-check na publicatie workflow-fix en README, US-013 c1-c5) | RONDE: 3 | MODUS: SNEL
RESULTAAT: NIET GESLAAGD (BELANGRIJK open: de nieuwe README en de conflictvrije nieuws.yml staan NIET op main; de publieke repo bevat de hele projectmap)

Live-check van 2026-10-10, 05:26 UTC. Alleen GET-verzoeken: raw.githubusercontent.com, api.github.com (publiek), codeload-archief van main (gelezen en gescand, niet uitgevoerd) en de site. Geen push, geen login, geen workflow gestart.

PER CRITERIUM:
- US-013-c1: OK. Hoofdpagina 200 text/html; nieuws.html 200; bronnen.html 200; style.css, app.js, favicon.svg 200; zz-onbekend.html 404 met eigen pagina.
- US-013-c2: NIET GETEST (nog niet bewezen). Op main staat cron "0 4 * * *". GET actions/runs?event=schedule geeft total_count 0 om 05:26 UTC, 86 minuten na het slot van 04:00 UTC. Dat is nog geen bewijs van een fout (GitHub kan vertragen), maar de geplande start is niet gezien.
- US-013-c3: OK (met voorbehoud). Site toont "Laatst bijgewerkt: 10 okt 2026 06:56" (time datetime 2026-10-10T04:56:45+00:00). Run 38025801943 (workflow_dispatch) conclusie success, aangemaakt 04:56:36Z; bot-commit ecae95a "Nieuws bijgewerkt" op 04:56:55Z staat op main. Geplande run nog niet gezien.
- US-013-c4: OK. Archief van main (104 bestanden) gescand op lokale paden, gebruikersnaam, e-mailadressen en sleutel-/wachtwoordpatronen. Alleen fictieve testvoorbeelden gevonden: "sk-..."-strings in tests/acceptance/test_US013_workflow.py, a.b@voorbeeld.nl en password=abcdefgh1234 als testinvoer in tests/test_online.py. Geen echte gegevens. Geen verboden bestanden (NTUSER*, .claude.json*, __pycache__, .env, README.technisch.md, sleutelbestanden) in de repo.
- US-013-c5: FAALT. Publieke README op main (raw en API: 124 regels, 17071 bytes, blob cbf874d) is de oude interne tekst: "team van drie AI-rollen", "/iteratie", projectstructuur. De korte site-README staat wel lokaal (22 regels) maar niet op main. Die korte versie bevat ook geen feedvoorbeeld en geen handmatige startinstructie, dus de c5-controle uit ronde 2 faalt na publicatie tenzij de eis wordt herzien (zie BENODIGD).
- Aanvullend: README.technisch.md op main GET 404 (OK).

SUITE: n.v.t. (live-check; geen acceptatietests gedraaid, geen bestanden in tests/acceptance gewijzigd)
REGRESSIE: n.v.t. in modus SNEL

BEVINDINGEN:
1. BELANGRIJK: de push van README.md en .github/workflows/nieuws.yml is niet op main terechtgekomen. Reproduceren: GET https://api.github.com/repos/steflennips/Nieuws/commits?sha=main. Laatste commits: 10 okt 04:56:55Z (bot "Nieuws bijgewerkt"), 9 okt 18:48:52Z (bot), en de enige commit van Stef is "Eerste versie" op 9 okt 18:41:05Z. Lokaal: git status toont README.md en .github/workflows/nieuws.yml als gewijzigd (niet gecommit); de lokale HEAD staat op ab87fb0 en loopt 2 bot-commits achter origin/main. Blob-hashes wijken af: README remote cbf874d, lokaal 7f9b2c9; nieuws.yml remote b1af054, lokaal 97e96f3. Verwacht: korte README en conflictvrije nieuws.yml op main. Werkelijk: de oude versies.
2. BELANGRIJK: de oude workflow staat nog op main (GET raw/API, regels 32-43): "git commit", "git pull --rebase", "git push" zonder retry en zonder waarschuwing. Verschillen met de lokale versie: lokaal fetch + reset naar origin, opnieuw toepassen van data/nieuws.json, maximaal 3 pogingen, waarschuwing en samenvatting i.p.v. mislukken, env BRANCH. Gelijk in beide: cron "0 4 * * *", workflow_dispatch, concurrency, contents: write als enige extra recht, geen secrets, stappen ophalen/bouwen/upload/deploy. Risico: run 37975841502 (head ab87fb0, workflow_dispatch) staat op conclusie failure, run_attempt 2, bijgewerkt 10 okt 04:49:30Z. Oorzaak niet vastgesteld (logs vereisen inloggen). Dit is precies het patroon dat de fix moest voorkomen.
3. BELANGRIJK (beslissing Stef): de publieke repo bevat de hele projectmap, niet alleen site en README. Op main staan onder meer CLAUDE.md, .claude/agents/ (3 rolbestanden), .claude/commands/iteratie.md, docs/STATUS.md (budget, aanroepen, logboek), docs/BACKLOG.md, docs/decisions/ en docs/test-reports/ (incl. iteratie-8-ronde-5 met NIET GESLAAGD), src/ en tests/. Geen geheimen of lokale paden gevonden (zie c4), maar de werkwijze die de korte README moest verbergen staat in de bestanden zelf. Stef moet beslissen of dat de bedoeling is.
4. KLEIN (bekend, ongewijzigd): /404 zonder extensie geeft 200 text/html (soft 404). /nieuws zonder .html geeft 200.
5. Open punt (geen bevinding): de geplande run is nog niet zichtbaar (zie c2).

NIET GETEST:
- US-013-c2 geplande run: nog niet zichtbaar 86 minuten na het slot; controle nodig op 11 okt rond 06:30 NL (actions/runs?event=schedule).
- Nieuwe workflow en README live: niet te testen zonder push (push valt buiten deze opdracht). Daardoor ook geen run na de push.
- Logs van run 37975841502 (oorzaak attempt 2): vereist inloggen.
- Visuele beoordeling 375 px en 1280 px: niet gedaan (alleen HTTP-checks).
- Lokale acceptatiesuite: niet opnieuw gedraaid (niet in de opdracht).

BENODIGD VAN BOUWER:
(1) Stef: lokale main eerst bijwerken (pull) en daarna README.md en .github/workflows/nieuws.yml committen en pushen naar main. Controleer met git show --stat dat de bot-commits alleen data/nieuws.json raken, dan geeft de pull geen conflict. Daarna opnieuw live-check (ronde 4).
(2) PO/Stef: c5-eis herzien (korte README zonder feedvoorbeeld en startinstructie) of README.technisch.md gebruiken, zoals open in ronde 2.
(3) Stef: beslissen of de hele projectmap (CLAUDE.md, .claude/, docs/) publiek mag blijven. Zo niet: de publieke repo moet beperkt worden tot site en README; dat is een wijziging buiten de Tester-scope.
(4) Stef: de foutregel uit de Actions-log van run 37975841502 (attempt 2) doorgeven.

BESTANDEN GEWIJZIGD DOOR MIJ: docs/test-reports/live-check-ronde-3.md (dit rapport). Geen andere bestanden. Tijdelijke downloads staan in de tijdelijke map van het systeem, buiten de projectmap.
