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
