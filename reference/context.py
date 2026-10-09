"""Vendor-neutral request materialization and declarative configuration evaluation."""
import copy
from .common import need, Unsupported, relative

def matches_scope(scope,environment):
    if scope['kind']=='global':return True
    if scope['root_id']!=environment.get('root_id'):return False
    if scope['kind']=='root':return True
    relative(scope['relative_path'],True);path=environment.get('relative_path','');relative(path,True)
    prefix=scope['relative_path'].rstrip('/')
    return not prefix or path==prefix or path.startswith(prefix+'/')

def predicate(expression,environment,depth=0):
    need(depth<=32 and isinstance(expression,dict) and len(expression)==1,'invalid predicate')
    op,value=next(iter(expression.items()))
    if op in ('all','any'):
        need(isinstance(value,list),'predicate list required');values=[predicate(x,environment,depth+1) for x in value]
        return all(values) if op=='all' else any(values)
    if op=='not':return not predicate(value,environment,depth+1)
    if op=='event_kind_in':
        need(isinstance(value,list) and all(isinstance(x,str) for x in value),'invalid event predicate');return environment.get('event_kind') in value
    if op=='root_is':need(isinstance(value,str),'invalid root predicate');return environment.get('root_id')==value
    if op=='path_prefix':
        need(isinstance(value,str),'invalid path predicate');relative(value,True)
        path=environment.get('relative_path','');relative(path,True)
        return not value or path==value or path.startswith(value.rstrip('/')+'/')
    raise Unsupported('unknown predicate operator')

def active(rule,environment):
    if not matches_scope(rule['scope'],environment):return False
    activation=rule['activation']
    if activation['kind']=='always':return True
    if activation.get('dialect')!='asif.activation/0.1':raise Unsupported('unsupported activation dialect')
    return predicate(activation['expression'],environment)

def resolve_configuration(doc,configuration_id,environment):
    config=next((x for x in doc['configurations'] if x['id']==configuration_id),None);need(config is not None,'unknown configuration')
    need(config['knowledge']=='effective','configuration not effective')
    binding=next((x for x in doc.get('continuation',{}).get('configuration_bindings',[]) if x['configuration_id']==configuration_id),None)
    need(binding is not None,'missing configuration binding')
    instructions={x['id']:x for x in config['instructions']};rules={x['instruction_id']:x for x in binding['instruction_rules']};selected=[]
    for id in binding['effective_order']:
        rule=rules[id]
        if not active(rule,environment):continue
        if rule['authority']=='unknown' or rule['merge_behavior']=='unknown':raise Unsupported('unknown instruction interpretation')
        if rule['authority']=='untrusted':raise Unsupported('untrusted content cannot become an instruction')
        same=[old for old in selected if all(rules[old][key]==rule[key] for key in ['authority','group_id','scope'])]
        if rule['merge_behavior']=='replace_same_scope':selected=[old for old in selected if old not in same]
        elif rule['merge_behavior']=='reject_conflict':
            need(all(instructions[old]['parts']==instructions[id]['parts'] for old in same),'instruction group conflict')
        selected.append(id)
    return {'configuration_id':configuration_id,'instruction_ids':selected,'instructions':[copy.deepcopy(instructions[id]) for id in selected],'scope':'neutral declaration evaluation; no runtime application'}

def evaluate_policy(config,environment):
    effects=[];considered=[]
    for policy in config['policies']:
        if not policy['enforcing']:continue
        if policy['type']!='asif.policy/0.1':
            if policy['enforcing']:raise Unsupported('unsupported enforcing policy')
            continue
        d=policy['definition'];need(d.get('effect') in ('allow','deny','ask'),'invalid policy effect')
        need(isinstance(d.get('tool_ids'),list) and all(isinstance(x,str) for x in d['tool_ids']),'invalid policy tools')
        if '*' not in d['tool_ids'] and environment.get('tool_id') not in d['tool_ids']:continue
        if active({'scope':d['scope'],'activation':d['activation']},environment):effects.append(d['effect']);considered.append(policy['id'])
    decision='deny' if 'deny' in effects else 'ask' if 'ask' in effects or not effects else 'allow'
    return {'decision':decision,'policy_ids':considered,'scope':'declarative policy evaluation; destination authorization still required'}

def reconstruct_request(doc,validated,context_id):
    context=next((x for x in doc['contexts'] if x['id']==context_id),None);need(context is not None,'unknown context')
    if context['fidelity'] in ('partial','unknown'):raise Unsupported('incomplete request context')
    if validated['unsupported_features']:raise Unsupported('required feature unsupported')
    resource_ids=set()
    for item in context['inputs']:
        if item['kind']=='tool_call' and item['arguments_status']!='complete':raise Unsupported('partial tool arguments')
        for part in item['parts']:
            if part['kind'] in ('resource','opaque'):resource_ids.add(part['resource_id'])
            if part['kind'] in ('opaque','structured'):raise Unsupported('opaque/structured content requires a declared request encoder')
    tools=[copy.deepcopy(t) for id in context['tool_ids'] for t in doc['tools'] if t['id']==id]
    for tool in tools:resource_ids.update(tool.get('resource_ids',[]))
    for id in sorted(resource_ids):validated['resources'].bytes(id)
    # The normalized form does not guess a provider's wire encoding or tokenize it.
    return {'request_version':'0.1','source':{'session_id':doc['session']['id'],'capture_id':doc['capture']['id'],'context_id':context_id},'fidelity':context['fidelity'],'inputs':copy.deepcopy(context['inputs']),'tools':tools,'model':copy.deepcopy(context.get('model')),'request_parameters':copy.deepcopy(context.get('request_parameters',{})),'configuration_id':context.get('configuration_id'),'resources':[copy.deepcopy(validated['resources'].records[id]) for id in sorted(resource_ids)],'provider_encoding':'not_selected','token_budget':'unmeasured','losses':[]}
