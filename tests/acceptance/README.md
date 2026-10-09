# Acceptatiesuite (Tester)

Geautomatiseerde tests voor de acceptatiecriteria uit `docs/BACKLOG.md`. Beheerd door de Tester.

## Draaien
Vanuit de projectmap, één commando (Python 3.10+, geen installatie nodig, geen internet nodig):
```
python -m unittest discover -s tests/acceptance -t tests/acceptance -v
```
- Sinds iteratie 7 (US-020) is er geen lokale app meer. De tests bouwen de statische site naar een tijdelijke map en draaien de ophaalcommando's tegen lokale testfeeds. Er hoeft niets vooraf gestart te zijn en er blijft niets draaien. Tests van de lokale app zijn geskipt met een reden (zie "Vervallen in iteratie 7" onderaan).
- De ophaal-tests (US-009/010/011) draaien `src/ophalen.py` tegen een lokale testserver op 127.0.0.1 (RSS, Atom, kapotte en trage feeds). Geen internet nodig.
- Het resultaat hangt NIET af van een aanwezige `data/nieuws.json`: de tests gebruiken een fixture in een tijdelijke map (`NIEUWS_BRON` bestaat niet meer). Alleen `TestEchtBestandInProject` leest het echte bestand, en wordt overgeslagen (NIET GETEST) als het ontbreekt.
- `test_US012_browser.py` gebruikt headless Microsoft Edge (`test_browser_layout.py` is vervallen) (`msedge.exe`, standaardlocatie) om 375 px en 1280 px te meten. Is Edge er niet, dan worden die tests overgeslagen en is de layout NIET GETEST. De layout-tests gebruiken de data die er staat (of voorbeelddata als `NIEUWS_BRON=voorbeeld` is gezet).
- Naamgeving: `US-003-c2` is in de code `test_US003_c2_...` (een koppelteken kan niet in een Python-naam).
- Gedeelde hulp (geen testmodule): `hulp_feeds.py` (lokale testserver, configuratie, subprocessen).

## Overzicht: criterium → testnaam

### Iteratie 1-2 (US-001 t/m US-008)
| Criterium | Testnaam | Bestand |
|---|---|---|
| US-001-c1 start met README-commando | `test_US001_c1_start_met_readme_commando` | test_acceptance.py |
| US-001-c2 navigatie: precies 3 items, juiste doelen | `test_US001_c2_navigatie_precies_drie_items_en_juiste_doelen` | test_acceptance.py |
| US-001-c3 actief menu-item gemarkeerd | `test_US001_c3_actief_menu_item_gemarkeerd` | test_acceptance.py |
| US-001-c4 leadsdeel: min. 10 leads, 2 per status, verzonnen (nieuwsdeel vervallen na US-009) | `test_US001_c4_voorbeelddata_minimum_en_verzonnen` | test_acceptance.py |
| US-001-c5 interfacelabels in het Nederlands (scope: labels, niet nieuwsinhoud) | `test_US001_c5_interface_is_nederlands` | test_acceptance.py |
| US-001-c6 375 px en 1280 px zonder horizontaal scrollen | `test_US001_c6_375_px_...`, `test_US001_c6_1280_px_...` | test_browser_layout.py |
| US-002-c1 nieuws nieuwste eerst, alle velden | `test_US002_c1_nieuws_nieuwste_eerst_met_alle_velden` | test_acceptance.py |
| US-002-c2 categoriefilter en juist aantal | `test_US002_c2_categoriefilter_toont_alleen_categorie_en_juist_aantal` | test_acceptance.py |
| US-002-c3 "Alle" toont weer alles | `test_US002_c3_alle_toont_weer_alles` | test_acceptance.py |
| US-002-c4 zoeken titel/samenvatting, hoofdletterongevoelig | `test_US002_c4_zoeken_titel_en_samenvatting_hoofdletterongevoelig` | test_acceptance.py |
| US-002-c5 "Geen nieuws gevonden", geen fout | `test_US002_c5_geen_resultaat_melding_zonder_fout` | test_acceptance.py |
| US-002-c6 titel opent bronlink in nieuw tabblad | `test_US002_c6_titel_opent_bronlink_in_nieuw_tabblad` | test_acceptance.py |
| US-003-c1 leads met alle velden | `test_US003_c1_leads_met_alle_velden` | test_acceptance.py |
| US-003-c2 statusfilter en juist aantal | `test_US003_c2_statusfilter_toont_alleen_status_en_juist_aantal` | test_acceptance.py |
| US-003-c3 "Alle" toont weer alle leads | `test_US003_c3_alle_toont_weer_alle_leads` | test_acceptance.py |
| US-003-c4 "Geen leads gevonden" bij leeg filter | `test_US003_c4_geen_leads_melding_bij_leeg_statusfilter` | test_acceptance.py (in-proces) |
| US-003-c5 statussen visueel te onderscheiden | `test_US003_c5_status_visueel_onderscheiden` | test_acceptance.py |
| US-003-c6 geen persoonsgegevens | `test_US003_c6_geen_persoonsgegevens` | test_acceptance.py (deels) |
| US-004-c1 5 nieuwste nieuws en 5 nieuwste leads | `test_US004_c1_vijf_nieuwste_nieuws_en_leads` | test_acceptance.py |
| US-004-c2 blokken: totaal + "Alles bekijken" | `test_US004_c2_blokken_tonen_totaal_en_alles_bekijken` | test_acceptance.py |
| US-004-c2 (layout) tegels 3 kolommen op 1280 px | `test_US004_c2_1280_px_overzicht_naast_elkaar_en_tegels_drie_kolommen` | test_browser_layout.py |
| US-004-c3 teller "Nieuwe leads" klopt | `test_US004_c3_teller_nieuwe_leads_klopt` | test_acceptance.py |
| US-004-c4 klik op item naar bronlink / leadsscherm | `test_US004_c4_klik_nieuws_naar_bronlink_en_lead_naar_leadsscherm` | test_acceptance.py |
| US-007-c1 favicon: geen 404, geen serverfout | `test_US007_c1_favicon_geen_404_en_geen_serverfout` | test_acceptance.py |
| US-007-c2 kleine letters geven hetzelfde filter | `test_US007_c2_kleine_letters_filter_gelijk_aan_juiste_schrijfwijze` | test_acceptance.py |
| US-007-c3 onbekend filter toont alles, "Alle" actief | `test_US007_c3_onbekende_filterwaarde_toont_alles_en_alle_actief` | test_acceptance.py |
| US-008-c1 kleuren op een plek (CSS-variabelen) | `test_US008_c1_kleuren_op_een_plek_gedefinieerd` | test_acceptance.py |
| US-008-c2 donkerblauw menu, grijze achtergrond, witte kaarten | `test_US008_c2_koptekst_achtergrond_en_witte_kaarten` | test_acceptance.py |
| US-008-c3 accentkleur alleen op links, actief menu, actief filter, knoppen | `test_US008_c3_accent_alleen_op_toegestane_plekken` | test_acceptance.py |
| US-008-c3 focusrand (stylesheet: kleur, contrast, geen accent) | `test_US008_c3_focusrand_in_koptekst_wit_op_donkerblauw_contrast`, `test_US008_c3_focusrand_overig_donkerblauw_op_lichte_achtergrond_contrast`, `test_US008_c3_focusrand_gebruikt_geen_accentkleur` | test_US008_c3_focusrand.py |
| US-008-c4 systeemfont, geen externe bestanden | `test_US008_c4_systeemfont_en_geen_externe_bestanden` | test_acceptance.py |
| US-008-c5 contrast minimaal 4,5:1 | `test_US008_c5_contrast_minimaal_4_5` | test_acceptance.py |
| US-008-c6 tellertegels alleen op startpagina | `test_US008_c6_tellertegels_alleen_op_startpagina` | test_acceptance.py |
| US-008-c7 je/jij, geen u/uw (scope: interfaceteksten) | `test_US008_c7_je_jij_geen_u_uw` | test_acceptance.py |
| US-008-c8 max-breedte 960-1200 px, gecentreerd | `test_US008_c8_breedte_en_responsief_in_stylesheet`, `test_US008_c8_1280_px_inhoud_gecentreerd_tussen_960_en_1200` | test_acceptance.py, test_browser_layout.py |
| US-008-c8 375 px: kaarten onder elkaar, geen scrollen | `test_US008_c8_375_px_kaarten_onder_elkaar_en_leesbaar` | test_browser_layout.py |

### Iteratie 3 (US-009, US-010, US-011)
| Criterium | Testnaam | Bestand |
|---|---|---|
| US-009-c1 8-10 feeds, min. 3 NL en 3 EN, naam/url/taal; time-out max 15 s | `test_US009_c1_config_8_tot_10_feeds_minstens_3_nl_en_met_naam_url_taal` | test_US009_feeds.py |
| US-009-c2 RSS 2.0 en Atom: titel, samenvatting, datum, bron, taal, link opgeslagen | `test_US009_c2_rss_en_atom_velden_opgeslagen` | test_US009_feeds.py |
| US-009-c3 HTML weg, samenvatting max 300 tekens, geen afbeeldingen/volle inhoud | `test_US009_c3_html_en_lange_tekst_platte_samenvatting_max_300` | test_US009_feeds.py |
| US-009-c4 zelfde link maar een keer | `test_US009_c4_zelfde_link_staat_maar_een_keer` | test_US009_feeds.py |
| US-009-c5 items ouder dan 60 dagen verwijderd | `test_US009_c5_items_ouder_dan_60_dagen_worden_verwijderd` | test_US009_feeds.py |
| US-009-c6 app toont opgehaalde items, nieuwste eerst, werkende link (zonder herstart) | `test_US009_c6_app_toont_opgehaalde_items_nieuwste_eerst_met_link` | test_US009_feeds.py |
| US-009-c7 per feed aantal items in de uitvoer (formaat; echte ronde: handmatig) | `test_US009_c7_uitvoer_toont_per_feed_aantal_items` | test_US009_feeds.py |
| US-009 (extra) robots.txt wordt gerespecteerd | `test_US009_extra_robots_txt_gerespecteerd` | test_US009_feeds.py |
| US-009-c7 (ronde 2, bevinding 1) bewaard telt na leeftijdsfilter, verouderd apart, uitvoer = JSON | `test_US009_c7_bewaard_na_leeftijdsfilter_verouderd_apart_en_consistent_met_json` | test_US009_ronde2.py |
| US-009-c7 (ronde 2, bevinding 1) feed met alleen verouderde items: OK met 0 bewaard | `test_US009_c7_feed_met_alleen_verouderde_items_is_ok_met_nul_bewaard` | test_US009_ronde2.py |
| US-009-c3 (ronde 2, bevinding 3) platte_tekst decodeert entiteiten niet dubbel (functieniveau) | `test_US009_c3_platte_tekst_decodeert_entiteiten_niet_dubbel` | test_US009_ronde2.py |
| US-009 (extra, ronde 2, bevinding 4) ongeldige of ontbrekende --config: exitcode 2, geen traceback | `test_US009_extra_ongeldige_config_geeft_nette_fout_exitcode_2` | test_US009_ronde2.py |
| US-010-c1 trefwoorden per categorie, NL en EN | `test_US010_c1_config_heeft_trefwoorden_nl_en_per_categorie` | test_US010_categorie.py |
| US-010-c2 categorie via hele woorden, hoofdletterongevoelig | `test_US010_c2_een_categorie_hoofdletterongevoelig_hele_woorden` | test_US010_categorie.py |
| US-010-c3 meeste treffers wint; gelijkspel AI, Automatisering, Data | `test_US010_c3_meeste_treffers_wint_en_gelijkspel_volgorde_ai_automatisering_data` | test_US010_categorie.py |
| US-010-c4 item zonder treffer niet opgeslagen | `test_US010_c4_item_zonder_treffer_wordt_niet_opgeslagen` | test_US010_categorie.py |
| US-010-c5 vaste testset (12 titels) krijgt verwachte categorie (it. 4 ronde 3: titel "Workflow-tools..." is "Workflow automation-tools...", zie wijzigingen) | `test_US010_c5_testset_titels_krijgen_verwachte_categorie` | test_US010_categorie.py |
| US-011-c1 onbereikbare, trage (time-out) en kapotte feed laten de rest doorgaan | `test_US011_c1_uitgevallen_feeds_laten_de_rest_doorgaan` | test_US011_foutafhandeling.py |
| US-011-c2 eerder opgeslagen items van mislukte feed blijven staan | `test_US011_c2_eerder_opgeslagen_items_van_mislukte_feed_blijven_staan` | test_US011_foutafhandeling.py |
| US-011-c3 per feed OK of FOUT met reden | `test_US011_c3_uitvoer_toont_ok_of_fout_met_reden_per_feed` | test_US011_foutafhandeling.py |
| US-011-c4 alle feeds mislukt: bestand ongewijzigd, foutcode; minstens 1 OK: code 0 | `test_US011_c4_alle_feeds_mislukt_laat_bestand_ongewijzigd_met_foutcode`, `test_US011_c4_alle_feeds_mislukt_zonder_bestaand_bestand_maakt_geen_bestand`, `test_US011_c4_minstens_een_geslaagde_feed_geeft_foutcode_0` | test_US011_foutafhandeling.py |
| US-011-c5 item zonder titel overgeslagen, zonder datum krijgt ophaaldatum | `test_US011_c5_item_zonder_titel_overgeslagen_zonder_datum_krijgt_ophaaldatum` | test_US011_foutafhandeling.py |
| Echte data (app): aantallen, volgorde, & in links geescapet, HTML in titel als tekst, tellers, zoeken, leeg/kapot bestand | `test_echte_data_*` (9 tests, klasse `TestEchteDataApp`) | test_echte_data_app.py |
| Echte data in project: `data/nieuws.json` geldig en veilig; app toont zelfde aantal en escaped links | `test_echte_data_bestand_in_project_is_geldig_en_veilig`, `test_echte_data_app_toont_zelfde_aantal_en_escaped_links_als_bestand` (NIET GETEST als bestand ontbreekt) | test_echte_data_app.py |

### Iteratie 4 (US-012, US-015, US-013 c2/c4/c5)
Alle tests in dit blok gebruiken een tijdelijke map (nooit `site/` of `data/` schrijven) en lokale fixture-data. De statische site wordt gebouwd met `src/bouw.py --uit <tijdelijke map>`. Gedeelde hulp: `hulp_statisch.py`.

| Criterium | Testnaam | Bestand |
|---|---|---|
| US-012-c1 bouwcommando maakt statische map zonder server-code; werkt via eenvoudige server | `test_US012_c1_bouwcommando_maakt_statische_map_zonder_server_code` | test_US012_statische_site.py |
| US-012-c2 navigatie precies Overzicht en Nieuws; geen leadsbestand | `test_US012_c2_navigatie_precies_overzicht_en_nieuws_op_elke_pagina`, `test_US012_c2_geen_leadsscherm_bestand` | test_US012_statische_site.py |
| US-012-c3 geen leadstatussen, leadscherm-elementen, verzonnen bedrijfsnamen of voorbeeldnieuws (toetst niet op losse "lead") | `test_US012_c3_geen_leadstatussen_of_leadscherm_in_bestanden`, `test_US012_c3_geen_verzonnen_bedrijfsnamen_uit_voorbeelddata`, `test_US012_c3_geen_voorbeeldnieuws_uit_app_data` | test_US012_statische_site.py |
| US-012-c4 nieuwsitem: bron, datum, samenvatting max 300, link; geen afbeeldingen | `test_US012_c4_nieuwsitem_toont_bron_datum_samenvatting_en_link`, `test_US012_c4_samenvattingen_zijn_afgekapt_met_puntjes_en_max_300`, `test_US012_c4_fixture_*`, `test_US012_c4_echte_data_*` | test_US012_statische_site.py |
| US-012-c5 voet: "Laatst bijgewerkt" (Nederlandse tijd), bronvermelding, bronnenlijst | `test_US012_c5_voet_laatst_bijgewerkt_bronvermelding_en_bronnenlijst`, `test_US012_c5_fixture_tijd_in_nederlandse_tijd` | test_US012_statische_site.py |
| US-012-c5 bronnenlijst bevat ALLE bronnen die op de site getoond worden (it. 4 ronde 3; bron van een item die niet meer in config staat) | `test_US012_c5_fixture_bron_die_niet_in_config_staat_staat_toch_op_bronnenlijst`, `test_US012_c5_echte_data_elke_getoonde_bron_staat_op_bronnenlijst` | test_US012_c5_bronnenlijst.py |
| US-012-c6 startpagina: tellers per categorie en 5 nieuwste items | `test_US012_c6_startpagina_tellers_per_categorie_kloppen_met_data`, `test_US012_c6_startpagina_toont_vijf_nieuwste_items` (vaknieuws, US-018 c8 aangepast), `test_US012_c6_weggelaten_nieuwere_items_uitzonderingen_positief_en_negatief`, `test_US012_c6_echte_data_tellers_kloppen` (statisch) en `test_US012_c6_startpagina_tellers_in_browser` (browser) | test_US012_statische_site.py, test_US012_browser.py |
| US-012-c7 filter en zoeken als US-002 c2-c5 en US-007 c2-c3 (in echte browser) | `test_US012_c7_categoriefilter_*`, `test_US012_c7_alle_toont_weer_alles_via_chip`, `test_US012_c7_zoeken_*`, `test_US012_c7_combinatie_*`, `test_US012_c7_speciale_tekens_*`, `test_US012_c7_lege_*` | test_US012_browser.py |
| US-012 bouwen zonder data: FOUT, exitcode 1, niets gepubliceerd; lege items en kapot bestand idem | `test_US012_bouw_zonder_data_geeft_fout_exitcode_1_en_publiceert_niets`, `test_US012_bouw_met_lege_items_geeft_fout_exitcode_1`, `test_US012_bouw_met_kapot_databestand_geeft_fout_exitcode_1` | test_US012_statische_site.py |
| US-012 links relatief, werken onder /<repo>/, geen externe bestanden | `test_US012_links_relatief_en_geen_externe_bestanden`, `test_US012_links_blijven_binnen_het_repo_pad_op_github_pages` | test_US012_statische_site.py |
| US-002 c1 (statisch) nieuwste eerst, alle velden | `test_US002_c1_statisch_nieuws_nieuwste_eerst_met_alle_velden` | test_statisch_regressie.py |
| US-002 c5 "Geen nieuws gevonden", geen fout (statisch) | `test_US002_c5_geen_resultaat_melding_zonder_fout` | test_US012_browser.py |
| US-002 c6 titel opent bronlink in nieuw tabblad (statisch) | `test_US002_c6_titel_opent_bronlink_in_nieuw_tabblad_statisch` | test_US012_browser.py |
| US-001 c2 (statisch) precies Overzicht en Nieuws | `test_US001_c2_statisch_navigatie_precies_overzicht_en_nieuws` | test_US012_browser.py |
| US-001 c3 (statisch) actief menu-item gemarkeerd | `test_US001_c3_statisch_actief_menu_item_gemarkeerd` | test_statisch_regressie.py |
| US-001 c5 (statisch) interfacelabels Nederlands | `test_US001_c5_statisch_interface_is_nederlands` | test_statisch_regressie.py |
| US-001 c6 (statisch) 375 en 1280 px zonder horizontaal scrollen, navigatie in beeld | `test_US001_c6_statisch_375_px_...`, `test_US001_c6_statisch_1280_px_...` | test_US012_browser.py |
| US-007 c1 (statisch) favicon geen 404 | `test_US007_c1_statisch_favicon_geen_404` | test_US012_statische_site.py |
| US-007 c2 kleine letters = juiste schrijfwijze (statisch) | `test_US007_c2_kleine_letters_categorie_gelijk_aan_juiste_schrijfwijze` | test_US012_browser.py |
| US-007 c3 onbekende filterwaarde toont alles, "Alle" actief (statisch) | `test_US007_c3_onbekende_filterwaarde_toont_alles_en_alle_actief` | test_US012_browser.py |
| US-008 c1-c8 (statisch): kleuren, achtergrond/kaarten, accent, font, contrast, tegels, je/jij, breedte | `test_US008_c1_statisch_...` t/m `test_US008_c8_statisch_breedte_...` (stylesheet en pagina's) | test_statisch_regressie.py |
| US-008 c8 (statisch, browser) 1280 px gecentreerd 960-1200; 375 px kaarten onder elkaar | `test_US008_c8_statisch_1280_px_...`, `test_US008_c8_statisch_375_px_...` | test_US012_browser.py |
| US-004 c2 (statisch) tegels drie kolommen op 1280 px | `test_US004_c2_statisch_1280_px_tegels_drie_kolommen` | test_US012_browser.py |
| US-015-c1 uitsluitingstermen in config (Data Master); uitgesloten tekst telt niet mee | `test_US015_c1_uitsluitingstermen_in_config_met_data_master`, `test_US015_c1_uitgesloten_tekst_telt_niet_mee_als_treffer` | test_US015_categorie.py |
| US-015-c2 Asustor-voorbeeld krijgt niet categorie Data | `test_US015_c2_firmware_met_data_master_krijgt_niet_categorie_data` | test_US015_categorie.py |
| US-015-c3 minstens 15 trefwoorden per categorie, NL en EN | `test_US015_c3_minstens_15_trefwoorden_per_categorie_nl_en` | test_US015_categorie.py |
| US-015-c4 vaste testset (26 titels: 25 met verwachte categorie, min. 5 per categorie, min. 3 echte; 1 zonder categorie) krijgt verwachte categorie | `test_US015_c4_vaste_testset_minstens_20_titels_min_5_per_categorie_en_3_echte`, `test_US015_c4_elke_testtitel_krijgt_de_verwachte_categorie` | test_US015_categorie.py |
| US-013-c2 cron dagelijks 04:00 UTC (06:00 NL zomertijd); handmatig; ophalen dan bouwen; publiceren na bouwen; geen secrets, contents: write | `test_US013_c2_*` | test_US013_workflow.py |
| US-013-c4 geheimenscan van alle tekstbestanden in de projectmap; geen geheim in feed-URLs | `test_US013_c4_geen_wachtwoorden_tokens_of_sleutels_in_repository`, `test_US013_c4_geen_geheim_in_configuratie_of_data_urls`, `test_US013_c4_mutatie_sleutelpatroon_vangt_echte_sleutels_en_negeert_slug` (it. 4 ronde 3) | test_US013_workflow.py |
| US-013-c5 README: feeds beheren en job handmatig starten; stappen online zetten | `test_US013_c5_readme_*` | test_US013_workflow.py |
| US-013-c5 README: letterlijke voorbeeldregel van een feed staat exact in config/feeds.json (it. 4 ronde 2) | `test_US013_c5_readme_bevat_letterlijke_feedregel_die_in_config_staat`, `test_US013_c5_readme_beschrijft_feed_toevoegen_verwijderen_en_handmatig_starten` | test_US013_c5_readme.py |
| US-012-c8 (browser, 375 px) placeholder "Zoek in nieuws" past volledig in het zoekveld (iframe 375 px, canvas-meting) | `test_US012_c8_placeholder_volledig_zichtbaar_op_375_px` | test_US012_c8_placeholder.py |
| US-012 aanvullend (KLEIN 6): eigen 404.html in de gebouwde site, Nederlands, geen externe bestanden | `test_US012_extra_404_html_bestaat_en_is_nederlands`, `test_US012_extra_404_html_laadt_niets_van_buiten` | test_US012_extra_404.py |
| US-015-c6 echte titels (ronde 8 okt) krijgen NIET de genoemde categorie; SageMaker HyperPod Spaces = AI; losse "data" telt niet | `test_US015_c6_echte_titels_niet_in_de_verkeerde_categorie`, `test_US015_c6_manage_sagemaker_hyperpod_spaces_is_ai_en_niet_data`, `test_US015_c6_losse_data_telt_niet_meer_als_categorie` | test_US015_categorie.py |
| US-015-c7 extra automatisering-feed (n8n) in config, in docs/decisions/2026-10-08-nieuwsfeeds.md en op bronnen.html; feedaantal 8-10 | `test_US015_c7_config_bevat_extra_automatisering_feed_zonder_login`, `test_US015_c7_feedaantal_binnen_8_tot_10_en_min_3_per_taal`, `test_US015_c7_feed_staat_in_feedbesluit`, `test_US015_c7_feed_staat_op_bronnen_html` | test_US015_c7_feeds.py |
| US-015-c8 Automatisering minstens 8 items na een echte ronde en filter niet leeg | NIET AUTOMATISCH (live feeds, niet deterministisch); handmatig met een ophaalronde naar een tijdelijke map, zie testrapport ronde 2 | - |
| US-015-c9 Archestra-titel (echte samenvatting) niet Automatisering; los "workflow(s)" telt niet; "workflow automation", "workflowautomatisering", "workflow-automatisering" wel (elk een testtitel) | `test_US015_c9_archestra_titel_met_echte_samenvatting_is_niet_automatisering`, `test_US015_c9_los_workflow_of_workflows_telt_niet_als_automatisering`, `test_US015_c9_workflow_automation_telt_als_automatisering`, `test_US015_c9_workflowautomatisering_telt_als_automatisering`, `test_US015_c9_workflow_automatisering_met_koppelteken_telt_als_automatisering` | test_US015_categorie.py |
| US-015-c10 config bevat minstens 10 specifieke Data-termen; vaste testset bevat minstens 5 extra titels, elk via een andere term | `test_US015_c10_config_bevat_minstens_10_specifieke_data_termen`, `test_US015_c10_losse_data_is_niet_in_config_als_data_term`, `test_US015_c10_minstens_5_extra_titels_elk_via_andere_specifieke_term_data` | test_US015_categorie.py |
| US-015-c11 minstens 1 extra gratis data-feed (AWS Big Data Blog) in config, bronnenlijst en feedbesluit; max 10 feeds, min 3 NL/3 EN | `test_US015_c11_config_bevat_gratis_datafeed_zonder_login`, `test_US015_c11_feedaantal_blijft_max_10_en_min_3_per_taal`, `test_US015_c11_datafeed_staat_in_feedbesluit`, `test_US015_c11_datafeed_staat_op_bronnen_html` | test_US015_c11_datafeed.py |
| US-015-c12 per categorie en per feed na een echte ronde: Data >= 8, Automatisering >= 8, geen feed > 60% van Data of Automatisering | NIET AUTOMATISCH (live feeds); handmatig met `python src/ophalen.py --uitvoer <tijdelijke map>/nieuws.json`, tellen per categorie en per feed. Zie testrapport it. 4 ronde 3 | - |

Wijzigingen aan bestaande tests in iteratie 4, ronde 1: **geen**. Iteratie 4, ronde 3 (fixronde 2 besluit): zie hieronder. Iteratie 4, ronde 2 (fixronde, tests van het gewijzigde criterium, zie hieronder). De lokale-app-tests (US-001 c2/c4 leadsdeel, US-003, US-004) blijven gelden voor `src/app.py`, niet voor de statische site.

## Wijzigingen aan de tests in iteratie 4, ronde 3 (na fixronde 2)
Aanleiding: `docs/decisions/2026-10-08-categorie-fixronde2-it4.md`. Niets verzwakt: dezelfde verwachte categorieen, alleen de vorm van de term of de testtitel is aangepast.
1. `test_US010_c5_testset_titels_krijgen_verwachte_categorie`: de titel "Workflow-tools maken processen voorspelbaar" (verwacht Automatisering) is "Workflow automation-tools maken processen voorspelbaar". Reden: los "workflow" vervalt (US-015 c9); de verwachte categorie blijft Automatisering via de specifieke vorm.
2. `test_US013_c4_geen_wachtwoorden_tokens_of_sleutels_in_repository`: het patroon voor "sk-" krijgt een grens: `(?<![A-Za-z0-9_/-])sk-...`. Reden: de URL-slug "...amazon-msk-with-next-generation-protocol" gaf een vals alarm. Nieuwe mutatietest `test_US013_c4_mutatie_sleutelpatroon_vangt_echte_sleutels_en_negeert_slug` toont dat realistische sleutels (OPENAI_API_KEY=sk-..., "sk-ant-...", Bearer sk-...) nog gevangen worden. Bekende beperking: een sleutel die direct na een letter, cijfer, "_", "/" of "-" staat (bijv. "KEY-sk-...") wordt niet gevangen.
3. Nieuw: `test_US015_c9_*` (5 tests, incl. Archestra-titel met de echte samenvatting), `test_US015_c10_*` (3 tests; de vaste testset kreeg 6 extra Data-titels, elk via een andere term), `test_US015_c11_datafeed.py` (4 tests), `test_US012_c5_bronnenlijst.py` (2 tests; zie hieronder).
4. Nieuw, NIET GESLAAGD bij oplevering: `test_US012_c5_echte_data_elke_getoonde_bron_staat_op_bronnenlijst` en `test_US012_c5_fixture_bron_die_niet_in_config_staat_staat_toch_op_bronnenlijst`. Oorzaak: bronnen.html wordt alleen uit config/feeds.json gebouwd (src/bouw.py), terwijl items 60 dagen blijven staan na het verwijderen van hun feed. Dat is een echte bevinding (BLOKKEREND), geen testfout; de test is niet aangepast.
5. c12 is niet automatisch (live feeds); de handmatige ronde staat in het testrapport.

## Wijzigingen aan de tests in iteratie 4, ronde 2 (fixronde categorie-indeling)
Aanleiding: `docs/decisions/2026-10-08-categorie-fixronde-it4.md`: het losse trefwoord "data" vervalt (alleen specifieke vormen tellen). Drie tests verwachtten het losse woord; ze zijn aangepast naar een specifieke Data-term. Er is niets verzwakt: dezelfde verwachte categorie en dezelfde test-opzet.
1. `test_US010_c2_een_categorie_hoofdletterongevoelig_hele_woorden`: `"DATA-opslag"` is `"DATABASE-opslag"` (verwacht Data, nu via `database*`).
2. `test_US010_c3_meeste_treffers_wint_en_gelijkspel_volgorde_ai_automatisering_data`: `"data data data AI"` is `"database database database AI"` (3 Data tegen 1 AI). De gelijkspelregels Automatisering/Data gebruiken nu `databases`/`database`, zodat het gelijkspel echt getest blijft (met het losse "data" was dat geen gelijkspel meer; de test was dan stil verzwakt).
3. `test_US015_c1_uitgesloten_tekst_telt_niet_mee_als_treffer`: `"data"` in de samenvatting is `"database"` (verwacht Data).
Nieuw: `test_US012_c8_placeholder_*` (browser), `test_US013_c5_readme.py`, `test_US015_c7_feeds.py`, `test_US012_extra_404.py`, en in `test_US015_categorie.py` de klasse `TestUS015Fixronde` (US-015 c6, met de vier echte titels en de SageMaker-titel). US-015 c8 is niet automatisch (zie beperkingen).

Browsertests (`test_US012_browser.py`): de Edge-aanroep gebruikt dezelfde werkwijze als `test_browser_layout.py` (een kleine proxy voegt een meetscript toe aan de pagina; Edge `--dump-dom` levert in deze omgeving geen uitvoer). Filter en zoeken worden getest via de URL-parameters (`?categorie=`, `?q=`) die de chips, de Alle-link en het zoekformulier gebruiken; het klikken zelf is niet geautomatiseerd.

Niet in de suite: US-005 en US-006 (status TODO), US-014 (nog niet in een iteratie). US-013 c1 (site bereikbaar op github.io) en c3 (Laatst bijgewerkt op de live site) zijn niet lokaal te testen en wachten op het hosting-account van Stef.

## Wijzigingen aan de tests van iteratie 1-2 (iteratie 3, ronde 1)
Deze wijzigingen verzwakken geen criterium; de reden staat erbij.
1. Alle tests van US-001 t/m US-008 in `test_acceptance.py` forceren `NIEUWS_BRON=voorbeeld` (`setUpModule`). De verwachte waarden (18 nieuwsitems, 12 leads, enz.) zijn ongewijzigd.
2. US-001-c4: het nieuwsdeel is verwijderd (backlog: vervalt na US-009). Het leadsdeel blijft.
3. US-001-c5 en US-008-c7: de controle op Engelse woorden en u/uw gaat over interfaceteksten (labels, knoppen, menu's), niet over nieuwstitels of samenvattingen uit bronnen (`interface_tekst`). Zonder die scope faalde c5 op een Engels woord in een echte nieuwstitel.
4. US-004-c4: de href wordt ontgeescapet voor de vergelijking (in HTML staat `&` als `&amp;`). Dit was een fout in de test, die alleen bij echte data zichtbaar werd.

## Iteratie 3, ronde 2
Bestaande tests ongewijzigd. Nieuw: `test_US009_ronde2.py` (gerichte controles na fixronde 1, zie tabel hierboven). Bevinding 3 is op functieniveau getest; de volledige pijplijn decodeert een titel met `&amp;amp;` nog steeds eenmaal extra (zie testrapport ronde 2).

## Beperkingen en handmatig te controleren
- **US-015-c5 en c8 (aantallen per categorie na een echte ophaalronde):** informatief en live; niet als deterministische test. Handmatig: `python src/ophalen.py --uitvoer <tijdelijke map>/nieuws.json` en tel de categorieen. Ronde 2 (it. 4): zie testrapport.
- **US-012-c8 (placeholder):** de test meet met Edge en canvas-tekstbreedte in een iframe van 375 px. Zonder Edge: NIET GETEST.
- **US-001-c1 (browser opent automatisch):** de test start de app met `GEEN_BROWSER=1`. Dat de browser zelf opent, is niet geautomatiseerd: handmatig door Stef.
- **US-003-c4:** met de huidige voorbeelddata is een leeg statusfilter via de UI niet te bereiken. De test controleert de melding daarom in-proces.
- **US-003-c6:** de test controleert op e-mail, telefoonachtige nummers, aanhefs- en URL-patronen. Of een bedrijfsnaam een persoonsnaam is, is niet automatisch te beoordelen.
- **US-008-c8 (375/1280 px):** gemeten met headless Edge in een iframe van 375 px.
- **Focusrand in de browser (US-008-c3):** de suite controleert de stylesheet. Zichtbaarheid is handmatig gecontroleerd (iteratie 2).
- **Visueel totaalbeeld** ("Stijl en uitstraling" in VISION.md): niet geautomatiseerd; Stef beoordeelt dit.
- **US-009-c7 (echte ophaalronde):** de suite controleert het formaat van de uitvoer. De echte ronde met de echte feeds is handmatig uitgevoerd en staat in het testrapport.
- **US-011-c1 time-out:** de test gebruikt een time-out van 1 s (zodat de test snel is). Het project-maximum van 15 s wordt in US-009-c1 gecontroleerd.
- **Windows en gesloten poorten:** een gesloten localhost-poort geeft op deze machine na ca. 1-2 s een connect-fout; de test checkt op FOUT, niet op de exacte reden.
- **US-016 c6 (feed-aandeel per categorie na een echte ophaalronde) en US-017 c5 (weigeraantallen per feed):** meldpunten, niet automatisch (live feeds). Handmatig met `python src/ophalen.py --uitvoer <tijdelijke map>/nieuws.json`; de uitkomst staat in het testrapport. US-017 c5 wordt wel automatisch gecontroleerd op het uitvoerformaat (`test_US017_c5_...`).
- **US-013 c1 en c3** (site op github.io, Laatst bijgewerkt op de live site): NIET GETEST, wachten op het hosting-account van Stef.
- **US-016 c7 / US-018 c6 (browser):** headless Edge; zonder Edge: NIET GETEST. Het visuele totaalbeeld staat in het testrapport (screenshots).

## Iteratie 6 (US-016, US-017, US-018) en iteratie 5 (online zetten voorbereiden)
Nieuwe bestanden: `test_US016_mix.py`, `test_US017_weigerlijst.py`, `test_US018_uitgelicht.py`, `test_iteratie5_online.py`, gedeelde hulp `hulp_browser.py`. Fixtures zijn lokaal; de statische site wordt met `--vandaag 2026-10-08` gebouwd (vaste peildatum voor Uitgelicht).

| Criterium | Testnaam | Bestand |
|---|---|---|
| US-016 c1 vier categorieen BI, Data, Automatisering, AI | `test_US016_c1_precies_vier_categorieen_bi_data_automatisering_ai` | test_US016_mix.py |
| US-016 c1 minstens 15 trefwoorden per categorie, NL en EN | `test_US016_c1_minstens_15_trefwoorden_per_categorie_nl_en` | test_US016_mix.py |
| US-016 c1 verplichte termen BI, Data, Automatisering | `test_US016_c1_bi_data_automatisering_bevatten_verplichte_termen` | test_US016_mix.py |
| US-016 c2 gelijkspel-volgorde BI, Data, Automatisering, AI (6 titels, incl. BI/AI) | `test_US016_c2_gelijkspel_bi_en_andere_volgorde_bi_data_automatisering_ai`, `test_US016_c2_volgorde_in_config_is_bi_data_automatisering_ai` | test_US016_mix.py |
| US-016 c3 AI alleen in titel telt | `test_US016_c3_ai_alleen_in_samenvatting_telt_niet_mee`, `test_US016_c3_ai_in_titel_telt_en_samenvatting_van_bi_telt_wel`, `test_US016_c3_item_met_ai_alleen_in_samenvatting_wordt_niet_opgeslagen` | test_US016_mix.py |
| US-016 c4 80 AI + 20 overig -> 13 AI + 20 (mix, site, tellers, Overzicht) | `test_US016_c4_mix_80_ai_en_20_overig_geeft_13_ai_en_20_overig`, `test_US016_c4_site_nieuws_tellers_en_overzicht_tonen_alleen_de_getoonde_items` | test_US016_mix.py |
| US-016 c4 AI-aandeel nooit boven 40% en maximaal (0-200 overige items, exact gerekend) | `test_US016_c4_ai_aandeel_nooit_boven_40_procent_en_maximaal` | test_US016_mix.py |
| US-016 c4 lokale app gebruikt hetzelfde plafond | `test_US016_c4_lokale_app_gebruikt_hetzelfde_plafond` | test_US016_mix.py |
| US-016 c4 echte data: AI-aandeel op de site hooguit 40% (alleen-lezen) | `test_US016_c4_echte_data_ai_aandeel_op_site_hooguit_40_procent` | test_US016_mix.py |
| US-016 c5 max 10 feeds, min 3 NL en 3 EN | `test_US016_c5_max_10_feeds_minstens_3_nl_en` | test_US016_mix.py |
| US-016 c5 min 2 BI-feeds en 2 algemene NL-bronnen | `test_US016_c5_minstens_2_bi_feeds_en_2_algemene_nl_bronnen` | test_US016_mix.py |
| US-016 c5 elke feed in feedbesluit met robots/gratis/geen login | `test_US016_c5_elke_feed_in_feedbesluit_met_robots_gratis_en_geen_login` | test_US016_mix.py |
| US-016 c5 elke feed op de bronnenlijst | `test_US016_c5_elke_feed_staat_op_de_bronnenlijst` | test_US016_mix.py |
| US-016 c6 meldpunt (feed-aandeel) | NIET AUTOMATISCH (live feeds); testrapport | - |
| US-015 c12 vervangen door US-016 c6 (backlog-tekst) | `test_US015_c12_is_vervangen_door_US016_c6_in_backlog` | test_US016_mix.py |
| US-016 c7 filterknoppen Alle, BI, Data, Automatisering, AI (Nieuws) en tegels (Overzicht) | `test_US016_c7_nieuws_heeft_filterknoppen_alle_bi_data_automatisering_ai`, `test_US016_c7_overzicht_heeft_tegels_bi_data_automatisering_ai` | test_US016_mix.py |
| US-016 c7 categorie=bi (hoofdletterongevoelig), browser: aantal, tellers, 375/1280 px | `test_US016_c7_categorie_bi_in_url_filtert_en_is_hoofdletterongevoelig`, `test_US016_c7_browser_*` (3 tests) | test_US016_mix.py, hulp_browser.py |
| US-016 c7 lokale app: BI-filter en chip | `test_US016_c7_lokale_app_categorie_bi_filter_en_chip` | test_US018_uitgelicht.py |
| US-016 c8 los "gegevens" is geen Data-trefwoord; samenstellingen wel | `test_US016_c8_los_gegevens_is_geen_data_trefwoord` | test_US016_mix.py |
| US-016 c8 drie NOS-titels met echte samenvatting krijgen geen Data | `test_US016_c8_drie_nos_titels_met_echte_samenvatting_krijgen_geen_data` | test_US016_mix.py |
| US-016 c9 ongeldige datum: item overgeslagen met melding (titel/link), bouw exitcode 0 | `test_US016_c9_ongeldige_datum_wordt_overgeslagen_met_melding_bouw_gaat_door` | test_US016_mix.py |
| US-016 c10 alleen AI-items: exitcode 1, melding noemt AI-plafond (niet "bevat geen nieuwsitems") | `test_US016_c10_alleen_ai_items_geeft_exitcode_1_en_melding_ai_plafond` | test_US016_mix.py |
| US-017 c1 weigerlijst met verplichte termen (titel) en promotietermen (samenvatting) | `test_US017_c1_weigerlijst_bevat_verplichte_termen` | test_US017_weigerlijst.py |
| US-017 c2 weigerterm in titel (hele woorden, hoofdletterongevoelig) | `test_US017_c2_weigerterm_in_titel_wordt_niet_opgeslagen_ook_met_trefwoord`, `test_US017_c2_hele_woorden_en_geen_valse_weigering` | test_US017_weigerlijst.py |
| US-017 c3 promotietermen alleen in samenvatting worden geweigerd | `test_US017_c3_promotieterm_alleen_in_samenvatting_wordt_geweigerd` | test_US017_weigerlijst.py |
| US-017 c4 vaste testset (5 weigeren, 7 toelaten na fixronde 1; deal/dealer) | `test_US017_c4_vaste_testset_klopt_voor_elke_titel`, `test_US017_c4_overnametitel_met_deal_en_dealer_worden_toegelaten` | test_US017_weigerlijst.py |
| US-017 c5 uitvoer per feed met geweigerd-aantal en voorbeeldtitels (formaat) | `test_US017_c5_ophaaluitvoer_meldt_geweigerd_per_feed_met_voorbeeldtitels` | test_US017_weigerlijst.py |
| US-017 c5 dubbele geweigerde link in een feed telt een keer (fixronde 1) | `test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer` | test_US017_weigerlijst.py |
| US-017 c5 echte aantallen per feed | NIET AUTOMATISCH; testrapport | - |
| US-017 c6 weigerlijst bevat evenement- en vendor-PR-patronen (incl. regex "nog <getal> ... tot") | `test_US017_c6_configuratie_bevat_evenement_en_vendor_pr_patronen` | test_US017_weigerlijst.py |
| US-017 c6 evenementpromo en vendor-PR (4 titels) worden geweigerd | `test_US017_c6_evenementpromo_en_vendor_pr_worden_geweigerd` | test_US017_weigerlijst.py |
| US-017 c6 overname, Power BI/Fabric-release, Gartner-titel zonder patroon worden toegelaten | `test_US017_c6_overname_productrelease_en_gartner_titel_worden_toegelaten` | test_US017_weigerlijst.py |
| US-017 c7 uitzonderingslijst bevat zakelijke combinaties | `test_US017_c7_uitzonderingslijst_bevat_zakelijke_combinaties` | test_US017_weigerlijst.py |
| US-017 c7 vaste testset laat "operational review" en "analogy game" toe | `test_US017_c7_vaste_testset_laat_zakelijke_combinaties_toe` | test_US017_weigerlijst.py |
| US-017 c7 "Review: ..." en "games" blijven geweigerd; tekst onder uitzondering telt niet | `test_US017_c7_review_en_games_blijven_geweigerd` | test_US017_weigerlijst.py |
| US-018 c1 min 2 algemene NL-headnieuws-feeds; relevantietermen compleet | `test_US018_c1_minstens_2_algemene_nl_headnieuws_feeds`, `test_US018_c1_deux_relevantietermen_compleet` | test_US018_uitgelicht.py |
| US-018 c2 Uitgelicht boven tegels, max 5, laatste 3 dagen, hooguit 2 AI, velden | `test_US018_c2_uitgelicht_staat_boven_de_tellertegels`, `test_US018_c2_max_5_items_uit_laatste_3_dagen_hooguit_2_ai`, `test_US018_c2_uitgelicht_item_toont_titel_link_bron_datum_categorie` | test_US018_uitgelicht.py |
| US-018 c2 lokale app | `test_US018_c2_lokale_app_uitgelicht_boven_tegels_en_juiste_items` | test_US018_uitgelicht.py |
| US-018 c3 scoreregel: volgorde (vaste titels), term telt een keer, titel+samenvatting, hele woorden; regel in README | `test_US018_c3_volgorde_hoogste_score_eerst_bij_gelijk_nieuwste_eerst`, `test_US018_c3_term_telt_een_keer_per_item_en_headnieuws_is_2`, `test_US018_c3_score_telt_titel_en_samenvatting_en_hele_woorden`, `test_US018_c3_scoreregel_staat_in_readme` | test_US018_uitgelicht.py |
| US-018 c4 minder dan 5 items; 0 items: "Nog geen uitgelicht nieuws" | `test_US018_c4_minder_dan_5_items_toont_alleen_de_beschikbare`, `test_US018_c4_nul_items_toont_nog_geen_uitgelicht_nieuws_zonder_fout`, `test_US018_c4_lokale_app_nul_items_nog_geen_uitgelicht_nieuws` | test_US018_uitgelicht.py |
| US-018 c5 vaknieuws = 5 nieuwste die niet in Uitgelicht staan (statisch en lokaal) | `test_US018_c5_vaknieuws_is_de_5_nieuwste_die_niet_in_uitgelicht_staan`, `test_US018_c5_lokale_app_vaknieuws_is_de_5_nieuwste_niet_in_uitgelicht` | test_US018_uitgelicht.py |
| US-018 c6 startpagina 375/1280 px zonder horizontaal scrollen; geen console-fouten | `test_US018_c6_startpagina_375_px_en_1280_px_geen_horizontaal_scrollen`, `test_US018_c6_startpagina_zonder_console_fouten` | test_US018_uitgelicht.py |
| US-016 c11 `--vandaag 2026-13-45` (en 2026-02-30): Nederlandse melding met JJJJ-MM-DD, exitcode 1, geen traceback; geldige datum bouwt | `test_US016_c11_ongeldige_maand_geeft_nederlandse_melding_exitcode_1`, `test_US016_c11_ongeldige_dag_geeft_dezelfde_nederlandse_melding`, `test_US016_c11_positieve_controle_geldige_peildatum_bouwt` | test_US016_c11_peildatum.py |
| US-018 c7 evenementtermen: niet in Uitgelicht/Vaknieuws, wel op Nieuws; "Eventueel" geen vals-positief; echte Techzine-titel (alleen-lezen op data/nieuws.json, NIET GETEST als de titel ontbreekt) | `test_US018_c7_evenementaankondiging_niet_in_uitgelicht_of_vaknieuws`, `test_US018_c7_evenementaankondiging_blijft_op_nieuws`, `test_US018_c7_gewoon_nieuws_blijft_in_uitgelicht`, `test_US018_c7_eventueel_is_geen_evenementterm`, `test_US018_c7_echte_techzine_titel_alleen_op_nieuws_als_die_in_de_data_staat` | test_US018_c7_c8_evenement_kort_ai.py |
| US-018 c8 Vaknieuws hooguit 2 AI, aangevuld met niet-AI (exacte volgorde); "Kort:" niet in Uitgelicht/Vaknieuws, wel op Nieuws | `test_US018_c8_vaknieuws_hooguit_2_ai_en_aangevuld_met_niet_ai`, `test_US018_c8_vaknieuws_exacte_volgorde`, `test_US018_c8_kort_titel_niet_in_uitgelicht_of_vaknieuws`, `test_US018_c8_kort_titel_blijft_op_nieuws`, `test_US018_c8_uitgelicht_hooguit_2_ai` | test_US018_c7_c8_evenement_kort_ai.py |
| It. 5 .gitignore bevat veiligheidsregels | `test_IT5_gitignore_bevat_veiligheidsregels` | test_iteratie5_online.py |
| It. 5 src/veilig_check.py eindigt met exitcode 0 | `test_IT5_veilig_check_eindigt_met_exitcode_0` | test_iteratie5_online.py |
| It. 5 workflow: cron, handmatig, rechten, geen eigen geheimen, volgorde, artefact | `test_IT5_c2_cron_dagelijks_0400_utc_is_0600_nl`, `test_IT5_c2_handmatig_starten_mogelijk`, `test_IT5_rechten_zijn_minimaal`, `test_IT5_c4_geen_eigen_geheimen_in_workflow`, `test_IT5_volgorde_ophalen_bouwen_publiceren`, `test_IT5_pad_van_artefact_is_site_en_data_alleen_bij_wijziging`, `test_IT5_naam_van_workflow_staat_in_readme` | test_iteratie5_online.py |
| It. 5 verse checkout: geen data / leeg data: geen crash, niets gepubliceerd; met werkende feed: geen voorbeelddata | `test_IT5_verse_checkout_zonder_data_geen_crash_en_niets_gepubliceerd`, `test_IT5_leeg_databestand_geen_crash_en_geen_publicatie`, `test_IT5_ontbrekend_bestand_met_werkende_feed_publiceert_alleen_echte_items` | test_iteratie5_online.py |
| It. 5 subpad /<repo>/: pagina's, assets en alle interne links | `test_IT5_subpad_pagina_en_assets_laden_onder_repo_pad`, `test_IT5_subpad_alle_interne_links_blijven_onder_repo_en_bestaan`, `test_IT5_subpad_zoekfilter_in_url_werkt_onder_repo_pad` | test_iteratie5_online.py |
| It. 5 README stappen A-E, stopinstructie, veilig_check-eindregel, geen lokaal pad | `test_IT5_readme_stappen_A_tot_E_en_commando_s_aanwezig`, `test_IT5_readme_toplevel_controle_met_stopinstructie`, `test_IT5_readme_veilig_check_eindregel_klopt_met_script`, `test_IT5_readme_geen_lokaal_pad_of_persoonlijk_account` | test_iteratie5_online.py |

### Wijzigingen aan bestaande tests in iteratie 6 (was -> nu, waarom)
Geen criterium verzwakt. Elke wijziging volgt uit een gewijzigd criterium (US-016/017/018, BACKLOG-notitie US-015) of uit het AI-plafond. Reden per regel.
1. `test_US010_c1` (categorie-set): was {Data, Automatisering, AI} -> nu {BI, Data, Automatisering, AI}. US-016 c1.
2. `test_US010_c2` (AI in samenvatting): was AI -> nu None; controle "AI in titel" toegevoegd. US-016 c3.
3. `test_US010_c3` (gelijkspel): was AI > Automatisering > Data -> nu BI > Data > Automatisering > AI. US-016 c2. Invoer "Data en AI" (los "data" telt sinds it. 4 niet) -> "Dataset en AI"; "Automatisering van databases" en "Automatisering, automatisering, database, database" verwachten nu Data (gelijkspel verliest van Data).
4. `test_US010_c5` (vaste testset): "Dashboards voor betere bedrijfsrapportage" was Data -> nu BI. US-016 c1 (dashboard en rapportage zijn BI-termen).
5. `test_US015_c4` (testset): "Nieuw dashboard toont rapportages in realtime" was Data -> nu BI. US-016 c1.
6. `test_US015_c10` (Data-termen): "business intelligence" en "Power BI" uit de lijst (BI, BACKLOG US-015 notitie); de extra titel "Power BI krijgt nieuwe koppelingen" -> "Databricks brengt een nieuwe versie van zijn dataplatform uit" (Data via databricks en dataplatform*). Er blijven 14 termen; eis minstens 10.
7. `hulp_statisch.fixture_items` item 7: was categorie AI ("Generative AI in de zorg") -> nu BI ("Dashboards voor de zorg: alles in een scherm"). Reden: met 4 AI en 4 overige items valt een AI-item weg door het AI-plafond. Gevolg: AI-tellingen in fixture-tests 4 -> 3 (`test_US012_c7_categoriefilter`, `test_US007_c2`, `test_US012_c6` browser), en teller-bi = 1 toegevoegd. Het totaal blijft 8.
8. `hulp_statisch.bouw()`: nieuwe parameter `vandaag` (`--vandaag`). Fixture-tests gebruiken vaste peildatum 2026-10-08 (was: klokdatum van de test, dus Uitgelicht hing van de dag af).
9. `test_US012_c4_nieuwsitem` (statisch): was zip op volgorde -> nu koppelen op link, en controle dat alle getoonde items op Nieuws staan (robuust bij gelijke datums en het AI-plafond).
10. `test_US012_c6_startpagina_toont_vijf_nieuwste_items`: was 5 nieuwste -> nu vaknieuws = 5 nieuwste getoonde items die niet in Uitgelicht staan (US-018 c5). Uitgelicht-titels uit de pagina gelezen. Vaknieuws kan minder dan 5 zijn als er minder items zijn.
11. `test_US012_c6_startpagina_tellers_per_categorie_kloppen_met_data`: loop nu ook over BI.
12. `TestSiteEchteData` (statisch, echte data): items waren Data/Automatisering/AI (70 van 104); nu incl. BI en na het AI-plafond (`verwacht_getoond`). Tellers loop incl. BI.
13. `test_US012_c5_bronnenlijst` (fixture): categorie AI -> Data. Anders verwijdert het AI-plafond alle items en faalt de bouw ("bevat geen nieuwsitems").
14. `test_US012_browser` fixture-tellingen: zie punt 7. `test_US004_c2_statisch_1280_px_tegels_drie_kolommen` -> `..._tegels_naast_elkaar`: was 3 kolommen (3 tellers) -> nu 4 kolommen (4 categorietellers, US-012 c6/US-016). Het 375 px-criterium (`test_US008_c8_statisch_375_px_kaarten_onder_elkaar`) is NIET aangepast; zie BEVINDING in het testrapport.
15. `test_statisch_regressie`: tegels op de startpagina 3 -> 4 (US-016); categorielijst incl. BI; fixture met vaste peildatum.
16. `test_acceptance` US-004 c1 en c4 (lokale app): vijf nieuwste -> vaknieuws (US-018 c5). Uitgelicht-titels uit de pagina gelezen (datum-onafhankelijk). Regex accepteert het bron-element in het vaknieuws-blok (US-018 c2 toont bron).
17. `test_echte_data_app`: `..._samenvatting_300...`: fixture AI -> Data (een los AI-item wordt door het AI-plafond weggelaten). `..._overzicht_tellers_en_vijf_nieuwste...`: het nieuwste item moet in Uitgelicht of in vaknieuws staan (US-018).
18. `test_US009_c6` (app toont opgehaalde items): verwachte aantallen en links na het AI-plafond (`verwacht_getoond`).

### Wijzigingen aan de tests in iteratie 6, ronde 2 (na fixronde 1; was -> nu, waarom)
Geen criterium verzwakt. Wijzigingen volgen uit het aangescherpte criterium (US-016 c8, US-017 c7) of uit een fixture die een niet-meer-Data-woord gebruikte.
19. `test_US010_c1_config_heeft_trefwoorden_nl_en_per_categorie`: Data-eis "gegevens" -> "gegevensanalyse". Los "gegevens" is geen Data-trefwoord meer (US-016 c8; besluit 2026-10-09-fixronde1-it6, punt 4). De samenstelling blijft Data-trefwoord.
20. `test_US011_c5_item_zonder_titel_overgeslagen_zonder_datum_krijgt_ophaaldatum`: fixture-beschrijving "Gegevens" -> "SQL" (item "Met datum over data"). Het item moest via een Data-trefwoord binnenkomen; met het los "gegevens" vervallen was het item zonder categorie en telde de test het item niet mee. Het criterium (titel leeg overslaan, datum krijgt ophaaldatum) is ongewijzigd.
21. `test_US017_c4_vaste_testset_klopt_voor_elke_titel`: "Gemini, metadata and the analogy game" van geweigerd (True) -> toegelaten (False). US-017 c7: 'analogy game' staat op de uitzonderingslijst. Daarna 5 weigeren en 7 toelaten in de testset (minstens 5 van elk vereist).
Nieuwe tests (geen wijziging van bestaande): `test_US016_c8_*` (2), `test_US016_c9_*`, `test_US016_c10_*`, `test_US017_c5_dubbele_geweigerde_link_in_feed_telt_een_keer`, `test_US017_c6_*` (3), `test_US017_c7_*` (3).

Nieuwe hulp: `hulp_statisch.verwacht_getoond(items)`: onafhankelijke uitwerking van het AI-plafond (k = (2n)//3 AI bij n overige items). `hulp_browser.py`: Site-klasse rond de bestaande Edge-proxy.

### Wijzigingen aan bestaande tests in iteratie 6, ronde 3 (Tester; was -> nu, waarom)
Geen criterium verzwakt. De wijziging volgt uit het gewijzigde US-018 c8 en c7 (besluit 2026-10-09-fixronde2-it6.md).
22. `test_US012_c6_startpagina_toont_vijf_nieuwste_items`: was: elk weggelaten item moet ouder zijn dan het oudste getoonde, en het aantal is min(5, aantal rest). Nu: (a) het aantal volgt de regel "max 5, max 2 AI" (`verwacht_vaknieuws_aantal`); (b) hooguit 2 AI getoond; (c) een weggelaten item dat nieuwer is dan het oudste getoonde, moet een geldige reden hebben: AI terwijl er al 2 AI getoond worden, een titel die met "Kort:" begint, of een evenementterm in titel/samenvatting (`mag_weggelaten`). Zonder reden blijft het een fout. Positief en negatief getoetst in `test_US012_c6_weggelaten_nieuwere_items_uitzonderingen_positief_en_negatief` (o.a. "Kortom:" en "Congresbezoekers" mogen niet uitgesloten worden; 1 AI getoond geeft geen uitzondering).
Nieuwe tests (ronde 3): `test_US018_c7_c8_evenement_kort_ai.py` (10 tests), `test_US016_c11_peildatum.py` (3 tests).

## Iteratie 7 (US-019, US-020, US-021; lokale app verwijderd)
Besluiten: `docs/decisions/2026-10-09-open-punten-a-d.md`, `docs/decisions/2026-10-09-criteria-feedruil-it7.md`, regressietabel in `docs/BACKLOG.md` ("Regressie na US-020").

### Nieuwe tests (criterium -> testnaam)
| Criterium | Testnaam | Bestand |
|---|---|---|
| US-019-c1 geen AWS Big Data, minstens 1 automatiseringsfeed, max 10 feeds, min 3 NL/3 EN, min 2 BI-feeds, min 2 NL-headnieuws (feeds op naam) | `test_US019_c1_aws_big_data_blog_staat_niet_meer_in_config`, `test_US019_c1_minstens_1_automatiseringsfeed`, `test_US019_c1_max_10_feeds_min_3_nl_en`, `test_US019_c1_min_2_bi_feeds_en_2_algemene_nl_headnieuws` | test_US019_automatiseringsfeed.py |
| US-019-c2 feed in bronnen.html en feedbesluit (gratis, geen login, robots, reden, afgevallen kandidaten) | `test_US019_c2_iteratie7_sectie_beschrijft_nieuwe_feed_gratis_login_robots_en_reden`, `test_US019_c2_nieuwe_automatiseringsfeeds_in_besluit_en_op_bronnen` | test_US019_automatiseringsfeed.py |
| US-019-c3 items van niet-geconfigureerde bron weg; falende feed in config houdt items (lokale testfeeds) | `test_US019_c3_items_van_bron_niet_in_config_verwijderd_falende_feed_blijft` | test_US019_automatiseringsfeed.py |
| US-019-c3 (echte data, alleen-lezen) geen items van niet-geconfigureerde bronnen | `test_US019_c3_echte_data_geen_items_van_niet_geconfigureerde_bronnen` | test_US019_automatiseringsfeed.py |
| US-019-c4 (echte data) minstens 1 item van een automatiseringsfeed; meting per categorie/feed is meldpunt (testrapport) | `test_US019_c4_echte_data_bevat_items_van_een_automatiseringsfeed` | test_US019_automatiseringsfeed.py |
| US-020-c1 src/app.py en src/data.py bestaan niet; geen leadwoorden (hele woorden) in src/, config/, README.md; geen leadstatussen | `test_US020_c1_app_py_en_data_py_bestaan_niet`, `test_US020_c1_geen_leadwoorden_in_src_config_en_readme`, `test_US020_c1_geen_leadstatussen_in_src_config_en_readme` | test_US020_lokale_app_weg.py |
| US-020-c1 geen leadwoorden in tests/ (uitzonderingen gedocumenteerd, zie hieronder) | `test_US020_c1_geen_leadwoorden_in_tests`, `test_US020_c1_uitzonderingen_zijn_gedocumenteerd` | test_US020_lokale_app_weg.py |
| US-020-c1 verzonnen bedrijfsnamen uit oude voorbeelddata | NIET GETEST: de lijst is niet meer beschikbaar (src/data.py verwijderd, geen commit-historie) | - |
| US-020-c2 geen http.server of verwijderde module (app, data, logica) in src/; src/ bevat alleen ophalen, bouw, mix, veilig_check | `test_US020_c2_geen_http_server_of_verwijderde_modules_in_src`, `test_US020_c2_src_bevat_alleen_ophalen_bouwen_mix_en_veilig_check` | test_US020_lokale_app_weg.py |
| US-020-c3 verse checkout (kopie zonder site/ en caches): ophalen (lokale testfeeds), bouwen, veilig_check, unittests zonder ImportError | `test_US020_c3_ophalen_werkt_zonder_app_bestanden`, `test_US020_c3_bouwen_werkt_zonder_app_bestanden`, `test_US020_c3_veilig_check_exitcode_0_in_verse_checkout`, `test_US020_c3_unittests_draaien_in_verse_checkout_zonder_importfout` | test_US020_lokale_app_weg.py |
| US-020-c4 README: geen startinstructie lokale app; wel ophalen, bouwen, statische server, feeds, publiceren | `test_US020_c4_geen_startinstructie_voor_lokale_app`, `test_US020_c4_readme_beschrijft_ophalen_bouwen_bekijken_feeds_en_publiceren` | test_US020_lokale_app_weg.py |
| US-021-c1 productblog met hoogste score niet in Uitgelicht; wel op Nieuws en in Vaknieuws | `test_US021_c1_productblog_met_hoogste_score_niet_in_uitgelicht`, `test_US021_c1_productblog_wel_op_nieuws_en_in_vaknieuws_als_nieuwste` | test_US021_uitgelicht.py |
| US-021-c2 alleen headnieuws; NL-punt; vaste volgorde (testconfig, NL eerst bij gelijke relevantie); productblog niet in Uitgelicht | `test_US021_c2_uitgelicht_exacte_volgorde_met_nl_punt`, `test_US021_c2_productblog_looker_qlik_niet_in_uitgelicht`, `test_US021_c2_readme_beschrijft_headnieuws_en_nl_punt` | test_US021_uitgelicht.py |
| US-021-c3 geen aanvulling (2 items geeft 2; 0 items: "Nog geen uitgelicht nieuws", Vaknieuws blijft) | `test_US021_c3_twee_geschikte_items_geven_precies_twee`, `test_US021_c3_nul_geschikte_items_toont_melding_en_vaknieuws_blijft` | test_US021_uitgelicht.py |
| US-021-c4 Vaknieuws ongewijzigd (5 nieuwste niet in Uitgelicht, ongeacht taal) | `test_US021_c4_vaknieuws_is_5_nieuwste_niet_in_uitgelicht_ongeacht_taal` | test_US021_uitgelicht.py |

### Regressie na US-020 (statische site; wat er nu de dekking is)
- US-001 c3, c5: `test_US001_c3_statisch_actief_menu_item_gemarkeerd`, `test_US001_c5_statisch_interface_is_nederlands` (test_statisch_regressie.py). c6: `test_US001_c6_statisch_375_px_*`, `test_US001_c6_statisch_1280_px_*` (test_US012_browser.py). c2 (navigatie Overzicht/Nieuws): `test_US001_c2_statisch_navigatie_precies_overzicht_en_nieuws`.
- US-002 c1: `test_US002_c1_statisch_nieuws_nieuwste_eerst_met_alle_velden`. c2-c4: `test_US012_c7_*` (categorie, Alle, zoeken; test_US012_browser.py). c5: `test_US002_c5_geen_resultaat_melding_zonder_fout`. c6: `test_US002_c6_titel_opent_bronlink_in_nieuw_tabblad_statisch`.
- US-007 c1: `test_US007_c1_statisch_favicon_geen_404` (test_US012_statische_site.py). c2/c3: `test_US007_c2_kleine_letters_categorie_gelijk_aan_juiste_schrijfwijze`, `test_US007_c3_onbekende_filterwaarde_toont_alles_en_alle_actief` (test_US012_browser.py).
- US-008 c1-c8: `test_US008_c1_statisch_*` t/m `test_US008_c8_statisch_*` (test_statisch_regressie.py; c8 breedte ook test_US012_browser.py); focusrand: test_US008_c3_focusrand.py (leest nu de stylesheet van de gebouwde site).
- US-009 c6: `test_US009_c6_site_toont_opgehaalde_items_nieuwste_eerst_met_link` (test_US009_feeds.py; was: de app).
- US-012 c3 (generiek): `test_US012_c3_geen_lead_velden_bedrijf_branche_gevonden`, `test_US012_c3_geen_voorbeeldmarkering_uit_app_data`. Verzonnen namen: NIET GETEST (zie hierboven).
- US-015 c7/c11 en US-016 c5 (iteratie 7): toetsen op de naam van de feed (regels: automatisering, BI/data), niet op vaste feednamen. US-015 c7 eist minstens 2 automatiseringsfeeds.
- US-013 c5: `test_US013_c5_readme_stappen_online_zetten` accepteert nu "openbaar" (de README-zin is "De repo moet openbaar zijn"; was "openbare"). Geen criterium verzwakt; de stappen zelf worden nog gecontroleerd.

### Vervallen in iteratie 7 (per test; de testfunctie blijft in het bestand of is geskipt, met reden)
Stand per einde iteratie 7: de drie bestanden `test_acceptance.py`, `test_browser_layout.py`, `test_echte_data_app.py` stonden geskipt op `raise unittest.SkipTest(...)`. **In iteratie 8 zijn ze verwijderd** (Stef akkoord, 2026-10-09; zie "Iteratie 8" hieronder). Hun tests tellen dus niet meer mee; de vervangende statische tests staan in de tabel hierboven.
- `test_acceptance.py`, lokale app: `test_US001_c1_start_met_readme_commando` (vervangen door US-012 c1, `test_US012_c1_bouwcommando_maakt_statische_map_zonder_server_code`); `test_US001_c2_navigatie_precies_drie_items_en_juiste_doelen` (vervangen: statisch, Overzicht/Nieuws); `test_US001_c4_voorbeelddata_minimum_en_verzonnen` (leadsdeel: vervallen, US-003 vervalt); `test_US001_c3_*` en `test_US001_c5_*` en `test_US002_c1..c6_*` (vervangen door de statische tests hierboven).
- `test_acceptance.py`, US-003 (alle 6 tests `test_US003_c1..c6_*`) en US-004 (`test_US004_c1_*`, `test_US004_c3_*`, `test_US004_c4_*`) vervallen volledig (BACKLOG: vervalt zodra US-012 klaar is; startpagina via US-012 c6 en US-018). US-004 c2 (`test_US004_c2_blokken_tonen_totaal_en_alles_bekijken`) vervallen; layout via `test_US004_c2_statisch_1280_px_tegels_naast_elkaar`.
- `test_acceptance.py`, US-007 en US-008 (app): `test_US007_c1..c3_*`, `test_US008_c1..c8_*` vervangen door de statische tests hierboven.
- `test_browser_layout.py`: `test_US001_c6_375_px_*`, `test_US001_c6_1280_px_*`, `test_US008_c8_*` (2), `test_US004_c2_1280_px_*`; vervangen door `test_US012_browser.py` (statisch, zelfde 375/1280 px-meting).
- `test_echte_data_app.py`: `test_echte_data_nieuws_toont_alle_items_uit_bestand_nieuwste_eerst`, `..._ampersand_in_link_...`, `..._html_in_titel_...`, `..._overzicht_tellers_...`, `..._zoeken_en_categorie_...`, `..._leeg_bestand_...`, `..._zonder_bestand_valt_terug_op_voorbeeld`, `..._kapot_bestand_...`, `..._samenvatting_300_tekens_...`, `test_echte_data_bestand_in_project_is_geldig_en_veilig` (zonder vervanging; geheimen dekt `src/veilig_check.py`), `test_echte_data_app_toont_zelfde_aantal_en_escaped_links_als_bestand`. Dekking statisch: `TestSiteEchteData` en `TestSiteFixture` in test_US012_statische_site.py.
- `test_US018_uitgelicht.py`, klasse `TestUS018Lokaal` (4 tests: `test_US018_c2_lokale_app_*`, `test_US018_c5_lokale_app_*`, `test_US018_c4_lokale_app_*`, `test_US016_c7_lokale_app_*`): uitgeschakeld met `@unittest.skip`. Dekking statisch: `TestUS018Statisch`, `test_US016_c7_browser_*`.
- `test_US016_mix.py`, `test_US016_c4_lokale_app_gebruikt_hetzelfde_plafond`: uitgeschakeld. Dekking: `test_US016_c4_mix_80_ai_en_20_overig_geeft_13_ai_en_20_overig` en `test_US016_c4_site_nieuws_tellers_en_overzicht_*` (via bouw).
- Unittests (tests/, Bouwer): verwijderde app-tests; de Bouwer-suite draait nu 112 tests (was 137 in iteratie 6).

### Zoekwoorden in deze map
De controle op leadwoorden (US-020 c1) staat in `test_US020_lokale_app_weg.py` (`EXEMPT_TESTBESTANDEN`). Dit README en `test_US012_statische_site.py` bevatten het woord als testhistorie of als zoekterm; daarom zijn ze uitgezonderd.

## Regel: het woord lead (vastgelegd in iteratie 8, besluit Stef)
- Het woord "lead" of "leads" (als los woord, hoofdletterongevoelig) komt NIET voor in `src/`, `config/`, `README.md` (projectmap) en `tests/`. Dit is US-020 c1.
- Uitzondering, alleen deze drie bestanden. De lijst staat in `EXEMPT_TESTBESTANDEN` in `test_US020_lokale_app_weg.py`:
  1. `tests/acceptance/test_US020_lokale_app_weg.py`: de controle zelf (zoekpatroon en de uitzonderingslijst).
  2. `tests/acceptance/test_US012_statische_site.py`: controles op afwezige leadlinks en -velden (zoektermen in strings).
  3. `tests/acceptance/README.md`: documentatie van de suite (deze regel en de testhistorie).
- Elk ander bestand met het woord laat `test_US020_c1_geen_leadwoorden_in_tests` falen. Een nieuwe uitzondering vraagt akkoord van Stef en moet in deze lijst en in `EXEMPT_TESTBESTANDEN` (sluitend).
- De verwijderde bestanden `test_acceptance.py`, `test_browser_layout.py` en `test_echte_data_app.py` staan niet meer in de uitzonderingslijst (iteratie 8).
- `test_US020_c1_uitzonderingen_zijn_gedocumenteerd` controleert dat deze sectie bestaat, dat elk uitzonderingsbestand bestaat en dat het in dit README genoemd wordt.

## Iteratie 8 (US-020 afronden, US-022 afwerking; Tester ronde 1)
Besluiten: Stef akkoord (a) verwijderen van de drie vervallen bestanden, (b) regel "lead" hierboven, (c) US-022 (BACKLOG).

### Nieuwe tests (criterium -> testnaam)
| Criterium | Testnaam | Bestand |
|---|---|---|
| US-022-c1 startpagina: geen totaal in de kop van Vaknieuws; link "Alle n berichten bekijken", n = items op Nieuws (fixture) | `test_US022_c1_fixture_startpagina_zonder_totaal_en_link_met_aantal_nieuws` | test_US022_afwerking.py |
| US-022-c1 idem op de site uit data/nieuws.json (NIET GETEST als het bestand ontbreekt) | `test_US022_c1_echte_data_startpagina_zonder_totaal_en_link_met_aantal_nieuws` | test_US022_afwerking.py |
| US-022-c2 ontbrekend configbestand: Nederlands, pad, exitcode 2, geen traceback, geen uitvoerbestand | `test_US022_c2_ontbrekend_configbestand_nederlandse_melding_exitcode_2` | test_US022_afwerking.py |
| US-022-c2 onleesbaar configbestand (geen JSON) | `test_US022_c2_onleesbaar_configbestand_geen_json_nederlandse_melding_exitcode_2` | test_US022_afwerking.py |
| US-022-c2 (extra) configbestand zonder leesbare tekst (UTF-8) en een map als configbestand | `test_US022_c2_configbestand_geen_tekst_nederlandse_melding_exitcode_2`, `test_US022_c2_map_als_configbestand_nederlandse_melding_exitcode_2` | test_US022_afwerking.py |
| US-022-c2 (extra, Tester it. 8) feed-item dat geen object is: nette melding, exitcode 2 | `test_US022_c2_extra_feed_item_dat_geen_object_is_geeft_geen_traceback` | test_US022_afwerking.py |
| US-022-c2 (extra, Tester ronde 2) feed zonder url: nette melding, exitcode 2 | `test_US022_c2_extra_feed_zonder_url_nederlandse_melding_exitcode_2` | test_US022_afwerking.py |
| US-022-c2 (extra, Tester ronde 2) feeds als object, leeg object, user_agent ontbreekt: nette melding, exitcode 2 | `test_US022_c2_extra_feeds_als_object_leeg_object_en_zonder_user_agent_exitcode_2` | test_US022_afwerking.py |

### Iteratie 8, Tester ronde 3 (US-022 c3-c5, lokale feeds, geen internet)
| Criterium | Testnaam | Bestand |
|---|---|---|
| US-022-c3 lege trefwoorden-object, sleutel "Ai", lege lijst, lege term, term met alleen spaties, tekst i.p.v. lijst, categorie ontbreekt: exitcode 2, Nederlandse melding, data ongewijzigd | `test_US022_c3_lege_trefwoorden_object_exitcode_2_data_ongewijzigd`, `test_US022_c3_typo_sleutel_Ai_noemt_categorie_AI_exitcode_2_data_ongewijzigd`, `test_US022_c3_lege_lijst_per_categorie_exitcode_2_data_ongewijzigd`, `test_US022_c3_lege_term_exitcode_2_data_ongewijzigd`, `test_US022_c3_term_met_alleen_spaties_exitcode_2_data_ongewijzigd`, `test_US022_c3_trefwoorden_als_tekst_i_p_v_lijst_exitcode_2_data_ongewijzigd`, `test_US022_c3_categorie_Data_ontbreekt_exitcode_2_data_ongewijzigd` | test_US022_c3_c5_vangnet.py |
| US-022-c3 reproductie ronde 2 (kopie van data/nieuws.json of 87 synthetische items, echte feedlijst, bereikbare feed, `trefwoorden: {}`): exitcode 2, bestand intact | `test_US022_c3_repro_ronde2_dataverlies_met_bereikbare_feed_en_echte_feeds` | test_US022_c3_c5_vangnet.py |
| US-022-c4 precies 50% (10 van 10 en 50 van 100) wordt geschreven, exitcode 0 | `test_US022_c4_precies_50_procent_wordt_geschreven_exitcode_0`, `test_US022_c4_precies_50_van_100_wordt_geschreven_exitcode_0` | test_US022_c3_c5_vangnet.py |
| US-022-c4 51% (51 van 100, 6 van 10) wordt geweigerd: exitcode 1, data ongewijzigd, melding met aantallen, `--forceer-opruimen`, "niets weggeschreven" | `test_US022_c4_51_procent_wordt_geweigerd_exitcode_1_data_ongewijzigd` | test_US022_c3_c5_vangnet.py |
| US-022-c4 `--forceer-opruimen` schrijft wel (exitcode 0) | `test_US022_c4_met_forceer_opruimen_wordt_wel_geschreven_exitcode_0` | test_US022_c3_c5_vangnet.py |
| US-022-c4 feedruil telt niet mee (30 items van een niet-geconfigureerde bron; 5 van 10 eigen items weg + 30 vreemde) | `test_US022_c4_feedruil_telt_niet_mee_items_van_niet_geconfigureerde_bron_geven_geen_vangnet`, `test_US022_c4_feedruil_met_50_procent_eigen_items_geen_vangnet` | test_US022_c3_c5_vangnet.py |
| US-022-c4 gewone ronde wordt niet geblokkeerd (lokale feed met nieuw item; echte data-kopie met echte trefwoorden) | `test_US022_c4_gewone_ronde_wordt_niet_geblokkeerd_nieuw_item_komt_erbij`, `test_US022_c4_echte_data_gewone_ronde_wordt_niet_geblokkeerd` (NIET GETEST als data/nieuws.json ontbreekt) | test_US022_c3_c5_vangnet.py |
| US-022-c4 workflow gebruikt `--forceer-opruimen` niet | `test_US022_c4_workflow_gebruikt_forceer_opruimen_niet` | test_US022_c3_c5_vangnet.py |
| US-022-c4 (extra, Tester ronde 3, BLOKKEREND-kandidaat) onleesbaar data-bestand (BOM of afgekapt) met 87 items wordt niet stil leeggeschreven | `test_US022_c4_extra_onleesbaar_data_bestand_leegt_de_opslag_niet` (ROOD bij ronde 3: zie testrapport) | test_US022_c3_c5_vangnet.py |
| US-022-c5a config met UTF-8-BOM wordt normaal gelezen (exitcode 0) | `test_US022_c5a_utf8_met_bom_wordt_normaal_gelezen_exitcode_0` | test_US022_c3_c5_vangnet.py |
| US-022-c5b uitsluitingen/weigertermen/weigertermen_samenvatting/weiger_uitzonderingen geen lijst van tekst: exitcode 2, data ongewijzigd | `test_US022_c5b_lijstvelden_geen_lijst_van_tekst_exitcode_2_data_ongewijzigd` | test_US022_c3_c5_vangnet.py |
| US-022-c5c feed-url niet http(s) (file:///, FILE:///, ftp://, zonder schema, leeg): exitcode 2, data ongewijzigd | `test_US022_c5c_feed_url_zonder_http_of_https_exitcode_2_data_ongewijzigd` | test_US022_c3_c5_vangnet.py |
| US-022-c5d `"feeds": []`: exitcode 2, "geen feeds ingesteld", niet "mislukt", data ongewijzigd | `test_US022_c5d_lege_feeds_eigen_melding_exitcode_2_data_ongewijzigd`, `test_US022_c5_geen_uitvoer_bij_configfout_zonder_bestaand_bestand` | test_US022_c3_c5_vangnet.py |

### Iteratie 8, Tester ronde 4 (extra dataverlies- en configtests, geen geschreven criteria; lokale feeds)
| Criterium | Testnaam | Bestand |
|---|---|---|
| US-022-c4 (extra, Tester ronde 4, BLOKKEREND-kandidaat) bewaar_dagen 6 (typo) wist niet stil 90% van de items | `test_US022_extra_r4a_bewaar_dagen_typo_wist_niet_stil_90_procent` | test_US022_ronde4_dataverlies.py |
| US-022-c5 (extra, ronde 4, BELANGRIJK) bewaar_dagen 0 of als tekst: exitcode 2, Nederlands, data ongewijzigd | `test_US022_extra_r4b_bewaar_dagen_nul_is_configfout`, `test_US022_extra_r4b_bewaar_dagen_tekst_is_configfout` | test_US022_ronde4_dataverlies.py |
| US-022-c4 (extra, ronde 4, BELANGRIJK) opgeslagen item zonder datum of id geeft geen traceback | `test_US022_extra_r4c_item_zonder_datum_geen_traceback`, `test_US022_extra_r4c_item_zonder_id_geen_traceback` | test_US022_ronde4_dataverlies.py |
| US-022-c4 (extra, ronde 4, positief) mislukte schrijfactie laat het origineel byte-gelijk (atomair schrijven) | `test_US022_extra_r4d_mislukte_schrijfactie_laat_origineel_intact` | test_US022_ronde4_dataverlies.py |

### Iteratie 8, Tester ronde 5 (extra dataverlies- en robuustheidstests, geen geschreven criteria; lokale feeds)
Alle zes tests zijn bij oplevering ROOD (bevindingen 1-3 van het testrapport ronde 5). Ze zijn niet verzwakt; de bouwer lost ze op.
| Criterium | Testnaam | Bestand |
|---|---|---|
| US-022-c4/c5 (extra, ronde 5, BLOKKEREND) items met datum in andere notatie (86 van 87) wissen niet stil met exitcode 0 | `test_US022_extra_r5a_andere_datumnotatie_wist_niet_stil_86_van_87` | test_US022_ronde5_dataverlies.py |
| US-019-c3 / US-022-c4 (extra, ronde 5, BELANGRIJK; ontwerpvraag PO) alle items van een niet-geconfigureerde bronnaam wissen niet stil | `test_US022_extra_r5b_bronnaam_van_alle_items_gewijzigd_wist_niet_stil` | test_US022_ronde5_dataverlies.py |
| US-022-c5 (extra, ronde 5, BELANGRIJK) bewaar_dagen extreem groot (1000000): geen traceback | `test_US022_extra_r5c_bewaar_dagen_extreem_groot_geen_traceback` | test_US022_ronde5_dataverlies.py |
| US-022-c4 (extra, ronde 5, BELANGRIJK) opgeslagen item met samenvatting als getal: geen traceback | `test_US022_extra_r5d_samenvatting_als_getal_geen_traceback` | test_US022_ronde5_dataverlies.py |
| US-022-c4 (extra, ronde 5, BELANGRIJK) opgeslagen item met bron als lijst: geen traceback | `test_US022_extra_r5e_bron_als_lijst_geen_traceback` | test_US022_ronde5_dataverlies.py |
| US-022-c5 (extra, ronde 5, BELANGRIJK) ongeldige re:-regex in weigertermen: geen traceback, data ongewijzigd | `test_US022_extra_r5f_ongeldige_regex_in_weigertermen_geen_traceback` | test_US022_ronde5_dataverlies.py |

### Gewijzigde tests (was -> nu, waarom)
Geen criterium verzwakt. De wijzigingen volgen uit het gewijzigde US-022 c1 (teller in de kop weg, link "Alle <n> berichten bekijken") of uit de EXEMPT-regel.
1. `test_US012_c6_startpagina_tellers_per_categorie_kloppen_met_data` (fixture en echte data): was `assertIn("%d in totaal")` -> nu geen "in totaal" op de startpagina en `>Alle %d berichten bekijken</a>`. US-022 c1.
2. `test_US016_c4_site_nieuws_tellers_en_overzicht_tonen_alleen_de_getoonde_items`: was `'<span class="totaal">33 in totaal</span>'` -> nu geen "in totaal" en `>Alle 33 berichten bekijken</a>`. US-022 c1. De tellers per categorie en het aantal op Nieuws blijven getoetst.
3. `test_US001_c5_statisch_interface_is_nederlands` (test_statisch_regressie.py): was "Alles bekijken" in de lijst -> nu "Alle <n> berichten bekijken" (regex). US-022 c1. De overige Nederlandse woorden blijven in de lijst.
4. `test_US020_c1_geen_leadwoorden_in_tests` en `test_US020_c1_uitzonderingen_zijn_gedocumenteerd`: EXEMPT-lijst was 5 bestandsnamen (waarvan 2 verwijderde en het README op bestandsnaam) -> nu 3 paden, sluitend (elk moet bestaan en in dit README staan). Zie "Regel: het woord lead".
5. Bytecode: `sys.dont_write_bytecode = True` staat nu vóór de imports in test_US010, test_US015_categorie, test_US016_mix, test_US017_weigerlijst en test_US018_uitgelicht. `test_US009_ronde2` start het subproces nu met `-B`. Geen criterium gewijzigd.
6. Verwijderd (akkoord Stef): `test_acceptance.py`, `test_browser_layout.py`, `test_echte_data_app.py` (alle tests erin waren geskipt; 43 regels met het woord lead). Niet verzwakt: hun dekking staat in de statische tests (zie "Regressie na US-020").

### Niet geautomatiseerd / NIET GETEST in iteratie 8
- US-020 c1 verzonnen bedrijfsnamen uit de oude voorbeelddata: NIET GETEST. De PO-aanname "de lijst staat in git (66e4d21, src/data.py)" klopt niet: commit 66e4d21 bevat geen bestanden en src/data.py is niet in de git-historie te vinden. Nodig: de lijst van de 12 voorbeeldbedrijven (van Stef of een kopie), dan als test toevoegen.
- Verwijderde bestanden: test_acceptance.py, test_browser_layout.py en test_echte_data_app.py zijn weg; de bijbehorende tests tellen niet meer mee.
