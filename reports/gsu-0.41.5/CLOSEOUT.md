# GSU Warder Evolution 0.41.5

## Vydanie a aktualizácia

Verejný tag v0.41.5 ukazuje na 30a420d5019446c1b33f48fe586addc5f9ead153. OPKG eviduje 1:0.41.5 s identitou enigma2-plugin-extensions-gsu-warder-evolution. Inštalačný adresár je Plugins/Extensions/GlassSysUtil. [Vydanie a súbory](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/releases/tag/v0.41.5)

| Overená položka | Výsledok |
|---|---|
| Verejný IPK | 3 873 060 bajtov |
| SHA-256 IPK | 115bc57d4c842049d72864a0e2deaf0eceb35f0bb7d53f515cc5533e9abc48fc |
| Súčet veľkostí rozbalených regulárnych súborov | 6 500 779 bajtov |
| Alokácia súborov po inštalácii OPKG v CI | 7 073 792 bajtov vo všetkých troch izolovaných inštaláciách |
| Aktivácia stabilného moderného feedu | fac1e9a9a9a7ab022f75361dc0af94b0c44e80b2 |
| Pôvodný most 13.41-r6 | 3 813 348 bajtov, SHA-256 a8e79609147666b27f18460b3340e099bb013664478a787746bcf56bb28052e2 |

Produkčný workflow zopakoval zostavenie, inštaláciu a migrácie na zlúčenom commite. Verejný balík aj súbor .sha256 porovnal s testovanými bajtmi pred aktiváciou moderného feedu. Pôvodné feedy na main a original-python314 ponúkajú r6. Historické migračné feedy ponúkajú r93. Aktualizátor z reálneho r6 akceptoval nový balík. Skúšky začínali zvlášť zo zverejnených r93, 13.41-r4 a 13.41-r5. Pri zmene identity overovali aj zachovanie nastavenia. [Publikácia](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/actions/runs/45786453936) · [Overenie verejných bajtov](public-verification.json)

## Funkcie a obrazovky

| Centrum | Obsah a ovládanie |
|---|---|
| Systém | Šesť kariet s CPU, RAM, swapom, voľnou flash, externým diskom a teplotou. Skóre zdrojov uvádza pokrytie. Živé grafy CPU, RAM, swapu, teploty a sieťového prenosu majú minútovú históriu, pozastavenie a interval 1/2/5 s. Samostatné okná procesov a logu, triedenie CPU/RAM a voliteľné upozornenia pri otvorení. |
| Príjem | Plávajúci merač nad TV, voliteľný zvuk, SNR/AGC/BER/dB/LOCK, štatistika a výpadky zámku, export CSV. Kanál a bitrate, parametre transpondéra, MIS/PLS/T2-MI, PID, audio, HDR/HLG a HDMI podľa podpory. Pasívny výber tunera, FBC a nahrávania. Natívny SatFinder, ručné ladenie, motor a blindscan sa otvárajú podľa možností image. Overená miestna záloha staníc, ochrana nahrávania a timeshiftu, náhľad služieb a oddelený export TV/rádio bouquetu. |
| Pamäť a úložisko | Voľné miesto a swap, dynamické mounty, SMART a teploty podľa disku. Ohraničená analýza piconov, skinov, pluginov, EPG, cache a logov. Odporučené umiestnenie piconov. Čiastočné výsledky sú označené. |
| Sieť | Rozhrania a rýchlosť linky, IP, brána, DNS, ping a strata paketov. Oddelená kontrola lokálnej brány, oficiálneho webu a aktualizačného feedu, sieťové mounty a osem posledných ručných meraní v otvorenom okne. |
| CAM / ECM | Modernizované panely s pôvodným ovládaním OSCam, CCcam a Mbox podľa dostupnej služby. Zostávajú dostupné správa CAM/SRV, ECM, OSD, klienti, čítačky a nastavenia. |
| Servis | Súbory a preklady proti inštalačnému manifestu, závislosti z OPKG alebo dpkg, kontrola metadát miestnych IPK a identifikácia inštalačných skriptov bez ich spustenia. Vybrané výnimky z crashlogov s odporúčaniami. Anonymný JSON má náhľad a výslovné miestne uloženie. Pôvodný podrobný balík je samostatne dostupný v Nástrojoch. |
| Warder Evolution | Stránky pre FullHDGlass, PiconHub, Radio, YouTube a GSU. Nainštalovaná verzia, dostupný oficiálny release, stav, kontrola miestnych závislostí a poznámky. Používateľ vstupuje do nainštalovaného projektu alebo priamo do kanonického aktualizátora GSU. |

Hlavné menu, diagnostické detaily, grafy aj kompaktné meranie používajú ovládanie diaľkovým ovládačom. Technické údaje sú dostupné po otvorení detailu. História má pevné limity, čítanie súborov a siete prebieha mimo GUI a obrazovky pri zatvorení zastavia svoje časovače. Živé grafy používajú natívne Canvas rozhranie Enigma2. [Používanie a obnova staníc](../../docs/POUZIVANIE.md) · [Referenčný audit vrátane Pulse Dashboard](../../docs/GSU-0.41.5-REFERENCE-AUDIT.md)

## Overenie a hranice výsledkov

Na presnom HEAD b90807a0a4a56a4fb36437fe1978ca00aaa33e54 prešlo 17 kontrol v piatich workflowoch. Regresná sada obsahuje 467 testov. Kontroly zahŕňali Python 3.9 a 3.14, OpenATV 8.0/8.0-next/master, OpenPLi release-9.2/develop a aktuálne diagnostické rozhrania OpenBH Python3.14. Pre 21 jazykov sa porovnali rozmery 3 024 textov tlačidiel a ponúk v štyroch rozlíšeniach s referenčným písmom. [PR #16](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/pull/16) · [Matica CPU a OpenBH](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/actions/runs/45785631262) · [Reprodukcia, alokácia a migrácie](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/actions/runs/45785631498)

| Prostredie | Priemer jedného odčítania | Maximum | CPU za 12 odčítaní |
|---|---:|---:|---:|
| x86_64, natívny CI runner | 0,836 ms | 5,149 ms | 6,258 ms |
| AArch64, natívny CI runner | 0,442 ms | 0,611 ms | 6,170 ms |
| ARMv7, QEMU | 3,278 ms | 12,628 ms | 41,217 ms |
| MIPS big-endian, QEMU | 3,607 ms | 15,787 ms | 40,888 ms |
| MIPSEL little-endian, QEMU | 3,357 ms | 13,923 ms | 39,679 ms |

Interval bol jedna sekunda. Meral sa čítací modul pri otvorenej diagnostike. Na AArch64 mal celý merací proces špičku RSS 14 312 KiB. Reálna spotreba pamäte GUI Enigma2, alokácia na flash a čas čítania senzorov sa líšia podľa prijímača a súborového systému.

Fyzické prijímače neboli počas prípravy 0.41.5 pripojené. Živý RF príjem, motor, blindscan, HDMI výstup, zvuk, konkrétne CAM služby a výsledný obraz na televízore preto nemajú fyzické overenie. Databázový náhľad transpondéra zobrazuje už evidované služby. Novonájdené služby zobrazuje príslušný natívny scanner. LinuxSat verejne potvrdil Pulse Dashboard 1.0 a údaje autora. Jeho IPK vyžadoval prihlásenie. Úplná funkčná parita s referenciami sa nepotvrdzovala.

## Oficiálny web

Existujúci [PR #44](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/pull/44) zosúladil katalóg aj produktový detail v slovenčine, angličtine, nemčine a ruštine. Prešli obsahové testy aj prehliadačové skúšky rozložení. GitHub Pages úspešne nasadil commit ae4cfd43707860e843edc98f22e2dbfc1b028e93. Popis galérie označuje snímky predchádzajúcej generácie rozhrania. [Nasadenie Pages](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/actions/runs/45788135168) · [Živý web GSU](https://warder-evolution.eu/gsu.html)

[Verejná kontrola vydania a oboch stránok po nasadení](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/actions/runs/45788582576).
