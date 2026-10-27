# Zostavenie a vydávanie

Aktuálna stabilná verzia: **13.40-r88**, základ runtime r86 s opravou natívneho callbacku informácií o kanáli v r88. Jediné aktívne jadro je `plugin/src/GlassSysUtil`. Inštalačný balík `enigma2-plugin-glasssysutil`, architektúra `all`; runtime adresár `Plugins/Extensions/GlassSysUtil` sa nemení.

## Overenie

CI používa Python 3.14.7. Pred publikáciou prebehnú jednotkové kontroly, compileall a dva bajtovo zhodné buildy. Výrobný IPK vzniká v `plugin/dist/`; grafické masters a dokumentácia nie sú jeho súčasťou. Potrebné pôvodné runtime súbory a obrázky sú zabalené z overených zdrojov. Nepridáva sa python3-gettext.

```sh
python3 -m unittest discover -s plugin/tests -q
python3 -m compileall -q plugin/src
python3 plugin/tools/build_ipk.py
```

## Publikácia

Zápis do vetvy `original-python314` s platnou zhodou `version`, `update/release-request` a prvého riadka RELEASE-NOTES spustí overený publisher. GitHub vydanie je stabilné a Latest. Existujúce vydanie sa nesmie prepisovať odlišným IPK; pri opakovaní sa najprv stiahne a porovná s buildom. Vydanie musí byť verejné. Konverzia existujúceho prerelease na stabilné je povolená až po overení bajtov.

Po overení publisher aktivuje oba feedy:

- `plugin/update/candidate.json`: aktuálny krátky názov repozitára.
- `restoration/update/candidate.json`: stará download URL potrebná pre staršie inštalácie; GitHub ju presmeruje.

Názov `candidate.json` a identifikátor `original-python314` sú kompatibilné technické identifikátory, nie označenie predbežného vydania. Oba feedy musia mať zhodnú verziu, hash a veľkosť. Neodstraňovať starú URL a nemeníť schému bez migračného postupu.

`main` zrkadlí aktuálny zdroj, dokumentáciu a finálne feedy. Pred zápisom načítať aktuálny SHA; použiť fast-forward s expected_sha, bez force push a rebase. Neposúvať vydávaciu vetvu počas publishera, aby jeho feed commit nenarazil na súbežný zápis.

## Stav podpory a schválenie

Používateľ schválil prejdené funkcie a UI na GigaBlue Quad 4K Pro / OpenATV 8 dňa 26. 10. 2026. Hostiteľské testy nie sú náhradou za fyzický prijímač. Žiadne tvrdenie o úplnom overení všetkých image/modelov alebo nedostupných CCcam/Mbox/SRV služieb. Podrobnosti sú v `plugin/TESTOVANIE.md` a `plugin/validation.json`.

Zoznam Releases obsahuje aktuálny podporovaný balík. Staré release assets sa odstraňujú iba explicitným ID/tag plánom po overení chráneného vydania a oboch feedov. Git tagy ani história sa nemažú.
