"""Build invented continuation scenarios and explicitly synthetic assessments."""
import copy
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from continuation_checks import inspect_session, subject, key
OUT=ROOT/'examples/continuation';OUT.mkdir(exist_ok=True)
BASE=json.loads((ROOT/'examples/tool-generated-files.session.json').read_text())
FEATURE='asif.portable-continuation/0.2'

def resource(id,text,purpose):
 raw=text.encode();return {'id':id,'media_type':'application/json' if purpose=='native' else 'text/plain','availability':'embedded','purpose':purpose,'text':text,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def dependency(id,kind,identity,resource_ids=()):
 return {'id':id,'kind':kind,'identity':identity,'accepted_versions':['1'],'platform':{'os':['macos','linux'],'architectures':['arm64','x86_64']},'required_for':['continue'],'depends_on':[],'resource_ids':list(resource_ids),'binding':{'kind':'builtin','reference':identity}}
def doc_for(slug):
 d=copy.deepcopy(BASE);d['session']['id']='session-'+slug;d['session']['title']=slug.replace('-',' ');d['capture']['id']='capture-'+slug
 d['session']['native_ids']=[{'provider':'example-agent-a','namespace':'source-runtime','value':'source-native'}]
 d['capture']['boundary']='Synthetic complete checkpoint through e4. No real runtime executed.'
 for r in d['resources']:
  if 'path' in r:
   r['text']=(ROOT/'examples'/r.pop('path')).read_text()
 d['resources'] += [resource('skill-template','Total the rows; retain source CSV and output files.\n','capability'),resource('native-state','{"session":"source-native","ordinals":[1,2,3,4]}\n','native')]
 d['configurations']=[{'id':'effective','knowledge':'effective','instructions':[{'id':'workspace-rule','parts':[{'kind':'text','text':'Use the declared workspace for file operations.'}],'scope':{'dialect':'example.scope/1','value':'workspace'},'activation':{'dialect':'example.activation/1','value':'always'},'provenance':{'mode':'synthetic','producer':'asif-examples','method':'Authored configuration fixture.','inputs':[]}}],'capabilities':[{'id':'summary-skill','type':'example.skill','definition':{'id':'inventory-summary','version':'1'},'resource_ids':['skill-template'],'required':True}],'policies':[{'id':'workspace-only','type':'example.policy/1','definition':{'file_access':'declared-workspace'},'enforcing':True}],'secret_requirements':[]}]
 inputs=[]
 for ev in d['events']:
  data=copy.deepcopy(ev['data']);kind=ev['kind']
  role=data.pop('role', 'tool' if kind=='tool_result' else 'assistant')
  parts=data.pop('parts',[])
  inputs.append({'id':'input-'+ev['id'],'kind':kind,'role':role,'parts':parts,'source_events':[{'event_id':ev['id']}],**data})
 inputs.insert(0,{'id':'input-instruction','kind':'message','role':'system','parts':copy.deepcopy(d['configurations'][0]['instructions'][0]['parts']),'source_events':[]})
 d['contexts']=[{'id':'continue-context','branch_id':'main','at_event_id':'e4','purpose':'continuation','fidelity':'reconstructed','inputs':inputs,'tool_ids':['summarize'],'configuration_id':'effective','request_parameters':{}}]
 cp=d['checkpoints'][0];cp.update(context_id='continue-context',configuration_id='effective',knowledge='observed',status='idle',requirements=[])
 d['environments']=[{'id':'project-env','kind':'workspace','description':'Synthetic project directory at the captured boundary.','resource_ids':['source-csv','output-csv','report'],'requirements':[],'definition':{'dialect':'example.workspace/1','value':{'cwd':'/Users/example/project'}}}]
 deps=[dependency('agent-runtime','agent_runtime','example-agent-a'),dependency('summary-tool','tool','example.inventory.summarize'),dependency('summary-skill','skill','example.inventory-summary',['skill-template'])]
 deps[1].update(tool_id='summarize',behavior={'id':'example.inventory.summarize','revision':'1','effects':'local','replay':'never'})
 deps[2]['depends_on']=['summary-tool']
 w={'id':'workspace-head','environment_id':'project-env','root_id':'project','at_event_id':'e4','source_root':'/Users/example/project','mode':'snapshot','selection':{'include':['inventory.csv','totals.csv','summary.md'],'exclude':['.cache/'],'complete_for_selection':True},'entries':[{'path':name,'kind':'file','mode':420,'resource_id':rid} for name,rid in [('inventory.csv','source-csv'),('totals.csv','output-csv'),('summary.md','report')]],'deletions':[],'base_snapshot_id':None}
 plan={'id':'continue-main','checkpoint_id':cp['id'],'context_id':'continue-context','configuration_id':'effective','workspace_ids':['workspace-head'],'dependency_ids':[x['id'] for x in deps],'service_binding_ids':[],'operation_ids':[],'native_import_id':'native','boundary':{'method':'quiesced','consistency':'consistent','evidence_resource_ids':[],'explanation':'Invented quiescent source checkpoint; illustrative evidence only.'},'context_accounting':[{'event_id':ev['id'],'disposition':'included','input_ids':['input-'+ev['id']],'explanation':'Retained as a typed input in the reconstructed continuation context.'} for ev in d['events']],'cwd':{'root_id':'project','relative_path':''},'path_references':[{'entity_type':'environment','entity_id':'project-env','json_pointer':'/definition/value/cwd','root_id':'project','relative_path':''}],'model_requirements':{'source_model':{'provider':'example','id':'model-a','revision':'1'},'capabilities':['text','tool_calls'],'media_types':['text/csv','text/markdown'],'overflow_policy':'block'},'next_action':{'kind':'resume_native','native_import_id':'native'}}
 d['continuation']={'profile_version':'0.2','source_runtime':{'agent':{'id':'example-agent-a','version':'1','state_format':'example-native/1'},'adapter':{'id':'example-adapter','version':'1'},'os':'macos','architecture':'arm64'},'workspaces':[w],'dependencies':deps,'configuration_bindings':[{'configuration_id':'effective','effective_order':['workspace-rule'],'instruction_rules':[{'instruction_id':'workspace-rule','authority':'system','merge_behavior':'append','group_id':'workspace-rules','priority':0,'scope':{'kind':'root','root_id':'project'},'activation':{'kind':'always'}}],'policy_ids':['workspace-only']}],'service_bindings':[],'operations':[],'native_imports':[{'id':'native','adapter':{'id':'example-adapter','version':'1'},'source_state_format':'example-native/1','accepted_target_agent_versions':['1'],'resource_ids':['native-state'],'mode':'continue','identity_policy':'preserve_if_safe','ordering_contract':'example.ordinal-order/1','index_contract':'example.native-index/1','conflict_policy':'reject'}],'plans':[plan]}
 d['required_features']=[FEATURE]
 for c in d['coverage']:
  if c['scope'] in ('configuration','environment','native'):c.update(status='complete',detail='All modeled data is included in this authored synthetic scenario.')
 return d

def report_for(d,raw,slug):
 expected=inspect_session(d,OUT)['continue-main']
 model=copy.deepcopy(d['continuation']['plans'][0]['model_requirements']['source_model'])
 return {'report_version':'0.2','evaluation_mode':'synthetic','id':'assessment-'+slug,'source':{'session_id':d['session']['id'],'capture_id':d['capture']['id'],'plan_id':'continue-main','document_sha256':hashlib.sha256(raw).hexdigest()},'destination':{'id':'example-cloud-runtime','runtime':{'agent':{'id':'example-agent-a','version':'1','state_format':'example-native/1'},'adapter':{'id':'example-adapter','version':'1'},'os':'linux','architecture':'x86_64'},'capabilities_sha256':hashlib.sha256(b'invented destination capability snapshot').hexdigest()},'assessed_at':'2026-09-26T12:00:00Z','expires_at':'2026-09-26T13:00:00Z','outcome':'ready','assessments':[{'subject':item['subject'],'status':'supported','required':item['required'],'detail':'Assumed supported in this synthetic example; no actual destination check occurred.','evidence_ids':['scenario'],**({'resolved':{'identity':next(x['identity'] for x in d['continuation']['dependencies'] if x['id']==item['subject']['id']),'version':'1'}} if item['subject']['kind']=='dependency' else {})} for item in expected],'path_bindings':[{'root_id':'project','destination_path':'/work/project','case_sensitive':True,'unicode_normalization':'none'}] if d['continuation']['workspaces'] else [],'identity_mappings':[{'entity_type':'native_session','source_id':'source-native','target_id':'source-native','target_namespace':'example-cloud-runtime'}] if d['continuation']['native_imports'] else [],'transformations':[],'model_assessment':{'source':model,'target':model,'tokenizer':'example-tokenizer/1','input_tokens':700,'input_limit':8000,'output_reserve':1000,'fit':'fits'},'blocking_reasons':[],'evidence':[{'id':'scenario','producer':'asif-examples','time':'2026-09-26T12:00:00Z','kind':'synthetic','detail':'Authored assumptions only. This receipt cannot authorize import or continuation.'}],'import_result':{'status':'not_attempted','evidence_ids':[],'detail':'No import was executed.'},'continuation_result':{'status':'not_tested','evidence_ids':[],'detail':'No agent was started.'}}

def write(slug,d,change_report=lambda r:None):
 raw=(json.dumps(d,indent=2)+'\n').encode();(OUT/(slug+'.session.json')).write_bytes(raw)
 report=report_for(d,raw,slug);change_report(report)
 (OUT/(slug+'.report.json')).write_text(json.dumps(report,indent=2)+'\n')

def adapt(r,kind,id,target,rule,owner=None):
 s=subject(kind,id,owner)
 for a in r['assessments']:
  if key(a['subject'])==key(s):a['status']='adapted';a['detail']=rule
 r['transformations'].append({'id':'adapt-'+kind+'-'+id,'subject':s,'target':target,'rule':rule,'losses':['Behavioral equivalence remains an explicit acceptance decision.'],'accepted':False,'evidence_ids':['scenario']})

def cross_report(r):
 r['destination']['id']='example-agent-b-runtime';r['destination']['runtime']['agent']={'id':'example-agent-b','version':'2','state_format':'example-b/2'}
 r['destination']['runtime']['adapter']={'id':'example-a-to-b','version':'1'}
 r['destination']['capabilities_sha256']=hashlib.sha256(b'invented agent-b capability snapshot').hexdigest()
 r['model_assessment']['target']={'provider':'example','id':'model-b','revision':'2'}
 r['identity_mappings'][0].update(target_id='target-native-b',target_namespace='example-agent-b-runtime')
 adapt(r,'dependency','agent-runtime','example-agent-b/2','Translate runtime requirements to the destination agent with an explicit compatibility mapping.')
 adapt(r,'dependency','summary-tool','example-b.inventory/2','Map CSV resource input and output references while preserving call/result identity and side effects.')
 adapt(r,'model','continue-main','example/model-b/2','Substitute the target model after measuring its input budget; no identical-output guarantee.')
 adapt(r,'native_import','native','example-b/2','Create a target-native representation with mapped identities and target ordering/index rules.')
 r['outcome']='adaptation_required'

write('another-computer',doc_for('another-computer'))
d=doc_for('another-agent');d['continuation']['native_imports'][0].update(mode='translate',identity_policy='map',accepted_target_agent_versions=['2'])
write('another-agent',d,cross_report)

d=doc_for('pending-remote-operation');d['events']=d['events'][:2]
d['events'][0]['data']['parts']=[{'kind':'text','text':'Publish this inventory report once.'},{'kind':'resource','resource_id':'source-csv','description':'Input inventory.'}]
d['events'][1]['data']['arguments']={'resource_id':'source-csv'}
d['tools'][0].update(name='example.inventory.publish',description='Publish an inventory report to a service.')
d['resources']=[r for r in d['resources'] if r['id']=='source-csv'];d['environments']=[]
d['branches'][0].update(event_ids=['e1','e2'],head_event_id='e2')
cp=d['checkpoints'][0];cp.update(at_event_id='e2',status='waiting',open_calls=[{'call_id':'call-1','state':'outcome_unknown'}])
ctx=d['contexts'][0];ctx.update(at_event_id='e2',inputs=ctx['inputs'][1:3]);ctx['inputs'][0]['parts']=copy.deepcopy(d['events'][0]['data']['parts'])
cfg=d['configurations'][0];cfg.update(instructions=[],capabilities=[],policies=[],secret_requirements=[{'handle':'publisher-login','purpose':'Authenticate to the target publishing account.'}])
d['session']['native_ids']=[]
p=d['continuation'];p['workspaces']=[];p['native_imports']=[]
tool=dependency('publisher','tool','example.inventory.publish');tool.update(tool_id='summarize',behavior={'id':'example.inventory.publish','revision':'1','effects':'remote','replay':'reconcile'})
p['dependencies']=[tool];p['configuration_bindings']=[{'configuration_id':'effective','effective_order':[],'instruction_rules':[],'policy_ids':[]}]
p['service_bindings']=[{'id':'publisher-service','service':'example.publisher','endpoint':{'kind':'https','locator':'https://publisher.example.invalid'},'account':{'provider':'example','subject':'account-A'},'auth_method':'oauth','audience':'example.publisher','scopes':['reports:write'],'secret_handles':['publisher-login'],'dependency_ids':['publisher']}]
p['operations']=[{'id':'publish-operation','call_id':'call-1','kind':'tool','external_identity':{'namespace':'example.publisher/account-A','value':'operation-42'},'state':'outcome_unknown','effects':'remote','replay':'reconcile','evidence_resource_ids':[],'recovery':{'strategy':'reconcile','handler_dependency_id':'publisher','idempotency_ref':None,'evidence_resource_ids':[]}}]
plan=p['plans'][0];plan.update(workspace_ids=[],dependency_ids=['publisher'],service_binding_ids=['publisher-service'],operation_ids=['publish-operation'],native_import_id=None,cwd=None,path_references=[],context_accounting=plan['context_accounting'][:2],next_action={'kind':'reconcile_operation','operation_id':'publish-operation'})
d['capture']['boundary']='Invented capture through e2, with no result for the remote publication.'
for c in d['coverage']:
 if c['scope']=='resources':c.update(status='complete',detail='All modeled input resources included.')
 if c['scope'] in ('native','environment'):c.update(status='known_empty',detail='No native artifact or workspace supplied by this invented non-coding scenario.')
def blocked_report(r):
 for a in r['assessments']:
  if a['subject']['kind'] in ('operation','service'):
   a.update(status='unresolved',detail='Remote outcome or destination login must be verified before any continuation.')
   r['blocking_reasons'].append({'subject':a['subject'],'reason':a['detail']})
 r['outcome']='blocked'
write('pending-remote-operation',d,blocked_report)
print('Built three continuation sessions and three explicitly synthetic destination reports.')
