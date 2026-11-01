# Direct source-page gapfill, October 31, 2026

This **additive catalog-only** branch proposes 9 publisher-released PS4 PKG links and preserves the prior 198 entries in original order. New direct catalog total: **207**. Existing 30k+ source entries, mod catalogs, queue, user data, signed updater, PKG, and native PS4 app code are untouched.

## New source-matched titles
- Jellyfin for PS4 v1.12 — jw-notes/JellyFin-PS4, IV0000-JFPS40000_00-JELLYFINPS400000.pkg. Publisher digest and asset size recorded; **Unverified** for actual transfer and PS4 installation.
- PS4 Homebrew Store v4.5 — LightningMods/PS4-Store, Store-R2.pkg. Publisher digest and asset size recorded; **Unverified** for actual transfer and PS4 installation.
- Ship of Harkinian PS4 v0.2.0 — alechurri/shipofharkinian-ps4, IV0000-SOHP00001_00-SHIPOFHARKINIAN0.pkg. Publisher digest and asset size recorded; **Unverified** for actual transfer and PS4 installation.
- 2 Ship 2 Harkinian PS4 v0.1.0 (experimental) — alechurri/2ship2harkinian-ps4, IV0000-TSHP00001_00-TWOSHIPHARKINIAN.pkg. Publisher digest and asset size recorded; **Unverified** for actual transfer and PS4 installation.
- XCloud4 v1.2.1 beta — asp11edgr/XCloud4, XCloud4-1.2.1-beta-publico.pkg. Publisher digest and asset size recorded; **Unverified** for actual transfer and PS4 installation.
- GMCA Media Center v1.4.0 — thcolin/gamepad-media-center-aggregator, IV0001-GMCA00000_00-GMCA000000003000.pkg. Publisher digest and asset size recorded; **Unverified** for actual transfer and PS4 installation.
- G-Diffuser PS4 v01.20 — iHaiDeeZ/G-Diffuser-PS4, G-Diffuser-PS4-v01.20.pkg. Publisher digest and asset size recorded; **Unverified** for actual transfer and PS4 installation.

### RetroArch publisher packages
- RetroArch PS4 Frontend v1.22.2-15 and the separate RetroArch PS4 Core Installer v1.22.2-15 were discovered in the developer's release assets. Both remain Unverified pending independent package and console checks. These were not already in the direct base catalog. The pFBN/pGBA/pGEN/pNES/pSNES packages were **already present**, so they were deliberately not duplicated.

## Important
- These additions appear as separate direct-file cards in their category after refreshing the base feed. 0.5.16 **does not automatically merge each corresponding source-page card with its new direct-download card**. That requires a separately reviewed native client change.
- These entries are **Unverified**, not Working. No binary content or PS4 gameplay was independently tested in this session. The host may fail, redirect, or change.
- Some open-source engines require legally obtained game data, media clients require services, and experimental ports can be incompatible with a particular firmware.
- The current source-only retail pages cannot be safely converted to direct packages without authorized publisher download files. No scraped hosting-page redirects were fabricated.
- Keep `catalog/library-store.json`, `catalog/library-links.json` and `catalog/expansion.json` unchanged. Do not delete custom FPKGi JSONs or touch installed games.
- **Do not merge yet:** run repository tests, audit package headers, and check direct URLs on an actual working environment before release. The branch is suitable for review; no new console installer is required for a catalog-only addition once approved.
