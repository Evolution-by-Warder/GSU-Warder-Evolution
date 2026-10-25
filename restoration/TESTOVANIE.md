# Pokračovanie testovania GSU — 24. 10. 2026 večer

## Cieľ a pracovná verzia

Najprv obnoviť všetky pôvodné funkcie a vzhľad GSU 13.20 na OpenATV 8 / Python 3.14.7. Moderný spoločný Warder dizajn riešiť až potom. Postupovať položku po položke, obrazovku po obrazovke spolu s používateľom.

- Pracovná vetva: `original-python314`; produkčná `warder-master-production` sa nemení.
- Nainštalovaný kandidát: **13.40-r10**, zdrojový commit `4f11d32cbd739dd6d6283b8dc7154ba41b008512`.
- Prijímač: GigaBlue UHD Quad 4K Pro, OpenATV 8, Python 3.14.7.
- IPK: `enigma2-plugin-glasssysutil_13.40-r10_all.ipk`, 2 159 770 B.
- SHA256 IPK: `9d066c1a881b16968a5adbcd77029a5de5d1ad85833fbc3ee3da8b8dc65abb2a`.
- Uložený balík: https://chatgpt.com/library?file_id=libfile_636702d5517c81918fe59d25ed44a8d8&account_id=personal
- 27 hostiteľských testov prešlo; CI 40126007199 úspešné. To neznamená úplné overenie funkcií na prijímači.
- Neupravovať starý moderný `src/`; obnovené jadro je `restoration/src/GlassSysUtil/plugin.py`. Opravy zaznamenať aj v `restoration/tools/port_source.py`, aby bola konverzia opakovateľná.

## Overené na prijímači

- Systémové informácie: procesy, Dmesg, CPU; vľavo/vpravo posúva horný panel, hore/dole dolný panel.
- Informácie o kanáli: údaje a picony, všetky ECM riadky, video a stabilnejšie audio bitrate. Päťciferná CAM revízia sa už v tomto okne zmestí.
- OSCam: hlavná ponuka a súhrn; zoznam čítačiek/proxy; r10 správne zobrazuje internal/active, vypnutú čítačku offline, cs378x/online aj emu/active. EMM stĺpce zodpovedajú dodanému HTML 11968.
- Entitlements po vložení fyzickej Irdeto karty: zobrazia sa štyri záznamy. Predtým bol Skylink iba prázdna čítačka. Obmedzenie entitlements pri cs378x je pôvodné správanie pluginu.
- Živý OSCam log: pribúdajú riadky a fungujú šípky.
- Konfiguračné súbory: zoznam a čítanie oscam.version, posúvanie textu. Aktuálna cesta z verzie: `/etc/tuxbox/config/oscam-uni/` (predtým oscam-stable), WebIf 8888.
- Používateľské skripty: zoznam siedmich pôvodných skriptov; Uptime_user.sh sa reálne vykonal a konzola oznámila dokončenie.
- Inštalácia IPK: zoznam našiel balík r10. Odinštalácia IPK: načíta zoznam nainštalovaných balíkov s verziami a posuvníkom. Samotná inštalácia/odinštalácia cez tieto okná sa neskúšala.
- Inštalácia TAR: okno sa otvorí; bez archívu zobrazí „Nenájdené žiadne súbory“. Rozbalenie neoverené.

## Presné miesto prerušenia a nasledujúci krok

Posledná snímka **1(20261024-194613).jpg**: samostatné okno **ECM Informácie**, nie veľké Informácie o kanáli. Načítané údaje (Irdeto, CAID, PID, reader/server, ECM Time) aj logo Irdeto. Neprenášať do dokumentácie CW hodnoty ani iné citlivé údaje zo snímky.

1. Ráno sa ešte opýtať, či sa v tomto okne priebežne mení **ECM Time**. Živé obnovovanie zatiaľ používateľ nepotvrdil.
2. Zaznamenaná oprava: v tomto samostatnom ECM okne je CAM verzia stále skrátená na `1196..`. Rozšíriť limit a/alebo dostupné miesto tak, aby bolo vidieť celú päťcifernú revíziu (napr. 11968), podobne ako už opravené Informácie o kanáli. Zatiaľ **neopravené**, nový IPK sa dnes nevydával.
3. Potom pokračovať ďalšou položkou hlavnej ponuky **CAM/SRV** a jej skutočnými obrazovkami. Neopakovať už potvrdené testy bez dôvodu.

## Zostávajúce hranice overenia

- CCcam transport bol opravený a testovaný na hostiteľovi; skutočný CCcam WebInfo na prijímači používateľ nemá. OSCam nie je CCcam WebInfo.
- OSCam klienti: prázdny zoznam, používateľ nemá vzdialených klientov; naplnený stav neoverený.
- Entitlements metadáta v hlavičke (n/a, neznáme názvy) nie sú potvrdené ako opravené.
- Enable/disable čítačiek, CAM reštart, balíkové operácie, TAR rozbalenie a ďalšie administratívne zásahy zatiaľ neoverené.
- Starý FTP aktualizátor ani produkčný automatický update nie sú týmto kandidátom vyhlásené za funkčné; kandidát nie je v produkčnom update feede.
- Pôvodné SD/FHD/UHD skiny a grafiku zachovať; žiadny nový dizajn počas obnovy.

## Ďalšia práca so zdrojom

Pred publikovaním vždy čerstvo načítať hlavu a strom vetvy, aktualizovať bez force/rebase s expected_sha. Po oprave spustiť primerané regresné testy pod Python 3.14.7 a deterministický build. Dokumentačný checkpoint nemení runtime, verziu ani existujúci r10 balík.

## Pokračovanie 25. 10. 2026 — r11

Samostatné ECM okno teraz používa ECMparser(cl=24), rovnako ako Informácie o kanáli. Pôvodné rozmery okna aj grafika sú zachované. Regresný test overuje obidve API časovača, 13 riadkov, plnú revíziu 11968, zmenu ECM Time pri ďalšom callbacku a zastavenie časovača po zatvorení. Spolu 28 testov úspešných pod Python 3.14.7. Pripravený kandidát 13.40-r11; zobrazenie plnej revízie a živú zmenu ECM Time musí ešte potvrdiť používateľ na prijímači. Potom pokračovať CAM/SRV. Historické údaje r10 vyššie označujú predchádzajúci večerný stav.

### Potvrdenie r11 a CAM/SRV

Tri snímky 1/2(20261025-003142).jpg a 3(20261025-003141).jpg potvrdzujú celú revíziu 11968 aj živé zmeny ECM Time 0.110, 0.108, 0.107. Samostatné ECM okno je týmto overené. CAM/SRV sa otvorí, ale starý správca hľadá iba UCM skripty a zobrazuje 0 CAM/SRV. Výpis prijímača potvrdil symlink `/etc/init.d/softcam -> /etc/init.d/softcam.oscam-uni`, dostupné softcam.None a softcam.oscam-uni. Pred zapojením ovládania čakáme na obsah softcam.oscam-uni. Lokálne rozpracovaná oprava CAID odstraňuje duplicity so zachovaním poradia; ešte nevydaná v IPK.

### Pripravené r12 — pôvodný správca a systémový SoftCAM

Používateľ dodal celý skript softcam.oscam-uni; potvrdil štart `/usr/bin/$CAM --config-dir /etc/tuxbox/config/$CAM ...`, PID súbor a akcie start/stop/restart/status. r12 uvádza aktuálne systémom zvolený SoftCAM ako CAM a zisťuje aktívny proces cez skutočný exe v /proc. Červené ho zastaví, zelené spustí alebo reštartuje. Vykonáva sa asynchrónne a úspech vyžaduje návratový kód aj očakávaný procesový stav. Symlink, systémové skripty ani výber OpenATV sa neprepisujú. Zoznam natívnych položiek pokrýva iba systémom zvolený SoftCAM; prepnutie na iný natívny balík zostáva správcovi image. Pôvodné UCM položky zachované. CAID sa už neopakujú. 37 hostiteľských testov úspešných; samotný runtime je presne reprodukovateľný transformáciou predchádzajúceho zdroja.

**Nasleduje:** nainštalovať r12, reštartovať GUI a overiť, že CAM/SRV ukáže oscam-uni ako aktívny CAM a zoznam CAID bez opakovania. SRV (0) je v tomto prípade očakávané, pretože OSCam beží cez systémový softcam, nie ako samostatný UCM SRV. Najprv overiť obrazovku; potom zelené pri označenom oscam-uni môže overiť reštart (krátky výpadok obrazu je očakávaný). Skutočné ovládanie na prijímači zatiaľ neoverené.

Názov CAM nie je napevno: testované oscam-uni, oscam-stable, oscam-custom aj my-softcam; podporený aj binárny symlink smerujúci na inak pomenovaný reálny súbor. Rozhoduje aktuálny systémový odkaz softcam a jeho zodpovedajúci súbor v /usr/bin.
