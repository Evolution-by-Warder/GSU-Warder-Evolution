# 26.11.2026 — Scoped diagnostic information dialogs and cancellation regression

HEAD `054eb888f7ebddd26dd77084ad6b5f18247c29a9` passed package reproduction/migrations and architectures. OpenATV/OpenPLi regression matrices each failed one of 501 tests because the category provider assertion still expected no arguments; it now checks the actual cancellation token. Added a Warder full-screen scrollable information dialog for diagnostic export results, report saving and unavailable project entry points. Only these GSU-owned information routes use it; native confirmation callbacks, destructive actions and all image-wide screens are untouched. New test verifies real routing and close/scroll controls. Remaining native tuner warnings, selection dialogs, legacy operations and physical checks not claimed complete. No production changes.

---

# 26.11.2026 — Fair storage category budgets and system regression repair

On HEAD `eb2cfd9618877817650e9fdb35b6322986f0adbb` package reproduction passed; OpenATV/OpenPLi regression jobs each failed one of 500 tests because the original AST inventory still required the explicitly replaced GlassSysInfoBrowser.HelpKey and other retired methods. Updated only that obsolete screen contract, preserving public class/constructor and every other inventory guard. Storage analysis now has independent 100,000-entry/3-second budgets per category, depth-bounded streaming traversal, cancellation, existing mount/symlink boundaries, and local configured PiconHub profile paths (verified actual four-profile settings keys on PiconHub main), XPicons/ZZPicons/data locations, custom PNG filtering and hardlink deduplication. Skin traversal excludes picon roots even when their scan is incomplete. Whole disk, arbitrary system and network paths not traversed. Small lower bounds show KiB instead of misleading 0.0 MiB; incomplete states remain explicit. Added fairness, real profile path, cancellation and formatting tests. Exact-head CI and receiver recheck pending; no publication.

---

# 26.11.2026 — Owner feedback: modern full-screen system information

Previous HEAD `8c7767b567e3d61a37bcc9fe89fabb1d7785b190` passed all four CI families (OpenATV 45810113912, OpenPLi 45810113667, architectures 45810113923, reproducibility 45810113679). Owner's screenshots show old packed System Information page duplicating process and log panels. Replaced the actual GlassSysInfoBrowser (same plugin/extension shortcut identity) with a full-screen six-card two-column layout, aligned typography, capacities, resource score, time and five observed protocol-daemon states. No duplicate process list or dmesg reads, old shell/temporary-file diagnostic path removed from the page. CPU/RAM/swap use shared modern measurements; RAM uses available rather than old raw free calculation. Disk temperature is optional non-waking SMART; all local mount detail still available via blue Details; green opens live monitoring and yellow refreshes. Protocol states mean daemon detected/not detected, not service reachability; missing observations remain unknown. Reused existing translated labels and artwork, no new binaries. Updated superseded legacy layout/help/refresh tests to validate new actual screen, independent log collector, one worker and closed callback, retained asset identity. New exact-head CI and physical receiver retest required; no production update.

---

# 26.11.2026 — Owner receiver feedback: integrated tuner screens and direct opening

Owner explicitly requests the native SatFinder and manual tuning black screens use the Warder visual style and removal of redundant Yes/No on opening. Reviewed real OpenATV 8.0 and OpenPLi release-9.2 ScanSetup, Satfinder and skin.py source. New native skin wraps existing configuration component and footer sources, shared Warder header, signal finder right panel uses raw frontend values and honest unknown states. Registered SatfinderMain retained with a scoped class substitution; unrecognized image entries keep native appearance. Native manual scan retains additive guard; SatFinder start rechecks recording safety. Direct user selection initiates verified backup without extra confirmation; existing recording/timeshift/nearby timer checks, duplicate suppression, stale callback rejection, backup failure blocks and native destructive action safeguards remain. Physical screenshot baseline prior HEAD ad51988e892fc86087af059f5cc269d025a80bca all four CI families SUCCESS, main menu/system cards/live charts/process/log and native finder/manual opening verified visually; other hardware checks remain. New exact-head CI and receiver retest mandatory. No production change.

---

# 26.11.2026 — OSCam embedded menu geometry and file navigation

Exact predecessor `31dbcda0fae7ee691f28fe4934c35b192e1f6019` passed all four workflow families: OpenATV 45806695851, OpenPLi 45806695563, architectures 45806695580 and reproducibility 45806695576. Audit found that OSCam workspace stretches legacy text/status geometry horizontally but not alpha-blended navigation icons, which can overlap labels and look too small in 42-pixel rows. Intro and file navigation now use one native geometry with square scaled icons, readable text, retained availability only on actual availability rows and exact original row IDs. File choices use settings/log symbols instead of an unconditional green status light; no file access, URLs, credentials, action dispatch, or CAM logic modified. Added geometry coverage at four resolutions and 1920x1200 plus actual file controller identity regression. Existing data tables and genuine state indicators remain unchanged. No new translatable strings; 21 catalogues retained. New exact-head CI and physical retest pending; production remains 0.41.5.

---

# 26.11.2026 — CAM/SRV action panel icon checkpoint

Continued PR #19 from `d7aa030e102504696ffb517e5c31db8064c708f1` (four workflow families in progress at inspection); earlier `ef18452b6ef78293ac74192e0307c5a455fb230f` completed all four workflow families SUCCESS. Added eight functional local icons to the right-hand CAM/SRV action panel. Selected background includes icon and label, fixed horizontal anchor scales with actual desktop width. The standalone SRV restart icon follows existing native visibility and autocheck icon moves with its existing row; visible heading follows installed server capability. Existing action IDs, focus semantics, commands, availability colors, native configuration and saves preserved. Tests cover icon geometry and layering at HD/FHD/WQHD/UHD and non-16:9, dynamic SRV visibility and title. New exact-head CI and physical receiver verification still required. No release, feed or website changes; production 0.41.5.

---

# 26.11.2026 — Legacy navigation icon checkpoint (continued from PR #19)

Previous exact HEAD `ef18452b6ef78293ac74192e0307c5a455fb230f`: diagnostics reproducibility 45805814172, OpenPLi 45805814142 and OpenATV 45805814149 SUCCESS; architecture run 45805814141 in progress at inspection. Stable release remains 0.41.5. This checkpoint adds a native settings icon gutter keyed by ConfigElement identity, with full-width native fallback for unknown, overflowing or missing icons; it retains existing settings values, native edit/save/cancel, row height and translations. Legacy CCcam, OSCam and Mbox diagnostic menu rows reuse local functional icons while retaining independent green/red availability indicators, disabled colors, row IDs and action dispatch. No CAM operations, configuration or data collectors changed. Regression fixtures cover icon identity, four resolutions, geometry, row status and missing assets. New exact-head CI and physical receiver retest are required; main CAM/SRV action panel and remaining legacy screens still need visual review. No release, feed or website mutation.

---

# 26.11.2026 — Inline resource cards and branded product navigation

Owner-approved two-panel UI extended: the System health check now renders six native metric cards in the right panel (CPU, RAM, swap, flash free, disk free with mount, sensor temperature). Storage category result uses the same six-card surface with measured relative bars only for complete scans and explicit partial/lower-bound states. Summary and measurement coverage remain visible. Existing full-screen details unchanged; selecting another route or refreshing hides old cards, stale callbacks rejected. Layout tested by new fixture assertions for HD/FHD/WQHD/UHD; actual hardware render pending.

Reused byte-identical approved FullHDGlass, PiconHub and YouTube plugin logo PNGs in 118b543fe88f46aa081854a15ac91994c2ea7cf0 and existing GSU logo; provenance plugin/artwork/warder-project-logos.json. Radio logo source blob 369b60c8efac9439d05c104ebf46fd32a94f1d60 (1,338,260 bytes) returned empty base64 via fetch_file and binary UnicodeDecodeError via fetch_blob; instead use the existing local installed WarderRadio/plugin.png with bounded size and semantic fallback, no duplicate large file or external download. Product rows use 120x58 FHD slot and stable IDs. New regression tests verify original logo blob identity, optional Radio fallback, real card values and layout. Runtime/test checkpoint fe112ac79eedf5843c28b91dddd36773f066017a. Exact-head CI queued (45805715590, 45805715712, 45805715568, 45805715705).

Earlier publisher checkpoint 4bf7a7003f15ea53a2138a7a1ae486f52a38d6c4: OpenATV, OpenPLi and reproducibility SUCCESS; architecture check still in progress at inspection. Reproducibility run 45804602559 verified two byte-identical private CI builds 3,912,836 bytes SHA256 ee38e0aefd9c2aca9f0931f4aa43f010e405b03e45c62bf7b7019e64919b3576, installed regular files 6,872,041 bytes. Real isolated OPKG checks passed r93/r4/r5 via r6 and direct 0.41.5 to 1:0.41.6, allocated installed files 7,532,544 bytes on all routes. These are earlier CI artifact bytes, not final or publicly published IPK. Production still 0.41.5. Remaining: legacy CAM and settings icon/navigation review, exact-head CI, actual receiver visual verification, production publication and web synchronization. Other projects unchanged.

---

# 26.11.2026 — Prepare 0.41.6 release machinery and migration checks

OpenPLi/OpenATV runs 45803201697 / 45803201817 on 35c2efb failed exactly one of 490 tests: PNG signature fixture used escaped backslashes rather than bytes. Corrected in 853c59884759d1f160c128a6b7cc269490a1f773 (same PNG/CRC/deflate integrity assertions). Reproducibility on that prior HEAD succeeded, 3,910,370 bytes, SHA256 e1f6f732cf9feb895a20188a29f56e91897a562153f3e6fe82817b504403f4a3 (unpublished 0.41.5-numbered development build; not production artifact).

Generalized modern publisher for stable 0.41.x runtime version, verifies version/request/notes and exact active predecessor in register/feed, forward-only upgrade, verifies previous public IPK bytes, keeps immutable tags/assets and frozen r6/r93 feeds. README preflight now precedes tag creation. Updated reproducibility workflow and real offline OPKG migration to test direct upgrade from active modern release in addition to three historical paths. Workflow changes manually inspected: same restricted main-only publishing context, permissions and four prerequisite workflow families; only version selection and predecessor artifact retrieval added. Draft source version/request and 21 localized release notes advanced atomically to 0.41.6 in 53a06707db6d568c193df22cf2b6142615227498. New publisher regressions in 2d0336cf406c37200bfa16f1599bb70eb5f5aef8. Exact HEAD CI pending. No merge, tag, public IPK, stable feed or web change; 0.41.5 remains current. Further UI work remains (legacy CAM/settings menus, official product logos and structured right-hand cards), and physical receiver retest remains outstanding. GSU first; other projects unchanged.

---

# 26.11.2026 — Six simultaneous live plots and navigation picons

Owner-approved modernization continued in PR #19. System live screen now renders six simultaneous 60-second trend cards (CPU, RAM, swap, temperature, RX, TX), with actual current values, independent scales and min/max/mean. One existing sampler and timer, no new workers per metric; missing observations create gaps, not fake data. Native CanvasSource.line confirmed in OpenATV 8.0 and OpenPLi 9.2. Existing signal history/export remains separate. System controls pause/resume and interval; arrow cycling is no longer needed on this screen.

Added 22 local navigation PNGs: four byte-identical existing Warder YouTube assets (search/history/settings/update, source manifest plugin/artwork/warder-navigation-sources.json) and 18 new transparent 64x64 original cyan/white functional symbols (design paths and blob SHA in plugin/artwork/warder-navigation-original.json). Binary tree commits 1f93564dec9149e656fc8d30c18e2e650b8f16e0, 3811bcd0951078bb0db49a3b679dfa04122d09d2, b409f3488c1289ddd7fdb0fc418cb8dbdd750bac. First all-at-once blob attempt exceeded connector call limit; no branch update from that attempt; smaller atomic batches succeeded. Navigation uses stable IDs, 48x48 FHD scaling, bounded local LoadPixmap cache, alpha blend and text fallback; main centre navigation dots replaced, red unavailable indicator retained. Centre/project list bindings added; project glyphs are semantic icons, not yet official product logos. Existing artwork/other projects unchanged. Settings and older CAM internal lists still pending.

Previous exact checkpoint 86de5331b75cc5634286c51bc3be5fff52e3a21b completed all four workflow families SUCCESS (45798853305, 45798853701, 45798853674, 45798853213). New runtime/test checkpoint 11fa1bf95d629cc73a667ce838ccc09f6f91e438 has new CI queued, not yet green. Added six-metric, missing-data, PNG CRC/deflate, route coverage, native pixmap and cache tests. Physical display/legibility not verified. Next: finish remaining UI including legacy menu icons and product logos, review exact-head CI, prepare safe modern publisher/version, verify receiver and release. No stable asset/feed/version change yet; GSU first.

---

# 26.11.2026 — Two-panel centre workspaces (owner screenshots)

Approved: retain navigation on the left and actual selected results on the right, using two independently outlined panels rather than a full-page list of descriptions followed by another screen. Implemented shared split layout, selected result title, timestamp/loading/error status, explanatory text before activation, OK/green loads read-only results inline for 12 routes plus all five product pages; yellow refreshes; blue opens full detail; up/down navigate left and left/right page the right result. Reused report collectors, no additional automatic active network tests on cursor movement. One worker at a time, cancellation/stale result checks and latest request queue. Native tuner-changing tools, legacy configuration screens, quick signal and live graph screens still open separately; process table, category meters, network panels and export remain available in full detail. Existing main menu/PIG unchanged. No new menu PNGs yet. Tests for panel separation, actual result binding, stale callback and project detail path, adjusted reference-font width check. Runtime/test checkpoint d1cbf9ed70af222729bca8d6fea3837e90b87a87. Exact HEAD CI and receiver verification pending; no release or production changes. Follow-up: refine right-hand visual cards and multi-metric live graph, menu icons, other remaining diagnostics and safe release tooling. Other four projects deferred until GSU complete.

---

# 26.11.2026 — Diagnostic descriptions and compact network dashboard

Owner requested useful descriptive sentences and one attractive screen instead of scrolling ordinary technical values. Added localized explanatory templates and complete system/process/active tuning descriptions for all 21 languages; all 17 diagnostic routes now show expanded content descriptions. Network overview now uses two side-by-side native panels with actual interfaces, speeds, IP addresses, gateways, DNS and mount count, with independent overflow navigation only if needed. Missing data and error fallback retained. Tests for descriptions, panels, focus, data binding and layout added. Runtime/test checkpoint c7057988eb3cf826b7fad2d7b88b28e5f12d2fb7. Shared icon standard saved in e74712e6d69c9f473f7eaf7a8b8d3e4af6f91540; actual new menu PNGs and integration still pending. Other bounded reports still require individual layout redesign, physical receiver check and exact HEAD CI; no production release changes. GSU first, other projects deferred.

---

# 26.11.2026 — Warder visual standard and single-screen diagnostic presentation

Owner approved small functional menu picons throughout all five projects, based on existing Radio/YouTube artwork, and replacement of decorative blue/green navigation dots in FullHDGlass settings without changing status indicators, menu density or actions. Full scope is recorded in [WARDER-ICON-STANDARD.md](docs/WARDER-ICON-STANDARD.md). GSU first; remaining projects deferred until GSU is complete.

Additional owner feedback: menu descriptions must explain actual functions in meaningful sentences (not merely Available memory). For bounded diagnostic data use one clear full-screen dashboard, two or three complementary panels, icon-led headings and aligned values rather than long scrolling prose. Keep separate expert details and scrolling only for genuinely unbounded lists, logs and release notes. Do not combine unrelated functions, hide unsupported hardware status, truncate necessary data, or reduce legibility. Apply this to tuner/channel details, storage, network, service, project pages and anonymous report as appropriate; preserve existing process table and live chart. Exact visual verification on receivers required. Implementation pending; no other project runtime changed.

OpenPLi CI 45795763637 on e139d6a failed one of 482 tests due to wrong test fixture import (Screens package returned a class). Corrected fixture import in 5981f4ef9108ee2939edd4d16b3f090bc66b870c; no runtime guard removed. Reproducibility run 45796906808 succeeded on that checkpoint; all final exact HEAD checks remain required.

---

# 26.11.2026 — Manual scan blank native screen on receiver

Owner's five screenshots show successful channel backup, confirmation, bare live TV, and EXIT returning to Reception centre. Root cause identified from source: GSU opens AdditiveScan subclass; native OpenATV Screen derives skinName from actual subclass and readSkin falls back to empty screen when no skin exists. OpenPLi ScanSetup explicitly provides ScanSetup/Setup names. Fix commit f1dd04ddc6802759b787c8fb33df664baf5ed1f0 preserves ScanSetup and native fallback names after parent initialization, without weakening additive scan/recording safeguards. Regression test commit 9f0afc867ed68d5b66c6b948cd5f20ae42829669 checks both native initialization styles and blocked/allowed scan flags. Earlier single-confirmation and direct tool navigation retained. Exact HEAD CI and physical retest pending; no production changes. Source evidence: openatv/enigma2 8.0 lib/python/Screens/Screen.py and lib/python/skin.py, OpenPLi/enigma2 release-9.2 ScanSetup.py. This is a distinct native skin lookup bug, not the common ScrollLabel layering issue.

---

# 26.11.2026 — Simplify native reception tool navigation (owner receiver screenshots)

Owner reported excessive navigation and repeated confirmation before SatFinder. Reception centre now expands the existing tuner-native route into registered native tool rows, retaining the compatibility selector only when needed. One explicit confirmation covers a verified private channel backup and possible live-TV interruption. No backup or retune on cancellation; recording/timeshift/nearby timer checks before consent, after consent and after backup, no launch if the owning screen changed or backup fails, duplicate requests suppressed. Last successful backup path shown in the centre detail panel rather than a second modal. Passive signal routes unchanged; native tool screens still use the image UI. Localized new consent in all 21 languages; tests cover direct routes, single consent, backup failure, recording and navigation cancellation. Pending exact-head CI and physical retest; no stable release yet.

---

# 26.11.2026 — detail presentation and live feed cross-check

Continued PR #19: group known transponder services into TV and Radio with counts; checked native OpenATV 8.0 db.cpp channelID query ordering (namespace/TSID/ONID). Tuner report separates transponder, tuner occupancy and channel information. Project pages display installed and stable version on separate lines. Forum preview presents the exact allowlisted JSON fields in readable sections, retains exact JSON for save and falls back to raw text for unknown schemas. Added route and presentation regressions. Read actual main manifests for all five projects: FullHDGlass 1.0.94, PiconHub 0.1.46, Radio 0.2.2, YouTube 1.0.4, GSU 0.41.5; feed identities, URLs and formats match the existing parser's expected inputs. Not proof of receiver network connectivity or installed package detection. Existing export and tuner safeguards unchanged. CI was queued on previous checkpoint; exact new HEAD and physical receiver checks required. Release tooling still pins 0.41.5 and must be generalized or advanced safely before a subsequent stable publication; existing tag/feed untouched.

---

# 26.11.2026 — 0.41.6 diagnostic output modernization

PR #19 extends the physical receiver rendering regression fix with a shared branded header (date, live clock, installed version; suspended on hide), a separate result/status area, six readable resource cards and real percent meters, source/mount identification, a native five-column process list (PID/name/state/RSS MiB/measured CPU, RAM/CPU sorting), six storage-category rows with measured sizes and relative bars only when all measurements are complete, chart axes with explicit scale and 60-second history, more legible disk capacities and SMART output, local network addresses/mount count and installation status. Empty results and failed refreshes show explicit unavailable states rather than stale or fabricated values. All new category captions are localized in 21 languages. Existing data collectors, privacy allowlist, tuner/recording safeguards, canonical update actions and approved artwork preserved.

Runtime/test checkpoint ead3e2c1ced227bd70552887cd5712d7f8b5db27. Added regressions for actual provider routing, native process and category binding, header lifecycle, blank translation, backing layers and all six modes at four resolutions. At checkpoint CI runs 45794499664 (package reproducibility), 45794499614 (OpenATV), 45794499501 (CPU architectures), 45794499606 (OpenPLi) were queued; no green result or physical receiver rendering claimed. PR remains draft; no version/tag/feed or web change. Remaining: inspect exact-head CI, verify all affected pages and visual quality on actual hardware; prepare subsequent stable release only after gates, then synchronize SK/EN/DE/RU website and register. Do not overwrite 0.41.5.

---

# 26.11.2026 — Physical receiver regression in 0.41.5

Owner supplied 12 screenshots: System overview RAM heading clipped; Processes, Log, Tuners, Transponder services, Storage, Space by category, Network overview, Connection test, Installation check, IPK /tmp, Forum report show blank content; unused green/blue buttons display gettext header. Code inspection confirmed native OpenATV ScrollLabel.applySkin forwards zPosition to child labels, not parent eWidget; modern opaque backings at +1/+2 occlude the parent at 0. Fix dashboard and CAM backings below 0, protect empty msgid globally, shorten RAM title and ensure footer noWrap, explicitly display Unavailable on empty report or native import failure. Added layout and route/provider regressions for all 11 report kinds and 5 project pages. Current work branch work/gsu-0416-rendering, no production changes, CI and physical receiver retest pending. No claim that all providers work on actual hardware. Next: run exact HEAD CI, inspect failures, verify content on receiver; release subsequent stable version only with verified gates. Do not rewrite 0.41.5.

---

# 26. 11. 2026 · stabilná 0.41.5 a nasadenie webu

[PR #16](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/pull/16) bol zlúčený po všetkých 17 úspešných kontrolách na b90807a0a4a56a4fb36437fe1978ca00aaa33e54. Publikovaný tag v0.41.5 smeruje na 30a420d5019446c1b33f48fe586addc5f9ead153. Verejné bajty a SHA-256 overil produkčný workflow 45786453936. Moderný feed je aktívny od fac1e9a9a9a7ab022f75361dc0af94b0c44e80b2.

IPK má 3 873 060 bajtov, SHA-256 115bc57d4c842049d72864a0e2deaf0eceb35f0bb7d53f515cc5533e9abc48fc. OPKG po každej migrácii alokoval 7 073 792 bajtov pre súbory balíka. Lokálne aj v CI prešlo 467 regresných testov. Výkon sa meral na dvoch natívnych runneroch a v troch emulovaných ABI. Výsledky a hranice fyzických skúšok uvádza [odovzdanie vydania](reports/gsu-0.41.5/CLOSEOUT.md).

Webový [PR #44](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/pull/44) prešiel oboma kontrolami na 9a28130cd0bd8a1db668bbeb54524df136146cf9. Nasadený commit ae4cfd43707860e843edc98f22e2dbfc1b028e93 potvrdil [GitHub Pages](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/actions/runs/45788135168). SK, EN, DE a RU obsahujú novú verziu, funkcie, kompatibilitu a odkazy. [Verejná kontrola](https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/actions/runs/45788582576) úspešne overila bajty vydania, sidecar, staré aj moderný feed, domovskú stránku, GSU detail a texty štyroch jazykov na skutočnej doméne warder-evolution.eu.

Pre prípadné ďalšie vydanie sa použije 0.41.6 a OPKG epoch 1. V rámci následného hardvérového overovania je otvorený živý príjem, motor, blindscan, HDMI/zvuk a zobrazenie na reálnom televízore.

# Produkčná aktivácia v0.41.5

Zdroj 30a420d5019446c1b33f48fe586addc5f9ead153, workflow 45786453936, overených 3873060 bajtov, SHA-256 115bc57d4c842049d72864a0e2deaf0eceb35f0bb7d53f515cc5533e9abc48fc. Samostatný stabilný feed je aktívny. Ďalší krok je aktualizácia webu SK/EN/DE/RU a kontrola Pages.

# 26. 11. 2026 · konečná kontrola balíka a alokácie

Na 9809b5f5083081d68668cd20f9f269b2ac57bf93 mali dve CI zostavy a lokálne bajty zhodný SHA-256 115bc57d4c842049d72864a0e2deaf0eceb35f0bb7d53f515cc5533e9abc48fc. Job 45784968376 overil tri cesty migrácie, veľkosť 3 873 060 bajtov a 6 500 779 bajtov súborov po rozbalení. Na natívnom CI AArch64 trvalo jedno odčítanie v priemere 0,423 ms (12 vzoriek po sekunde), CPU 5,908 ms spolu, špička procesu 14 312 KiB. OpenATV 45784968596, OpenPLi 45784968381, inštalátor 45784968501 a OpenBH uspeli. V emulácii už cieľové interpretery bežali. V izolovanej zostave chýbal modul unicodedata pre IDNA pri getaddrinfo, ktorý sa doplnil do cieľového interpretera. Plugin používa štandardné moduly image.

CI teraz eviduje aj skutočnú alokáciu súborov po inštalácii OPKG pre každú migračnú cestu. Započítava diskové bloky súborov z výstupu opkg files, každý inode raz. Matice oboch image aj kontrola inštalátora majú explicitný checkout presného PR HEAD. Lokálne 467 regresných testov. Produkcia a web sú podmienené úspešným overením.

# 26. 11. 2026 · kandidát pred vydaním

Predchádzajúci HEAD 5e5b062a70a03dec43cfa0f05ee62f52a4a0dd4c prešiel OpenATV 45784124685, OpenPLi 45784124525, inštalátorom 45784124554 a reprodukciou/migráciou 45784124546. Log linkera z behu 45784124598 ukázal presnú príčinu zlyhania krížovej zostavy. Premenná LIBC s názvom architektúry kolidovala s rovnomennou premennou CPython. Workflow už používa samostatný názov pre výber správneho balíka Debian.

Aktuálny kandidát dopĺňa údaje DVB-T/T2 a DVB-S/S2 podľa údajov ovládača, opätovne overuje súbežné zmeny súborov v zálohe a zabraňuje uloženiu zálohy používateľa na sieťový mount. Príručka zodpovedá novým centrám a vysvetľuje obnovu. Lokálne prešlo 466 testov a 3 024 kontrol rozmerov. Dve zostavy IPK majú 3 873 060 bajtov a SHA-256 115bc57d4c842049d72864a0e2deaf0eceb35f0bb7d53f515cc5533e9abc48fc, bežné súbory po rozbalení 6 500 779 bajtov. Produkčná aktivácia a web sa evidujú až po úspešnom merge a kontrole verejných bajtov.

# 26. 11. 2026 · meranie a optimalizácia teplotných čidiel

Na 17f50f2745ade5e90757880722c8da09cdf59af4 uspeli OpenATV 45782325859, OpenPLi 45782325928, reprodukcia/migrácie 45782325936 aj kontrola inštalátora 45782325857. OpenBH prešiel aj kontrolou 3 024 ovládacích textov. Pri zostavovaní krížového CPython zachytilo CI 45782325842 problém s nesúvisiacimi rozšíreniami pre vývojový hostiteľ. Nové zostavenie cieli na skutočné natívne moduly potrebné na spustenie samplera a IPv4/IPv6 pod emuláciou.

Meranie odhalilo zbytočné opakované čítanie pomalých tepelných senzorov. Živé meranie používa päťsekundový interval pre tento senzor, zobrazuje vek výsledku a štatistiku počíta z čerstvých pozorovaní. CPU a sieť zostávajú pri nastavenom intervale. Lokálne meranie na x86_64, 12 vzoriek po sekunde, priemer 0,539 ms, CPU 7,832 ms spolu, špička procesu 11 136 KiB. Čísla nepopisujú reálny prijímač. Ďalší krok je kontrola všetkých troch emulovaných ABI, presného kandidáta a produkčná verifikácia.

Manuálne preskúmané vydávacie workflowy a ich volané skripty. Historické vydávacie vetvy spúšťa ich vlastná vetva, r6 má len manuálnu obnovu pôvodných bajtov. Moderné zverejnenie vyžaduje úspech všetkých štyroch volaných pracovných postupov, overený IPK z toho istého behu, stav hlavnej vetvy a historických feedov. Pri zhodnom už zverejnenom tagu iba kontroluje existujúce bajty. Zápis na main je bez force. Referenčné zdroje sa načítavajú v read-only joboch. Lokálne 465 testov, balík 3 871 820 bajtov, SHA-256 b0aee79b5566cfd6de66208143d0b8bc1d949f81e889c96685bb8c0110637a8a. Toto je kontrola pracovného balíka.

# 26. 11. 2026 · výsledky kandidáta a rozhrania prijímača

Na e08b766f399eceb865febd6ad3ff217bce6ba3cd prešli matice OpenATV (45781593896), OpenPLi (45781593863), kontrola balíka s migráciami a publikátorom (45781593912), inštalátor (45781594076) aj natívne rozhrania OpenBH. Kompilátor troch emulovaných cieľov nevedel pri konfigurácii CPython na hostiteľovi spustiť cieľový getaddrinfo. Overenie sa presúva do hotového cieľového interpretera pod QEMU pre IPv4 aj IPv6. Na vývojovej vetve sa zatiaľ nevydal žiadny IPK.

Posledné doplnenia zahŕňajú pasívny výber tunera bez preladenia, oddelenie výsledku testu internetu od zlyhania aktualizačného servera, rozpoznanie výpadkov zámku, anonymný výstup s povolenými diagnostickými hodnotami a meranie rozmerov 3 024 preložených ovládacích prvkov. Kontrola odhalila príliš dlhý ruský popis živých meraní. Nasleduje kontrola presného HEAD a publikácia po úspechu.

# 26. 11. 2026 · príprava publikácie 0.41.5

PR #16, commit 66e2962371ad71ed042fa0f7ee5aa49e79f98ff9. OpenATV 45780291483, OpenPLi 45780291593, reprodukcia a migrácia 45780291413 aj inštalátor 45780291582 uspeli. Lokálne 458 testov. Pri prvom zostavení emulátorových testov (45780291482) chýbali hlavičky cieľovej libc. Doplnené sú explicitné závislosti pre každú ABI a kontrola natívnych rozhraní OpenBH. Emuláciu evidujeme oddelene od meraní na fyzickom prijímači.

Vydávací postup používa balík z úspešnej migrácie a vyžaduje zhodu vetvy, revízie, existujúcich historických feedov, tagu, verejného IPK aj súčtu. Oprávnenie na zápis má len produkčný job na main. Pri kolízii nemôže prepísať existujúci tag či verejný balík. Samotná príprava pracovnej vetvy feed neaktivuje. Ďalší krok je verifikácia presného HEAD a verejná kontrola po schválenom merge.

# 26. 11. 2026 · diagnostika a ochrana zoznamu staníc

Commit cf26ac4e881d110f6162507910d291d4967455ac v PR #16 prešiel OpenATV (45778734178), OpenPLi (45778734177), reprodukciou s migráciami a natívnym meraním x86_64/AArch64 (45778734238) a kontrolou inštalátora (45778734218).
Ďalšia zmena pridáva stav závislostí balíka, samostatné stránky piatich projektov, kanonický vstup do aktualizácií a náhľad anonymného výstupu aj z pôvodných Nástrojov. Pred vstupom do natívneho ladenia sa vytvorí lokálna súkromná kópia lamedb a bouquetov so spätným overením každého súboru. Obnova spočíva v spätnom skopírovaní overených súborov do konfiguračného adresára Enigma2 pri zastavenom GUI. Umiestnenie zálohy sa zobrazí pred ladením. Súbor settings sa nekopíruje.
Referenčné jadrá OpenPLi release-9.2 a OpenATV master poskytujú isTimeshiftActive aj isTimeshiftEnabled a zhodný vstup do manuálneho ladenia. Pribudli kontrola lokalizačných súborov, HiSilicon a meranie pod emulovanými MIPS/MIPSEL/ARMv7. Fyzické zariadenia neboli pripojené. Produkčný r6 aj staré feedy zostávajú aktívne. Nasleduje kontrola emulovaných výsledkov a vydávacieho postupu.

# 26. 11. 2026 · overenie migrácie a auditu

Implementačný commit 0f76366b94dbb97e002318064823bc489640296b prešiel štyrmi workflowmi. Nasledujúci commit 4088a82731a3fb5734faf0ca32847e912ddf1973 zaviedol verejnú verziu 0.41.5 a interné balíkové číslo 1:0.41.5. Tri relevantné workflowy uspeli (45776767657, 45776767676, 45776767689). Job 139762183252 overil tri izolované aktualizácie r93/r4/r5 → r6 → 1:0.41.5 so skutočnými historickými IPK a zachovaným nastavením. CI meranie tohto medzistupňa: 3851822 komprimovaných bajtov, 6428850 bajtov regulárnych súborov; SHA-256 fa86333b6051139f8c9315558b6ad4018111d19723fc81c075397ed63084885f. Vývojový balík sa nevydával.

Presná kontrola odhalila rozdiel medzi OS bajtom gzip hlavičky Pythonu 3.12 a 3.14. Ďalšia dávka normalizuje gzip, dopĺňa šesťkarietový prehľad, plávajúci signál s voliteľným zvukom, detailné CAM panely, HDMI dáta, bezpečný export služieb TP, ochranu timeshiftu, doplnkové testy a meranie samplera. Funkčné zdroje, hranice a pôvod porovnania sú v docs/GSU-0.41.5-REFERENCE-AUDIT.md. Odkaz LinuxSat a rozsah verejného auditu výslovne doplnil vlastník. Ďalší krok: verifikovať presný HEAD, lokálny a CI hash, hardvérové obmedzenia, konečný publikátor a web až po stabilnom vydaní.

---

# 26. 11. 2026 · GSU 0.41.5, PR #16

Vlastník schválil implementáciu, kontrolované zlúčenie a stabilné vydanie po overení v rozsahu zadania. Integrácia produkčného main e064e426d1c7388200b9ed4727aacbf5e5705bc8 do pracovnej vetvy je cbe4de0cb836d3589b8d7188574b1761e259bad1. Zachované oba nezávislé bloky registra. Na integračnom commite a0f0adfef5637b2e728b234d11c83d07ddf368fc uspeli štyri workflowy vrátane reprodukovateľnosti 45774748963, OpenATV 45774749143, OpenPLi 45774748935 a balíkovej kontroly 45774749115.

R6: tag v13.41-r6 ukazuje na 45a9fad7be6e20a6eae6055c0cb59551be45b9f9. Porovnanie SHA verejného assetu s nezávisle stiahnutým CI IPK potvrdilo 3813348 bajtov a a8e79609147666b27f18460b3340e099bb013664478a787746bcf56bb28052e2. Produkčný workflow 45773458863 overil verejné bajty a sprievodný súčet. Nový stable-modern.json je zatiaľ prázdny. Produkčná verzia zostáva r6.

Funkčný prírastok: natívne grafy so 60-sekundovou históriou, SNR/AGC/dB/BER/LOCK, export CSV, merania CPU/RAM/swap/senzorov/RX/TX, CPU a RSS procesov, natívne ladenie chránené kontrolou nahrávania, príjem a parametre streamu, SMART bez prebúdzania diskov, kategórie obsadenia, meranie brány/HTTPS, stav piatich oficiálnych feedov, kontrola inštalácie, náhľad anonymného exportu a kontrola lokálnych IPK. Vlastné rozloženia pre štyri rozlíšenia. Nové obrazovky sú dostupné z menu. Posledná miestna sada pred doplnením špecifického testu IPK mala 448 úspešných testov. Hardvér nebol meraný. Pokračovanie: overiť nový HEAD, skompletizovať číslovanie balíka, migráciu v OPKG, fyzické schopnosti prijímačov a otvorené položky auditu pred vydaním. Web sa synchronizuje po publikácii.

---

# 2026-11-26 — stable r6 publication

PR #15, immutable source `45a9fad7be6e20a6eae6055c0cb59551be45b9f9`, workflow 45773458863, public IPK SHA-256 `a8e79609147666b27f18460b3340e099bb013664478a787746bcf56bb28052e2`, 3813348 bytes. Both native matrices and packaged install gate passed. Feed activation via atomic fast-forward below; website verification remains pending.

---

# 2026-11-26 — Owner-approved independent version numbering

Target public version `0.41.5`, OPKG version `1:0.41.5`, GitHub tag `v0.41.5`, subsequent releases `0.41.6` etc. Stable r5 was already published: source `9e03199394ca498d30120cca5cf184752e0f1bbf`, SHA256 `17de1b2624dd90b77d2c8c05ceba997e683c2d66d888212dda21e31233ef7085`. Do not overwrite. Existing updater only parses historical versions and validates exact control version, so direct feed switch would break installed receivers. Prepare final legacy-compatible r6 bridge and separate modern feed, keep old feed on bridge and frozen r93 feeds unchanged. Implement epoch-aware package builder, manifest and installed health validation, version comparison and history, localized notes, tests for actual old updater and OPKG, then stable publisher and four-language website. No production changes at this checkpoint. Branch `work/gsu-version-normalization`. Existing r5 website synchronization remains separately required.

---

# 2026-11-26 — Consolidated GSU 0.41.5 architecture

See [GSU-0.41.5-ARCHITECTURE.md](docs/GSU-0.41.5-ARCHITECTURE.md) for seven-centre navigation, progressive disclosure, feature requirements, technical modules, reference audit and release gates. Specification commit `34d52512bf1610b9836db1570750e7112bd97f8f`. Design only; implementation and complete reference audit remain open. Technical migration PR #15 remains separate.

---

# 2026-11-26 — Owner-required progressive disclosure and living-room usability

GSU 0.41.5 must be simple on the surface and professional in depth. Organize every redesigned area in three levels: concise overview with key measured values and meaningful status; drill-down details with history, graphs and recommendations; optional expert diagnostics (processes, logs, technical tuner/stream identifiers and service actions). One screen, one primary purpose; avoid information overload and duplicate navigation. Use generous spacing, legible TV-distance typography, consistent remote-control actions, short localized labels, accessible status text alongside colors, explicit unknown states and capability-aware visibility. Show only supported actionable functions; never fabricate health status from missing measurements. Preserve existing features and expert access, with no unnecessary complexity for beginners. Validate focus, long labels, scrolling, contrast and HD/FHD/WQHD/UHD layouts; test real receiver usability and performance. Approved UX requirement, not implemented functionality.

---

# 2026-11-26 — Owner-required differentiation from native image tools

GSU 0.41.5 must provide compelling value beyond stock OpenATV, OpenPLi, OpenBH and other Enigma2 system-information screens. Before implementing each feature, compare actual native image capabilities and existing GSU functionality; document the incremental value, avoid duplicate menus, reuse native APIs when suitable. Prioritize measured history/trends, actionable evidence-based diagnostics, cross-resource correlations, storage category breakdown, process resource attribution, network failure isolation, signal stability/lock-loss analysis, tuner occupancy and recording conflicts where supported, crash summaries, verified package integrity and Warder ecosystem status. Health scoring must be transparent, show measured checks/thresholds and unknown values, not invent observations or guarantee causes; only make recommendations justified by available measurements and avoid universal hardware temperature thresholds. Shared history is bounded and collected only when needed; optional alerts must be opt-in with negligible background load. Preserve compatibility, privacy, user configuration and existing functionality. No duplicated stock features solely for visual novelty. New UI is a unified Warder dashboard with drill-down details and actionable insights. This is a design requirement, not an implementation or parity claim.

---

# 2026-11-26 — Expanded signal centre scope approved by owner

Extend functional assimilation with EvgQuickSignal, CiefpSignalInfo and CiefpSatelliteAnalyzer, native SatFinder/PositionerSetup and SatScanner as reference products. Audit actual features and existing GSU warder_channel/bitrate_worker before implementation; do not claim source-level parity from prior discussion alone. Integrate into existing Channel Information, not duplicate main-menu functions. Target: current service and tuner selection, SNR/AGC/BER/lock and supported dB, bounded history/min/max/mean, signal instability and lock-loss diagnostics, optional audio feedback for dish alignment, orbital position and transponder parameters (DVB-S/S2/S2X, MIS/PLS/T2-MI, DVB-T/T2/C/C2 only when supported), video/audio bitrate/PIDs/codecs/resolution, native tuning/scanning/blindscan and DiSEqC/USALS only through supported image APIs, compact quick signal view, optional local measurement export. No invented measurements or inferred unsupported capability; display unavailable explicitly. Read-only default; protect playback and recordings, require explicit confirmation for tuner retuning/motor movement/bouquet changes and preserve existing configuration. No conditional-access bypass. Reuse common sampling and graph widgets, cancel on close, 21 languages, all four resolutions, no GLES requirement. Compare sources and record actual feature coverage, tests and receiver limitations. Own implementation and UI; no third-party asset copying. Scope only, not implementation or verified parity.

---

# 2026-11-26 — Owner-approved functional assimilation of five reference products

Target stable 0.41.5, own implementations and UI, no copied third-party assets. Reference inventory (public documentation reviewed, not exhaustive source audit):
- E2 Doctor: https://www.linuxsat-support.com/thread/163145-e2-doctor/ — health score with check states and recommendations, image/Python/resources/network/tuner/mount/OPKG/EPG/picon/bouquet integrity checks, crashlog exception summaries, IPK metadata/dependency/script/architecture risk inspection, repair proposals and reversible actions where safe. Never delete files or modify configuration automatically; explicit confirmation, protected targets, validated backup/rollback before any supported mutation. No stale-lock removal without proving inactivity.
- Pulse Dashboard: https://www.linuxsat-support.com/thread/162383-pulse-dashboard/ — combined live hardware/signal telemetry, SNR/AGC, encryption type labels, active CAM, temperature sensor fallbacks, local network status, orbital position.
- MemOrganize: https://www.linuxsat-support.com/thread/162699-memorganize-is-a-smart-plugin-for-enigma2-receivers-to-manage-memory/ — readable grouped process names, per-process memory/CPU, flash directory analysis, swap details; investigate safe maintenance, never kill critical or unknown processes or drop caches automatically.
- CiefpSatelliteAnalyzer: https://github.com/ciefp/CiefpSatelliteAnalyzer — tuner selection and lock/SNR/AGC/BER history, signal logging, tuning, DiSEqC/USALS, multistream/T2MI and Abertis scanning, blindscan when native hardware supports it, bouquet preview/deduplication/import. Use native image APIs, explicit confirmation for tuning or writing bouquets, protect current playback/recordings and existing lists, no conditional-access bypass.
- LinuxSat Panel: https://github.com/OwnerPlugins/LinuxsatPanel — package-manager detection, installed inventory, approved source search, installation/update progress, release history, log viewer, LCN ordering and curated addon management. No untrusted arbitrary scripts, credential feeds or unauthorized CAM access. Warder projects retain canonical verified updaters; third-party catalog/install support requires verified provenance, integrity and compatibility.

Mandatory next step: compare actual source/runtime behavior against GSU feature by feature; mark existing/partial/missing/unsupported, source evidence, implementation module, tests, hardware limitations. Reuse the existing system/ECM/channel/CAM/swap/tools views; process and log full-width subsections; no duplicate modules or navigation. Implement safely in batches, with 21-language coverage, HD/FHD/WQHD/UHD, native compatibility and lifecycle tests. Aim for compressed IPK under 7 MB, measure actual size and installed footprint; target is not a verified limit. Keep r6 migration isolated. No public stable 0.41.5 until implemented and verified, no claim of full parity from documentation alone.

---

# 2026-11-26 — Approved UI modernization direction for GSU 0.41.5

Owner explicitly approved modernization of existing screens to current Warder Evolution standards, not merely adding six features. Preserve existing functionality, brand/logo/header, blue-cyan identity, PIG, remote-control usability, all 21 languages and HD/FHD/WQHD/UHD, without requiring GLES. Avoid duplicate functions. In particular, remove the two large Processes and System Log panels from the existing System Information overview and give each its own full-width detail view within the System Information section. Target navigation: Overview / Processes / System Log / Storage / Network / Live Monitoring. Overview uses reclaimed space for legible RAM, swap, root/flash, local disks, CPU load, temperatures, network/service status and health warnings. Processes: PID/name/state, scrolling, optionally measured CPU/RAM and sorting; read-only. Log: full-width scrolling, refresh, optional severity filter where reliable; no raw private logs in exported reports. Storage and network diagnostics must reuse the same views/data from any Tools shortcuts, not duplicate implementations. Live graphs use bounded history and stop sampling on close. Proposed navigation: left/right between sections, up/down for lists/scroll, yellow refresh, red back, OK detail; validate actual key bindings and preserve existing actions. Modernize main menu/right panel, channel/ECM/transponder/signal screens, CAM/OSCam/SRV and other legacy layouts consistently; preserve underlying actions and data. Use shared responsive layout components; verify long translations, native CI, lifecycle and receiver performance. This is an approved design direction, not implemented functionality. Keep technical r6 migration separate; deliver six features and UI modernization in stable 0.41.5.

---

# 2026-11-26 — GSU 0.41.5 feature scope approved by owner

Six features: expand existing System Health diagnostics, bounded live CPU/RAM/swap/temperature/network graphs, read-only storage analysis including picons, timed network diagnostics, Warder Evolution installed-project and update centre, and privacy-first diagnostic report export. Reuse warder_tools.py and warder_tools_ui.py rather than duplicate existing diagnostics. All user-facing strings in 21 languages; HD/FHD/WQHD/UHD, MIPS/ARM, no GLES dependency. Background workers must be bounded and UI callbacks ignored after close; no automatic deletion, configuration changes or upload; no credentials, raw configuration or private logs in new report. Project centre must use official feeds and preserve individual updater ownership. Develop independently from technical r6 bridge PR #15; integrate after verified r6 publication, then full CI, epoch migration and stable 0.41.5 publication, web SK/EN/DE/RU and registers. Existing releases/feeds unchanged. No feature implementation claimed yet.

---

# 2026-11-26 — stable r5 publication

PR #14, source `9e03199394ca498d30120cca5cf184752e0f1bbf`, workflow 45763722273, public IPK SHA-256 `17de1b2624dd90b77d2c8c05ceba997e683c2d66d888212dda21e31233ef7085`, 3812194 bytes. Both native matrices and packaged install gate passed. Feed activation via atomic fast-forward below; website verification remains pending.

---

# 2026-11-26 — GSU PR #14 stable candidate preparation

Source r5 version and explicit release request staged; 21 localized release notes and historical entries retained. New one-shot publisher: read-only PR package gates, native CI, deterministic IPK, actual r4 updater validator, public IPK and sidecar comparison, both stable feeds advanced atomically with no force, frozen r93 bridges unchanged. No release/feed advance has occurred. Exact HEAD requires all relevant CI before manual merge. Website sync after actual publication.

---

# 2026-11-26 — GSU PR #14 runtime-module checkpoint

Exact HEAD 65540c1562b37c8e6b1a2ccc8c1610c912376335 passed all 10 checks including independent AST inventory. Added seven additional CAM package, OSCam start, About and diagnostic bundle UI messages in all 21 languages; 174 common + 257 supplemental keys (431 total). Added placeholder equality regression for supplementary entries. English diagnostic archive summary remains machine-readable; no runtime behavior change. Stable r4 remains unchanged until publishing gates.

---

# 2026-11-26 — GSU PR #14 ninth legacy checkpoint

Added final 32 direct legacy help/operation strings in all 21 languages. 174 common + 250 supplementary keys (424 total), all regex-inventoried literal `_()` calls in plugin.py covered except 11 explicitly retained protocol/path/device identifiers. Added an independent AST regression for coverage; if it reveals additional literals, translate them before merge. Exact HEAD c55c6387894b5d98cbf7fdd76f5305c81561c2c3 passed 10/10 CI. Remaining: inspect AST result and other runtime modules, activate r5 source/notes, prepare safe production publishing, verify CI and public artifact/feeds. No stable feed change.

---

# 2026-11-26 — GSU PR #14 eighth legacy checkpoint

Added 38 real CAM, OSD, network mount and settings messages in 21 languages. 174 common + 218 supplementary keys (392 total); 43 remaining direct literal candidates include technical names and paths. Exact HEAD 90fdd87bf5c5c34a233084e9ec88a014fde0e049 passed 10/10 CI. No runtime behavior or stable feed change. New HEAD needs CI.

---

# 2026-11-26 — GSU PR #14 seventh legacy checkpoint

Added 43 actual OSCam/CAM errors, script results, update and other status/operation strings in all 21 languages. 174 common + 180 supplementary keys (354 total). 81 remaining direct literal candidates include protocol names and paths. Exact HEAD cd583b3baf5068fc6403736d7a61d33a72929b9c passed 10/10 CI. New HEAD requires CI. No runtime behavior, release or stable feed changes.

---

# 2026-11-26 — GSU PR #14 sixth legacy checkpoint

Added 27 actual debugging, numeric validation and filesystem help strings across all 21 languages. 174 common + 137 supplementary keys (311 total). Remaining 124 direct literal candidates include protocol identifiers and paths. Numeric size syntax, ECM/EMM/CW, I/O, IFD and filesystem names preserved. Prior HEAD 7a34f259c2b1c602210c38915e542c90f7514bff passed 10/10 CI; latest HEAD requires fresh CI. No release or production feed changes.

---

# 2026-11-26 — GSU PR #14 fifth legacy checkpoint

Added 32 real device, mount, filesystem, text editor and CAM/SRV menu labels in all 21 languages. 174 common + 110 supplementary keys (284 total); 151 remaining direct literal candidates, including technical identifiers. Previous HEAD `7a34f259c2b1c602210c38915e542c90f7514bff` had 7/10 CI success and 3 pending at review; no merge before full localization audit and fresh green CI. German/French Partition is a legitimate identical spelling. No release, feed or runtime behavior change.

---

# 2026-11-26 — GSU PR #14 fourth legacy checkpoint

Previous exact HEAD `08bc24baa927ceabf8006069aa5de1a936da0ea9` passed 10/10 CI. Added 20 legacy device-management, partition, path and CAM/SRV error messages in all 21 languages (78 supplementary keys, 174 common keys). Preserved existing translations, gettext precedence and runtime behavior. 183 previously inventoried direct literal candidates still need review; technical identifiers may be excluded. No r5 release or production feed change. Fresh CI required.

---

# 2026-11-26 — GSU PR #14 third legacy checkpoint

Previous HEAD `9f656a4373af26d0196783d221f94d4421a885cd` passed 10/10 CI. Added 30 further user-facing labels across 21 languages: device manager, expert settings, CAM search and client status. Supplement now 58 keys; common catalogues 174 keys. 203 remaining direct literal candidates, including technical identifiers. No release, feed, storage operation or CAM behavior changed.

---

# 2026-11-26 — GSU PR #14 second legacy checkpoint

Previous HEAD `6bfa300fdbcaad9ba733e94f4b3e32eeb5d75649` passed all 10 CI checks, including Python 3.9/3.14, OpenATV master/8.0/8.0-next, OpenPLi develop/release-9.2 and hooks. Added 20 further real legacy status/error/action strings to all 21 languages (28 supplementary keys total), including mount/unmount, partition creation/deletion, untrusted downloads and uninstall/OSCam restart. Existing translation precedence unchanged. Remaining legacy inventory 233 distinct raw literal candidates (includes technical terms and paths); review before release. No version or feed change.

---

# 2026-11-26 — GSU PR #14 checkpoint (not released)

Predecessor `49107d887dc71c80f916c419ad71b9c76a4a85e7`: 21 common JSON catalogues, 174 keys; previous CI 10/10 successful. Legacy direct translation-call inventory found 261 distinct literals absent from the common English JSON, including technical labels, mounting/partition warnings, CAM diagnostics and settings. This checkpoint adds eight high-priority destructive-operation and configuration warnings translated for all 21 languages in the packaged supplementary catalogue, preserving existing JSON and original gettext precedence. Remaining legacy strings still need review and translation; do not claim full UI coverage or activate r5 until reviewed and exact HEAD CI is green. Current stable 13.41-r4 SHA256 `48d8f90a6f1665f28e777b615f4dd25b1b8afc0b85128685965d44b66134acb2`; no changes to storage operations, settings, stable feed or release tag. No public TEST release.

---

## 26.11.2026 — Verified 174-key localization checkpoint

HEAD `a49ac47317af593d8a279f95933600059e4a95ac`: all 10 checks SUCCESS (Python 3.9/3.14 regression and layouts, OpenATV master/8.0-next/8.0, OpenPLi develop/release-9.2, hooks). All 21 catalogues contain the expanded 174 common keys. No remaining CI failure at this SHA. Legacy runtime label audit, activation of r5 version and localized release notes, and canonical stable publisher remain open. Existing v13.41-r4 and updater feeds unchanged. Do not merge incomplete draft #14.

## 26.11.2026 — Additional runtime messages

HEAD `816379658822e9a32a7d730c97065d31f58a83f9` completed all 10 CI checks successfully after schedule localization. Added 22 more shared messages in all 21 languages for CAM feeds, native startup, OSCam clients/readers and swap UI (174 common keys in total). Existing translations preserved. Fresh CI required. Legacy plugin.py audit remains open; no stable publication or feed change.

## 26.11.2026 — Night batch checkpoint, PR #14

HEAD `7d042eb63623c910f4d1467c58f82f3638cd3481`: 10/10 checks passed, including both Python regressions, both layout matrices, 5 native image checks and hooks. Corrected historical migration fixture notes using actual r93 history and version-independent package identity tests; no immutable IPK or feed touched. Expanded all 21 catalogues with 11 recurring schedule / weekday labels (152 shared keys), preserving existing values. Latest changes need fresh CI. Audit found many additional legacy strings in plugin.py (278 literal candidates before schedule additions), CAM feed, OSCam clients/readers and swap UI; do not merge until actual user-visible text is localized and verified. Next: complete those catalogues, activate version/notes and inspect canonical stable publication mechanism. Production v13.41-r4 remains intact.

## 26.11.2026 — CI checkpoint, draft PR #14

HEAD `9a8adcea7205ce210347272e4147f35740a7d9eb`: native OpenPLi 2/2 and OpenATV 3/3 SUCCESS; Python 3.9 and 3.14 now execute, but regression fails: Chinese month strings differed from numeric localized date and the historical migration-bridge build has r94-only release-notes substitution with current r4 metadata; test_package_identity.py also hardcodes r94. Corrected numeric Chinese months in this commit; bridge test/build fixture needs separate safe correction without touching immutable r93 or feeds. 21 translated r5 release notes staged separately, not activated. Remaining runtime labels and canonical stable publisher still pending. No release/merge permitted.

## 2026-11-26 — Owner-approved 21-language candidate (incomplete)

Base `b3ba187fa26d9167eaae6f5f1160abc64dcb9996`; production remains v13.41-r4. All eleven new 141-key JSON catalogues (nl, pt, ro, tr, al, el, et, lt, fa, uk, zh) staged, exact key/format-placeholder check performed before commit. Runtime language list expanded to 21 on this draft only, days/months and aliases integrated, update/history language selection normalized; new regression tests added. Existing Python 3.9 CI failed before running tests (ubuntu-latest = 26.04; Python 3.9 unavailable). Pin only Python matrix regression jobs to Ubuntu 22.04, keep native checks and both Python versions. Remaining: audit runtime labels outside the 141 common keys, calendar menu labels, release notes, version and safe publisher, all new CI and production verification. No release or feed change. Do not merge this partial draft.

## Current checkpoint — 2026-11-02: common stable release completed

Authoritative state: FullHDGlass **1.0.63**, GSU **13.41-r4**, PiconHub **0.1.40** are normal published releases and their live updater channels are active. Earlier publishing pauses and candidate-only statements below are historical and were superseded by the owner's explicit release authorization.

- Immutable public IPKs and SHA-256 sidecars were verified; sources, bundled histories, README and production records were updated.
- FullHDGlass main production and native TEST updater feeds offer the same verified 1.0.63 IPK. The main 1.0.18 migration bridge remains frozen.
- GSU original-python314 stable and PiconHub plugin/futuristic-rebuild stable feeds are active. GSU r93 identity bridges remain frozen; PiconHub 0.1.32 retains its documented one-time manual installation path.
- Existing settings, four PiconHub profiles, downloaded picons, managed CAM startup and deliberate user font sizes are preserved.
- Final public download checks and actual installed updater offer/parser checks are recorded in reports/common-stable/live-updater.json. These are host checks; exhaustive physical receiver/GLES/resolution coverage is not claimed.
- The three technical Slovak web descriptions supplied in chat are archived in each repository's docs/CURRENT-RELEASE.md. No separate website publication was performed.
- TEST preparation PRs were closed with stable-release references. No additional candidate or release is awaiting publication from this session.

FullHDGlass uses 1.0.63 rather than the initially planned 1.0.62 so package version ordering permits normal upgrades from 1.0.62-test6. Continue future development from current main and prepare new changes as separately versioned candidates; do not rebuild or overwrite the released IPKs.

Historical notes follow.

# Pending owner request — History: five entries — 1 November 2026

At the next normal release, expand the displayed History from the latest 4 entries to the latest 5 entries in all three projects: FullHDGlass, PiconHub and GSU. This instruction supersedes the earlier four-entry limit recorded below.

Keep the existing compact layout, version/date headings, separators, localization and brief user-facing descriptions. Preserve the complete source history; only the number of entries shown in the UI changes. Do not apply the limit to installation or processing output.

Record this as pending work only. Do not create a new IPK, bump a version or change update feeds solely for this request. Include and verify five visible entries when preparing the next authorized release.

---

# Current repair status — 31 October 2026

The four-entry localized History view and verified 13.20 installation repair are included in the new 13.40-r95 repair package. The release workflow and 393 tests passed; the original missing-file errors reproduce before the fix and disappear after it in real isolated opkg. Physical receiver retest of r95 remains pending. Existing r93 bridge and stable update feeds remain unchanged.

The following request is retained as a historical requirement, now implemented by this repair.

---

# Next release — History presentation

Status: required with the next functional fix or enhancement; no standalone IPK for this task.
Requested by the repository owner on 31 October 2026.

- Show only the latest 4 history entries in the plugin UI.
- Give every entry a clear version/date heading and a visible separator.
- Keep each description brief (at most 3 properly wrapped display lines), so the list fits cleanly on screen.
- Follow the active environment language for UI labels.
- Show only general user-facing changes; omit internal filenames, paths, implementation details, diagnostic/testing notes and working conversations.
- Preserve the full historical source and Git history; the limit applies only to the UI view.
- Preserve installer/result output and its existing actions; do not apply the 4-entry history limit to operational results.

Include this work when the plugin next changes. Check the history screen with long descriptions, language variants and the newest four entries before publishing that release.

## 2026-11-02 common stable release authorised

Owner resumed publication and explicitly requested all accumulated repairs as normal releases: FullHDGlass 1.0.63, GSU 13.41-r4, PiconHub 0.1.40. The earlier pause is superseded. Preserve settings and deliberately enlarged fonts. Source, public package checks, immutable releases and live update feeds are recorded by the common release workflow. See docs/COMMON-STABLE-20261102.md.

## Stable activation 2026-11-02

GSU 13.41-r4 published as a normal release; public IPK and checksum verified. Main metadata updated. Runtime updater branch activation is recorded separately after verification. Earlier TEST publishing pause is superseded by the owner’s explicit stable-release request.
