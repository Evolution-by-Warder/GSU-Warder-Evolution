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
