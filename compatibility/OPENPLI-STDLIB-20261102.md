# GSU 13.41-r2 — OpenPLi minimal Python TEST

Oprava chyby `ModuleNotFoundError: No module named 'dataclasses'`. PiconHub pri konfigurácii a GSU pri štarte aktualizácií používali tento modul iba pre nemenný záznam údajov o vydaní. Záznam teraz používa `collections.namedtuple` z jadra Pythonu. Zachovaná je nemennosť polí, nezávislý slovník poznámok pre každé vydanie aj všetky kontroly verzie, URL, SHA256 a stavu nainštalovaného balíka.

Nová regresia úmyselne zablokuje import `dataclasses` a preverí štart aktualizátora aj jeho záznamy. Publikovanie navyše skúša konečný IPK: skutočný zabalený poinštalačný overovač a štart aktualizátora musia prejsť s blokovaným `dataclasses`. Nepreskakujú sa žiadne inštalačné kontroly a nepoužíva sa vynútená inštalácia.

PiconHub má 228 testov, GSU 413 testov. Matice kontrolujú Python 3.9/3.14, OpenPLi release-9.2/develop a OpenATV 8.0/8.0-next/master. História zachováva predchádzajúci verejný balík; zdroj jej metadát je overený kontrolným súčtom predchádzajúceho IPK.

Toto je samostatný TEST. Produkčné aktualizácie sa nemenia. PiconHub sa inštaluje ako 0.1.39-test3; GSU používa 13.41-r2 vo vydaní označenom TEST, aby sa zachovalo natívne poradie verzií opkg. Najbližšie ostré verzie musia byť aspoň PiconHub 0.1.40 a GSU 13.41-r3.

FullHDGlass 1.0.62-test4 podľa používateľovho výpisu dokončil vlastnú inštaláciu úspešne. Hlásenie `skin_user-hdg17.xml-opkg` znamená zachovanie používateľského nastavenia. Chyba nasledovala až pri opätovnej konfigurácii staršieho nedokončeného PiconHubu. FullHDGlass pri tejto oprave nepotrebuje ďalší balík.
