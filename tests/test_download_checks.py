import importlib.util, hashlib, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('checks',Path(__file__).resolve().parents[1]/'tools/check_downloads.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Response:
    def __init__(self,status=206,headers=None,body=b'\x7fCNT'+b'x'*4092):
        self.status=status;self.headers=headers or {'Content-Range':'bytes 0-3/4096'};self.body=body;self.offset=0
    def geturl(self): return 'https://developer.example/file.pkg'
    def __enter__(self): return self
    def __exit__(self,*_): return False
    def read(self,n):
        chunk=self.body[self.offset:self.offset+n];self.offset+=len(chunk);return chunk
class DownloadChecksTests(unittest.TestCase):
    def test_mod_formats_are_probed_as_their_own_types(self):
        for format,prefix in [('sprx',b'\x4f\x15\x3d\x1d'),('json',b'{\n  '),('zip',b'PK\x03\x04')]:
            item={'id':'test','title':'Test','format':format,'urls':['https://developer.example/file'],'size_bytes':4096}
            self.assertTrue(m.probe(item,lambda *a,**k:Response(body=prefix+b'x'*4092))['ok'])

    def test_html_is_not_a_cheat_file(self):
        item={'id':'test','title':'Test','format':'json','urls':['https://developer.example/file'],'size_bytes':4096}
        self.assertFalse(m.probe(item,lambda *a,**k:Response(body=b'<htm'+b'x'*4092))['ok'])

    def test_patch_and_menu_archive_formats(self):
        for format,prefix in [('xml',b'<?xm'),('bz2',b'BZh9'),('rar',b'Rar!')]:
            item={'id':'test','title':'Test','format':format,'urls':['https://developer.example/file'],'size_bytes':4096}
            self.assertTrue(m.probe(item,lambda *a,**k:Response(body=prefix+b'x'*4092))['ok'])

    def test_raw_payload_probe_requires_catalog_hash(self):
        item={'id':'test','title':'Test','format':'bin','urls':['https://developer.example/file'],'size_bytes':4096}
        self.assertFalse(m.probe(item,lambda *a,**k:Response())['ok'])
    def probe(self,response,**kwargs):
        item={'id':'test','title':'Test','urls':['https://developer.example/a.pkg'],'size_bytes':4096}
        return m.probe(item,lambda *a,**k:response,**kwargs)
    def test_normal_probe(self): self.assertTrue(self.probe(Response())['ok'])
    def test_webpage_rejected(self): self.assertFalse(self.probe(Response(body=b'<htm'+b'x'*4092))['ok'])
    def test_conflicting_size_rejected(self): self.assertFalse(self.probe(Response(headers={'Content-Range':'bytes 0-3/1234'}))['ok'])
    def test_missing_range_rejected(self): self.assertFalse(self.probe(Response(headers={'Content-Length':'4'}))['ok'])
    def test_range_ignored_is_reported(self):
        r=self.probe(Response(status=200,headers={'Content-Length':'4096'}));self.assertTrue(r['ok']);self.assertFalse(r['range_supported'])
    def test_unsafe_urls_rejected(self):
        for url in ['https://user:pass@developer.example/a','http://developer.example/a']:
            with self.assertRaises(ValueError):m.safe_url(url)
    def test_archive_hosts_allowed(self):
        self.assertEqual(m.safe_url('https://archive.org/download/item/a.pkg'),'archive.org')
        self.assertEqual(m.safe_url('https://dn721302.ca.archive.org/a.pkg'),'dn721302.ca.archive.org')
    def test_full_hash_verified(self):
        body=b'\x7fCNT'+b'x'*4092; item={'id':'x','title':'x','urls':['https://developer.example/a.pkg'],'size_bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
        responses=[Response(body=body),Response(status=200,headers={'Content-Length':str(len(body))},body=body)]
        r=m.probe(item,lambda *a,**k:responses.pop(0),full=True)
        self.assertTrue(r['ok']);self.assertEqual(r['full_transfer'],'verified')
    def test_full_hash_mismatch_fails(self):
        body=b'\x7fCNT'+b'x'*4092; item={'id':'x','title':'x','urls':['https://developer.example/a.pkg'],'size_bytes':len(body),'sha256':'0'*64}
        responses=[Response(body=body),Response(status=200,headers={'Content-Length':str(len(body))},body=body)]
        r=m.probe(item,lambda *a,**k:responses.pop(0),full=True)
        self.assertFalse(r['ok']);self.assertIn('SHA-256 mismatch',r['error'])



