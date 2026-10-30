# Catalog

`catalog.json` uses schema 1:

- `schema`: integer, currently `1`.
- `items`: array of downloadable content records.
- Each record has a stable `id`, display `title`, `category`, exact `size_bytes` when known, optional `sha256`, and one or more direct HTTPS `urls`.
- `note` contains compatibility or provenance caveats.

## Current entries

The current catalog contains two developer-published homebrew packages:

1. Apollo Save Tool v2.4.0 — developer release includes a SHA-256 digest.
2. PS4 Cheats Manager v1.2.2 — developer release metadata does not publish a SHA-256 digest, so the field is empty.

Neither package has been tested on the target console/firmware by this project.

## Adding an item

Use a stable ID and a direct HTTPS download URL. Verify that the source is the developer's release page and that the asset is actually a PS4 PKG. Do not copy estimated sizes into `size_bytes`; use an exact byte count or omit/zero it according to the client schema. Leave the hash empty if you cannot obtain a trusted digest.

Commercial games, updates, and DLC are catalog metadata only unless the project has explicit redistribution permission for the actual package files. Never use Internet Archive mirrors or provider share pages as direct package URLs.
