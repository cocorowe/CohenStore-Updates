# CohenStore 0.5.16

Native PS4 store update: version code 516, APP_VER 01.16, signed feed revision 11. Title ID CHST00001 and the installed updater signing identity are retained.

## Install

Open Store Updates, press R3, then X. Wait for Update ready, close CohenStore, and install CohenStore-516.pkg using GoldHEN Package Installer from HDD (/data/pkg). Reopen and confirm 0.5.16, then press R3 in a browsing tab to load the expanded catalogs. Your existing /data/FPKGi files and download queue are preserved.

## Browse and download

- L1/R1 changes category. Triangle searches names, CUSA, versions and creators.
- Outside Mod Menus, L2 switches Direct files / All listings. R2 jumps ahead 40 rows. Holding D-pad repeats navigation.
- Mod Menus retains L2 type filters and R2 version filters. Touchpad opens full setup/source details in all browsing categories.
- X downloads direct files. Source-page records show their original URL and cannot enter the download queue. Those pages may require separate manual steps, accounts or payment.
- Square opens the queue. Select an entry and use R2 to cancel/remove it. Circle pauses; X retries supported failed/paused entries.

## What is included

The combined feeds contain 32,817 records, including game variants and metadata/source pages. They are not 32,817 unique games or working PKGs. There are 2,554 direct-file records and 30,263 source references across the categories. The existing direct base catalog has 123 entries.

Mod Menus contains 2,049 records: 1,929 cheat variants, 89 patch variants, 16 menu entries, 10 legacy payload builds, one plugin bundle and four tools/source records. Seven of the 16 menu entries have creator release files; nine link to creator sources. New files include Silent Virtues for RDR1 and Atian's BO4 script. RAR/GSCC/BIN/BZ2 downloads require the creator's matching manual setup; downloading does not inject or execute them. No newly verified GTA V 1.56 native menu was found. Existing Lotus builds retain their actual supported versions.

The Updates category now includes 386 CUSA-specific XML game-patch variants from the maintained PS-Game-Patch project. These are optional patch data, not retail game-update PKGs. Select the exact CUSA/version. Touchpad in Details can copy a downloaded patch to /data/GoldHEN/patches/xml, with backups and identity checks. PS4 Cheats Manager/game_patch handles activation; patches are not enabled automatically.

New creator packages include Crema, Dolphin, HENkaku, M33, Resonance, Payload Guest and Shattered Pixel Dungeon; PS4Vibe is supplied by its public homebrew host. Other app, homebrew and emulator pages are labeled as sources. DLC has five source records and no new verified direct package.

The Ephellon, huggingfacer, Pegasus and previously supplied catalogs are represented according to their content. Hosting pages and store purchase links are kept distinct from download files. Custom FPKGi JSONs remain supported. Only four visible cards are copied per frame, with cached filtering, so the expanded index is not scanned/copied every frame.

## Download checks

112 backup Archive URLs were added without removing existing listings. All 204 examined mirror endpoints passed a 128-byte PKG header, content ID, exact-size and HTTP-range probe. A passing probe is not a complete transfer test or a speed guarantee; hosts can change or become unavailable.

Creator mod files have pinned sizes and SHA-256 hashes. Source-cheat and patch data was checked against captured Git trees. The real app downloader completed the Silent Virtues RAR, ArabicGuy compressed payload and an AER XML patch with matching hashes. New homebrew packages passed header/identity/size checks; their complete installation and execution were not tested.

## Validation and limits

124 app tests and 18 repository tests passed. Tests cover large cached indexes, source-only queue rejection, mod data formats, patch backup/CUSA checks and existing cancel/retry/update behavior. Native compilation and PKG digest/signature validation passed. New browsing performance, mod setup and patch behavior still need testing on a real PS4. Launch-time official game update blocking remains deferred.

## Private source and rebuild

The matching source ZIP is provided privately with every release. The public repository contains the compiled installer, signed feed, catalogs and validation tooling. Never publish the updater signing key. Upstream menus and tools remain attributed to their creators; a file hash verifies transfer integrity and does not prove game compatibility.

Build the desktop client with make and run make test. For PS4, use tools/build_ps4.py with OpenOrbis PS4 Toolchain 0.5.4 and LLVM 18. Set OO_PS4_TOOLCHAIN and LLVM_BIN to the installed paths; add the packaging tool's OpenSSL 1.1 compatibility libraries to LD_LIBRARY_PATH if needed. See catalog/expansion-audit.json, catalog/mod-sources.json and tools/build_catalog_expansion.py for input and validation records. The generator's --inputs directory contains external research snapshots; the generated catalogs and app build sources are included in the ZIP.
