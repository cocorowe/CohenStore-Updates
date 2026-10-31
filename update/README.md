# CohenStore 0.5.14

Downloads: press Square to open the queue. Circle pauses the active transfer and keeps it resumable. R2 cancels/removes the selected task, discards its unfinished transfer and keeps completed packages. X resumes/retries. A canceled item can be added again from Games.

Completed game packages use readable title, title ID and version filenames with a stable suffix in /data/pkg. Older hash-named packages are checked against their receipts before being renamed, without another download. Existing unrelated files and the working catalog are preserved.

Install: Store Updates, R3, X. Once ready, close CohenStore and install CohenStore-514.pkg through GoldHEN Package Installer using source HDD. Reopen and confirm 0.5.14.

Validation: 94 app tests passed, including active cancellation, removing another task during a transfer, preserving completed packages, and migration of old package names. Native PS4 build and package digest/signature checks passed. The new controls still need testing on a PS4.

Launch-time game-update blocking is deferred. No new Updates, DLC or mod-menu downloads have been added; compatibility still needs verification. Current app source remains private.
