#!/usr/bin/env python3
"""Validate the public CohenStore content catalog and update-manifest scaffold."""
import json
import urllib.parse
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

mods_path=ROOT/'catalog/mods.json'
if mods_path.exists():
    mods=json.loads(mods_path.read_text(encoding='utf-8'))
    if mods.get('schema')!=1 or not isinstance(mods.get('items'),list) or not mods['items']:
        raise SystemExit('mods: expected nonempty schema-1 catalog')
    mod_ids=set()
    for item in mods['items']:
        if not item.get('id') or item['id'] in mod_ids or item['id'] in seen:raise SystemExit('mods: duplicate or missing id')
        mod_ids.add(item['id'])
        if item.get('category')!='mod_menus' or item.get('mod_kind') not in ('menu','cheats','plugin','tool','payload'):
            raise SystemExit('mods: missing mod classification')
        if item.get('format') not in ('pkg','prx','sprx','json','bin','zip'):raise SystemExit('mods: unsupported file format')
        if not re.fullmatch(r'[a-f0-9]{64}',item.get('sha256','')) or type(item.get('size_bytes')) is not int or item['size_bytes']<4:
            raise SystemExit('mods: verified hash and exact size required')
        if not isinstance(item.get('urls'),list) or not item['urls']:raise SystemExit('mods: missing URLs')
        for url in item['urls']:
            p=urllib.parse.urlsplit(url)
            if p.scheme!='https' or not p.hostname or p.username or p.password or any(ord(c)<=32 for c in url) or '\\' in url or '%' in p.netloc:raise SystemExit('mods: invalid HTTPS URL')
        if item.get('format') in ('sprx','prx','json'):
            name=item.get('install_name','')
            if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,95}',name) or '..' in name or not name.endswith('.'+item['format']):raise SystemExit('mods: unsafe install filename')
            if len(item.get('title_ids',[]))!=1 or not re.fullmatch(r'CUSA\d{5}',item['title_ids'][0]) or len(item.get('game_versions',[]))!=1:raise SystemExit('mods: exact CUSA/version required')
        if item.get('format')=='json' and item.get('install_name')!=item['title_ids'][0]+'_'+item['game_versions'][0]+'.json':raise SystemExit('mods: cheat filename identity mismatch')
    print(f'Validated {len(mod_ids)} separately versioned mod/cheat entries.')

expanded_ids=set(seen)
for filename in ('expanded-mods.json','expansion.json','library-store.json','library-links.json'):
    path=ROOT/'catalog'/filename
    if not path.exists():continue
    data=json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema')!=1 or not isinstance(data.get('items'),list) or not data['items']:raise SystemExit(filename+': invalid catalog')
    for item in data['items']:
        if not item.get('id') or not item.get('title') or item['id'] in expanded_ids:raise SystemExit(filename+': duplicate/missing id or title')
        expanded_ids.add(item['id'])
        if item.get('category') not in ('games','updates','dlc','homebrew','apps','emulators','mod_menus'):raise SystemExit(filename+': invalid category')
        urls=item.get('urls',[])
        if not isinstance(urls,list) or len(urls)>16:raise SystemExit(filename+': invalid URL list')
        if filename.startswith('library-') and urls:raise SystemExit(filename+': source index must not advertise direct files')
        source=item.get('source_url','')
        if not urls and not source:raise SystemExit(filename+': no file or source page')
        for value in urls+([source] if source else []):
            p=urllib.parse.urlsplit(value)
            if p.scheme not in ('http','https') or not p.hostname or p.username or p.password or any(ord(c)<=32 for c in value) or '\\' in value or '%' in p.netloc:raise SystemExit(filename+': unsafe URL')
        if urls:
            if any(not u.startswith('https://') for u in urls):raise SystemExit(filename+': file downloads must use HTTPS')
            if type(item.get('size_bytes')) is not int or item['size_bytes']<4:raise SystemExit(filename+': direct file needs exact size')
            if item.get('format','pkg')!='pkg' and not re.fullmatch(r'[a-f0-9]{64}',item.get('sha256','')):raise SystemExit(filename+': mod data needs a hash')
        if item.get('format')=='xml' and (item.get('mod_kind')!='patch' or len(item.get('title_ids',[]))!=1 or item.get('install_name')!=item['title_ids'][0]+'.xml'):raise SystemExit(filename+': invalid patch install metadata')
    print(f'Validated {len(data["items"])} records in {filename}.')

print(f"Validated {len(seen)} base catalog entries and schema-1 manifest scaffold.")



