#!/usr/bin/env python3
"""Fail before a release silently replaces CohenStore's catalog with older data."""
import argparse
import json
import pathlib
import sys

MIN_COUNTS = {
    "catalog/catalog.json": 207,
    "catalog/library-store.json": 12205,
    "catalog/library-links.json": 18046,
}

def count_entries(payload, path):
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in ("items", "entries", "records", "games", "packages"):
            if isinstance(payload.get(key), list):
                return len(payload[key])
        # An ID-keyed mapping is valid, but exclude schema/metadata wrappers.
        if payload and all(isinstance(v, dict) for v in payload.values()):
            return len(payload)
    raise ValueError(f"{path}: unknown catalog schema; inspect before publishing")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path("."))
    args = parser.parse_args()
    failed = False
    for relative, minimum in MIN_COUNTS.items():
        path = args.root / relative
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
            count = count_entries(payload, relative)
            if count < minimum:
                print(f"FAIL {relative}: {count} entries; expected at least {minimum}")
                failed = True
            else:
                print(f"PASS {relative}: {count} entries (minimum {minimum})")
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
            print(f"FAIL {relative}: {exc}")
            failed = True
    if failed:
        print("RELEASE BLOCKED: preserve the existing catalogs and reconcile source/package inputs.")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
