"""Guard additive direct publisher links and the existing source libraries."""
import json
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
NEW_PREFIX='github-publisher:'
class DirectGapfillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=json.loads((ROOT/'catalog/catalog.json').read_text())['items']
        cls.new=[x for x in cls.catalog if x['id'].startswith(NEW_PREFIX)]
    def test_keeps_prior_198_entries_and_appends_only(self):
        self.assertEqual(len(self.catalog),205)
        self.assertEqual(len(self.new),7)
        self.assertEqual(len({x['id'] for x in self.catalog}),len(self.catalog))
        self.assertTrue(all(not x['id'].startswith(NEW_PREFIX) for x in self.catalog[:198]))
        self.assertEqual(self.catalog[198:],self.new)
    def test_publisher_metadata_is_explicitly_unverified(self):
        for item in self.new:
            with self.subTest(item=item['id']):
                self.assertEqual(item['format'],'pkg')
                self.assertIn('Unverified',item['compatibility'])
                self.assertRegex(item['sha256'],r'^[0-9a-f]{64}$')
                self.assertIs(type(item['size_bytes']),int)
                self.assertGreater(item['size_bytes'],10000)
                self.assertEqual(len(item['urls']),1)
                self.assertTrue(item['urls'][0].startswith('https://github.com/'))
                self.assertIn('/releases/download/',item['urls'][0])
                self.assertTrue(item['source_url'].startswith('https://github.com/'))
    def test_source_library_record_counts_are_preserved(self):
        for filename,minimum in [('library-store.json',12205),('library-links.json',18046),('expansion.json',394),('expanded-mods.json',2000)]:
            with self.subTest(filename=filename):
                payload=json.loads((ROOT/'catalog'/filename).read_text())
                self.assertEqual(payload['schema'],1)
                self.assertGreaterEqual(len(payload['items']),minimum)
    def test_provenance_report_lists_each_direct_package(self):
        report=json.loads((ROOT/'reports/direct-source-gapfill-20261031.json').read_text())
        self.assertEqual(report['baseline_catalog_records'],198)
        self.assertEqual(report['proposed_base_records'],205)
        self.assertEqual(len(report['entries']),7)
        self.assertEqual({x['id'] for x in report['entries']},{x['id'] for x in self.new})
if __name__=='__main__':unittest.main()
