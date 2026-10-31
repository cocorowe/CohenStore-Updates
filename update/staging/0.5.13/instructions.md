# CohenStore 0.5.13 staging and catalog diagnostics repair

The installer-folder helper now opens an existing directory before attempting
mkdir. If creation is required, it reopens the directory rather than relying on
EEXIST/errno mapping. Existing folder permissions and non-directory files are
preserved. Actual write access is still checked with a removable unique probe.
Verified cached updates are made readable before folder preparation, and a
staging failure reports the retained PKG path instead of losing the download.

The same helper is used for games and app updates. The catalog parser accepts
all 119 current feed entries, including 101 Archive titles. Catalog rejection
now includes the first entry error and valid/rejected counts while preserving
the existing cache. The UI displays the real compiled application version.

Update version code 513, APP_VER 01.13, title/content identity CHST00001 and the
existing signing identity are retained. An older updater may still fail staging
this repair, because the repaired code cannot run until installed.

Manual recovery without another USB transfer:
1. Check Store Updates with R3 and download 0.5.13 with X.
2. If staging fails, close CohenStore and open PS4-Xplorer.
3. Copy /data/CohenStore/downloads/ffdcbf88b1f14835.pkg to /data/pkg.
4. Install that copied PKG with GoldHEN Package Installer using source HDD.
5. Reopen, confirm version 0.5.13, and refresh Games with R3.
Only copy the completed .pkg, never a .part file. Keep existing data and receipts.
If the installer path is missing, inaccessible or not a directory, inspect it
before changing it. A USB install of this same PKG is an alternative.

Validation: 89 desktop tests pass, including a regression denying mkdir without
setting errno for an existing writable folder. Native frontend tests cover
Archive catalog refresh and detailed rejection without destroying its cache.
The PS4 executable compiles and its PKG passes digest/signature checks. Actual
console folder access, installation and game launch still require PS4 testing.
