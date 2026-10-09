# 2026-10-08: Lijst nieuwsfeeds (actueel na iteratie 7, gelijk aan config/feeds.json)

Alle feeds zijn gratis, openbaar (geen login) en `robots_toegestaan` gaf per feed True (gecontroleerd op 2026-10-08 met `ophalen.robots_toegestaan` en een echte ophaalronde zonder fouten). De voorwaarden van de bronnen zijn niet juridisch beoordeeld: we tonen alleen titel, korte samenvatting (max. 300 tekens), datum en een link naar het origineel.

Max. 10 feeds, minstens 3 NL en 3 EN, minstens 2 vooral BI, minstens 2 algemene NL-bronnen (US-016 c5). Feeds met `"headnieuws": true` tellen mee voor de score van het blok Uitgelicht (US-018).

BI / analytics (EN, 3):
- Power BI Blog (Microsoft): https://powerbi.microsoft.com/en-us/blog/feed/ (nieuw it. 6; 12 van 13 items BI)
- Microsoft Fabric Blog: https://blog.fabric.microsoft.com/en-us/blog/feed/ (nieuw it. 6; 17 van 20 BI)
- SQLBI: https://www.sqlbi.com/blog/feed/ (nieuw it. 6; weinig items per maand, wel zeer inhoudelijk over BI/DAX)

Automatisering (EN, 3):
- Microsoft Power Platform Blog (Power Automate): https://www.microsoft.com/en-us/power-platform/blog/feed/ (nieuw it. 7; vervangt AWS Big Data Blog)
- Camunda Blog (procesautomatisering): https://camunda.com/blog/feed/
- n8n Blog (workflow-automatisering): https://blog.n8n.io/rss/

Algemene NL tech/business-bronnen (NL, 4; allemaal headnieuws):
- Computable: https://www.computable.nl/feed/
- Emerce: https://www.emerce.nl/feed
- Techzine: https://www.techzine.nl/feed/
- NOS Tech: https://feeds.nos.nl/nosnieuwstech (nieuw it. 6; vervangt Tweakers)

Totaal 10 feeds: 6 EN, 4 NL.

## Wijzigingen iteratie 6 (US-016: minder AI, meer BI en algemeen nieuws)
Verwijderd (te AI-zwaar of te weinig zakelijk):
- KDnuggets: 8 van 8 items AI.
- InfoQ AI, ML & Data Engineering: 8 van 12 items AI; 1 webinar geweigerd.
- BigDATAwire (Datanami): 7 van 10 AI.
- Tweakers: gadgetnieuws; van 40 items bleven er 2 over (beide AI), 2 geweigerd door het kwaliteitsfilter (review, gamelaptops).
Toegevoegd: Power BI Blog, Microsoft Fabric Blog, SQLBI (BI) en NOS Tech (algemeen NL; overheids- en Kamernieuws raakt de Deux-relevantietermen).
Onderzocht en niet gekozen: NU.nl Tech (robots toegestaan, 14 van 15 AI) en NU.nl Economie (1 relevant item van 30), FlowingData (1 item), Tableau-blog (403), Qlik-blog en Google Cloud Data Analytics (geven HTML, geen feed), ThoughtSpot (404), Frankwatching en ICT Magazine (Cloudflare-blokkade), RTL Nieuws tech (404), MKB.nl (404).
De items van de verwijderde feeds zijn eenmalig uit data/nieuws.json gehaald voor een schone meting; in het normale proces blijven items van verwijderde feeds tot 60 dagen staan.

Resultaat echte ophaalronde 2026-10-08 (104 items opgeslagen en getoond): BI 34 (33%), Data 18 (17%), Automatisering 20 (19%), AI 32 (31%); BI+Data 50%. Aantallen per feed: zie de bouwersrapportage. Open: Automatisering net onder 20%, AWS Big Data levert 61% van Data (US-016 c6 is een meldpunt, geen harde eis).

## Eerdere geschiedenis (kort)
- It. 3: VentureBeat AI (429) en AI News vervangen; AG Connect (404) en Frankwatching (403) -> Techzine; Tweakers direct i.p.v. feedburner; Computable /feed/.
- It. 4: n8n Blog (US-015 c7), AWS Big Data Blog vervangt AWS Machine Learning Blog (c11), Camunda vervangt MIT Technology Review (100% AI). Zapier Blog geprobeerd en weer verwijderd (bijna alles AI). Niet gekozen: Power Automate blog (weinig items), Mendix en Make (403), UiPath (feed te groot), Workato (timeout).

## Wijzigingen iteratie 7 (US-019: AWS Big Data eruit, automatiseringsfeed erbij)
Verwijderd: AWS Big Data Blog (diepteartikelen, 61-73% van Data). De bijbehorende items zijn bij de eerstvolgende ophaalronde automatisch uit data/nieuws.json verwijderd (bron staat niet meer in de config).
Toegevoegd: **Microsoft Power Platform Blog (Power Automate)**, https://www.microsoft.com/en-us/power-platform/blog/feed/. Gratis, geen login, `robots_toegestaan` gaf True (2026-10-09, ook met de eigen User-Agent), voorwaarden niet juridisch beoordeeld (alleen titel, korte samenvatting en link). Gekozen omdat het de enige onderzochte werkende feed is die vooral over Power Automate, Power Pages en low-code/procesautomatisering gaat: van 10 items kregen 6 een categorie (4 Automatisering, 1 AI, 1 Data), in de echte ronde 6 nieuwe items. Het is Engelstalig: een Nederlandstalige feed over procesautomatisering bestaat niet vrij beschikbaar (zie hieronder). Geen headnieuws (productblog).
Onderzocht en afgevallen (2026-10-09):
- Nederlandstalig: Automatiseringgids (time-out, 2 URL-varianten), AG Connect, DataNews, Dutch IT Channel, Procesverbeteren.nl, Centric, Blue10, Rubix, Dutchcowboys, Microsoft Nederland nieuws (404/410), LowCode.nl en RPA-Nederland (SSL-certificaatfout), ZDNet NL (HTML in plaats van feed), Computable-rubriek automatisering en RPA-tag (feed leeg), Techzine-tag automatisering (403), Emerce-tag automatisering (feed werkt maar is algemeen/AI-columns, geen automatisering), Sogeti NL (werkt, 10 items, maar 3 van 10 kregen een categorie en alle drie AI), Marketingfacts en ICT Magazine (marketing resp. algemeen/AI), ITdaily (Belgisch, algemeen, niet automatisering).
- Engelstalig: Zapier Blog (werkt, maar 12 van 25 AI), Workato (werkt, 6 items; marketingachtig vendor-PR, 3 van 6 categorie), Mendix en Make (403), OutSystems, Appian, UiPath, Tray, Bonita, Flowable, Kissflow, Process Excellence Network, RPA Today, Nintex, Pipedream, BPM.com (404 of geen feed), n8n community-forum (supportvragen, geen nieuws).
Resultaat: 10 feeds (6 EN, 4 NL), 3 BI-feeds, 4 NL-headnieuwsfeeds. Meetpunten na echte ophaalronde 2026-10-09 (87 items opgeslagen en getoond): zie de bouwersrapportage; BI 37%, AI 36%, Automatisering 22%, Data 6%.
