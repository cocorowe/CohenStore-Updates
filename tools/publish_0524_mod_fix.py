#!/usr/bin/env python3
"""Safely publish a signed 0.5.24 *testing* recovery update; never touch legacy update/release.json."""
import hashlib
import json
from pathlib import Path
import shutil
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

BASE = Path("update")
PKG = BASE / "packages/CohenStore-0.5.24-Mod-Menu-Fix-PS4-TEST.pkg"
SIGNED_STAGE = BASE / "staging/0.5.24/release.json"
RECOVERY = BASE / "recovery/release.json"
MANIFEST = BASE / "recovery/manifest.json"
HISTORY = BASE / "recovery/history"
EXPECTED_SHA256 = "ce4148dccf36f9429f6685a400ae45f32e04184b335fac1fa7602ebcae11f107"
EXPECTED_BYTES = 46006272
CONTENT_ID = "IV0000-CHST00001_00-COHENSTORE000000"
PKG_URL = "https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/packages/CohenStore-0.5.24-Mod-Menu-Fix-PS4-TEST.pkg"
OLD_KEY = bytes.fromhex("6d7df4c99728545705a58cb75c6e15aa097f03ab452c86726da359668bbfec41")
RECOVERY_KEY = bytes.fromhex("1f6a3ab8b52f4a47bd74195a32cd9279b2b534977fba448e5dde3bcc0302318d")

def verified_envelope(path, pubkey):
    outer = json.loads(path.read_text(encoding="utf8"))
    data = outer["signed_payload"].encode()
    Ed25519PublicKey.from_public_bytes(pubkey).verify(bytes.fromhex(outer["signature"]), data)
    return json.loads(data)

def check_catalog(path, min_count):
    data=json.loads(Path(path).read_text(encoding="utf8"))
    entries=data.get("items",[])
    assert isinstance(entries,list) and len(entries)>=min_count,(path,len(entries))

def main():
    legacy = verified_envelope(BASE / "release.json", OLD_KEY)
    assert (legacy["version_code"],legacy["revision"]) == (517,12), "legacy feed changed"
    recovery = verified_envelope(RECOVERY, RECOVERY_KEY)
    assert (recovery["version_code"],recovery["revision"]) == (522,13), "recovery feed changed; stop, do not overwrite"
    old_manifest = json.loads(MANIFEST.read_text(encoding="utf8"))
    assert old_manifest["app_update"]["version_code"] == 522
    for p,n in [("catalog/catalog.json",207),("catalog/library-store.json",12205),("catalog/library-links.json",18046)]:
        check_catalog(p,n)
    new=verified_envelope(SIGNED_STAGE,RECOVERY_KEY)
    expected=dict(schema=1,channel="testing",revision=14,version="0.5.24",
                  version_code=524,title_id="CHST00001",content_id=CONTENT_ID,
                  size_bytes=EXPECTED_BYTES,sha256=EXPECTED_SHA256,url=PKG_URL)
    assert new == expected, "signed payload differs from target package or version"
    assert not PKG.is_file(), "target PKG already published; refusing overwrite"
    candidate=Path("/tmp/cohenstore-0524-verified.pkg")
    assert candidate.is_file() and candidate.stat().st_size==EXPECTED_BYTES,"wrong package bytes"
    h=hashlib.sha256()
    with candidate.open("rb") as f:
        header=f.read(0x64)
        h.update(header)
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    assert h.hexdigest()==EXPECTED_SHA256,"package SHA-256 mismatch"
    assert header[:4]==b"\\x7fCNT".decode("unicode_escape").encode("latin1") and header[0x40:0x64]==CONTENT_ID.encode(), "wrong PS4 package ID"
    PKG.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(candidate,PKG)
    HISTORY.mkdir(parents=True,exist_ok=True)
    previous_release=HISTORY / "0.5.22-release.json"
    previous_manifest=HISTORY / "0.5.22-manifest.json"
    assert not previous_release.exists() and not previous_manifest.exists(), "history already exists"
    shutil.copy2(RECOVERY,previous_release)
    shutil.copy2(MANIFEST,previous_manifest)
    shutil.copy2(SIGNED_STAGE,RECOVERY)
    MANIFEST.write_text(json.dumps({
      "schema":1,"channel":"testing","content_version":24,"app_version":"0.5.24",
      "app_update":{"version":"0.5.24","version_code":524,
                    "release_manifest_url":"https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/recovery/release.json"},
      "announcements":["CohenStore 0.5.24 TEST: Mod Menu Touchpad and plugins.ini inspection fixes. Physical PS4 test pending; keep a known-working installer."]
    },indent=2)+"\\n",encoding="utf8")
    assert verified_envelope(RECOVERY,RECOVERY_KEY)==expected
    assert verified_envelope(previous_release,RECOVERY_KEY)==recovery
    print("PASS: 0.5.24 package hash/size/identity and signed recovery feed; history saved; old feed unchanged")

if __name__ == "__main__":
    main()
