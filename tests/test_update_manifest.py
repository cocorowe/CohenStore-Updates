import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class UpdateManifestTests(unittest.TestCase):
    def test_matches_signed_payload_metadata(self):
        m=json.loads((ROOT/'update/manifest.json').read_text())
        r=json.loads((ROOT/'update/release.json').read_text())
        p=json.loads(r['signed_payload'])
        self.assertEqual(m['channel'],p['channel'])
        self.assertEqual(m['app_version'],p['version'])
        self.assertEqual(m['app_update']['version'],p['version'])
        self.assertEqual(m['app_update']['version_code'],p['version_code'])
    def test_opt_in_full_check(self):
        source=(ROOT/'.github/workflows/check-downloads.yml').read_text()
        self.assertIn("github.event_name == 'workflow_dispatch'",source)
        self.assertIn('inputs.full_transfer == true',source)
        self.assertNotIn(r'if: \${{',source)
