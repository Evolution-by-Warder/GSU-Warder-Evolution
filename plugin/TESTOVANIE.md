# Aktuálny checkpoint —25.10.2026, r49 publikované

Pracovať výhradne v original-python314, runtime plugin/src/GlassSysUtil. Bez force/rebase. Aktuálny kód je zjednotený v plugin/; main zobrazuje rovnakú vyčistenú štruktúru. Staré vetvy nie sú zdrojom zostavenia. GSU Warder Evolution je spoločný neprekladaný názov. Hlavná obrazovka má spoločný banner, živé hodiny,11 položiek, liveTV vpravo a popis pod ním,4 farebné akcie vrátane modrého O plugine. Nadpis Hlavná ponuka a spodný purpose riadok sú odstránené; panely využívajú miesto. LiveTV a návrat do normálu potvrdené používateľom.

Informácie o systéme: r45 zle prekrývalo pôvodné texty; r46 má pozadie/rám/panel vo vrstvách-3/-2/-1 a transparentné texty. Snímka1(20261025-164108).jpg potvrdzuje ľavé popisky aj pravé procesy/Dmesg a používateľ potvrdil všetky4 šípky. Funkčnú opravu neotvárať znova bez dôvodu.

Používateľ odmietol schematické hardvérové ikony r47, ale výslovne schválil ponechanie šípok. r48 mení11 hardvérových ikon na farebné plastické RAM/disky/USB/karty/CPU/teplomery/Linux, podobné pôvodným, so skutočne priehľadným okolím bez čiernych dlaždíc a odrazov. V r48 boli šípky a stavové bodky bajtovo nezmenené. Následne používateľ žiada zmeniť aj šípky, takže r49 má nové plastické strieborno-tyrkysové šípky; stavové bodky zostávajú nezmenené. Väčšie512px výrobné podklady a prompty sú v artwork/system-raster; do IPK idú iba pripravené120px PNG. Pôvodné odmietnuté hardvérové SVG sú odstránené, generátor ponecháva iba stavové bodky.

260 testov Python3.14.7 úspešných; dva zhodné buildy, CI40215979311 úspešné vrátane publikácie a overenia vzdialených bajtov. Zdroj a28e602a61b624ccec9970446d09843e6db65924. Feed overený: r49,3639402B,SHA25680432461c90e190acc7be3b345b1c304aff9ef3b41b89bd7476ab9ba233d72c4.

## Otvorené požiadavky — pokračovanie po r49 (25. 10. 2026)

1. Informácie o systéme: hardvérové ikonky mierne zväčšiť, iba ak sa zmestia bez prekrytia textov. Používateľ výslovne dovolil ponechať veľkosť, ak nie je dosť miesta. Existujúce farebné plastické PNG ponechať, negenerovať nové.
2. Spodné vertikálne bargrafy pri spodných ikonkách sú privysoko: zarovnať ich spodky so spodkami príslušných ikoniek. Presunúť spolu živý bargraf aj jeho podklad. Skontrolovať HD/FHD/UHD, zachovať pomery strán a funkcie. Úpravy patria do plugin/src/GlassSysUtil/warder_system.py a zmysluplných geometrických testov.
3. Referenčná snímka k bodom 1–2: 1(20261025-172724).jpg, pôvodná lokálna cesta /workspace/scratch/53fa7d0977c8/upload/1(20261025-172724).jpg. Snímka ešte nebola vyhodnotená pre výpadok prostredia; nezamieňať to za schválenie celej grafiky.
4. Následne zabudovať jazykovú podporu celého GSU podľa jazyka systému, vrátane dní a mesiacov v hlavičke. Dohodnutý rozsah: slovenčina, čeština, angličtina, nemčina, poľština, maďarčina, ruština, francúzština, taliančina a španielčina; pri chýbajúcom preklade angličtina. Spoločný názov GSU Warder Evolution neprekladať. Skontrolovať aj dlhšie preklady, zarovnanie hlavičky a texty tlačidiel.

Tieto úpravy zatiaľ NIE SÚ implementované ani vydané. r49 zostáva posledná vydaná verzia; r50 nebolo vytvorené. Pracovné prostredie počas zadávania nebolo dostupné, pri zápise tohto checkpointu už opäť fungovalo. Najprv dokončiť vyššie uvedenú geometriu v aktuálnej sekcii, potom pokračovať lokalizáciou; nepreskakovať medzi sekciami.

Pred vydaním primerané testy Python3.14.7, kompilácia, dva zhodné buildy a CI; novú verziu sprístupniť cez existujúci GSU updater. Opakované skúšky CAM, swapu, diagnostického archívu a už potvrdených šípok nežiadať. CCcam/Mbox a samostatný SRV bez príslušnej služby stále nie sú hardvérovo overené; celý plugin neoznačovať za úplne overený.

## Štruktúra repozitára

Aktuálny plugin, zdroje grafiky, testy, build a updater sú v plugin/. Starý paralelný src/, testy, packaging, legacy, staré roadmapy, dva nepoužívané workflow a dokončené jednorazové konverzné skripty sú odstránené. Pôvodné runtime resources.tar.gz, kontrolné súčty a inventár sú potrebné pre súčasný build a regresné testy, preto zostávajú. Historický priebeh je v Git histórii.

restoration/update/candidate.json je iba kompatibilná adresa pre už nainštalované verzie. Publisher ju udržiava obsahovo zhodnú s plugin/update/candidate.json s pôvodnou adresou balíka pre prísnu kontrolu starého aktualizátora až po overení vydaného IPK. Nemať tam druhé jadro ani druhý build. Čistenie samo nemení runtime ani verziu/IPK; otvorené grafické a jazykové úlohy vyššie zostávajú rozpracované.

Kontrola štruktúry: dva nezávislé buildy vytvorili presne pôvodný vydaný r49 IPK, 3639402 B, SHA256 80432461c90e190acc7be3b345b1c304aff9ef3b41b89bd7476ab9ba233d72c4. Zdrojový runtime a súbory prijímača sa čistením nemenia.

## Premenovanie repozitára — r50

Repozitár je Evolution-by-Warder/GSU-Warder-Evolution. Nový aktualizátor používa nový názov a plugin/update/candidate.json. Existujúce verzie používajú starú raw adresu (HTTP200 overené) a kompatibilný feed s pôvodným download URL; GitHub presmeruje stiahnutie. Test kontroluje manifest aj pôvodným prísnym parserom. Zachovať oba feedy pri každom vydaní. CI pri prvom presune zachytil chýbajúce ignorované PNG; požadované pôvodne verzované grafické súbory sú doplnené. Pred publikáciou overiť čistý checkout bez lokálnych neverzovaných súborov.
