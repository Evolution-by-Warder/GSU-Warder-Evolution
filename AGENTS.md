# GSU-Warder-Evolution – pravidlá pre prácu

## Trvalé pravidlo dokončovania schválenej práce (22. 11. 2026)

Toto pravidlo výslovne požadoval vlastník pre **všetky projekty Evolution-by-Warder**. Je nadradené starším všeobecným formuláciám o opakovanom schvaľovaní každého merge, IPK a produkčného zápisu.

1. **Jedno schválenie na konkrétny rozsah.** Ak vlastník schválil pomenovanú úpravu, celú dávku, vydanie alebo vopred definovanú automatickú aktualizáciu, súhlas zahŕňa aj obvyklé dokončovacie kroky v tomto rozsahu: vytvorenie PR, absolvovanie povinných testov, zlúčenie do `main`, zostavenie/vydanie príslušného finálneho balíka (ak projekt balíky vydáva) a aktualizáciu produkčného kanála. **Nepýtaj sa znovu na ten istý súhlas pri každom kroku ani v novom chate/Worku.** Rozsah a zdroj schválenia zapíš do PR a projektového denníka.
2. **Dokončenie po úspešnej verifikácii.** Pokiaľ rozsah zahŕňa produkčné vydanie a všetky povinné relevantné CI/regresné testy prejdú, bezpečne dokonči merge → release → verifikáciu skutočne publikovaného artefaktu/SHA-256 → aktualizáciu produkcie. Ak je nastavená schválená automatizácia, nech postup vykoná ona. Nevydávaj zbytočné medziverzie a nenechávaj hotové, schválené PR otvorené iba kvôli opakovanému žiadaniu.
3. **Žiadne neautorizované rozšírenie.** Test-only/draft, nová neschválená funkcia, zmena schválenej grafiky, neoverená licencia, zásah do súkromných dát, mazaní/zálohovaní či zmena autentifikácie nesmú byť ticho považované za schválené na produkciu. V týchto prípadoch si vyžiadaj jedno nové konkrétne schválenie.
4. **Povinné stop-podmienky.** Zlyhané alebo neúplné CI, zmena očakávaného SHA, nejasná identita artefaktu, konflikt vetvy, nedostatočné oprávnenia, bezpečnostná chyba alebo neoverená publikácia blokujú merge/vydanie. Skutočný stav a blokáciu zapíš; nikdy netvrď, že automatický merge či release prebehol, ak nie je doložený na GitHube.
5. **Trvalé odovzdanie.** Každý nový chat/Work načíta tieto pravidlá, aktuálny `main`, otvorené PR, CI, posledné vydanie a projektový register. Pokračuj od posledného overeného kroku a dokonči už schválenú prácu bez návratu na staré opakované schvaľovanie. Zachovaj používateľské súbory, existujúce schválené picony a históriu.

Toto je záväzné pravidlo práce vo všetkých repozitároch; **samo vloženie tohto textu nespúšťa GitHub automatizáciu**. Ak chýba mechanizmus automatického vykonania, odlíš pripravenú politiku od reálne aktivovaného workflowu.


Tieto bezpečnostné pravidlá dopĺňajú existujúcu dokumentáciu projektu a chránia produkčné súbory. Rozsah úloh a vlastníctvo príslušných komponentov zostávajú nezmenené.

## Bezpečnosť GitHub prístupu, autentifikácie a nahrávania

- Na všetky projektové repozitáre používaj iba už schválené a autorizované GitHub pripojenia a podporované operácie. Bez výslovného predchádzajúceho súhlasu vlastníka nemeň spôsob autentifikácie, neprechádzaj na nové webové prihlasovanie, nevytváraj tokeny a nežiadaj heslá, jednorazové 2FA kódy ani iné prihlasovacie tajomstvá.
- Ak narazíš na obmedzenie prenosu veľkých alebo binárnych súborov, zastav len dotknutý prenos, zaznamenaj presnú príčinu, chybu a možné bezpečné riešenia. Nový spôsob prihlasovania či prenosu vyžaduje predchádzajúce výslovné schválenie vlastníka. Bežné technické rozhodnutia v rámci už povoleného spojenia môžu pokračovať.
- Neopakuj bez konca zlyhávajúce Base64 uploady ani autentifikačné pokusy. Ak nie je dostupný bezpečný schválený prenos, zachovaj existujúce výsledky a jasne odlíš lokálne pripravené archívy od skutočne nahraných a overených súborov.
- Pracuj na oddelených vetvách a pred každým zásahom over cieľovú vetvu, SHA-256 a integritu už schválených súborov. Nečakaná zmena hashov je blokácia, nie dôvod na automatické prepísanie. Produkčné zlúčenie a publikovanie vyžadujú preukázateľný súhlas s daným rozsahom; už udelený súhlas sa pri technickom dokončovaní neopakuje (pozri trvalé pravidlo vyššie).
- Po každej bezpečne dokončenej dávke ulož overiteľný commit a aktualizuj príslušný projektový register s presným SHA, rozsahom testov, stavom uploadu a zostávajúcimi nespracovanými výstupmi. Bez overenia vzdialeného súboru a hashov netvrď, že upload bol úspešný.

## Technické vykonanie automatického zlúčenia

- Pripravený workflow `.github/workflows/warder-approved-scope-auto-merge.yml` automaticky vyhodnocuje otvorené PR po dokončení relevantného CI, po schvaľovacom komentári a dennou bezpečnostnou kontrolou.
- Po **existujúcom výslovnom schválení konkrétneho rozsahu** doplň na dotknutý PR komentár z autorizovaného účtu vlastníka `Evolution-by-Warder` obsahujúci presne jediný riadok `<!-- WARDER_APPROVED_SCOPE_SHA:<aktualny-40-znakovy-HEAD-SHA> -->`. Ide o technický záznam už udeleného súhlasu, **nie dôvod znovu sa pýtať používateľa**. Po ďalšom commite najprv skontroluj, či je stále v povolenom rozsahu, a potom obnov schvaľovací SHA marker bez novej otázky.
- Workflow zlúči iba nedraftový PR z toho istého repozitára do `main`, po úspechu CI, bez konfliktov a s presne zhodným SHA; ochrany vetvy sa nikdy neobchádzajú. **Bez úspešného CI sa nič automaticky nezlučuje.** Zmeny `AGENTS.md` a `.github/workflows/` zostávajú zámerne pod manuálnou bezpečnostnou kontrolou.
- GitHub zlučovanie samo nevydáva IPK ani nemení produkčný aktualizátor; po merge musí schválený a úspešný projektový vydávací workflow urobiť vlastnú kontrolu oficiálneho artefaktu a až potom publikáciu. Ak publishing nie je automatizovaný alebo zlyhal, hlás to ako blokáciu, nie ako dokončené vydanie.

## Povinná synchronizácia oficiálneho webu pri každom vydaní (25. 11. 2026)

Vlastník výslovne nariadil pre všetky súčasné aj budúce projekty Evolution-by-Warder: **každé nové schválené a overené stabilné vydanie skinu/pluginu musí v tom istom vydávacom cykle aktualizovať aj https://warder-evolution.eu/.** Ide o povinný dokončovací krok, nie voliteľnú úlohu na neskôr. Súhlas s vydaním zahŕňa synchronizáciu v jeho rozsahu bez opakovaného schvaľovania.

- Over skutočne publikovaný stabilný GitHub release, tag, verziu, IPK, dostupnosť a kontrolný súčet artefaktu. Test-only, draft, prerelease a neoverené buildy neuvádzaj ako stabilné.
- V centrálnom repozitári YouTube-Warder-Evolution aktualizuj `docs/index.html` a produktový detail: verziu, status, priame odkazy na IPK a release notes, dátum overenia, popis zmien, funkcie, kompatibilitu, jazykovú podporu a ostatné reálne zmenené údaje vo všetkých štyroch jazykoch SK/EN/DE/RU. Pri dátových aktualizáciách bez nového IPK aktualizuj dotknuté verejné údaje, ak sa zmenili. Zachovaj nedotknuté produkty, grafiku, galérie a právne/autentifikačné stránky. Informačná bublina planéty preberá existujúci obsah detailu, nie duplicitné údaje.
- Pracuj cez webový PR z aktuálneho main, koordinuj súbežné zmeny. Po úspešnom webovom CI zlúč, over úspešné GitHub Pages nasadenie a správnu verejnú verziu a odkazy. Nedostupné verejné overenie či zlyhanie nasadenia zapíš ako blokáciu.
- V projektovom registri a webovej dokumentácii eviduj release/tag, webový PR/commit, testy a nasadenie. Vydanie neoznač za kompletne dokončené, kým nie je synchronizácia webu overená. Pri blokácii rozlišuj vydaný plugin od neaktualizovaného webu. Pri novom projekte doplň katalóg a detail s planétou podľa dokumentácie.
- Platí aj pre automatizované vydania. Samotný zápis pravidla nie je automatický cross-repository trigger; kým taký mechanizmus nie je preukázateľne zavedený, vykonáva synchronizáciu zodpovedný release Work/agent. Existujúce CI, bezpečnostné stop-podmienky a pravidlá autentifikácie zostávajú záväzné.

Centrálne pokyny: [WEBSITE-RELEASE-POLICY.md](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/blob/main/WEBSITE-RELEASE-POLICY.md), [zdroj webu](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/tree/main/docs), [dokumentácia animácie](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/blob/main/docs/WEBSITE-ORBIT.md).

Pre tento projekt: `docs/gsu.html` v centrálnom webovom repozitári.

## Trvalé číslovanie GSU Warder Evolution (26. 11. 2026)

Vlastník výslovne schválil prechod na vlastné trojzložkové číslovanie: cieľová verzia `0.41.5`, potom `0.41.6` atď. Historické verzie 13.x-rN, tagy a IPK zostávajú nemenné. Nové používateľské verzie nemajú príponu -r ani epochu; OPKG metadata používajú epochu `1:`. Zachovať identitu balíka, adresár a nastavenia.

**Povinná migračná brána:** existujúci r5 aktualizátor neprijíma X.Y.Z a vyžaduje presnú zhodu verzie IPK s manifestom. Najprv pripraviť kompatibilnú stabilnú prechodovú verziu `13.41-r6` s novým parserom, validáciou epochy a oddeleným novým stabilným feedom. Pôvodný stabilný feed musí zostať dostupný pre staré aktualizátory a ponúkať prechodový r6; zmrazené r93 feedy sa nemenia. Následne publikovať `0.41.5` iba po overení reálneho prechodu r93/r4/r5 → r6 → 0.41.5, OPKG epochy, kontroly inštalácie, histórie, natívnych CI a verejných IPK/feedov. Nepoužívať force-downgrade ani meniť existujúce tagy. Web aktualizovať až po overení produkcie, vo všetkých štyroch jazykoch. Zapisovať presné SHA, testy, artefakty a blokácie do registra.

## Migrácie a veľkosť aktívneho repozitára

Pred vydaním over čistú inštaláciu, aktualizáciu zo skutočného podporovaného základu, jej opakovanie, bezpečné správanie pri chybe a návrat na pôvodnú zostavu. Pre každý nahradený súbor urči jeho vlastníctvo a spravované cesty. Zachovaj používateľské nastavenia, samostatné zálohy, údaje ostatných pluginov aj licenčne požadované súbory.

Pri zmene skontroluj nové veľké binárne objekty, archívy a životnosť skúšobných artefaktov. Potrebné verejné balíky, katalógy a migračné adresy eviduj s ich závislosťami. Pred čistením histórie zmeraj Git aj pracovný strom, over nezávislú šifrovanú obnovu a vyžiadaj potvrdenie vlastníka pre zásah do histórie, produkčných referencií alebo viditeľnosti. Výsledok a následnú kontrolu služieb zapíš do registra. Rovnaké pravidlá preberajú nové projekty.

## Čistá náhrada programových súborov cez OPKG

Pri inštalácii, aktualizácii a obnove ponechaj nastavenia, prihlásenie, OAuth, knižnicu a ostatné osobné dáta na pôvodných cestách. Pred zmenou over cieľový podpísaný IPK, vlastníctvo ciest a účinok preinst, prerm, postrm a postinst. OPKG nahrádza vlastný programový obsah a nový plugin načíta existujúcu konfiguráciu. Poškodené alebo chýbajúce staré súbory sú podporovaný vstup. Kontrola integrity patrí novému balíku a výsledku inštalácie.

Rešpektuj zámok, závislosti a vlastníctvo iných balíkov. Odstraňuj iba vlastný nahraditeľný kód a jeho cache. Bežná výmena prebieha bez zálohy alebo obnovy nedotknutých dát, medziverzií a ďalších archívov. Ak starý odinštalátor zasahuje do osobných dát, najprv oprav konkrétny deštruktívny krok alebo dolož najmenšiu potrebnú výnimku. Otestuj zmiešaný a neúplný stav aj načítanie pôvodných dát po výmene. Toto rozhodnutie má prednosť pred skoršími pokynmi k tejto výmene. [Rozhodnutie vlastníka, 28. 11. 2026](https://github.com/Evolution-by-Warder/Trezor/issues/5#issuecomment-7235637234).
