"""One synthetic capture, five next actions, and independently bound reports."""
import copy, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from reference.continuation import inspect_session
OUT=ROOT/'examples/continuation'
d=json.loads((OUT/'another-computer.session.json').read_text())
d['session'].update(id='session-action-specific',title='One capture assessed for five different next actions')
d['capture'].update(id='capture-action-specific',boundary='Synthetic capture through e5; no runtime executed. Missing media, optional assets, a pending decision and a remote job have different relevance to each next action.')
d['resources'] += [
 {'id':'missing-media','media_type':'image/png','purpose':'input','availability':'unavailable','explanation':'Referenced image was not captured.'},
 {'id':'optional-asset','media_type':'text/plain','purpose':'capability','availability':'unavailable','explanation':'Optional formatting template not supplied.'}]
text='Choose whether to continue the workshop summary.\n';raw=text.encode()
d['resources'].append({'id':'decision-guide','media_type':'text/plain','purpose':'input','availability':'embedded','text':text,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
part={'kind':'resource','resource_id':'missing-media'}
d['events'][0]['data']['parts'].append(copy.deepcopy(part))
d['contexts'][0]['inputs'][1]['parts'].append(copy.deepcopy(part))
event={'id':'e5','sequence':4,'actor_id':d['events'][-1]['actor_id'],'kind':'decision_request','causes':[{'event_id':'e4'}],'provenance':{'mode':'synthetic','producer':'asif-examples','method':'authored pending decision','inputs':[]},'data':{'request_id':'choose-next','decision_kind':'question','prompt':[{'kind':'resource','resource_id':'decision-guide'}],'options':[]}}
d['events'].append(event);d['branches'][0]['event_ids'].append('e5');d['branches'][0]['head_event_id']='e5'
cp=d['checkpoints'][0];cp.update(at_event_id='e5',open_decisions=[{'request_id':'choose-next','state':'pending'}])
cp['requirements']=[{'id':'viewer','kind':'example.viewer','description':'Resolve destination inspection capability.','required_for':['read'],'status':'available'}, {'id':'media-input','kind':'example.input','description':'Supply the image before model use.','required_for':['context'],'status':'unavailable','resource_id':'missing-media'}]
d['contexts'][0]['at_event_id']='e5'
config=d['configurations'][0]
config['capabilities'].append({'id':'optional-formatting','type':'example.template','definition':{},'resource_ids':['optional-asset'],'required':False})
p=d['continuation'];p['workspaces'][0]['at_event_id']='e5'
p['dependencies'][1]['required_for']=[]
model_dep=copy.deepcopy(p['dependencies'][0]);model_dep.update(id='media-decoder',kind='model',identity='example.media-decoder',required_for=['context'],resource_ids=['missing-media'])
p['dependencies'].append(model_dep)
p['service_bindings']=[{'id':'job-service','service':'example.jobs','endpoint':{'kind':'https','locator':'https://jobs.example.invalid'},'account':{'provider':'example','subject':'account-A'},'auth_method':'none','audience':'example.jobs','scopes':[],'secret_handles':[],'dependency_ids':['summary-tool']}]
p['operations']=[{'id':'remote-job','kind':'service_job','external_identity':{'namespace':'example.jobs/account-A','value':'job-42'},'state':'outcome_unknown','effects':'remote','replay':'reconcile','evidence_resource_ids':[],'recovery':{'strategy':'reconcile','handler_dependency_id':'summary-tool','idempotency_ref':None,'evidence_resource_ids':[]}}]
plan=p['plans'][0];plan['dependency_ids'].append('media-decoder');plan['service_binding_ids']=['job-service'];plan['operation_ids']=['remote-job']
plan['context_accounting'].append({'event_id':'e5','disposition':'not_input','input_ids':[],'explanation':'Pending decision is displayed by the destination, not appended to model input.'})
p['plans']=[]
for action in ['await_user','await_decision','reconcile_operation','model_request','resume_native']:
    item=copy.deepcopy(plan);item['id']=action;item['next_action']={'kind':action}
    if action=='await_decision':item['next_action']['request_id']='choose-next'
    if action=='reconcile_operation':item['next_action']['operation_id']='remote-job'
    if action=='resume_native':item['next_action']['native_import_id']='native'
    p['plans'].append(item)
for coverage in d['coverage']:
    if coverage['scope']=='decisions':coverage.update(status='complete',detail='One pending synthetic decision through e5.')
raw=(json.dumps(d,indent=2)+'\n').encode();(OUT/'action-specific.session.json').write_bytes(raw)
expected=inspect_session(d,OUT)
base=json.loads((OUT/'another-computer.report.json').read_text())
for plan in p['plans']:
    action=plan['id'];r=copy.deepcopy(base)
    r['id']='assessment-'+action;r['source']={'session_id':d['session']['id'],'capture_id':d['capture']['id'],'plan_id':action,'document_sha256':hashlib.sha256(raw).hexdigest()}
    r['assessments']=[];r['blocking_reasons']=[]
    r['path_bindings']=base['path_bindings'] if action in ('model_request','resume_native','reconcile_operation') else []
    r['identity_mappings']=[]
    r['model_assessment'].update(tokenizer=None,input_tokens=None,input_limit=None,fit='unknown')
    for item in expected[action]:
        s=item['subject'];kind=s['kind'];id=s['id'];required=item['required']
        a={'subject':s,'required':required,'status':'supported' if required else 'omitted','detail':'Synthetic supported prerequisite.' if required else 'Deferred for this action; original source remains preserved.','evidence_ids':['scenario'] if required else []}
        if required:
            if kind=='resource' and id in ('missing-media','optional-asset') or kind=='model' or kind=='plan' and action in ('model_request','resume_native') or kind=='checkpoint_requirement' and id=='media-input' or kind=='operation' and action!='reconcile_operation':
                a.update(status='unresolved',detail='Required input, model fit, decision or prior operation outcome is unresolved for this action.')
            elif kind=='dependency':
                dep=next(x for x in p['dependencies'] if x['id']==id);a['resolved']={'identity':dep['identity'],'version':'1'}
            elif kind=='service':a['resolved']={'account':p['service_bindings'][0]['account'],'audience':'example.jobs','scopes':[],'secret_handles':[],'endpoint':'https://jobs.example.invalid'}
            elif kind=='operation':a['resolved']={'recovery_strategy':'reconcile','external_identity':p['operations'][0]['external_identity']}
            elif kind in ('checkpoint_requirement','environment_requirement'):a['resolved']={'status':'available'}
        r['assessments'].append(a)
        if required and a['status']=='unresolved':r['blocking_reasons'].append({'subject':s,'reason':a['detail']})
    r['outcome']='blocked' if r['blocking_reasons'] else 'ready'
    filename='action-specific.report.json' if action=='await_user' else 'action-specific-'+action+'.report.json'
    (OUT/filename).write_text(json.dumps(r,indent=2)+'\n')
print('Built one capture with five action-specific reports (synthetic only).')
