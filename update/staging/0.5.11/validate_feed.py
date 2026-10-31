#!/usr/bin/env python3
"""Validate the public CohenStore content catalog and update-manifest scaffold."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog/catalog.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "update/manifest.json").read_text(encoding="utf-8"))

if catalog.get("schema") != 1 or not isinstance(catalog.get("items"), list):
    raise SystemExit("catalog: expected schema 1 and an items array")
seen = set()
for index, item in enumerate(catalog["items"]):
    prefix = f"catalog item {index}"
    if not isinstance(item, dict):
        raise SystemExit(f"{prefix}: expected object")
    for field in ("id", "title", "category"):
        if not isinstance(item.get(field), str) or not item[field].strip():
            raise SystemExit(f"{prefix}: missing {field}")
    if item["id"] in seen:
        raise SystemExit(f"{prefix}: duplicate id {item['id']}")
    seen.add(item["id"])
    urls = item.get("urls")
    if not isinstance(urls, list) or not urls:
        raise SystemExit(f"{prefix}: urls must be a non-empty array")
    if any(not isinstance(url, str) or not url.startswith("https://") for url in urls):
        raise SystemExit(f"{prefix}: every URL must use HTTPS")
    digest = item.get("sha256", "")
    if digest and not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
        raise SystemExit(f"{prefix}: sha256 must be 64 hex characters or empty")

if manifest.get("schema") != 1 or manifest.get("channel") not in ("stable", "testing"):
    raise SystemExit("manifest: unsupported schema or channel")
if not isinstance(manifest.get("content_version"), int) or manifest["content_version"] < 1:
    raise SystemExit("manifest: content_version must be a positive integer")
if not isinstance(manifest.get("announcements"), list) or not isinstance(manifest.get("catalog_updates"), list):
    raise SystemExit("manifest: announcements and catalog_updates must be arrays")

print(f"Validated {len(seen)} catalog entries and schema-1 manifest scaffold.")

