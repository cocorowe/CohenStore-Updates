# Catalog

`catalog.json` uses schema 1. Each entry has a stable `id`, display `title`, `category`, exact `size_bytes`, optional `sha256`, direct HTTPS `urls`, and a provenance/compatibility `note`.

## Current entries

1. **Apollo Save Tool v2.4.0** — developer-published homebrew package with publisher-provided SHA-256 digest.
2. **PS4 Cheats Manager v1.2.2** — developer-published homebrew package; its release metadata does not publish a SHA-256 digest, so the field is empty.
3. **PS MTP Explorer 1.01** — developer-published app with publisher-provided SHA-256 digest. Upstream reports testing on firmware 9.00, 10.01, and 11.00; 13.52 compatibility is unknown.

None of these packages has been installed or tested on the target console by this project.

## Adding an item

Use a stable ID and a direct HTTPS download URL. Verify that the source is the developer's release page and that the asset is actually a PS4 PKG. Do not copy estimated sizes into `size_bytes`; use an exact byte count or zero when unknown. Leave the hash empty if you cannot obtain a trusted digest.

Commercial games, updates, and DLC are catalog metadata only unless the project has explicit redistribution permission for the actual package files. Never use Internet Archive mirrors or provider share pages as direct package URLs.
