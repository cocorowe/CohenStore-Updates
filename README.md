# CohenStore Updates

**Current app repair: 0.5.13.** This release uses an existing installer folder
without relying on the error returned by mkdir. It also shows the actual
installed version and a specific catalog rejection reason.

If an older updater cannot stage this repair, download it, close CohenStore,
and copy `/data/CohenStore/downloads/ffdcbf88b1f14835.pkg` into `/data/pkg` with
PS4-Xplorer. Install that copied package in GoldHEN's HDD Package Installer,
then reopen and refresh Games with R3. See [update instructions](update/README.md).

The current application source and private signing key are not part of the
public upload. Older source archives are still present in this public updates repository.

## Current listings

The feed preserves the homebrew, emulator and tool listings and adds 101 public Archive game entries.
Games: 2048, Relic Hunters Zero, Sonic Time Twisted, Sonic 1 SMS Remake,
and Sonic 2 SMS Remake. Emulators: pFBN, pGBA, pGEN, pNES and pSNES.
Apps/tools: Apollo Save Tool, PS4 Cheats Manager, PS MTP Explorer, ezRemote Client and PS4 Package Link.

Download URLs and exact sizes come from publisher release metadata. Published
hashes are retained when available; unknown hashes stay empty. Release metadata
checks do not establish full transfer reliability or PS4 firmware 13.52 support.
Emulators require separately supplied compatible game files.

The additional Archive entries come from the user-selected FPKGi source. Game updates, DLC and GTA menus have not been populated.
No verified GTA 1.56/CUSA00419 plugin binary is currently available in this feed.
Shattered Pixel Dungeon was held back because its release description and API
asset digest disagree, and it needs additional Sony modules.

## Automatic catalog maintenance

The Refresh developer game catalog workflow checks an explicit allowlist of
developer repositories daily and supports manual runs. It tests its merger,
fetches release metadata, validates the complete feed, and commits changes only
when the catalog changes. A failed fetch does not overwrite the existing feed.
Unchanged asset IDs keep curated notes and metadata.

The new mint client checks the configured feed at startup by default and keeps
its cache on errors. The user can also enable checks every 15 minutes while the
app is open. Older clients retain their own refresh settings.

The allowlist includes PS4 Package Link, a developer-published PS4/Windows companion for managing and installing user-authorized PKGs over a local network. The English PS4 package is listed; its Polish counterpart shares the same app identity and is not duplicated in the catalog.\n\nThe workflow updates listings, not game binaries or the installed store app.
The installed app still needs a new PKG for code/interface changes. Signed app updates are available through the Store Updates tab. See
[update instructions](update/README.md) for the current installer test.

## Download link monitoring

The Check catalog download links workflow checks the current feed daily and on
catalog changes. It requests only the first four bytes, checks the PKG/PRX
header and advertised size, and records whether the host supports byte ranges.
Its JSON report is retained as a GitHub Actions artifact for 14 days. A failure
does not erase the catalog. HTTPS downgrade redirects are refused. Header checks do not establish complete-file integrity, PS4 launch
support or future reliability.

During the 0.5.2 repair, full desktop downloads of 2048 (35,454,976 bytes) and
Relic Hunters Zero (71,696,384 bytes) completed. 2048 matched the publisher's
SHA-256. Relic Hunters Zero has no publisher digest to compare. Console testing
on firmware 13.52 is still pending.

Optional full verification is available through the manual workflow input
`full_transfer=true`. It downloads eligible files only when a publisher SHA-256
is present and the advertised size is at most 256 MiB, then checks the exact
byte count and complete SHA-256. Larger files and entries without a publisher
digest are explicitly skipped. This mode is not part of the daily schedule,
to avoid repeatedly transferring large packages. Neither mode establishes
PS4 installation or launch compatibility.

## Catalog rules

- Use developer-published or authorized direct HTTPS downloads.
- Exclude share-page URLs, embedded credentials and invented sizes, hashes or compatibility claims. Internet Archive is allowed following the user’s revised preference.
- Do not add commercial game downloads without distribution authorization.
- Treat firmware/game-version compatibility as unknown until tested.
- PKG and PRX are separate formats. Plugin activation and package installation
  remain manual in the client.
- Version, title-ID and parent-game metadata must describe the actual package.

The feed remains compatible with the older schema-1 client. Optional metadata
is ignored by older clients. No reference-only cards with empty download arrays
are published to this live feed, because older clients reject them.

