# 2026-10-08: Online zetten voorbereiden (iteratie 5, Bouwer)

- Hosting: GitHub Pages vanuit een nieuwe, lege, openbare repo onder Stefs bestaande GitHub-account (geen organisatie). Adres `<accountnaam>.github.io/<repo>`; in de README staan placeholders.
- Eigen repo alleen in `POC app` (git-root is nu de gebruikersmap). README geeft controles met `git rev-parse --show-toplevel` en `git remote -v`; `src/veilig_check.py` scant vooraf wat git zou meenemen (geheimen, e-mailadressen, lokale paden, verdachte bestandsnamen).
- Wat meegaat: `.claude/`, `CLAUDE.md`, `docs/`, `data/nieuws.json`, tests. Reden: het is een en hetzelfde projectwerk; weglaten zou de repo onvolledig maken en bevat na de scan geen geheimen. Wel in `.gitignore`: `site/`, caches, `.env`, logs, sleutelbestanden, `NTUSER*`, `.claude.json*`, `.claude/settings.local.json`. Gevolg: de repo en dus het werkproces zijn openbaar (README vermeldt dit).
- Workflow: `configure-pages` verwijderd (niet nodig, vermijdt extra rechten); `git pull --rebase` voor de push tegen een afgewezen push. Rechten: `contents: write` (bouwen), `pages: write` + `id-token: write` (publiceren). De veiligheidsscan draait bewust niet in de job (artikeltekst uit feeds kan vals alarm geven).
- Eerste run: `ophalen.py` kan overweg met ontbrekend of leeg `data/nieuws.json`; mislukt alles, dan faalt de run en wordt niets gepubliceerd (geen voorbeelddata).
- `bronnen.html`: bron buiten de config krijgt een link als al haar artikelen op dezelfde https-site staan, anders blijft het platte tekst.
