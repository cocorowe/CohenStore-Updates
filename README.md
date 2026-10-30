# CohenStore Updates

This public repository hosts the **content catalog** used by CohenStore. It is separate from the CohenStore PS4 application source and does not itself build or update the installed app.

## Live catalog

- Catalog JSON: [catalog/catalog.json](catalog/catalog.json)
- Raw HTTPS URL used by the current development frontend:

  `https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/catalog/catalog.json`

The current source can fetch this catalog over HTTPS, validate schema 1, and keep its previous local catalog if a refresh fails. The source currently supports catalog refresh; it does **not** yet parse `update/manifest.json`, verify a signed manifest, apply artwork/announcement deltas, or update the CohenStore application PKG.

## Update manifest

`update/manifest.json` is a scaffold for future update support. Do not treat it as an active app updater until the PS4 client implements trusted publisher-signature verification, version/rollback checks, and a tested content-update workflow.

## Catalog rules

- Only add downloads published by the developer or another source authorized to distribute the file.
- Do not add commercial game PKGs unless distribution is explicitly authorized. A listing is not permission to redistribute.
- Use direct HTTPS package URLs, not file-hosting share pages.
- Keep exact byte sizes. Use an empty SHA-256 only when the publisher does not provide a digest; label it clearly.
- Record unknown compatibility as unknown. Never claim PS4 firmware compatibility without testing.
- Do not add PRX plugins as PKGs. Plugin payloads require a separate plugin-install workflow.

See [catalog/README.md](catalog/README.md) and [update/README.md](update/README.md).
