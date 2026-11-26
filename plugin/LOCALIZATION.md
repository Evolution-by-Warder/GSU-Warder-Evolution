# Jazyková podpora

Jazyk sa preberá z config.osd.language bez zmeny globálneho locale Enigmy. Podporované kódy: en, sk, cs, de, pl, hu, ru, fr, it, es, al, el, et, fa, lt, nl, pt, ro, tr, uk, zh (pracovný kandidát r5; stabilná r4 bez zmeny). Regionálne kódy a zápis s pomlčkou sa normalizujú; nepodporovaný jazyk a chýbajúci preklad používajú anglický zdrojový text. Prepínač lokalizácie GSU zostáva rešpektovaný.

Udržiavané katalógy sú UTF-8 JSON súbory v src/GlassSysUtil/locale/. Obsahujú 174 spoločných kľúčov a samostatný doplnok 110 historických textov pre hlavné ponuky, bežné ovládanie, systémové a kanálové popisky, aktualizácie, informácie o projekte a základné správy diagnostiky/swapu. Slovenský katalóg navyše zachováva existujúce fallback texty. Pôvodné cs/sk gsu.mo v runtime resources zostávajú druhou vrstvou prekladu. Texty, ktoré nemajú preklad ani v jednej vrstve, sú anglické; všetky historické dialógy nie sú vo všetkých jazykoch úplne preložené.

Katalógy sa cachujú podľa jazyka a cesty. Preklady sa nečítajú z disku pri každom prekreslení. Nepribúda závislosť python3-gettext ani grafické/nástrojové balíky na prijímači. Značka GSU Warder Evolution, názvy služieb, adresy, PIDy a namerané údaje sa neprekladajú. Popisky sú oddelené od živých hodnôt.

Pri dopĺňaní zachovať všetky %s/%d argumenty, nové riadky a technické identifikátory. Testy kontrolujú 21 katalógov, základné pokrytie, argumenty formátu, výber a vypnutie jazyka, gettext fallback, cache, balenie do IPK a zachovanie zdrojov/komponentov obrazovky.

Dni a mesiace hlavičky sú definované pre všetkých 21 jazykov. Používateľ schválil aktuálne slovenské rozloženie na prijímači. Vizuálna šírka všetkých textov vo všetkých ďalších jazykoch nie je týmto potvrdená.
