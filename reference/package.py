"""ASIF ZIP-STORED transport and detached Ed25519 manifest signatures."""
import base64
import hashlib
import io
import json
from pathlib import Path
import stat
import zipfile
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from .common import need, Invalid, read, decode, relative, MAX_DOCUMENT, MAX_RESOURCE, MAX_TOTAL
from .core import validate_document
MANIFEST='asif-package.json'
DOMAIN=b'ASIF-PACKAGE-MANIFEST-v1\0'
MAX_MEMBERS=1024

def encode(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode('utf8')

def package_bytes(source):
    source=Path(source);raw=read(source);doc=decode(raw);validated=validate_document(doc,source.parent)
    files={'session.json':raw}
    for id,r in validated['resources'].records.items():
        if r['availability']=='embedded' and 'path' in r:
            need(r['path'].casefold() not in ('session.json',MANIFEST),'reserved package path')
            files[r['path']]=validated['resources'].bytes(id)
    need(len(files)+1<=MAX_MEMBERS,'package member limit')
    inventory=[{'path':name,'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest()} for name,content in sorted(files.items())]
    manifest=encode({'package_version':'0.1','session':'session.json','files':inventory})
    files[MANIFEST]=manifest
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_STORED) as archive:
        for name,content in sorted(files.items()):
            item=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));item.create_system=3;item.external_attr=(stat.S_IFREG|0o600)<<16
            archive.writestr(item,content)
    raw_archive=stream.getvalue();need(len(raw_archive)<=MAX_TOTAL+MAX_DOCUMENT,'package byte limit')
    return raw_archive

def inspect_package(raw):
    need(len(raw)<=MAX_TOTAL+MAX_DOCUMENT,'package byte limit')
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            items=archive.infolist();need(len(items)<=MAX_MEMBERS,'package member limit');files={};folded=set();total=0
            for item in items:
                name=item.filename;relative(name)
                need(item.orig_filename==name and '\0' not in name,'invalid package name')
                need(name.casefold() not in folded,'duplicate/colliding package member');folded.add(name.casefold())
                need(not item.is_dir() and stat.S_IFMT(item.external_attr>>16) in (0,stat.S_IFREG),'nonregular package member')
                need(item.compress_type==zipfile.ZIP_STORED and not item.flag_bits&1,'unsupported package encoding')
                limit=MAX_DOCUMENT if name in (MANIFEST,'session.json') else MAX_RESOURCE
                need(item.file_size<=limit,'package member byte limit');total+=item.file_size;need(total<=MAX_TOTAL,'package total limit')
                with archive.open(item) as f:content=f.read(limit+1)
                need(len(content)==item.file_size,'package member size mismatch');files[name]=content
    except (zipfile.BadZipFile,RuntimeError,NotImplementedError) as exc:raise Invalid('invalid ZIP container') from exc
    need(MANIFEST in files and 'session.json' in files,'missing package metadata')
    manifest=decode(files[MANIFEST]);need(manifest.get('package_version')=='0.1' and manifest.get('session')=='session.json','unsupported package manifest')
    inventory=manifest.get('files');need(isinstance(inventory,list),'invalid inventory');seen=set()
    for item in inventory:
        need(isinstance(item,dict) and set(('path','bytes','sha256'))<=item.keys(),'invalid inventory record')
        name=item['path'];relative(name);need(name!=MANIFEST and name not in seen,'duplicate inventory');seen.add(name)
        need(name in files,'missing inventoried member');content=files[name]
        need(isinstance(item['bytes'],int) and not isinstance(item['bytes'],bool) and item['bytes']==len(content),'inventory length mismatch')
        need(item['sha256']==hashlib.sha256(content).hexdigest(),'inventory digest mismatch')
    need(seen==files.keys()-{MANIFEST},'unlisted package member')
    for name in files:
        for other in files:need(not other.startswith(name+'/'),'package file/directory collision')
    # Check resource closure without extracting or accessing the network/host filesystem.
    doc=decode(files['session.json'])
    from .core import SCHEMA
    SCHEMA.validate(doc)
    expected={'session.json',MANIFEST}
    for r in doc['resources']:
        if r['availability']=='embedded' and 'path' in r:
            name=r['path'];relative(name);need(name not in ('session.json',MANIFEST),'reserved package resource path')
            need(name in files,'missing packaged resource')
            need(len(files[name])==r['bytes'] and hashlib.sha256(files[name]).hexdigest()==r['sha256'],'packaged resource integrity')
            expected.add(name)
    need(expected==files.keys(),'package has unrelated files')
    return files

def signature(raw_archive,private_key):
    files=inspect_package(raw_archive);digest=hashlib.sha256(files[MANIFEST]).digest()
    key=Ed25519PrivateKey.from_private_bytes(private_key);public=key.public_key().public_bytes_raw()
    return encode({'signature_version':'0.1','algorithm':'Ed25519','manifest_sha256':digest.hex(),'key_id':'sha256:'+hashlib.sha256(public).hexdigest(),'signature':base64.b64encode(key.sign(DOMAIN+digest)).decode('ascii')})

def verify_signature(raw_archive,raw_signature,trusted_public_key):
    files=inspect_package(raw_archive);sig=decode(raw_signature);digest=hashlib.sha256(files[MANIFEST]).digest()
    need(sig.get('signature_version')=='0.1' and sig.get('algorithm')=='Ed25519','unsupported signature')
    need(sig.get('manifest_sha256')==digest.hex(),'signed manifest mismatch')
    need(sig.get('key_id')=='sha256:'+hashlib.sha256(trusted_public_key).hexdigest(),'untrusted signing key')
    try:Ed25519PublicKey.from_public_bytes(trusted_public_key).verify(base64.b64decode(sig['signature'],validate=True),DOMAIN+digest)
    except (InvalidSignature,ValueError,KeyError) as exc:raise Invalid('invalid package signature') from exc
    return {'status':'verified','key_id':sig['key_id'],'manifest_sha256':digest.hex(),'scope':'package bytes under caller-supplied trusted key; no continuation claim'}

def write_new(path,content):
    path=Path(path)
    with path.open('xb') as stream:stream.write(content)
