# CohenStore 0.5.9 installer-folder test

Completed verified PKGs are now saved directly in /data/pkg for GoldHEN HDD
Package Installer. Close CohenStore, open GoldHEN Package Installer, select
source HDD, and keep Search Subfolders off for the current console test.
No file-manager copy is required for future completed downloads. Installation
still requires the user to select the package in GoldHEN.

Incomplete and rejected transfers remain in /data/CohenStore/downloads with
.part extensions. PRX plugins retain their separate manual installation flow.
A PKG appears in the installer only after the existing format, size and
configured SHA-256 checks pass. Receipts and atomic final renames are retained.

The app explicitly sets its own data/download folders and the installer folder
to 0755, and publishes verified PKGs as 0644. It does not change owners/groups,
apply recursive permission changes, rename pkg.backup, or edit other apps.
A non-directory at the installer path is preserved and reported as an error.

To prepare an older completed download already held by CohenStore, select its
completed queue/history entry and press X. The app re-verifies its saved
receipt and package, then stages it without another HTTP transfer. Cached
packages with failed checks are preserved with an error rather than replaced.

Store Updates still uses R3 to check and X to download a newer signed store
release. Updates also receive readable staging permissions. 0.5.9 has version
code 59, PS4 APP_VER 00.59 and the same CHST00001 title/content IDs and public
signing key as earlier versions. It installs over the closed existing store.

Validation: 81 desktop tests pass. Seven native boot/UI tests were then rerun
with explicit assertions that existing data/download folders become 0755.
A full 71,696,384-byte Relic Hunters upload was downloaded through the desktop
engine from a local HTTP server and atomically published in an installer test
folder with a matching SHA-256 and 0644 permissions. This is a desktop test,
not evidence of PS4 networking or installation success. The native executable
compiles and its PKG passes all package digest/signature checks. Real-console
validation of 0.5.9 remains required.
