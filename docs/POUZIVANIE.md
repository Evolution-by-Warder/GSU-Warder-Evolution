# Používanie GSU Warder Evolution

GSU otvorte zo zoznamu pluginov. Pri zatvorení hlavnej ponuky sa obnoví plný TV obraz. Dostupnosť informačných položiek závisí od služieb na prijímači.

## Hlavná ponuka 0.41.5

Šípkami vyberte jedno zo siedmich centier. Otvorte ho tlačidlom OK. Červené alebo EXIT vás vráti o úroveň vyššie. Žlté v hlavnej ponuke otvorí nastavenia a modré informácie o plugine. V ďalších oknách sledujte farebné popisky na obrazovke.

| Centrum | Čo v ňom nájdete |
|---|---|
| Systém | Šesť kariet zobrazuje procesor, RAM, swap, flash, dostupné externé úložisko a teplotu. Skóre vychádza z dostupnej RAM a miesta vo flash. Vedľa neho vidíte počet vyhodnotených kontrol. Procesy a systémový log majú samostatné obrazovky. |
| Príjem | Rýchle meranie nad televíznym obrazom, živý graf, informácie o kanáli, bitrate, služby transpondéra a prehľad tunerov. V zozname tunerov modrým tlačidlom prezriete aj ďalší tuner bez preladenia. |
| Pamäť a úložisko | Voľná pamäť, disky, správa swapu a miesto spotrebované piconmi, skinmi, pluginmi, EPG, cache a logmi. Čiastočný výsledok znamená, že prehliadka dosiahla časový alebo početný limit. |
| Sieť | Rozhrania, rýchlosť linky, brána, DNS a meranie siete. Kontrola dostupnosti skúša zvlášť bránu, oficiálny web a aktualizačný feed. História obsahuje posledných osem ručne spustených testov v otvorenom okne. |
| CAM / ECM | Informácie o ECM, klienti a čítačky podľa dostupnej služby, správa CAM/SRV a nastavenia OSD. |
| Servis | Integrita súborov, stav závislostí, stručná analýza crashlogov a kontrola metadát miestnych IPK v adresári /tmp. V položke Report pre fórum si môžete prezrieť a potom uložiť anonymný JSON. Podrobný miestny diagnostický balík v Nástrojoch obsahuje aj systémové údaje a logy. |
| Warder Evolution | Vyberte jeden z piatich projektov. Stránka zobrazí nainštalovanú verziu, oficiálne dostupné vydanie a jeho poznámky. Modré tlačidlo otvorí nainštalovaný projekt alebo aktualizátor GSU. |

Na grafe šípky prepínajú veličinu. Zelené pozastaví meranie, žlté prepína interval 1, 2 alebo 5 sekúnd. Graf drží poslednú minútu. Teplotu odčíta najviac raz za päť sekúnd, údaj Δt ukazuje jej vek. Pri signáli modré uloží namerané hodnoty do nového CSV v /tmp. Pomlčka znamená, že ovládač neposkytol meranie. Voliteľný zvuk rýchleho merača vyžaduje dostupný miestny prehrávač.

### Ladenie a obnova staníc

V prehľade transpondéra zelené uloží aktuálne známe TV služby a modré rozhlasové služby do nového súboru v /tmp. Novonájdené stanice pri aktívnom ladení zobrazuje natívna obrazovka skenovania danej image. GSU ponúkne SatFinder, motor či blindscan podľa vybavenia prijímača. Pri nahrávaní, timeshifte alebo blízkom plánovanom nahrávaní je vstup do aktívneho nastavenia zablokovaný.

Pred aktívnym ladením si poznačte zobrazený adresár overenej zálohy. Obsahuje pôvodnú databázu staníc a bouquety. Na miestnom disku bez podpory súkromných oprávnení alebo bez dostupného miestneho disku sa použije /tmp. Ak má záloha prežiť reštart prijímača, skopírujte ju z /tmp na vlastné úložisko. Pri obnove zastavte GUI Enigma2, porovnajte SHA-256 uložených súborov so SHA256.json a vráťte príslušné súbory do pôvodného konfiguračného adresára Enigma2. Potom znova spustite GUI.

## Dva vstupy do ECM

V hlavnom GSU vyberte Informácie ECM pre pravý panel. Na rýchlu kontrolu nad plnou TV použite dlhé modré a položku **(GSU) Informácie ECM** v rozšíreniach. Samostatné okno je zámerne zachované.

Obe zobrazenia ukazujú názov aktuálnej stanice a picon stanice vedľa kódovania. Názov stanice sa získava z Enigmy, nie zo súboru ECM. Dlhý text CAM sa v samostatnom okne nezalamuje a nezobrazuje identifikátor za @.

Nastavenia Informácie ECM na obrazovke používajú výber v spodnej časti pravého panela. Zmenu hodnoty potvrdí OK; zelené Uložiť uloží nastavenia. Nastaviť polohu otvára polohovací nástroj. Vlastná uložená poloha sa zachováva.

## Aktualizácia

Kontrola prebehne pri každom otvorení GSU; ručne ju spustí položka Aktualizácia. Červené **Nie** odmietne novú verziu, zelené **Áno** potvrdí inštaláciu. Pri automatickej ponuke OK / EXIT neinštaluje. Bez novej verzie alebo pri chybe sa zobrazuje Naspäť.

Sieťová a inštalačná práca beží mimo GUI. Balík sa overí pred spustením opkg. Po úspechu zostane iba hlásenie o aktualizovaní a GUI sa o tri sekundy reštartuje. Ak je nainštalovaná staršia verzia, jej vlastná ponuka môže mať ešte starší vzhľad až do dokončenia aktualizácie.

## CAM

Štart, zastavenie a prepnutie využívajú natívne CAM skripty a overujú skutočný proces. Automatický štart a kontrola behu sú voliteľné; ručné zastavenie cez správcu sa rešpektuje. Ponuky sťahovania, odstránenia, výberu CAM, OSCam štart konfigurácie a oneskorenia sa zobrazujú v ľavom paneli správcu. Operácie dostupné len pre nepoužívané služby nemusia byť aktívne.
