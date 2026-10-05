"""Selected continuation invariants, not a runtime importer or full ASIF validator."""
import base64
from datetime import datetime
import hashlib
import json
from pathlib import Path
import unicodedata
from jsonschema import Draft202012Validator
from .common import Invalid, need, unique, relative, acyclic, pointer
from .core import validate_document, Validator, SUPPORTED
from .requirements import plan_requirements
from .capabilities import inspect_capabilities
from .workspace import workspace_states, check_git

ROOT=Path(__file__).resolve().parents[1]
SESSION=Draft202012Validator(json.loads((ROOT/'schemas/session.schema.json').read_text()))
REPORT=Validator(json.loads((ROOT/'schemas/continuation-report.schema.json').read_text()))
FEATURE='asif.portable-continuation/0.2'
def subject(kind,id,owner=None):
    s={'kind':kind,'id':id}
    if owner is not None:s['owner_id']=owner
    return s
def key(s):return (s['kind'],s.get('owner_id'),s['id'])
def date(value):
    out=datetime.fromisoformat(value.replace('Z','+00:00'));need(out.tzinfo is not None,'time needs timezone');return out

def inspect_session(doc,folder):
    validated=validate_document(doc,folder)
    need('continuation' in doc,'continuation profile absent')
    p=doc['continuation']
    core={name:unique(doc[name]) for name in ['events','contexts','checkpoints','configurations','resources','environments','tools','branches','participants']}
    for name in ['workspaces','dependencies','service_bindings','operations','native_imports','plans']:unique(p[name])
    resources=core['resources']
    deps=unique(p['dependencies']);workspaces=unique(p['workspaces']);operations=unique(p['operations'])
    bindings=unique(p['configuration_bindings'],'configuration_id');services=unique(p['service_bindings']);native=unique(p['native_imports'])
    states=workspace_states(p)
    pending=set(deps)
    while pending:
        roots={id for id in pending if not (set(deps[id]['depends_on'])&pending)}
        need(roots,'dependency cycle');pending-=roots
    for d in deps.values():
        need(set(d['depends_on'])<=deps.keys(),'missing dependency')
        need(set(d['resource_ids'])<=resources.keys(),'missing dependency resource')
        if d['kind']=='tool':need(d['tool_id'] in core['tools'],'missing dependency tool')
    for w in workspaces.values():
        check_git(w,validated['resources'],deps)
        need(w['environment_id'] in core['environments'],'missing workspace environment')
        if w['base_snapshot_id'] is not None:need(w['base_snapshot_id'] in workspaces,'missing workspace base')
        paths=set()
        for entry in w['entries']:
            relative(entry['path']);need(entry['path'] not in paths,'duplicate workspace path');paths.add(entry['path'])
            if entry['kind']=='file':need(entry['resource_id'] in resources,'missing workspace resource')
        for deletion in w['deletions']:relative(deletion)
        if 'git' in w:
            g=w['git'];need(set(g['bundle_resource_ids'])<=resources.keys(),'missing Git bundle')
            for entry in g['index_entries']:
                relative(entry['path'])
                if entry['resource_id']:need(entry['resource_id'] in resources,'missing index blob')
            need(set(g['lfs_dependency_ids'])<=deps.keys(),'missing LFS dependency')
            for module in g['submodules']:
                relative(module['path']);need(module['dependency_id'] in deps,'missing submodule dependency')
    for op in operations.values():
        handler=op['recovery']['handler_dependency_id']
        need(handler is None or handler in deps,'missing recovery handler')
        need(set(op['evidence_resource_ids']+op['recovery']['evidence_resource_ids'])<=resources.keys(),'missing operation evidence')
        if op['recovery']['strategy']=='restart':
            need(op['replay']=='idempotent' and op['recovery']['idempotency_ref'] and op['recovery']['evidence_resource_ids'],'unsafe restart declaration')
    plan_subjects={}
    for plan in p['plans']:
        need(plan['checkpoint_id'] in core['checkpoints'],'missing checkpoint')
        cp=core['checkpoints'][plan['checkpoint_id']]
        need(plan['context_id']==cp['context_id'] and plan['configuration_id']==cp['configuration_id'],'checkpoint binding mismatch')
        need(plan['context_id'] in core['contexts'] and plan['configuration_id'] in core['configurations'],'missing context/configuration')
        ctx=core['contexts'][plan['context_id']];config=core['configurations'][plan['configuration_id']]
        need(ctx['purpose']=='continuation' and ctx['at_event_id']==cp['at_event_id'] and ctx['branch_id']==cp['branch_id'],'stale continuation context')
        need(ctx.get('configuration_id')==config['id'],'context configuration mismatch')
        branch=core['branches'][cp['branch_id']]
        need(branch['head_event_id']==cp['at_event_id'],'checkpoint is not branch head')
        need(set(plan['workspace_ids'])<=workspaces.keys(),'missing selected workspace')
        need(set(plan['dependency_ids'])<=deps.keys(),'missing selected dependency')
        need(set(plan['service_binding_ids'])<=services.keys(),'missing selected service')
        need(set(plan['operation_ids'])<=operations.keys(),'missing selected operation')
        selected_deps=set(plan['dependency_ids'])
        for id in selected_deps:need(set(deps[id]['depends_on'])<=selected_deps,'incomplete dependency closure')
        roots={workspaces[id]['root_id'] for id in plan['workspace_ids']}
        need(len(roots)==len(plan['workspace_ids']),'multiple selected states for root')
        for id in plan['workspace_ids']:need(workspaces[id]['at_event_id']==cp['at_event_id'],'workspace boundary mismatch')
        if plan['cwd']:
            need(plan['cwd']['root_id'] in roots,'missing cwd root');relative(plan['cwd']['relative_path'],True)
        for path in plan['path_references']:
            need(path['root_id'] in roots,'missing mapped root');relative(path['relative_path'],True)
            group={'event':'events','resource':'resources','environment':'environments','configuration':'configurations'}
            entities=deps if path['entity_type']=='dependency' else core[group[path['entity_type']]]
            need(path['entity_id'] in entities,'missing path mapping entity')
            need(path['json_pointer'].startswith('/'),'invalid JSON pointer')
            try:value=pointer(entities[path['entity_id']],path['json_pointer'])
            except Invalid as exc:raise Invalid('path mapping pointer missing: '+str(exc)) from exc
            need(isinstance(value,str),'path mapping does not address a string')
        accounting=unique(plan['context_accounting'],'event_id');inputs=unique(ctx['inputs'])
        need(set(accounting)==set(branch['event_ids']),'incomplete context accounting')
        for a in accounting.values():need(set(a['input_ids'])<=inputs.keys(),'missing accounted input')
        calls={};terminal=set();indexes={}
        for item in ctx['inputs']:
            for source in item['source_events']:
                if 'capture_id' not in source:need(source['event_id'] in core['events'],'missing context source')
            if item['kind']=='tool_call':
                need(item['call_id'] not in calls,'duplicate context call');need(item['tool_id'] in core['tools'],'unknown context tool');calls[item['call_id']]=item
            if item['kind']=='tool_result':
                call=item['call_id'];need(call in calls,'orphan context result');need(call not in terminal,'result after terminal')
                need(item['result_index']>indexes.get(call,-1),'result order');indexes[call]=item['result_index']
                if item['terminal']:terminal.add(call)
            if item['kind'] in ('tool_call','tool_result'):
                for source in item['source_events']:
                    if 'capture_id' not in source:
                        ev=core['events'][source['event_id']]
                        need(ev['kind']==item['kind'] and ev['data']['call_id']==item['call_id'],'context tool correlation changed')
                        if 'transformation' not in item:
                            fields=['tool_id','arguments','arguments_status'] if item['kind']=='tool_call' else ['parts','result_index','terminal','outcome']
                            need(all(item[field]==ev['data'][field] for field in fields),'unreported tool context transformation')
        selected_ops=[operations[id] for id in plan['operation_ids']]
        bound_calls=[op.get('call_id') for op in selected_ops if 'call_id' in op]
        need(len(bound_calls)==len(set(bound_calls)),'duplicate operation call binding')
        need({x['call_id'] for x in cp['open_calls']}<=set(bound_calls),'unbound open call')
        need({x['call_id'] for x in cp['open_calls']}==set(calls)-terminal,'open call state disagrees with context')
        for op in selected_ops:
            if 'call_id' in op:need(op['call_id'] in calls,'operation call absent from context')
            handler=op['recovery']['handler_dependency_id'];need(handler is None or handler in selected_deps,'recovery dependency not selected')
        next_action=plan['next_action']
        if next_action['kind']=='reconcile_operation':need(next_action['operation_id'] in plan['operation_ids'],'next operation not selected')
        if next_action['kind']=='await_decision':need(next_action['request_id'] in {x['request_id'] for x in cp['open_decisions']},'next decision not pending')
        if next_action['kind']=='resume_native':need(next_action['native_import_id']==plan['native_import_id'] and plan['native_import_id'] is not None,'next native import mismatch')
        need(config['id'] in bindings,'missing effective configuration binding')
        cb=bindings[config['id']];instructions=unique(config['instructions']);rules=unique(cb['instruction_rules'],'instruction_id')
        need(set(cb['effective_order'])==set(instructions)==set(rules),'incomplete instruction bindings')
        priorities=[rules[id]['priority'] for id in cb['effective_order']];need(priorities==sorted(priorities),'instruction precedence mismatch')
        need(set(cb['policy_ids'])=={x['id'] for x in config['policies']},'incomplete policy bindings')
        for rule in rules.values():
            if rule['scope']['kind']!='global':need(rule['scope']['root_id'] in roots,'instruction root not selected')
            if rule['scope']['kind']=='path_prefix':relative(rule['scope']['relative_path'],True)
        for id in plan['service_binding_ids']:
            svc=services[id];need(set(svc['dependency_ids'])<=selected_deps,'service dependency not selected')
            need(set(svc['secret_handles'])<={x['handle'] for x in config['secret_requirements']},'undeclared secret handle')
        if plan['native_import_id']:need(plan['native_import_id'] in native,'missing native import')
        plan_subjects[plan['id']]=plan_requirements(doc,plan,states)
    return plan_subjects

def inspect_report(doc,raw,report,folder,*,now,current_snapshot=None):
    expected=inspect_session(doc,folder);REPORT.validate(report)
    source=report['source'];need(source['session_id']==doc['session']['id'] and source['capture_id']==doc['capture']['id'],'report source mismatch')
    need(source['document_sha256']==hashlib.sha256(raw).hexdigest(),'report digest mismatch')
    need(source['plan_id'] in expected,'report plan missing')
    need(date(report['assessed_at'])<=now<date(report['expires_at']),'stale assessment')
    need(date(report['assessed_at'])<date(report['expires_at']),'invalid assessment interval')
    assessments={key(a['subject']):a for a in report['assessments']}
    need(len(assessments)==len(report['assessments']),'duplicate assessment')
    requirements={key(item['subject']):item['required'] for item in expected[source['plan_id']]}
    needed=set(requirements)
    need(needed<=assessments.keys(),'missing subject assessment')
    need(needed==assessments.keys(),'unexpected subject assessment')
    for k,required in requirements.items():need(assessments[k]['required']==required,'selected subject downgraded to optional' if required else 'optional subject marked required')
    evidence=unique(report['evidence'])
    for a in report['assessments']:need(set(a['evidence_ids'])<=evidence.keys(),'missing assessment evidence')
    for t in report['transformations']:
        need(key(t['subject']) in needed,'unexpected transformation subject')
        need(set(t['evidence_ids'])<=evidence.keys(),'missing acceptance evidence')
        if assessments[key(t['subject'])]['status']=='omitted':need(bool(t['losses']),'omission transformation requires loss')
    for result in [report['import_result'],report['continuation_result']]:need(set(result['evidence_ids'])<=evidence.keys(),'missing result evidence')
    if report['evaluation_mode']=='synthetic':
        need(report['import_result']['status']=='not_attempted' and report['continuation_result']['status']=='not_tested','synthetic execution claim')
    else:
        need(all(e['kind']!='synthetic' for e in evidence.values()),'synthetic evidence in observed report')
        for result,success,kind in [(report['import_result'],'imported','import'),(report['continuation_result'],'continued','continuation')]:
            if result['status']==success:need(any(evidence[id]['kind']==kind for id in result['evidence_ids']),'missing runtime evidence')
    p=doc['continuation'];plan=next(x for x in p['plans'] if x['id']==source['plan_id'])
    action=plan['next_action']['kind'];agent=action in ('model_request','resume_native')
    cp=next(x for x in doc['checkpoints'] if x['id']==plan['checkpoint_id'])
    if report['import_result']['status']=='imported':need(agent,'import claim exceeds assessed action')
    if report['continuation_result']['status']=='continued':need(agent or action=='reconcile_operation','continuation claim exceeds assessed action')
    def assessed(kind,id,owner=None):return assessments[key(subject(kind,id,owner))]
    def blocker(kind,id,owner=None):need(assessed(kind,id,owner)['status'] in ('unresolved','unsupported','omitted'),'known blocker marked supported')
    config=next(c for c in doc['configurations'] if c['id']==plan['configuration_id'])
    if config['knowledge']!='effective':blocker('configuration',config['id'])
    binding=next(b for b in p['configuration_bindings'] if b['configuration_id']==config['id'])
    for rule in binding['instruction_rules']:
        if rule['authority']=='unknown' or rule['merge_behavior']=='unknown':blocker('instruction',rule['instruction_id'],config['id'])
    if plan['boundary']['consistency']!='consistent' or plan['boundary']['method']=='best_effort':blocker('plan',plan['id'])
    if agent and cp['open_decisions']:blocker('plan',plan['id'])
    ctx=next(c for c in doc['contexts'] if c['id']==plan['context_id'])
    if ctx['fidelity'] in ('partial','unknown'):blocker('context',ctx['id'])
    if any(a['disposition']=='unavailable' for a in plan['context_accounting']):blocker('context',ctx['id'])
    for r in doc['resources']:
        k=key(subject('resource',r['id']))
        if k in needed and r['availability'] in ('unavailable','excluded','redacted','unknown'):blocker('resource',r['id'])
    for op in p['operations']:
        if op['id'] not in plan['operation_ids']:continue
        reconciling=action=='reconcile_operation' and op['id']==plan['next_action']['operation_id']
        if reconciling:
            if op['recovery']['strategy'] not in ('reconcile','reconnect'):blocker('operation',op['id'])
            a=assessed('operation',op['id'])
            if a['status']=='supported':
                resolved=a.get('resolved',{})
                need(bool(a['evidence_ids']) and resolved.get('recovery_strategy')==op['recovery']['strategy'] and op['external_identity'] is not None and resolved.get('external_identity')==op['external_identity'],'unverified operation recovery')
        elif op['state'] in ('pending','running','outcome_unknown'):blocker('operation',op['id'])
    for owner_kind,owners in [('checkpoint_requirement',[cp]),('environment_requirement',doc['environments'])]:
        for owner in owners:
            for requirement in owner['requirements']:
                k=key(subject(owner_kind,requirement['id'],owner['id']))
                if k not in needed:continue
                a=assessments[k]
                if a['status']=='supported':
                    resolved=a.get('resolved',{})
                    need(bool(a['evidence_ids']) and resolved.get('status')=='available','unverified core requirement')
                    if 'secret_handle' in requirement:need(requirement['secret_handle'] in resolved.get('secret_handles',[]),'unresolved requirement secret')
    for d in p['dependencies']:
        if d['id'] in plan['dependency_ids']:
            a=assessed('dependency',d['id'])
            if a['status']=='supported':
                resolved=a.get('resolved',{})
                need(resolved.get('identity')==d['identity'] and resolved.get('version') in d['accepted_versions'],'unverified dependency binding')
                runtime=report['destination']['runtime']
                need(runtime['os'] in d['platform']['os'] and runtime['architecture'] in d['platform']['architectures'],'unsupported dependency platform')
    for svc in p['service_bindings']:
        if svc['id'] in plan['service_binding_ids']:
            a=assessed('service',svc['id'])
            if a['status']=='supported':
                resolved=a.get('resolved',{})
                need(resolved.get('account')==svc['account'] and resolved.get('audience')==svc['audience'],'wrong service identity')
                need(set(svc['scopes'])<=set(resolved.get('scopes',[])) and set(svc['secret_handles'])<=set(resolved.get('secret_handles',[])),'unresolved service access')
                need(bool(resolved.get('endpoint')),'unresolved service endpoint')
    if plan['native_import_id']:
        n=next(x for x in p['native_imports'] if x['id']==plan['native_import_id'])
        if assessed('native_import',n['id'])['status']=='supported':
            need(report['destination']['runtime']['agent']['version'] in n['accepted_target_agent_versions'],'unsupported native target version')
    for f in doc['required_features']:
        if f not in SUPPORTED:blocker('feature',f)
    selected_roots={w['root_id'] for w in p['workspaces'] if w['id'] in plan['workspace_ids']}
    roots={w['root_id'] for w in p['workspaces'] if w['id'] in plan['workspace_ids'] and (assessed('workspace',w['id'])['required'] or assessed('workspace',w['id'])['status'] in ('supported','adapted'))}
    mappings=unique(report['path_bindings'],'root_id');need(roots<=mappings.keys()<=selected_roots,'incomplete path bindings')
    flattened=workspace_states(p)
    for w in p['workspaces']:
        if w['id'] not in plan['workspace_ids'] or w['root_id'] not in mappings:continue
        mapping=mappings[w['root_id']];paths=[]
        for e in flattened[w['id']].values():
            value=e['path'];norm=mapping['unicode_normalization']
            if norm!='none':value=unicodedata.normalize(norm,value)
            if not mapping['case_sensitive']:value=value.casefold()
            need(value not in paths,'destination path collision');paths.append(value)
    model=report['model_assessment'];need(model['source']==plan['model_requirements']['source_model'],'model source mismatch')
    if model['fit']=='fits':
        need(model['tokenizer'] is not None and model['input_tokens'] is not None and model['input_limit'] is not None,'unmeasured context fit')
        need(model['input_tokens']+model['output_reserve']<=model['input_limit'],'context exceeds budget')
    else:blocker('model',plan['id'])
    if model['source']!=model['target']:need(assessed('model',plan['id'])['status']!='supported','silent model substitution')
    required=[a for a in report['assessments'] if a['required']]
    blockers=[a for a in required if a['status'] in ('omitted','unresolved','unsupported')]
    pending=False
    for a in report['assessments']:
        if a['status']=='adapted':
            ts=[t for t in report['transformations'] if key(t['subject'])==key(a['subject'])]
            need(ts,'adaptation without mapping')
            if a['required']:pending |= any(not t['accepted'] for t in ts)
    pending |= any(requirements[key(t['subject'])] and not t['accepted'] for t in report['transformations'])
    predicted='blocked' if blockers else 'adaptation_required' if pending else 'ready'
    need(report['outcome']==predicted,'incorrect readiness outcome')
    reasons={key(r['subject']) for r in report['blocking_reasons']}
    need({key(a['subject']) for a in blockers}==reasons,'missing or extraneous blocking reason')
    if not blockers:need(not reasons,'nonblocking report has blocking reasons')
    current=inspect_capabilities(report,plan,now,current_snapshot,doc)
    return {'outcome':predicted,'operational_authorization':False,'evaluation_mode':report['evaluation_mode'],'current_snapshot_matches':current}
