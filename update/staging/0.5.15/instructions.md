# CohenStore 0.5.15 Mod Menus & Cheats

Native PS4 application, version code 515, APP_VER 01.15, update revision 10. Title ID CHST00001 and the existing updater signing identity are retained. This updates CohenStore, not PS4 system firmware.

## Install
Open Store Updates, press R3 then X. Once ready, close CohenStore and install CohenStore-515.pkg using GoldHEN Package Installer (HDD). Reopen and confirm 0.5.15. The mod catalog is bundled for offline browsing and refreshes separately at catalog/mods.json. The existing games catalog and /data/FPKGi custom files are preserved.

## Mod Menus controls
- L2 cycles All, Menus, Cheats, Tools, Plugins and Payloads.
- R2 cycles All versions, 1.56 and 1.57 shortcuts. Search by game, CUSA-containing title, version or creator where listed.
- X downloads. Touchpad opens the full features/setup page.
- In that page, Touchpad installs a downloaded cheat file or enables/disables a downloaded game-specific menu. Circle returns.
- Menu enable checks CUSA and APP_VER in /system_data/priv/appmeta (including external games). Missing or mismatched metadata blocks enable. GoldHEN Plugin Loader must already be enabled. Close the game before switching; changes apply on the next game launch.
- Known store core menus for the same CUSA switch instead of stacking. Existing unknown plugins in the title or default section block enable instead of being deleted. Known utility plugin lines and other games are preserved. Configuration and replaced mod files receive separate backups.
- Cheats install as data in /data/GoldHEN/cheats/json. Select the exact CUSA/game version and enable cheats through GoldHEN in-game. An existing SHN/MC4 for the same target is kept and blocks conflicting JSON installation.
- Plugin ZIP bundles require manual extraction, or use the included PS4 Cheats Manager package for plugin and patch management. BIN payload downloading is supported only with a pinned hash and exact size. No automatic payload injection, firmware patches, or PC DLL/ASI execution is provided.

## Included content
5 real menu builds: Lotus for GTA V 1.27 and 1.48 (CUSA00419); Havana for RDR2 1.00 (upstream experimental), 1.29 and 1.32 (CUSA03041, documented target). Plus 1,542 pinned GoldHEN eboot JSON cheat files, an official GoldHEN plugin bundle, and PS4 Cheats Manager. Menu builds are not relabeled as compatible with GTA V 1.56. Velora, Explosive and other suggested names need actual creator releases and compatibility evidence before inclusion. Multiple core menus and PC asset conversions are not assumed safe.

The base catalog has 120 entries. One new Cyberpunk 2077 01.31 listing passed two public-mirror header, CUSA and exact-size probes; its complete 59.4 GB transfer and installation were not tested. Pegasus supplied 866 game rows, mostly duplicates. Goat Simulator 3 was private and excluded. The 17,065-row huggingfacer list consists primarily of hosting/shortener pages, not verified direct downloads. Ephellon provides store metadata; PSDevWiki's JSON page documents app version files. New import adapters preserve this distinction. No unverified mass import was published.

## Validation
117 app tests passed, including complete bundled mod-catalog navigation offline, filter/detail controls, backups, external game metadata, wrong-version rejection, switching, JSON identity checks, cancellation and legacy filename migration. Native PS4 compilation and PKG digest/signature checks passed. Full developer-release menu assets were downloaded and hashed; accepted cheat bytes matched the pinned upstream Git tree. A real Havana SPRX and Killzone JSON also completed through the app downloader and matched catalog hashes. New menu/cheat execution and system-folder access need PS4 testing.

## Source & rebuild
Current CohenStore source remains private; send the matching source ZIP with each installer. Never publish the signing key. Original upstream menus and tools remain hosted by their authors. Their download hashes provide transfer integrity, not a guarantee of game compatibility. See catalog/mod-sources.json, catalog/mod-audit.json and catalog/source-review.json for reproducible input and review records.

Build the desktop client and run tests with make test. Native builds use tools/build_ps4.py with OpenOrbis PS4 Toolchain 0.5.4, LLVM 18 and OpenSSL 1.1 compatibility libraries. Set OO_PS4_TOOLCHAIN and LLVM_BIN to your installed SDK/compiler paths; add the SDK packaging tool's OpenSSL library directory to LD_LIBRARY_PATH if required. All app and catalog sources needed to rebuild are included.

Launch-time official game update blocking remains deferred. No new standalone game-update/DLC packages were invented.
