"""Core references, provenance, graph and selected-history semantics."""
import json
from pathlib import Path
from decimal import Decimal
from jsonschema import Draft202012Validator, validators
from .common import Invalid, Unsupported, need, unique, acyclic, Resources, pointer, decode
ROOT=Path(__file__).resolve().parents[1]
TYPES=Draft202012Validator.TYPE_CHECKER.redefine('integer',lambda checker,value:not isinstance(value,bool) and (isinstance(value,int) or isinstance(value,(float,Decimal)) and value==int(value)))
Validator=validators.extend(Draft202012Validator,type_checker=TYPES)
SCHEMA=Validator(json.loads((ROOT/'schemas/session.schema.json').read_text()))
SUPPORTED={'asif.portable-continuation/0.1','asif.streams/0.1','asif.external-bindings/0.1'}


def effective(events):
    superseded={e['supersedes']['event_id'] for e in events if 'supersedes' in e and 'capture_id' not in e['supersedes']}
    return [e for e in events if e['id'] not in superseded]


def history_state(events,external_calls=None,external_requests=None):
    calls=dict(external_calls or {});requests=dict(external_requests or {});closed={};decisions={};tasks={};indices={};executions={}
    call_events={};selected={e['id'] for e in effective(events)}
    for event in events:
        # Fold call amendments in place: removing the original could orphan a
        # result or decision recorded before the amendment was captured.
        if event['kind']!='tool_call' and event['id'] not in selected:continue
        data=event['data'];kind=event['kind']
        if kind=='tool_call':
            id=data['call_id']
            if id in calls:
                prior=event.get('supersedes',{})
                need(id in call_events and 'capture_id' not in prior and prior.get('event_id')==call_events[id],'conflicting selected call versions')
            calls[id]=data;call_events[id]=event['id']
        elif kind=='tool_result':
            id=data['call_id'];need(id in calls,'orphan tool result');need(id not in closed,'tool result after terminal')
            need(data['result_index']>indices.get(id,-1),'tool result index order');indices[id]=data['result_index']
            if data['terminal']:closed[id]=data['outcome']
        elif kind=='decision_request':
            id=data['request_id'];need(id not in requests,'duplicate decision request');requests[id]=data
            if 'call_id' in data:need(data['call_id'] in calls,'decision call missing')
            if 'task_id' in data:need(data['task_id'] in tasks and tasks[data['task_id']]['revision']==data['task_revision'],'decision task revision mismatch')
        elif kind=='decision_resolution':
            id=data['request_id'];need(id in requests,'orphan decision resolution');need(id not in decisions,'contradictory decision resolutions')
            if 'selected_option_id' in data:need(data['selected_option_id'] in {x['id'] for x in requests[id]['options']},'unknown decision option')
            decisions[id]=data
        elif kind=='task_update':
            id=data['task_id'];prior=tasks.get(id)
            if prior:
                need(data.get('previous_revision')==prior['revision'] and data['revision']>prior['revision'],'task revision transition')
                if prior['status'] in ('completed','failed','cancelled') and data['status'] in ('pending','in_progress'):
                    need(bool(data.get('reopen_reason')),'task reopen reason missing')
            else:need('previous_revision' not in data,'task predecessor not in selected history')
            tasks[id]=data
        elif kind=='execution_transition':
            id=data['execution_id'];old=executions.get(id)
            need(old not in ('completed','failed','cancelled','interrupted'),'terminal execution reopened')
            executions[id]=data['status']
    return {'calls':calls,'closed_calls':closed,'requests':requests,'decisions':decisions,'tasks':tasks,'executions':executions}


def validate_document(doc,folder):
    SCHEMA.validate(doc)
    collections={name:unique(doc[name]) for name in ['participants','events','branches','executions','contexts','configurations','tools','resources','environments','checkpoints','losses']}
    resources=Resources(doc,folder);events=collections['events'];participants=collections['participants']
    acyclic({id:[p['parent_participant_id']] if 'parent_participant_id' in p else [] for id,p in participants.items()},'participant')
    sequences=[e['sequence'] for e in events.values()];need(len(sequences)==len(set(sequences)),'duplicate event sequence')
    need(sequences==sorted(sequences),'events not serialized in sequence order')
    for branch in collections['branches'].values():
        need(set(branch['event_ids'])<=events.keys(),'missing branch event')
        need(branch['head_event_id']==(branch['event_ids'][-1] if branch['event_ids'] else None),'wrong branch head')
        positions={id:i for i,id in enumerate(branch['event_ids'])}
        for id in branch['event_ids']:
            for cause in events[id]['causes']:
                if 'capture_id' not in cause and cause['event_id'] in positions:
                    need(positions[cause['event_id']]<positions[id],'branch causal order')
    def event_ref(value):
        if 'capture_id' not in value:need(value['event_id'] in events,'missing local event reference')
    def parts(values):
        for part in values:
            if part['kind'] in ('resource','opaque'):resources.ref(part['resource_id'])
    def provenance(value):
        for item in value.get('inputs',[]):event_ref(item)
        for source in value.get('sources',[]):
            resources.ref(source['resource_id']);loc=source.get('locator')
            if loc is None:continue
            if loc['syntax']=='bytes':
                need(isinstance(loc.get('offset'),int) and not isinstance(loc['offset'],bool) and loc['offset']>=0,'invalid source offset')
                need(isinstance(loc.get('length'),int) and not isinstance(loc['length'],bool) and loc['length']>=0,'invalid source length')
                r=resources.records[source['resource_id']]
                need('bytes' in r and loc['offset']+loc['length']<=r['bytes'],'source span outside resource')
            elif loc['syntax']=='json_pointer':
                need(isinstance(loc.get('value'),str),'invalid structured source locator')
                if source['resource_id'] in resources.cache:pointer(decode(resources.bytes(source['resource_id'])),loc['value'])
    calls={};requests={};task_revisions=set();causes={};supersessions={}
    external_calls={};external_requests={}
    for binding in doc.get('external_bindings',[]):
        target=external_calls if binding['kind']=='call' else external_requests
        need(binding['id'] not in target,'duplicate external binding');target[binding['id']]=binding['descriptor']
    for id,e in events.items():
        need(e['actor_id'] in participants,'missing actor')
        if 'execution_id' in e:need(e['execution_id'] in collections['executions'],'missing execution')
        provenance(e['provenance']);causes[id]=[];supersessions[id]=[]
        for cause in e['causes']:
            event_ref(cause)
            if 'capture_id' not in cause:
                need(events[cause['event_id']]['sequence']<e['sequence'],'noncausal event order');causes[id].append(cause['event_id'])
        need(len(causes[id])==len(set(causes[id])),'duplicate cause')
        if 'supersedes' in e:
            event_ref(e['supersedes'])
            if 'capture_id' not in e['supersedes']:
                prior=events[e['supersedes']['event_id']]
                need(prior['sequence']<e['sequence'] and prior['kind']==e['kind'],'invalid supersession')
                if e['kind']=='decision_resolution':need(prior['data']['request_id']==e['data']['request_id'],'decision correction changed request')
                supersessions[id].append(prior['id'])
        d=e['data'];kind=e['kind']
        for name in ('parts','prompt','answer'):
            if name in d:parts(d[name])
        if kind=='tool_call':
            need(d['call_id'] not in external_calls,'duplicate call identity')
            if 'supersedes' in e:
                need('capture_id' not in e['supersedes'],'call amendment requires local predecessor')
                prior=events[e['supersedes']['event_id']];previous=prior['data']
                need(d['call_id']==previous['call_id'] and d['tool_id']==previous['tool_id'],'call amendment changed invocation')
                need(d.get('retry_of')==previous.get('retry_of'),'call amendment changed retry relationship')
                need(e['actor_id']==prior['actor_id'] and e.get('execution_id')==prior.get('execution_id'),'call amendment changed actor or execution')
                need(previous['arguments_status']!='complete','completed call cannot be amended')
                need(previous['arguments_status']!='partial' or d['arguments_status']!='unknown','call argument knowledge regressed')
            else:need(d['call_id'] not in calls,'duplicate call identity')
            need(d.get('retry_of')!=d['call_id'],'retry must use new call identity')
            need(d['tool_id'] in collections['tools'],'missing tool definition');calls[d['call_id']]=d
        elif kind=='decision_request':
            need(d['request_id'] not in requests and d['request_id'] not in external_requests,'duplicate decision request')
            unique(d['options']);requests[d['request_id']]=d
        elif kind=='task_update':
            key=(d['task_id'],d['revision']);need(key not in task_revisions,'duplicate task revision');task_revisions.add(key)
        elif kind in ('context_checkpoint','configuration_change','execution_transition','resource_change'):
            field,collection={'context_checkpoint':('context_id','contexts'),'configuration_change':('configuration_id','configurations'),'execution_transition':('execution_id','executions'),'resource_change':('resource_id','resources')}[kind]
            need(d[field] in collections[collection],'missing '+field)
            for field in ('replaced_context_id','previous_resource_id'):
                if field in d:need(d[field] in collections['contexts' if field=='replaced_context_id' else 'resources'],'missing predecessor')
        elif kind=='extension' and d['interpretation_required']:need(d['type'] in doc['required_features'],'ungated required extension')
    acyclic(causes,'causal');acyclic(supersessions,'supersession')
    for e in events.values():
        d=e['data']
        if e['kind']=='tool_result':need(d['call_id'] in calls or d['call_id'] in external_calls,'orphan tool result')
        if e['kind']=='decision_resolution':need(d['request_id'] in requests or d['request_id'] in external_requests,'orphan decision resolution')
    for binding in doc.get('external_bindings',[]):
        if binding['kind']=='call':need(binding['descriptor']['tool_id'] in collections['tools'],'missing external tool')
        else:parts(binding['descriptor']['prompt']);unique(binding['descriptor']['options'])
    for t in collections['tools'].values():
        Draft202012Validator.check_schema(t['input_schema'])
        if 'output_schema' in t:Draft202012Validator.check_schema(t['output_schema'])
        for id in t.get('resource_ids',[]):resources.ref(id)
    for c in collections['configurations'].values():
        for name in ('instructions','capabilities','policies'):unique(c[name])
        unique(c['secret_requirements'],'handle')
        for i in c['instructions']:parts(i['parts']);provenance(i['provenance'])
        for capability in c['capabilities']:
            for id in capability['resource_ids']:resources.ref(id)
        for id in c.get('environment_ids',[]):need(id in collections['environments'],'missing configuration environment')
    for environment in collections['environments'].values():
        for id in environment['resource_ids']:resources.ref(id)
    for execution in collections['executions'].values():
        need(execution['participant_id'] in participants,'missing execution participant')
        need(set(execution['context_ids'])<=collections['contexts'].keys(),'missing execution context')
    for r in resources.records.values():
        if r['purpose']=='session_memory':need('provenance' in r,'memory provenance missing')
        if 'provenance' in r:provenance(r['provenance'])
    for context in collections['contexts'].values():
        need(context['branch_id'] in collections['branches'],'missing context branch')
        boundary=context['at_event_id']
        if boundary is not None:need(boundary in collections['branches'][context['branch_id']]['event_ids'],'context boundary outside branch')
        if 'configuration_id' in context:need(context['configuration_id'] in collections['configurations'],'missing context configuration')
        need(set(context['tool_ids'])<=collections['tools'].keys(),'missing context tool');unique(context['inputs'])
        typed=[]
        for index,item in enumerate(context['inputs']):
            parts(item['parts'])
            for source in item['source_events']:
                event_ref(source)
                if 'capture_id' not in source and boundary is not None:need(events[source['event_id']]['sequence']<=events[boundary]['sequence'],'context uses future event')
            if item['kind'] in ('tool_call','tool_result'):
                if item['kind']=='tool_call':need(item['tool_id'] in collections['tools'],'missing context call tool')
                typed.append({'id':item['id'],'kind':item['kind'],'data':item})
        history_state(typed)
    heads={id:[] for id in collections['branches']}
    for cp in collections['checkpoints'].values():
        need(cp['branch_id'] in collections['branches'],'missing checkpoint branch');branch=collections['branches'][cp['branch_id']]
        need(cp['at_event_id'] is None and not branch['event_ids'] or cp['at_event_id'] in branch['event_ids'],'checkpoint boundary outside branch')
        if cp['at_event_id']==branch['head_event_id']:heads[branch['id']].append(cp)
        if cp['context_id']:
            need(cp['context_id'] in collections['contexts'],'missing checkpoint context')
            ctx=collections['contexts'][cp['context_id']];need(ctx['branch_id']==cp['branch_id'],'checkpoint context branch mismatch')
            if ctx['at_event_id'] is not None:need(cp['at_event_id'] is not None and events[ctx['at_event_id']]['sequence']<=events[cp['at_event_id']]['sequence'],'checkpoint context is newer than boundary')
        if cp['configuration_id']:need(cp['configuration_id'] in collections['configurations'],'missing checkpoint configuration')
        ids=branch['event_ids'][:branch['event_ids'].index(cp['at_event_id'])+1] if cp['at_event_id'] else []
        state=history_state([events[id] for id in ids],external_calls,external_requests)
        unique(cp['open_calls'],'call_id');unique(cp['open_decisions'],'request_id');unique(cp['tasks'],'task_id')
        for call in cp['open_calls']:need(call['call_id'] in state['calls'] and call['call_id'] not in state['closed_calls'],'checkpoint call not open')
        for decision in cp['open_decisions']:need(decision['request_id'] in state['requests'] and decision['request_id'] not in state['decisions'],'checkpoint decision not open')
        for task in cp['tasks']:need(task['task_id'] in state['tasks'] and task['revision']==state['tasks'][task['task_id']]['revision'],'checkpoint task revision mismatch')
        coverage={c['scope']:c['status'] for c in doc['coverage']}
        if cp['knowledge']!='unknown':
            if coverage['tools']=='complete':need({x['call_id'] for x in cp['open_calls']}==state['calls'].keys()-state['closed_calls'].keys(),'unaccounted open call')
            if coverage['decisions']=='complete':need({x['request_id'] for x in cp['open_decisions']}==state['requests'].keys()-state['decisions'].keys(),'unaccounted open decision')
    for id,cps in heads.items():need(len(cps)==1,'branch requires exactly one head checkpoint')
    for branch in collections['branches'].values():history_state([events[id] for id in branch['event_ids']],external_calls,external_requests)
    nonempty={name:bool(doc[name]) for name in ['participants','branches','executions','contexts','resources']}
    nonempty.update(configuration=bool(doc['configurations']),environment=bool(doc['environments']),conversation=any(e['kind']=='message' for e in events.values()),tools=bool(doc['tools']) or bool(calls),decisions=bool(requests),tasks=bool(task_revisions),native=any(r['purpose']=='native' for r in resources.records.values()),usage=bool(doc.get('usage')))
    for cov in doc['coverage']:
        if cov['status']=='known_empty':need(not nonempty.get(cov['scope'],False),'known-empty coverage contains data')
    for loss in collections['losses'].values():
        for r in loss.get('references',[]):
            name={'event':'events','resource':'resources','context':'contexts','configuration':'configurations','participant':'participants','execution':'executions','branch':'branches','checkpoint':'checkpoints','tool':'tools','environment':'environments'}.get(r['type'])
            if name:need(r['id'] in collections[name],'missing loss reference')
    result={'collections':collections,'resources':resources,'unsupported_features':sorted(set(doc['required_features'])-SUPPORTED)}
    from .streams import assemble_streams
    result['streams']=assemble_streams(doc,result)
    return result
