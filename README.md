# GSU Warder Evolution

Plugin pre Enigma2: informácie o prijímači a kanáli, ECM a OSCam, správa CAM, swap a diagnostika v spoločnom vzhľade Warder Evolution.

**r92 prináša tichú prevádzku: bez automatických gsu.log, autostart a bitrate logov; df/dmesg sa spracúva v pamäti. Zachováva schválené rozhranie a funkcie r90.**

**Stabilné vydanie: 13.40-r92. Produkčné povýšenie cleanup kandidáta schválil vlastník 29. októbra 2026.** Rozhranie a prejdené funkcie schválil používateľ na GigaBlue Quad 4K Pro s OpenATV 8. Vydanie je verejné **Latest**, bez označenia prerelease.

[Stiahnuť aktuálne vydanie](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/releases/latest) · [Používanie](docs/POUZIVANIE.md) · [Zmeny](CHANGELOG.md) · [Overenie a údržba](plugin/TESTOVANIE.md)

## Čo plugin ponúka

- Informácie o systéme a kanáli vrátane signálu, dátového toku a piconov.
- OSCam informácie v dvoch paneloch, prehľad serverov, klientov a čítačiek podľa dostupných služieb.
- ECM v pravom paneli alebo malom samostatnom okne cez dlhé modré: názov stanice, picon stanice a kódovania.
- Správu CAM s natívnym štartom, zastavením a prepínaním; voliteľný štart a kontrolu behu na pozadí.
- Nastavenia OSD ECM, správu swapu a diagnostické nástroje.
- Automatickú kontrolu novej verzie pri otvorení aj ručnú kontrolu. Po úspešnej aktualizácii sa GUI reštartuje o tri sekundy.

## Inštalácia a aktualizácia

Z vydania stiahnite súbor `enigma2-plugin-glasssysutil_13.40-r90_all.ipk` a nainštalujte ho cez správcu lokálnych balíkov prijímača. Existujúce inštalácie použijú aktualizátor priamo v GSU. Inštalačná identita a adresár `Plugins/Extensions/GlassSysUtil` sa nemenia, aby zostali zachované nastavenia a existujúce vstupy do pluginu.

Aktualizátor overuje veľkosť, SHA256 a obsah balíka pred inštaláciou. Automatická aj ručná ponuka používa preložené potvrdenie **Nie / Áno**. Bez novej verzie alebo pri chybe zostáva **Naspäť**.

## Jazyky a kompatibilita

Rozhranie sleduje jazyk prijímača: slovenčina, čeština, angličtina, nemčina, poľština, maďarčina, ruština, francúzština, taliančina a španielčina. Chýbajúce historické preklady používajú anglický text. [Rozsah lokalizácie](plugin/LOCALIZATION.md).

Vývojové kontroly používajú Python 3.14.7; používateľské overenie prebehlo na OpenATV 8. Nie je tým potvrdená funkčnosť na každom modeli a image ani nepoužívané CCcam/Mbox/samostatné SRV služby.

## Vývoj

Jediné aktívne jadro je v [`plugin/`](plugin/). `main` obsahuje aktuálny projekt, `original-python314` je vydávacia vetva. Jej názov a interný identifikátor feedu zostávajú kvôli kompatibilite; vydania sú stabilné.

```sh
python3 -m unittest discover -s plugin/tests -q
python3 plugin/tools/build_ipk.py
```

CI spúšťa testy, porovná dva buildy a overí skutočné bajty vydaného IPK pred aktiváciou oboch aktualizačných zdrojov. [Postup vydávania](docs/VYDAVANIE.md).

## Autorstvo

Projekt vychádza z Glass System Utility 13.20. Pôvodné autorstvo a potrebné pôvodné zdroje zostávajú zachované; Warder Evolution označuje pokračovanie, údržbu a úpravy. Výrobné grafické podklady sú v `plugin/artwork/` a do prijímača sa neinštalujú.
