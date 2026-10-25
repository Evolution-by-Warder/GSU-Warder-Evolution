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
