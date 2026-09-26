"""Synthetic profile/report acceptance checks; never starts or imports an agent."""
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError
from continuation_checks import inspect_session, inspect_report, Invalid
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'examples/continuation'
NOW=datetime(2026,9,26,12,30,tzinfo=timezone.utc)
for name in ['session','continuation','continuation-report']:
    Draft202012Validator.check_schema(json.loads((ROOT/'schemas'/(name+'.schema.json')).read_text()))
results=[]
fixtures={}
for file in sorted(FOLDER.glob('*.session.json')):
    slug=file.name.removesuffix('.session.json');raw=file.read_bytes();doc=json.loads(raw)
    report=json.loads(file.with_name(slug+'.report.json').read_text())
    outcome=inspect_report(doc,raw,report,FOLDER,now=NOW)
    assert outcome['operational_authorization'] is False
    fixtures[slug]=(doc,raw,report)
    results.append({'case':slug,'passed':True,'outcome':outcome['outcome']})

base,raw,report=fixtures['another-computer']
def negative_source(name,mutate,expected,fixture='another-computer'):
    doc=copy.deepcopy(fixtures[fixture][0]);mutate(doc)
    try:inspect_session(doc,FOLDER)
    except (Invalid,ValidationError) as exc:
        assert expected is None or expected in str(exc),(name,exc)
    else:raise AssertionError('invalid source accepted: '+name)
    results.append({'case':name,'passed':True,'outcome':'rejected'})

def negative_report(name,mutate,expected,fixture='another-computer',mutate_source=None):
    doc,source,receipt=copy.deepcopy(fixtures[fixture]);mutate(receipt)
    if mutate_source:
        mutate_source(doc);source=(json.dumps(doc,indent=2)+'\n').encode();receipt['source']['document_sha256']=hashlib.sha256(source).hexdigest()
    try:inspect_report(doc,source,receipt,FOLDER,now=NOW)
    except (Invalid,ValidationError) as exc:
        assert expected is None or expected in str(exc),(name,exc)
    else:raise AssertionError('invalid report accepted: '+name)
    results.append({'case':name,'passed':True,'outcome':'rejected'})

negative_source('profile-not-gated',lambda d:d.update(required_features=[]),None)
negative_source('profile-declaration-without-data',lambda d:d.pop('continuation'),None)
negative_source('untyped-context',lambda d:d['contexts'][0]['inputs'][0].pop('kind'),None)
negative_source('orphan-tool-result',lambda d:next(i for i in d['contexts'][0]['inputs'] if i['kind']=='tool_result').update(call_id='absent'),'orphan tool result')
negative_source('changed-tool-result',lambda d:next(i for i in d['contexts'][0]['inputs'] if i['kind']=='tool_result').update(result_index=2),'unreported tool context transformation')
negative_source('stale-context',lambda d:d['contexts'][0].update(at_event_id='e1'),'context uses future event')
negative_source('wrong-checkpoint-config',lambda d:d['checkpoints'][0].update(configuration_id=None),'checkpoint binding mismatch')
negative_source('mixed-workspace-boundary',lambda d:d['continuation']['workspaces'][0].update(at_event_id='e1'),'workspace boundary mismatch')
negative_source('workspace-traversal',lambda d:d['continuation']['workspaces'][0]['entries'][0].update(path='../file'),'unsafe path')
negative_source('missing-path-selector',lambda d:d['continuation']['plans'][0]['path_references'][0].update(json_pointer='/absent'),'path mapping pointer missing')
negative_source('dependency-cycle',lambda d:d['continuation']['dependencies'][0].update(depends_on=['agent-runtime']),'dependency cycle')
negative_source('incomplete-dependency-closure',lambda d:d['continuation']['plans'][0]['dependency_ids'].remove('summary-tool'),'incomplete dependency closure')
negative_source('missing-skill-resource',lambda d:d['continuation']['dependencies'][2]['resource_ids'].append('font-not-captured'),'missing dependency resource')
negative_source('missing-instruction-rule',lambda d:d['continuation']['configuration_bindings'][0].update(instruction_rules=[]),'incomplete instruction bindings')
negative_source('missing-policy-binding',lambda d:d['continuation']['configuration_bindings'][0].update(policy_ids=[]),'incomplete policy bindings')
negative_source('incomplete-context-accounting',lambda d:d['continuation']['plans'][0]['context_accounting'].pop(),'incomplete context accounting')
negative_source('corrupt-resource',lambda d:d['resources'][0].update(sha256='0'*64),'resource integrity')
negative_source('replacement-without-baseline',lambda d:d['continuation']['native_imports'][0].update(conflict_policy='replace_if_unchanged'),None)
negative_source('unsafe-operation-restart',lambda d:d['continuation']['operations'][0]['recovery'].update(strategy='restart'),'unsafe restart declaration','pending-remote-operation')
negative_source('unbound-open-call',lambda d:d['continuation']['plans'][0].update(operation_ids=[]),'unbound open call','pending-remote-operation')
negative_source('undeclared-secret',lambda d:d['continuation']['service_bindings'][0].update(secret_handles=['other-login']),'undeclared secret handle','pending-remote-operation')
negative_report('changed-source-digest',lambda r:r['source'].update(document_sha256='0'*64),'report digest mismatch')
negative_report('expired-assessment',lambda r:r.update(expires_at='2026-09-26T12:01:00Z'),'stale assessment')
negative_report('missing-assessment',lambda r:r['assessments'].pop(),'missing subject assessment')
negative_report('optional-downgrade',lambda r:r['assessments'][0].update(required=False),'selected subject downgraded')
negative_report('context-overflow',lambda r:r['model_assessment'].update(input_tokens=7999),'context exceeds budget')
negative_report('unknown-tokenizer',lambda r:r['model_assessment'].update(tokenizer=None),'unmeasured context fit')
negative_report('silent-model-substitution',lambda r:r['model_assessment']['target'].update(id='different-model'),'silent model substitution')
negative_report('unverified-dependency-version',lambda r:next(a for a in r['assessments'] if a['subject']['kind']=='dependency')['resolved'].update(version='9'),'unverified dependency binding')
negative_report('unsupported-platform',lambda r:r['destination']['runtime'].update(os='other-os'),'unsupported dependency platform')
negative_report('missing-root-binding',lambda r:r.update(path_bindings=[]),'incomplete path bindings')
negative_report('partial-capture-marked-ready',lambda r:None,'known blocker marked supported',mutate_source=lambda d:d['continuation']['plans'][0]['boundary'].update(consistency='partial'))
negative_report('partial-configuration-marked-ready',lambda r:None,'known blocker marked supported',mutate_source=lambda d:d['configurations'][0].update(knowledge='partial'))
negative_report('unknown-authority-marked-ready',lambda r:None,'known blocker marked supported',mutate_source=lambda d:d['continuation']['configuration_bindings'][0]['instruction_rules'][0].update(authority='unknown'))
negative_report('unavailable-resource-marked-ready',lambda r:None,'known blocker marked supported',mutate_source=lambda d:(d['resources'][-2].pop('text'),d['resources'][-2].update(availability='unavailable',explanation='Missing required skill resource.')))
negative_report('adaptation-without-mapping',lambda r:r['transformations'].pop(),'adaptation without mapping','another-agent')
negative_report('pending-operation-marked-ready',lambda r:r.update(outcome='ready'),'incorrect readiness outcome','pending-remote-operation')
negative_report('synthetic-import-claim',lambda r:r['import_result'].update(status='imported'),'synthetic execution claim')

def wrong_account(r):
    a=next(a for a in r['assessments'] if a['subject']['kind']=='service')
    a.update(status='supported',resolved={'account':{'provider':'example','subject':'account-B'},'audience':'example.publisher','scopes':['reports:write'],'secret_handles':['publisher-login'],'endpoint':'https://publisher.example.invalid'})
negative_report('wrong-service-account',wrong_account,'wrong service identity','pending-remote-operation')

def collision(d):
    w=d['continuation']['workspaces'][0];entry=copy.deepcopy(w['entries'][0]);entry['path']='INVENTORY.CSV';w['entries'].append(entry)
negative_report('destination-case-collision',lambda r:r['path_bindings'][0].update(case_sensitive=False),'destination path collision',mutate_source=collision)
# Explicitly accepted transformations change the simulated outcome, not execution authority.
doc,source,receipt=copy.deepcopy(fixtures['another-agent'])
for transformation in receipt['transformations']:transformation['accepted']=True
receipt['outcome']='ready'
assert inspect_report(doc,source,receipt,FOLDER,now=NOW)['operational_authorization'] is False
results.append({'case':'accepted-adaptations-simulated','passed':True,'outcome':'ready'})
summary={'asif_version':'0.3','profile':'asif.portable-continuation/0.1','scope':'Synthetic profile shape, selected semantic invariants and destination report outcomes','checks':len(results),'passed':len(results),'real_runtime_tests':0,'independent_implementations':0,'operational_authorization':False,'results':results}
(ROOT/'tests/continuation-results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
