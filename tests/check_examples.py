"""Validate example structure, resource integrity, and selected local references.

This fixture checker is deliberately not a full ASIF conformance implementation.
"""
import base64
import copy
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import wave
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples'
SCHEMA = json.loads((ROOT / 'schemas/session.schema.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA)

def unique(records):
    result = {record['id']: record for record in records}
    assert len(result) == len(records), 'duplicate identity'
    return result

def check(document, folder):
    VALIDATOR.validate(document)
    collections = {key: unique(document[key]) for key in ['participants', 'events', 'branches',
                   'contexts', 'configurations', 'resources', 'tools', 'checkpoints']}
    events, resources = collections['events'], collections['resources']
    sequences = [event['sequence'] for event in events.values()]
    assert len(set(sequences)) == len(sequences), 'duplicate event sequence'
    for event in events.values():
        assert event['actor_id'] in collections['participants'], 'missing actor'
        for cause in event['causes']:
            if 'capture_id' not in cause:
                assert cause['event_id'] in events, 'missing cause'
                assert events[cause['event_id']]['sequence'] < event['sequence'], 'noncausal serialization'
    for branch in collections['branches'].values():
        assert all(e in events for e in branch['event_ids']), 'missing branch event'
        assert branch['head_event_id'] == (branch['event_ids'][-1] if branch['event_ids'] else None), 'wrong branch head'
    for ctx in collections['contexts'].values():
        assert ctx['branch_id'] in collections['branches'], 'missing context branch'
        assert ctx['at_event_id'] is None or ctx['at_event_id'] in events, 'missing context boundary'
        assert all(t in collections['tools'] for t in ctx['tool_ids']), 'missing context tool'
        if 'configuration_id' in ctx:
            assert ctx['configuration_id'] in collections['configurations'], 'missing configuration'
        for item in ctx['inputs']:
            for source in item['source_events']:
                assert 'capture_id' in source or source['event_id'] in events, 'missing context source'
    for checkpoint in collections['checkpoints'].values():
        assert checkpoint['branch_id'] in collections['branches'], 'missing checkpoint branch'
        assert checkpoint['at_event_id'] == collections['branches'][checkpoint['branch_id']]['head_event_id'], 'wrong checkpoint boundary'
        assert checkpoint['context_id'] is None or checkpoint['context_id'] in collections['contexts'], 'missing checkpoint context'

    # The examples intentionally use resource_id only for actual resource references.
    # Arbitrary vendor payloads are outside this fixture-specific traversal contract.
    def references(value):
        if isinstance(value, dict):
            if 'resource_id' in value:
                assert value['resource_id'] in resources, 'missing resource reference'
            for key, child in value.items():
                if key not in ('input_schema', 'output_schema'):
                    references(child)
        elif isinstance(value, list):
            for child in value:
                references(child)
    references(document)
    for loss in document['losses']:
        for reference in loss.get('references', []):
            if reference['type'] == 'resource':
                assert reference['id'] in resources, 'missing loss resource'

    embedded, paths = 0, []
    for resource in resources.values():
        if resource['availability'] != 'embedded':
            continue  # In particular, do not fetch external locators.
        if 'text' in resource:
            raw = resource['text'].encode('utf-8')
        elif 'data' in resource:
            raw = base64.b64decode(resource['data'], validate=True)
        else:
            name = resource['path']
            assert '\\' not in name and ':' not in name, 'unsafe resource path'
            assert all(p not in ('', '.', '..') for p in name.split('/')), 'unsafe resource path'
            assert not PurePosixPath(name).is_absolute(), 'unsafe resource path'
            file = folder / name
            assert file.resolve().is_relative_to(folder.resolve()), 'unsafe resource path'
            current = folder
            for segment in name.split('/'):
                current = current / segment
                assert not current.is_symlink(), 'symlink resource path'
            assert file.is_file(), 'missing resource file'
            raw = file.read_bytes()
            paths.append(name)
        assert len(raw) == resource['bytes'], 'resource length mismatch'
        assert hashlib.sha256(raw).hexdigest() == resource['sha256'], 'resource digest mismatch'
        if resource['media_type'] == 'audio/wav':
            with wave.open(io.BytesIO(raw), 'rb') as audio:
                assert audio.getnframes() == 800 and audio.getframerate() == 8000
                assert audio.readframes(800) == b'\0\0' * 800
        embedded += 1
    return {'embedded_resources_verified': embedded, 'file_paths': paths}

results = []
for file in sorted(EXAMPLES.glob('*.session.json')):
    result = check(json.loads(file.read_text()), file.parent)
    results.append({'example': file.name, 'passed': True, **result})

base = json.loads((EXAMPLES / 'image-and-document.session.json').read_text())
negatives = [
    ('corrupt-digest', lambda d: d['resources'][0].update(sha256='0' * 64), 'resource digest mismatch'),
    ('wrong-byte-count', lambda d: d['resources'][0].update(bytes=0), 'resource length mismatch'),
    ('missing-reference', lambda d: d['events'][0]['data']['parts'][1].update(resource_id='absent'), 'missing resource reference'),
    ('path-traversal', lambda d: d['resources'][0].update(path='../SPEC.md'), 'unsafe resource path'),
    ('wrong-branch-head', lambda d: d['branches'][0].update(head_event_id='e1'), 'wrong branch head')]
for name, mutate, expected in negatives:
    value = copy.deepcopy(base)
    mutate(value)
    try:
        check(value, EXAMPLES)
    except AssertionError as error:
        assert str(error) == expected, (name, error)
    else:
        raise AssertionError('negative case accepted: ' + name)

report = {'scope': 'Synthetic fixture structure, embedded bytes and selected references only',
          'examples_passed': len(results), 'negative_checks_passed': len(negatives),
          'embedded_resources_verified': sum(r['embedded_resources_verified'] for r in results),
          'file_attachments_verified': len({p for r in results for p in r['file_paths']}),
          'full_semantic_conformance_tested': False, 'interoperability_tested': False,
          'continuation_tested': False, 'results': results}
(ROOT / 'tests/example-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'results'}, indent=2))
