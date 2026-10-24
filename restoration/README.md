# GSU 13.20 original-runtime recovery

This is the recovered original plugin, not the w20 replacement dashboards.
It is a receiver-validation candidate for OpenATV 8 / Python 3.14.7. Production source and its existing Releases are unchanged.

The supplied original IPK SHA256 is `81aea6eb25b5ed519e904af87a3d7bece5d32ae6886a1690dac8ab47306fe3f7`. Its Python 2.6 bytecode was decompiled with uncompyle6 3.9.3, then syntax-translated with Python 3.12 lib2to3. The original 2.6 and 3.12 bytecode inventories match: 574 code objects, including 62 classes and 510 named functions/methods. Names and argument counts are recorded in `original-inventory.json`; matching inventories do not prove behavioral equivalence.

`tools/recover_source.py` reproduces recovery from the original IPK. It corrects the decompiler's constant-list index/value bug before generation. `tools/port_source.py` records the compatibility edits. `generatePS.chck`, the internal retry closure in the old process-list shell loop, is superseded by a bounded procfs reader; no screen or user-facing feature is replaced with a placeholder.

Runtime changes are explicit: normal Python source instead of version-selected bytecode; current native text input; unicode/UTF-8 networking with bounded timeouts and a private authenticated opener; OSCam detection independent of the obsolete `/usr/UCM_CamSrv_bin` path; configuration discovery through its version file; native package-manager discovery; no copying incompatible libcrypto ABIs or replacing system binaries on import. Original helper executables are private resources selected by the receiver architecture. The newer original's blank blue main-menu caption is preserved.

The original SD/FHD/UHD skin definitions and original graphics/font/translations are retained. `resources.tar.gz` is a deterministic archive of the actual runtime assets, individually pinned by `resources.json`. Legacy Python cores, `/usr/bin/ftplib.py` and the old bytecode-selecting installer are not installed. Original default scripts and configuration templates are supplied only where the receiver has no existing file.

Build: `python3 restoration/tools/build_ipk.py`. The output is one deterministic `enigma2-plugin-glasssysutil_13.40-r1_all.ipk`. All runtime Python files compile under 3.14.7. Host tests exercise imports with native API doubles, all original signatures and main-menu contexts, and local OSCam configuration/authentication. They cannot validate real tuners, mounts, CAM restart, package operations or other receiver changes. Those remain unverified until tested on hardware. Original FTP services and legacy native helper ABI availability are external compatibility limits, not functionality verified by source recovery. This candidate is not published to automatic production updates.

The original AGC converter is retained under the unique `GSUAgcConv` name to avoid replacing another skin’s converter. Its progress value is an integer for the current native GUI API. Skin-file hashes verify that the converter reference is the only change to the original SD/FHD/UHD skin definitions.
