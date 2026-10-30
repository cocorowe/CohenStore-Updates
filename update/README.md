# CohenStore app updates

CohenStore 0.5.5 adds the Store Updates tab. Install the saved 0.5.5 UPDATER-TEST package once through USB. Older builds do not have this updater.

- Open Store Updates with L1/R1.
- Press R3 to check for a release.
- Press X to download a newer release after checking.
- Close CohenStore and install the verified package through GoldHEN Package Installer, with its source set to /data/pkg.
- Circle pauses an update download. R2 refreshes the content catalog.

The published release is 0.5.5. An installed 0.5.5 should report up to date. It will download a package when a newer signed version is published.

## Active feed

The client reads `update/release.json`. It verifies the Ed25519 signature of the exact `signed_payload` string using the public key embedded in the installed app. It checks the release channel, revision, version, official repository URL, package size, SHA-256 and CohenStore package identity before staging it.

`manifest.json` retains the older catalog planning fields and points at the active release feed. The 0.5.5 updater reads `release.json` directly.

The package URL is pinned to an immutable Git commit. GitHub publication verified the full saved package size, SHA-256, magic and content ID before committing it. No update installs automatically.

## Future publication

Keep the existing private signing key outside the public repository and outside the PS4. Increase APP_VERSION_CODE and PS4 APP_VER when building a new release. Publish the PKG, then use the source's `tools/publish_update.py` with the existing private key, exact package, increased revision and commit-pinned HTTPS URL. Publish its output as `update/release.json`.

The recovery publication workflow assembled the already-built package from small uploads and removed the staging files. It does not build the PS4 app or hold its private signing key.

## Validation limits

The recovered source passed 72 desktop app tests. The repository checks pass. Console HTTPS, controller interaction, real download and GoldHEN installation still require a PS4 test.
