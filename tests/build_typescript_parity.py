"""Export the existing Python continuation checks as a reusable TypeScript parity corpus.
Python is needed to refresh expected results, not to run the TypeScript CLI or tests.
"""
import base64,copy,inspect,json,runpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
import continuation_checks
from reference.common import encode,Invalid,Unsupported
from jsonschema.exceptions import ValidationError
cases=[]
def wrap(kind,original):
 def invoke(*args,**kwargs):
  name=next((f.frame.f_locals['name'] for f in inspect.stack() if f.function in ('negative_source','negative_report')),kind+'-'+str(len(cases)+1))
  case={'name':name,'kind':kind,'document':copy.deepcopy(args[0]),'folder':'examples/continuation'}
  if kind=='report':case.update(raw=base64.b64encode(args[1]).decode(),report=copy.deepcopy(args[2]),now=kwargs['now'].isoformat())
  if kwargs.get('current_snapshot') is not None:case['current_snapshot']=base64.b64encode(kwargs['current_snapshot']).decode()
  try:result=original(*args,**kwargs)
  except (Invalid,ValidationError) as exc:
   case['expected']={'accepted':False,'schema_error':isinstance(exc,ValidationError),'unsupported':isinstance(exc,Unsupported)};cases.append(case);raise
  else:
   case['expected']={'accepted':True,'result':copy.deepcopy(result)};cases.append(case);return result
 return invoke
continuation_checks.inspect_session=wrap('session',continuation_checks.inspect_session)
continuation_checks.inspect_report=wrap('report',continuation_checks.inspect_report)
runpy.run_path(str(ROOT/'tests/check_continuation.py'))
(ROOT/'tests/typescript-parity-cases.json').write_bytes(encode({'asif_version':'0.3','source':'tests/check_continuation.py','independent_implementations':0,'cases':cases}))
print('Exported',len(cases),'Python continuation outcomes for TypeScript parity checks.')
