# GSU Warder Evolution 0.41.5 — produktová a technická špecifikácia
26.11.2026 | Schválený smer vývoja, konsolidovaný návrh architektúry; nie hotová implementácia.

## 1. Cieľ a hranice
Vlastný moderný produkt, nie zbierka cudzích pluginov. Funkčná asimilácia užitočných vlastností, vlastná implementácia a grafika, bez duplicít. Pridaná hodnota oproti natívnym obrazovkám OpenATV/OpenPLi/OpenBH a ďalších image: história, súvislosti, merateľné diagnózy, odporúčania, jednotný ekosystém. Pred implementáciou porovnať konkrétne verzie referenčných a natívnych nástrojov; verejná dokumentácia nie je dôkaz kompletnej parity. Zachovať všetky existujúce funkcie a prístup k nim.

## 2. Informačná architektúra
Sedem hlavných položiek; pracovné slovenské názvy, lokalizovať do 21 jazykov.
- Systémové centrum: Prehľad / Živé monitorovanie / Procesy / Systémový log. Stav CPU, RAM, swap, flash, teploty a stručné odporúčania. Procesy a logy samostatné plnohodnotné obrazovky. Odkazy do úložiska a siete používajú tie isté detailné obrazovky.
- Centrum príjmu: Prehľad aktuálneho kanála / Signál a história / Transpondér / Tunery a nahrávanie / Anténa a motor / Ladenie a skenovanie / Obraz, zvuk a dátový tok. Zachovať existujúce informácie o kanáli a bitrate.
- Pamäť a úložisko: RAM a swap (existujúca správa swapu), root/flash, lokálne disky, kategórie obsadenia, picony, SMART iba ak podporované, odporúčania, detail procesov cez systémové centrum. Bez automatického mazania.
- Sieťové centrum: rozhrania, link speed, lokálne pripojenie, brána, DNS, internet, dostupnosť oficiálnych serverov, odozva/strata paketov, sieťové mounty, história testov. Časové limity, bez blokovania GUI.
- CAM / ECM centrum: všetky existujúce CCcam/OSCam/Mbox, ECM a OSD, CAM/SRV, čítačky, klienti, štartovanie a nastavenia; modernizovať zobrazenie, nie meniť fungovanie ani umožňovať neoprávnený prístup.
- Servisné centrum: integrita, crashlogy, IPK kontrola, existujúci diagnostický export (modernizovaný, nie duplicitný), odporúčania; benchmark, zálohy a aktívne opravy sú návrhy vyžadujúce bezpečnostné rozpracovanie a potvrdenie rozsahu tam, kde menia dáta alebo konfiguráciu.
- Warder Evolution centrum: FullHDGlass, PiconHub, Radio, YouTube, GSU; nainštalovaná verzia, overená dostupná verzia, kompatibilita, stav, poznámky, vstup do kanonického aktualizátora. Žiadne tiché preinštalovanie.
Nastavenia a O plugine na farebných tlačidlách hlavného menu. Existujúce položky presunúť až po inventúre ich identifikátorov, akcií a podmienok; žiadna funkcia nesmie zmiznúť.

## 3. Vizuálny systém a ovládanie
Modro-tyrkysová Warder identita, zachovať logo, hlavičku, PIG a živý čas/dátum tam, kde majú zmysel. Moderné sekčné karty a typografia čitateľná z pohovky, veľký aktívny fokus, dostatok priestoru, krátke názvy. Tri úrovne: okamžitý prehľad, detaily a história, expertné údaje. Jedna obrazovka = jeden účel. Farebné stavy doplniť textom; neznáme hodnoty nepovažovať za OK. OK otvorí detail, šípky vyberajú/posúvajú, červené späť, žlté obnoviť v diagnostike, modré kontextová akcia, zelené potvrdenie/výber; na hlavnom menu žlté nastavenia, modré O plugine. Zachovať existujúce akcie cez kontextové ponuky. Všetky rozlíšenia HD/FHD/WQHD/UHD, 21 jazykov vrátane dlhých textov a perzštiny; testovať fokus a pretekanie textu. Bez povinného GLES.

## 4. Funkčné požiadavky
Health: merané kontroly, transparentné skóre s pokrytím a neznámymi kontrolami, vysvetlenie a odporúčania; žiadne univerzálne teplotné limity bez podkladov pre konkrétny hardware. Korelácie neprezentovať ako dokázané príčiny.
Performance: CPU z rozdielov čítačov, RAM MemAvailable/fallback označený, swap, teplota zo skutočných senzorov, sieťové delta čítače; 60 s história, interval 1/2/5 s ako návrh, pauza, ukončenie merania pri zatvorení, bez zbytočného pozadia.
Storage: kategórie picony/pluginy/skiny/EPG/cache/logy, mount boundaries, hardlink dedup, symlink bezpečnosť, limit skenu, zobraziť neúplný výsledok; SMART iba dostupný read-only nástroj. Žiadny benchmark zápisu na flash bez osobitného bezpečného režimu.
Signal: skutočné SNR/AGC/BER/lock, dB iba natívne dostupné, min/max/priemer, výpadky, história, zvukový režim voliteľný; DVB-S/S2/S2X/T/T2/C/C2, MIS/PLS/T2-MI iba ak hardware/API podporuje. PIDs, kodeky, bitrate, rozlíšenie, HDR/HLG, HDMI údaje podľa dostupnosti. Tunery/FBC, obsadenosť a nahrávanie cez natívne API. Retune/blindscan/motor/DiSEqC/USALS/bouquet preview a zápis len cez podporované API a potvrdenie, ochrana playbacku a nahrávok. Žiadne obchádzanie podmieneného prístupu.
Service: overené hash manifesty, package manager detekcia, bezpečné čítanie IPK control metadata bez vykonávania skriptov, crashlog exception summary bez záruky diagnózy. Export allowlist údajov, náhľad, lokálny súbor, žiadne tokeny, heslá, CAM konfigurácie, raw logy, identifikátory či automatické uploady. Voliteľné upozornenia opt-in, rate limit.
Project centre: oficiálne stabilné manifesty, správna identita balíka, kontrola tagu/hash/veľkosti podľa kanonických updaterov, žiadne neoverené zdroje. Rozšírené cudzorodé katalógy, LCN, zásahy do systému a zálohy iba po preukázaní bezpečnosti a schválení konkrétnych mutácií.

## 5. Referenčný audit
E2 Doctor, Pulse Dashboard, MemOrganize, CiefpSatelliteAnalyzer, LinuxSat Panel, EvgQuickSignal, CiefpSignalInfo, SatFinder, SatScanner, PositionerSetup. Pre každý konkrétny feature zapísať zdroj/verziu, existujúce GSU pokrytie, stock image pokrytie, chýbajúcu hodnotu, implementáciu, test a hardware obmedzenie. Stav: inventár z verejnej dokumentácie, úplný audit zdrojov a runtime ešte otvorený. Žiadna kópia cudzej grafiky, kódu bez kompatibilnej licencie ani neoprávnených funkcií.

## 6. Technická architektúra
Reuse warder_main, warder_screen, warder_resolution, warder_system, warder_channel, bitrate_worker, warder_tools/warder_tools_ui, swap_ops/swap_ui, CAM/ECM moduly a plugin_update; presné rozhrania overiť pred zásahom. Navrhované nové vrstvy: capability registry; read-only providers; spoločný bounded sampler a history model; health rules; bezpečné report builder; shared view components; navigation registry. Jeden zdroj dát a detailnej obrazovky na oblasť. Len lazy-load pri otvorení, asynchrónne I/O s limitmi, žiadne nové povinné knižnice, cancellation/generation token na zatvorenie, žiadne UI volania z worker thread. Výkon zmerať na MIPS/MIPSEL aj ARM/AArch64; cieľ IPK < 7 MB (nie nameraná garancia).

## 7. Realizácia a akceptácia
A. Inventúra menu, akcií, API, zdrojov a stock image; feature matrix a regresný baseline.
B. Spoločné layout/navigation/capability/provider vrstvy; prehľad + procesy/logy; zachovať pôvodné funkcie.
C. Živé merania, storage, sieť, health rules, privacy report.
D. Signal Center, CAM/ECM modernizácia, Warder centrum; bezpečné natívne pokročilé akcie.
E. Lokalizácia všetkých nových reťazcov do 21 jazykov, kontrola placeholderov, fallback, rozlíšenia, fokus, výkon a lifecycle. Testy nedostupného hardware, výpadku siete, malého flash, nahrávania, uzatvorenia obrazovky, citlivých údajov, integrity IPK. Žiadne nepravdivé potvrdenie fyzických testov.
F. Oddelene dokončiť r6 PR #15 a overiť verejnú migráciu. Integrovať feature branch na aktuálny main po r6, OPKG epoch 1:0.41.5, public 0.41.5, staré feedy na r6 a zmrazené r93 bridge feedy nezmenené. CI exact HEAD, manuálny audit workflowov, deterministický IPK, verejné bajty/SHA/tag/feed. Web SK/EN/DE/RU, Pages, release notes a registre. Žiadny verejný TEST ani prázdna verzia.
Stav dokumentu: návrh na implementáciu, neobsahuje hotové obrazovky, merania ani potvrdenú funkčnú paritu.
