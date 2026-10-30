#!/usr/bin/env python3
"""Probe four bytes of each catalog file. This is not a full transfer/PS4 test."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request


def safe_url(url):
    parts = urllib.parse.urlsplit(url)
    host = (parts.hostname or '').lower().rstrip('.')
    if parts.scheme != 'https' or not host or parts.username or parts.password:
        raise ValueError('An HTTPS URL without embedded credentials is required')
    if host == 'archive.org' or host.endswith('.archive.org'):
        raise ValueError('Internet Archive is excluded')
    return host


class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, newurl):
        safe_url(newurl)
        return super().redirect_request(request, fp, code, message, headers, newurl)


def probe(item, open_url=None):
    result = {'id': item['id'], 'title': item['title'], 'ok': False,
              'scope': 'four-byte header and advertised size only'}
    try:
        url = item['urls'][0]
        result['host'] = safe_url(url)
        req = urllib.request.Request(url, headers={'Range': 'bytes=0-3',
             'Accept-Encoding': 'identity', 'User-Agent': 'CohenStore-LinkCheck/0.5.2'})
        if open_url is None:
            open_url = urllib.request.build_opener(Redirects()).open
        with open_url(req, timeout=20) as response:
            safe_url(response.geturl())
            result['http_status'] = response.status
            result['range_supported'] = response.status == 206
            if response.status == 206:
                match = re.fullmatch(r'bytes 0-3/(\d+)', response.headers.get('Content-Range', ''))
                if not match: raise ValueError('Invalid partial-response range')
                total = int(match[1])
            elif response.status == 200:
                total = int(response.headers.get('Content-Length', '0'))
            else:
                raise ValueError('Unexpected response status')
            if total < 4 or (item.get('size_bytes') and total != item['size_bytes']):
                raise ValueError('Missing or conflicting file size')
            result['advertised_size_bytes'] = total
            prefix = response.read(4)
            expected = (b'\x4f\x15\x3d\x1d', b'\x7fELF') if item.get('format') == 'prx' else (b'\x7fCNT',)
            if prefix not in expected: raise ValueError('Response is not the selected package/plugin format')
            if response.headers.get('Content-Encoding', 'identity').lower() != 'identity':
                raise ValueError('Encoded file response')
        result['ok'] = True
    except urllib.error.HTTPError as error:
        result['error'] = 'HTTP ' + str(error.code)
    except (ValueError, OSError, urllib.error.URLError) as error:
        # Avoid exposing redirect tokens or credentials through exception URLs.
        result['error'] = str(error) if isinstance(error, ValueError) else type(error).__name__
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', default='catalog/catalog.json')
    parser.add_argument('--report', default='reports/download-check.json')
    args = parser.parse_args()
    catalog = json.loads(Path(args.catalog).read_text())
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(probe, catalog['items']))
    report = {'schema': 1, 'checked_at': datetime.now(timezone.utc).isoformat(),
              'scope': 'Small header probes. Does not establish full-file integrity, console support, or future availability.',
              'results': results}
    path = Path(args.report); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp'); temp.write_text(json.dumps(report, indent=2)+'\n'); temp.replace(path)
    failures = [r for r in results if not r['ok']]
    print(f"Header checks passed: {len(results)-len(failures)}/{len(results)}. Full transfers and PS4 launches are separate checks.")
    for result in failures: print(result['title'] + ': ' + result['error'])
    return bool(failures)


if __name__ == '__main__': raise SystemExit(main())
