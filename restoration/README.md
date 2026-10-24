# GSU 13.20 original-runtime recovery

This is the recovered original plugin, not the w20 replacement dashboards.
It is a receiver-validation candidate for OpenATV 8 / Python 3.14.7. Production source and its existing Releases are unchanged.

The supplied original IPK SHA256 is `81aea6eb25b5ed519e904af87a3d7bece5d32ae6886a1690dac8ab47306fe3f7`. Its Python 2.6 bytecode was decompiled with uncompyle6 3.9.3, then syntax-translated with Python 3.12 lib2to3. The original 2.6 and 3.12 bytecode inventories match: 574 code objects, including 62 classes and 510 named functions/methods. Names and argument counts are recorded in `original-inventory.json`; matching inventories do not prove behavioral equivalence.

`tools/recover_source.py` reproduces recovery from the original IPK. It corrects the decompiler's constant-list index/value bug before generation. `tools/port_source.py` records the compatibility edits. `generatePS.chck`, the internal retry closure in the old process-list shell loop, is superseded by a bounded procfs reader; no screen or user-facing feature is replaced with a placeholder.

Runtime changes are explicit: normal Python source instead of version-selected bytecode; current native text input; unicode/UTF-8 networking with bounded timeouts and a private authenticated opener; OSCam detection independent of the obsolete `/usr/UCM_CamSrv_bin` path; configuration discovery through its version file; native package-manager discovery; no copying incompatible libcrypto ABIs or replacing system binaries on import. Original helper executables are private resources selected by the receiver architecture. The newer original's blank blue main-menu caption is preserved.

The original SD/FHD/UHD skin definitions and original graphics/font/translations are retained. `resources.tar.gz` is a deterministic archive of the actual runtime assets, individually pinned by `resources.json`. Legacy Python cores, `/usr/bin/ftplib.py` and the old bytecode-selecting installer are not installed. Original default scripts and configuration templates are supplied only where the receiver has no existing file.

Build: `python3 restoration/tools/build_ipk.py`. The output is one deterministic `enigma2-plugin-glasssysutil_13.40-r7_all.ipk`. All runtime Python files compile under 3.14.7. Host tests exercise imports with native API doubles, all original signatures and main-menu contexts, and local OSCam configuration/authentication. They cannot validate real tuners, mounts, CAM restart, package operations or other receiver changes. Those remain unverified until tested on hardware. Original FTP services and legacy native helper ABI availability are external compatibility limits, not functionality verified by source recovery. This candidate is not published to automatic production updates.

The original AGC converter is retained under the unique `GSUAgcConv` name to avoid replacing another skin’s converter. Its progress value is an integer for the current native GUI API. Skin-file hashes verify that the converter reference is the only change to the original SD/FHD/UHD skin definitions.

## 13.40-r2: system information screen

Initial process and dmesg population and CPU timer startup now run after either native timer connection API. Yellow refresh reuses one timer and callback. Closing before the first layout refresh is safe. Two regression tests cover both signal APIs, refreshed content, timer reuse and early close. The original screen layout is unchanged. Receiver screenshots of r1 demonstrate the blank panels; r2 still needs receiver confirmation.

## 13.40-r3: channel information screen

Receiver validation confirms r2 process/dmesg panels, CPU display and independent scrolling. Channel initialization now continues after either native timer API for both bitrate and ECM timers; previously the fallback skipped all service metadata and picon loading. Satellite names retain Unicode, stream transfer text shows its rate rather than a service reference, and closing stops the pending bitrate timer. A regression exercises service/transponder fields, three picon assignments, the ECM callback and timer teardown with both APIs. Original screen definitions and artwork remain unchanged. Bitrate helper ABI and actual channel output still need receiver validation.

## 13.40-r4: channel row alignment and bitrate reads

ECM uses the current native label ellipsis mode (`eLabel.setWrap(2)`) to keep long CAM/version text within its row; the eleven values are normalized independently. CAIDs retain first-seen order without duplicates. Bitrate output is buffered across native dataAvail boundaries and consumes complete video/audio row pairs; tests cover fragmented and combined reads and repeated CAIDs. The first six helper output fragments and numeric PID/helper invocation metadata are recorded in `/tmp/gsu-bitrate.log` (no credentials or ECM data). This enables diagnosis if video remains zero: the legacy helper's actual video measurement is not proven fixed. The original SD/FHD/UHD skin files and artwork are unchanged.

## 13.40-r5: restore multiline ECM and replace legacy bitrate helper

Receiver evidence: the legacy ARM helper returns zero video and 186-191 kbit/s audio for valid PIDs 3001/3011 on demux 0. Native label ellipsis unexpectedly hid all but the first ECM row; use normal non-wrapping multiline rendering instead. The binary bitrate fallback is replaced by a standalone Python worker with Linux DVB `DMX_OUT_TSDEMUX_TAP`, independent read-only PID filters and 1 MiB buffers. This measures TS bytes including transport headers, rather than legacy PES bytes. Sampling uses monotonic time and nonblocking polling outside the GUI. Existing optional native BitrateViewer support is retained. Unit tests cover filter parameters, allocation failure, overflow, fragmented reads, statistics and cleanup. Actual support for this output mode and nonzero video are still awaiting the receiver test.

## 13.40-r6: independent low-latency audio sampling

Receiver evidence confirms r5 video and multiline ECM are working; audio arrives in bursts through TSDEMUX_TAP. Retain video TS filtering, but use DMX_OUT_TAP PES output for audio, matching the previously working original helper. Audio has a separate 64 KiB kernel buffer and 32 KiB read requests; video retains its 1 MiB buffer and 256 KiB reads. Statistics remain measured bytes per monotonic interval, with no synthetic smoothing or invented nonzero values. Tests verify that the main sampling loop selects different outputs and read sizes for video/audio. The diagnostic log intentionally retains only its first six output fragments; repeated cat calls do not restart the measurement. Hardware confirmation of audio behavior is pending.

## 13.40-r7: show full CAM build number

User confirmed r6 stable audio measurement. Increase the channel ECM values width from 292 to 340 px at FHD, scaled proportionally for SD/UHD, using the available gap before the picon. Increase this screen's ECM parser limit to 24 so the complete five-digit revision (e.g. 11966) survives its original version truncation. No smaller font or wrapping; original skin files remain intact. Layout test checks the larger column remains before the channel picon.
