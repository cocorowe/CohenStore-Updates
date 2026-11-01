"""Verify all uploaded bytes before changing any public active-feed files."""
from pathlib import Path
import hashlib,json,struct,shutil
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

stage=Path('update/staging/0.5.17')
key=Ed25519PublicKey.from_public_bytes(bytes.fromhex('6d7df4c99728545705a58cb75c6e15aa097f03ab452c86726da359668bbfec41'))
def verified(path):
    envelope=json.loads(path.read_text())
    key.verify(bytes.fromhex(envelope['signature']),envelope['signed_payload'].encode())
    return json.loads(envelope['signed_payload'])
previous=verified(Path('update/release.json'))
assert (previous['version_code'],previous['revision'],previous['sha256'])==(516,11,'22d9d9013c6afeb8011292fbf65ee09df1172a45bb1270375ae54cca3c5d645b'), 'Unexpected previous live release'
expected=json.loads((stage/'expected.json').read_text())
parts=sorted(stage.glob('*.pkgpart'))
assert [p.name for p in parts]==list(expected['parts']), 'Missing/extra package parts'
for part in parts:assert hashlib.sha256(part.read_bytes()).hexdigest()==expected['parts'][part.name],part.name
raw=b''.join(p.read_bytes() for p in parts)
assert len(raw)==expected['package_size']==17956864
assert hashlib.sha256(raw).hexdigest()==expected['package_sha256']=='cb0ae0ed7a3bc6f229df91914cb4826197820a82c9cd06e04de82387f80e1c23'
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==expected['package_git_sha']
assert raw[:4]==b'\x7fCNT' and raw[0x40:0x64]==b'IV0000-CHST00001_00-COHENSTORE000000'
count,table=struct.unpack_from('>I',raw,0x10)[0],struct.unpack_from('>I',raw,0x18)[0]
assert 0<count<4096 and table+count*32<=len(raw)
sfo=None
for i in range(count):
    row=struct.unpack_from('>8I',raw,table+i*32)
    if row[0]==0x1000:
        assert row[4]+row[5]<=len(raw);sfo=raw[row[4]:row[4]+row[5]]
assert sfo and sfo[:4]==b'\0PSF'
_,version,keys,values,n=struct.unpack_from('<5I',sfo)
assert version==0x101 and n<1024 and 20+n*16<=len(sfo)
fields={}
for i in range(n):
    ko,fmt,length,capacity,vo=struct.unpack_from('<HHIII',sfo,20+i*16)
    assert length<=capacity and values+vo+length<=len(sfo)
    name=sfo[keys+ko:sfo.index(b'\0',keys+ko)].decode()
    if name in ('TITLE_ID','CONTENT_ID','APP_VER'):fields[name]=sfo[values+vo:values+vo+length].rstrip(b'\0').decode()
assert fields=={'TITLE_ID':'CHST00001','CONTENT_ID':'IV0000-CHST00001_00-COHENSTORE000000','APP_VER':'01.17'},fields
release=verified(stage/'release.json')
assert (release['version'],release['version_code'],release['revision'],release['channel'],release['schema'])==('0.5.17',517,12,'testing',1)
assert release['sha256']==hashlib.sha256(raw).hexdigest() and release['size_bytes']==len(raw)
assert release['title_id']==fields['TITLE_ID'] and release['content_id']==fields['CONTENT_ID']
assert release['url']=='https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/packages/CohenStore-0.5.17-TEST.pkg'
manifest=json.loads((stage/'manifest.json').read_text())
assert manifest['app_version']==manifest['app_update']['version']=='0.5.17' and manifest['app_update']['version_code']==517
assert manifest['content_version']>json.loads(Path('update/manifest.json').read_text())['content_version']
assert manifest['channel']=='testing' and manifest['app_update']['release_manifest_url']=='https://raw.githubusercontent.com/cocorowe/CohenStore-Updates/main/update/release.json'
for name,minimum in [('catalog.json',207),('library-store.json',12205),('library-links.json',18046)]:
    data=json.loads(Path('catalog',name).read_text());assert len(data['items'])>=minimum
    assert len({i['id'] for i in data['items']})==len(data['items'])
Path('update/packages/CohenStore-0.5.17-TEST.pkg').write_bytes(raw)
for source,target in [('release.json','update/release.json'),('manifest.json','update/manifest.json'),('repository-readme.md','README.md'),('instructions.md','update/README.md'),('release-0517.json','reports/release-0517.json')]:shutil.copyfile(stage/source,target)
print('Verified full PKG, signing identity, embedded SFO, release monotonicity and preserved catalog counts. PS4 hardware testing remains pending.')
