"""Executable local reference checks; no independent or live-agent evidence."""
import base64, copy, hashlib, io, json, sys, tempfile, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reference.common import Invalid, Unsupported, decode, encode, load, pointer, relative
from reference.core import validate_document, history_state
from reference.continuation import inspect_session
from reference.context import predicate, resolve_configuration, evaluate_policy, reconstruct_request
from reference.workspace import restore, workspace_states
from reference.package import package_bytes, inspect_package, signature, verify_signature
from reference.redaction import audit
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from jsonschema.exceptions import ValidationError
ROOT=Path(__file__).resolve().parents[1];results=[]
def check(name,fn):
    fn();results.append({'case':name,'passed':True})
def rejects(fn,expected):
    try:fn()
    except (Invalid,ValidationError) as exc:assert expected in str(exc),(expected,str(exc))
    else:raise AssertionError('accepted invalid input: '+expected)
def equal(a,b):assert a==b,(a,b)
for file in sorted((ROOT/'examples').rglob('*.session.json')):
    check('validate-'+file.stem,lambda f=file:validate_document(load(f)[0],f.parent))

def session_case(case):
    d=load(ROOT/'examples'/case['fixture'])[0]
    for edit in case['edits']:
        target=d
        for key in edit['path'][:-1]:target=target[int(key) if isinstance(target,list) else key]
        key=int(edit['path'][-1]) if isinstance(target,list) else edit['path'][-1]
        if edit.get('remove'):del target[key]
        elif isinstance(target,list) and key==len(target):target.append(copy.deepcopy(edit['value']))
        else:target[key]=copy.deepcopy(edit['value'])
    if case.get('schema_error'):
        try:validate_document(d,ROOT/'examples')
        except ValidationError:pass
        else:raise AssertionError('accepted structurally invalid task event')
    elif 'error' in case:
        rejects(lambda:validate_document(d,ROOT/'examples'),case['error'])
    else:
        validate_document(d,ROOT/'examples')
        events={e['id']:e for e in d['events']}
        if 'task_states' in case:
            partial=next(c['status'] for c in d['coverage'] if c['scope']=='tasks')=='partial'
            for branch in d['branches']:
                if branch['id'] not in case['task_states']:continue
                state=history_state([events[id] for id in branch['event_ids']],partial_tasks=partial)
                actual={key:state[key] for key in ('task_dependencies','task_history_gaps')}
                actual['tasks']={id:{k:task[k] for k in ('revision','status')} for id,task in state['tasks'].items()}
                equal(actual,case['task_states'][branch['id']])
            return
        external_calls={b['id']:b['descriptor'] for b in d.get('external_bindings',[]) if b['kind']=='call'}
        state=history_state([events[id] for id in d['branches'][0]['event_ids']],external_calls)
        actual={'calls':{id:{k:call[k] for k in ('arguments','arguments_status')} for id,call in state['calls'].items()},'closed_calls':state['closed_calls']}
        equal(actual,case['expected'])

for case in json.loads((ROOT/'tests/tool-call-progression-cases.json').read_text())['cases']:
    check('call-progression-'+case['name'],lambda c=case:session_case(c))
for case in json.loads((ROOT/'tests/task-semantics-cases.json').read_text())['cases']:
    check('task-semantics-'+case['name'],lambda c=case:session_case(c))

def preserved_partial_capture():
    partial=load(ROOT/'examples/tool-call-partial.session.json')[0]
    completed=load(ROOT/'examples/tool-call-completed.session.json')[0]
    equal(partial['session']['id'],completed['session']['id'])
    assert partial['capture']['id']!=completed['capture']['id']
    for collection in ('events','resources','streams','contexts'):
        later={x['id']:x for x in completed[collection]}
        for record in partial[collection]:equal(record,later[record['id']])
    validated=validate_document(completed,ROOT/'examples')
    inputs=reconstruct_request(completed,validated,'context-completed')['inputs']
    calls=[item for item in inputs if item['kind']=='tool_call']
    equal(len(calls),1);equal(calls[0]['arguments'],{'document_id':'meeting-42'})
    equal(calls[0]['source_events'],[{'event_id':'call-complete'}])
check('call-progression-retains-immutable-evidence',preserved_partial_capture)

folder=ROOT/'examples/continuation';doc,raw=load(folder/'another-computer.session.json');validated=validate_document(doc,folder)
check('strict-duplicate-key',lambda:rejects(lambda:decode(b'{"a":1,"a":2}'),'duplicate JSON key'))
check('strict-nonfinite',lambda:rejects(lambda:decode(b'{"a":NaN}'),'non-JSON numeric constant'))
check('bounded-depth',lambda:rejects(lambda:decode(('['*130+'0'+']'*130).encode()),'nesting limit'))
check('unknown-number-preservation',lambda:equal(decode(encode(decode(b'{"future":0.123456789012345678901234567890}'))),decode(b'{"future":0.123456789012345678901234567890}')))
check('pointer-escaped-keys',lambda:equal(pointer({'a/b':{'~':[2]}},'/a~1b/~0/0'),2))
check('pointer-invalid-escape',lambda:rejects(lambda:pointer({},'/a~2'),'invalid pointer escape'))
for path in ['../a','/tmp/a','a\\b','C:a','NUL','a/../b','a.']:
    check('path-'+path,lambda p=path:rejects(lambda:relative(p),'path'))
check('request-typed-inputs',lambda:equal(reconstruct_request(doc,validated,doc['contexts'][0]['id'])['inputs'],doc['contexts'][0]['inputs']))
check('configuration-order',lambda:equal(resolve_configuration(doc,doc['configurations'][0]['id'],{'root_id':doc['continuation']['workspaces'][0]['root_id'],'relative_path':''})['instruction_ids'],doc['continuation']['configuration_bindings'][0]['effective_order']))
check('predicate-component-prefix',lambda:equal(predicate({'path_prefix':'src'},{'relative_path':'src-other/file'}),False))
check('predicate-combination',lambda:equal(predicate({'all':[{'event_kind_in':['tool_call']},{'not':{'root_is':'other'}}]},{'event_kind':'tool_call','root_id':'work'}),True))
check('predicate-unknown',lambda:rejects(lambda:predicate({'execute':'anything'},{}),'unknown predicate'))
policy=lambda effect,enforcing=True:{'id':effect,'type':'asif.policy/0.1','enforcing':enforcing,'definition':{'effect':effect,'tool_ids':['*'],'scope':{'kind':'global'},'activation':{'kind':'always'}}}
check('policy-deny-precedence',lambda:equal(evaluate_policy({'policies':[policy('allow'),policy('deny')]},{})['decision'],'deny'))
check('policy-default-ask',lambda:equal(evaluate_policy({'policies':[]},{})['decision'],'ask'))
def event(id,kind,data,**kw):return {'id':id,'kind':kind,'data':data,**kw}
request=event('q','decision_request',{'request_id':'q','options':[{'id':'yes','label':'Yes'}]})
answer=event('a','decision_resolution',{'request_id':'q','outcome':'allowed'})
change=event('b','decision_resolution',{'request_id':'q','outcome':'denied'})
check('contradictory-decisions',lambda:rejects(lambda:history_state([request,answer,change]),'contradictory decision'))
check('explicit-decision-amendment',lambda:equal(history_state([request,answer,{**change,'supersedes':{'event_id':'a'}}])['decisions']['q']['outcome'],'denied'))
task=event('t1','task_update',{'task_id':'task','revision':1,'status':'completed'})
reopen=event('t2','task_update',{'task_id':'task','revision':2,'previous_revision':1,'status':'pending'})
check('unexplained-task-reopen',lambda:rejects(lambda:history_state([task,reopen]),'reopen reason'))
check('explained-task-reopen',lambda:history_state([task,event('t2','task_update',{**reopen['data'],'reopen_reason':'New requirement'})]))
call=event('c','tool_call',{'call_id':'c'});res=event('r','tool_result',{'call_id':'c','result_index':0,'terminal':True,'outcome':'success'})
check('terminal-result-final',lambda:rejects(lambda:history_state([call,res,event('r2','tool_result',{**res['data'],'result_index':1})]),'after terminal'))

def source_mutation(fn,message):
    d=copy.deepcopy(doc);fn(d);rejects(lambda:validate_document(d,folder),message)
check('missing-actor',lambda:source_mutation(lambda d:d['events'][0].update(actor_id='absent'),'missing actor'))
check('provenance-span',lambda:source_mutation(lambda d:d['events'][0]['provenance'].update(sources=[{'resource_id':d['resources'][0]['id'],'locator':{'syntax':'bytes','offset':999999,'length':1}}]),'source span outside'))
check('causal-self-cycle',lambda:source_mutation(lambda d:d['events'][0].update(causes=[{'event_id':d['events'][0]['id']}]),'branch causal order'))

def stream_fixture():
    d=copy.deepcopy(doc);e=next(e for e in d['events'] if e['kind']=='tool_call');content=encode(e['data']['arguments']).decode()
    r={'id':'stream-bytes','media_type':'application/json','purpose':'native','availability':'embedded','text':content,'bytes':len(content.encode()),'sha256':hashlib.sha256(content.encode()).hexdigest()};d['resources'].append(r)
    for c in d['coverage']:
        if c['scope']=='native':c.update(status='complete')
    d['required_features'].append('asif.streams/0.1');d['streams']=[{'id':'stream-1','kind':'tool_arguments','event_id':e['id'],'call_id':e['data']['call_id'],'status':'complete','segments':[{'index':0,'resource_id':r['id'],'offset':0,'length':3,'terminal':False},{'index':1,'resource_id':r['id'],'offset':3,'length':r['bytes']-3,'terminal':True}]}];return d
check('stream-assembled-arguments',lambda:equal(validate_document(stream_fixture(),folder)['streams']['stream-1']['status'],'complete'))
def broken_stream():
    d=stream_fixture();d['streams'][0]['segments'][1]['index']=2;rejects(lambda:validate_document(d,folder),'completeness mismatch')
check('stream-missing-fragment',broken_stream)

def external():
    d=copy.deepcopy(doc);e=next(e for e in d['events'] if e['kind']=='tool_call');d['events'].remove(e)
    for b in d['branches']:b['event_ids'].remove(e['id'])
    for ev in d['events']:ev['causes']=[x for x in ev['causes'] if x['event_id']!=e['id']]
    for c in d['contexts']:
        for i in c['inputs']:i['source_events']=[x for x in i['source_events'] if x['event_id']!=e['id']]
    d['required_features'].append('asif.external-bindings/0.1');d['external_bindings']=[{'kind':'call','id':e['data']['call_id'],'source':{'session_id':'earlier','capture_id':'earlier-capture','event_id':e['id']},'descriptor':{k:e['data'][k] for k in ['tool_id','arguments','arguments_status']}}]
    return validate_document(d,folder)
check('external-call-binding',external)

with tempfile.TemporaryDirectory() as temp:
    temp=Path(temp);w=doc['continuation']['workspaces'][0]
    check('restore-selected-tree',lambda:restore(doc,validated,w['id'],temp/'restored'))
    for entry in w['entries']:
        if entry['kind']=='file':check('restored-bytes-'+entry['path'],lambda e=entry:equal((temp/'restored'/e['path']).read_bytes(),validated['resources'].bytes(e['resource_id'])))
    check('restore-no-overwrite',lambda:rejects(lambda:restore(doc,validated,w['id'],temp/'restored'),'already exists'))
    check('restore-rollback',lambda:rejects(lambda:restore(doc,validated,w['id'],temp/'failed',fail_after=1),'injected staging'))
    check('rollback-cleaned',lambda:equal([x.name for x in temp.iterdir()],['restored']))
    delta=copy.deepcopy(w);delta.update(id='delta',mode='delta',base_snapshot_id=w['id'],entries=[],deletions=[w['entries'][0]['path']])
    check('delta-deletion',lambda:equal(w['entries'][0]['path'] in workspace_states({'workspaces':[w,delta]})['delta'],False))
    bad=copy.deepcopy(delta);bad['deletions']=['missing'];check('delta-absent-deletion',lambda:rejects(lambda:workspace_states({'workspaces':[w,bad]}),'absent from base'))
    collision=copy.deepcopy(doc);extra=copy.deepcopy(w['entries'][0]);extra['path']=extra['path'].upper();collision['continuation']['workspaces'][0]['entries'].append(extra)
    check('restore-case-collision',lambda:rejects(lambda:restore(collision,validated,w['id'],temp/'collision',case_sensitive=False),'path collision'))
    source=ROOT/'examples/image-and-document.session.json';packed=package_bytes(source)
    check('deterministic-package',lambda:equal(packed,package_bytes(source)))
    check('package-raw-document',lambda:equal(inspect_package(packed)['session.json'],source.read_bytes()))
    key=Ed25519PrivateKey.generate();sig=signature(packed,key.private_bytes_raw());public=key.public_key().public_bytes_raw()
    check('signature-verification',lambda:equal(verify_signature(packed,sig,public)['status'],'verified'))
    check('signature-wrong-key',lambda:rejects(lambda:verify_signature(packed,sig,Ed25519PrivateKey.generate().public_key().public_bytes_raw()),'untrusted signing key'))
    def changed_zip(name,content,compression=zipfile.ZIP_STORED):
        files=inspect_package(packed);files[name]=content;out=io.BytesIO()
        with zipfile.ZipFile(out,'w',compression=compression) as z:
            for n,v in files.items():z.writestr(n,v)
        return out.getvalue()
    check('package-content-tamper',lambda:rejects(lambda:inspect_package(changed_zip('session.json',b'{}')),'inventory length mismatch'))
    check('package-traversal',lambda:rejects(lambda:inspect_package(changed_zip('../outside',b'')),'unsafe path'))
    check('package-unlisted-member',lambda:rejects(lambda:inspect_package(changed_zip('unlisted',b'')),'unlisted package member'))
    check('package-compression-refused',lambda:rejects(lambda:inspect_package(changed_zip('session.json',source.read_bytes(),zipfile.ZIP_DEFLATED)),'unsupported package encoding'))
    def redaction():
        d=copy.deepcopy(doc);d['secret-demo']='needle';d['encoded-demo']=base64.b64encode(b'needle').decode();d['needle']={'needle':'needle'}
        result=audit(encode(d),validated,['needle']);equal(result['status'],'matches_found');assert 'needle' not in json.dumps(result);assert any(x['location'].endswith('/base64') for x in result['findings'])
    check('redaction-duplicates-base64-no-value-leak',redaction)
summary={'asif_version':'0.3','scope':'Local vendor-neutral reference implementation checks','checks':len(results),'passed':len(results),'independent_implementations':0,'real_runtime_tests':0,'results':results}
(ROOT/'tests/reference-results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
