# CohenStore 0.5.10 installer permissions fix

0.5.9 incorrectly treated failure to chmod an existing /data/pkg as a download
failure. A shared folder can permit writing without allowing CohenStore to
change its mode. The new client preserves existing installer folder permissions
and checks write access with a unique temporary file that is removed immediately.
New folders created by CohenStore still receive 0755; verified PKGs receive 0644.
Game downloads and Store Updates use the same folder check. Non-directory paths
and genuinely unwritable directories are rejected without replacing their data.

Install this PKG over the closed CohenStore 0.5.9 using GoldHEN Package Installer.
An existing 0.5.9 updater can hit the same permission error while staging this
repair, so one manual installation is required. Future updates use the fixed check.
Then open CohenStore, select the failed download in the queue and press X to retry.
Completed verified PKGs go directly into /data/pkg. Incomplete files and receipts
remain under /data/CohenStore/downloads. GoldHEN installation remains manual.

Version 0.5.10 uses version code 60 and PS4 APP_VER 00.60, with the existing
CHST00001 title/content IDs and update signing identity. The regression fixture
reproduces the old error by denying chmod on an otherwise writable folder.
The repair also checks that an unwritable destination is rejected before HTTP.
Desktop and package validation do not establish success on a real PS4.
