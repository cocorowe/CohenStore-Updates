import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('checks',ROOT/'tools/check_downloads.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceStatusTests(unittest.TestCase):
    def test_header_not_full_transfer(self):
        self.assertEqual(m.classify_download_result({'ok':True})[0],'Unverified')
    def test_full_hash_is_working(self):
        self.assertEqual(m.classify_download_result({'ok':True,'full_transfer':'verified'})[0],'Working')
    def test_temporary_sources_non_blocking(self):
        for err in ('HTTP 500','HTTP 502','HTTP 429','URLError'):
            with self.subTest(err=err):
                s,reason,blocking=m.classify_download_result({'ok':False,'error':err})
                self.assertEqual(s,'Unverified')
                self.assertFalse(blocking)
    def test_missing_url_not_entire_game(self):
        self.assertEqual(m.classify_download_result({'ok':False,'error':'HTTP 404'})[0],'Unavailable')
    def test_corruption_still_fails(self):
        for err in ('Full download SHA-256 mismatch','Invalid partial-response range'):
            with self.subTest(err=err):
                self.assertTrue(m.classify_download_result({'ok':False,'error':err})[2])
