# CohenStore 0.5.24 DEV (private source handoff)
Status: **development only; do not merge into the live updater feed**.

The owner-provided 0.5.23 source was extended locally to build a 0.5.24 test package. Source and binary are saved in the owner’s ChatGPT development artifacts, not in this public repository.

## Package identity
- `CohenStore-0.5.24-DEV-TEST.pkg`: 46,006,272 bytes; SHA256 `98b8ba634f72c49988a98ea3ddcdc89cc3d3715a8b175cb90eda516a58d9a2e2`
- Embedded SFO `APP_VER 01.24`, title ID `CHST00001`, content ID `IV0000-CHST00001_00-COHENSTORE000000`
- Extracted catalog count: 207 direct items; 12,205 library-store; 18,046 library-links. All three JSON files matched developer source byte-for-byte.
- 209 packaged `.cimg` covers, including two generated *unofficial* fallback images, not publisher artwork.

## Changes
- New rights-gated, HTTPS/sha256-pinned cover importer for approved PNG artwork; exact IDs, size and redirect protections. Developer-side tool only.
- Two original AI artwork covers for Blue Boi Quickz and SpaceShooter, preserving previous generated placeholders in a backup. Existing 2048 cover remains unchanged.
- Non-destructive audit of 207 source entries: 16 creator-release, 59 publisher-homebrew listing, 132 rights-unverified. The audit does not certify live download availability.
- Selected-title hero and clearer download status in the Console UI; Mint layout preserved.
- Developer-side GTA V Story Mode blueprint exporter for CUSA00419 version-specific drafts, with disabled-by-default features. **Does not create or install an executable game plugin.**
- Source report, tests, checksums and previews saved privately.

## Validation
- 59/59 download tests passed
- 96/96 catalog/mod/update/artwork/AI tests passed
- 17/17 native transport/recovery/catalog guard/import tests passed
- **172 tests in completed suites passed.** Longer native startup suite timed out and is excluded.
- Native OpenOrbis build, PKG integrity validation, and extraction succeeded.
- Real PS4 console testing **pending**.

## Unfinished
Full licensed artwork and verified authorized PKG coverage; on-console background cover downloads; exact Store UI replication; AI executable mod compiler; auto-install and native notifications. Do not label these completed.

## Release safety
The original signed `update/release.json` and `update/manifest.json` are unchanged. The separate 0.5.22 recovery-channel publication and real 0.5.21 bridge validation remain pending. The owner must preserve backups and use a deliberate console smoke test before any live update. No private signing key or full source is included here.
