"""Structural checks only; this is not an ASIF semantic validator."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / 'schemas/session.schema.json').read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema)
example = json.loads((ROOT / 'examples/awaiting-approval.session.json').read_text())
results = []

def check(name, mutate, expected):
    value = copy.deepcopy(example)
    mutate(value)
    errors = list(validator.iter_errors(value))
    assert (not errors) == expected, (name, [e.message for e in errors])
    results.append({'case': name, 'expected_shape': 'valid' if expected else 'invalid', 'passed': True})

check('awaiting-approval-example', lambda x: None, True)
check('unknown-optional-property', lambda x: x.update(future={'unknown': [1, 'שלום']}), True)
check('0.4-version-rejected', lambda x: x.update(asif_version='0.4'), False)
check('0.3-version-rejected', lambda x: x.update(asif_version='0.3'), False)
check('future-version-rejected', lambda x: x.update(asif_version='0.6'), False)
check('missing-version-rejected', lambda x: x.pop('asif_version'), False)
check('previous-version-rejected', lambda x: x.update(asif_version='0.2-draft.4'), False)
check('missing-state-declaration', lambda x: x.pop('checkpoints'), False)
check('missing-coverage-domain', lambda x: x['coverage'].pop(), False)
check('duplicate-coverage-domain', lambda x: x['coverage'][-1].update(scope='participants'), False)
check('unknown-coverage-status', lambda x: x['coverage'][0].update(status='probably-complete'), False)
check('missing-event-actor', lambda x: x['events'][0].pop('actor_id'), False)
check('unknown-core-kind', lambda x: x['events'][0].update(kind='vendor-magic'), False)
check('missing-message-parts', lambda x: x['events'][0]['data'].pop('parts'), False)
check('missing-call-correlation', lambda x: x['events'][2]['data'].pop('call_id'), False)
check('missing-argument-completeness', lambda x: x['events'][2]['data'].pop('arguments_status'), False)
check('synthetic-without-method', lambda x: x['events'][0]['provenance'].pop('method'), False)
check('synthetic-without-inputs', lambda x: x['events'][0]['provenance'].pop('inputs'), False)
check('incomplete-external-reference', lambda x: x['events'][1]['causes'][0].update(capture_id='elsewhere'), False)
check('no-branch', lambda x: x.update(branches=[]), False)
check('duplicate-event-in-branch', lambda x: x['branches'][0]['event_ids'].append('e1'), False)
check('no-head-checkpoint', lambda x: x.update(checkpoints=[]), False)
check('invented-open-call-state', lambda x: x['checkpoints'][0]['open_calls'][0].update(state='safe-to-repeat'), False)
check('exact-context-without-settings', lambda x: x['contexts'][0].update(fidelity='exact'), False)
check('missing-context-input-provenance', lambda x: x['contexts'][0]['inputs'][0].pop('source_events'), False)
check('missing-tool-contract', lambda x: x['tools'][0].pop('input_schema'), False)

def resource(value, **fields):
    value['resources'] = [{'id':'r1','media_type':'text/plain','purpose':'input',**fields}]

check('unavailable-resource-explained', lambda x: resource(x, availability='unavailable', explanation='Source bytes unavailable.'), True)
check('unavailable-resource-unexplained', lambda x: resource(x, availability='unavailable'), False)
check('embedded-resource-missing-integrity', lambda x: resource(x, availability='embedded', text='abc'), False)
check('embedded-two-encodings', lambda x: resource(x, availability='embedded', text='abc', data='YWJj', bytes=3, sha256='0'*64), False)
check('external-with-embedded-content', lambda x: resource(x, availability='external', locator='urn:example:r1', explanation='External content.', text='abc'), False)

result = {'asif_version':'0.5', 'scope':'JSON Schema structure only', 'schema_valid':True, 'checks':len(results), 'passed':len(results), 'semantic_conformance_tested':False, 'interoperability_tested':False, 'continuation_tested':False, 'results':results}
(ROOT / 'tests/results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'results'}, indent=2))
