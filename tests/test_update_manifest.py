import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class UpdateManifestTests(unittest.TestCase):
    def test_informational_manifest_matches_active_signed_payload(self):
        m=json.loads((ROOT/'update/manifest.json').read_text())
        p=json.loads(json.loads((ROOT/'update/release.json').read_text())['signed_payload'])
        self.assertEqual(m['channel'],p['channel'])
        self.assertEqual(m['app_version'],p['version'])
        self.assertEqual(m['app_update']['version'],p['version'])
        self.assertEqual(m['app_update']['version_code'],p['version_code'])
        self.assertEqual(m['app_update']['release_manifest_url'],'https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/release.json')
