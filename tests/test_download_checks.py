import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('checks',Path(__file__).resolve().parents[1]/'tools/check_downloads.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Response:
    def __init__(self, status=206, headers=None, prefix=b'\x7fCNT'):
        self.status=status;self.headers=headers or {'Content-Range':'bytes 0-3/4096'};self.prefix=prefix
    def geturl(self):return 'https://developer.example/file.pkg'
    def __enter__(self):return self
    def __exit__(self,*_):return False
    def read(self,n):
        if n!=4:raise AssertionError('Probe tried to download more than four bytes')
        return self.prefix

class DownloadChecksTests(unittest.TestCase):
    def probe(self,response):
        return m.probe({'id':'test','title':'Test','urls':['https://developer.example/a.pkg'],'size_bytes':4096},lambda *a,**k:response)
    def test_reads_only_four_bytes_and_matches_size(self):self.assertTrue(self.probe(Response())['ok'])
    def test_webpage_rejected(self):self.assertFalse(self.probe(Response(prefix=b'<htm'))['ok'])
    def test_conflicting_size_rejected(self):self.assertFalse(self.probe(Response(headers={'Content-Range':'bytes 0-3/1234'}))['ok'])
    def test_missing_range_rejected(self):self.assertFalse(self.probe(Response(headers={'Content-Length':'4'}))['ok'])
    def test_range_ignored_is_reported(self):
        r=self.probe(Response(status=200,headers={'Content-Length':'4096'}));self.assertTrue(r['ok']);self.assertFalse(r['range_supported'])
    def test_archive_and_credentials_rejected(self):
        for url in ['https://archive.org/a','https://web.archive.org/a','https://user:pass@developer.example/a','http://developer.example/a']:
            with self.assertRaises(ValueError):m.safe_url(url)
