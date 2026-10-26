# Aktuálny stav — GSU Warder Evolution

Aktualizované 26. 10. 2026. **Ostrá prevádzka je spustená od 13.40-r87.** Používateľ po r86 potvrdil dokončenie a výslovne autorizoval stabilné vydanie aj úplný zápis dokumentácie. Aktuálny runtime a rozloženie r86 sa v r87 nemenili; zmenili sa iba verzia, vydávacie metadáta, poznámky a dokumentácia.

## Repozitár a autoritatívne súbory

- Repozitár: Evolution-by-Warder/GSU-Warder-Evolution.
- Jediné aktívne jadro: `plugin/src/GlassSysUtil`.
- `original-python314` je vydávacia vetva, `main` zrkadlí aktuálny projekt a finálne feedy. Historická `warder-master-production` sa nemení.
- Inštalačná identita `enigma2-plugin-glasssysutil`, adresár `Plugins/Extensions/GlassSysUtil`; zobrazovaný názov GSU Warder Evolution.
- Pred zápisom načítať aktuálny SHA. Bez force push/rebase, zápis fast-forward s expected_sha. Neposúvať vydávaciu vetvu počas publishera.
- Potrebné resources, inventáre, pôvodné skiny, konvertory a defaults sú súčasťou overovania a balenia. Nové runtime Python/PNG/locale súbory sa balia z aktuálneho jadra. Výrobné masters sa neinštalujú.

## Stabilné vydanie a dôkazy

- Verzia: **13.40-r87**, verejné GitHub **Latest**, `prerelease=false`, `draft=false`, release ID424266966.
- Zdroj vydania: `45aaa86780ed6b7be707f02e9a78684226f555ed`.
- CI:40328378779, success; **361 testov** na Python3.14.7, compileall, dva identické buildy a kontrola skutočne publikovaného IPK.
- IPK:3 680 642 bajtov.
- SHA256: `a981085699f22bb4b9fb97ddc6a2d3af4b452920fa8fe51c962ce16f70c73d6b`.
- Oba feedy overené na r87 s rovnakou verziou/hashom/veľkosťou.
- Cleanup40328562919 odstránil nahradené r86; API potvrdilo iba r87. Spolu63 starých vydaní odstránených podľa explicitných plánov, Git tagy a história zachované. Spotrebovaný request odstránený.
- Podrobný strojový záznam a aktuálne zdrojové kontrolné súčty: `validation.json`.

## Rozsah schválenia

Používateľský priechod a aktuálne rozhranie sú schválené na GigaBlue Quad 4K Pro / OpenATV 8. Dnešný zoznam je uzavretý; ďalšie zmeny iba na novú požiadavku. Neotvárať znova schválené obrazovky ani opakovať celý priechod.

`receiver_tested=false` v strojovom zázname znamená neúplné pokrytie všetkých zariadení, image a nedostupných CCcam/Mbox/samostatných SRV služieb. Neznamená zlyhanie používateľského priechodu. Hostiteľské API doubles nepotvrdzujú natívne kreslenie, výkon ani hardvér.

## Schválená grafika a navigácia

- Spoločný banner s dátumom, živým časom a sekundami; verzia v dvoch riadkoch, údaje zarovnané.
- Hlavné menu:11 stabilných ID vľavo, LiveTV vpravo, modré O plugine. Nepotrebné nadpisy/účelový spodný riadok odstránené. Návrat obnoví plnú TV.
- Pravý workspace pre ECM, swap, nástroje, O plugine, ručnú aktualizáciu a OSD nastavenia. Funkčné kontroléry zostávajú; nevytvárať nové kópie backendu.
- Jemná priehľadnosť panelov, jednotný nepriehľadný modrý výber, krátke farebné čiary a centrované popisky tlačidiel.
- Systém/kanál: zachované merania a komponenty, farebné plastické RGBA ikony bez čiernych dlaždíc, ikonky nad údajmi a metre zarovnané. Systémové skupiny posunuté doprava; posuvníky majú nepriehľadné farby. Riadok Družica je nižšie a hodnota v zákryte s transpondérom; pozícia aplikovaná aj natívne.
- Systémová Nápoveda nahradí obsah celého veľkého okna a návrat obnoví pôvodné widgety aj posuv. Nastavenia používajú veľký spoločný rám.
- Clipped HeaderArtwork škáluje plnú bitmapu vo vlastnom rodičovi. Nezamieňať za loadImage so zdanlivým resize PNG.
- ScrollLabel natívny rodič má z=0; veľké panelové výplne musia byť pod ním. Opravené neviditeľné texty O plugine / Aktualizácia. Zachovať správne vrstvenie.

## ECM a OSD

- Dva zámerné vstupy: hlavné GSU zobrazí ECM v pravom paneli; dlhé modré → (GSU) Informácie ECM otvorí samostatné malé okno nad plnou TV. Tento priamy vstup používateľ výslovne žiada zachovať.
- Obe ECM zobrazenia majú názov aktuálnej stanice nad piconom stanice a kódovania. Názov je z natívnej služby Enigmy, picon z existujúceho resPicon s prvými10 poľami referencie. Nezmenená referencia znovu nečíta picon; názov sa obnovuje aj pri cache.
- Externé okno je jemne širšie; jeho CAM sa zobrazuje bez @buildhash. Iba externé hodnoty majú noWrap, aby sa pri dlhom CAM nerozladili riadky. Interné ECM ponecháva celý schválený CAM.
- Iba interný názov stanice: x1160/y672/w680/h40 FHD, picony y760. r85 XML posun sa na snímke neprejavil; r86 preto pri InlineECM.show explicitne aplikuje native move/resize. Používateľ následne potvrdil hotovo a ostrú prevádzku. Externý názov sa neposúva.
- OSD výbery sú v spodnej polovici pravého panela. Zelené uloží konfiguráciu; vstupné editory menia iba rozpracovanú hodnotu. EXIT zruší editor. Nastaviť polohu je zámerne samostatný polohovací nástroj.
- Nápoveda Stlač OK pre úpravu je y562 FHD; pri spodnom editore je skrytá a po návrate sa obnoví. Statické a pohyblivé OSD majú oddelené súradnice; explicitná uložená poloha sa nemigruje na nový default násilne.

## OSCam a CAM

- OSCam: trvalé menu vpravo, informácie/detail vľavo; automatický fokus detailu a prechod panelov šípkami, zachovanie výberu pri refreshi.
- Povoľovanie lokálneho DVBAPI používa len na oprávnenom loopback vybranom OSCame obnovu cez riadený reštart. Text potvrdenia upozorňuje na krátke čakanie. Používateľ overil odstránenie anonymous duplicitného stavu po povolení.
- Správca CAM: výber CAM, sťahovanie, odstraňovanie, OSCam štart konfigurácia a oneskorenie v ľavom paneli; pravé akcie zostávajú. Nepotrebné modré Presunúť výber odstránené.
- NativeSoftcam kontroluje identitu procesov a skutočný výsledok štartu/zastavenia/prepnutia, nie iba chybné exit kódy starých init skriptov. Zombie sa nepovažuje za bežiaci CAM.
- Autostart10s, voliteľná kontrola15s, vzájomný zámok, rešpektovanie manuálneho zastavenia, backoff a synchronizácia uloženého nastavenia. Používateľ tieto postupy overil.
- Starý nedôveryhodný FTP nepoužívať. Balíky CAM idú cez systémový feed s detekciou architektúry/image; ručne vložená binárka nemusí patriť žiadnemu opkg balíku. Nepoužívané SRV zostáva skryté.

## Aktualizácie a vydávanie

- Automatická kontrola pri každom otvorení aj ručná položka Aktualizácia. Sieť/inštalácia mimo GUI; veľkosť, SHA256 a obsah IPK sa overujú pred opkg.
- Automatická ponuka používa veľký spoločný presvitný rám. Ručná kontrola využíva pravý panel. Červené Nie / zelené Áno sú lokalizované; biele duplicitné voľby odstránené. Pri automatickej ponuke OK/EXIT odmietne. Bez novej verzie alebo pri chybe Naspäť.
- Úspešná inštalácia zobrazí len hlásenie o aktualizovaní a reštarte GUI o3 sekundy, potom quitMainloop(3). Inštalačné overenia zostávajú.
- Stabilný publisher od r87 vytvára Latest bez prerelease; existujúce bajty sú nemenné. Povolený retry alebo povýšenie existujúceho prerelease až po overení stiahnutého súboru. Draft sa odmieta.
- `plugin/update/candidate.json` je aktuálny feed; `restoration/update/candidate.json` zachováva starý presne validovaný download URL pre staré inštalácie. Názvy candidate/original-python314 sú technická kompatibilita. Oba musia mať rovnakú verziu/hash/veľkosť. Nikdy neodstrániť starú URL bez migrácie.

## Lokalizácia a balenie

Desať JSON katalógov (en/sk/cs/de/pl/hu/ru/fr/it/es),141 spoločných kľúčov a pôvodný cs/sk gettext fallback. Regionálna normalizácia a cache; par62=False znamená angličtinu. Bez globálnej zmeny locale a bez závislosti python3-gettext. Anglický fallback pre nepreložené historické dialógy, nie tvrdenie úplného prekladu. Dni/mesiace vo všetkých10 jazykoch; všetky jazykové šírky fyzicky neoverené.

## Dokumentácia a pokračovanie

README a CHANGELOG opisujú stabilný stav; `docs/POUZIVANIE.md` ovládanie a `docs/VYDAVANIE.md` overenie/publikáciu. Staré podrobné vývojové zápisy sú v Git histórii a nie sú aktívnymi pokynmi.

GSU je týmto uzavreté. Nová samostatná úloha používateľa: v repozitári **FullHDGlass-Warder-Evolution** upraviť obrazovky bez LiveTV na rovnakú jemnú priehľadnosť ako GSU; nemení to tento plugin.
