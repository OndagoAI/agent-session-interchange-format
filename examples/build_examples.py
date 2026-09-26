"""Build deterministic, invented ASIF examples and small public fixture assets."""
import base64
import copy
import hashlib
import io
import json
from pathlib import Path
import struct
import wave
import zlib

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
SCOPES = ['participants', 'conversation', 'branches', 'executions', 'contexts',
          'configuration', 'tools', 'decisions', 'tasks', 'resources',
          'environment', 'native', 'usage']

def text(value):
    return {'kind': 'text', 'text': value}

def part(identifier, description):
    return {'kind': 'resource', 'resource_id': identifier, 'description': description}

def provenance():
    return {'mode': 'synthetic', 'producer': 'asif-examples',
            'method': 'Authored synthetic fixture; no real user data or model execution.', 'inputs': []}

def event(identifier, actor, kind, data):
    return {'id': identifier, 'sequence': 0, 'actor_id': actor, 'kind': kind,
            'causes': [], 'provenance': provenance(), 'data': data}

def message(identifier, role, parts):
    return event(identifier, 'person' if role == 'user' else 'agent', 'message',
                 {'role': role, 'parts': parts})

def resource(identifier, media_type, content, *, storage='text', filename=None, purpose='input'):
    raw = content.encode('utf-8') if isinstance(content, str) else content
    result = {'id': identifier, 'media_type': media_type, 'availability': 'embedded',
              'purpose': purpose, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
              'provenance': provenance()}
    if storage == 'path':
        (ASSETS / filename).write_bytes(raw)
        result['path'] = 'assets/' + filename
        result['name'] = filename
    elif storage == 'data':
        result['data'] = base64.b64encode(raw).decode('ascii')
    else:
        result['text'] = raw.decode('utf-8')
    return result

def context(identifier, at, inputs, *, purpose='model_request', tools=()):
    return {'id': identifier, 'branch_id': 'main', 'at_event_id': at, 'purpose': purpose,
            'fidelity': 'reconstructed', 'inputs': inputs, 'tool_ids': list(tools)}

def input_record(identifier, role, parts, sources, transformation=None):
    result = {'id': identifier, 'kind': 'message', 'role': role, 'parts': parts,
              'source_events': [{'event_id': e} for e in sources]}
    if transformation:
        result['transformation'] = transformation
    return result

def session(slug, title, events, resources, *, contexts=(), tools=(), losses=(), requirements=()):
    events = copy.deepcopy(events)
    for index, entry in enumerate(events):
        entry['sequence'] = index
        entry['causes'] = [{'event_id': events[index-1]['id']}] if index else []
    head = events[-1]['id']
    coverage = []
    for scope in SCOPES:
        status, detail = 'not_inspected', 'Not modeled by this synthetic attachment example.'
        if scope in ['participants', 'conversation', 'branches', 'resources']:
            status, detail = 'complete', 'All declared records in this invented scenario are included.'
        if scope in ['decisions', 'tasks'] or (scope == 'tools' and not tools):
            status, detail = 'known_empty', 'No such activity is part of this invented scenario.'
        if scope == 'tools' and tools:
            status, detail = 'complete', 'The defined tool, call and terminal result are included.'
        if scope == 'contexts' and contexts:
            status, detail = 'partial', 'Illustrative reconstructed inputs; effective runtime configuration is not captured.'
        if scope == 'resources' and any(r['availability'] != 'embedded' for r in resources):
            status, detail = 'partial', 'References are represented; some original content is not embedded. See each resource and the losses.'
        coverage.append({'scope': scope, 'status': status, 'detail': detail})
    participants = [{'id': 'person', 'kind': 'human'}, {'id': 'agent', 'kind': 'agent'}]
    if tools:
        participants.append({'id': 'tool-runner', 'kind': 'tool'})
    return {'asif_version': '0.3',
            'capture': {'id': 'capture-' + slug, 'producer': {'name': 'asif-examples', 'version': '1'},
                        'consistency': 'consistent', 'boundary': 'Invented example through ' + head + '; no real model or tool ran.'},
            'session': {'id': 'session-' + slug, 'title': title, 'native_ids': [], 'lineage': []},
            'participants': participants, 'events': events,
            'branches': [{'id': 'main', 'event_ids': [e['id'] for e in events], 'head_event_id': head}],
            'executions': [], 'contexts': list(contexts), 'configurations': [], 'tools': list(tools),
            'resources': resources, 'environments': [],
            'checkpoints': [{'id': 'head', 'branch_id': 'main', 'at_event_id': head,
                             'knowledge': 'unknown', 'status': 'unknown',
                             'context_id': contexts[-1]['id'] if contexts else None, 'configuration_id': None,
                             'open_calls': [], 'open_decisions': [], 'tasks': [],
                             'requirements': [{'id': 'configuration', 'kind': 'asif.configuration',
                                               'description': 'Resolve effective configuration and destination capabilities.',
                                               'required_for': ['continue'], 'status': 'unresolved'}, *requirements]}],
            'coverage': coverage, 'losses': list(losses), 'required_features': []}

def save(slug, value):
    (ROOT / (slug + '.session.json')).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def png():
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    rows = b''.join(b'\0' + b''.join(bytes((240 if x < 8 else 40, 180 if y < 8 else 60, 90))
                                      for x in range(16)) for y in range(16))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 16, 16, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))

def pdf():
    stream = b'BT /F1 14 Tf 40 160 Td (Synthetic meeting notes) Tj 0 -24 Td (Decision: review the draft on Friday.) Tj ET\n'
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 400 220] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
               b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'endstream']
    out, offsets = b'%PDF-1.4\n', [0]
    for index, value in enumerate(objects, 1):
        offsets.append(len(out)); out += str(index).encode() + b' 0 obj\n' + value + b'\nendobj\n'
    start = len(out)
    out += b'xref\n0 6\n0000000000 65535 f \n'
    out += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    return out + f'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode()

# 1. Multiple attachments, extracted document text, and repeated image references.
image = resource('image', 'image/png', png(), storage='path', filename='color-grid.png')
document = resource('document', 'application/pdf', pdf(), storage='path', filename='meeting-notes.pdf')
extracted = resource('document-text', 'text/plain', 'Synthetic meeting notes\nDecision: review the draft on Friday.\n', purpose='derived_input')
extracted['provenance']['sources'] = [{'resource_id': 'document'}]
user_parts = [text('Review these two attachments.'), part('image', 'Synthetic 16 × 16 color grid.'), part('document', 'One-page invented meeting notes.')]
events = [message('e1', 'user', user_parts), message('e2', 'assistant', [text('The notes schedule a draft review on Friday. The image is a color grid.'), part('image', 'The same image, referenced again without another copy.')])]
ctx = context('request', 'e1', [input_record('i1', 'user', [text('Review these two attachments.'), part('image', 'Original image.'), part('document-text', 'Text extracted from the PDF.')], ['e1'], 'Use the recorded extracted-text resource for the PDF; preserve the original PDF separately.')])
save('image-and-document', session('image-and-document', 'Image and PDF attachments', events, [image, document, extracted], contexts=[ctx]))

# 2. Inline base64 media and a distinct textual annotation. Silence is not speech.
buffer = io.BytesIO()
with wave.open(buffer, 'wb') as audio:
    audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(8000); audio.writeframes(b'\0\0' * 800)
audio_resource = resource('audio', 'audio/wav', buffer.getvalue(), storage='data')
annotation = resource('transcript', 'text/plain', '[Synthetic fixture: 0.1 seconds of silence; no speech.]\n', purpose='derived_input')
annotation['provenance']['sources'] = [{'resource_id': 'audio'}]
events = [message('e1', 'user', [text('Does this sample contain speech?'), part('audio', 'Synthetic silent WAV fixture.')]), message('e2', 'assistant', [text('This fixture contains silence.'), part('transcript', 'Explicit annotation; not a transcript of invented speech.')])]
save('audio-and-transcript', session('audio-and-transcript', 'Inline audio and text annotation', events, [audio_resource, annotation]))

# 3. Input/output files and tool result correlation. These events are authored examples.
source = resource('source-csv', 'text/csv', 'item,count\napples,2\npears,3\n')
output = resource('output-csv', 'text/csv', 'item,count\napples,2\npears,3\nTOTAL,5\n', storage='path', filename='totals.csv', purpose='output')
report = resource('report', 'text/markdown', '# Inventory summary\n\nTotal items: **5**.\n', storage='path', filename='summary.md', purpose='output')
tool = {'id': 'summarize', 'name': 'example.inventory.summarize', 'description': 'Create a total and report from a CSV resource.',
        'input_schema': {'type': 'object', 'properties': {'resource_id': {'type': 'string'}}, 'required': ['resource_id'], 'additionalProperties': False}}
events = [message('e1', 'user', [text('Total this inventory and return the files.'), part('source-csv', 'Inline input CSV.')]),
          event('e2', 'agent', 'tool_call', {'call_id': 'call-1', 'tool_id': 'summarize', 'arguments': {'resource_id': 'source-csv'}, 'arguments_status': 'complete'}),
          event('e3', 'tool-runner', 'tool_result', {'call_id': 'call-1', 'result_index': 0, 'terminal': True, 'outcome': 'success', 'parts': [part('output-csv', 'CSV with total row.'), part('report', 'Markdown report.')]}),
          message('e4', 'assistant', [text('The total is 5.'), part('output-csv', 'Download the output CSV.'), part('report', 'Read the summary.')])]
save('tool-generated-files', session('tool-generated-files', 'Tool-generated CSV and report', events, [source, output, report], tools=[tool]))

# 4. Availability is explicit. A locator is not a fetch instruction.
resources = [
    {'id': 'missing', 'media_type': 'application/pdf', 'purpose': 'input', 'availability': 'unavailable', 'explanation': 'The transcript referenced a PDF whose bytes could not be recovered.'},
    {'id': 'external', 'media_type': 'video/mp4', 'purpose': 'input', 'availability': 'external', 'locator': 'https://media.example.invalid/recording.mp4', 'explanation': 'Location recorded only; no network access occurred.'},
    {'id': 'excluded', 'media_type': 'application/zip', 'purpose': 'input', 'availability': 'excluded', 'explanation': 'Intentionally omitted by the example export selection.'},
    {'id': 'unknown', 'media_type': 'image/png', 'purpose': 'input', 'availability': 'unknown', 'explanation': 'The exporter did not inspect attachment availability.'}]
events = [message('e1', 'user', [text('Review the referenced attachments.'), *[part(r['id'], r['explanation']) for r in resources]])]
requirements = [{'id': 'required-pdf', 'kind': 'asif.resource', 'resource_id': 'missing', 'description': 'The requested review needs the missing PDF.', 'required_for': ['continue'], 'status': 'unavailable'}]
losses = [{'id': 'missing-pdf', 'stage': 'capture', 'kind': 'unavailable', 'scope': 'resources', 'references': [{'type': 'resource', 'id': 'missing'}], 'explanation': resources[0]['explanation']},
          {'id': 'excluded-zip', 'stage': 'capture', 'kind': 'excluded', 'scope': 'resources', 'references': [{'type': 'resource', 'id': 'excluded'}], 'explanation': resources[2]['explanation']}]
save('attachment-availability', session('attachment-availability', 'Missing, external, excluded and uninspected attachments', events, resources, requirements=requirements, losses=losses))

# 5. Sanitized bytes have their own identity and digest; the original is not carried.
original = {'id': 'original', 'media_type': 'text/plain', 'purpose': 'input', 'availability': 'redacted', 'explanation': 'Original contact details intentionally not included in this fixture.'}
sanitized = resource('sanitized', 'text/plain', 'Contact: [REDACTED]\nRequest: review the draft.\n', purpose='derived_input')
events = [message('e1', 'user', [text('Review this request.'), part('original', 'Original withheld document.')]),
          event('e2', 'agent', 'note', {'category': 'redaction', 'parts': [text('A sanitized replacement is supplied.'), part('sanitized', 'Distinct replacement resource.')]}),
          message('e3', 'assistant', [text('The supplied request asks for a draft review. Contact details are redacted.')])]
ctx = context('sanitized-context', 'e2', [input_record('i1', 'user', [text('Review this request.'), part('sanitized', 'Sanitized content only.')], ['e1', 'e2'], 'Replace the unavailable original with the explicitly redacted derivative.')])
loss = {'id': 'redaction-1', 'stage': 'redaction', 'kind': 'redaction', 'scope': 'resources', 'references': [{'type': 'resource', 'id': 'original'}, {'type': 'resource', 'id': 'sanitized'}], 'explanation': 'Contact details removed; original bytes cannot be recovered from this example. The replacement hash covers only sanitized bytes.'}
save('redacted-attachment', session('redacted-attachment', 'Redacted original and separate sanitized replacement', events, [original, sanitized], contexts=[ctx], losses=[loss]))

# 6. A file retained in history does not automatically remain in active context.
notes = resource('notes', 'text/markdown', '# Project notes\n\n- Review: Friday\n- Output: a short summary\n', storage='path', filename='project-notes.md')
memory = resource('summary-memory', 'text/plain', 'Draft review is on Friday; the requested output is a short summary.\n', purpose='session_memory')
memory['provenance']['inputs'] = [{'event_id': 'e1'}, {'event_id': 'e2'}]
events = [message('e1', 'user', [text('Remember the decisions in these notes.'), part('notes', 'Original notes remain preserved.')]),
          message('e2', 'assistant', [text('The review is Friday and the deliverable is a short summary.')]),
          event('e3', 'agent', 'context_checkpoint', {'context_id': 'compacted', 'reason': 'compaction', 'replaced_context_id': 'before'})]
before = context('before', 'e1', [input_record('i1', 'user', events[0]['data']['parts'], ['e1'])])
after = context('compacted', 'e2', [input_record('i2', 'user', [text('Retained session summary:'), part('summary-memory', 'Explicit summary memory selected for continuation.')], ['e1', 'e2'], 'Summarize the prior exchange; omit the full notes from this selected context.')], purpose='continuation')
loss = {'id': 'context-compaction', 'stage': 'normalization', 'kind': 'summarization', 'scope': 'contexts', 'explanation': 'The compacted input loses original detail; history and original attachment remain preserved.'}
save('compaction-with-attachment', session('compaction-with-attachment', 'Preserved attachment and compacted working context', events, [notes, memory], contexts=[before, after], losses=[loss]))

print('Built six session examples and five deterministic file attachments.')
