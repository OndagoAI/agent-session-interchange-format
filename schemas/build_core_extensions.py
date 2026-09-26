"""Add neutral streaming and partial-capture bindings to the core schema."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'session.schema.json';s=json.loads(p.read_text())
S={'type':'string','minLength':1};N={'type':'integer','minimum':0,'maximum':9007199254740991}
def obj(props,required=None):return {'type':'object','properties':props,'required':list(props) if required is None else required,'additionalProperties':True}
def arr(x):return {'type':'array','items':x}
def ref(name):return {'$ref':'#/$defs/'+name}
def when(field,value,then):return {'if':{'properties':{field:{'const':value}},'required':[field]},'then':then}
s['$defs']['event']['allOf'][5]['then']['properties']['data']['properties']['reopen_reason']=S
s['$defs']['stream_segment']=obj({'index':N,'resource_id':S,'offset':N,'length':N,'terminal':{'type':'boolean'}})
s['$defs']['stream']=obj({'id':S,'kind':{'enum':['tool_arguments','tool_result_text']},'event_id':S,'call_id':S,'result_index':N,'status':{'enum':['partial','complete']},'segments':arr(ref('stream_segment'))},['id','kind','event_id','call_id','status','segments'])
s['$defs']['stream']['allOf']=[when('kind','tool_result_text',{'required':['result_index']})]
s['$defs']['external_binding']=obj({'kind':{'enum':['call','request']},'id':S,'source':obj({'session_id':S,'capture_id':S,'event_id':S}),'descriptor':obj({},[])})
s['$defs']['external_binding']['allOf']=[when('kind','call',{'properties':{'descriptor':obj({'tool_id':S,'arguments':{},'arguments_status':{'enum':['complete','partial','unknown']}})}}),when('kind','request',{'properties':{'descriptor':obj({'decision_kind':{'enum':['approval','question','plan_review']},'prompt':arr(ref('part')),'options':arr(obj({'id':S,'label':{'type':'string'}}))})}})]
for field,definition,feature in [('streams','stream','asif.streams/0.1'),('external_bindings','external_binding','asif.external-bindings/0.1')]:
 s['properties'][field]=arr(ref(definition))
 gates=[{'if':{'required':[field]},'then':{'properties':{'required_features':{'contains':{'const':feature}}}}},{'if':{'properties':{'required_features':{'contains':{'const':feature}}}},'then':{'required':[field]}}]
 for gate in gates:
  if gate not in s['allOf']:s['allOf'].append(gate)
p.write_text(json.dumps(s,indent=2)+'\n')
print('Added streaming and external-binding schemas.')
