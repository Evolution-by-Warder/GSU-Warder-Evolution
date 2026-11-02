# GSU 13.41-r4

Aktívne ostré vydanie pre OpenPLi a OpenATV.

Spoločná verzia pre OpenPLi a OpenATV. Opravený štart aktualizátora bez modulu dataclasses a pád ECM panela na OpenPLi; rovnaké volania sú opravené aj v informáciách o kanáli a klientoch OSCam. Zahrnuté sú úpravy zoznamov, rozlíšení HD/FHD/WQHD/UHD a kompatibility OpenATV 8.1/GLES. Nastavenia a spravované štartovanie CAM-u zostávajú zachované. Po aktualizácii reštartujte GUI.

[Stiahnuť IPK](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/releases/download/v13.41-r4/enigma2-plugin-extensions-gsu_13.41-r4_all.ipk)

SHA-256: `48d8f90a6f1665f28e777b615f4dd25b1b8afc0b85128685965d44b66134acb2`

Overené verejné bajty, dodané inštalačné kontroly a natívne rozhrania OpenPLi/OpenATV. Úplné fyzické testovanie všetkých modelov a rozlíšení sa netvrdí.

## Text pre web

**GSU 13.41-r4 – spoločné vydanie pre OpenPLi a OpenATV**

Aktualizácia GSU prináša súhrn opráv kompatibility systémovej utility s prostrediami OpenPLi a OpenATV. Zmeny sa týkajú predovšetkým štartu aktualizátora, zobrazovania informácií o dekódovaní a prispôsobenia používateľského rozhrania rôznym rozlíšeniam.

Hlavné zmeny:

- **Odstránená závislosť aktualizátora od modulu `dataclasses`**, ktorého neprítomnosť v niektorých obrazoch spôsobovala chybu pri konfigurácii balíka alebo spustení aktualizačnej časti.
- **Opravený pád ECM panela na OpenPLi**, spôsobený rozdielmi v dostupných metódach textových prvkov Enigma2.
- **Zjednotená obsluha textových prvkov** aj v informáciách o kanáli a zobrazení klientov OSCam.
- **Úpravy zoznamov a rozloženia obrazoviek** pre HD, Full HD, WQHD a UHD vrátane súvisiacich zmien pre OpenATV 8.1 a GLES.
- **Zachované overovanie inštalovaných súborov a integrity aktualizácií**, vrátane kontroly verzie a kontrolného súčtu sťahovaného IPK.

Existujúce nastavenia a spravované štartovanie CAM-u zostávajú zachované. Pre staršie inštalácie je naďalej dostupná potrebná prechodová aktualizácia; po jej inštalácii a reštarte GUI možno pokračovať na aktuálne vydanie.

Verzia **13.41-r4** je spoločná pre OpenPLi aj OpenATV a je zaradená do aktualizačného kanála GSU. **Po aktualizácii reštartujte GUI.**
