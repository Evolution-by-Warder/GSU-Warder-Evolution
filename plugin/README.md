# GSU Warder Evolution — plugin

Jediné aktívne jadro je `src/GlassSysUtil/`. Balík sa inštaluje ako `enigma2-plugin-glasssysutil` do `/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/`; identita a konfigurácia zostávajú kompatibilné s existujúcimi inštaláciami.

Z koreňa repozitára:

```sh
python3 -m unittest discover -s plugin/tests -q
python3 plugin/tools/build_ipk.py
```

`resources.tar.gz` a `resources.json` obsahujú potrebné pôvodné runtime súbory a ich kontrolné súčty. `skins-original.json` a `original-inventory.json` slúžia regresným testom. `converters/` a `defaults/` sa pribalia do IPK. Grafické výrobné podklady v `artwork/` sa do IPK nepribaľujú.

Aktuálny stav a ďalšie požiadavky sú v [TESTOVANIE.md](TESTOVANIE.md), zmeny vydanej verzie v [update/RELEASE-NOTES.md](update/RELEASE-NOTES.md). Celý plugin nie je označený ako plne overený na všetkom hardvéri. Používateľom prejdené funkcie a aktuálne rozhranie sú schválené pre ostrú prevádzku od 13.40-r87. Obmedzenia neoverených hardvérových a nepoužívaných služieb zostávajú uvedené v checkpointe.
