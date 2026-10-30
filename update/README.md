# CohenStore app updates

0.5.5 opens and checks this feed on the user's PS4. Version 0.5.6 is the first newer package offered for testing the complete update download and installation.

1. In Store Updates on 0.5.5, press R3, then X to download 0.5.6.
2. Wait for "Update ready", then close CohenStore.
3. In GoldHEN Package Installer, set the source to /data/pkg and install CohenStore-56.pkg.
4. Open the store. The footer should show 0.5.6. R3 on Store Updates should report up to date.

A USB installer is only required to bootstrap from an older version without the updater or to recover after a failed test. No update installs automatically.

## Game downloads

0.5.6 keeps the native response-header fix from 0.5.4. Retrying a paused or failed item now uses the current catalog URLs, size and SHA-256 instead of keeping stale saved metadata. HTTP errors identify the failing host without exposing signed query tokens.

Refresh Games with R3 and test 2048 v1.0. Square opens the download queue; X retries an old failed item. Game packages remain under /data/CohenStore/downloads and require manual installation. Successful desktop transfer does not establish PS4 networking or game compatibility.

## Feed and publisher trust

The client reads update/release.json directly. It verifies the Ed25519 signature of the exact signed_payload bytes against its embedded public key. It validates release channel, revision, version, official HTTPS repository URL, size, SHA-256 and package identity before staging.

The active package URL is pinned to a Git commit. manifest.json retains the older catalog planning fields and points to the active signed feed.

Keep the existing private signing key outside this repository and outside the PS4. Increase APP_VERSION_CODE and APP_VER for each client release, and increase the signed revision. Use tools/publish_update.py from the source archive with the exact package and a commit-pinned official URL.

## Sources and validation

The 0.5.6 source archive is in update/sources/. All 74 local app tests pass. The PS4 executable compiles and its PKG passes package hash/signature checks. Publication reconstructed the new PKG from a compressed difference against 0.5.5 and verified its exact full SHA-256 before committing.

The full game download workflow uses the desktop engine to download all of 2048 and compare its size and publisher SHA-256. Console update download, installation and game download completion are still awaiting the user's test.
