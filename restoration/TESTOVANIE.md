# Aktuálny checkpoint —25.10.2026, r49 pripravené

Pracovať výhradne v original-python314, runtime restoration/src/GlassSysUtil. Produkčná warder-master-production sa nemení, bez force/rebase. GSU Warder Evolution je spoločný neprekladaný názov. Hlavná obrazovka má spoločný banner, živé hodiny,11 položiek, liveTV vpravo a popis pod ním,4 farebné akcie vrátane modrého O plugine. Nadpis Hlavná ponuka a spodný purpose riadok sú odstránené; panely využívajú miesto. LiveTV a návrat do normálu potvrdené používateľom.

Informácie o systéme: r45 zle prekrývalo pôvodné texty; r46 má pozadie/rám/panel vo vrstvách-3/-2/-1 a transparentné texty. Snímka1(20261025-164108).jpg potvrdzuje ľavé popisky aj pravé procesy/Dmesg a používateľ potvrdil všetky4 šípky. Funkčnú opravu neotvárať znova bez dôvodu.

Používateľ odmietol schematické hardvérové ikony r47, ale výslovne schválil ponechanie šípok. r48 mení11 hardvérových ikon na farebné plastické RAM/disky/USB/karty/CPU/teplomery/Linux, podobné pôvodným, so skutočne priehľadným okolím bez čiernych dlaždíc a odrazov. V r48 boli šípky a stavové bodky bajtovo nezmenené. Následne používateľ žiada zmeniť aj šípky, takže r49 má nové plastické strieborno-tyrkysové šípky; stavové bodky zostávajú nezmenené. Väčšie512px výrobné podklady a prompty sú v artwork/system-raster; do IPK idú iba pripravené120px PNG. Pôvodné odmietnuté hardvérové SVG sú odstránené, generátor ponecháva iba schválené šípky/bodky.

260 testov Python3.14.7 úspešných; dva zhodné buildy, CI40215452598 úspešné vrátane publikácie a overenia vzdialených bajtov. Zdroj2f3e0b6022f74ca42b46097d894e75b5307d37cb. Feed overený: r48,3633030B,SHA2564a0fa9047f56f643f8cba9ec8cff2d9f2274d9547132195f5a56c67986ee7383.

Najbližšie: aktualizovať cez GSU na r49 a posúdiť nové ikonky priamo v Informáciách o systéme. Nový vzhľad zatiaľ nie je schválený na prijímači. Anglické popisky zostávajú ďalšia kozmetika, neboli týmto vydaním preložené. Opakované skúšky CAM, swapu, diagnostického archívu a už potvrdených šípok nežiadať. CCcam/Mbox a samostatný SRV bez príslušnej služby stále nie sú hardvérovo overené; celý plugin neoznačovať za úplne overený.

Staršie odseky nižšie sú história; aktuálne kroky vyššie majú prednosť.

## OSCam klienti — uzavretie skúšky r35

Zrušenie otázky voľbou Nie, odchod/opätovné otvorenie, následné zakázanie a povolenie účtu Gigablue boli vyskúšané. Zákaz označil účet disabled/offline; živé lokálne DVBAPI spojenie pokračovalo ako anonymous. Povolenie odstránilo disabled, ale meno spojenia sa zmenilo späť na Gigablue až po ručnom reštarte OSCamu. Používateľ potvrdil obraz po prepnutí aj pred týmto reštartom a po reštarte dodal stav Gigablue OK. Podľa výslovného rozhodnutia Zakázať/Povoliť zachovať bez úpravy; nerobiť automatický CAM reštart ani nepremenovávať anonymous.

Referenčný upstream OpenVisionE2/oscam module-webif.c: disable nastaví disabled=1 a kill_account_thread pri nenetworkovom module prepne cl->account na first_client->account; enable iba nastaví disabled=0. oscam-client.c pomenúva účet bez usr ako anonymous. To vysvetľuje pozorovaný jav, ale nejde o kontrolu presného zdroja nainštalovanej binárky.

Dodaná gsu-cam-diagnostika.txt zachytáva monotónne časy 25121–25207: počas troch fáz rovnaký softcam symlink, hash init skriptu a živé PIDy 20965/20966. par50=False, pomocný guard enabled=true, autostart log nedostupný. Nesúlad môže byť starý súbor a nedokazuje bežiaci časovač. Diagnostika nezachytila pôvodnú stratu výberu CAM, jej príčina zostáva nepreukázaná. Predošlý log končil pri uptime17303, zatiaľ čo aktuálny uptime bol24725; preto ho nemožno pripísať poslednému zákazu/povoleniu klienta.

r36 opravuje konkrétne reprodukovateľnú medzeru: pri GUI štarte bez native výberu sa pôvodne nevytvoril controller. Teraz existuje aj pre neskorší výber, rešpektuje živý prepínač a ručný GSU stop; bez živého controlleru sa zneplatní starý guard. 215 hostiteľských testov prešlo. Nový IPK: 2 185 256 B, SHA256 `304b774a32ac9b6620ce02ebfff5fd5943d97dcd431629d02e06d7ec2fd4bd0a`. Zdrojový commit `31afb4fa1b2d07d72aee87b446946c65d9eb89b0`, CI40196871017 úspešné vrátane publikácie a overenia stiahnutých verejných bajtov. Release `v13.40-r36` je verejný prerelease a izolovaný feed už ukazuje na r36. Parser aktuálneho feedu ponúkne r36 pre r35, pri r36 neponúka nič. Library IPK `libfile_12ee11432f548191917ef456efa8ee58`. Prijímač vyžaduje jednorazovú ručnú inštaláciu r36 a GUI reštart; následné novšie vydania už ponúkne vstavaný updater.

---

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

### Prijímač potvrdil r12 — CAM stop/start/reštart

Snímka 1(20261025-004052).jpg potvrdila aktívny oscam-uni a CAID bez duplicít. Snímky 1/2(20261025-004217).jpg potvrdili úspešný skript reštartu; používateľ výslovne potvrdil, že po chvíli sa vrátil obraz aj ECM údaje (dočasné chýbanie bolo počas reštartu). Snímky 1/2(20261025-004553).jpg potvrdili samostatné zastavenie (Aktívny CAM: Žiadne) a následný štart (Aktívny CAM: oscam-uni, logo Irdeto a ECM údaje obnovené).

**Drobná zostávajúca chyba textu:** po úspešnom zastavení zostáva druhý stavový riadok „CAM/SRV spustené“, hoci aktívny CAM je správne Žiadne. Native callback musí aktualizovať aj statCamSrvbin podľa aktuálneho procesu. Zaradiť do ďalšej dávky; stop/start/reštart už netreba zbytočne opakovať. Ďalej hlavná ponuka OSD ECM.

### Pravá ponuka CAM/SRV — zostať pri nej

Používateľ upozornil, že sa nesmie preskočiť pravá ponuka. Modré posúva červenú šípku po pravej strane nadol, žlté aktivuje označenú položku. Ukončiť + žlté bolo potvrdené návratom do hlavného menu. Stiahnuť CAM/SRV používateľ už aktivoval: pripájanie zamrzne so spinnerom. Analýza zdroja potvrdila moreCamSrv -> chckFtp -> FTP_ALL, host picons.techneteuweb.eu cez FTP port 21. chckFtp aj ftp_center.updatemenulist používajú ftplib.FTP bez explicitného timeoutu v GUI vlákne; po prihlásení ide ftp_center do adresára architektúry (na tomto prijímači arm) a spúšťa FTP LIST. Spinner sám osebe nepotvrdzuje nekonečný cyklus; môže ísť o blokujúce DNS/connect/login/LIST. Dostupnosť servera zo siete prijímača nie je zatiaľ overená. Nezapisovať FTP prihlasovacie údaje do poznámok. Najbližšia oprava: pripojenie a načítanie zoznamu mimo GUI, konečný čas čakania, zrozumiteľná chyba a návrat do ponuky pri nedostupnosti. Potom pokračovať Zmazať CAM/SRV a ďalšími pravými položkami, až následne OSD ECM.

### r13 a preverenie pôvodnej domény — 25. 10. 2026

Používateľ doložil presmerovanie webu na ww17.techneteuweb.eu a oznámil varovanie na adware. Priamy DNS-over-HTTPS dotaz vrátil NS ns11.abovedomains.com a ns12.abovedomains.com; picons A 103.224.182.242; ww17 CNAME 11490.searchmagnified.com, A 199.191.50.190. To podporuje parkovanie domény, nie dôkaz zmeny vlastníka či konkrétneho malvéru. Oficiálny manuál Above.com potvrdzuje jeho abovedomains DNS a služby parkovania: https://www.above.com/manual/pm-add-domains.html a https://www.above.com/domain-parking-services.html . WHOIS sa nepodarilo získať, identita držiteľa neoverená. Priama FTP skúška TCP/21 na zistenej IP vrátila v tomto prostredí Network is unreachable; žiadny banner ani zoznam nebol získaný. Webové HEAD pokusy vypršali. Nepoužili sa staré FTP heslá ani sa nič nesťahovalo. Neprezentovať tento výsledok ako dôkaz zatvoreného portu alebo chýbajúcich súborov na serveri.

r13 odstraňuje pôvodný FTP endpoint a pribalené prihlasovacie údaje z runtime, spoločná brána chckFtp bez siete oznámi vypnutý nedôveryhodný zdroj. Tým sa zastaví zamŕzajúci pokus; dôveryhodná náhrada zatiaľ neexistuje. Opravený aj starý druhý stavový riadok po zastavení CAM. 39 testov úspešných. Pokračovať pravou ponukou: najprv overiť oznam Stiahnuť CAM/SRV v r13, potom otvoriť Zmazať CAM/SRV a preveriť len zoznam; nie je potrebné odinštalovať fungujúci OSCam. Ďalšie položky zatiaľ nepreskakovať.

### Finálna náplň r13 — zmena požiadavky na náhradu CAM feedom

Používateľ potvrdil, že FTP nejde ani jemu, a požiadal nahradiť archaické balíky feedom SoftCAM pre OpenATV (presnú adresu nepozná). R13 preto NEKONČÍ pri vypnutej ponuke: Stiahnuť CAM/SRV otvorí pôvodný zoznam, ktorý cez systémový opkg načíta aktuálne nakonfigurované zdroje. GSU nepridáva feed ani nespúšťa vzdialený inštalačný skript. opkg update (limit 45 s) a opkg list (15 s) bežia cez deferToThread mimo GUI. Názvy a verzie CAM sa filtrujú a zobrazujú v pôvodnom okne, pri neúspešnom update sa označí cache, prázdny/neplatný riadok nič neinštaluje. Výber vyžiada potvrdenie, potom otvorí pôvodnú konzolu s opkg install presného názvu bez force prepínačov. Pred inštaláciou OSCam balíka musí používateľ podľa pôvodného pravidla zastaviť bežiaci OSCam. Po zatvorení sa neskorý výsledok nezapisuje do okna. 47 host testov úspešných. Staré aktualizácie GSU/OSCam cez FTP zostávajú vypnuté a nesmú sa vydávať za hotové moderné aktualizátory.

**Presný ďalší krok:** inštalovať r13, reštart GUI, pravá ponuka Stiahnuť CAM/SRV (modré presúva šípku, žlté aktivuje). Najprv overiť ponúknutý zoznam/verzie a ovládanie počas načítania. Ak nič nenájde, overiť existujúcu konfiguráciu feedu v /etc/opkg a lokálny zoznam opkg; nevymýšľať adresu ani nepovažovať externé CAM feedy za balíky dodávané OpenATV. Samotná inštalácia nového CAM balíka ešte neoverená. Potom pokračovať Zmazať CAM/SRV a ostatnými pravými položkami; nepreskakovať na OSD ECM.

### r14 — čistý OpenATV a rôzne prijímače

Používateľ dodal enigma2-plugin-softcam-feed-universal_4.8-r0_all.ipk (2112 B, SHA256 35aa75731d36192402093631bfd6cd2b4b2ef0f5494f1f8eac4d538bc4d63e81). Archív bol iba prečítaný, jeho skripty sa nespúšťali. Inštalátor odvodzuje http://updates.mynonpublic.com/oea/$OEVER/$ARCH a zapisuje /etc/opkg/$ARCH-3rdparty-secret-feed.conf; okrem toho však maže konfigurácie a niektoré CAM súbory. Túto čistiacu časť nekopírovať. Používateľ výslovne chce funkciu aj na čistom OpenATV bez samostatnej inštalácie feed IPK a aj na iných strojoch.

Potvrdené prijímačom: architecture=cortexa15hf-neon-vfpv4, distro=openatv, oe=OE-Alliance 6.0. Upstream SusanOV/softcamfeed obsahuje oea/6.0/cortexa15hf-neon-vfpv4/Packages.gz aj reálne CAM balíky. Aktuálny OpenATV SystemInfo.py číta enigma.info zo SCOPE_LIBDIR (Tools/Directories.py -> ${libdir}/); používateľ potvrdil /usr/lib/enigma.info.

R14 pri prvom načítaní feedu v pracovnom vlákne zachová existujúci SoftCAM feed, alebo podľa metadát aktuálneho prijímača vytvorí jediný chýbajúci konfiguračný súbor. Nepoužíva konkrétny model ani architektúru GigaBlue ako default. Neodhadzuje architektúru podľa uname. Neznáme/neplatné údaje odmietne. Zápis atomický bez prepisovania, bez mazania CAM súborov či cudzích feedov. Predvolený ARM sa nesmie zaviesť. Testované adresy pre aarch64, mips32el, sh4, cortexa7hf a cortexa15hf-neon-vfpv4. 54 host testov úspešných.

**Ďalej:** používateľ má zatiaľ nainštalované r12. R13 balík bol technicky uložený, ale pred jeho odovzdaním používateľ doplnil požiadavku na čistý image; odovzdať už r14. Po inštalácii + GUI reštarte otvoriť pravú položku Stiahnuť CAM/SRV a overiť zoznam a svižné ovládanie. Na aktuálnom stroji feed už môže existovať, takže to nepreukáže prvotné vytvorenie na čistom image. Skutočná inštalácia CAM balíka sa ešte netestovala. Potom pokračovať ďalšou pravou položkou Zmazať CAM/SRV; nepreskakovať zvyšok ponuky.

### R14 — zoznam CAM balíkov na prijímači potvrdený

Snímky 1/2(20261025-012312).jpg ukazujú prechod z Loading package list... na naplnený katalóg (CCcam, doscam, gbox, mgcamd, ncam, OSCam), s verziami a posuvníkom. To potvrdzuje načítanie zoznamu, nie samotnú inštaláciu ani vytvorenie feedu na čistom image. Svižné ovládanie počas načítania ešte používateľ výslovne nepotvrdil. Drobnosti do ďalšej dávky: preložiť Loading package list... a upraviť výšku zoznamu/riadkov tak, aby spodný čiastočne zobrazený riadok nebol odrezaný. Ďalej overiť šípky a otvorenie potvrdenia zeleným bez nutnosti meniť fungujúci CAM. Potom Zmazať CAM/SRV a zvyšok pravej ponuky.

### R14 — potvrdenia, ručný CAM a reálna inštalácia

Používateľ potvrdil šípky hore/dole. Snímky 1/2/3(20261025-012740).jpg potvrdili výber CCcam, otázku po zelenom a návrat po Nie so zachovaným výberom. Snímka 3(20261025-012610).jpg potvrdila pôvodnú požiadavku zastaviť OSCam pred inštaláciou iného OSCam balíka.

Zmazať CAM/SRV zobrazilo prázdny zoznam. Kód stále filtruje iba glasssysutil-*; je potrebné doplniť moderné CAM balíky. Tento konkrétny oscam-uni však nie je balík: opkg list-installed našiel len enigma2-plugin-extensions-oscamstatus 7.50 a softcam-feed-universal 4.8-r0, oba opkg search na /usr/bin/oscam-uni vrátili no path found. Používateľ výslovne potvrdil, že ho vložil ručne. Súbor 1186772 B, skript softcam.oscam-uni a vlastnú konfiguráciu zachovať; netváriť sa, že sa dá odstrániť cez opkg.

**Reálna inštalácia potvrdená:** snímky 1/2/3(20261025-013830).jpg ukazujú potvrdenie Áno, konzolu s /usr/bin/opkg install enigma2-plugin-softcams-oscam-master a úspešné Installing/Configuring balíka, závislosti pcsc-lite 2.5.1, ccid 1.8.4, pcsc-lite-lib 2.5.1 a pcsc-tools 1.7.5, koniec Príkaz dokončený bez viditeľnej chyby. OSCam-master 11968-git10887+39e78a40+39e78a4688-r3 sa stiahol z existujúceho http://updates.mynonpublic.com/oea/5.6/cortexa15hf-neon-vfpv4/ . Systém pritom hlási OE-Alliance 6.0. R14 zachovalo už nastavený feed, preto netvrdiť, že tento test potvrdzuje správne založenie 6.0 feedu na čistom image. Existujúci 5.6 zdroj treba preveriť a vyriešiť kompatibilitu pred vyhlásením úplnej podpory.

Ďalej zavrieť konzolu aj sťahovací zoznam a pozrieť správcu CAM/SRV. Súčasný NativeSoftcam podporuje len systémom zvolený script; zobrazenie a prepínanie všetkých novo nainštalovaných CAMov je ešte potrebné doplniť. Aktualizácia OSCam a OScam štart konfigurácia sú stále pôvodné SRV/UCM vetvy; moderné balíky samy tieto sivé položky nesprístupnia. Stále preverovať celú pravú ponuku, nepreskakovať na OSD ECM.

### r15 — dokončené v zdroji, nasleduje overenie na prijímači

Snímka 1(20261025-014041).jpg po úspešnej inštalácii ukázala CAM-y (1), zvolenú hodnotu Žiadne a zastavený CAM. R14 podporovalo iba aktuálny systémový odkaz. R15 načíta všetky platné dvojice softcam.* + binárny súbor a ponechá v riadku systémom zvolený CAM aj po zastavení. Očakávané sú teraz aspoň oscam-master a ručný oscam-uni.

Zelené na inom natívnom CAM spustí izolovaný worker: stop starého, atomický prechod odkazu, štart nového. Pri chybe obnoví odkaz a pokúsi sa obnoviť predtým bežiaci CAM; ak starý nejde zastaviť, druhý sa nespúšťa. Binaries/konfigurácie sa nekopírujú. Registrácia balíka sa zisťuje z opkg .list vlastníctva; ručný oscam-uni sa nevydáva za IPK. Zmazať CAM/SRV už filtruje aj moderné CAM balíky a chráni bežiaci balík. Aktualizácia OSCam sa pri balíkom spravovanom OSCame sprístupní a používa update && install z aktuálnych systémových feedov s potvrdením a kontrolou zastaveného OSCamu. OScam štart konfigurácia pre natívne CAMy zostáva sivá — starý UCM editor sa na ne nesmie použiť.

65 host testov úspešných, overená aj reprodukovateľnosť AST transformácií. Pôvodné grafiky/skin súbory sa nemenia. Drobnosti anglického textu načítania a odrezaného spodného riadku zostávajú zapísané do ďalšej dávky. Nesúlad existujúceho feedu 5.6 vs OE 6.0 zostáva neuzavretý, nerobiť tichý prepis používateľského zdroja.

**Ďalej:** nainštalovať r15 + GUI reštart, zobraziť správcu a šípkami v prvom riadku overiť oba natívne CAMy. Potom skúsiť zvoliť oscam-master a zelené. Bez platnej konfigurácie nemusí dekódovať, stav procesu je samostatná vec; používateľ chce overiť postup/funkcie celého pluginu, nie konkrétny CAM. Po potvrdení výberu/štartu ďalej stop/reštart, aktualizácia balíka a zobrazenie/zrušenie odinštalovania. Pravú ponuku nepreskakovať.

### Po r15 — prijímač odhalil dve nezávislé chyby

Snímky 1(20261025-015452).jpg a 2(20261025-015454).jpg potvrdili CAM-y (2), výber master/uni, obidva zastavené; Aktualizácia OSCam stále sivá. Štart master skončil Chyba, snímka 1(20261025-015637).jpg. Terminálová diagnostika NativeSoftcam potvrdila selected=oscam-uni, available=[oscam-master,oscam-uni], package_for(master)=None. Spúšťací skript vypísal `/usr/bin/oscam-master: error while loading shared libraries: libssl.so.3: cannot open shared object file` a FAILED. Neoznačovať to za úspešný štart ani bez dôkazu za chybu samotnej zmeny odkazu. Nezamieňať SONAME knižnice vytvorením falošného symlinku.

Samostatná chyba GSU: evidencia balíka iba cez predpokladané opkg .list súbory nie je na tomto image spoľahlivá. Rozpracovaná oprava číta opkg list-installed raz na pozadí pri obnove ponuky, cache pre ovládanie a aktualizácie vypĺňa v GUI callbacku. Zároveň ochrana odinštalovania porovná presný natívny názov s kandidátnymi názvami balíka aj bez .list metadát, aby aktívny master nebolo možné omylom odstrániť. Ešte nevydané; testy a balík až po dokončení.

Externé balíky master z upstream 5.6/r3 aj 6.0/r4 majú Depends iba libdvbcsa, libusb1, pcsc-lite, pcsc-tools. Statické čítanie ELF neposkytlo riadky DT_NEEDED; netvrdiť preto, že r4 určite vyrieši chýbajúce SSL3. Pred opravou feedu/knižníc potrebujeme konkrétnu verziu OpenSSL, dostupné SSL balíky a presný feed súbor v prijímači. Existujúci feed 5.6 pri OE6.0 zostáva podozrením na nekompatibilitu, nie samostatným potvrdeným vysvetlením knižničnej chyby.

### r16 — príčina ABI potvrdená a opravy pripravené

Prijímač: openssl version -> OpenSSL 4.0.3 (29 Sep 2026), katalóg ponúka libssl4/libcrypto4, nie libssl3. Aktívny zdroj presne /etc/opkg/cortexa15hf-neon-vfpv4-3rdparty-secret-feed.conf -> http://updates.mynonpublic.com/oea/5.6/cortexa15hf-neon-vfpv4 . Toto je stará vetva pri OE-Alliance 6.0.

Externé ARM binárky sú UPX komprimované; pôvodné readelf pred rozbalením nedalo závislosti. Po rozbalení oficiálnym UPX v5.2.1 (hostiteľský nástroj, ARM kód sa nespúšťal) je potvrdené: master 5.6/r3 -> libssl.so.3 + libcrypto.so.3; master 6.0/r4 -> libssl.so.4 + libcrypto.so.4. Detaily a SHA sú v oscam-abi-evidence.json. Príčinou konkrétneho štartového zlyhania je teda starý balík pre inú vetvu, nie potreba podvrhnúť názov knižnice.

R16 pri známom providerovi porovná aj EXISTUJÚCI zdroj s metadátami prijímača. Pred zmenou overí Packages.gz a architektúru, uloží pôvodnú konfiguráciu do .warder-backup, atomicky nahradí iba URL a vytvorí .warder-refresh-pending. Až úspešný opkg update zruší pending a dovolí ponúkať zoznam. Pri zlyhaní a pri opätovnom otvorení sa nesmie použiť cache pre starý systém. Cudzie vlastné providery sa nemenia. Aktualizácia cez pravú položku tiež pred opkg update/install pripraví kompatibilný zdroj na pozadí.

Oprava balíkovej evidencie: opkg list-installed beží raz pri obnove správcu v pracovnom vlákne (timeout 8 s), výsledok sa prenesie do cache v GUI. Tlačidlá už nemusia hádať cestu k opkg .list databáze. Guard odinštalovania bežiaceho CAM funguje aj bez týchto súborov. 73 testov úspešných.

**Ďalší krok:** používateľ má r15. Nainštalovať r16 a reštart GUI. Otvoriť Stiahnuť CAM/SRV; tým sa starý zdroj opraví a obnoví katalóg pre OE6.0. Vybrať už inštalovaný oscam-master a potvrdiť Áno — má sa cez opkg nahradiť r3 za r4 (alebo novší balík danej správnej vetvy). Zatiaľ neštartovať stále pôvodný r3 bez jeho aktualizácie. Po úspešnej aktualizácii skúsiť zelené na master a overiť aktívny proces. Sledovať aj sprístupnenie pravej Aktualizácie OSCam. Ručný oscam-uni a jeho konfigurácia zachované. OScam štart konfigurácia pre natívne CAMy je stále nedokončená; pokračovať celou pravou ponukou.


## 2026-10-25 — r16 prijímač a oprava r17

- Prijímač potvrdil prechod feedu OE5.6 → OE6.0, aktualizáciu OSCam r3 → r4 a úspešné spustenie oscam-master.
- Zastavenie cez init skript hlási FAILED; PID súbor /var/tmp/oscam-master.pid chýba. /proc ukázal živý rodičovský proces 22042 (S, PPid1, /usr/bin/oscam-master) a zombie potomka 22044 (Z, PPid22042).
- Po odporúčanom cielenom ukončení rodiča správca ukazuje Žiadny spustený CAM/SRV, ale aktualizácia stále hlási potrebu zastaviť OSCam. Kontrola oscamRunning doteraz čítala len comm, preto blokovala aj zombie záznamy.
- r17 kontroluje aj State: Z/X/x neblokujú; živý proces vedľa zombie stále blokuje. Ošetrený zánik procesu počas čítania. Zmena je aj v port_source.py. 76 host testov úspešných na Python3.14.7.
- Nasleduje nainštalovať r17 + reštart GUI a overiť Aktualizácia OSCam pri zastavenom CAM. Samostatne zostáva vyriešiť spoľahlivé zastavenie oscam-master s chýbajúcim PID súborom. Neoznačovať celé CAM/SRV menu za hotové.


## 2026-10-25 — r17 potvrdený, r18 pripravený

- r17 na prijímači: potvrdenie Aktualizácia OSCam sa otvorilo. Po Áno sa načítali feedy vrátane OE6.0; konzola ukázala No packages installed or removed a Príkaz dokončený bez viditeľnej chyby. Následné zelené tlačidlo úspešne spustilo oscam-master (Aktívny CAM + CAM/SRV spustené). Nešlo o inštaláciu novej verzie, ale overenie aktualizačného postupu pri nezmenených balíkoch.
- Používateľ prikázal pokračovať a odišiel si oddýchnuť. Pripraviť r18 bez ďalšieho vyžadovania skúšok počas jeho neprítomnosti.
- r18: pôvodný stop skript + overenie reálnych procesov, potom cielený SIGTERM a až pri neúspechu SIGKILL. Bez závislosti od PID súboru. Exe a starttime overené pred signálom, pidfd na podporovanom kerneli. Všetko v samostatnom procese cez existujúci eConsoleAppContainer; GUI nečaká blokujúco. Rovnaké zastavovanie pri reštarte a prepnutí CAM.
- Host testy: 82 úspešných na Python3.14.7. Skutočné neškodné procesy sleep bez PID súboru: bežný končí TERM, ignorujúci TERM končí KILL; iný executable zostáva bežať. Test aj opätovného použitia PID, zombie, staršieho kernelu a odmietnutia štartu po neúspešnom zastavení.
- Po návrate používateľa: nainštalovať r18, reštart GUI, pri oscam-master skúsiť červené Zastaviť → žiadny aktívny CAM, zelené Štart → aktívny CAM, znova zelené Reštart → aktívny CAM. Bez ručných kill príkazov. Potom pokračovať pravou ponukou (Zmazať CAM/SRV, štart konfigurácia a ďalšie), nepreskočiť zvyšok menu.
- Stav r18 zatiaľ potvrdený iba host testami; plná validácia pluginu stále nie. Produkčná vetva a automatická produkčná aktualizácia sa nemenia.


## 2026-10-25 — prijímač r18 overený, r19 ponuka INFO

Potvrdené snímkami na prijímači:
- 053948/1: Script zastavenia vykonaný + Žiadny spustený CAM/SRV + Aktívny CAM Žiadne. /2: štart úspešný, master aktívny. /3 priebeh reštartu a /4 Script reštartu vykonaný + master aktívny.
- 055133: odinštalačný zoznam obsahuje len balík master/r4; ručný uni sa správne neponúka. 055228 je iba potvrdzovací dialóg; ochrana sa vykonáva až po Áno. 055405: bežiaci master zablokovaný hláškou používa sa, nemôže byť odinštalovaný.
- 055521: po zastavení odstránenie balíka dokončené; package skript volí softcam None; upravené konfigurácie ponechané. FAILED je opakované stop z package skriptu pri už zastavenom CAM-e, nie zlyhanie odstránenia.
- 055656: opätovná inštalácia OE6.0/r4 dokončená, master štartuje OK. Používateľské konfigy zachované; package vzory zapísané ako -opkg.
- 055902: zapnutie farebných skratiek; 060110/060111: zadané 010 a riadok ukazuje10s; 060215: reštart SRV zapnutý; 060310: autokontrola vypnutá. Overené prepnutie nastavení, nie natívny odložený štart ani automatická obnova/SRV.
- 061613: GSU vyžiadalo reštartGUI kvôli nastaveniam; používateľ reštartoval. 062133/1 zelené otvára OpenATV pluginy, /2 červené bez ECM okna. Skratka červeného nepotvrdená funkčná.
- Overený aktuálny zdroj OpenATV: ButtonSetupActions má prioritu-10; červené HbbTV má0 a activateRedButton vraciaNone aj pri bezčinnej vetve. Short INFO je InfoPressed, long INFO showEventInfoPlugins. 063818/063817 používateľ potvrdzuje eventview a natívnu ponuku rozšírení.
- Po otázke na INFO používateľ odsúhlasil doplnenie GSU – ECM Info do dlhej INFO ponuky. Rozpracovaný zásah do obsluhy červeného bol odstránený; r19 žiadne nové monkeypatch/keymap zmeny neobsahuje. Pridaný len WHERE_EVENTINFO descriptor, event_info.py callback a reprodukovateľná zmena port_source.py. 84 host testov úspešných na3.14.7.

Ďalšia skúška: nainštalovať r19 + reštartGUI, počas TV podržať INFO → GSU – ECM Info → OK. Má otvoriť pôvodnú obrazovku ECMInfo. KrátkeINFO má naďalej otvárať reláciu a zelené pluginy. Potom zostávajú OScam štart konfigurácia (natívny editor stále sivý), native autostart/autocheck a zvyšné položky hlavného GSU menu. Pripraviť exp.image je sivé; nezačínať zásahy do image bez kontroly účelu. Produkčná vetva ani updater sa nemenia.


## 2026-10-25 — r19 ECM overené, dohoda o jednom prístupe, r20

- Snímka064453: r19 dlhéINFO → GSU ECM Info otvorilo pôvodné ECM Informácie, správne OSCam11968, Irdeto a ECM Time. Jedna snímka potvrdzuje načítanie, nie časovú aktualizáciu.
- Snímky064719 a065148: v dlhom modrom je už päť GSU položiek (hlavnéGSU, kanál, systém, CAM/SRV, zariadenia). Používateľ výslovne nechce kombinovať prístupy a nové skratky. Schválené odstrániť starú zelenú/červenú voľbu a sústrediť aj ECMInfo do tohto menu.
- r20: ECM descriptor presunutý z WHERE_EVENTINFO na WHERE_EXTENSIONSMENU, názov (GSU) ECM Info. MenuINFO sa už GSU položkou nerozširuje. Všetky ostatné rozšírenia zostávajú.
- Odstránená registrácia monkeypatch InfoBarPlugins pri sessionstart. Pôvodné názvy shortcut funkcií sú ponechané len ako úmyselne neaktívne kompatibilné vstupy; par40 sa číta kvôli starým settings, ale nemá účinok.
- Voľba Keystart/Enable CAM-SRV ECM Start odstránená z CAM správcu, modré ju pri prechádzaní preskočí. Riadky oneskorenia, reštartuSRV, autokontroly a exp.image presunuté po jednom do pôvodných pozícií predchodcu pre SD/FHD/UHD. Nerobí sa nový dizajn. Zatvorenie už nevyžaduje reštart kvôli vyradenej voľbe.
- Build vynecháva iba GSUmain keymapcontext; UCMActions (ovládanie vo vnútri správcu) ponechané. Pôvodné zdrojové skiny a archív resources nemeníme.
- 88 host testov na Python3.14.7 úspešných; AST zo zdrojovej transformácie sa zhoduje s runtime. Na prijímači r20 zatiaľ neoverené.

Ďalšie kroky: inštalácia r20 + reštartGUI (odstráni aj už načítaný starý hook), dlhé modré → (GSU) ECM Info → OK, krátke/dlhéINFO pôvodné správanie a zelené pluginy. CAM správca nemá Keystart riadok ani medzeru, modré prechádza z OScam štart konfigurácia priamo na oneskorenie. Potom pokračovať položkami hlavnéhoGSU podľa používateľa, nevydávať úplné potvrdenie native autostartu/autocheck/SRV ani sivého native cfg editora.


## 2026-10-25 — ďalšia práca iba v CAM/SRV, r21 natívna štart konfigurácia

- Používateľ zrušil drobnú požiadavku na celý CAM riadok v ECM okne: neimplementovať, počká na redesign. Výslovný postup: dokončiť jednu sekciu úplne a až potom ďalšiu; neodbočovať na OSD ECM.
- Zostávajúce poradie: OScam štart konfigurácia → odložený štart → autokontrola → samostatný SRV → preverenie Pripraviť exp.image. Otvorenie ECM v r20 je doložené snímkou065742; cestu cez dlhé modré posledná odpoveď označuje podmienečne, keďže snímka zachytáva až samotné ECM okno.
- Používateľ dodal skutočné --help z oscam-master 2.26.09-11968@39e78a46. ConfigDir /etc/tuxbox/config/oscam-master, temp /tmp/.oscam. Podporuje -c,-t,-b,-B,-r0/1/2,-w,-I,-S,-d,-p(max4096,default32),-a,-s,-g1/2. UTF8 vo výstupe nie je, preto ho natívny editor neponúka. Pôvodný editor zapisoval do Oscam_Srv.sh a pre native nefungoval.
- Vysvetlený účel štart konfigurácie: pokročilé parametre spustenia, nie konfigurácia kariet/reader/server. Používateľ chápe rozdiely image a prikázal pokračovať.
- r21 natívny editor otvorí pôvodný oscam_start skin, ale lokálne položky pre vybraný CAM. Read actual --help/init v deferToThread; ukladanie tiež mimo GUI. Zrušenie nič nemení v globálnych GSU nastaveniach ani na disku. Názov CAM v titulku.
- Nastavenia per CAM: /etc/enigma2/gsu-softcam-start/NAME.json, prvý originálny init backup NAME.init-backup. Uloženie nemení bežiaci CAM. Prefix iba na rozpoznanej jedinej daemon invocation; zachová shellpipeline, PIDFILE, daemon a neznáme originálne argumenty. Konfigy OSCam sa neprepisujú. Chýbajúca cesta, neznámy skript či zmena skriptu počas editácie zastavia zápis.
- GSU start/restart/switch používajú worker a pred startom reaplikujú uložený adaptér po prepísaní package init skriptu. Externý package postup môže do tejto reaplikácie použiť pôvodné parametre. Pri odstránení GSU prerm --restore-all vracia aktuálny init príkaz (nie starý celý backup), aby nezmazal iné admin/package úpravy.
- Natívne spúšťanie na pozadí a PID súbor sú v editore pevné hodnoty podľa služby, ostatné podporované voľby editovateľné. Ladenie je maska0–65535, pending1–4096. Pôvodný UCM editor pre legacy vetvu zostáva.
- 102 testov na Python3.14.7 úspešných. Reálny neškodný shellový init → Python adaptér → argv recorder overuje medzery a shellové znaky v cestách bez vykonávania ako shell. Testy rušenia, rollbacku, chyby, stale script, oddeleniaCAM, aktualizovaného initu a odinštalovania. Nový native editor a štart s jeho hodnotami zatiaľ len host overenie.

Najbližšie na prijímači: r21 inštalácia + reštartGUI, Správca CAM/SRV → vybrať oscam-master → pravá OScam štart konfigurácia → žlté. Najprv snímka hodnôt a overiť načítané cesty. Potom skúška Cancel bez zápisu; následne uložiť napríklad debug128 alebo restart1, overiť uloženie a zelený reštart, podľa /proc cmdline skutočné parametre, následne vrátiť pôvodné hodnoty. Neoznačiť native štart editor za receiver-potvrdený bez týchto dôkazov. Žiadny presun do druhej hlavnej sekcie.


## 2026-10-25 — r21 chyba otvorenia, r22 oprava

- Používateľ dodal snímku073119: Nepodarilo sa načítať štart konfiguráciu OSCam-u / exec() arg1 must be a string, bytes or code object. Editor sa neotvoril a používateľ nič neukladal.
- Overený aktuálny OpenATV Screen.py: onLayoutFinish callback, ktorý nie je typu boundmethod, sa posiela do exec(). V novom editore bol lambda callback pre titulok. Toto je chyba nášho kódu, nie potvrdený problém OSCam configu.
- r22 mení titulok na bound metódu set_title. Súčasne odstraňuje kolíziu self.values(): Screen.values musí vracať GUI komponenty pri execBegin/show/hide, nie slovník hodnôt nastavení. Zber nastavení teraz collect_values.
- Dva nové regresné testy reprodukujú presné rozlišovanie boundmethod/exec aj iteráciu komponentov. 104 testov na Python3.14.7 úspešných; kompilácia a deterministický build tiež. Skutočné otvorenie editora na prijímači zatiaľ nepotvrdené.
- Najbližšie iba r22 inštalácia + reštartGUI → Správca CAM/SRV → oscam-master → OScam štart konfigurácia žltým → snímka pred uložením. Zostávame výhradne v CAM/SRV.


## 2026-10-25 — r22 prijímač a r23 oneskorený natívny štart

- Snímka074434: natívny editor oscam-master sa správne otvoril, zobrazuje cesty /etc/tuxbox/config/oscam-master, /tmp/.oscam a /var/tmp/oscam-master.pid. Snímky074823(1–3): potvrdenie uloženia, následný reštart, aktívny oscam-master a obnovené ECM údaje. Ukladané pôvodné hodnoty; zmenená voľba v /proc cmdline ani Cancel zatiaľ nedoložené.
- Pri kontrole par48 zistené, že pôvodný AutoCams časovač štartuje iba v else vetve pri úspešnom timeout.connect, fallback ho nespustí. Navyše pôvodný startCamSrv obsahuje nedosiahnuteľnú vetvu a používa len legacy UCM skripty. Natívny CAM túto hodnotu nepoužíval.
- r23 pridáva samostatný jednorazový časovač pre vybraný natívny CAM po sessionstart. Používa par48, podporuje connect aj zoznamové signály; zrušenie pri ukončení GUI. Worker po čase znova overí pôvodný výber a aktuálne procesy. Bežiaci CAM (aj iný) nepreštartuje. Chýbajúci vybraný CAM spustí overenou natívnou službou. Priečinky ani boot služby image nemení. Preto nejde o vynútené oneskorenie služby, ktorú už pred Enigmou spustilo OpenATV.
- /tmp/gsu-softcam-autostart.log má monotónne časové značky; scheduled, skipped alebo starting/started, worker finished. Log je obmedzený, neobsahuje heslá, nesleduje symlinky. Mount checker zostáva samostatný. Autokontrola a samostatný SRV sú stále ďalšie úlohy; legacy UCM vetva zostáva neoverená.
- 112 testov na Python3.14.7: časovač bez GUI blokovania, spustenie až v callbacku, len raz, oba signálovéAPI, cancel, zmenený výber, už bežiaci/ iný CAM, chyba štartu, session hook a zachovanie mount checkeru. r23 na prijímači zatiaľ neoverené.

Najbližšie: inštalácia r23, reštartGUI, počkať aspoň nastavený čas a `cat /tmp/gsu-softcam-autostart.log`. Pri už bežiacom OSCam očakávať skipped: already running a žiadny výpadok. Potom kontrolovaná skúška: zastaviť CAM v GSU, reštartovať iba GUI, sledovať záznam a či sa chýbajúci CAM spustí po nastavenom čase. Ak image spustí CAM skôr, záznam má ukázať skipped, nie predstierať potvrdenie oneskoreného štartu. Zostať v CAM/SRV.


## 2026-10-25 — r23 prijímač potvrdený, r24 autokontrola natívneho CAM

- Používateľ dodal /tmp/gsu-softcam-autostart.log: 7821.959 scheduled master delay10, 7832.561 skipped alreadyrunning, 7832.633 code0. Druhá skúška po zastavení CAM a reštarte ibaGUI: 7956.977 scheduled, 7967.600 starting, 7968.959 started, 7969.171 code0. Potvrdené obidve vetvy jednorazového oneskoreného štartu na prijímači.
- Používateľ prikázal pokračovať; stále iba CAM/SRV. r24 dopĺňa natívnu autokontrolu par50. Interval zachovaný600s, prepínač aplikuje zmenu okamžite. Samostatný timer, žiadne proc scan/stop/start v periodickom GUI callbacku. Kontrola výberu, identity a štart sú vo worker procese.
- Proces beží → nič nereštartovať. Vybraný CAM chýba → start_verified. Iný natívny CAM beží → nič nespúšťať. Nehodnotiť ECM/FTA ako poruchu. Chyba → ďalší pokus až po normálnom intervale, bez nekonečného spinneru.
- Ručné Zastaviť v GSU pozastaví automatiku pre konkrétny CAM v danej GUI session. Úspešný ručný štart/reštart obnoví dohľad. Neúspešné zastavenie vráti predchádzajúci dohľad; neúspešný štart po zámernom zastavení zachová pauzu. ReštartGUI vytvára novú session a oneskorený štart ostáva ako v r23. Externý stop mimoGSU sa nedá odlíšiť od výpadku; pri zapnutom dohľade sa obnoví.
- /run/gsu-softcam-session.json: atomický token/enable príznak. Ručný príkaz a shutdown zneplatnia čakajúce automatické workery. Vypnutie par50 zneplatní periodickú kontrolu, neblokuje počiatočný štart. /run/gsu-softcam-operation.lock serializuje CLI natívne príkazy iba vo workeroch. Žiadne zamykanie na GUI vlákne. Ochrana pred duplicitným dokončením callbacku.
- 123 testov na Python3.14.7. Zahŕňajúoba signálovéAPI, živý toggle, interval600s, opätovné plánovanie, ručnú pauzu, neúspešný stop/start, zmenuvýberu, stale guard, disable a shutdown, chybu workera. Reálny druhý Python proces potvrdzuje filelock: čaká na uvoľnenie prvého, potom pokračuje. Zdrojová transformácia reprodukuje runtime. Reálna periodická obnova na prijímači zatiaľ nepotvrdená.

Najbližšie: r24 inštalácia + GUIrestart, pravá ponuka Povoliť autokontrolu CAM/SRV žltým → text Zakázať autokontrolu a log autocheck enabled interval600s. Po desaťminútovom cykle log autocheck checking a skipped alreadyrunning. Potom kontrolovaná simulácia výpadku mimo GUI: CLI native_softcam.py --action stop --name oscam-master (obchádza len manuálnu GUI pauzu; používa overené zastavenie), neprepínať výber; do ďalšieho cyklu sa má obnoviť. Ručné Zastaviť v GSU naopak musí zostať zastavené aj cez celý cyklus, až zelený štart obnoví dohľad. Možno vrátiť vypnuté pôvodné par50. Ďalšia položka až po potvrdení: samostatný SRV, potom exp.image; neopúšťať sekciu.


## 2026-10-25 — r24 autokontrola potvrdená, r25 zrýchlenie

- Prijímač: 8715.233 autocheck enabled interval600s; 9315.235 checking, 9315.765 alreadyrunning, 9315.848 code0. Kontrola po600s a bežiaci CAM nedotknutý.
- Simulácia výpadku príkazom native_softcam.py --action stop --name oscam-master: služba stopOK. 9915.850 checking, 9916.462 starting, 9917.775 started, 9917.855 code0. Automatická obnova na prijímači potvrdená.
- Ručné zastavenie červeným v GSU v9:34: log9985.387 manual stop master ok. Následne10585.389 a11185.404 skipped manualstop/commandinprogress. Potvrdené rešpektovanie zámerného zastavenia počas dvoch celých intervalov. Používateľ správne odmietol desaťminútové čakanie pri reálnom výpadku; odsúhlasil15s a postupne dlhšie prestávky po chybe. Najprv výslovne požadoval dokončiť starý test; r25 sa dovtedy nepublikovala.
- r25: natívny základný interval15s, po zlyhaníworkera30/60/120/240/max300s. Úspech návrat15s, ručný príkaz/reconfigure/inýCAM ruší starý failure delay. Zrušený starý worker nesmie meniť delay novšieho zámeru. Prvé periodické plánovanie až po dokončení/skončení odloženého štartu; nepredbehne ani počiatočný30s delay.
- Pomocník pri natívnomCAM zobrazuje15s vrátane slovenskej fallback lokalizácie. Pôvodná10min UCM vetva sa nemení; nejde o tvrdenie, že legacyUCM bol týmto obnovený. Ochrany ručného zastavenia a serializácia z r24 ostávajú.
- 128 testov Python3.14.7 vrátane rastu a stropu delay, návratu poúspechu, resetu po ručnomzásahu/zmeneCAM, stale completion a nepredbehnutia startupdelay. Kompilácia, transformáciazdroja a deterministický build kontrolované. Nových15s a backoff na prijímači zatiaľ neoverené.

Najbližšie: r25 inštalácia + reštartGUI. Autokontrola má zostať zapnutá, log enabled interval15s. Po počiatočnom štarteCAM a aspoňjednom autocheck cykle možno zopakovať externý CLI stop (nie červenýmGSU); do ďalšej15s kontroly plus čas štartu sa obnoví. Po približne30s tail log. Potom krátka skúška červenéhoGSU stop cez dva15s cykly a zelenýštart naobnovu. Až potom samostatnýSRV a exp.image. Žiadny presun doďalšej sekcie.


## 2026-10-25 — r25 potvrdené, r26 podmienené SRV

- Prijímač r25:11539.680 scheduled10s, enabled interval15s.11549.680 autostartchecking,11550.325 alreadyrunning code0. Po externomCLI stop11565.424 checking,11566.021 starting,11567.395 started,11567.468 code0;11582.502 ďalšia kontrola alreadyrunning. Potvrdený15s interval a úspešnáobnova. Backoff pri chybe zostáva host-testovaný.
- Prvý dodanýlog nemal manualstop aCAM stálebežal; neopísali sme toakochybu pauzy, vyžiadali explicitné zastavenie. Potom11713.169 manualstopmasterok,11728.170 skippedmanualstop. Snímky090342 potvrdzujú Žiadny spustenýCAM aAktívnyCAMŽiadne; následná090449 Scriptspustenívykonaný, Aktívnyoscam-master aECM. Potvrdené zámerné zastavenie aj následný štart. Samotná snímka nedokazuje ďalšíperiodický cyklus po ručnomštarte; netvrdiť navyše.
- Používateľ riešil zmyselSRV a programyNCam/CCcam/iné. Vysvetlené samostatnýlokálnyserver verzus vzdialenýserver/protokol. Odsúhlasil SRVštandardneskryť a zobrazovaťlen pri podporovanom nainštalovanom samostatnomserveri; nemažemefunkciu anikonfiguráciu.
- r26: početSRV vychádza z platných presne*_Srv.sh. binarystatus číta obmedzenýtext, literalSrvBin bezexpanzií/traversal, vyžaduje spustiteľnýskript a spustiteľnýbinárnysúbor. Skript musí byť vexistujúcomUCMadresári, nečítaaliasinam. Žiadne spúšťanie ani sieťpridetekcii. Zálohyskriptu a chýbajúce/neplatnébinárky sa zaSRVnepočítajú.
- BezSRV ConfigList ibaCAM, druhépôvodnéšípky pomenované akoPixmapkomponenty a skryté spolu sactivSrv/SrvPic/txt7. Pravétxt8/txt9 idú do predchádzajúcichpresnýchpozícií, modrépreskočí7, priamaaktivácia7 bezSRV ničnerobí. Captiongettext používa pôvodnékľúče, výslednéCAM/SRVsa skráti naCAMlenbezservera. PriCamSrvListrefresh sa viditeľnosť/riadky/pozície/označenia obnovujú obojsmerne. ConfigList sa priodstráneníSRVvráti naindex0, ukazovateľ z7na8.
- PôvodnéUCMštart/stop/SRVrestart a par49 sa zachovávajú, nie sú týmreceiver-overené. Rovnako žiadna nová univerzálnadetekcia natívnehocardserveraostatnýchimage; podporovanýje existujúciUCMformát.
- 135testov Python3.14.7: executable-only discoverybezvykonania, nesprávnenázvy aaliasy, prázdnyserverlist, preskok/skrytiereštartu, obnova po inštalácii aopätovnéskrytie po odstránení, rozmery a posuny, šípkyvSD/FHD/UHD. NativeAPIstubs doplnené o skutočnéčíselnébody/rozmery. Zdrojovátransformácia reprodukujeruntime. r26receiverzatiaľneoverené.

Najbližšie iba nainštalovaťr26 + GUIrestart aotvoriťSprávcuCAM. Na tomto prijímači bezSRV má byť jedenCAMriadok, bezAktívnySRV/šípokdruhéhoradka/reštartuSRV, názvySprávcaCAM, StiahnuťCAM aZmazaťCAM. Modré musípreskočiť zOneskorenieštartu priamonaAutokontrolu. Po potvrdeníriešiť poslednúpoložkuPripraviťexp.image; neoznačiť nepoužívanýSRVruntimezafunkčneotestovaný.


## 2026-10-25 — r26 zobrazenie potvrdené, r27 úplné odstránenie exp.image

- Snímka092425 z r26 potvrdzuje názov Správca CAM, iba riadok CAM-y(2), skryté SRV šípky/stav/reštart a kompaktné pravé menu. OSCam aj ECM sú aktívne. Navigácia modrým zostáva overená host testami; zo snímky ju nemožno potvrdiť.
- Používateľ sa pýtal na účel položky Pripraviť exp.image. Reálny kód zastavoval, zakazoval, odinštalovával alebo mazal dccamd. Vytváral kompatibilné odkazy starých ciest a upravoval bootup/bootmisc. Po vysvetlení používateľ výslovne prikázal funkciu celkom odstrániť.
- r27 odstraňuje metódy univCamMng.killDccamd, doLnk a chckDccamd úplne, bez neaktívnych náhrad. Odstránené sú tiež txt9, aa[9], obsluha indexu9, enaYellow a inicializačné kontroly dccamd a starých ciest. V plugin.py nezostal kód tejto funkcie na úpravy systému.
- compact_skin odstraňuje txt9 vo všetkých rozlíšeniach. srv_visibility už neodkazuje na jeho riadok ani pomocníka. Modré po Autokontrole (index8) prejde na Ukončiť (index0). Podmienená podpora SRV a nastavenia CAM zostávajú zachované.
- Pôvodný historický manifest ani grafické assety sa nemenia. Test inventára povoľuje presne tri používateľom odsúhlasené odstránenia; ostatné pôvodné názvy a signatúry stále overuje. remove_exp_image_port reprodukuje odstránenie ako posledný krok zdrojovej transformácie.
- Prešlo136 testov na Python3.14.7, kompilácia a deterministický build. Testy overujú návrat menu, neprítomnosť widgetu, pomocníka a metód aj zachovanie existujúcich CAM a SRV kontrol. Zobrazenie r27 na prijímači zatiaľ nie je potvrdené.

Najbližšie: inštalácia r27, reštart GUI a snímka Správcu CAM bez Pripraviť exp.image. Modré musí z Autokontroly prejsť na Ukončiť. Skutočná prevádzka samostatného SRV zostáva neoverená, pretože na prijímači nie je nainštalovaný.


## 2026-10-25 — r27 prijímač potvrdený; r28 OSD ECM a kontrolka CAM

- Snímky093241/093350/093351 potvrdzujú odstránenie exp.image z r27 a návrat modrým z Autokontroly na Ukončiť. Pomocník uvádza15 sekúnd. OSCam a ECM ostávajú aktívne.
- Používateľ požiadal o zelený znak pred CAM spustené a červený pri zastavení. Výslovne chcel túto kozmetiku spojiť s ďalším krokom, bez samostatného IPK.
- Ďalšia sekcia je OSD ECM. Používateľ sa pýtal na účel, porovnal ho s ECM Info cez dlhé modré a chce vidieť skutočnú ukážku. OSD zatiaľ zachovať; nejde o požiadavku odstránenia. Následne explicitne autorizoval všetko opraviť a sprístupniť. Pôvodný vzhľad sa nemení.
- r28 opravuje chybný tok readEcmInfo: priradenie času a volanie ECMparser boli za return vo vetve nezmeneného súboru. Pri novom súbore tak caid a ďalšie premenné nemali hodnotu. Parsovanie teraz predchádza porovnaniu zmien. Opravená voľba static/rolling a návrat po unsupported-CA správe.
- Statické widgety sa vytvoria pri oboch eTimer signal API. prepareOsd je bound layout metóda a vypína orezávanie viacriadkových štítkov. Čas parser normalizuje na sekundy, prah sa preto porovnáva po násobení1000.
- Vypnutie a koniec služby zastavia oba časovače a vyčistia cache. FTA má jasnú informáciu, nečíta staré ECM z kódovanej stanice. Scrolling začne s krátkym odsadením. Režimy stále používajú pôvodné skiny; zmena typu zostáva s pôvodným GUI restart potvrdením.
- Polohovací dialóg stopne časovač na OK aj späť a hranice počíta podľa reálneho rozmeru obrazovky a okna. Save/cancel zahrnie aj voľby, ktoré sa po vypnutí OSD skryli. Samostatné potvrdenie polohy zostáva zachované.
- Kontrolka statPic pri natívnom CAM: zelená pri aktívnom procese, červená pri zastavení. Inicializácia aj dokončenie ručných príkazov aktualizujú farbu. Existujúci500ms timer žiada najviac raz za sekundu async active_name cez deferToThread, nie proc scan na GUI vlákne. UI sa aktualizuje len pri zmene. Generácia bráni použitiu starého výsledku po ručnom príkaze, closed guard po zatvorení.
- Prešlo149 testov Python3.14.7 vrátane oboch OSD režimov/API, zmeneného a nezmeneného ECM, prahu času, chýbajúceho súboru, FTA, vypnutia, polohy, skrytých nastavení a async farieb/stale výsledkov. Zdrojové transformácie reprodukujú runtime. OSD ani farby na prijímači r28 ešte nie sú potvrdené.

Najbližšie: inštalovať r28 a reštartovať GUI. OSD ECM informácie → Povoliť Áno, ponechať Rolované info, zelené Uložiť, zavrieť GSU a prepnúť na kódovanú stanicu. Po krátkom štarte má ísť posúvaný text cez TV obraz; vyžiadať skutočnú snímku a spätnú väzbu. Potom skúsiť Statické info a potvrdiť požadovaný GUI restart. Overiť polohu a vypnutie bez pretrvávajúceho overlay. Súčasne v Správcovi CAM overiť zelenú/červenú pred stavovým riadkom vrátane automatickej obnovy. Zostať pri OSD až do dokončenia sekcie.


## 2026-10-25 — r28 rolované OSD potvrdené; r29 širší riadok

- Snímky100013(1–3) ukazujú povolené OSD, Rolované info, prah500ms, obnovu4s a rýchlosť150ms. Posúvaný text je viditeľný nad nastaveniami, nad Správcom CAM aj počas samotného sledovania TV. Rôzne úseky textu a používateľov popis potvrdzujú rolovanie. Zelená kontrolka pri CAM spustené je potvrdená. Červená a statický panel ešte nemajú receiver dôkaz.
- Používateľ oprávnene uviedol, že pôvodný krátky riadok ukazuje len útržok údaja a neplní účel. r29 preto rozširuje iba rolované OSD na polovicu šírky obrazovky:640/960/1920px pri1280/1920/3840px. Písmo, výška, rýchlosť a obsah zostávajú zachované.
- osd_layout.rolling_skin je spoločný pre skutočný overlay aj SelectPosition. Pôvodné bitmapové orámovanie sa za behu nahradí dvoma natívnymi farebnými obdĺžnikmi s tenkým modrým okrajom; žiadne zmeny či nové kópie obrázkov. Statický skin ostáva pôvodný.
- place zobrazenie obmedzí na reálne hranice okna a desktopu bez automatického uloženia starých súradníc. Pri nastavovaní polohy súradnice zodpovedajú viditeľnej pozícii, aby sa šípkami dalo hneď pohybovať. OK a späť ďalej riadia uloženie/zrušenie polohy.
- Prešlo152 testov Python3.14.7 vrátane šírky/písma/okraja pri troch rozlíšeniach, zhody overlay/preview a obmedzenia polohy bez zápisu. Zdrojová transformácia reprodukuje runtime; kompilácia a deterministický build sú kontrolované. Nová šírka ani statické OSD ešte nie sú overené na prijímači.

Najbližšie: inštalácia r29 a reštart GUI; OSD môže zostať povolené z r28. Prepnúť na kódovanú stanicu a poslať snímku širšieho rolovaného riadka. Ak poloha nevyhovuje, OSD nastavenia → Nastaviť pozíciu → OK a šípky. Potom dokončiť test statického typu, jeho prepnutia s GUI restartom, polohy a vypnutia. Nepreskakovať do ďalšej sekcie.


## 2026-10-25 — r29 širší riadok prijatý; r30 pravý odstup

- Snímka101012 potvrdzuje širší rolovaný riadok r29. Končí však presne na pravej hrane, takže rámik vyzerá odstrihnutý. Používateľ chce skrátiť pravú stranu a výslovne uviedol, že inak je zobrazenie už OK.
- r30 skracuje rolované okno o šírku desktopu/32:40px pri1280,60px pri1920 a120px pri3840. Pri Full HD má preto900px namiesto960 a pri aktuálnej obmedzenej polohe začína stále na960, končí na1860 a necháva60px odstup.
- Pôvodný ľavý začiatok pri zobrazenej polohe sa nemení. right_limit je spoločný pre zobrazenie a pravú šípku polohovacieho dialógu. Aj pri pohybe doprava tak zostane odstup. Statické OSD používa pôvodné hranice; písmo, výška, obsah ani rýchlosť sa nemenia.
- Prešlo152 testov Python3.14.7 s aktualizovanými kontrolami šírky, pravého odstupu, overlay/preview a polohy. Zdrojová transformácia reprodukuje runtime. r30 na prijímači zatiaľ nepotvrdené.

Najbližšie: r30 inštalácia a reštart GUI, potvrdiť viditeľný pravý rámik s odstupom. Potom dokončiť statický typ OSD a vypnutie/polohu; nepresúvať sa do ďalšej sekcie bez dokončenia.

## 2026-10-25 — OSD ECM uzavreté; r31 správa swapu

- r30 prijímač: 102717 potvrdzuje celý rolovaný rámik s pravým odstupom; používateľ schválil. 103231 statický panel čitateľne zobrazuje CAID/CHID/PID/SID/Using/Time/System/CAM. 103523 potvrdzuje ručný presun doprava; používateľ výslovne nechce polohu nastavovať napevno. 103706 po reštarte GUI drží polohu. 103912 po vypnutí panel zmizol, používateľ potvrdil OK. OSD ECM sekcia uzavretá v tomto overenom rozsahu.
- Ďalšia sekcia Správa swapu: 104140 zobrazuje /dev/mmcblk0p12 (partition) a /media/hdd/swapfile (file), po262140KiB, využité0. 104232 editor otvorený, predvolené Žiadne a automatický časový názov. 104334/104335 voľby disku iba Žiadne alebo /media/hdd. Používateľ nevytváral ani nemazal swap; odsúhlasil opravu pred skúškou.
- r31 swap_ops.py: parsovanie /proc/swaps s dekódovaním ciest; lokálne rw ext2/ext3/ext4/XFS mounty pod/media bez hardcoded názvu disku. Žiadne shellové skladanie príkazov, limit45s pre systémové nástroje, kontrola kódu aj aktívneho swapu. Exkluzívne vytvorenie0600, žiadne prepisovanie existujúceho súboru/symlinku,16MiB rezerva; postupné fyzické vyplnenie nulami mimoGUI. Pri chybe nový swap vypnúť a až potom zmazať; pri zlyhaní vypnutia súbor zachovať a hlásiť chybu.
- Mazanie swapových oddielov odmietnuté pred akciou; iba vybraný aktívny regulárny súbor na podporovanom médiu, bez symlinkov/hardlinkov. swapoff musí skončiť úspešne a swap zmiznúť z/proc/swaps. Potvrdenie má defaultNie a zachytáva konkrétnu cestu.
- Zmenyfstab presným prvým poľom a typomswap, zachované komentáre a podobné názvy; atomický zápis s právami/vlastníkom a kontrolou zistených súbežných zmien. Pri zlyhaní zápisu/odstránenia obnoviť konfiguráciu/aktiváciu, ak je to možné. Pôvodný globálnydeleteFstab používaný inými sekciami zatiaľ nedotknutý. Lock serializuje iba GSU swapové operácie.
- swap_ui.py: pôvodné obrazovky a ovládanie, deferredworker na objavenie diskov aj mutácie, viditeľný stav cez titulok, ochrana opakovania a zavretia počas operácie, neskorý callback po zavretí ignorovaný. Chyba ponechá editor otvorený, úspech až po overení a konfigurácii. swap_port.py reprodukuje zmeny a zachováva pôvodné signatúry.

Najbližšie: nainštalovaťr31 a reštartGUI. V Správe swapu najprv na oddiele skúsiť žlté: má iba vysvetliť, že oddiel sa tu nemaže. Potom Pridať→32MB, /media/hdd, názovgsu_test; vytvoriť a sledovať odozvu a výsledok. Overiť tretí aktívny riadok a presnýfstabzáznam; potom zmazať iba/media/hdd/swapfile_gsu_test, overiť návrat k pôvodným dvomswapom a odstránenie iba testovacieho záznamu. Existujúce swapy zachovať. Nemeniť ďalšiu sekciu, kým sa tento postup nedokončí.

## 2026-10-25 — r31 prijímač: správa swapu uzavretá v overenom rozsahu

- 112039: žlté na /dev/mmcblk0p12 odmietlo mazanie hláškou „Swapové oddiely sa v tejto ponuke nemažú.“
- 112255 snímky1/2: vytvorený /media/hdd/swapfile_gsu_test, 32MiB (32764KiB aktívnych), tretí aktívny riadok s prioritou-3; pôvodný oddiel a /media/hdd/swapfile zostali aktívne. Odozvu počas dlhého vytvárania nemožno dokázať zo statických snímok.
- 112421/112422 snímky1–3: potvrdenie obsahuje presnú testovaciu cestu, úspešné zmazanie a návrat k dvom pôvodným aktívnym swapom.
- Používateľ následne dodal ls: /media/hdd/swapfile_gsu_test neexistuje; grep -F swapfile_gsu_test /etc/fstab bez výstupu. Overené odstránenie súboru aj jeho konfiguračného záznamu. Sekcia swap uzavretá v rozsahu týchto úspešných skúšok; zlyhania a rollback sú host-testované, nie zámerne vyvolané na prijímači.
- Ďalšia položka v hlavnom menu je Channel Settings (Nastavenia staníc), settings_satxml → settings_center: importZIP/RAR z/tmp s dvoma voľbami, s/bez aktualizácie satellites.xml. Najprv pozrieť úvodné okno a zoznam archívov. Pôvodná implementácia má blokujúci shell unzip/unrar, chybnú skladbu ZIPcesty, vyžaduje presne6 pomocných súborov, deštruktívne odstraňuje aktuálne settingy pred overeným kopírovaním a odstraňuje zdrojový archív. Pred importom reálneho zoznamu staníc treba opraviť spracovanie, validáciu a obnovu pri chybe. Nevykonávať starý import na používateľových staniciach počas prvotnej prehliadky.

## 2026-10-25 — r32: vyradenie troch nepotrebných sekcií

Používateľ výslovne rozhodol odstrániť import zoznamov staníc („vyhodit“), následne Automatické inštalácie a Správu cron-u („urcite von a myslim aj to pod nim -spravovanie crond-u“). Správca zariadení bol len predmetom otázky na užitočnosť; v tomto balíku zostáva zachovaný.

Odstránené triedy: settings_satxml, settings_center, autoInstallMain, autoInstallMngMain, autoInstStatus, cronMng a SetupCronConf. Odstránené tri riadky menu s ID10/12/13, spúšťacie vetvy, globálna inštancia autoInstallMng, volanie autoInstallStart zo sessionAutostart, samostatný pomocník fill používaný iba cronom a import CompConsole používaný iba jeho správcom. Odstránená aj kontrola dostupnosti cron-u z hlavného menu. Teda žiadne skryté spúšťanie AutoInstall po štarte, ani keď bol historický par15 zapnutý. Staré konfiguračné kľúče zostávajú čitateľné pre kompatibilitu, bez vykonávacieho kódu.

Odstránenie nemení skutočné zoznamy staníc, archívy, systémový cron, jeho úlohy ani autostart image. CAM autostart/obnova a OSD session hooky sú zachované. Pôvodný inventár zostáva historický; test výslovne povoľuje týchto7 odstránených tried a ich metódy a globálnyfill. Runtime má55tried a13položiek menu.

ID ďalších položiek zachované. SysUtilMngMain.reactivate vyhľadáva popis podľa ID, nie podľa indexu v skrátenom zozname. 177 host testov zahŕňa popisy všetkých zostávajúcich riadkov, spustenie Správcu zariadení/Textového editora a session štart s par15=True, kde sa nevytvorí žiadny inštalačný timer ani príkaz. Transformácie reprodukujú runtime; zostavenie a syntax overené pred vydaním.

Najbližšie: nainštalovať r32, reštart GUI a overiť hlavné menu bez troch vyradených sekcií a správne pomocné texty. Správca zariadení zostáva, kým nebude jednoznačne odsúhlasené jeho odstránenie. Nepovažovať otázku na účel za súhlas so zmazaním.

## 2026-10-25 — r33: OSCam / Stav klientov

Používateľ sa vrátil k OSCam informáciám. Snímky114112 a124102: WebIf pri porte8884 ukazuje Clients1/1, klientGigablue, protokoldvbapi, camd.socket, kanálJOJ PLUS HD, stavOK. Snímka114230: GSU Stav klientov má prázdny zoznam a iba bodky v detailoch. Používateľ žiada pokračovať v oprave. Nehardcodovať modelprijímača ani menoGigablue; použiť názov účtu zOSCamu.

Príčina v kóde: oscam_Users čítal iba userconfig.html a rozpoznával presné riadkyHTML/tabulátory/poradie atribútov, potom vyžadoval konkrétny počet pozícií. Moderný usercol1 s vnoreným odkazom/iným poradím atribútov alebo oznamovacím číslom mohol preskočiť alebo zahodiť. Nepreukázané, ktorý konkrétny detailHTML bol na tomto prijímači rozhodujúci; jeho skutočnýHTMLdump nemáme.

Nové oscam_clients.py: APIpart=status typc pre živých klientov; APIpart=userstats pre účty a čítače; spojenie podľa názvu bez premenovania. Samostatné IDthid zachová viac relácií jedného účtu. Server/http/readers/proxies sa nezamieňajú za klientov. Offline účty ponechané. HTMLfallback podľa triedusercol/statuscol, data-sort-value/odkazu používateľa; dekoratívny notifier s číslom sa neprilepí k názvu. Bez štatistík zostane živý klient viditeľný, chýbajúce hodnoty sú pomlčky, nie nuly. Čítače patria celému účtu; pri viacerých reláciách nejde o samostatné per-session čítače. CWCycleAPI neposkytuje a zostáva pomlčka.

Zdroj schémy: OpenVisionE2/oscam master, webif/api.xml/status_statusbits.xml, userconfiglist_userconfigs.xml, status.xml, userconfiglist.xml, webif/userconfig/userconfig_entry.html, webif/status/status_clientstatusbit.html a module-webif.c. Nepovažovať syntetické testovacie odpovede podľa týchto šablón za zachytenú odpoveď prijímača.

oscam_clients_ui.py: pôvodnýskin a verejné metódy, sieť mimoGUI cezdeferToThread, jeden request naraz, timer8s až po dokončení, zachovanie vybratej položky podľa ID, zastavenie a ignorovanie callbackov po zavretí. Pri chybe zobraziť neúspešné načítanie, vymazať staré hodnoty a naplánovať ďalší pokus; neuzavrieť okno. Modré existujúce enable/disable najprv potvrdí konkrétny účet(defaultNie), zachytí meno pred dialógom, URLzakóduje a v pracovnom vlákne overí vrátený stav. Bez čitateľného účtu tlačidlo nedostupné. Otvorenie/obnova nikdy nemení účty.

Prešlo197 host testov naPython3.14.7 vrátane reálneho lokálnehoHTTPservera sBasicprihlásením, obochAPIendpointov, modernéhoHTMLsnotifierom2, viacerýchrelácií, chýbajúcichčítačov, neplatnejXML/DOCTYPE, výberu poobnove, chýb a zatvorenia počasnačítania. Pôvodné metódyoscam_Users majú zachované signatúry; zaniknuté vnorenécleanMe je výslovne evidovaná implementačná náhrada, podobne akogeneratePS.chck. Transformáciaoscam_clients_port reprodukujeruntime AST.

Najbližšie: nainštalovaťr33, reštartGUI, OSCam informácie→Stav klientov. Overiť Gigablue/dvbapi a aktuálnykanál, rozumnéčítače, pohybvýberu ak je viacúčtov, obnovu a odchod bezpádu. Počas prvej skúšky netreba meniť účet modrým. Ak sú údaje stále prázdne, získať odpoveďAPIstatus/userstats s odfiltrovanými citlivýmiúdajmi; nezačať hádať modelnázov.

Správca zariadení, Textovýeditor a Reset hesla zostávajú, lebo boli predmetom otázok/odporúčania, nie výslovného súhlasu s odstránením. Tri sekcie odsúhlasené v r32 sú odstránené aj v tejto verzii.

## 2026-10-25 — r33 prijímač potvrdený; r34 zarovnanie detailov klienta

Snímka120152 potvrdzuje opravené načítanie: Gigablue, zelený indikátor, dvbapi(client:Enigma2,protocolversion:3), stavOK. Viditeľné camd.socket, JOJ PLUS HD[M7Group], časové polia, OK539/NOK0/IGN0/TOUT0, CACHE0/TUN0/LTIME470ms/EOK12990/ENOK0. Nie je dokázané, či konkrétny prijímač využil XML alebo fallback; neprezentovať syntetické šablóny ako zachytené odpovede. Modré ovládanie účtu sa neskúšalo a pri tejto skúške ho netreba aktivovať.

Na zábere sa dlhý protokol a kanál zalamujú v ľavom hodnotovom Labeli, preto sa ďalšie údaje zobrazujú pri nesprávnych názvoch a zasahujú do tlačidiel. r34 cez boundprepareClients v onLayoutFinish vypína setWrap(0) na všetkých6 labeloch názvov/hodnôt. Každé explicitné odriadkovanie označuje ďalšie pole; dlhý obsah sa oreže v rámci svojho riadka a neposúva polia nižšie. V úzkom poliProtocol je iba názovdvbapi; celý pôvodný popis zostáva v hornom zozname. Údaje zOSCamu sa nemenia ani nehardcodujú.

Prešlo199 host testov: navyše presný dlhý protokol z prijímača, zachovaných5 polí v poradí adresa/protokol/kanál/čas na kanáli/idle a všetkých6 setWrap volaní cez boundlayoutcallback. Zdrojová transformácia reprodukuje runtime zo vstupu r32(c5c0812). Zachovaná pôvodná geometria a ostatné obrazovky.

Najbližšie: inštalovaťr34 a reštartGUI, otvoriť OSCam informácie→Stav klientov a porovnať spodné riadky. Protokol musí byť jedným riadkom, kanál priChannel, čas priCh_Time a nečinnosť priIdle, bez presahu do tlačidiel. Potom overiť odchod z okna a opätovné otvorenie/obnovu.

## 2026-10-25 — r34 zarovnanie potvrdené; r35 širší ľavý stĺpec

Snímka120658: r34 drží protokoldvbapi, Channel, Ch_Time a Idle na správnych riadkoch bez presahu do tlačidiel. Údaje a stavGigablueOK sa obnovujú; z jedného záberu nemožno hodnotiť celý cyklus ani reakcie ovládača. Používateľ výslovne žiada posunúť strednýOK/NOK a pravýCACHE/TUN stĺpec doprava, aby vošlo celé[M7Group].

Novýclients_skin v oscam_clients_ui upraví iba runtimeXMLtejto obrazovky: stredná skupina +šírka/12, pravá +šírka/24; ľavá hodnota sa rozšíri o posun strednej. Šírka hodnôt strednej/pravej sa primerane zmenší, aby zostali medzery a pravý okraj. PriFullHDposuny120/60px, ľaváhodnota420px, hodnotyčítačov240px. Zachované fonty, výšky, pozícia a veľkosť okna, hornýzoznam a spodné tlačidlá. Pôvodné skinové súbory a ich hash zostávajú nedotknuté.

Jednorazová kontrola geometrieSD/FHD/UHD: rozsahy skupín SD(10,100,380)/(390,500,660)/(670,790,950), FHD(15,150,570)/(585,750,990)/(1005,1185,1425), UHD(30,300,1140)/(1170,1500,1980)/(2010,2370,2850), kde trojica znamenázačiatoknázvov/začiatokhodnôt/koniechodnôt. Žiadne prekrývanie ani vodorovnýpresah; zoznam a tlačidlá majú totožné atribúty. Skutočný pribalenýprivfont pri25px: JOJ PLUS HD[M7Group] s medzerami podľaOSCamu meria316.33px, novýpriestor420px.

Prešlo199existujúcichtestov Python3.14.7, transformácia reprodukuje runtime. Najbližšie: r35inštalácia/GUIreštart a rovnaké OSCam→Stavklientov; overiť celý názovkanála s[M7Group] a čitateľné stredné/pravéčítače.

## 2026-10-25 — r35 prijímač: rozloženie schválené

Používateľ dodal snímku121510 a potvrdil „teraz to je OK“. Celý JOJ PLUS HD[M7Group] s medzerami je viditeľný, stredný a pravý stĺpec sú oddelené a riadky hodnôt sedia pri názvoch. Rozloženie ponechať. Záber potvrdzuje Gigablue/dvbapi/OK a aktuálne čítače; nepreukazuje samotné modré ovládanie účtu.

Pokračovať v tej istej sekcii: najprv modré Zakázať musí otvoriť otázku s názvom Gigablue a voľbou Nie sa zrušiť bez zmeny účtu. Potom červeným odísť a znovu otvoriť Stav klientov; overiť opätovné načítanie bez pádu. Reálne vypnutie/zapnutie účtu stále neoverené, neoznačiť za receiver-tested iba podľa dialógu. Neskákať do ďalšej sekcie počas tejto skúšky. Táto aktualizácia je iba záznam prijímača, bez nového IPK a bez zmien runtime.

## 2026-10-25 — r36 prijímač: menu a ručná kontrola aktualizácie

Snímky 1/2(20261025-132307).jpg ukazujú GSU13.40-r36, jedenásť položiek hlavného menu a jednu spodnú Aktualizáciu; Správca zariadení, Textový editor a Reset hesla nie sú v zozname. Druhá snímka zobrazuje slovenskú odpoveď „Plugin je aktuálny.“ To potvrdzuje otvorenie r36 a úspešnú kontrolu rovnakej verzie. Samotné snímky nepotvrdzujú tichú kontrolu pri otvorení, kontrolu vypnutej autokontroly, aktualizáciu novším IPK ani reštart za tri sekundy. Neskúšať ďalšiu inštaláciu rovnakej verzie len na opakovanie tejto kontroly. Ďalšie funkčné overenie zostáva autokontrola CAM; novšiu aktualizáciu overiť pri ďalšom potrebnom vydaní.

## 2026-10-25 — r36 prepínač autokontroly potvrdený; r37 čítačky/proxy

Používateľský konzolový výstup po vypnutí: Nastavenie False a Pomocný stav enabled False. Po zapnutí: iba Pomocný stav enabled True. Zdroj config.plugins.GlassSysUtil.par50 je ConfigYesNo(default=True), preto Enigma2 predvolenú True do settings neukladá. Overené oba smery synchronizácie prepínača; nie nové meranie obnovy po páde procesu alebo štartu GUI bez vybraného CAM.

Pri kontrole zostávajúcej OSCam sekcie nájdené oscam_readers.chngState: synchronný getUrlData a bezpodmienečná hláška Reader/Proxies action finished. r37 presúva načítanie/obnovu/akciu do workerov, pridáva potvrdenie Nie ako default, presný URL-encoded názov a nový kontrolný read po zmene. Chybný/nepotvrdený výsledok už nehlási úspech. Zachované pôvodné renderery, geometria, čítače a protokolové obmedzenia entitlements; opravené escapovanie názvu pri entitlements. Kontrola výsledného stavu starého neparsovateľného HTML môže skončiť neoverené aj pri skutočne vykonanej akcii; netvrdiť úspech naslepo.

Prešlo228 testov Python3.14.7 a AST reprodukcia transformácie. Prvý reálny receiver test r37 má zároveň overiť novú aktualizáciu z r36. Nevydávať zbytočnú falošnú verziu iba na test aktualizátora. Zakázať/Povoliť klienta zostáva podľa rozhodnutia používateľa bez zmeny.

## 2026-10-25 — r37 zverejnená cez vstavaný kanál

Zdrojový commit38a05f400b0de1b9363e9683afa5a02dfb114589, CI40198250001 úspešné vrátane228 testov, dvojitého deterministického buildu a publikácie. Verejný releasev13.40-r37: IPK2 186 370B, SHA2565e8775f69fffadb6480ca3556069aabc457d6db38de3fecaa3400900e14c609e, rovnaký ako lokálny. Kanálcandidate.json bol CI posunutý na r37 až po stiahnutí a porovnaní zverejnených bajtov. Parser aktuálneho feedu ponúka r37 pre nainštalovanú r36; pri r37 neponúka nič. Teraz čakáme na skutočnú aktualizáciu používateľa z GSU a následný GUI reštart, potom na skúšku čítačiek. Nespúšťať novú ručnú IPK inštaláciu namiesto skúšky updatera, pokiaľ sa neobjaví konkrétna chyba.

## 2026-10-25 — prijímač: aktualizácia r36 → r37 potvrdená

Po pokynoch otvoriť r36, potvrdiť r37, nechať dokončiť inštaláciu a GUI reštart používateľ uviedol „aktualizacia OK“. Celý postup je používateľom potvrdený ako úspešný; nejde o nezávislé meranie presného trojsekundového intervalu. Nový IPK nie je potrebný.

Nasledujúci krok v tej istej OSCam sekcii: OSCam informácie → Stav serverov/čítačiek, vybrať čítačku a stlačiť modré. Otázka musí obsahovať jej presný názov a predvolené Nie; zvoliť Nie a skontrolovať návrat bez zmeny stavu a bez pádu. Reálne vypnutie/zapnutie skúšať až potom na vhodnej nepoužívanej čítačke. Neopakovať už potvrdenú aktualizáciu ani klientské ovládanie.

## 2026-10-25 — čítačky potvrdené; všeobecné balíky a skripty výslovne vyradené

Používateľ potvrdil čítačkovú otázku s menom/defaultNie a návrat po Nie. Po reálnej skúške uviedol „obe smery funguju“. Túto časť OSCam uzavrieť v danom rozsahu.

Po začatí kontroly všeobecného inštalátora používateľ označil celú sekciu za zbytočnú a výslovne uviedol „ja by som to cele vyrazil“. Finálna r38 preto žiadny opravený všeobecný inštalátor ani testovací IPK neobsahuje. Odstránené triedy ipk_script_center, script_center, ipk_center a tar_center, položkaID5 a dispatch. Hlavné menu10 položiek. Zdieľaná odinštalovacia trieda sa používa v CAM/SRV, preto je ponechaná iba s CAM filtrom aj pri default argumente. Predvolené skripty sa už nepribaľujú/nekopírujú; existujúce používateľské súbory na prijímači sa nemažú. Skupina siedmich skriptových zdrojov v restoration/scripts bola odstránená.

229 host testov a AST reprodukcia prešli; nasleduje aktualizácia a overenie zjednodušeného menu na prijímači. Žiadny nový dizajn a žiadna zmena klientského Zakázať/Povoliť.

## 2026-10-25 — finálna r38 s odstránenou sekciou zverejnená

Zdroj baf7de36cea55f138b21b6052b00417e2f3f3b25, CI40200701330 úspešné vrátane229 testov, porovnania dvoch buildov a publikácie. IPK2 184 164B, SHA25678fd19347a24a207c2bbe575c0515a2a9159147bd6426bed003fe19fb1bfc717. Verejný v13.40-r38 a izolovaný feed už obsahujú finálne odstránenie celej všeobecnej sekcie, žiadnu z rozpracovaných opráv inštalátora. Kontrola skutočného IPK potvrdila neprítomnosť default-scripts/* a *_user.sh, postinst sa nedotýka /usr/script. Nasleduje iba vstavaná aktualizácia používateľa a potvrdenie desaťpoložkového menu.

## 2026-10-25 — vybrané Warder utility z balíka w19

Používateľ priložil enigma2-plugin-glasssysutil_13.38-w19_all.ipk (SHA256a1ec935c35ebb2bc7c320067a1aff30ed7dab565494571a891d8709cbbb83d6c). Iba staticky rozbalený/prečítaný; neinštaloval sa. Modré v tomto starom balíku otváralo GSUWarderTools so16 položkami. Po odporúčaní preniesť iba súhrnnú kontrolu stavu a diagnostický balík používateľ schválil novú položku Nástroje/Utility a výber užitočných funkcií.

r39 pridáva práve tieto2 nástroje. Kontrola používa izolovaný worker s20s timeoutom, bez externých sieťových testov a bez statvfs NFS/CIFS; menu neblokuje. Neprístupné úložisko sa neoznačí OK. Nástroje aj výsledok majú pôvodný štýl, bound layout callbacks a šípky/červené naspäť. Pri archíve ide o0600 unikátny súbor v /tmp; report.json/health.txt/README + prípadne2 obmedzené logy GSU. Konfiguračné súbory účtov a hesiel, kompletné settings, worker token a celé crashlogy sa nezbierajú. Vybrané4 GSU nastavenia, enabled guard, názov selectedCAM, procesy, hardvér a gateway/DNS sú diagnostické údaje. Text sa filtruje; JSON zostáva platný. Žiadne automatické nahrávanie súboru a žiadna zmena systému. Staré široké dashboardy a ostatné utility sa nekopírovali.

243 host testov prešlo vrátane reálneho podprocesu, archívu a regresie natívnych callbackov; AST reprodukcia súhlasí. Nasleduje zverejnenie a prvá skúška na prijímači. Bez potvrdenia používateľa neoznačiť nové obrazovky za receiver-verified.

## 2026-10-25 — r39 Nástroje zverejnené

Zdroj6652510126317d97ff223ef067ae27ef96d7fe89, CI40202236358 úspešné vrátane243 testov, dvojitého deterministického zostavenia a publikácie. IPK2 191 722B, SHA256a99d16593137b08ea881c01690b358ee61580256ebba784cb3caf3088d395920. Verejný v13.40-r39 a izolovaný feed už ukazujú na tento zhodný balík. Nasleduje iba aktualizácia používateľa priamo z GSU, Nástroje→Kontrola stavu a prvý diagnostický archív. Nové obrazovky zatiaľ nie sú receiver-verified; nesľubovať, že sú na konkrétnom prijímači overené iba podľa host testov.

## 2026-10-25 — r39 prijímač: Kontrola stavu a skutočný diagnostický archív

Snímka1(20261025-143227).jpg potvrdzuje načítanú slovenskú Kontrolu stavu s pamäťou, tromi lokálnymi úložiskami, sieťou, Enigmou, oscam-uni, teplotou a tunermi bez presahu do červeného Naspäť. Samotná snímka nedokazuje reakcie ovládača počas zberu ani posúvanie dlhého výstupu.

Používateľ následne dodal skutočný gsu-diagnostics-20261025-153329-j54ju0dp.tar.gz,3464B. Archív bol prečítaný priamo z lokálnej prílohy, nič sa nerozbaľovalo/spúšťalo. Obsahuje4 pravidelné súbory: README.txt158B,health.txt534B,report.json15024B,softcam-autostart.log1411B. JSON je platný, verzia13.40-r39, čas2026-10-25 15:33:29+0100, prijímač OpenATV8.0.1/OE6.0/Python3.14.9/Gigablue gbquad4kpro. Zistený aj vybraný CAMoscam-uni, par50True a guardTrue. Log37riadkov ukazuje opakované kontroly, skipped:already running a code0. Kontrola nenašla konfigurácie s účtami/heslami ani credential-marker riadky; log nevyžadoval redakciu. Bitrate log nie je priložený, čo je podľa dostupnosti správne. Kompletná súkromná príloha ani LAN údaje sa do verejného repozitára nekopírujú.

Tvorba a čitateľnosť archívu sú týmto overené na prijímači. Používateľ upozornil, že samostatná Kontrola stavu duplikuje Informácie o systéme. Asistent súhlasil a odporučil odstrániť iba túto samostatnú obrazovku a ponechať tvorbu balíka. Táto ďalšia úprava ešte nebola vykonaná ani vydaná; neoznačovať r39 za verziu bez Kontroly stavu.

## 2026-10-25 — r40 O plugine a odstránenie duplicitného okna

Používateľ potvrdil „ano ano, info o plugine“. Implementované Nástroje→O plugine s verziou čítanou z lokálneho version, pôvodným projektom GSU13.20, Warder Evolution ako pokračovaním/úpravami a poďakovaním pôvodným autorom bez vymyslených mien. Zmeny aktuálneho vydania sú pribalené ako release-notes.txt z update/RELEASE-NOTES.md. Header musí pri zostavení aj pri zobrazení sedieť s verziou, inak sa staré poznámky nezobrazia. Bez siete a bez nového zberu údajov; pôvodný scrollviewer/šípky/červené Naspäť.

Samostatná Kontrola stavu bola odstránená z UI, ktorú používateľ označil za duplicitu. Nástroje majú2 položky: diagnostický balík a O plugine. Interný health.txt v archíve a jeho collector sa zachovávajú pre podporu. Nepridával sa ďalší vlastný errorlog ani história aktualizácií, keďže používateľ vybral teraz len info o plugine. Prešlo245 host testov a AST reprodukcia transformácie. Nasleduje aktualizácia a skúška nového okna na prijímači.

## 2026-10-25 — r40 O plugine zverejnené

Zdroj9efd7b2389ae876b40a17f61f2399fd61b6b5ea6, CI40203765977 úspešné vrátane245 testov, dvoch totožných buildov a publikácie. IPK2 192 220B, SHA256301fed0916a080bac3b55bb5582115d941c817529d1acf14acf3c32022bb46f9. Verejný v13.40-r40 a izolovaný feed už ukazujú na tento balík. Kontrola skutočného IPK potvrdila release-notes.txt s headerom GSU13.40-r40 zhodným s nainštalovaným version. Používateľ má aktualizovať priamo z GSU a otvoriť Nástroje→O plugine. Nové okno ešte nie je prijímačom potvrdené; diagnostický archív bol overený v r39 a jeho zber sa nemenil.

### r41 hostiteľské overenie

253 testov Python3.14.7 úspešných; kompilácia a dva bajtovo rovnaké buildy. IPK3467430B, SHA256cf8363c622ef84b607465a65260e6cbdf920e669352a67f9a2d558793e5675f3. Testy pokrývajú11 riadkov aj pri zaokrúhlení HD, všetky dynamické widgety, nepriehľadné panely, zarovnanie dátumu/verzie, jazykové dátumy, oba timer signály/stop/neskorý callback, nemenné menuID/stavy/dispatch a priehľadnú160x96 ikonu. Transformácia r40→r41 reprodukovala runtime presne. Zdroj d06226a62b2f8645450616852b273b41655d0612; CI40208512135 úspešné vrátane publikácie a overenia vzdialených bajtov. Verejný prerelease v13.40-r41 a candidate.json overené: veľkosť aj SHA zodpovedajú lokálnemu testovanému balíku. Feed commit6f1577c80679fbbfc1b6ee72c253d9f8a1541b76. Na prijímači nový vzhľad a ikona zatiaľ čakajú na posúdenie.

### r41 reálna obrazovka a požiadavka na živé TV

Snímka1(20261025-155109).jpg potvrdzuje hlavné menu r41: všetkých11 položiek, názov/popis Informácií o systéme vpravo, slovenský dátum, čas so sekundami a verziu. Samotná snímka nedokazuje pohyb, plynutie sekúnd ani ikonu v prehliadači pluginov. Používateľ potom výslovne žiada grafiku ako v našom skine s liveTV vpravo hore; potvrdil názov/popis pod videom.

r42 pridáva iba natívny Pig source=session.VideoPicture,16:9 viewport a presun existujúceho názvu/popisu podň. Bez volania playService/stopService, bez vlastného PiP a bez ďalšieho tunera. Skúška: aktualizovať cez GSU na r42, otvoriť hlavné menu na TV stanici, overiť obraz/zvuk, šípkami meniaci sa názov a popis pod videom. Otvoriť bežnú sekciu a vrátiť sa; po zatvorení GSU sa musí obnoviť obraz na celú plochu. Neprepínať ani nereštartovať CAM na túto grafickú skúšku. r42 živé video a návrat celej plochy zatiaľ neoverené na prijímači.

r42 hostiteľské overenie:254 testov Python3.14.7, kompilácia a dva zhodné buildy úspešné. IPK3467340B, SHA25699442409d2da1286deb76cefcb9aac3048ec52b9aa6211cd56479c7b434f5ba4. Zdroj0702263a78e21ce420fcfc90a5f23ea277f5498e; CI40209272337 úspešné vrátane publikácie a overenia vzdialených bajtov. Verejný prereleasev13.40-r42 a aktualizačný feed overené: veľkosť aj SHA zhodné s lokálnym balíkom. Feedcommit4b19601ab49ebca283fbab8f7353e1b73ffd1faa. Na prijímači živé video a jeho obnovenie zatiaľ čakajú na skúšku.

r43 hostiteľské overenie:256 testov Python3.14.7 úspešných po odstránení purpose riadka, kompilácia a dva zhodné buildy. IPK3467474B, SHA2561a94d8d3871671c77377cbecb220cdddae137a628ea14951cd8c610a485d6f57. Publikácia/CI zatiaľ čakajú.

### r44

Používateľ výslovne schválil kratší názov GSU Warder Evolution. r44 mení spoločnú konštantu názvu; najbližšie overiť názov v prehliadači pluginov. r43 bol publikovaný cez CI40210792043; feed aj SHA zhodné s lokálnym testovaným balíkom.

### r45 ďalšia sekcia

Snímka1(20261025-162230).jpg potvrdzuje r44 hlavné menu, väčšie panely bez nadpisu/spodného riadka, liveTV a4 farebné tlačidlá. Používateľ žiada pokračovať. r45 upravuje Informácie o systéme do spoločného rámu/hlavičky, zachováva všetky pôvodné komponenty a zber dát. Najbližšie: aktualizovať, otvoriť Informácie o systéme a poslať snímku; overiť ľavé údaje, dva pravé výpisy a šípky, návrat červeným. Celý CAM/swap znovu netestovať.

### r46 oprava vrstiev

Snímka1(20261025-163228).jpg ukazuje chýbajúce ľavé popisky a oba pravé výpisy v r45. OpenATV ScrollLabel.py smeruje zPosition na vnútorné labely, parent eWidget zostáva0; nové pozadie0 ho preto prekrývalo. r46 má backdrop-3, rám-2 a panel-1. Texty ostávajú transparentné nad nepriehľadným panelom, takže sa neprekrývajú pôvodné presahujúce rozsahy. Pôvodné PNG majú alpha204–255; zapnutý blend namiesto off ich zjemní, čierny obsah tým nie je úplne odstránený. Overiť na prijímači pred pokračovaním inej sekcie.

### r47 ikonky

Používateľ potvrdil zobrazené popisky a oba výpisy aj šípky všetkými smermi v r46, snímka1(20261025-164108).jpg. Funkčnú opravu neopakovať. Výslovne žiada nové ikonky bez čiernych podkladov. r47 nahrádza15 symbolov transparentnými PNG z vlastných SVG predlôh, zachováva význam aj natívne ovládanie. Najbližšie overiť vizuálny výsledok Informácií o systéme po aktualizácii.

### r48 grafika hardvéru

Používateľ výslovne odmietol schematické hardvérové ikony r47, ale schválil a požaduje ponechať šípky. Chce farebné plastické a jasne rozpoznateľné predmety podobné pôvodným, bez čiernych podkladov/odrazov. r48 nahrádza11 hardvérových symbolov; šípky a stavové bodky sú bajtovo zachované. Zber údajov ani rozloženie sa nemení. Najbližšie: posúdiť reálne ikonky v Informáciách o systéme po aktualizácii, funkčnú skúšku šípok z r46 bez dôvodu neopakovať.

### r49 zmena požiadavky na šípky

Po publikácii r48 používateľ výslovne požiadal zmeniť aj šípky, aby mali spoločný dizajn. Predchádzajúca požiadavka zachovať ich grafiku je tým prekonaná. r49 nahrádza iba grafiku oboch smerových šípok, ponecháva význam, klávesové väzby a stavové bodky. Najbližšie posúdiť hardvérové ikonky aj šípky spolu v prijímači; ovládanie už bolo potvrdené v r46.
