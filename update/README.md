# CohenStore 0.5.8 update test after 0.5.7 repair

The user’s 0.5.5 client checks the feed but reports a package mismatch during
update download. The exact failing validation sub-check is not yet confirmed.
Inspection found a concrete ABI hazard in the installed OpenOrbis headers:
mode_t is first defined as unsigned int, hiding a later unsigned-short
compatibility definition. The compiled stat.st_size access is at offset 80.
The size validator now measures the file with fseeko/ftello instead of stat,
matching the download engine’s existing file-size method. Size, signed
publisher identity, SHA-256, PKG magic and content ID remain mandatory.

Install CohenStore-0.5.7-UPDATER-REPAIR.pkg once through USB because the old
client rejects an update before corrected code can execute. Then check Store
Updates with R3 and download 0.5.8 with X. Close the app when Update ready is
shown. Install /data/pkg/CohenStore-58.pkg through GoldHEN Package Installer.
No package is installed automatically.

Errors now distinguish UPD-OPEN, UPD-SEEK, UPD-SIZE and UPD-HASH, and include
the measured/expected byte counts for a size failure. Update staging errors
are recorded in the diagnostics log. Old queue/download data is preserved.
The stale-catalog-link retry fix and HTTP header-size fix remain included.

Validation: all 74 app tests pass. Update tests deliberately make stat fail
and still require valid signed packages to verify and stage. Changed size,
hash, publisher signature and PKG identity remain rejected. Native repair
and test packages compile and pass package validation. The console cause
and successful repaired update download remain to be confirmed on PS4.
