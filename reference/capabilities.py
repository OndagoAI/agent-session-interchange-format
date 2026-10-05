"""Exact-byte destination snapshot evidence; no destination probing or authorization."""
import base64
import binascii
from datetime import datetime
from decimal import Decimal
import hashlib
import json
import re
from pathlib import Path
from .common import need, Invalid, Unsupported, decode, unique
from .core import Validator

FORMAT='asif.destination-capabilities/0.1'
MAX_SNAPSHOT=1024*1024
schema=json.loads((Path(__file__).resolve().parents[1]/'schemas/continuation-report.schema.json').read_text())
SNAPSHOT=Validator({'$ref':'#/$defs/capability_snapshot','$defs':schema['$defs']})
KINDS={'dependency':'dependency','configuration':'configuration','instruction':'configuration','capability':'capability','policy':'policy','model':'model','context':'model','workspace':'workspace','service':'service','operation':'operation','native_import':'native_import','environment':'environment','checkpoint_requirement':'environment','environment_requirement':'environment'}

def time(value):
    need(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2})',value) is not None,'invalid snapshot time')
    if not value.endswith('Z'):need(int(value[-5:-3])<24 and int(value[-2:])<60,'invalid snapshot time')
    try:out=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:raise Invalid('invalid snapshot time') from None
    need(out.tzinfo is not None,'snapshot time needs timezone');return out

def same(a,b):
    # JSON equality preserves boolean/number distinctions, including extensions.
    if isinstance(a,bool) or isinstance(b,bool):return type(a) is type(b) and a==b
    if isinstance(a,dict) and isinstance(b,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    if isinstance(a,(int,float,Decimal)) and isinstance(b,(int,float,Decimal)):return Decimal(str(a))==Decimal(str(b))
    return type(a) is type(b) and a==b

def snapshot_bytes(report):
    envelope=report['destination']['capabilities_snapshot']
    if envelope['format']!=FORMAT:raise Unsupported('unsupported capability snapshot format')
    if envelope['availability']!='supplied':raise Unsupported('capability snapshot unavailable')
    need(len(envelope['data'])<=4*((MAX_SNAPSHOT+2)//3),'capability snapshot byte limit')
    try:raw=base64.b64decode(envelope['data'],validate=True)
    except (ValueError,binascii.Error):raise Invalid('invalid snapshot base64') from None
    need(base64.b64encode(raw).decode()==envelope['data'],'noncanonical snapshot base64')
    need(0<len(raw)<=MAX_SNAPSHOT and len(raw)==envelope['bytes'],'capability snapshot byte count')
    need(hashlib.sha256(raw).hexdigest()==report['destination']['capabilities_sha256'],'capability snapshot digest mismatch')
    return raw

def inspect_capabilities(report,plan,now,current_snapshot=None,doc=None):
    raw=snapshot_bytes(report);need(not raw.startswith(b'\xef\xbb\xbf'),'snapshot UTF-8 BOM forbidden')
    snapshot=decode(raw)
    need(isinstance(snapshot,dict),'snapshot must be an object')
    need(isinstance(snapshot.get('snapshot_version'),str),'missing or invalid snapshot version')
    if snapshot['snapshot_version']!='0.1':raise Unsupported('unsupported capability snapshot version')
    SNAPSHOT.validate(snapshot)
    destination=report['destination'];envelope=destination['capabilities_snapshot']
    need(snapshot['destination_id']==destination['id'] and same(snapshot['runtime'],destination['runtime']),'snapshot destination mismatch')
    need(snapshot['evaluation_mode']==report['evaluation_mode'],'snapshot evaluation mode mismatch')
    need(time(snapshot['observed_at'])<=time(report['assessed_at'])<time(report['expires_at'])<=time(snapshot['expires_at']),'snapshot assessment interval mismatch')
    need(time(snapshot['observed_at'])<=now<time(snapshot['expires_at']),'stale capability snapshot')
    evidence=unique(report['evidence']);e=evidence.get(envelope['evidence_id'])
    need(e is not None,'missing snapshot evidence')
    need(e['producer']==snapshot['producer'] and time(e['time'])==time(snapshot['observed_at']),'snapshot evidence mismatch')
    need(e['kind']==('synthetic' if snapshot['evaluation_mode']=='synthetic' else 'inspection'),'snapshot evidence kind mismatch')
    components=unique(snapshot['components'])
    for a in report['assessments']:
        ids=a['component_ids'];need(set(ids)<=components.keys(),'missing snapshot component')
        if a['status'] not in ('supported','adapted'):continue
        kind=a['subject']['kind'];expected=KINDS.get(kind)
        bound=[components[id] for id in ids]
        need(all(c['status']=='available' for c in bound),'unavailable snapshot component claimed supported')
        if expected:
            selected=[c for c in bound if c['kind']==expected]
            need(len(selected)==1,'missing or ambiguous destination component binding');c=selected[0]
        else:
            if kind=='feature':need(a['subject']['id'] in snapshot['supported_features'],'snapshot feature unsupported')
            continue
        if kind=='dependency' and a['status']=='supported':
            r=a.get('resolved',{});need(r.get('identity')==c['identity'] and r.get('version')==c['version'],'snapshot dependency mismatch')
        elif kind in ('model','context'):
            m=report['model_assessment'];need(same(m['target'],c['model']),'snapshot model mismatch')
            if m['fit']=='fits':need(m['tokenizer']==c['tokenizer'] and m['input_limit']==c['input_limit'],'snapshot model budget mismatch')
            if kind=='model' and a['status']=='supported':need(set(plan['model_requirements']['capabilities'])<=set(c['capabilities']) and set(plan['model_requirements']['media_types'])<=set(c['media_types']),'snapshot model capability mismatch')
        elif kind=='service' and a['status']=='supported':
            r=a.get('resolved',{});need(all(same(r.get(k),c[k]) for k in ('account','audience','endpoint')) and set(r.get('scopes',[]))<=set(c['scopes']) and set(r.get('secret_handles',[]))<=set(c['secret_handles']),'snapshot service mismatch')
        elif kind=='workspace':
            workspace=next(w for w in doc['continuation']['workspaces'] if w['id']==a['subject']['id'])
            need(c['root_id']==workspace['root_id'],'snapshot workspace root mismatch')
            bindings={b['root_id']:b for b in report['path_bindings']};b=bindings.get(c['root_id'])
            need(b is not None and all(b[k]==c[k] for k in ('destination_path','case_sensitive','unicode_normalization')),'snapshot workspace mismatch')
        elif kind=='operation' and a['status']=='supported' and plan['next_action']['kind']=='reconcile_operation':
            r=a.get('resolved',{});need(all(same(r.get(k),c[k]) for k in ('recovery_strategy','external_identity')),'snapshot operation mismatch')
    if current_snapshot is not None:
        need(current_snapshot==raw,'destination capabilities changed; reassessment required')
    return current_snapshot is not None
