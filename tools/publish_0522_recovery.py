#!/usr/bin/env python3
"""Publish a separately signed recovery feed; never replace the legacy updater."""
import hashlib
import json
import shutil
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

STAGE = Path("update/staging/0.5.22")
OUTPUT = Path("update/packages/CohenStore-0.5.22-SIGNED-UPDATE-TEST.pkg")
FEED = Path("update/recovery/release.json")
EXPECTED_HASH = "12068575c8771e0ae23a805a0769d75afbe5675d5285a3c49fa64b3becd5b71d"
EXPECTED_SIZE = 45154304
URL = "https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/packages/CohenStore-0.5.22-SIGNED-UPDATE-TEST.pkg"
NEW_KEY = bytes.fromhex("1f6a3ab8b52f4a47bd74195a32cd9279b2b534977fba448e5dde3bcc0302318d")
OLD_KEY = bytes.fromhex("6d7df4c99728545705a58cb75c6e15aa097f03ab452c86726da359668bbfec41")
PARTS = [
    ("000.part", 12582912, "5187936a56bec016cf7a5ff7054edfb81f1a1d6d09f2cc83e397488017f2e23e"),
    ("001.part", 12582912, "7bb06ecd1f877bf67c0a1cd0ee08b5571530134cc7e6ebb532a74845ff4aff6f"),
    ("002.part", 12582912, "bc807748313fae0c1ac7afae930c683a649761b017ee573366c172850c25d16f"),
    ("003.part", 7405568, "3feb368e222db505a2db447cb510555c039f5f5ea411fcbf20d5a3409f6cf85f"),
]
CONTENT_ID = "IV0000-CHST00001_00-COHENSTORE000000"

def verify_envelope(path, key):
    body = json.loads(Path(path).read_text(encoding="utf-8"))
    signed = body["signed_payload"].encode("utf-8")
    Ed25519PublicKey.from_public_bytes(key).verify(bytes.fromhex(body["signature"]), signed)
    return json.loads(signed)

def check_catalog(path, minimum):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = data.get("items", [])
    assert isinstance(entries, list) and len(entries) >= minimum, f"{path}: catalog shrank"

def main():
    old = verify_envelope("update/release.json", OLD_KEY)
    assert old["version_code"] == 517 and old["revision"] == 12, "Legacy live feed changed; stop"
    assert not OUTPUT.exists() and not FEED.exists(), "Recovery release already exists; no overwrite"
    for path, count in [("catalog/catalog.json", 207), ("catalog/library-store.json", 12205),
                        ("catalog/library-links.json", 18046)]:
        check_catalog(path, count)
    assert sorted(p.name for p in STAGE.glob("*.part")) == [p[0] for p in PARTS], "Missing or extra parts"
    signed = verify_envelope(STAGE / "release.json", NEW_KEY)
    expected = dict(schema=1, channel="testing", revision=13, version="0.5.22", version_code=522,
                    title_id="CHST00001", content_id=CONTENT_ID,
                    size_bytes=EXPECTED_SIZE, sha256=EXPECTED_HASH, url=URL)
    assert signed == expected, "Signed release differs from verified build"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    hash_obj = hashlib.sha256()
    size = 0
    with OUTPUT.open("wb") as dst:
        for filename, length, sha in PARTS:
            part = STAGE / filename
            assert part.stat().st_size == length, f"Wrong size: {filename}"
            data = part.read_bytes()
            assert hashlib.sha256(data).hexdigest() == sha, f"Wrong hash: {filename}"
            hash_obj.update(data)
            dst.write(data)
            size += len(data)
    assert size == EXPECTED_SIZE and hash_obj.hexdigest() == EXPECTED_HASH, "Wrong final package hash"
    with OUTPUT.open("rb") as package:
        header = package.read(0x64)
    assert header[:4] == bytes([0x7f, 67, 78, 84]) and header[0x40:0x64] == CONTENT_ID.encode(), "Wrong PS4 PKG identity"
    FEED.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(STAGE / "release.json", FEED)
    (FEED.parent / "manifest.json").write_text(json.dumps({
        "schema": 1, "channel": "testing", "content_version": 22, "app_version": "0.5.22",
        "app_update": {"version": "0.5.22", "version_code": 522,
                       "release_manifest_url": "https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/recovery/release.json"},
        "announcements": ["0.5.22 signed recovery update; install 0.5.21 trust bridge once before using this feed."]
    }, indent=2) + "\n", encoding="utf-8")
    print("PASS: old feed untouched, authenticated new feed, package size/hash/identity and catalog floors")
    print("PASS: recovery files staged; GitHub commit still required")

if __name__ == "__main__":
    main()
