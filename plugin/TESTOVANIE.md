# Aktuálny checkpoint — 25. 10. 2026, r53 publikované

## Projekt a vydávanie

Repozitár Evolution-by-Warder/GSU-Warder-Evolution. Jediné jadro: plugin/src/GlassSysUtil, všetky testy/build/grafické podklady/update sú v plugin/. main obsahuje aktuálny vyčistený projekt; original-python314 je pracovná a vydávacia vetva. Historická warder-master-production sa nemení. Bez force push/rebase; pred zápisom čítať aktuálny SHA a posúvať ref s expected_sha. Inštalačná identita/cesta zostáva enigma2-plugin-glasssysutil, Plugins/Extensions/GlassSysUtil; zobrazovaný názov GSU Warder Evolution sa neprekladá.

r53 zdroj0b2baaeddb16268253b0c025529372700b68bcad, CI40221037539 úspešné vrátane kontroly skutočných vydaných bajtov.277 testov Python3.14.7 a dva identické buildy z čistého checkoutu. IPK3656708 B,SHA25679d8ab669d8c546e919bf95d4b972874dffad3fd341221e3a46049370d969cba. Oba feedy overené na r53. Celý plugin nie je označený ako kompletne hardvérovo overený.

Nový updater číta plugin/update/candidate.json cez nový krátky názov repozitára. Existujúce r49 a staršie používajú restoration/update/candidate.json a presne overujú starý download URL; kompatibilný feed musí preto obsahovať pôvodný názov repository, ktorý GitHub presmeruje. Oba feedy musia zdieľať verziu/hash/veľkosť; nikdy ich nezmazať. Publisher ich aktualizuje až po kontrole vydaného IPK. Starý raw aj download URL bol po premenovaní overený ako HTTP200. Nová release title je GSU Warder Evolution.

Staré paralelné jadro src/, jeho testy/packaging, staré roadmapy/workflow a dokončené jednorazové konverzné skripty sú odstránené. Potrebné resources.tar.gz, manifests, pôvodné skiny a inventár sú súčasťou aktuálneho buildu/regresných testov, preto zostávajú. Pozor na plugin/.gitignore: nové locale/ a images/ sú výslovne povolené; prvé presunutie omylom vynechalo PNG, CI to zachytil a r50 opravil. Vždy overovať čistý checkout.

## Posledná požiadavka a r53

Používateľ potvrdil r51 zväčšenie ikoniek a zarovnanie spodných bargrafov snímkou1(20261025-175740).jpg a správou teraz to je OK. Snímka1(20261025-181813).jpg potom ukázala r52 slovenské systémové popisky; používateľ výslovne žiada ikonky NAD údajmi, ktoré symbolizujú. Snímka bola prezretá.

R53 systémové informácie: ikonky zachovávajú schválenú20% väčšiu veľkosť, pomery strán a horizontálne stredy; tri rady sú na y190/445/700 FHD, ich údaje na280/535/790. Pamäte sú nad pamäťovými údajmi, disky/karty nad úložiskami, teploty/CPU nad spodnými hodnotami. Pamäťové/diskové bargrafy aj podklady sa presúvajú spolu s údajmi. Spodné hddtempbar/hddstate/cpubar/tempDBbar aj podklady zostávajú zarovnané so spodkami ikoniek. Spodné texty majú58px a nezasahujú do protokolov. HD/FHD/UHD testy overujú odstupy, veľkosť, centrá, roviny údajov a zhodu podkladov. Pravé procesy/Dmesg, šípky, zber údajov a časovače sa nemenia. Nové r53 rozloženie ešte čaká na posúdenie na prijímači.

## Jazyky a Informácie o kanáli — r52 zachované

Spoločný i18n.py: jazyk config.osd.language,10 jazykov en/sk/cs/de/pl/hu/ru/fr/it/es, regionálna normalizácia, cache podľa jazyka/cesty, pôvodné cs/sk gettext ako fallback. Prepínač par62=False znamená angličtinu. Žiadna nová python3-gettext závislosť ani globálna zmena locale.129 spoločných kľúčov pre ponuky, ovládanie, aktualizácie, systém/kanál a základné hlášky; SK navyše zachováva staršie fallback texty. Chýbajúci preklad je anglický; netvrdiť úplný preklad všetkých historických dialógov. Presný rozsah a údržba sú v LOCALIZATION.md. Dni/mesiace hlavičky sú vo všetkých10 jazykoch. Nové source locale/*.json sú súčasťou IPK.

Informácie o kanáli už používajú spoločný Warder banner/header, názov služby, ECM/bitrate vľavo, picony/signál uprostred a transpondér vpravo, širokú referenciu dole a centrované červené ukončenie s krátkou čiarou. warder_channel.py zachováva všetky pôvodné pomenované komponenty a source/convert väzby, päť piconov, ECM/bitrate worker, pôvodné stop/close a klávesy. Samostatný header timer sa zatvára cez onClose. Nové testy overujú všetky3 rozlíšenia, zdroje, bounds, timer a oddelenie preložených popisov od živých hodnôt. Pôvodný timer test izoluje iba nový header. Používateľ túto kanálovú obrazovku zatiaľ samostatne neposúdil.

## Releases — dokončené

Na výslovný pokyn používateľa odstránených28 starých Releases workflow40220658958; po vydaní r53 odstránené aj nahradené r52 workflow40221152719. Obe úlohy success, API overilo iba v13.40-r53 s IPK a SHA256 súborom. Git tagy a história sa nemenili. cleanup_releases.py a samostatný workflow sú udržiavané nástroje pre prípad ďalšej výslovnej požiadavky. Mazanie vyžaduje explicitný zoznam ID/tagov a zhodu oboch live feedov, pred prvým DELETE sťahuje a kontroluje zachovaný IPK (hash/size/control). Neodstraňuje nevyžiadané, aktuálne ani novšie verzie. Spotrebovaný .github/release-cleanup.json je odstránený, takže nezostáva aktívny starý request.

## Zachovať potvrdené správanie a postup

Postupovať obrazovku po obrazovke. Teraz posúdiť r53 systémové rozloženie a potom už pripravené Informácie o kanáli; nepreskakovať do ďalšej funkčnej sekcie. Hlavné menu:11 stabilných ID, spoločný banner, biele živé sekundy, dvojriadková verzia, liveTV vpravo s popisom,4 centrované farebné akcie, modré O plugine. Používateľ potvrdil liveTV aj návrat celého TV obrazu. Nadpis Hlavná ponuka a spodný purpose riadok sú odstránené.

Systémové vrstvy pozadie/rám/panel sú-3/-2/-1; transparentné texty musia zostať viditeľné vrátane natívneho ScrollLabel parentu na nule. Používateľ potvrdil texty a všetky4 šípky. Schematické r47 ikonky odmietol; zachovať farebné plastické r48/r49 PNG s alpha bez čiernych dlaždíc/odrazov. Grafické masters v artwork sa neinštalujú.

Funkčný priechod uzavrel po r40. Nežiadať znovu skúšky potvrdených CAM štart/stop/prepínanie,15s autocheck/manuálny stop, OSD polohy, swap cleanup, diagnostického archívu, aktualizácií, čítačiek a šípok. Zakázať/Povoliť klienta zachovať bez automatického CAM reštartu; lokálne DVBAPI môže pokračovať ako anonymous, používateľ správanie prijal. CCcam/Mbox a samostatný SRV bez príslušnej služby nie sú hardvérovo overené. Starý nedôveryhodný FTP nikdy nepoužívať.
