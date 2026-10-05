"""Synthetic destination declarations. Never inspect a real runtime or credentials."""
import base64,copy,hashlib,json
from reference.capabilities import FORMAT,KINDS

def bind_snapshot(doc,report):
    plan=next(p for p in doc['continuation']['plans'] if p['id']==report['source']['plan_id'])
    components=[]
    for a in report['assessments']:
        subject=a['subject'];kind=KINDS.get(subject['kind']);a['component_ids']=[]
        if kind is None:continue
        id='component-'+str(len(components)+1)
        c={'id':id,'kind':kind,'identity':'example.'+subject['kind']+'.'+subject['id'],'version':'1','revision':'synthetic-state-1','status':'available'}
        resolved=a.get('resolved',{})
        if kind=='dependency':c.update(identity=resolved.get('identity',a['subject']['id']),version=resolved.get('version','1'))
        if kind=='dependency' and a['status']=='adapted':
            mapping=next(t for t in report['transformations'] if t['subject']==subject)
            # These authored example mappings explicitly target version 2.
            c.update(identity=mapping['target'].rsplit('/',1)[0],version='2')
        if kind=='native_import':c.update(identity=report['destination']['runtime']['adapter']['id'],version=report['destination']['runtime']['adapter']['version'])
        if kind=='model':
            m=report['model_assessment'];c.update(identity=m['target']['provider']+'/'+m['target']['id'],version=m['target']['revision'],model=copy.deepcopy(m['target']),tokenizer=m['tokenizer'],input_limit=m['input_limit'],media_types=plan['model_requirements']['media_types'],capabilities=plan['model_requirements']['capabilities'])
        if kind=='service':
            src=next(s for s in doc['continuation']['service_bindings'] if s['id']==subject['id'])
            c.update(account=copy.deepcopy(resolved.get('account',src['account'])),audience=resolved.get('audience',src['audience']),scopes=resolved.get('scopes',[]),secret_handles=resolved.get('secret_handles',[]),endpoint=resolved.get('endpoint',src['endpoint']['locator']))
            if a['status']=='unresolved':c['status']='unknown'
        if kind=='workspace':
            w=next(w for w in doc['continuation']['workspaces'] if w['id']==subject['id'])
            binding=next((b for b in report['path_bindings'] if b['root_id']==w['root_id']),None)
            c.update(binding or {'root_id':w['root_id'],'destination_path':'/work/project','case_sensitive':True,'unicode_normalization':'none'})
        if kind=='operation':
            op=next(o for o in doc['continuation']['operations'] if o['id']==subject['id'])
            c.update(recovery_strategy=op['recovery']['strategy'],external_identity=copy.deepcopy(op['external_identity']))
            if a['status']=='unresolved':c['status']='unknown'
        components.append(c);a['component_ids']=[id]
    snapshot={'snapshot_version':'0.1','id':'snapshot-'+report['id'],'destination_id':report['destination']['id'],'producer':'asif-examples','evaluation_mode':'synthetic','observed_at':report['assessed_at'],'expires_at':report['expires_at'],'runtime':copy.deepcopy(report['destination']['runtime']),'runtime_revision':'synthetic-runtime-1','supported_features':doc['required_features'],'components':components}
    raw=(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n').encode()
    report['destination']['capabilities_sha256']=hashlib.sha256(raw).hexdigest()
    report['destination']['capabilities_snapshot']={'format':FORMAT,'availability':'supplied','data':base64.b64encode(raw).decode(),'bytes':len(raw),'evidence_id':'snapshot-inspection'}
    report['evidence']=[e for e in report['evidence'] if e['id']!='snapshot-inspection']+[{'id':'snapshot-inspection','producer':'asif-examples','time':snapshot['observed_at'],'kind':'synthetic','detail':'Authored destination snapshot; no live inspection or credential lookup.'}]
    return raw
