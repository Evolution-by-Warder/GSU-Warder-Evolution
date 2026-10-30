# Overené zaradenie Warder pluginov

| Produkt | Skupina pri odstránení | Zobrazená položka |
| --- | --- | --- |
| GSU 13.40-r94 | Balíčky s rozšíreniami | gsu-warder-evolution |
| PiconHub 0.1.32 | Balíčky s rozšíreniami | piconhub-warder-evolution |
| FullHDGlass 1.0.41 | Balíčky vzhľadu | fullhdglass-warder-evolution |

Zaradenie bolo overené spustením skutočnej funkcie getPackageInfo z upstream OpenATV. Nový GSU prešiel 375 testami, skutočnou offline výmenou a odstránením cez opkg, spätnou obnovou a spustením reálneho prerm v chroot. Oba verejné IPK majú overenú veľkosť a SHA256. Nové fyzické potvrdenie prechodu na prijímači sa netvrdí.

Aktualizácia existujúcej GSU prebieha cez vstavaný aktualizátor v dvoch krokoch: r93, reštart GUI, r94. Nastavenia a spravované štartovanie CAM-u zostávajú zachované; oba balíky sa overia pred odstránením starej identity a pri chybe je pripravená obnova. PiconHub aj skin už mali správne kategórie a dostali kratšie názvy súborov; verzie ani runtime sa nemenili. Podrobnosti sú v reports/plugin-groups-20261030.json a docs/PLUGIN-PACKAGE-GROUPS.json.
