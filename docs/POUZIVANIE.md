# Používanie GSU Warder Evolution

GSU otvorte zo zoznamu pluginov. Pri zatvorení hlavnej ponuky sa obnoví plný TV obraz. Dostupnosť informačných položiek závisí od služieb na prijímači.

## Panely a ovládanie

Hlavná ponuka je vľavo a živá TV vpravo. ECM, swap, nástroje, O plugine a ručná aktualizácia využívajú pravý panel. OSCam a správca CAM majú vlastné dvojpanelové obrazovky. Šípky vľavo/vpravo menia aktívny panel tam, kde sú dostupné oba zoznamy; hore/dole ovládajú jeho obsah. OK otvorí vybranú položku. Rozhodujú aktuálne farebné popisky v spodnej lište.

Červené / EXIT sa vracia späť. Modré v hlavnej ponuke otvorí O plugine. V systémových informáciách zelená Nápoveda nahradí obsah veľkého okna; návrat obnoví údaje a rolovanie. Pravé procesy a systémový log majú vlastné posúvanie.

## Dva vstupy do ECM

V hlavnom GSU vyberte Informácie ECM pre pravý panel. Na rýchlu kontrolu nad plnou TV použite dlhé modré a položku **(GSU) Informácie ECM** v rozšíreniach. Samostatné okno je zámerne zachované.

Obe zobrazenia ukazujú názov aktuálnej stanice a picon stanice vedľa kódovania. Názov stanice sa získava z Enigmy, nie zo súboru ECM. Dlhý text CAM sa v samostatnom okne nezalamuje a nezobrazuje identifikátor za @.

Nastavenia Informácie ECM na obrazovke používajú výber v spodnej časti pravého panela. Zmenu hodnoty potvrdí OK; zelené Uložiť uloží nastavenia. Nastaviť polohu otvára polohovací nástroj. Vlastná uložená poloha sa zachováva.

## Aktualizácia

Kontrola prebehne pri každom otvorení GSU; ručne ju spustí položka Aktualizácia. Červené **Nie** odmietne novú verziu, zelené **Áno** potvrdí inštaláciu. Pri automatickej ponuke OK / EXIT neinštaluje. Bez novej verzie alebo pri chybe sa zobrazuje Naspäť.

Sieťová a inštalačná práca beží mimo GUI. Balík sa overí pred spustením opkg. Po úspechu zostane iba hlásenie o aktualizovaní a GUI sa o tri sekundy reštartuje. Ak je nainštalovaná staršia verzia, jej vlastná ponuka môže mať ešte starší vzhľad až do dokončenia aktualizácie.

## CAM

Štart, zastavenie a prepnutie využívajú natívne CAM skripty a overujú skutočný proces. Automatický štart a kontrola behu sú voliteľné; ručné zastavenie cez správcu sa rešpektuje. Ponuky sťahovania, odstránenia, výberu CAM, OSCam štart konfigurácie a oneskorenia sa zobrazujú v ľavom paneli správcu. Operácie dostupné len pre nepoužívané služby nemusia byť aktívne.
