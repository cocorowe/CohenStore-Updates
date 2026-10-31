#!/usr/bin/env python3
"""Report source evidence; optionally download bounded files with catalog SHA-256."""
import argparse, hashlib, http.client, json, os, re, urllib.error, urllib.parse, urllib.request
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
        result['full_transfer']='skipped: no catalog SHA-256'; return
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
    result['scope']='four-byte probe plus complete transfer and catalog SHA-256'

def probe(item,open_url=None,full=False):
    result={'id':item['id'],'title':item['title'],'ok':False,'scope':'four-byte header and advertised size only'}
    if not item.get('urls'):
        result.update(skipped=True,scope='Source/metadata record; no direct file requested')
        return result
    try:
        url=item['urls'][0]; result['host']=safe_url(url)
        result['checked_url']=url
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
            format=item.get('format','pkg')
            if format in ('prx','sprx'): valid=prefix in (b'\x4f\x15\x3d\x1d',b'\x7fELF')
            elif format=='json': valid=prefix.lstrip().startswith(b'{')
            elif format=='zip': valid=prefix==b'PK\x03\x04'
            elif format=='rar': valid=prefix==b'Rar!'
            elif format=='bz2': valid=len(prefix)==4 and prefix[:3]==b'BZh' and prefix[3:4] in b'123456789'
            elif format=='xml': valid=prefix.lstrip().startswith((b'<?xm',b'<Pat')) or prefix.startswith(b'\xef\xbb\xbf<')
            elif format=='gscc': valid=len(prefix)==4 and bool(item.get('sha256'))
            elif format=='bin': valid=len(prefix)==4 and bool(item.get('sha256'))
            else: valid=prefix==b'\x7fCNT'
            if not valid: raise ValueError('Response is not the selected package/plugin format')
            if response.headers.get('Content-Encoding','identity').lower()!='identity': raise ValueError('Encoded file response')
        result['ok']=True
        if full: verify_full(item,result,open_url)
    except urllib.error.HTTPError as error:
        result['error']='HTTP '+str(error.code); result['ok']=False
    except (ValueError,OSError,urllib.error.URLError,http.client.HTTPException) as error:
        result['error']=str(error) if isinstance(error,ValueError) else type(error).__name__; result['ok']=False
    return result

def classify_download_result(result):
    """Evidence for this checked URL, never a claim about every mirror or PS4 installation."""
    if result.get('skipped'):
        return 'Unverified','source-or-metadata-only',False
    if result.get('ok'):
        if result.get('full_transfer')=='verified':
            return 'Working','complete-file-hash-verified',False
        return 'Unverified','header-only-or-skipped',False
    error=str(result.get('error',''))
    match=re.fullmatch(r'HTTP (\d{3})',error)
    status=int(match[1]) if match else None
    if status in (404,410):return 'Unavailable','checked-source-not-found',False
    if status in (401,403,407):return 'Unverified','access-restricted',False
    if status in (408,425,429) or (status is not None and 500<=status<=599):
        return 'Unverified','temporary-source-failure',False
    if error in ('URLError','TimeoutError','ConnectionError','ConnectionResetError','ConnectionAbortedError',
                 'RemoteDisconnected','IncompleteRead','BadStatusLine','HTTPException','OSError'):
        return 'Unverified','temporary-network-failure',False
    return 'Unverified','invalid-response-or-integrity-failure',True

def full_transfer_requested(event_name,event):
    """Second guard if a workflow expression is accidentally edited incorrectly again."""
    value=event.get('inputs',{}).get('full_transfer') if isinstance(event,dict) and isinstance(event.get('inputs',{}),dict) else None
    return event_name=='workflow_dispatch' and (value is True or value=='true')

def make_report(results,checked_at=None):
    for result in results:
        status,reason,blocking=classify_download_result(result)
        result.update(source_status=status,classification=reason,blocking_check_error=blocking)
    counts={name:sum(r['source_status']==name for r in results) for name in ('Working','Unverified','Unavailable')}
    return {'schema':2,'checked_at':checked_at or datetime.now(timezone.utc).isoformat(),
            'scope':'First direct URL per record only. Header probes do not verify complete files; hashes do not prove console installation. Other mirrors and game availability are not inferred.',
            'summary':{'total':len(results),**counts,'blocking':sum(r['blocking_check_error'] for r in results),
                       'host_failures':sum(not r['ok'] and not r.get('skipped',False) and not r['blocking_check_error'] for r in results),
                       'skipped':sum(r.get('skipped',False) for r in results)},'results':results}

def report_exit_code(report,strict_host_health=False):
    if report['summary']['blocking']:return 1
    if strict_host_health and report['summary']['host_failures']:return 2
    return 0

def write_summary(report):
    s=report['summary']
    message=f"Source checks: Working={s['Working']}, Unverified={s['Unverified']}, Unavailable={s['Unavailable']}; integrity errors={s['blocking']}, host failures={s['host_failures']}, skipped={s['skipped']}."
    print(message)
    failures=[r for r in report['results'] if not r['ok'] and not r.get('skipped')]
    for r in failures:print(r['title']+': '+r.get('error','check failed')+' ['+r['classification']+']')
    if os.environ.get('GITHUB_ACTIONS')=='true':
        if s['blocking']:print('::error title=Invalid download response or integrity failure::See the uploaded JSON report; affected files were not verified.')
        if s['host_failures']:print('::warning title=External host availability unresolved::'+str(s['host_failures'])+' checked URLs failed. Temporary failures remain Unverified; other mirrors were not checked.')
    path=os.environ.get('GITHUB_STEP_SUMMARY')
    if path:
        with open(path,'a',encoding='utf-8') as stream:
            stream.write('## Download source evidence\n\n'+message+'\n\n'+report['scope']+'\n\n')
            for r in failures:
                # Avoid Markdown/control injection from upstream titles. Exact URLs stay in the report.
                clean=lambda v:re.sub(r'[\r\n<>`|]',' ',str(v))[:200]
                stream.write('- '+clean(r['title'])+': '+clean(r.get('error'))+' ('+clean(r['classification'])+').\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog',default='catalog/catalog.json')
    parser.add_argument('--report',default='reports/download-check.json')
    parser.add_argument('--full',action='store_true',help='Verify complete downloads with catalog SHA-256, up to 256 MiB each')
    parser.add_argument('--require-manual-dispatch',action='store_true',help='Require GitHub workflow_dispatch and explicit full_transfer=true before any full transfer')
    parser.add_argument('--strict-host-health',action='store_true',help='Exit 2 for host failures, separately from exit 1 for integrity/invalid responses')
    args=parser.parse_args()
    if args.require_manual_dispatch:
        try:event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
        except (KeyError,OSError,ValueError):event={}
        if not args.full or not full_transfer_requested(os.environ.get('GITHUB_EVENT_NAME'),event):
            parser.error('Full transfers require manual workflow_dispatch with full_transfer=true; no URLs were requested')
    catalog=json.loads(Path(args.catalog).read_text())
    with ThreadPoolExecutor(max_workers=2 if args.full else 4) as executor:
        results=list(executor.map(lambda item:probe(item,full=args.full),catalog['items']))
    report=make_report(results)
    path=Path(args.report); path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp'); temp.write_text(json.dumps(report,indent=2)+'\n'); temp.replace(path)
    if args.full: print('Complete files verified against catalog hashes: '+str(sum(r.get('full_transfer')=='verified' for r in results)))
    write_summary(report)
    return report_exit_code(report,args.strict_host_health)

if __name__=='__main__': raise SystemExit(main())



