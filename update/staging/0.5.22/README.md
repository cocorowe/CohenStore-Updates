# CohenStore recovery channel 0.5.22

**The current, original CohenStore updater is not changed here.** It will keep offering signed 0.5.17 until an existing publisher signing key is recovered.

This directory is for uploading four **verified binary chunks** of a 0.5.22 testing PKG. The recovery publish workflow will validate every chunk, the complete PKG digest and title identity, the signed Ed25519 release envelope and catalog size before atomically committing `update/packages/CohenStore-0.5.22-SIGNED-UPDATE-TEST.pkg` and `update/recovery/release.json` to `main`.

**Upload exactly:** `000.part`, `001.part`, `002.part`, `003.part`, from the owner-provided signed PKG files. Do not rename or recompress the parts. Use GitHub **Add file → Upload files** while viewing this directory on branch `main`. Each file is under 25 MB.

The first installed PS4 version that accepts the recovery key is `0.5.21`, which the owner must install manually **once**. After the recovery feed is published, a console running 0.5.21 should be able to check R3 and download the signed 0.5.22 PKG with X into `/data/pkg`, then install it through GoldHEN. **Neither native PS4 build has been tested on the console yet.** Always keep backups of `/data/CohenStore` and a known-working PKG. Do not uninstall your current app.

No signing private key should ever be uploaded here, committed, or pasted into an issue. Preserve the new private signing key securely offline for later signed releases.
