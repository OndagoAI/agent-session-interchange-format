"""Emit the draft portable-continuation schemas; no remote schema fetches."""
import copy
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
S={'type':'string','minLength':1}; T={'type':'string'}; B={'type':'boolean'}
N={'type':'integer','minimum':0,'maximum':9007199254740991}
H={'type':'string','pattern':'^[0-9a-f]{64}(?![\\s\\S])'}
def enum(*values):return {'enum':list(values)}
def arr(item,minimum=0):return {'type':'array','items':item,'minItems':minimum}
def ids():return {**arr(S),'uniqueItems':True}
def obj(props,required=None):return {'type':'object','properties':props,'required':list(props) if required is None else required,'additionalProperties':True}
def ref(name):return {'$ref':'#/$defs/'+name}
def null(item):return {'anyOf':[item,{'type':'null'}]}
def when(field,value,then):return {'if':{'properties':{field:{'const':value}},'required':[field]},'then':then}
D={}
D['agent']=obj({'id':S,'version':null(S),'state_format':null(S)})
D['runtime']=obj({'agent':ref('agent'),'adapter':obj({'id':S,'version':null(S)}),'os':S,'architecture':S})
D['model']=obj({'provider':S,'id':S,'revision':null(S)})
D['entry']=obj({'path':S,'kind':enum('file','directory','symlink'),'mode':{'type':'integer','minimum':0,'maximum':511},'resource_id':S,'target':S},['path','kind'])
D['entry']['allOf']=[when('kind','file',{'required':['mode','resource_id']}),when('kind','directory',{'required':['mode']}),when('kind','symlink',{'required':['target']})]
D['git']=obj({'object_format':S,'head':null(S),'branch':null(S),'bundle_resource_ids':ids(),'prerequisites':arr(obj({'object_id':S,'availability':enum('embedded','external','unavailable','unknown'),'resource_id':S},['object_id','availability'])),'index_entries':arr(obj({'path':S,'stage':{'type':'integer','minimum':0,'maximum':3},'mode':S,'resource_id':null(S),'object_id':null(S)})),'submodules':arr(obj({'path':S,'object_id':S,'dependency_id':S})),'lfs_dependency_ids':ids()})
D['workspace']=obj({'id':S,'environment_id':S,'root_id':S,'at_event_id':null(S),'source_root':S,'mode':enum('snapshot','delta','refs'),'selection':obj({'include':arr(S),'exclude':arr(S),'complete_for_selection':B}),'entries':arr(ref('entry')),'deletions':arr(S),'base_snapshot_id':null(S),'git':ref('git')},['id','environment_id','root_id','at_event_id','source_root','mode','selection','entries','deletions','base_snapshot_id'])
D['workspace']['allOf']=[when('mode','delta',{'properties':{'base_snapshot_id':S}}),when('mode','snapshot',{'properties':{'base_snapshot_id':{'type':'null'},'deletions':{'maxItems':0}}}),when('mode','refs',{'required':['git']})]
D['behavior']=obj({'id':S,'revision':S,'effects':enum('none','local','remote','unknown'),'replay':enum('never','idempotent','reconcile','unknown')})
D['dependency']=obj({'id':S,'kind':enum('agent_runtime','model','executable','package','skill','plugin','hook','tool','policy','service','resource'),'identity':S,'accepted_versions':ids(),'platform':obj({'os':ids(),'architectures':ids()}),'required_for':{**arr(enum('read','context','continue')),'uniqueItems':True},'depends_on':ids(),'resource_ids':ids(),'binding':obj({'kind':enum('builtin','package','command','service','opaque'),'reference':S}),'tool_id':S,'behavior':ref('behavior')},['id','kind','identity','accepted_versions','platform','required_for','depends_on','resource_ids','binding'])
D['dependency']['allOf']=[when('kind','tool',{'required':['tool_id','behavior']})]
D['scope']=obj({'kind':enum('global','root','path_prefix'),'root_id':S,'relative_path':T},['kind'])
D['scope']['allOf']=[when('kind','root',{'required':['root_id']}),when('kind','path_prefix',{'required':['root_id','relative_path']})]
D['activation']=obj({'kind':enum('always','predicate'),'dialect':S,'expression':{}},['kind'])
D['activation']['allOf']=[when('kind','predicate',{'required':['dialect','expression']})]
D['configuration_binding']=obj({'configuration_id':S,'effective_order':ids(),'instruction_rules':arr(obj({'instruction_id':S,'authority':enum('system','developer','user','untrusted','unknown'),'merge_behavior':enum('append','replace_same_scope','reject_conflict','unknown'),'group_id':S,'priority':{'type':'integer'},'scope':ref('scope'),'activation':ref('activation')})),'policy_ids':ids()})
D['service']=obj({'id':S,'service':S,'endpoint':obj({'kind':enum('https','stdio','local_socket','other'),'locator':S}),'account':obj({'provider':S,'subject':S}),'auth_method':enum('none','api_key','oauth','login','other'),'audience':S,'scopes':ids(),'secret_handles':ids(),'dependency_ids':ids()})
D['operation']=obj({'id':S,'call_id':S,'kind':enum('tool','process','service_job','agent'),'external_identity':null(obj({'namespace':S,'value':S})),'state':enum('pending','running','succeeded','failed','cancelled','outcome_unknown'),'effects':enum('none','local','remote','unknown'),'replay':enum('never','idempotent','reconcile','unknown'),'evidence_resource_ids':ids(),'recovery':obj({'strategy':enum('reconcile','reconnect','restart','refuse'),'handler_dependency_id':null(S),'idempotency_ref':null(S),'evidence_resource_ids':ids()})},['id','kind','external_identity','state','effects','replay','evidence_resource_ids','recovery'])
D['operation']['allOf']=[when('kind','tool',{'required':['call_id']})]
D['native']=obj({'id':S,'adapter':obj({'id':S,'version':S}),'source_state_format':S,'accepted_target_agent_versions':ids(),'resource_ids':ids(),'mode':enum('copy','continue','translate'),'identity_policy':enum('new','preserve_if_safe','map'),'ordering_contract':S,'index_contract':S,'conflict_policy':enum('reject','new_identity','replace_if_unchanged'),'baseline_sha256':H},['id','adapter','source_state_format','accepted_target_agent_versions','resource_ids','mode','identity_policy','ordering_contract','index_contract','conflict_policy'])
D['native']['allOf']=[when('conflict_policy','replace_if_unchanged',{'required':['baseline_sha256']}),when('mode','copy',{'properties':{'identity_policy':{'const':'new'}}})]
D['accounting']=obj({'event_id':S,'disposition':enum('included','summarized','not_input','unavailable'),'input_ids':ids(),'explanation':S})
D['accounting']['allOf']=[when('disposition',v,{'properties':{'input_ids':{'minItems':1}}}) for v in ['included','summarized']]
D['next_action']=obj({'kind':enum('model_request','await_user','await_decision','reconcile_operation','resume_native'),'request_id':S,'operation_id':S,'native_import_id':S},['kind'])
D['next_action']['allOf']=[when('kind',kind,{'required':[field]}) for kind,field in [('await_decision','request_id'),('reconcile_operation','operation_id'),('resume_native','native_import_id')]]
D['plan']=obj({'id':S,'checkpoint_id':S,'context_id':S,'configuration_id':S,'workspace_ids':ids(),'dependency_ids':ids(),'service_binding_ids':ids(),'operation_ids':ids(),'native_import_id':null(S),'boundary':obj({'method':enum('quiesced','transactional','bounded_read','best_effort'),'consistency':enum('consistent','partial','unknown'),'evidence_resource_ids':ids(),'explanation':S}),'context_accounting':arr(ref('accounting')),'cwd':null(obj({'root_id':S,'relative_path':T})),'path_references':arr(obj({'entity_type':enum('event','resource','environment','configuration','dependency'),'entity_id':S,'json_pointer':S,'root_id':S,'relative_path':T})),'model_requirements':obj({'source_model':ref('model'),'capabilities':ids(),'media_types':ids(),'overflow_policy':enum('block','propose_compaction')}),'next_action':ref('next_action')})
profile={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:asif:portable-continuation:0.1','title':'ASIF portable continuation 0.1',**obj({'profile_version':{'const':'0.1'},'source_runtime':ref('runtime'),'workspaces':arr(ref('workspace')),'dependencies':arr(ref('dependency')),'configuration_bindings':arr(ref('configuration_binding')),'service_bindings':arr(ref('service')),'operations':arr(ref('operation')),'native_imports':arr(ref('native')),'plans':arr(ref('plan'),1)}),'$defs':D}
(ROOT/'continuation.schema.json').write_text(json.dumps(profile,indent=2)+'\n')
# The embedded schema has its own $id so its local references remain self-contained.
core=json.loads((ROOT/'session.schema.json').read_text())
core['$id']='urn:asif:0.3:session'
core['properties']['asif_version']={'const':'0.3'}
core['properties']['continuation']={'$ref':'#/$defs/continuation'}
core['$defs']['continuation']=profile
inp=core['$defs']['context_input'];props=inp['properties']
props.update({'kind':enum('message','tool_call','tool_result'),'call_id':S,'tool_id':S,'arguments':{},'arguments_status':enum('complete','partial','unknown'),'result_index':N,'terminal':B,'outcome':enum('success','error','cancelled','unknown')})
if 'kind' not in inp['required']:inp['required'].insert(1,'kind')
inp['allOf']=[when('kind','tool_call',{'required':['call_id','tool_id','arguments','arguments_status'],'properties':{'role':{'const':'assistant'}}}),when('kind','tool_result',{'required':['call_id','result_index','terminal','outcome'],'properties':{'role':{'const':'tool'}},'allOf':[when('terminal',False,{'properties':{'outcome':{'const':'unknown'}}})]})]
core['allOf']=[{'if':{'required':['continuation']},'then':{'properties':{'required_features':{'contains':{'const':'asif.portable-continuation/0.1'}}}}},{'if':{'properties':{'required_features':{'contains':{'const':'asif.portable-continuation/0.1'}}},'required':['required_features']},'then':{'required':['continuation']}}]
(ROOT/'session.schema.json').write_text(json.dumps(core,indent=2)+'\n')
# Reports are separate immutable documents bound to exact source bytes.
R={'runtime':D['runtime'],'agent':D['agent'],'model':D['model']}
R['subject']=obj({'kind':enum('plan','context','model','workspace','dependency','service','configuration','instruction','capability','policy','resource','operation','native_import','feature'),'id':S,'owner_id':S},['kind','id'])
R['assessment']=obj({'subject':ref('subject'),'status':enum('supported','adapted','omitted','unresolved','unsupported'),'required':B,'detail':S,'evidence_ids':ids(),'resolved':obj({'identity':S,'version':null(S),'account':obj({'provider':S,'subject':S}),'scopes':ids(),'audience':S,'endpoint':S,'secret_handles':ids()},[])},['subject','status','required','detail','evidence_ids'])
R['evidence']=obj({'id':S,'producer':S,'time':S,'kind':enum('inspection','compatibility_test','authorization','acceptance','import','continuation','synthetic'),'detail':S,'reference':S},['id','producer','time','kind','detail'])
R['transformation']=obj({'id':S,'subject':ref('subject'),'target':S,'rule':S,'losses':arr(S),'accepted':B,'evidence_ids':ids()})
R['transformation']['allOf']=[when('accepted',True,{'properties':{'evidence_ids':{'minItems':1}}})]
R['result']=obj({'status':S,'evidence_ids':ids(),'detail':S})
report={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:asif:continuation-report:0.1','title':'ASIF destination continuation report',**obj({'report_version':{'const':'0.1'},'evaluation_mode':enum('synthetic','observed'),'id':S,'source':obj({'session_id':S,'capture_id':S,'plan_id':S,'document_sha256':H}),'destination':obj({'id':S,'runtime':ref('runtime'),'capabilities_sha256':H}),'assessed_at':S,'expires_at':S,'outcome':enum('ready','blocked','adaptation_required'),'assessments':arr(ref('assessment'),1),'path_bindings':arr(obj({'root_id':S,'destination_path':S,'case_sensitive':B,'unicode_normalization':enum('none','NFC','NFD')})),'identity_mappings':arr(obj({'entity_type':S,'source_id':S,'target_id':S,'target_namespace':S})),'transformations':arr(ref('transformation')),'model_assessment':obj({'source':ref('model'),'target':ref('model'),'tokenizer':null(S),'input_tokens':null(N),'input_limit':null(N),'output_reserve':N,'fit':enum('fits','exceeds','unknown')}),'blocking_reasons':arr(obj({'subject':ref('subject'),'reason':S})),'evidence':arr(ref('evidence')),'import_result':obj({'status':enum('not_attempted','imported','failed','rolled_back'),'evidence_ids':ids(),'detail':S}),'continuation_result':obj({'status':enum('not_tested','continued','blocked','failed'),'evidence_ids':ids(),'detail':S})}),'$defs':R}
(ROOT/'continuation-report.schema.json').write_text(json.dumps(report,indent=2)+'\n')
print('Emitted ASIF 0.3 session schema, continuation profile and destination report schema.')
