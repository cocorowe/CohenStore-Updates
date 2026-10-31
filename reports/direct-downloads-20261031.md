# Direct homebrew download additions

This catalog-only proposal follows the approved merge of PR #2. It adds actual PKG URLs to the existing base catalog used by CohenStore 0.5.16. The native installer, private app source, signed feed, title identity, user queue/settings/favorites and custom FPKGi files are unchanged. No new app installation or USB conversion is needed after an approved catalog merge.

## Coverage

Added 75 direct-file records: 28 apps, 8 homebrew, 2 emulators, 37 games. The base catalog grows from 123 to 198. All original entries and the expanded metadata/mod feeds are preserved byte-for-byte at the item level. Samples are labeled under Homebrew. Five ioQuake3 variants are engines that require separately supplied game data, not five complete retail games. Source release versions are retained separately; an uninspected SFO APP_VER is left unknown.

Examples include Sonic Robo Blast 2, Freedoom Phases 1/2, OpenTyrian, PicoPlay, Control4Free, Playfin and RommPS. VR titles retain VR in their names and require the publisher's headset/controller checks. Ports and server clients retain their own-data/server prerequisites.

## Evidence and limits

49 creator repositories and151 public publisher listings were reviewed.118 candidate files were probed.78 passed 128-byte PKG header, source/actual title-ID, content-ID syntax and exact advertised-size checks. Existing/older host duplicates were then excluded. Failed identity checks and temporary timeouts remain in the audit; they are not silently promoted or called unavailable games.

Three complete transfers passed through the desktop download engine: Freedoom Phase 1 (40,697,856 bytes) and PicoPlay (6,619,136 bytes) matched GitHub's publisher digests. OpenTyrian (19,791,872 bytes) completed and received an observed pinned SHA-256; its host did not supply a publisher digest. No new PS4 installation/gameplay claim is made. Remaining header-only entries are Unverified and may still encounter upstream server failures.

Each entry records its upstream URL, author, release label, package identity, evidence time, digest origin, status and rights evidence. Creator licenses are attributed. Public homebrew-host listings often omit a software license; that is stated rather than inventing one. No binary is mirrored into this repository, and no new commercial game PKGs, ROM collections, system-firmware tools or PS5-only packages are added. A public download button is the recorded distribution evidence for host listings, not a claim of ownership or a permissive source license.

The original 30,263 reference records remain references. Existing retail game pages need a legitimate direct package source before they can become downloadable. The new raw totals include versions, engines and source pages; they are not counts of unique games or console-tested packages. See direct-download-audit-20261031.json and direct-download-additions-20261031.json for exact counts and per-entry evidence.

## On the PS4 after approval/merge

1. Keep CohenStore 0.5.16 installed. Press R3 in a browsing tab to refresh the catalog.
2. In Games, use L2 until Direct files is selected. Triangle searches titles such as Freedoom or Sonic Robo Blast 2.
3. X queues the selected direct file. Square opens the queue; R2 cancels/removes the selected task. Completed packages are retained.
4. After completion, close CohenStore and use GoldHEN Package Installer, HDD /data/pkg. Read the entry's setup requirements, especially for engine-only ports, VR titles, emulators and server clients.

Until this proposal is approved, the public catalog remains at its previous contents. A new signed native release is a separate approval. To revert this catalog proposal, restore catalog/catalog.json from baseline commit b6f4c77155b14f56e40360f9e92f08833dd9faf5; do not delete user data or downloaded packages. P2's grouped metadata/offline-art architecture, P3's deeper download manager, dual layouts and AI/mod-building stages remain separate unfinished work.
