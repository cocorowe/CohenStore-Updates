#!/usr/bin/env python3
"""Check catalog headers; optionally download bounded files with publisher SHA-256."""
import argparse, hashlib, json, re, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

MAX_FULL_BYTES = 256 * 1024 * 1024
CHUNK_BYTES = 1024 * 1024

def safe_url(url):
    parts=urllib.parse.urlsplit(url); host=(parts.hostname or '').lower().rstrip('.')
    if parts.scheme!='https' or not host or parts.username or parts.password: raise ValueError('An HTTPS URL without embedded credentials is required')
    return host

class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,request,fp,code,message,headers,newurl):
        safe_url(newurl); return super().redirect_request(request,fp,code,message,headers,newurl)

def make_opener(): return urllib.request.build_opener(Redirects()).open

def verify_full(item,result,open_url):
    digest=item.get('sha256',''); size=item.get('size_bytes')
    if not re.fullmatch(r'[0-9a-fA-F]{64}',digest or ''):
        result['full_transfer']='skipped: no publisher SHA-256'; return
    if type(size) is not int or size<4 or size>MAX_FULL_BYTES:
        result['full_transfer']='skipped: size missing or above 256 MiB safety limit'; return
    req=urllib.request.Request(item['urls'][0],headers={'Accept-Encoding':'identity','User-Agent':'CohenStore-FullVerifier/0.6'})
    h=hashlib.sha256(); count=0
    with open_url(req,timeout=60) as response:
        safe_url(response.geturl())
        if response.status!=200: raise ValueError('Full download did not return HTTP 200')
        if response.headers.get('Content-Encoding','identity').lower()!='identity': raise ValueError('Encoded full-file response')
        while True:
            chunk=response.read(CHUNK_BYTES)
            if not chunk: break
            count+=len(chunk)
            if count>size: raise ValueError('Full download exceeds expected size')
            h.update(chunk)
    if count!=size: raise ValueError('Full download size mismatch')
    actual=h.hexdigest(); result['full_transfer_bytes']=count; result['full_sha256']=actual
    if actual.lower()!=digest.lower(): raise ValueError('Full download SHA-256 mismatch')
    result['full_transfer']='verified'
    result['scope']='four-byte probe plus complete transfer and publisher SHA-256'

def probe(item,open_url=None,full=False):
    result={'id':item['id'],'title':item['title'],'ok':False,'scope':'four-byte header and advertised size only'}
    try:
        url=item['urls'][0]; result['host']=safe_url(url)
        req=urllib.request.Request(url,headers={'Range':'bytes=0-3','Accept-Encoding':'identity','User-Agent':'CohenStore-LinkCheck/0.6'})
        open_url=open_url or make_opener()
        with open_url(req,timeout=30) as response:
            safe_url(response.geturl()); result['http_status']=response.status
            result['range_supported']=response.status==206
            if response.status==206:
                match=re.fullmatch(r'bytes 0-3/(\d+)',response.headers.get('Content-Range',''))
                if not match: raise ValueError('Invalid partial-response range')
                total=int(match[1])
            elif response.status==200: total=int(response.headers.get('Content-Length','0'))
            else: raise ValueError('Unexpected response status')
            if total<4 or (item.get('size_bytes') and total!=item['size_bytes']): raise ValueError('Missing or conflicting file size')
            result['advertised_size_bytes']=total
            prefix=response.read(4)
            expected=(b'\x4f\x15\x3d\x1d',b'\x7fELF') if item.get('format')=='prx' else (b'\x7fCNT',)
            if prefix not in expected: raise ValueError('Response is not the selected package/plugin format')
            if response.headers.get('Content-Encoding','identity').lower()!='identity': raise ValueError('Encoded file response')
        result['ok']=True
        if full: verify_full(item,result,open_url)
    except urllib.error.HTTPError as error:
        result['error']='HTTP '+str(error.code); result['ok']=False
    except (ValueError,OSError,urllib.error.URLError) as error:
        result['error']=str(error) if isinstance(error,ValueError) else type(error).__name__; result['ok']=False
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog',default='catalog/catalog.json')
    parser.add_argument('--report',default='reports/download-check.json')
    parser.add_argument('--full',action='store_true',help='Verify complete downloads with publisher SHA-256, up to 256 MiB each')
    args=parser.parse_args(); catalog=json.loads(Path(args.catalog).read_text())
    with ThreadPoolExecutor(max_workers=2 if args.full else 4) as executor:
        results=list(executor.map(lambda item:probe(item,full=args.full),catalog['items']))
    report={'schema':1,'checked_at':datetime.now(timezone.utc).isoformat(),
      'scope':'Header probes plus bounded full transfers with publisher SHA-256.' if args.full else 'Small header probes; no full-file integrity or console compatibility claim.',
      'results':results}
    path=Path(args.report); path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp'); temp.write_text(json.dumps(report,indent=2)+'\n'); temp.replace(path)
    failures=[r for r in results if not r['ok']]
    if args.full: print('Complete files verified against publisher hashes: '+str(sum(r.get('full_transfer')=='verified' for r in results)))
    print(f"Header checks passed: {len(results)-len(failures)}/{len(results)}. Console launch compatibility is not tested.")
    for result in failures: print(result['title']+': '+result.get('error','check failed'))
    return bool(failures)

if __name__=='__main__': raise SystemExit(main())


