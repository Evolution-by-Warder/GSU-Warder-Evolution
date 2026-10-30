# Installation package filenames

Publish exactly one IPK filename and its SHA-256 file per new native version:

`enigma2-plugin-extensions-gsu_VERSION_all.ipk`

The internal opkg Package identity, plugin-browser group, installed runtime, version and update-feed addresses remain unchanged. A filename cleanup does not require a new receiver IPK. Builds, release uploads and raw package staging use only the short filename; no native long alias is emitted.

The owner's 30 October 2026 cleanup removes only verified byte-identical long aliases and their checksum files. Short public files and all active update targets are verified before and after removal. Older migration packages remain available. PiconHub is excluded because its current updater still requires its long filename. Trezor is excluded and is not accessed.

Evidence: `reports/short-only-publication-20261030.json`.
