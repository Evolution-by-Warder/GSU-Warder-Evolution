# Zmeny GSU Warder Evolution

## 13.40-r88 — 27. 10. 2026 — oprava pádu

- Informácie o kanáli: callback zarovnania družice je viazaná metóda, ktorú natívny OpenATV správne vykoná. Opravuje `TypeError: exec() arg 1 must be a string, bytes or code object` pri otvorení aj cez dlhé modré.
- Regresný test kontroluje natívny typ callbackov a súradnice v troch rozlíšeniach. Overenie na prijímači po tejto oprave ešte čaká.

## 13.40-r87 — 26. 10. 2026 — stabilné vydanie

- Spustenie ostrej prevádzky po schválení používateľom; zachovaný runtime a grafika r86.
- Stabilné verejné vydania GitHub Latest a kompatibilné aktualizácie existujúcich inštalácií.
- Spoločný banner, jemne priehľadné panely, živá TV a jednotné ovládanie.
- Systémové/kanálové informácie, panelový OSCam a správca CAM.
- ECM s názvom stanice a dvoma piconmi v internom aj samostatnom okne. Externý CAM bez identifikátora za @, hodnoty bez zalamovania; interný názov vyššie nad piconmi.
- Automatická a ručná aktualizácia v spoločnom vzhľade, preložené Nie / Áno, bez duplicitných bielych volieb. Úspešná inštalácia reštartuje GUI po troch sekundách.
- Nápoveda a nastavenia v spoločných oknách; O plugine a ručná kontrola v pravom paneli.
- Desať jazykových katalógov a zachované pôvodné preklady.

Predchádzajúce r37–r86 boli vývojové vydania a používateľské opravy. Ich zdroje a história zostávajú v Gite; zoznam Releases obsahuje aktuálny podporovaný balík.
