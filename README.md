# GSU Warder Evolution

Plugin pre Enigma2: informácie o prijímači a kanáli, ECM/OSCam, správa CAM, swap a diagnostika. Vychádza z pôvodného Glass System Utility 13.20 a pokračuje spoločným vzhľadom Warder Evolution.

## Aktuálny projekt

Jediný udržiavaný kód je v [`plugin/`](plugin/). Overovaná platforma je OpenATV 8 / Python 3.14.7; úplná funkčnosť na všetkých prijímačoch sa netvrdí. Aktuálna vydaná verzia je **13.40-r50**.

- [`plugin/src/GlassSysUtil/`](plugin/src/GlassSysUtil/): Python zdroje a grafika pre prijímač.
- [`plugin/tests/`](plugin/tests/): regresné testy.
- [`plugin/tools/`](plugin/tools/): zostavenie IPK, publikácia a príprava grafiky.
- [`plugin/artwork/`](plugin/artwork/): výrobné grafické podklady; neinštalujú sa do prijímača.
- [`plugin/update/`](plugin/update/): overený feed, poznámky k verzii a požiadavka na vydanie.
- [`plugin/TESTOVANIE.md`](plugin/TESTOVANIE.md): aktuálny stav a dohodnuté ďalšie úlohy.

## Zostavenie a aktualizácia

```sh
python3 -m unittest discover -s plugin/tests -q
python3 plugin/tools/build_ipk.py
```

Výsledok je v `plugin/dist/`. CI používa Python 3.14.7, spustí testy a porovná dva buildy. Vydania a aktualizačný feed publikuje pracovná vetva `original-python314` až po overení skutočných bajtov vydaného IPK. `main` obsahuje vyčistenú štruktúru projektu; iné historické vetvy nie sú zdrojom aktuálneho balíka.

Nainštalovaný plugin kontroluje novšiu verziu pri otvorení a ponúka aj ručnú kontrolu. Po úspešnej inštalácii oznámi reštart GUI o tri sekundy. Cesta `restoration/update/candidate.json` zostáva iba ako kompatibilný feed pre existujúce inštalácie; nejde o druhý plugin.

## Autorstvo

Pôvodné autorstvo Glass System Utility zostáva pôvodným autorom. Warder Evolution označuje pokračovanie, údržbu a úpravy. Potrebné pôvodné grafické a pomocné zdroje sú zachované s kontrolnými súčtami. Staré implementácie a dokumentácia zostávajú dostupné v Git histórii.
