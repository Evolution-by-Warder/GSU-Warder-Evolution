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
