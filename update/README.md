# Update manifest

`manifest.json` is currently a **schema-1 planning scaffold**, not a live in-app updater.

The PS4 source currently fetches `catalog/catalog.json` directly. It does not yet parse this manifest. The manifest fields reserve space for:

- `channel`: stable or testing.
- `content_version`: monotonically increasing content revision.
- `announcements`: human-readable release notes.
- `catalog_updates`: future content/catalog update references.
- `app_update`: future application PKG update metadata.

Before this file can drive updates, the client must implement and test manifest parsing, trusted publisher signatures (a plain SHA-256 hash is not publisher authentication), HTTPS-only references, version/rollback protection, atomic catalog replacement, and explicit user confirmation for app PKG updates. No app package may be silently installed.
