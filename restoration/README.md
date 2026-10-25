# GSU 13.20 original-runtime recovery

This is the recovered original plugin, not the w20 replacement dashboards.
It is a receiver-validation candidate for OpenATV 8 / Python 3.14.7. Production source and its existing Releases are unchanged.

The supplied original IPK SHA256 is `81aea6eb25b5ed519e904af87a3d7bece5d32ae6886a1690dac8ab47306fe3f7`. Its Python 2.6 bytecode was decompiled with uncompyle6 3.9.3, then syntax-translated with Python 3.12 lib2to3. The original 2.6 and 3.12 bytecode inventories match: 574 code objects, including 62 classes and 510 named functions/methods. Names and argument counts are recorded in `original-inventory.json`; matching inventories do not prove behavioral equivalence.

`tools/recover_source.py` reproduces recovery from the original IPK. It corrects the decompiler's constant-list index/value bug before generation. `tools/port_source.py` records the compatibility edits. `generatePS.chck`, the internal retry closure in the old process-list shell loop, is superseded by a bounded procfs reader; no screen or user-facing feature is replaced with a placeholder.

Runtime changes are explicit: normal Python source instead of version-selected bytecode; current native text input; unicode/UTF-8 networking with bounded timeouts and a private authenticated opener; OSCam detection independent of the obsolete `/usr/UCM_CamSrv_bin` path; configuration discovery through its version file; native package-manager discovery; no copying incompatible libcrypto ABIs or replacing system binaries on import. Original helper executables are private resources selected by the receiver architecture. The newer original's blank blue main-menu caption is preserved.

The original SD/FHD/UHD skin definitions and original graphics/font/translations are retained. `resources.tar.gz` is a deterministic archive of the actual runtime assets, individually pinned by `resources.json`. Legacy Python cores, `/usr/bin/ftplib.py` and the old bytecode-selecting installer are not installed. Original default scripts and configuration templates are supplied only where the receiver has no existing file.

Build: `python3 restoration/tools/build_ipk.py`. The output is one deterministic `enigma2-plugin-glasssysutil_13.40-r14_all.ipk`. All runtime Python files compile under 3.14.7. Host tests exercise imports with native API doubles, all original signatures and main-menu contexts, and local OSCam configuration/authentication. They cannot validate real tuners, mounts, CAM restart, package operations or other receiver changes. Those remain unverified until tested on hardware. Original FTP services and legacy native helper ABI availability are external compatibility limits, not functionality verified by source recovery. This candidate is not published to automatic production updates.

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

## 13.40-r8: CCcam WebInfo text compatibility

Replace every original CCcam urlopen call with a private bounded transport that supplies Unicode text to the existing screen parsers. It removes userinfo from request URLs, handles Basic/Digest authentication without changing the global opener, enforces a four-second timeout and 4 MiB response limit, and closes network responses before returning a StringIO. Unreachable configured servers remain visible and unavailable instead of disappearing. Tests include an actual local authenticated HTTP server, all eight original CCcam menu entries, and an unavailable configured server. Receiver use requires a running local CCcam WebInfo or configured reachable remote WebInfo endpoint; OSCam alone does not provide CCcam WebInfo. Real CCcam data and config-changing actions remain unverified. Original appearance is retained.

## 13.40-r9: OSCam reader-table columns

Read modern HTML reader rows by `readercol` cell classes rather than positional offsets. Protocol comes from the protocol icon title; nested status/IP text is joined with spaces, and EMM counters map explicitly to columns 7-10. Preserve the legacy parser for pages without classed reader rows. The existing selection record retains the real protocol for entitlements eligibility. Tests cover icon metadata, nested tags/entities, HTML reflow, disabled entries, distinct counters and the actual screen integration. Primary markup reference: https://github.com/gfto/oscam/blob/master/webif/readers/readers_readerlist.html and readerctypbit.html. Original screen geometry/artwork retained; list text uses the available row width. User receiver verification pending. Includes the r8 CCcam transport work, which was not separately installed on the receiver.

## 13.40-r10: exact 11968 receiver markup

The supplied receiver HTML establishes that status/address is readercol20, protocol is the readercol2 data-sort-value, and the added TOUT column moves the two-value Filtered counter to readercol7 and EMM error/written/skipped/blocked to readercol8-11. Read these correctly while retaining the older four-value readercol7 layout. A sanitized four-row fixture derived from the actual page validates exact counters for local/upstream readers, disabled status, protocol metadata, status/address spacing and HTML reflow. Only the sanitized table rows are committed, not the supplied full WebIf page. Receiver confirmation pending.

## Receiver checkpoint — 2026-10-24 evening

The r10 Readers screen is now confirmed on the receiver. Detailed partial validation, remaining limits and the exact next step are recorded in [TESTOVANIE.md](TESTOVANIE.md). Resume at standalone ECM Information: confirm live ECM Time refresh, fix its still-truncated five-digit CAM revision, then continue with CAM/SRV. This documentation checkpoint does not change the runtime or issue another IPK.

## 13.40-r11: standalone ECM full CAM revision

Use the same 24-character parser limit as Channel Information in the standalone ECM Information screen, retaining the full five-digit CAM build in its existing value column. No skin geometry or artwork changes. A regression covers both native timer APIs, initial encrypted-service population, thirteen rows, a changed ECM Time on the next callback, five-second timer rearming and stopping on close. 28 host tests pass; live refresh and the revised display still require receiver confirmation.

## 13.40-r12: OpenATV selected SoftCAM support

The original CAM manager now lists the image-selected `/etc/init.d/softcam` target (confirmed receiver target: softcam.oscam-uni). It detects the running binary by its actual `/proc/PID/exe`, and invokes the existing init script asynchronously for start, stop or restart. Completion checks both the exit status and actual process state. It never changes the image SoftCAM selection or writes legacy UCM status files. The native entry covers the currently selected SoftCAM; switching among other native packages remains the image manager’s responsibility. Existing UCM entries and original screen geometry remain intact. Repeated broadcast CAIDs are deduplicated in original order. 37 host tests cover discovery, invalid targets, executable identity, all three callback API forms, command failures, lifecycle controls, legacy conflict handling and original screen integration. Receiver confirmation of r12 detection and controls is pending.

Receiver screenshots confirm r11 full CAM revision 11968 and live ECM Time changes (0.110, 0.108, 0.107).

## 13.40-r13: image package feeds replace the legacy CAM FTP

Download CAM/SRV now reuses the original list screen for CAM packages from the receiver's configured opkg feeds. Feed refresh and catalogue parsing run in a background worker with finite 45/15-second subprocess timeouts; closing the screen ignores late results. No feed URL or installer is added by GSU. Failed refresh can show the cached catalogue with an explicit warning. Empty/error rows cannot install anything. The package name and available versions are shown; installation requires confirmation and uses plain opkg install without force-overwrite/downgrade. Stop OSCam before selecting an OSCam package, as the original workflow required. After installation the cached catalogue is reloaded without another feed refresh. Images without opkg show an unavailable catalogue rather than using another guessed source.

The historical FTP endpoint and bundled credentials are removed from the runtime. Other old plugin/OSCam FTP updater callers receive a disabled-source explanation; those updater entries are not claimed to use the new CAM catalogue yet. The native completion callback also updates the secondary running/stopped status label. 47 host tests pass. The new feed listing and actual package installation still need receiver validation.

Receiver reports describe a web redirect and adware warning. DNS lookup on 2026-10-25 returned ns11/ns12.abovedomains.com, picons A 103.224.182.242, and ww17 CNAME 11490.searchmagnified.com. These support a parking inference, not proof of ownership change or malware. Direct TCP/21 probing was blocked by this execution environment (Network is unreachable); no banner or FTP contents were obtained and no historical credentials were used. OpenATV documents SoftCAM packages as an external feed: https://openatv.github.io/enigma2-doku/en/entschluesselung/softcam-feed/ . GSU delegates source selection to the image's existing package-manager configuration.

## 13.40-r14: clean-image feed setup for each receiver

When Download CAM/SRV first refreshes the catalogue, GSU reuses an already configured SoftCAM feed. If none exists, it reads distro, OE-Alliance version and package architecture from /usr/lib/enigma.info and adds exactly one configuration file using the supplied softcam-feed-universal 4.8-r0 feed scheme. It does not install or execute that old IPK, remove old feeds/CAM files, change SoftCAM selection, or start a CAM. Configuration publication is atomic and does not overwrite existing files. Unsupported/unknown metadata fails clearly without guessing a machine architecture. The provider's cortexa7hf -> cortexa7hf-vfp mapping is retained. No receiver model is hardcoded.

The user's receiver confirms openatv / OE-Alliance 6.0 / cortexa15hf-neon-vfpv4. The corresponding upstream directory exists; other receivers derive their own version and architecture. Tests exercise aarch64, mips32el, sh4 and multiple ARM variants, unknown/injected metadata, first setup, subsequent reuse and preservation of unrelated configuration. 54 host tests pass. Actual initial setup on a clean receiver and the new package catalogue remain unverified on hardware.

Inspected input IPK SHA256: 35aa75731d36192402093631bfd6cd2b4b2ef0f5494f1f8eac4d538bc4d63e81. Upstream: https://github.com/SusanOV/softcamfeed . The external feed remains operated by its own supplier; GSU does not describe it as packages supplied by OpenATV itself.
