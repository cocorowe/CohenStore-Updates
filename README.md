# CohenStore Updates

Content feed for CohenStore, separate from its PS4 application source.

Live feed: https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/catalog/catalog.json

## Current listings

The feed contains five homebrew games, five emulators, and four apps/tools.
Games: 2048, Relic Hunters Zero, Sonic Time Twisted, Sonic 1 SMS Remake,
and Sonic 2 SMS Remake. Emulators: pFBN, pGBA, pGEN, pNES and pSNES.
Apps/tools: Apollo Save Tool, PS4 Cheats Manager, PS MTP Explorer and ezRemote Client.

Download URLs and exact sizes come from publisher release metadata. Published
hashes are retained when available; unknown hashes stay empty. Release metadata
checks do not establish full transfer reliability or PS4 firmware 13.52 support.
Emulators require separately supplied compatible game files.

Commercial games, game updates, DLC and GTA menus have not been populated.
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

The workflow updates listings, not game binaries or the installed store app.
The installed app still needs a new PKG for code/interface changes. The update
manifest remains a scaffold; signed app updates are not implemented.

## Download link monitoring

The Check catalog download links workflow checks the current feed daily and on
catalog changes. It requests only the first four bytes, checks the PKG/PRX
header and advertised size, and records whether the host supports byte ranges.
Its JSON report is retained as a GitHub Actions artifact for 14 days. A failure
does not erase the catalog. Internet Archive and HTTPS downgrade redirects are
refused. Header checks do not establish complete-file integrity, PS4 launch
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
- Exclude Internet Archive, share-page URLs, embedded credentials and invented
  sizes, hashes or compatibility claims.
- Do not add commercial game downloads without distribution authorization.
- Treat firmware/game-version compatibility as unknown until tested.
- PKG and PRX are separate formats. Plugin activation and package installation
  remain manual in the client.
- Version, title-ID and parent-game metadata must describe the actual package.

The feed remains compatible with the older schema-1 client. Optional metadata
is ignored by older clients. No reference-only cards with empty download arrays
are published to this live feed, because older clients reject them.
