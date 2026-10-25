# Aktuálny checkpoint — 25. 10. 2026, r51 publikované

## Repozitár a zostavenie

Repozitár: Evolution-by-Warder/GSU-Warder-Evolution. Jediné aktívne jadro: plugin/src/GlassSysUtil. main obsahuje aktuálnu vyčistenú štruktúru; originál pracovnej vetvy a vydávanie sú v original-python314. Nepoužívať staré alternatívne jadrá, force push ani rebase. Historická warder-master-production sa nemení. Inštalačné meno/cesta zostávajú kompatibilné: enigma2-plugin-glasssysutil, Plugins/Extensions/GlassSysUtil.

Staré paralelné src/, tests/, packaging/, legacy/, roadmapy, dva nepoužívané workflow a dokončené konverzné skripty sú odstránené. História zostáva v Gite. Potrebné resources.tar.gz, kontrolné súčty, pôvodné skiny a inventár sú súčasťou súčasného buildu/testov a nesmú sa zmazať. Výrobné grafické podklady sú v plugin/artwork, do IPK idú iba malé runtime PNG.

Nový updater používa nový názov a plugin/update/candidate.json. Existujúce r49 a staršie overujú presne pôvodnú repository URL: restoration/update/candidate.json preto obsahuje pôvodný download URL, ktorý GitHub presmeruje. Oba feedy musia mať rovnakú verziu, SHA256 a veľkosť. Publisher ich zapíše až po kontrole skutočne vydaných bajtov. Stará raw adresa aj staré sťahovanie boli po premenovaní overené ako HTTP200. Pri presune CI zachytil ignorované grafické súbory; sú doplnené a .gitignore ich výslovne povoľuje. Pred publikáciou overovať čistý checkout.

## Posledné vydanie

13.40-r51: zdroj55211bff644f0881a928cc9427f193459e890df5, CI40218557443 úspešné vrátane vzdialenej kontroly vydaného IPK a aktualizácie feedov. 261 testov Python3.14.7 úspešných; dva zhodné buildy. IPK3639866 B, SHA2568dee8f6830d88bbe165f6b751ce4f25281f56125d986e4bc152de6fff31604ef. Celý plugin receiver_tested=false; nejde o tvrdenie o všetkom hardvéri.

Systémové ikonky sú zväčšené o20%, zachovávajú pomery strán, stredy a vyhradený zvislý priestor. Spodné hddtempbar, hddstate, cpubar a tempDBbar aj ich podklady sú presunuté tak, aby ich spodky boli zarovnané so spodkami príslušných ikoniek. Test kontroluje HD/FHD/UHD, medzeru medzi ikonou a bargrafom, vycentrovanie a spoločnú hranu podkladu. Šípky a stavové bodky sa nemenia. Snímka1(20261025-172724).jpg bola prezretá ako podklad; nový r51 vzhľad ešte nie je overený na prijímači. Používateľ dovolil nezväčšiť ikonky, ak by nebol priestor; v terajšom rozložení sa zmestia.

## Ďalšia úloha — jazyky

Používateľ žiada jazykovú podporu podľa jazyka systému vrátane dní/mesiacov v hlavičke: slovenčina, čeština, angličtina, nemčina, poľština, maďarčina, ruština, francúzština, taliančina a španielčina. Chýbajúci preklad má používať angličtinu. Názov GSU Warder Evolution neprekladať. Overiť aj dlhé texty, zarovnanie hlavičky a tlačidlá. Toto NIE JE implementované vydaním r51.

Súčasný stav lokalizácie: v resources.tar.gz sú pôvodné gsu.po/mo pre cs/sk; plugin.py priraďuje gettext pri importe podľa config.osd.language/par62. Nové UI moduly majú miestne slovenské fallback slovníky. warder_main.py už má dni a mesiace pre všetkých10 jazykov, ale ostatné texty ešte nie. Niektoré popisky pôvodných skinov sú statické anglické XML texty. Zjednotiť mechanizmus, preklady pribaliť bez novej python3-gettext závislosti, nezmeniť globálne locale procesu.

## Zachovať potvrdené správanie

Postupovať sekciu po sekcii; nepreskakovať medzi nimi. Hlavné menu:11 stabilných ID, spoločný banner, živý dátum/čas s bielymi sekundami, dvojriadková verzia, liveTV vpravo a popis pod ním,4 centrované farebné akcie, modré O plugine. Nadpis Hlavná ponuka a spodný purpose riadok odstránené. Používateľ potvrdil liveTV a obnovu celého TV obrazu po zatvorení.

Informácie o systéme: pozadie/rám/panel vo vrstvách-3/-2/-1 a transparentné texty. Používateľ potvrdil texty, procesy/Dmesg a všetky4 šípky. Schématické ikony r47 odmietol; r48/r49 používajú farebné plastické predmety/šípky s alpha bez čierneho pozadia. Neobnovovať odmietnuté SVG ani negenerovať nové predmety pre geometrické úpravy.

Funkčný priechod používateľ uzavrel po r40. Nežiadať znovu skúšky potvrdených CAM štart/stop/prepínanie,15s autocheck/manuálny stop, OSD polohy, swap test-cleanup, diagnostického archívu, aktualizácií, OSCam čítačiek a šípok. Zakázať/Povoliť klienta zachovať bez automatického CAM reštartu; živé lokálne DVBAPI môže pokračovať ako anonymous, používateľ toto správanie prijal. Skutočné CCcam/Mbox a samostatný SRV bez príslušnej služby nie sú hardvérovo overené. Nepripájať starý nedôveryhodný FTP.

## r52 — jazyky a Informácie o kanáli

Používateľ potvrdil r51 vzhľad na prijímači správou „teraz to je OK“, snímka1(20261025-175740).jpg. Veľkosť ikoniek a spodné bargrafy sú schválené, neotvárať ich znovu bez nového problému.

Nový i18n.py má cachované katalógy10 jazykov,129 spoločných kľúčov a rozšírený SK fallback; pôvodné cs/sk gettext zostávajú. UI používa spoločný mechanizmus, rešpektuje par62, neznáme/chýbajúce texty sú anglické. Dni/mesiace bez globálnej zmeny locale. Nie všetky staré dialógy sú kompletne preložené; presný rozsah je v LOCALIZATION.md.

Informácie o kanáli prevedené do spoločného Warder rámu: banner/header, názov služby, oddelené ECM/bitrate, logá/signal a transpondér, široká referencia dole, centrované červené ukončenie s krátkou čiarou. Zachované všetky pôvodné pomenované komponenty a natívne source/convert väzby, päť piconov, čítanie ECM/bitrate, stop/close a klávesy. Samostatný header timer sa zastaví pri zatvorení. Pôvodný funkčný timer test izoluje nový header, nové testy overujú jeho lifecycle a rozloženie HD/FHD/UHD. Nový vzhľad a jazyky treba posúdiť na prijímači.
