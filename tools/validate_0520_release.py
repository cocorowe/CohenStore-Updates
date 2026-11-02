#!/usr/bin/env python3
"""Verify an offline-signed CohenStore 0.5.20 release before changing the live feed."""
import argparse
import hashlib
import json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

PUBKEY=bytes.fromhex("6d7df4c99728545705a58cb75c6e15aa097f03ab452c86726da359668bbfec41")
HASH="f0b3e9fa550ee37cd896b6e44934ef09cb308e584932607d5a2d74a3f0692cf9"
SIZE=45154304
CONTENT_ID="IV0000-CHST00001_00-COHENSTORE000000"
URL="https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/packages/CohenStore-0.5.20-DEV-TEST.pkg"

def verified_payload(path):
    obj=json.loads(Path(path).read_text())
    msg=obj["signed_payload"].encode()
    Ed25519PublicKey.from_public_bytes(PUBKEY).verify(bytes.fromhex(obj["signature"]),msg)
    return json.loads(msg)

def verify(pkg,release,previous):
    old=verified_payload(previous)
    assert (old["version_code"],old["revision"])==(517,12),"Previous live release changed; stop and reconcile"
    actual=verified_payload(release)
    expected={"schema":1,"channel":"testing","revision":13,"version":"0.5.20",
      "version_code":520,"title_id":"CHST00001","content_id":CONTENT_ID,
      "size_bytes":SIZE,"sha256":HASH,"url":URL}
    assert actual==expected,"Signed metadata differs from verified candidate"
    pkg=Path(pkg)
    assert pkg.stat().st_size==SIZE,"Wrong package size"
    digest=hashlib.sha256()
    with pkg.open("rb") as handle:
        header=handle.read(0x64)
        handle.seek(0)
        while True:
            block=handle.read(1024*1024)
            if not block: break
            digest.update(block)
    assert digest.hexdigest()==HASH,"Wrong package hash"
    assert header[:4]==bytes([0x7f,67,78,84]),"Wrong package header"
    assert header[0x40:0x64].decode("ascii")==CONTENT_ID,"Wrong package identity"
    print("PASS: prior feed, signature, signed metadata, package size, digest and identity")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--package",required=True)
    p.add_argument("--release",required=True)
    p.add_argument("--previous",required=True)
    a=p.parse_args()
    verify(a.package,a.release,a.previous)
