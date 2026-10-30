#!/usr/bin/env python3
"""Refresh an explicit allowlist of developer-published PS4 release assets."""
import json
import re
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECTS=[('skidgfx/PS4-2048','2048','games'),
          ('MDashK/Relic-Hunters-Zero-PS4','Relic Hunters Zero','games')]

def merge_release(catalog, repo, title, category, release):
    assets=release.get('assets',[])
    if not isinstance(assets,list): raise ValueError('Invalid release assets')
    existing={item['id']:item for item in catalog['items']}
    for asset in assets:
        name=asset.get('name','')
        if not isinstance(name,str) or not name.lower().endswith('.pkg'): continue
        url=asset.get('browser_download_url','')
        if not url.startswith('https://github.com/'+repo+'/releases/download/'):
            raise ValueError('Release asset must be served from its developer repository')
        size=asset.get('size')
        if type(size) is not int or not 4<=size<=512*1024**3: raise ValueError('Invalid exact asset size')
        asset_id=asset.get('id')
        if type(asset_id) is not int or asset_id<1: raise ValueError('Invalid asset ID')
        item_id=repo+'/'+str(asset_id)
        if item_id in existing: continue  # Preserve curated metadata for an unchanged asset.
        digest=asset.get('digest') or ''
        sha=digest[7:] if digest.startswith('sha256:') else ''
        if sha and not re.fullmatch('[0-9a-f]{64}',sha): raise ValueError('Invalid publisher digest')
        match=re.search(r'-([A-Z0-9]{9})_00-',name)
        item={'id':item_id,'title':title+' '+release.get('tag_name',''),'category':category,
              'format':'pkg','app_version':release.get('tag_name','').removeprefix('v'),
              'title_ids':[match[1]] if match else [],'source_url':release.get('html_url') or 'https://github.com/'+repo+'/releases',
              'size_bytes':size,'sha256':sha,'urls':[url],
              'note':'Developer-published homebrew. '+('Publisher SHA-256 supplied. ' if sha else 'No publisher SHA-256 supplied. ')+
                     'Full transfer and firmware 13.52 launch have not been tested.'}
        catalog['items'].append(item); existing[item_id]=item
    return catalog

def main():
    target=ROOT/'catalog/catalog.json'
    original=target.read_text(encoding='utf-8'); catalog=json.loads(original)
    if catalog.get('schema')!=1 or not isinstance(catalog.get('items'),list): raise ValueError('Invalid catalog')
    # No write occurs until every allowlisted release has been fetched successfully.
    for repo,title,category in PROJECTS:
        req=urllib.request.Request('https://api.github.com/repos/'+repo+'/releases/latest',headers={'User-Agent':'CohenStore-DeveloperCatalog/0.5','Accept':'application/vnd.github+json'})
        with urllib.request.urlopen(req,timeout=30) as response:
            raw=response.read(5*1024*1024+1)
        if len(raw)>5*1024*1024: raise ValueError('Release metadata too large')
        merge_release(catalog,repo,title,category,json.loads(raw))
    if catalog!=json.loads(original):
        temp=target.with_suffix('.json.tmp');temp.write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8');temp.replace(target)
    print('Developer game catalog refreshed; downloads were not gameplay-tested.')

if __name__=='__main__': main()
