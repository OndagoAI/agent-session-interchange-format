"""Build linked field tables and schema-checked examples from the ASIF schemas.
Authored examples/descriptions live in object-examples.json and object-descriptions.json.
"""
import copy, json, re, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
FILES={'session':'objects.md','continuation':'continuation-objects.md','continuation-report':'report-objects.md'}
SCHEMAS={name:json.loads((ROOT/'schemas'/f'{name}.schema.json').read_text()) for name in FILES}
EVENTS=SCHEMAS['session']['$defs']['event']['properties']['kind']['enum']
NAMES={'session:':'ASIF Document','session:/properties/session':'Session','session:/properties/session/properties/native_ids/items':'Native Identifier','session:/properties/session/properties/lineage/items':'Lineage','session:/properties/capture/properties/producer':'Producer','session:/$defs/event_ref':'Event Reference','session:/$defs/context_input':'Context Input','session:/$defs/part/oneOf/0':'Text Part','session:/$defs/part/oneOf/1':'Resource Part','session:/$defs/part/oneOf/2':'Structured Part','session:/$defs/part/oneOf/3':'Opaque Part','session:/$defs/provenance/properties/sources/items':'Provenance Source','session:/$defs/provenance/properties/sources/items/properties/locator':'Source Locator','session:/$defs/checkpoint/properties/open_calls/items':'Open Call','session:/$defs/checkpoint/properties/open_decisions/items':'Open Decision','session:/$defs/checkpoint/properties/tasks/items':'Task State','session:/$defs/event/properties/data':'Event Data','session:/$defs/event/properties/extensions':'Extension Map','session:/$defs/external_binding/allOf/0/then/properties/descriptor':'External Call Descriptor','session:/$defs/external_binding/allOf/1/then/properties/descriptor':'External Request Descriptor','continuation:':'Continuation Profile','continuation:/$defs/entry':'Workspace Entry','continuation:/$defs/git':'Git State','continuation:/$defs/behavior':'Tool Behavior','continuation:/$defs/service':'Service Binding','continuation:/$defs/native':'Native Import','continuation:/$defs/accounting':'Context Accounting','continuation:/$defs/plan':'Continuation Plan','continuation-report:':'Destination Report'}
NAMES['session:/$defs/external_binding/allOf/1/then/properties/descriptor/properties/options/items']='External Request Option'
def title(name,path):
 key=name+':'+path
 if key in NAMES:return NAMES[key]+' Object'
 if path.startswith('/$defs/event/allOf/'):
  number=int(path.split('/')[4]);suffix=' Option' if path.endswith('/options/items') else ' Data'
  return EVENTS[number].replace('_',' ').title()+suffix+' Object'
 tokens=[x for x in path.split('/') if x and x not in ('$defs','properties','items','anyOf','oneOf') and not x.isdigit()]
 return ' '.join(tokens).replace('_',' ').title()+' Object'
def anchor(name,path):return re.sub('[^a-z0-9]+','-',title(name,path).lower()).strip('-')
def resolve(schema,path):
 value=schema
 for part in path.lstrip('/').split('/') if path else []:value=value[int(part)] if isinstance(value,list) else value[part.replace('~1','/').replace('~0','~')]
 return value
OBJECTS={}
def collect(name,value,path=''):
 if path=='/$defs/continuation' and name=='session':return
 if isinstance(value,dict):
  if value.get('type')=='object':OBJECTS[(name,path)]=value
  for key,child in value.items():collect(name,child,path+'/'+key)
 elif isinstance(value,list):
  for i,child in enumerate(value):collect(name,child,path+'/'+str(i))
for name,schema in SCHEMAS.items():collect(name,schema)
def validator(name,path):
 return Draft202012Validator({'$ref':SCHEMAS[name]['$id']+'#'+path},registry=__import__('referencing').Registry().with_resource(SCHEMAS[name]['$id'],__import__('referencing').Resource.from_contents(SCHEMAS[name])))
def link(name,path,label=None):
 if name=='session' and path=='/$defs/continuation':name,path='continuation',''
 return '['+(label or title(name,path))+']('+FILES[name]+'#'+anchor(name,path)+')'
def typ(name,node,path):
 if '$ref' in node:
  target=node['$ref'][1:]
  if target=='/$defs/part':return ' / '.join(link(name,target+'/oneOf/'+str(i)) for i in range(4))
  return link(name,target)
 if (name,path) in OBJECTS:return link(name,path)
 if node.get('type')=='array':return 'array of '+typ(name,node['items'],path+'/items')
 if 'const' in node:return '`'+json.dumps(node['const'])+'`'
 if 'enum' in node:return 'enum'
 for key in ('anyOf','oneOf'):
  if key in node:return ' / '.join(typ(name,v,path+'/'+key+'/'+str(i)) for i,v in enumerate(node[key]))
 t=node.get('type','JSON value');return ' / '.join(t) if isinstance(t,list) else t

def constraints(s):
 parts=[]
 if 'enum' in s:parts.append('One of '+', '.join('`'+json.dumps(v)+'`' for v in s['enum'])+'.')
 for k,label in [('minimum','Minimum'),('maximum','Maximum'),('minItems','Minimum items'),('maxItems','Maximum items'),('minLength','Minimum length'),('pattern','Pattern')]:
  if k in s:parts.append(f'{label}: `{s[k]}`.')
 if s.get('uniqueItems'):parts.append('Items MUST be unique.')
 return ' '.join(parts)

def condition_text(s):
 out=[]
 for field,others in s.get('dependentRequired',{}).items():out.append('When `'+field+'` is present, '+', '.join('`'+v+'`' for v in others)+' MUST also be present.')
 for rule in s.get('allOf',[]):
  if 'if' not in rule:continue
  condition=rule['if'];parts=[]
  for k,v in condition.get('properties',{}).items():
   if 'const' in v:parts.append('`'+k+'` is `'+json.dumps(v['const'])+'`')
   elif 'contains' in v:parts.append('`'+k+'` contains `'+str(v['contains'].get('const'))+'`')
  if not parts:parts=['`'+k+'` is present' for k in condition.get('required',[])]
  then=rule['then'];requirements=[]
  if then.get('required'):requirements.append('require '+', '.join('`'+x+'`' for x in then['required']))
  for k,v in then.get('properties',{}).items():
   if 'const' in v:requirements.append('`'+k+'` MUST be `'+json.dumps(v['const'])+'`')
   elif 'contains' in v:requirements.append('`'+k+'` MUST contain `'+str(v['contains'].get('const'))+'`')
   elif v.get('required'):requirements.append('`'+k+'` requires '+', '.join('`'+x+'`' for x in v['required']))
  if then.get('oneOf'):requirements.append('exactly one of '+', '.join('`'+v+'`' for x in then['oneOf'] for v in x.get('required',[])))
  if 'not' in then:
   forbidden=[v for x in then['not'].get('anyOf',[then['not']]) for v in x.get('required',[])]
   if forbidden:requirements.append('omit '+', '.join('`'+v+'`' for v in forbidden))
  if parts and requirements:out.append('When '+ ' and '.join(parts)+', '+'; '.join(requirements)+'.')
 for key,word in [('anyOf','at least one'),('oneOf','exactly one')]:
  if key in s and all('required' in x for x in s[key]):out.append('Supply '+word+' of: '+', '.join(' + '.join('`'+v+'`' for v in x['required']) for x in s[key])+'.')
 return out

def emit(path,text):
 if "--check" in sys.argv:
  if not path.exists() or path.read_text()!=text:raise ValueError("Generated documentation drift: "+str(path))
 else:path.write_text(text)

def build():
 samples=json.loads((HERE/'object-examples.json').read_text());variants=json.loads((HERE/'object-variants.json').read_text());metadata=json.loads((HERE/'object-descriptions.json').read_text());manifest=[]
 for name,file in FILES.items():
  entries=[(path,node) for (group,path),node in OBJECTS.items() if group==name]
  lines=['# '+{'session':'Core object reference','continuation':'Continuation object reference','continuation-report':'Destination report object reference'}[name],'','Version: **0.3**. [Specification](../SPEC.md) · [Core](objects.md) · [Continuation](continuation-objects.md) · [Reports](report-objects.md)','','Every example below is JSON Schema checked. Object fragments use IDs resolved by an enclosing session or report; they are not standalone session documents. Full scenarios are in [examples](../examples/README.md). Required means unconditionally required; conditional rules follow each table. Normative [session semantics](../SEMANTICS.md) and [continuation rules](../CONTINUATION.md) also apply.','','## Contents','']
  lines += ['- '+link(name,path) for path,node in entries]
  for path,node in entries:
   key=name+':'+path;sample=samples[key];validator(name,path).validate(sample)
   meta=metadata.get(key,{});desc=meta.get('description',metadata['purposes'].get(title(name,path).removesuffix(' Object'),''))
   if not desc:raise ValueError('Missing object purpose: '+key+' '+title(name,path))
   semantic=meta.get('rules', 'See [session semantics](../SEMANTICS.md).' if name=='session' else 'See [portable-continuation rules](../CONTINUATION.md).')
   lines += ['', '<a id="'+anchor(name,path)+'"></a>','', '## '+title(name,path),'',desc,'','### Fixed fields','']
   props=node.get('properties',{});required=node.get('required',[])
   if props:
    lines+=['| Field | Type | Required | Description |','| --- | --- | --- | --- |']
    for field,shape in props.items():
     description=meta.get('fields',{}).get(field,metadata['fields'].get(field,''))
     if not description:raise ValueError('Missing field description: '+key+'/'+field)
     detail=(description+' '+constraints(shape)).strip().replace('|','\\|').replace('\n',' ')
     lines.append('| <a id="'+anchor(name,path)+'-'+field+'"></a>`'+field+'` | '+typ(name,shape,path+'/properties/'+field)+' | '+('Yes' if field in required else 'No')+' | '+detail+' |')
   else:lines+=['No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.']
   lines+=['','### Rules','',semantic]
   rules=condition_text(node)
   if rules:lines+=['']+['- '+rule for rule in rules]
   lines+=['','Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.','','### Example','','```json',json.dumps(sample,indent=2,ensure_ascii=False),'```']
   for variant in variants.get(key,[]):
    validator(name,path).validate(variant['value'])
    lines+=['','### '+variant['title'],'',variant['description'],'','```json',json.dumps(variant['value'],indent=2,ensure_ascii=False),'```']
   manifest.append({'schema':name+'.schema.json','pointer':path,'example_key':key,'page':file,'anchor':anchor(name,path)})
  emit(HERE/file,'\n'.join(lines)+'\n')
 emit(HERE/'object-index.json',json.dumps(manifest,indent=2)+'\n')
 print(f'Built {len(manifest)} object definitions with validated examples.')
if __name__=='__main__':build()
