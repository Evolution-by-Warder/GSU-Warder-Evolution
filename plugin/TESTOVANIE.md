# Aktuálny checkpoint — 26. 10. 2026, r74 spodný editor

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


## r57 – oprava pádu pri otvorení OSCamu

Prijímačový log 20261026-060718-enigma2-crash.log potvrdil pád r56:
Screen.createGUIScreen -> exec(method, ...) -> TypeError, pretože onLayoutFinish
obsahoval lambda funkciu. OpenATV rozlišuje viazanú metódu a text skriptu podľa
isinstance(method, type(self.close)). Opravené na self.begin; výber servera je uložený
v atribúte. Regresný test vykonáva identické rozlišovanie všetkých callbackov.
Žiadna zmena rozloženia alebo OSCam akcií. 290 testov Python3.14.7 aj v čistom
checkoute prešlo, dva identické buildy:3662198 B, SHA256
e97f9f0670497216b9bfd055eae3865525b327683915393d9aa36f5172ac5ae8.
Prijímačové potvrdenie opravy zatiaľ chýba.

Publikované r57: zdroj ea928644f332a566cc537aff128f7edc59fd4975, CI40272777670 success. Oba feedy overené: r57 / 3662198 B / zhodný SHA256 vyššie.

Chybné vydanie r56 odstránené workflow40272834229 success. API overilo iba r57; spolu33 odstránených vydaní, tagy a história zachované. Spotrebovaný request zmazaný.


## r58 – ovládanie ľavého panelu OSCamu

Snímky 1(20261026-051447).jpg a 1(20261026-051540).jpg potvrdzujú otvorenie r57
bez predchádzajúceho pádu a správne zobrazenie úvodu/súhrnu. Používateľ hlási,
že pohyb zostal vpravo. Root ActionMap teraz vždy spotrebuje up/down a volá
priamo up/down aktívneho MenuList alebo pageUp/pageDown ScrollLabel. Žiadne
prenechanie šípok natívnemu spoločnému fokusu viacerých listboxov. Pravá ponuka
sa nemení pri pohybe vo výsledkoch. selectionEnabled je zapnuté iba pre aktívny
panel; ostatné zoznamy nevykresľujú výber. Doprava/doľava menia panel, pôvodné
farebné akcie ostávajú. Testy pokrývajú šesť ľavých zoznamov, text súboru a obe
strany prepínania. 293 testov aj z čistého checkoutu, zhodné dva buildy3662312 B,
SHA256 5a5d11fab40dcb8ec1f9261bce4c46a9deaf150ffaceca3f3fdd4af9271997a5.
Zatiaľ čaká na potvrdenie ovládania na prijímači.


## r59 – pravá ponuka predvolená podľa používateľa

Používateľ upresnil: predvolene hore/dole vpravo, doľava aktivuje ľavý panel,
doprava opäť pravý. Toto nahrádza automatické prepínanie doľava po otvorení výsledkov.
Výber výsledkov teraz ponechá pravú ponuku aktívnu. Súbor/oprávnenia otvorené zľava
ostávajú vľavo, návrat zachová predchádzajúci fokus. Stále sa používa priame smerovanie
up/down z r58 a iba jeden zvýraznený zoznam. 294 testov Python3.14.7, dva identické
čisté buildy3662394 B, SHA256 f77736521d21b97318be84ae26fc37e34c7f9bbd882f79319eb500d0687482fb.
Prijímačové potvrdenie ovládania zatiaľ chýba. r58 vydané zdrojom
1c6fb01e71dc55691b6c93875837927ae0860ede, CI40273485815 success, oba feedy overené.
Staré r57 odstránené workflow40273582391 success; API overilo iba r58 (spolu34 odstránení).

Publikované r59: zdroj c1e868bcb43abd32b0e8107b74934976d86b34d9, CI40273740657 success. Oba feedy overené na r59 / 3662394 B / SHA256 vyššie.

Nahradené r58 odstránené workflow40273822150 success; API overilo iba r59 (spolu35 odstránení). Spotrebovaný request zmazaný, tagy a história zachované.


## r60 – jednotné zvýraznenie v celom GSU

Snímky r59 1(20261026-052831).jpg,2(20261026-052903).jpg potvrdili pohyb medzi
čítačkami a aktualizáciu počítadiel. 1(20261026-053031).jpg a snímky 053157/053158
potvrdili oprávnenia, posun a návrat do čítačiek. Presvitanie LiveTV sa vyskytuje
na výbere; používateľ vyžaduje rovnaké nepriehľadné modré zvýraznenie ako hlavné
menu v celom plugine. warder_main.style_lists raz upraví importované vlastné skiny
pred definíciou Screen tried: zoznamy list/config/devices/txt/log_info/entitlements_list.
Mení iba farby výberu; systémový skin ani globálny Enigma štýl sa nemení.
Dynamické OSCam zoznamy používajú tú istú konštantu. Testy overujú každý listový
widget všetkých troch skinových rozlíšení aj reálne exporty pluginu.
Texty kariet odsadené od ikon, interné TypeCRD/CAIDcrd normalizované na Type/CAID.
297 testov prešlo aj v čistom checkoute, dva identické buildy3662806 B, SHA256
ce297ce3a193c3a148dcffa24e1082b3ca288f22f34358e6695143a3cfa0af41.
Vizuálne potvrdenie r60 na prijímači zatiaľ chýba.

Publikované r60: zdroj b825858a6b8548c2cfe3d78ec7bd197f7222fd7c, CI40275205808 success. Oba feedy overené r60 / 3662806 B / SHA256 vyššie.

Nahradené r59 odstránené workflow40275325752 success; API overilo iba r60 (spolu36 odstránení). Spotrebovaný request zmazaný, tagy/história zachované.


## r61 – OK v ľavých výsledkoch nesmie zatvárať panel

Snímky r60 054154 potvrdili nepriehľadné modré zvýraznenie na oboch stranách aj
odsadenie ikon v oprávneniach. Snímky054326 potvrdili klienta Gigablue a živé údaje,
ale OK vyvolalo starý oscam_Users.exit a vrátilo úvod OSCamu. Root choose teraz OK
spotrebuje pre users/summary/log/file/entitlements. Users a summary aktualizujú
podrobnosti vybraného riadka; žiadne nové vymyslené detailné okno. Readers/files
ďalej prepúšťajú OK pôvodnej akcii otvárajúcej oprávnenia alebo súbor.
Návrat cez červené a prepínanie doľava/doprava ostávajú.
299 testov Python3.14.7 aj v čistom checkoute, dva identické buildy3662832 B,
SHA256 2fd4189f5ca92fe9942de68f83f1aed6829e39979df21b018345b6705593fdb0.
Prijímačové potvrdenie OK zatiaľ chýba.

Publikované r61: zdroj b0fe5e758aa95ae199017c0bad20f2de33c21733, CI40275956332 success. Oba feedy overené r61 / 3662832 B / SHA256 vyššie.

Nahradené r60 odstránené workflow40276053192 success; API overilo iba r61 (spolu37 odstránení). Spotrebovaný request zmazaný, tagy/história zachované.


## r62 – lokálny DVBAPI re-enable a návrat k automatickému ľavému panelu

Používateľ potvrdil OK klientov, log vrátane zachovania pozície pri obnovení,
konfiguračné súbory/posun/návrat a obnovenie LiveTV po odchode. Sekcia r61 prejdená.
Povoľovanie/zakazovanie čítačiek aj účtov overené. Snímky060516 ukazujú, že zákaz
Gigablue prepne DVBAPI na anonymous; povolený účet zostáva offline až do reštartu.
Používateľ výslovne schválil automatický reštart iba pri povolení lokálneho DVBAPI.
Nový worker overuje loopback URL, skutočný zvolený bežiaci proces, jeho config-dir
z argv (alebo PID-overeného oscam.version), [dvbapi] enabled/user a presný WebIF
port/schéma. Najprv musí API potvrdiť povolenie, potom sa pod rovnakým command_lock
ako CAM správca vykoná NativeSoftcam.restart_verified. Po spustení sa mimo GUI
čaká najviac20s (+ timeout jednotlivého HTTP volania) na pôvodné DVBAPI meno,
potom sa načíta čerstvý zoznam. Žiadne filtrovanie anonymous ani falošné dáta.
Zakázanie, iné účty a vzdialené endpointy sa nereštartujú. Zmena výberu CAM alebo
chyba/timelimit sa hlási ako už povolený účet s neúspešnou obnovou, nie úspešný reštart.
Ovládanie podľa nového upresnenia používateľa: v CELEJ sekcii Informácie o OSCame
OK vpravo automaticky aktivuje ľavý obsah, doprava vracia ponuku a doľava výsledky.
To nahrádza pravidlo r59 (pravá ponuka ostáva po OK). Vnorené návraty zachovajú fokus.
310 testov Python3.14.7 aj z čistého checkoutu. Dva identické buildy3664744 B,
SHA256 ff83872e39c25981437850b2c88016483c77b1843d3e4ef04ce2d05db4188f24.
Reštart/obnova potrebuje potvrdenie na prijímači. Celý plugin receiver_tested=false.
Používateľ navrhol jemnú priehľadnosť oboch OSCam panelov; zatiaľ diskusia,
v r62 bez zmeny pozadia. Odporúčané10% priehľadné tmavé panely, nepriehľadný výber.


## r63 – jemne priehľadné OSCam panely

r62 publikované zdrojom cd2febe5ddc260fb9e260091b4a1f943397f439d,
CI40279007494 success; oba feedy overené. Používateľ následne výslovne potvrdil:
„vyskusal to zakazovanie a povolovanie klinta dvbapi, pekne to funguje“.
DVBAPI obnova je teda prijímačovo overená v r62; nereprodukovať tento test zbytočne.
Používateľ schválil jemnú priehľadnosť oboch OSCam panelov. r63 má Enigma farbu
#1a102136 (~10% priehľadnosť). Root je transparentný, za panelmi nie je plný
nepriehľadný cyan obdĺžnik ani celoplošný obrázok; rámy sú štyri samostatné čiary.
Widgety obsahu transparentné, výber/main.SELECTION nepriehľadný. Hlavička, okraje
a spodné tlačidlá zostávajú plné. HeaderArtwork je natívny eWidget vysoký164 FHDpx,
ktorý oreže svoj plnoobrazovkový škálovaný ePixmap potomok; pôvodné PNG sa nemení.
Overené podľa OpenATV eWidgetDesktop.calcWidgetClipRegion (potomkovia sú orezaní
viditeľnou oblasťou rodiča). PNG loader sám ignoruje požadované rozmery, preto
sa škáluje pri kreslení, nie dekódovaním do menšieho header widgetu.
Konfigurácia obnovy sa číta malým vlastným parserom; nevzniká závislosť na samostatne
balenom configparser. Funkcie a databáza účtov sa nemenia.
312 testov Python3.14.7 aj z čistého checkoutu, dva identické buildy3665352 B,
SHA256 c074843fc4a8c2dbe0e12044782b5846dee826df5364e2d8ff2d618f1e1f0496.
Čaká sa už len na vizuálne potvrdenie priehľadnosti/banneru na prijímači.


## r64 – informácia v potvrdení povolenia klienta

r63 publikované zdrojom 7b72f324f46835d7d32bb8105d24370264242818,
CI40280241163 success, oba feedy overené. Priehľadnosť ešte čaká na snímku.
Používateľ žiada pri Ano/Nie vysvetliť čakanie na reštart/refresh, aby ho nemiatol
starý zoznam počas spracovania. Pri povolení je teraz krátky druhý odsek:
„Po povolení chvíľu počkajte, kým sa zmena prejaví a zoznam obnoví. Pri lokálnom
DVBAPI účte sa na pozadí reštartuje OSCam.“ Pri zákaze sa nepridáva. Desať jazykov,
138 spoločných katalógových kľúčov. Nie ostáva predvolené a nič nevykoná.
313 testov Python3.14.7 aj z čistého checkoutu; dva identické buildy3666062 B,
SHA256 b7843a7d1b0ce4c645890c06af55f680a5681610cc86d298e884f53c8f422aa3.
Aktuálne treba iba vizuálne overenie priehľadnosti/banneru a novej správy.

Publikované r64: zdroj 654a568489c0d1f82a01bf50f45914fc87344fec, CI40280660157 success. Oba feedy overené r64 / 3666062 B / SHA256 vyššie.

Nahradené r61–r63 odstránené workflow40280828196 success; API overilo iba r64 (spolu40 odstránení). Spotrebovaný request zmazaný, tagy/história zachované.


## r65 — ECM v hlavnom pravom paneli

Používateľ schválil r64: OSCam priehľadnosť, ovládanie a hlášky sú OK. Na jeho ďalší pokyn Informácie o ECM nahrádzajú LiveTV v pravom paneli hlavného menu. Ľavá ponuka zostáva dostupná. Prvé červené obnoví LiveTV, ďalšie zavrie menu. Otvorenie inej obrazovky zastaví ECM timer a obnoví pripravenosť LiveTV bez zastavenia/preladenia kanála. Pôvodný ECM parser a 5-sekundové obnovovanie ostávajú zachované; malé rozlíšenia pod 1280 používajú pôvodný dialóg. Správca CAM sa teraz nemení.

320 testov Python 3.14.7 prešlo aj v čistom checkoute, compileall a diff check OK. Dva nezávislé buildy sú zhodné: 3667220 B, SHA256 d1ac6d5b093c81c9ec2296da604fa10c5fbcc170c60baf49d80fd991a375d373. Natívny vzhľad ECM a návrat LiveTV musí ešte potvrdiť prijímač.

R65 publikované: zdroj94575bc1af68cf246a4a3f960a4e2b281eef76f1, CI40284135235 success vrátane stiahnutia a kontroly vydaného balíka. Oba aktualizačné feedy overené na r65 s vyššie uvedenou veľkosťou a hashom.

Nahradené r64 odstránené workflow40284220781; API overilo iba v13.40-r65 s IPK a SHA256. Spolu41 odstránených vydaní, Git tagy a história zachované.


## r66 — preklady ECM

Snímka1(20261026-071243).jpg potvrdzuje ECM v pravom paneli. Používateľ výslovne zachováva čiernu piconu a žiada iba preklad anglických popisov. Chyba: pred hľadaním prekladu sa odstraňovala dvojbodka, ale locale kľúče ju obsahujú. R66 ju zachováva; test kontroluje Operátor a Čas ECM aj nezmenené CHID a parserovú predlohu. 320 testov prešlo.

R66 publikované: zdroj985996f35088b5c09a66c80803435de0f5f72409, CI40284764313 success vrátane deterministického dvojitého buildu a kontroly vydaných bajtov. Oba feedy overené na r66: 3667024 B, SHA256 bd636876d7c23e893ce112ad90037be334d6f9c21c0db76aa3cb53572d1cda78.

Nahradené r65 odstránené workflow40284856704; API overilo iba v13.40-r66. Spolu42 odstránených vydaní, Git tagy a história zachované.


## r67 — oddelené ECM popisy

Používateľ snímkou1(20261026-072259).jpg potvrdil anglické popisy aj po ďalšom GUI reštarte. Reštart sa už vykonáva automaticky; neopakovať tento návrh. Receiver diagnostika potvrdzuje r66 zdroj aj správne slovenské JSON hodnoty. Presná príčina na prijímači zatiaľ nie je dokázaná. R67 odstraňuje patchovanie setText zdieľaného Labelu: interný parserový Label zostáva súkromný, nový zobrazovací Label dostáva preložené popisy po otvorení aj po každom obnovení. Test používa reálny SK katalóg a overuje CHID aj nezmenenú internú predlohu. 321 testov prešlo; natívny výsledok musí potvrdiť box.

R67 publikované: zdroj6c0a0bd0eb7c0188a6b208be7b0cbd22f29f2f34, CI40285869341 success vrátane zhodných buildov a kontroly vydaných bajtov. Oba feedy overené: 3667108 B, SHA256 5c32f52b0550e75cf74473d68b53215dd9968c46da4d78669ad3a58f03d28a90.

Nahradené r66 odstránené workflow40285973189; API overilo iba v13.40-r67. Spolu43 odstránených vydaní; Git tagy a história zachované.


## r68 — Správca CAM

Snímka1(20261026-072903).jpg z r67 preukazuje správne slovenské ECM popisy. Logo čiernej picony zostáva na výslovný pokyn. Ďalšia sekcia je správca CAM: používateľ schválil rovnaký princíp ako OSCam, pravý panel akcie, ľavý CAM a stav, horizontálne šípky prepínajú panely.

Nový warder_cam.py mení iba prezentáciu a navigačnú vrstvu: pôvodné pomenované komponenty, konfiguračné hodnoty, natívne príkazy, časovače, zelený štart/reštart a červený stop sú zachované. Hore/dole vpravo prechádza akcie vrátane spätného posunu a vynechania odstránených/nedostupných SRV položiek. OK vpravo aktivuje akciu; vľavo otvorí zoznam hodnôt vybraného konfiguračného riadku. Zrušenie nič nemení, potvrdenie iba nastaví výber, nespúšťa CAM. Modré prepne na pravý panel a ďalšiu akciu. EXIT pôvodne zavrie správcu a vráti hlavné menu/LiveTV. Tenké rámiky, rovnaké modré zvýraznenie a hlavička s časom/verziou. Malé rozlíšenia pod1280 zostávajú pôvodné.

327 testov Python3.14.7 prešlo, compileall a diff check OK. Nové kontroly zachovaných komponentov/bounds HD/FHD/UHD, navigácie, výberu a zachovaných farebných handlerov. Existujúce SRV testy používajú rozmery aktuálneho skinu namiesto starých čísel42/82. Nový natívny vzhľad a navigáciu musí ešte potvrdiť prijímač; už overené backend skúšky neopakovať.

R68 publikované: zdroj2e923bda7007c882f4feb02bacb3b0880c94c907, CI40287426629 success vrátane deterministického dvojitého buildu a kontroly vydaných bajtov. Oba feedy overené: 3668966 B, SHA256 844622f2e5941a7c1ecfa2da1f1374e35f27f588bcc777e2ba7dc8a3054ec83d.

Nahradené r67 odstránené workflow40287552293; API overilo iba v13.40-r68. Spolu44 odstránených vydaní; Git tagy a história zachované.


## r69 — priehľadnosť a obsah vľavo

Prezreté snímky1(20261026-074516).jpg a1/2(20261026-074916).jpg. Používateľ chce jemnú priehľadnosť celého správcu a všetky tieto ponuky v ľavom paneli: Stiahnuť CAM, Zmazať CAM, OSCam štart konfigurácia, Oneskorenie štartu, samotný výber CAM. Všetko zahrnuté do jednej r69; r69 sa ešte priebežne nevydávala.

Použitý rovnaký PANEL_GLASS #1a102136, CLEAR a orezaný HeaderArtwork ako v schválenom OSCame. Žiadny nepriehľadný obrázok/plný cyan obdĺžnik pod panelmi; len tenké rámiky a jedna alpha vrstva. Textové komponenty/config majú priehľadný podklad, vybraná položka zostáva nepriehľadne modrá.

warder_cam_panes.py vlastní vopred vytvorené natívne list/config/title widgety hlavného správcu. Session proxy zachytí iba výslovne požadované obrazovky a výbery, pôvodné Python controllery sa používajú bez samostatného Session okna. Zachované pôvodné feedy, ochrana bežiaceho CAM pred zmazaním, store štart konfigurácie. Odinštalačný zoznam sa načítava v pracovnom vlákne; zatvorené panely odmietajú oneskorené výsledky. Červené/EXIT obnoví základný panel alebo zruší vnorený výber. Zelené v konfigurácii ukladá, vo výbere potvrdzuje. Samotná zmena CAM hodnoty CAM nespúšťa. Oneskorenie je výber1–30s s pôvodným uložením. Vnorené výbery v konfigurácii zachovávajú rozpracované hodnoty. Viditeľnosť základných status komponentov je počas obsahu blokovaná, aby backend refresh nevykreslil stav cez zoznam.

Potvrdzovacie MessageBox, Console priebeh opkg a editory hodnôt/priečinkov zostávajú modal; netvrdiť, že už je vložený úplne každý historický dialóg. Malé rozlíšenia pod1280 zachovávajú pôvodné správanie.

335 testov Python3.14.7 prešlo. Kontroly glass vrstiev, zachovaných komponentov, odložených výsledkov, vložených ponúk, save/cancel, delay a výberov; samostatné testy používajú reálny startup controller so simulovaným store, bez zápisu do prijímača. Natívny výsledok čaká na potvrdenie boxu.

R69 publikované: zdroj8aaf649d90b1ebd235fb476a07b631af6071b8ec, CI40288939178 success vrátane čistého checkoutu, zhodných buildov a kontroly vydaných bajtov. Oba feedy overené: 3671812 B, SHA256 79a2f5fea275ba61970d10fc963c1150d5ababae55f3b2189ec3e83108a73771.

Nahradené r68 odstránené workflow40289114626; API overilo iba v13.40-r69. Spolu45 odstránených vydaní, Git tagy a história zachované.


## r70 — odstránenie modrého tlačidla správcu

Prezretých všetkých7 snímok:1–5(20261026-080152/080153).jpg,6(7).jpg,7(1).jpg. Preukazujú priehľadnosť, CAM výber, feed zoznam, odinštalačný zoznam, štart konfiguráciu a oneskorenie v ľavom paneli. Nie sú dôkazom vykonania inštalácie/odinštalácie ani uloženia hodnôt. Používateľ žiada zrušiť modré Presunúť výber, pretože navigáciu už riešia šípky. R70 odstraňuje footer aj funkciu (modré sa spotrebuje bez posunu, aby neprepadlo pôvodnému handleru). Zostávajúce červené/zelené/žlté sú rovnomerne centrované v troch stĺpcoch. Všetky vložené obrazovky používajú spoločný footer.

336 testov prešlo. Prvý beh mal izolovaný5s timeout reálneho shell smoke testu native_start_config; opakovaný kompletný beh bez zmien kódu prešiel za7.7s. Žiadne procesy zo skúšky nezostali. Nová regresia overuje neprítomnosť modrého widgetu, nečinnosť jeho klávesu a rovnaké rozmery troch footerov.


## r70 publikácia a r71 pravý panel

R70 publikované: zdroj1ad2b9dda2820e12d78d77f4069cc5faa696505a, CI40289803826 success, oba feedy overené na r70. Nahradené Releases69/70 sa upracú po overenom vydaní71.

Používateľ upresnil, že Informácie ECM, Správa swapu a Nástroje majú používať MENŠÍ PRAVÝ panel namiesto LiveTV, ľavá hlavná ponuka zostáva. Ide o krátke obsahy, prípadné korekcie až podľa výsledku na boxe. Netýka sa to prehodenia panelov správcu CAM.

warder_right.py transformuje iba runtime skin hlavného menu: priehľadný root, orezaný spoločný banner, tenké rámiky/jedna10% alpha vrstva a prepínateľné nepriehľadné podklady pre pôvodné menu. Nepriehľadný normálny vzhľad a LiveTV sa obnovia po odchode; počas ECM/swap/tools sú podklady aj dekorácie videa schované. Pig a nepriehľadné vrstvy majú explicitné oddelené zPosition, preview nie je prekryté. Ostatné systémové/kanálové/OSCam skiny sa nemenia.

Pôvodné swap/tools/diagnostic/create controllery sú headless, používajú vopred vytvorené widgety pravého panela a Session proxy pre vnorené Create/Diagnostic. Originálne operácie swap_store a diagnostický worker sa nemenia; busy blokuje návrat z operácie, onClose zatvára async výsledky. Vytvorenie swapu obsahuje pôvodné3 polia vpravo; konfiguračné výbery/editor a potvrdzovacie MessageBox sú ešte modal. Nástroje majú zoznam a popis vpravo, výsledok archívu ScrollLabel vpravo. Hore/dole posúva aktívny panel, doľava/doprava mení focus, červené obnoví predchádzajúci obsah/LiveTV. Zelené/žlté používajú originálne akcie modelu. Bez stop/playService. ECM ponecháva schválený parser/picon/legendu a iba prepína rovnaké glass podklady.

343 testov Python3.14.7 prešlo, compileall/diff check OK. Nové testy používajú originálne controllery: Tools/Diagnostic návrat, Swap/Create busy, neotvorenie Session dialógu pre vložené stránky, ECM glass, obnova PIG bez preladenia a bounds HD/FHD/UHD. Skutočný natívny vzhľad r71 ešte čaká na prijímač; celý plugin zostáva receiver_tested=false.

R71 publikované: zdroj0f2ca65296c479f04b2342fa7266c75ba4dd7774, CI40291132117 success vrátane čistého checkoutu a zhodných buildov/kontroly vydaných bajtov. Oba feedy overené na r71: 3674528 B, SHA256 86d13a1986a562d09bb1782e87b0fe6beca50633281790e4ae3c373cd24b3671.

Nahradené r69/r70 odstránené workflow40291271244; API overilo iba v13.40-r71. Spolu47 odstránených vydaní, Git tagy a história zachované.


## r72 — Informácie ECM na obrazovke

Prezreté0(10).jpg,1/2(20261026-082320).jpg. Swap/tools sú v pravom paneli, ale používateľ upozornil na pôvodné samostatné nastavenia Informácie ECM NA OBRAZOVKE (ID8), nie na read-only ECM(ID6). Toto rozlíšenie sa predtým prehliadlo. R72 vkladá aj OSD_ECM_Menu do existujúceho pravého config widgetu.

Použité pôvodné save/saveOnly/exitCancel/chckSetup/setPosition. OK mení bool alebo otvorí editor/voľbu hodnoty; pole Set position zachová pôvodný pozičný editor. Green uloží, red zruší; typové zmeny ponechávajú pôvodné potvrdenie GUI reštartu. Normálny návrat aj nútené zatvorenie zastavia chckTimer a rušia neuložené hodnoty; uložené hodnoty sa následne nerušia.

Session proxy teraz rozlišuje dočasné modal editory/potvrdenia od skutočného odchodu z hlavného menu: nevyhadzuje pravý controller pri onHide editora. Callback/onShown obnoví skrytý PIG počas aktívneho panelu. Tým sa opravuje aj prípad straty swap konfigurácie po výbere hodnoty v r71.

346 testov prešlo vrátane reálneho OSD controllera so simulovaným config/save/cancel, rozbalenia polí po zapnutí, zastavenia timeru a zachovania modelu pri modal editore. Skutočný natívny výsledok čaká na prijímač. Pôvodné systémové nastavenie alebo poloha OSD sa nemenia bez potvrdenia používateľom.

R72 publikované: zdroj0fe1e856ed4aee01106fcb590a056708bb05999b, CI40292458200 success vrátane čistého checkoutu/deterministických buildov/kontroly vydaných bajtov. Oba feedy overené: 3674988 B, SHA256 fe47612b03b0f6176d24b3b971c85529cac68bd44199aa50b52722dec30842dd.

Nahradené r71 odstránené workflow40292575618; API overilo iba v13.40-r72. Spolu48 odstránených vydaní; Git tagy a história zachované.


## r73 — aj výber Typ v pravom paneli

Prezreté0(20261026-083359).jpg a1(20261026-083400).jpg: nastavenia OSD ECM sú správne vpravo, ale ich Typ otvára starý modal ChoiceBox. Používateľ žiada upraviť aj výber. R73 mení zoznamové hodnoty pravého config panela na vlastný pravý list v rovnakej obrazovke, vrátane Statické/Rolované info a swapových výberov. Udržuje aktuálnu hodnotu označenú, OK/green potvrdzuje iba rozpracovanú hodnotu, red ruší bez zmeny. Vráti pôvodný model a footer Save; trvalé uloženie je stále samostatné. OSD hint timer sa počas výberu zastaví a po návrate obnoví. Pri prepnutí sekcie sa stav voľby zahodí.

347 testov prešlo vrátane potvrdenia/zrušenia typu a dôkazu, že sa neotvára Session okno. Prvý nový test omylom použil v stuboch neimplementované setCurrentIndex; opravený na existujúce moveToIndex bez zmeny natívneho ovládania. Natívne zobrazenie výberu čaká na box.


## r74 — horné nastavenia zostávajú, editor dole

Používateľ výslovne upresnil: po OK na Typ/Prah/Čas obnovy/Čas zobrazenia či Rýchlosť nesmie zmiznúť horné menu. Pravý panel sa vizuálne rozdelí, nastavenia zostanú hore, editor sa otvorí DOLE. Výnimka Nastaviť polohu ponecháva pôvodný pozičný editor. R73 bola už publikovaná (zdroj7156edd777c38d14a5002c9184f3e87f6b458b77, CI40293852343 success), no používateľské snímky0/1(20261026-111150).jpg ukazujú práve jej nahradenie celého pravého obsahu; r74 to mení. Obe snímky prezreté.

Nové right_editor_* widgety: oddeľovacia čiara y560, titulok y580, list y635–875 alebo číselná hodnota y650–730, pomoc dole y890–955 (FHD). Horný right_config sa neschováva. Výber začne na aktuálnej hodnote, čísla sa zadávajú0–9 (prvá číslica nahradí pôvodné číslo) alebo menia šípkami, pomoc ukazuje povolený rozsah. Rozpracovaný buffer nemení config do OK/green; red ho zahodí. Kontrola rozsahov1–2000,2–12,4–15,50–450. Konfiguračné uloženie zostáva ďalší samostatný krok. OSD hint timer je počas editoru pozastavený.

349 testov Python3.14.7 prešlo, compileall/diff check OK. Nové testy zachovanej hornej časti a dolného listu, dočasného číselného bufferu, odmietnutia hodnoty mimo rozsahu, potvrdenia a zrušenia a bounds HD/FHD/UHD. Native receiver výsledok čaká na potvrdenie. Dočasný checkout bol po obnove pracovného prostredia znova získaný z originálnej vydávacej vetvy; žiadne neuložené zmeny sa nestratili.
