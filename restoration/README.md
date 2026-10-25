# GSU 13.20 original-runtime recovery

This is the recovered original plugin, not the w20 replacement dashboards.
It is a receiver-validation candidate for OpenATV 8 / Python 3.14.7. Production source and its existing Releases are unchanged.

The supplied original IPK SHA256 is `81aea6eb25b5ed519e904af87a3d7bece5d32ae6886a1690dac8ab47306fe3f7`. Its Python 2.6 bytecode was decompiled with uncompyle6 3.9.3, then syntax-translated with Python 3.12 lib2to3. The original 2.6 and 3.12 bytecode inventories match: 574 code objects, including 62 classes and 510 named functions/methods. Names and argument counts are recorded in `original-inventory.json`; matching inventories do not prove behavioral equivalence.

`tools/recover_source.py` reproduces recovery from the original IPK. It corrects the decompiler's constant-list index/value bug before generation. `tools/port_source.py` records the compatibility edits. `generatePS.chck`, the internal retry closure in the old process-list shell loop, is superseded by a bounded procfs reader; no screen or user-facing feature is replaced with a placeholder.

Runtime changes are explicit: normal Python source instead of version-selected bytecode; current native text input; unicode/UTF-8 networking with bounded timeouts and a private authenticated opener; OSCam detection independent of the obsolete `/usr/UCM_CamSrv_bin` path; configuration discovery through its version file; native package-manager discovery; no copying incompatible libcrypto ABIs or replacing system binaries on import. Original helper executables are private resources selected by the receiver architecture. The newer original's blank blue main-menu caption is preserved.

The original SD/FHD/UHD skin definitions and original graphics/font/translations are retained. `resources.tar.gz` is a deterministic archive of the actual runtime assets, individually pinned by `resources.json`. Legacy Python cores, `/usr/bin/ftplib.py` and the old bytecode-selecting installer are not installed. Original default scripts and configuration templates are supplied only where the receiver has no existing file.

Build: `python3 restoration/tools/build_ipk.py`. The output is one deterministic `enigma2-plugin-glasssysutil_13.40-r31_all.ipk`. All runtime Python files compile under 3.14.7. Host tests exercise imports with native API doubles, all original signatures and main-menu contexts, and local OSCam configuration/authentication. They cannot validate real tuners, mounts, CAM restart, package operations or other receiver changes. Those remain unverified until tested on hardware. Original FTP services and legacy native helper ABI availability are external compatibility limits, not functionality verified by source recovery. This candidate is not published to automatic production updates.

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

## 13.40-r15: installed CAM discovery, switching and package actions

The manager now discovers all matching executable softcam.* scripts and binaries, including stopped and unselected CAMs. It retains the image-selected CAM in the selection row even when stopped. Explicitly starting a different native CAM launches a separate Python worker: stop the previous one, atomically change the image SoftCAM symlink, then start the selected one. A failed new start restores the old selection and attempts to restart a previously running CAM; a failed stop never starts a second CAM. Expected-selection checks reject a stale request. Native process status is determined by /proc executable identity. Existing binaries and configuration files are not copied or removed. Returning from package operations refreshes the manager's native status.

Modern CAM packages now appear alongside original UCM packages in the uninstall list, while feed installers and OSCamStatus remain excluded. A running package-owned native CAM cannot be removed. Manual binaries such as the user's oscam-uni have no package to remove or update. For package-managed native OSCam selections the Update OSCam entry is enabled and uses the configured image feeds via opkg update && opkg install, with confirmation, stopped-CAM checks and no force flags. The old UCM command-line configuration editor remains disabled for native CAMs and is a separate unfinished compatibility item.

65 host tests pass, including all-installed discovery, package/manual distinction, stop/switch/start sequencing, failed-start restoration, failed-stop protection, changed selection, package-update confirmation, stopped/running uninstall checks and modern uninstall filtering. Recovery transformations reproduce the final plugin AST. Original skin files and artwork remain intact. New native switching, update and uninstall still require receiver confirmation.

Receiver evidence before this change: r14 successfully installed and configured oscam-master plus dependencies. The manager still showed only one CAM because it listed the current native selection only. The existing receiver feed targets OE 5.6 although enigma.info reports OE-Alliance 6.0; this release does not silently rewrite that existing feed or claim the compatibility mismatch resolved.

## 13.40-r16: ABI-matched SoftCAM feed and real package registration

Receiver diagnostics establish that the installed OE 5.6 OSCam-master binary requires libssl.so.3, while the image has OpenSSL 4.0.3 and reports OE-Alliance 6.0. Static inspection of the upstream packed binaries, after UPX decompression without execution, confirms OE 5.6/r3 needs libssl.so.3 and libcrypto.so.3; OE 6.0/r4 needs libssl.so.4 and libcrypto.so.4. Exact binary hashes, upstream blob IDs and DT_NEEDED records are in oscam-abi-evidence.json.

For the known updates.mynonpublic.com/oea provider, GSU now checks an existing feed against the current receiver's OE version and architecture. It verifies a matching CAM package in the new Packages.gz index, retains the original configuration in a .warder-backup sidecar and atomically changes only that source URL. Custom providers are preserved. A pending-refresh marker prevents incompatible cached lists being shown if refresh fails, including after reopening the screen. Both CAM catalogue loading and native OSCam updating prepare the feed off the GUI thread. No ABI symlinks, copied libraries or arbitrary compatibility binaries are introduced. The installed old CAM is upgraded separately through the normal package confirmation workflow.

Native CAM package registration now comes from opkg list-installed in a background worker, with a finite timeout and a GUI-side cache. This fixes the receiver's package_for(None) result caused by assuming particular opkg .list locations. Running native CAM removal is also guarded by the exact CAM/package name mapping when metadata files are absent. 73 host tests pass. Receiver verification of the migrated feed, the replacement OSCam binary and the update controls is still pending. Native command-line configuration editing and the minor download-list visual/translation issues remain separate unfinished items.

## 13.40-r17: ignore terminated CAM processes in update checks

Read process State as well as comm before blocking an OSCam/OSEmu update. Zombie and dead entries do not represent a running CAM; live processes still block. Reproduced with the receiver live-parent/zombie-child evidence and covered by 76 host tests. Native shutdown with a missing PID file remains a separate receiver issue; this release does not add forced termination.

## 13.40-r18: verified native CAM shutdown and restart

Native stop/restart now run in the asynchronous command worker. After the original init stop script (20s timeout), wait up to 2s for actual termination; then target only the selected executable with SIGTERM, wait 2s and use SIGKILL only if it survives, with 1s final verification. Process starttime is checked before signalling and pidfd is used on supported kernels. Zombie/dead entries are ignored. Switching CAMs uses the same verified shutdown before changing selection. No package init scripts, binary files, PID files or CAM configurations are rewritten.

82 Python3.14.7 host tests pass, including real harmless Linux processes for both graceful and forced shutdown without a PID file, and a separate executable left running. These tests do not replace receiver confirmation. Receiver r17 confirms successful update workflow with no package changes and subsequent oscam-master start.

## 13.40-r19: ECM Info in the native long-INFO menu

Register GSU – ECM Info through PluginDescriptor.WHERE_EVENTINFO and open the original ECMInfo screen on selection. The entry is available independently of the legacy color-shortcut setting. Existing short-INFO, long-INFO menu and color-button mappings are preserved; no image keymaps or native event handlers are rewritten. The proposed red-button fallback was not shipped: the user chose the native INFO menu.

84 Python3.14.7 host tests pass, including descriptor registration with color shortcuts enabled/disabled and the real callback. Receiver r18 now confirms stop/start/restart, running-CAM removal protection, removal and reinstall with config preservation. Native delayed startup, automatic recovery and SRV runtime operations are still unverified; native OSCam start-configuration editing remains disabled.

## 13.40-r20: consolidate quick GSU access in Extensions

Move (GSU) ECM Info to the existing Extensions menu (long blue on the validated receiver), alongside the five other GSU entries. Remove its long-INFO registration and retire the old global red/green shortcut hook and manager setting. Remaining CAM manager rows move into the removed row's exact positions at SD/FHD/UHD. The installed keymap retains original UCMActions and omits the retired GSUmain context. Old par40 settings remain readable but have no effect; retained original shortcut function signatures are intentional no-ops. Existing image INFO and color mappings are untouched.

88 Python3.14.7 host tests pass. Tests cover native menu registration, the actual ECMInfo callback, no global InfoBar modification with an old enabled setting, menu traversal without the removed item and all three layouts. Runtime AST matches the reproducible source transformation. Receiver r19 confirmed ECMInfo display; the consolidation in r20 remains to be tested.

## 13.40-r21: native OSCam start configuration

Enable start settings for native OSCam candidates, including manually installed binaries. Probe that executable's --help and inspect its native init command in a worker. The original-style editor uses per-CAM values, actual configuration/temp directories, debug mask, restart level, clock wait, pending ECM limit and supported diagnostics. Unsupported options stay hidden. Native daemon and PID-file ownership remain fixed so the image service can still manage the CAM.

Saving records options in /etc/enigma2/gsu-softcam-start/NAME.json and keeps the first original init script as NAME.init-backup. Only the executable invocation in a recognized native init script is prefixed with the stdlib argv adapter; shell expansions, other commands and unknown native arguments remain intact. Values become argv, never shell text. The CAM keeps running until an explicit start/restart. Unsupported scripts or stale editor snapshots fail without overwriting the init script. Config/card/server files are untouched.

Native GSU start/restart reapplies a saved adapter if a package update restored the init script. External package operations can temporarily use their own default start arguments until this reapplication; this is not a claim of image-wide update integration. The IPK removal hook restores managed invocation prefixes before removing GSU. Old UCM editing remains available for legacy entries.

102 Python3.14.7 host tests pass, including real harmless shell-to-adapter-to-argv-recorder execution, per-CAM isolation, cancel, error rollback, script replacement and uninstall cleanup. Runtime AST matches the scoped port transformation. Receiver validation of r21 is pending. The CAM/SRV section remains active until native boot delay, autocheck, SRV and the legacy experimental-image entry are resolved.

## 13.40-r22: fix native start editor opening on OpenATV

Use a bound onLayoutFinish method: OpenATV passes other callback objects to exec(), so the original lambda caused a TypeError before the editor opened. Rename the settings collector from values() to collect_values() to preserve Screen's component enumeration during execBegin/show/hide. Two regression tests cover those actual receiver API contracts. 104 Python3.14.7 host tests pass; receiver opening still needs confirmation. The r21 receiver error happened before any user save.


## 13.40-r23: delayed native CAM startup

Receiver r22 screenshots confirm native startup editor opens, saves original values and oscam-master restarts with ECM recovery. Changed-option propagation and cancel persistence remain separate checks. A native session timer now uses the configured 1–30 second delay, with both Enigma timer signal APIs. The worker checks the original selection again and only starts a missing CAM; an already running CAM or another running native CAM is left alone. Image boot service configuration is unchanged: an image-started CAM may already be running before the timer expires. GUI shutdown cancels a pending timer. Mount checks remain independent. The bounded diagnostic log `/tmp/gsu-softcam-autostart.log` records monotonic timestamps, scheduling, skips and worker results. Native autocheck/recovery, separate SRV and experimental image preparation remain pending. The legacy UCM startup branch is not newly validated by this change.


## 13.40-r24: native CAM process autocheck

Receiver r23 logs verify both cases: already running master is skipped about 10.6 seconds after scheduling; stopped master is started about 10.6 seconds after scheduling and verified with worker code0. r24 connects par50 to a separate 600-second timer. The switch takes effect immediately. Each check runs in a worker and revalidates selection and actual executable identity. It starts a missing selected native CAM, leaves running CAMs alone, and does not use ECM or channel decoding as a health criterion. A failed attempt is retried at the next normal interval. Manual GSU stop suspends recovery for that CAM until successful manual start/restart or a new GUI session. Failed manual stop restores the previous monitoring state. Guard tokens cancel queued automatic requests after manual commands or shutdown; disabling autocheck cancels queued periodic requests while preserving initial startup. A worker-only file lock serializes GSU native operations. External service stops cannot be identified as manual GSU stops and may be recovered when monitoring is enabled. Runtime recovery remains receiver-unverified. Separate SRV and legacy UCM startup are not newly validated.


## 13.40-r25: faster native recovery

Receiver r24 logs confirm periodic running-CAM skip, recovery of an externally stopped master, and suppression after manual GSU stop across two complete 600-second cycles. At the user's request, native monitoring now checks every15 seconds after initial startup completes. A failed worker increases the retry interval to30,60,120,240 and at most300 seconds; a successful result resets it to15 seconds. Manual intervention, a new selection and reconfiguration also reset the failure delay. A cancelled worker's late completion cannot impose a delay on newer manual intent. Periodic checks cannot bypass a configured initial30-second startup delay. The native CAM help text now describes15 seconds, including Slovak fallback; the legacy UCM help remains unchanged. 128 Python3.14.7 host tests pass. New interval/backoff behavior still requires receiver validation.


## 13.40-r26: conditional standalone server controls

Receiver r25 confirms15-second recovery, subsequent running-CAM skip, intentional GUI-stop suppression, and successful manual restart with ECM restoration. User approved hiding standalone SRV controls unless a supported local server is detected. The manager now lists only the CAM row when no valid UCM standalone server is installed, hides its status and second-row arrows, skips the SRV restart action and compacts the right-side options. Captions use CAM in that case. Original SRV handling and saved settings are retained. Refreshing after installation/removal restores/hides controls without a GUI restart. Discovery reads the existing UCM script's literal SrvBin name, requires an executable script and binary, and does not execute either; missing binaries, backup filenames, dynamic paths and external script aliases do not qualify. This detects the existing supported UCM server format, not arbitrary network peers or every image's cardserver implementation. Original SD/FHD/UHD asset files remain unchanged. 135 host tests pass; SRV display on the receiver and actual server operation remain unverified because none is installed there.


## 13.40-r27: remove obsolete experimental-image preparation

Receiver r26 screenshot092425 confirms CAM-only captions, no empty standalone-server row/status/restart, and a running OSCam with ECM data. User explicitly requested complete removal of experimental-image preparation after its behavior was explained. The manager no longer contains that widget, help entry, action, initialization probes or control flag. The three original methods killDccamd, doLnk and chckDccamd are deleted, including their dccamd removal/service/package commands and boot-script/symlink mutation code. Runtime skin compaction removes the obsolete row at SD/FHD/UHD, and navigation wraps after autocheck. The immutable original inventory remains historical evidence; tests explicitly allow only these three newly authorized method removals and continue checking the remaining original signatures. 136 Python3.14.7 host tests pass. r27 receiver display still needs confirmation; standalone SRV runtime remains untested because none is installed.


## 13.40-r28: restore OSD ECM and CAM state indicator

Receiver r27 screenshots093241/093350/093351 confirm obsolete image preparation is gone, navigation wraps from autocheck to Exit, the15-second help is visible and OSCam/ECM remain active. User wants to evaluate the original OSD ECM overlay before deciding its value and explicitly authorized restoration. Recovered OSD parsing was unreachable after a return, leaving fields uninitialized when a file changed; parsing now runs before change detection. Static and scrolling branches and unsupported-CA handling are repaired, static widgets exist with either timer API, and current native labels retain multiline values. Time thresholds use the parser's normalized seconds converted to milliseconds. Channel end/disable clears state and stops timers, and FTA does not display stale encrypted-channel ECM. Position selection stops its timer on either exit and clamps to actual screen dimensions. Save/cancel cover options even when hidden after disabling the feature. Original OSD type-change GUI restart remains.

The existing CAM state icon now uses green for a running CAM and red for a stopped CAM at initialization and command completion. While the manager is open, its existing timer requests a bounded-rate background process-state sample to reflect automatic/external state changes. It does not scan processes on each GUI tick or redraw unchanged state; stale results after manual actions or close are ignored. 149 host tests pass. OSD behavior and colors require receiver validation; no claim of real display correctness is made from host tests.


## 13.40-r29: readable scrolling ECM strip

Receiver r28 screenshots100013 confirm scrolling OSD is visible in settings, CAM manager and normal television; the running-CAM status icon is green. User finds the original306px Full HD strip too narrow. The scrolling overlay and position preview now share a responsive half-screen width:640px at1280,960px at1920 and1920px at3840. Font, height, scroll speed and data are unchanged. Native rectangles reproduce the thin blue frame without stretching its bitmap border. Display coordinates are clamped to the real window/screen dimensions without silently saving user settings; the position editor uses the visible clamped coordinates. Static mode is unchanged apart from the shared bounds check. 152 host tests pass; wide-strip appearance and static mode still need receiver confirmation.


## 13.40-r30: inset the scrolling strip's right edge

Receiver r29 screenshot101012 shows the wide scrolling strip ending flush with the screen edge. User accepts the wider display and requests shortening only on the right. The strip is now60px shorter at1920px, leaving a60px right inset at its previous clamped left position; the same ratio gives40px at1280 and120px at3840. Overlay placement and the position editor enforce the same right bound. Static mode retains its prior bounds. Font, height, data and speed are unchanged. 152 host tests pass; the inset remains receiver-unverified.

## 13.40-r31: responsive swap file management

Preserves the original swap screens. Disk discovery, file allocation, mkswap, swapon and swapoff run in a worker. Operations check return codes and the actual active swap table. Creation uses exclusive private files, validates mounted writable local ext2/ext3/ext4/XFS storage under /media and free space, and rolls back failed activation/configuration. The delete action refuses swap partitions, captures the confirmed file, verifies swapoff, and removes only its exact swap entry from fstab. Failed configuration or unlink attempts preserve/restore the file and active state where possible. fstab updates are atomic and reject observed concurrent changes; overlapping GSU swap mutations are locked. Network, read-only and other filesystem types are not offered. Existing swap entries remain visible, including partitions.

Receiver evidence closes the OSD ECM section: scrolling inset accepted, static panel displays ECM, user-positioned panel survives GUI restart, and disabling removes it. No fixed right-side placement is imposed. Receiver swap screenshots confirm two active 256 MB entries (partition and HDD file), the original editor opens and offers None or /media/hdd. The r31 worker operations still require real receiver create/delete validation.
