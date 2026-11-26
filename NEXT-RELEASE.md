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
