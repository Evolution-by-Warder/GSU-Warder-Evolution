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
