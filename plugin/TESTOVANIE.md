# Aktuálny checkpoint — 26. 10. 2026, r56 publikované

## Projekt a vydávanie

Repozitár Evolution-by-Warder/GSU-Warder-Evolution. Jediné jadro: plugin/src/GlassSysUtil, všetky testy/build/grafické podklady/update sú v plugin/. main obsahuje aktuálny vyčistený projekt; original-python314 je pracovná a vydávacia vetva. Historická warder-master-production sa nemení. Bez force push/rebase; pred zápisom čítať aktuálny SHA a posúvať ref s expected_sha. Inštalačná identita/cesta zostáva enigma2-plugin-glasssysutil, Plugins/Extensions/GlassSysUtil; zobrazovaný názov GSU Warder Evolution sa neprekladá.

r55 zdrojf936e7e3b4c6c0953b9df865f44b76d4afb0945d, CI40222366028 úspešné vrátane kontroly skutočných vydaných bajtov.278 testov Python3.14.7 a dva identické buildy z čistého checkoutu. IPK3656778 B,SHA256cff650e7d526a4db388aa3a55a06d8e8598919182ee68340fa86feb37ae53ff4. Oba feedy overené na r55. Celý plugin nie je označený ako kompletne hardvérovo overený.

Nový updater číta plugin/update/candidate.json cez nový krátky názov repozitára. Existujúce r49 a staršie používajú restoration/update/candidate.json a presne overujú starý download URL; kompatibilný feed musí preto obsahovať pôvodný názov repository, ktorý GitHub presmeruje. Oba feedy musia zdieľať verziu/hash/veľkosť; nikdy ich nezmazať. Publisher ich aktualizuje až po kontrole vydaného IPK. Starý raw aj download URL bol po premenovaní overený ako HTTP200. Nová release title je GSU Warder Evolution.

Staré paralelné jadro src/, jeho testy/packaging, staré roadmapy/workflow a dokončené jednorazové konverzné skripty sú odstránené. Potrebné resources.tar.gz, manifests, pôvodné skiny a inventár sú súčasťou aktuálneho buildu/regresných testov, preto zostávajú. Pozor na plugin/.gitignore: nové locale/ a images/ sú výslovne povolené; prvé presunutie omylom vynechalo PNG, CI to zachytil a r50 opravil. Vždy overovať čistý checkout.

## Posledná požiadavka a r53

Používateľ potvrdil r51 zväčšenie ikoniek a zarovnanie spodných bargrafov snímkou1(20261025-175740).jpg a správou teraz to je OK. Snímka1(20261025-181813).jpg potom ukázala r52 slovenské systémové popisky; používateľ výslovne žiada ikonky NAD údajmi, ktoré symbolizujú. Snímka bola prezretá.

R53 systémové informácie: ikonky zachovávajú schválenú20% väčšiu veľkosť, pomery strán a horizontálne stredy; tri rady sú na y190/445/700 FHD, ich údaje na280/535/790. Pamäte sú nad pamäťovými údajmi, disky/karty nad úložiskami, teploty/CPU nad spodnými hodnotami. Pamäťové/diskové bargrafy aj podklady sa presúvajú spolu s údajmi. Spodné hddtempbar/hddstate/cpubar/tempDBbar aj podklady zostávajú zarovnané so spodkami ikoniek. Spodné texty majú58px a nezasahujú do protokolov. HD/FHD/UHD testy overujú odstupy, veľkosť, centrá, roviny údajov a zhodu podkladov. Pravé procesy/Dmesg, šípky, zber údajov a časovače sa nemenia. Používateľ následne žiadal iba posun protokolov; r54 rieši tento posun.

## Jazyky a Informácie o kanáli — r52 zachované

Spoločný i18n.py: jazyk config.osd.language,10 jazykov en/sk/cs/de/pl/hu/ru/fr/it/es, regionálna normalizácia, cache podľa jazyka/cesty, pôvodné cs/sk gettext ako fallback. Prepínač par62=False znamená angličtinu. Žiadna nová python3-gettext závislosť ani globálna zmena locale.129 spoločných kľúčov pre ponuky, ovládanie, aktualizácie, systém/kanál a základné hlášky; SK navyše zachováva staršie fallback texty. Chýbajúci preklad je anglický; netvrdiť úplný preklad všetkých historických dialógov. Presný rozsah a údržba sú v LOCALIZATION.md. Dni/mesiace hlavičky sú vo všetkých10 jazykoch. Nové source locale/*.json sú súčasťou IPK.

Informácie o kanáli už používajú spoločný Warder banner/header, názov služby, ECM/bitrate vľavo, picony/signál uprostred a transpondér vpravo, širokú referenciu dole a centrované červené ukončenie s krátkou čiarou. warder_channel.py zachováva všetky pôvodné pomenované komponenty a source/convert väzby, päť piconov, ECM/bitrate worker, pôvodné stop/close a klávesy. Samostatný header timer sa zatvára cez onClose. Nové testy overujú všetky3 rozlíšenia, zdroje, bounds, timer a oddelenie preložených popisov od živých hodnôt. Pôvodný timer test izoluje iba nový header. Používateľ túto kanálovú obrazovku výslovne schválil snímkou2(20261025-182832).jpg.

## Releases — dokončené

Na výslovný pokyn používateľa odstránených28 starých Releases workflow40220658958; po vydaní r53 odstránené aj nahradené r52 workflow40221152719. Obe úlohy success, API overilo iba v13.40-r53 s IPK a SHA256 súborom. Git tagy a história sa nemenili. cleanup_releases.py a samostatný workflow sú udržiavané nástroje pre prípad ďalšej výslovnej požiadavky. Mazanie vyžaduje explicitný zoznam ID/tagov a zhodu oboch live feedov, pred prvým DELETE sťahuje a kontroluje zachovaný IPK (hash/size/control). Neodstraňuje nevyžiadané, aktuálne ani novšie verzie. Spotrebovaný .github/release-cleanup.json je odstránený, takže nezostáva aktívny starý request.

## Zachovať potvrdené správanie a postup

Postupovať obrazovku po obrazovke. Systémové rozloženie r54 je schválené. Kanálový vzhľad tiež, s jedinou výhradou skráteného označenia CAM; r55 opravuje iba toto. Na prijímači teraz posúdiť iba celé označenie CAM, neopakovať už schválené vizuálne/funkčné skúšky. Ďalej postupovať sekciu po sekcii. Hlavné menu:11 stabilných ID, spoločný banner, biele živé sekundy, dvojriadková verzia, liveTV vpravo s popisom,4 centrované farebné akcie, modré O plugine. Používateľ potvrdil liveTV aj návrat celého TV obrazu. Nadpis Hlavná ponuka a spodný purpose riadok sú odstránené.

Systémové vrstvy pozadie/rám/panel sú-3/-2/-1; transparentné texty musia zostať viditeľné vrátane natívneho ScrollLabel parentu na nule. Používateľ potvrdil texty a všetky4 šípky. Schematické r47 ikonky odmietol; zachovať farebné plastické r48/r49 PNG s alpha bez čiernych dlaždíc/odrazov. Grafické masters v artwork sa neinštalujú.

Funkčný priechod uzavrel po r40. Nežiadať znovu skúšky potvrdených CAM štart/stop/prepínanie,15s autocheck/manuálny stop, OSD polohy, swap cleanup, diagnostického archívu, aktualizácií, čítačiek a šípok. Zakázať/Povoliť klienta zachovať bez automatického CAM reštartu; lokálne DVBAPI môže pokračovať ako anonymous, používateľ správanie prijal. CCcam/Mbox a samostatný SRV bez príslušnej služby nie sú hardvérovo overené. Starý nedôveryhodný FTP nikdy nepoužívať.

## r54 — posledná kozmetika systémovej obrazovky

Používateľ poslal1(20261025-182710).jpg (r53 systém) a2(20261025-182832).jpg (r52 kanál), obe prezreté. Výslovne potvrdil druhú obrazovku ako OK: kanálový Warder vzhľad je schválený. Pri systémovej žiada posunúť Protokoly o jeden riadok nižšie. R54 posúva všetky titulky protokolov a obe on/off stavové bodky o26 FHD px, proporcionálne HD/UHD. Zvislé prázdne textové bunky sa ohraničia spodkom panelu978; žiadne údaje ani detekcia služieb sa nemenia. Nové obrázky ani funkčné zmeny nepribúdajú.

R54 publikované a oba feedy overené. Používateľ následne upresnil, že myslí CELÝ blok Protokoly vrátane FTP/Telnet/VPN/Samba/NFS a farebných ukazovateľov pod nimi. Implementácia už od začiatku zahŕňa všetky titulky aj oba on/off stavy každej bodky; všetko sa posúva o jeden textový riadok spoločne. FHD titulky y884, bodky y918–943; spodok panelu978 má rezervu. HD/UHD pomerné polohy overené;277 testov aj CI success. Druhá dodaná obrazovka Informácie o kanáli je výslovne schválená ako OK, nemení sa.

Po vydaní r54 odstránené aj nahradené r53, cleanup workflow40221709652 success. API overilo iba v13.40-r54; spolu odstránených30 starých vydaní, Git tagy/história zachované. Spotrebovaný request odstránený.

## r55 — celé označenie CAM

Používateľ potvrdil systémovú obrazovku r54 snímkou1(20261025-183534).jpg a textom1 beriem. Druhú kanálovú obrazovku tiež schvaľuje s jedinou opravou: zobraziť celý CAM názov/verziu. Snímka2(20261025-183534).jpg prezretá, viditeľné OScam (2.26.09-11968-8..). Príčinou je predčasné cutMe nad oscVersion v ECMparser(cl=24), nie chýbajúce dáta z OSCamu. Pre kanálový readEcmInfo sa pridáva keyword-only full_cam=True; pôvodný positional interface a limity ostatných polí aj správanie ostatných volaní zostávajú. Reálny parser test číta ecm.info a version a kontroluje celú2.26.09-11968-802 aj zhodu ostatných polí s pôvodným výsledkom. Rozloženie, fonty a ostatné obrazovky sa nemenia.

R55 vydané:278 testov Python3.14.7 z čistého checkoutu, dva zhodné IPK3656778 B,SHA256cff650e7d526a4db388aa3a55a06d8e8598919182ee68340fa86feb37ae53ff4, zdrojf936e7e3b4c6c0953b9df865f44b76d4afb0945d, CI40222366028 success. Oba feedy overené na r55. Test overuje skutočné čítanie plnej verzie; nejde iba o mockovaný výstup. Pôvodný positional signature ECMparser(cl) je zachovaný, nový prepínač je keyword-only. Celý parserov výsledok okrem CAM verzie je zhodný s pôvodným režimom. Prvá systémová fotografia bola tiež prezretá a jej schválenie je zapísané; kanálová obsahuje aj video/audio bitrate hodnoty. R55 CAM text ešte treba vidieť na prijímači.

Nahradené r54 odstránené workflow40222445982 success; API overilo iba v13.40-r55. Spolu odstránených31 starých vydaní. Spotrebovaný request zmazaný, Git tagy a história zachované.


## r56 – OSCam v dvoch paneloch (26. 10. 2026)

Používateľ prijal r55 a žiada pokračovať OSCamom. Ponuka je vpravo namiesto LiveTV,
úvodné údaje prijímača/OSCam/štartu/uptime vľavo. Výsledky vrátane súborov a oprávnení
zostávajú vľavo v jednom natívnom Screen; pôvodné kontroléry a ich funkcie sú zachované.
Vľavo fungujú pôvodné akcie; doprava prepne ovládanie do ponuky, doľava späť.
Späť z výsledku -> úvod OSCamu -> hlavná ponuka s LiveTV. Skryté časovače a ActionMap
sú vypnuté; oneskorené dialógové callbacky po zatvorení sú ignorované.
Rozpracované lokálne súbory predchádzajúceho prostredia sa nezachovali; implementácia
bola znovu vytvorená nad presným publikovaným r55. Hostiteľské testy nenahrádzajú
kontrolu kreslenia/fokusu na prijímači. Aktuálne čaká na prijímačové overenie.

289 testov Python 3.14.7 prešlo aj z čistého checkoutu. Dva identické IPK buildy: 3662346 B, SHA256 90aa221dc7c3fa1e7077240492e18819987209f9ce713cd0daec140981d34c9b.

Publikované: zdroj 88a4ffbe012c8abe1e3b0b10fd16ad04d82a98df; CI40271924200 (original) a CI40271928990 (main) success. Oba feedy majú r56, 3662346 B a zhodný SHA256. Vizuál a fokus na prijímači ešte neoverené.

Nahradené vydanie r55 odstránené workflow40272024725 success. API overilo iba v13.40-r56; spolu odstránených32 starých vydaní, tagy/história zachované. Spotrebovaný request zmazaný.
