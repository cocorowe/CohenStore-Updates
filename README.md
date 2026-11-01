# CohenStore 0.5.17 TEST

Native PS4 testing-channel update, version code 517, APP_VER 01.17, signed updater revision 12. Title ID CHST00001 and the existing signing identity are unchanged. Published with the owner's explicit approval. **Physical PS4 testing of 0.5.17 is pending.**

[Download CohenStore 0.5.17 TEST PKG](update/packages/CohenStore-0.5.17-TEST.pkg)

## Update from CohenStore 0.5.16

Open Store Updates, press R3, then X. Wait for Update ready, close CohenStore, and install CohenStore-517.pkg from GoldHEN Package Installer using HDD /data/pkg. Reopen and confirm 0.5.17. The app does not install itself automatically. Keep a backup of /data/CohenStore and the known working 0.5.16 installer. Do not uninstall the store first.

## Changes

- Startup restores saved source indexes offline. Corrupt or missing caches use bundled fallback without erasing the original.
- L2 outside Mod Menus cycles Direct files / All listings / Grouped titles. Grouping uses exact linked_source_id matching; original sources remain available in All listings.
- Refresh preserves omitted record IDs, provenance and known newer local package versions. Settings changes preserve unknown fields. Corrupt queues and settings remain available for recovery.
- Package title/content identity checks when metadata supplies them, cached-package rechecks, occupied/zero-byte destination preservation and safe updater staging remain included.
- Settings: Quick-start downloads defaults ON. OFF requires X confirmation or Circle cancel. Browsing never starts downloads.
- In-app download notifications default ON and are independently toggleable. Queue progress and local rolling history are retained. These are not native OS notifications or proof of installation.
- Interface style offers Mint (default) / Console. Choose the style then Apply interface style. Both use the same catalog, downloads, favorites, search, L2 views and settings. Preferences are per installation, not per PS4 user. The Console layout is an early original four-tile design; advanced media caching/details remain future work.
- Auto-install is visibly unavailable and stays OFF. Verified PKGs retain the normal /data/pkg manual-install path.

## Catalogs and controls

All published catalog files remain unchanged. The package bundles the current 207 direct base entries and both full source indexes: 12,205 + 18,046 records. Combined feeds contain 32,901 records, including 2,638 direct-file records and 30,263 source references. These are not unique games or verified playable downloads. Creator/source listings, regions, versions, mods, patches and custom /data/FPKGi files are preserved. The Updates category includes XML gameplay patches, which are distinct from retail/FPKG update installers.

L1/R1 categories, Triangle search, Touchpad details/setup, Square queue, Circle pause, R2 cancel/remove in queue, X resume/retry, L3 favorite and R3 refresh are retained. Mod Menus retains its L2 type and R2 version filters. Source-only records cannot be queued. Game/mod compatibility must match the actual target version and CUSA.

## Validation and limits

152 application/native-simulation tests passed. OpenOrbis 0.5.4 / LLVM18 native compilation and PKG validation passed. The actual package's embedded SFO is APP_VER 01.17 with the original title/content identity. PKG size: 17,956,864 bytes. SHA256: cb0ae0ed7a3bc6f229df91914cb4826197820a82c9cd06e04de82387f80e1c23.

The standard Mint library screen matched the original desktop rendering pixel-for-pixel. A desktop benchmark loaded all 32,901 records, but host timings are not PS4 performance measurements. Firmware and GoldHEN versions for the owner's console remain unknown. Real startup, offline restore, L2 modes, queue/download behavior and optional layout/notification controls still require PS4 testing. Automatic installation and native system notifications are unfinished. No game, save, plugin configuration or console dependency is changed by publication.

Matching source, logs, checksums and recovery instructions are supplied privately. Private signing keys and source ZIPs are not added to this release. Historical public sources belong to older versions.

[Known 0.5.16 rollback installer](update/packages/CohenStore-0.5.16-CATALOG-EXPANSION.pkg). Preserve settings and user files. If GoldHEN refuses a downgrade, stop without uninstalling or deleting data. See [release validation](reports/release-0517.json).
