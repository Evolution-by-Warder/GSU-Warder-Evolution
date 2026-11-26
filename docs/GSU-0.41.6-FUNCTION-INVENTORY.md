# Funkčný inventár a ochrana pred duplicitami — GSU 0.41.6

26.11.2026. Kontrola aktuálneho vývojového HEAD `3038602601ccd527fb458bda731d2c31320949e4` a pôvodného referenčného auditu [GSU-0.41.5-REFERENCE-AUDIT.md](GSU-0.41.5-REFERENCE-AUDIT.md). Ide o statickú kontrolu funkcií a ciest v menu, nie nové meranie na prijímači. Návrhy rozšírení ešte nie sú implementované.

## Pravidlo ďalšej práce

Pred každým rozšírením vyhľadať existujúci vlastník funkcie, zber dát, používateľskú cestu a testy. Použiť spoločný zdroj údajov a rozšíriť existujúcu obrazovku alebo jej podrobnosti. Nevytvárať duplicitu v menu, ďalší samostatný sampler, paralelný aktualizátor alebo druhú správu s rovnakým obsahom. Nový modul iba pri skutočne odlišnej funkcii. Pasívny výber položky nesmie spustiť zápis, ladenie ani aktívny sieťový test. Nedostupné hodnoty zobrazovať ako neznáme.

| Oblasť | Existujúci vlastník a funkcia | Medzera / rozhodnutie |
|---|---|---|
| Systém | warder_system_data.dashboard/information, warder_live.Sampler, warder_telemetry.cpu_counters, warder_system.Information, warder_overview, warder_chart | CPU už meria súhrnne, nie jednotlivé jadrá. Rozšíriť spoločné počítadlá o jadrá, frekvencie a uptime, ak sú vystavené. Nepridávať druhý živý systémový prehľad. |
| Procesy | warder_system_data.process_table, CentreMenu/Report, RSS/CPU triedenie | Voliteľné PSS len pre vybraný proces a pri dostupnom smaps_rollup; nie ďalší zoznam procesov. |
| Pamäť a úložisko | warder_storage.report/category_snapshot/smart/configured_picons, warder_telemetry.memory_values, swap_ops/swap_ui | SMART zdravie/teplota, mounty, kategórie a piconové profily už existujú. Detail atribútov SMART a diskové I/O, pamäťové členenie, prehľad EPG/timeshift umiestnenia rozšíriť tam. Prípadný rebríček súborov len v jasne vymedzenom lokálnom priestore, s limitom a bez mazania. |
| Sieť | warder_network.collect/local_addresses/ping/diagnostics/overview_panels, warder_live RX/TX, warder_system_data.observed_services | Už máme adresy, gateway, DNS nastavenie, speed, ping loss/RTT, HTTPS feed/site, počet mountov, FTP/Telnet/VPN/Samba/NFS daemon observations a súhrnný RX/TX. Rozšíriť jeden zber o MAC, duplex, link/wi-fi, per-interface counters/errors, údaje mountov bez credentials, SSH/OpenWebif a oddelený pozorovaný stav portov. DNS aktívny test na výslovnú akciu; DNS konfigurácia nie je dôkaz funkčného resolvera. Znovupoužiť Sampler, nie ďalší paralelný worker. |
| Príjem | warder_tuners.details/slots, warder_signal.SignalMonitor, warder_tuner_ui.Header, warder_chart, warder_quick, warder_services | FBC root/link, nahrávajúce/aktívne tunery, HDR/HDMI/audio, MIS/PLS/T2MI a ďalšie parametre už existujú. Meranie a sken oddelené, CSV všetkých metrík existuje. Prípadné uložené meracie profily a porovnávanie transpondérov rozšíriť z aktuálneho finder history, bez ďalšieho skenera a bez automatickej zmeny kanálov. |
| Informácie o kanáli | plugin.channelInfoCenter, warder_channel, bitrate_worker, warder_tuners.details | Zachovať pôvodné picony, identifikátory, bitrate a ECM, použiť existujúce parametre tunera. Modernizovať rozloženie, odstrániť orezanie, doplniť kodek iba ak je dostupný. |
| CAM/ECM | warder_ecm.InlineECM, plugin.ECMInfo/channelInfoCenter, warder_oscam, warder_cam | Už je živá hodnota ECM a čítanie údajov; navrhnutá časová história musí využívať existujúci zber, rozlišovať chýbajúce/nekódované údaje a nepočítať opakované čítanie jedného záznamu ako novú udalosť. |
| Servis | warder_service.health/crash_summary/forum_snapshot, warder_package_status.database/dependency_state, warder_ipk.inspect/review, warder_tools.run_task/write_bundle | Kontrola manifestu GSU, závislostí, obmedzená sumarizácia tried výnimiek, anonymný JSON náhľad a diagnostický archív už existujú. Detailný lokálny prehliadač crashlogov a inventár nainštalovaných pluginov sú medzery. Rozšíriť existujúci package DB parser; žiadna duplicitná správa pre fórum ani automatické odstraňovanie balíkov. |
| Zálohy | warder_scan_backup.create/copy_database | Overená privátna záloha pred natívnym ladením existuje. Prehľad existujúcich záloh je samostatná medzera. Obnova znamená zmenu používateľských súborov, vyžaduje osobitne bezpečný návrh; zatiaľ nepridávať. |
| Warder centrum | warder_projects.report/release/installed/status_label/entrypoint, ProjectMenu/ProjectReport, plugin_update_ui | Lokálna/stabilná verzia, stav aktualizácie, poznámky, architektúra, závislosti a priame otvorenie oficiálnych pluginov už existujú. Súhrn piatich produktov môže znovu použiť report; žiadny spoločný neoverený inštalátor. |
| Smart Diagnostics | warder_health.resource_check/health_summary, warder_system_data.overview, warder_tools.Probe.collect/summary, warder_service.health, warder_network | Existujúce skóre RAM/flash a read-only diagnostika. Rozšíriť orchestráciu existujúcich kontrol; nezobrazovať neoverené disky, internet či CAM ako úspešné. Žiadne nové univerzálne skóre bez pokrytia a dokumentácie. |

## Poradie po kontrole

1. Dokončiť navigáciu všetkých legacy ciest (CAM/ECM, swap, OSD, update); jednotné pravé panely, bez návratu do hlavného menu.
2. Rozšíriť sieťový zber, nezdvojovať existujúce testy ani grafy.
3. Lokálny crashlog prehliadač a inventár pluginov v Servisnom centre.
4. Modernizovať existujúce Informácie o kanáli.
5. Rozšíriť existujúce merania CPU/pamäť/disk a ECM, podľa dostupnosti image.
6. Zjednotiť výsledky v existujúcej diagnostike; až potom rozhodnúť o súhrnnom rozhraní.
7. Overiť jazykové kľúče vo všetkých 21 katalógoch, CI a fyzický prijímač.

Audit pôvodných referencií zostáva zdrojom inšpirácie, nie dôkazom, že cudzie pluginy boli spustené. Nepridávať cudzie binárky, nekontrolované feedy, automatické mazanie či zmeny autentifikácie. Rozsah funkcií sa overuje pred implementáciou po každom novom HEAD.


## Stav implementácie po dávkach (kontrola HEAD `4811cdd9828fec9491b15d37df254b8aa7843168`)

- Systém: CPU po jadrách, frekvencie, uptime, PSS vybraného procesu — zapracované.
- Úložisko: podrobná RAM, pasívne I/O, rozšírený SMART — zapracované. Konfigurované EPG/timeshift cesty a rebríček súborov nie sú dokončené.
- Sieť: rozhrania, MAC/duplex/Wi-Fi, kumulatívne počítadlá, mounty, služby/SSH/porty a explicitný DNS/NSS test — zapracované. OpenWebif atribúcia a samostatná história rozhraní nie sú implementované; súhrn RX/TX už existuje.
- Príjem: uložené satelitné merania v rámci Enigma2 session, porovnanie do 12 záznamov, bez skenu — zapracované.
- Kanál: nové rozloženie, natívne merania, viacriadkové CAID — zapracované; doplnenie kodeku nie je potvrdené.
- ECM: história pozorovaných aktualizácií súboru, nie úplný log požiadaviek — zapracované.
- Servis: inventár balíkov, lokálny prehliadač crashlogov, Smart Diagnostics — zapracované.
- Navigácia: vlastníctvo rodičovského centra, pasívny náhľad a pozastavenie pri skrytí — zapracované; všetky legacy akcie ešte nie sú skutočne inline v pravom paneli. SWAP/OSD/ECM používajú zjednotené podriadené obrazovky.
- Zálohy: táto dávka pridáva prehľad manifestov, nie opätovné overenie hashov ani obnovu. Žiadne automatické mazanie.
- Warder centrum: existujúci report/verzie/poznámky/otvorenie produktu zachované; hromadný súhrn piatich projektov nie je nový implementovaný pohľad.
- Lokalizácia: spoločné kľúče a placeholdery v 21 katalógoch, statické testy; čitateľnosť na fyzických prijímačoch ešte overiť.

Ostré vydanie blokuje neukončené CI presného HEAD a požadovaný fyzický retest. Nevyhlasovať zostávajúce voliteľné rozšírenia za hotové ani meniť produkciu bez splnenia brány.
