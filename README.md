# POC app

Proefproject waarin een team van drie AI-rollen een app bouwt: **Product Owner**, **Bouwer** en **Tester**. Stef is de opdrachtgever.

## Starten
1. Open deze map in Claude Code (`claude` in deze map).
2. Typ `/iteratie` om de eerste ronde te starten. De Product Owner begint met een intake en stelt je vragen.
3. Na elke iteratie krijg je een korte samenvatting en geef je groen licht voor de volgende.

Opties: `/iteratie <extra instructie>`, bijvoorbeeld `/iteratie focus op het dashboard`.

## Structuur
- `CLAUDE.md` werkwijze en loop-protocol
- `.claude/agents/` de drie rollen
- `.claude/commands/iteratie.md` het commando voor één iteratie
- `docs/` vision, backlog, status, testrapporten (door de hoofdsessie opgeslagen), beslissingen
- `src/` ophalen, bouwen, mix en veiligheidscontrole (Bouwer)
- `tests/` eigen tests van de Bouwer; `tests/acceptance/` de acceptatiesuite van de Tester

## Nieuws ophalen en site bouwen
Vereist: Python 3.10 of nieuwer. Verder niets installeren. Alle commando's draai je vanuit deze map. Er is geen lokale app meer: het product is de statische nieuwssite (map `site/`).

Eerst nieuws ophalen:
```
python src/ophalen.py
```
Dit leest `config/feeds.json` (10 gratis RSS/Atom-feeds: algemeen NL-nieuws, BI en automatisering; trefwoorden per categorie, bewaartermijn 60 dagen) en schrijft `data/nieuws.json`. Per feed zie je `OK` met aantallen (items in feed, bewaard na het 60-dagenfilter, nieuw, verouderd) of `FOUT` met een korte reden; een uitgevallen feed breekt niets (oude items blijven staan). Een ontbrekend of ongeldig `--config`-bestand geeft een nette foutmelding (exitcode 2). De config wordt gecontroleerd voordat er iets gebeurt (exitcode 2, Nederlandse melding, `data/nieuws.json` blijft ongewijzigd): `trefwoorden` moet de categorieen `BI`, `Data`, `Automatisering` en `AI` bevatten (let op de hoofdletters), elk met een niet-lege lijst van niet-lege termen; `uitsluitingen`, `weigertermen`, `weigertermen_samenvatting` en `weiger_uitzonderingen` moeten lijsten van tekst zijn; elke feed-url begint met `http://` of `https://`; `feeds` mag niet leeg zijn. Een config met BOM (Kladblok) wordt gewoon gelezen.

**Vangnet tegen wissen (`--forceer-opruimen`).** Zou de herindeling van de opgeslagen items (nieuwe trefwoorden, uitsluitingen of weigertermen) meer dan 50% van de items van bronnen die in de config staan verwijderen, dan schrijft `python src/ophalen.py` niets weg: exitcode 1 en een melding met de aantallen. Precies 50% wordt nog geschreven, 51% niet. Items van bronnen die niet meer in de config staan tellen niet mee (die worden altijd verwijderd). Controleer in zo'n geval eerst de config op een typo. Is de grote opruiming echt de bedoeling, draai dan eenmalig en handmatig `python src/ophalen.py --forceer-opruimen`. **Onleesbaar opslagbestand.** Bestaat `data/nieuws.json` (of het pad van `--uitvoer`) maar is het onleesbaar (afgekapt, ongeldige JSON, geen UTF-8, UTF-8 met BOM, een andere structuur dan een object met een lijst `items`, of het pad is een map), dan stopt `ophalen.py` voordat er iets wordt opgehaald: Nederlandse melding met het pad, exitcode 2, het bestand blijft byte-gelijk en er komt geen `.tmp`-restbestand. Herstel of verwijder het bestand dan zelf. Een ontbrekend bestand is toegestaan (eerste run begint leeg); een bestand van 0 bytes (of alleen witruimte) telt ook als leeg, omdat er niets te verliezen is. **Leeftijdsopruiming en `bewaar_dagen`.** `bewaar_dagen` in de config moet een geheel getal van minimaal 1 zijn (standaard 60); anders stopt `ophalen.py` met exitcode 2 en een Nederlandse melding. Het vangnet geldt ook voor de leeftijdsopruiming: verdwijnt door herindeling en opruiming samen meer dan 50% van de opgeslagen items van geconfigureerde bronnen (bijv. door een typo als 6 i.p.v. 60), dan wordt niets geschreven (exitcode 1) tenzij je `--forceer-opruimen` gebruikt. Het gewone dagelijkse verouderen blijft ver onder die grens. **Onvolledige opgeslagen items.** Een opgeslagen item met een ontbrekende of ongeldige link of datum (bijv. `null`), of een titel die geen tekst is, wordt overgeslagen met een Nederlandse waarschuwing (titel en link) en niet meer bewaard; de run gaat gewoon door. Ontbreekt alleen het `id`, dan wordt het hersteld uit de link. De dagelijkse GitHub-job (`.github/workflows/nieuws.yml`) gebruikt die optie bewust niet. Exitcode 0 als minstens een feed slaagde; slaagt geen enkele, dan blijft het bestand ongewijzigd en is de exitcode 1. `data/nieuws.json` hoort wel in git: de dagelijkse job bewaart de laatste 60 dagen daarin. Items van een bron die niet meer in `config/feeds.json` staat worden bij het ophalen verwijderd; items van een feed die wel in de config staat maar even uitvalt blijven staan.

Feeds toevoegen of verwijderen: pas de lijst `feeds` in `config/feeds.json` aan (naam, url, taal `nl`/`en`). Trefwoorden staan in dezelfde file: hele woorden, hoofdletterongevoelig; een `*` aan het eind betekent "woorden die hiermee beginnen" (bijv. `automati*`). Er zijn 4 categorieen: BI, Data, Automatisering en AI. De categorie met de meeste treffers wint, bij gelijkspel in de volgorde BI, Data, Automatisering, AI; een AI-woord telt alleen als het in de titel staat (in de samenvatting niet). Items zonder treffer worden niet bewaard. Onder `uitsluitingen` staan termen die niet meetellen als treffer (bijv. `Data Master`, een Asustor-productnaam, en `data center*`); voeg daar een term toe als een productnaam een item in de verkeerde categorie duwt. Bij elke ophaalronde worden ook de al opgeslagen items opnieuw ingedeeld.

**Kwaliteitsfilter (weigerlijst).** In `config/feeds.json` staat `weigertermen`: een item met zo'n term in de titel (hele woorden, hoofdletterongevoelig, `*` = woorden die ermee beginnen) wordt niet opgeslagen, bijvoorbeeld webinar, deals (maar niet "deal": overnamenieuws blijft staan), review, smartphone, game*, console*, gadget*. `weigertermen_samenvatting` (sponsored, gesponsord, partnerbijdrage, advertorial) geldt ook voor de samenvatting. Per feed meldt het ophalen hoeveel items zijn geweigerd, met een paar voorbeeldtitels. Een term met voorvoegsel `re:` is een reguliere expressie (zo staat "nog vier weken tot" erin). `weiger_uitzonderingen` bevat zakelijke combinaties die niet meetellen (operational review, code review, peer review, security review, analogy game, game theory, gamechanger, game changer). Het ophaallog telt per feed unieke nieuwe links. Voeg een term toe of haal hem weg als het filter te veel of te weinig tegenhoudt. Het ophalen volgt `robots.txt` en meldt zich met een eigen User-Agent.

Wat staat er op de site:
- **Overzicht** (`index.html`): bovenaan het blok Uitgelicht (zie de scoreregel hieronder), daaronder tellertegels per categorie, en het blok Vaknieuws. AI is hooguit 40% van de getoonde nieuwsitems.
- **Nieuws** (`nieuws.html`): alle opgehaalde artikelen, filter op BI / Data / Automatisering / AI, zoeken op trefwoord.

Het uiterlijk (strak en zakelijk, donkerblauw met teal accent, kleuren als CSS-variabelen bovenaan `site/style.css`, gegenereerd door `src/bouw.py`) werkt op 1280 px en op telefoonbreedte (375 px). Filterwaarden in de URL zijn hoofdletterongevoelig; onbekende waarden tonen alles.

## Openbare statische site bouwen
```
python src/ophalen.py     # eerst nieuws ophalen (zie boven)
python src/bouw.py        # bouwt de map site/ uit data/nieuws.json en config/feeds.json
```
Opties: `--data`, `--config`, `--uit` (andere paden) en `--vandaag JJJJ-MM-DD` (peildatum voor Uitgelicht, voor tests; standaard vandaag).

**AI-plafond.** Bij het bouwen blijven alle BI-, Data- en Automatisering-items staan en van AI alleen de nieuwste items, zodat AI hooguit 40% van alle getoonde items is (naar beneden afgerond; bij 20 andere items dus 13 AI). Bestaat alles uit AI-items, dan stopt de bouw met een melding over het AI-plafond (exitcode 1); een item met ongeldige datum wordt overgeslagen met een waarschuwing (exitcode 0). Nieuws, tellertegels en Overzicht gebruiken alleen die getoonde items; in `data/nieuws.json` blijft alles bewaard.

**Uitgelicht (scoreregel).** Het blok Uitgelicht op het Overzicht toont maximaal 5 items uit de laatste 3 dagen (datum van vandaag min 3 dagen of nieuwer), waarvan hooguit 2 AI, en **alleen items uit feeds met `"headnieuws": true`**. Productblogs (Power BI, Fabric, n8n, Camunda, enz.) staan dus nooit in Uitgelicht, wel op Nieuws en eventueel in Vaknieuws. Score per item: 2 punten als de bron een headnieuws-feed is, plus 1 punt als die feed taal `nl` heeft (voorkeur voor Nederlands), plus 1 punt per verschillende term uit `deux_relevantie` (in `config/feeds.json`) in titel of samenvatting (hele woorden). Hoogste score eerst; bij gelijke score de nieuwste eerst. Is er te weinig headnieuws, dan toont het blok minder dan 5 items; het wordt niet aangevuld met productblogs. Zijn er helemaal geen geschikte headnieuws-items, dan staat er "Nog geen uitgelicht nieuws". Het blok Vaknieuws daaronder (geen taalvoorkeur) toont de 5 nieuwste items die niet in Uitgelicht staan, hooguit 2 AI (aangevuld met de volgende nieuwste niet-AI-items; zijn die er niet, dan zijn het er minder dan 5). Uitgesloten van Uitgelicht en Vaknieuws (maar wel op Nieuws): titels die met "Kort:" beginnen (digests) en items met een term uit `evenement_termen` (config/feeds.json; evenement, conferentie, congres, summit, world forum, meld je aan, aanmelden, inschrijven) in titel of samenvatting, hele woorden, hoofdletterongevoelig. Pas die lijst zelf aan. De lijst `deux_relevantie` (MKB, ZZP, Nederland, Power BI, n8n, enz.) pas je zelf aan. In `site/` staan `index.html` (Overzicht met Uitgelicht, tellers per categorie (BI, Data, Automatisering, AI) en Vaknieuws), `nieuws.html` (filter en zoeken, werkt in de browser via `?categorie=AI&q=zoekterm`), `bronnen.html` (alle bronnen, gelinkt vanuit de voet), `404.html` (eigen foutpagina, door GitHub Pages automatisch getoond), `style.css`, `app.js` en favicons. Alle links zijn relatief, dus de map werkt overal, ook onder `https://<account>.github.io/<repo>/`. Er staat geen voorbeelddata in; zonder `data/nieuws.json` stopt het commando met een foutmelding. De map `site/` staat in `.gitignore` (wordt door de job gebouwd).

Lokaal bekijken (eenvoudige statische server, na het bouwen): `python -m http.server 8000 --directory site` en ga naar http://127.0.0.1:8000 (stoppen: Ctrl+C).

## Online zetten op GitHub Pages (stappen voor Stef, eenmalig)
Het workflow-bestand staat klaar in `.github/workflows/nieuws.yml`. Er zijn geen wachtwoorden, tokens of sleutels voor nodig: de job gebruikt het automatische `GITHUB_TOKEN` van GitHub zelf. Je gebruikt je **bestaande GitHub-account** (geen organisatie nodig); het adres wordt `https://<accountnaam>.github.io/<repo>/`. Vervang `<accountnaam>` en `<repo>` hieronder door je eigen gebruikersnaam en de naam die je de repo geeft (bijv. `nieuws`).

**Wat openbaar wordt.** De repo moet **openbaar** zijn (gratis plan), dus alles wat je pusht kan iedereen lezen. Bewuste keuze: `.claude/`, `CLAUDE.md` en `docs/` gaan mee (werkafspraken en logboek van dit project, zonder geheimen), net als `data/nieuws.json`. Niet mee gaan `site/` (bouwt de job zelf), `__pycache__`, `.env`, `*.log`, sleutelbestanden en alles wat op `NTUSER` of `.claude.json` lijkt (zie `.gitignore`). Zie `docs/decisions/2026-10-08-online-zetten-voorbereiding.md`.

**Stap A: controle vooraf (PowerShell, in de map `POC app`)**
1. Draai de veiligheidscontrole:
   ```
   python src/veilig_check.py
   ```
   Het moet eindigen met `OK: geen geheimen, e-mailadressen, lokale paden of verdachte bestanden gevonden.` (exitcode 0). Staat er `NIET VEILIG`, los dat dan eerst op en draai opnieuw.
2. Kijk waar git nu naar wijst:
   ```
   git rev-parse --show-toplevel
   git remote -v
   ```
   De git-map boven `POC app` is nu je **hele gebruikersmap** (het pad eindigt op je gebruikersnaam, niet op `POC app`). Die mag je **nooit** pushen. Heeft die al een `origin`, dan hoort die bij je gebruikersmap: voeg hem niet opnieuw toe en push er niets naartoe.

**Stap B: repo aanmaken op github.com** (ingelogd met je bestaande account)
1. Klik rechtsboven op **+ > New repository**.
2. Owner: je eigen account. Repository name: `<repo>`. Kies **Public**. Zet **Add a README file**, **.gitignore** en **license** allemaal **uit** (de repo moet leeg zijn). Klik **Create repository**.

**Stap C: de projectmap als eigen repo (PowerShell, in de map `POC app`)**
```
git init
git rev-parse --show-toplevel
```
De tweede regel **moet** een pad tonen dat eindigt op `POC app`. Toont hij je gebruikersmap, **stop dan** en push niets. Klopt het, ga dan door:
```
python src/veilig_check.py
git add .
git status
git commit -m "Eerste versie"
git branch -M main
git remote add origin https://github.com/<accountnaam>/<repo>.git
git remote -v
git push -u origin main
```
Kijk bij `git status` (voor het committen) of er niets bij staat wat je niet openbaar wilt hebben; `site/`, `NTUSER*` en `.claude.json` horen er niet tussen. `git remote -v` moet twee keer `<accountnaam>/<repo>` tonen. Bij het pushen vraagt GitHub om in te loggen via een browservenster; zet nooit een token in een bestand.

**Stap D: Pages en rechten (in de repo op github.com)**
1. **Settings > Pages > Build and deployment > Source: GitHub Actions**.
2. **Settings > Actions > General > Workflow permissions: Read and write permissions** (nodig om de nieuwe `data/nieuws.json` terug te zetten in de repo), daarna **Save**.

**Stap E: eerste keer starten.** Start de job eenmalig handmatig (zie hieronder, bij de vetgedrukte kop over handmatig starten). Na een minuut of twee staat de site op `https://<accountnaam>.github.io/<repo>/`. Geef die URL door; dan wordt hij gecontroleerd. De eerste run haalt het nieuws op en publiceert alleen echte data (nooit voorbeeldartikelen); lukt dat niet (alle feeds onbereikbaar), dan faalt de run zichtbaar en wordt er niets gepubliceerd.

Daarna draait de job elke dag om 04:00 UTC (06:00 Nederlandse zomertijd, 05:00 in de winter; GitHub kan de start enkele minuten tot uren uitstellen). Hij haalt het nieuws op, bouwt de site, bewaart `data/nieuws.json` in de repo en publiceert. De "Laatst bijgewerkt"-tijd in de voet laat zien wanneer dat voor het laatst gelukt is. GitHub zet geplande jobs uit na 60 dagen zonder activiteit in de repo; de dagelijkse data-commit voorkomt dat meestal, en je kunt hem altijd weer aanzetten onder Actions.

**Job handmatig starten:** in de repo tabblad **Actions > Nieuws verversen en publiceren > Run workflow > Run workflow**. Fouten (bijv. alle feeds onbereikbaar) zie je daar in het logboek van de run.

**Feeds beheren:** open `config/feeds.json` in de repo (potlood-icoon op GitHub, of lokaal bewerken en pushen). Pas de lijst `feeds` aan: daarin staat per feed een regel. Een feed **toevoegen** doe je door een regel toe te voegen (let op de komma tussen regels, de laatste regel heeft geen komma), bijvoorbeeld:
```
{"naam": "Microsoft Power Platform Blog (Power Automate)", "url": "https://www.microsoft.com/en-us/power-platform/blog/feed/", "taal": "en"}
```
(`taal` is `nl` of `en`. Bij een algemene NL-bron kun je `, "headnieuws": true` achter `"taal": "nl"` zetten, zoals bij Computable in het bestand: alleen items van zulke feeds komen in aanmerking voor het blok Uitgelicht; bij `nl` krijgen ze daar 1 extra punt.) Een feed **verwijderen** doe je door zijn hele regel te verwijderen. Commit daarna en start de job handmatig. Een feed verwijderen haalt ook de al opgeslagen items van die feed weg bij de eerstvolgende ophaalronde. Trefwoorden en uitsluitingen pas je op dezelfde plek aan.

Tests draaien:
```
python -m unittest discover -s tests -v
```
Dit omvat ook de tests voor het bouwcommando, het workflow-bestand (`tests/test_bouw.py`), de mix, het kwaliteitsfilter en Uitgelicht (`tests/test_mix.py`) en de categorie-indeling met een vaste testset van 35 titels plus 6 echte titels met samenvatting (`tests/test_categorie.py`). De tests werken zonder internet (lokale testfeeds op 127.0.0.1) en zonder `data/nieuws.json`. De acceptatietests van de Tester staan in `tests/acceptance/` (zie `tests/acceptance/README.md`). Commando: `python -m unittest discover -s tests/acceptance -t tests/acceptance -v`.

## Proefronde (optioneel, bij een nieuw project)
Draai bij een nieuw project voordat je de echte app bouwt één proefronde met een triviale app (bijvoorbeeld een pagina met een teller). Controleer:
1. `/agents` toont `product-owner` (opus), `builder` (sonnet) en `tester` (haiku).
2. De PO stelt intakevragen en die komen bij jou terecht.
3. De Bouwer bouwt en de app start (en servers worden weer afgesloten).
4. De Tester schrijft tests alleen in `tests/acceptance/`; de gebiedscontrole met git meldt geen overtredingen.
5. Het testrapport staat in `docs/test-reports/`, de tellers in `docs/STATUS.md` kloppen.
6. De samenvatting aan jou is kort en bevat een verbruiksregel.
Gooi het resultaat daarna weg (nieuwe map of `git reset`) en begin met de echte app.
