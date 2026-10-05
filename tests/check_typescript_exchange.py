"""Exercise both local CLIs and verify newly written packages/signatures in both directions.
Requires Node 24+ on PATH or an explicit ASIF_NODE executable. Not independent evidence.
"""
import json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];node=os.environ.get('ASIF_NODE','node');results=[]
def invoke(language,*args,expected=0):
 command=[sys.executable,str(ROOT/'asif.py')] if language=='python' else [node,str(ROOT/'asif.ts')]
 p=subprocess.run(command+[str(a) for a in args],cwd=ROOT,capture_output=True,text=True)
 assert p.returncode==expected,(language,args,p.returncode,p.stdout,p.stderr)
 return json.loads(p.stdout)
def compare(name,*args,expected=0):
 a=invoke('python',*args,expected=expected);b=invoke('typescript',*args,expected=expected);assert a==b,(name,a,b);results.append({'case':name,'passed':True})
source=ROOT/'examples/continuation/another-computer.session.json';doc=json.loads(source.read_text())
compare('validate','validate',source)
compare('request','request',source,doc['contexts'][0]['id'])
compare('report','validate-report',source,source.with_name('another-computer.report.json'),'--at','2026-09-26T12:30:00Z')
with tempfile.TemporaryDirectory() as tmp:
 tmp=Path(tmp);private=tmp/'private.key';private.write_bytes(bytes(range(32)));public=ROOT/'examples/package-test-public.key'
 image=ROOT/'examples/image-and-document.session.json'
 for producer,consumer in [('python','typescript'),('typescript','python')]:
  archive=tmp/(producer+'.zip');sig=tmp/(producer+'.sig.json')
  invoke(producer,'pack',image,archive);invoke(producer,'sign',archive,'--private-key',private,'--output',sig)
  assert invoke(consumer,'verify-package',archive)['status']=='integrity_verified'
  assert invoke(consumer,'verify-signature',archive,'--signature',sig,'--trusted-public-key',public)['status']=='verified'
  results.append({'case':producer+'-to-'+consumer+'-package-and-signature','passed':True})
 assert (tmp/'python.zip').read_bytes()==(tmp/'typescript.zip').read_bytes()
 assert (tmp/'python.sig.json').read_bytes()==(tmp/'typescript.sig.json').read_bytes()
 results.append({'case':'identical-package-and-signature-bytes','passed':True})
 for language in ['python','typescript']:invoke(language,'restore-workspace',source,doc['continuation']['workspaces'][0]['id'],tmp/language)
 for entry in doc['continuation']['workspaces'][0]['entries']:
  if entry['kind']=='file':assert (tmp/'python'/entry['path']).read_bytes()==(tmp/'typescript'/entry['path']).read_bytes()
 results.append({'case':'restored-file-bytes','passed':True})
 patterns=tmp/'patterns.json';patterns.write_text(json.dumps(['asif_version']))
 compare('redaction-result','audit-redaction',source,'--patterns',patterns,expected=1)
 bad=tmp/'bad.json';bad.write_text('{"a":1,"a":2}')
 compare('invalid-json-exit-2','validate',bad,expected=2)
 # A valid core document with an unsupported required feature remains inspectable.
 value=json.loads((ROOT/'examples/awaiting-approval.session.json').read_text());value['required_features']=['example.unknown/1'];unknown=tmp/'unknown.json';unknown.write_text(json.dumps(value))
 compare('unsupported-feature-exit-3','validate',unknown,expected=3)
result={'asif_version':'0.4','scope':'Python/TypeScript CLI and package exchange, shared authorship','checks':len(results),'passed':len(results),'independent_implementations':0,'real_runtime_tests':0,'results':results}
(ROOT/'tests/typescript-exchange-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
