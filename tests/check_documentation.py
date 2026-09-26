"""Check object coverage, every reference example, generated tables and local navigation."""
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'docs'))
from build_reference import OBJECTS,validator,FILES,anchor
samples=json.loads((ROOT/'docs/object-examples.json').read_text());variants=json.loads((ROOT/'docs/object-variants.json').read_text())
index=json.loads((ROOT/'docs/object-index.json').read_text())
assert {(x['schema'].removesuffix('.schema.json'),x['pointer']) for x in index}==set(OBJECTS),'Undocumented schema object'
assert len(samples)==len(OBJECTS),'Missing or orphaned primary object example'
count=0
for (name,path),schema in OBJECTS.items():
 key=name+':'+path;validator(name,path).validate(samples[key]);count+=1
 for extra in variants.get(key,[]):validator(name,path).validate(extra['value']);count+=1
 page=(ROOT/'docs'/FILES[name]).read_text()
 for field in schema.get('properties',{}):assert 'id="'+anchor(name,path)+'-'+field+'"' in page,(key,field)
subprocess.run([sys.executable,str(ROOT/'docs/build_reference.py'),'--check'],check=True,capture_output=True)
# Ensure the root example also has valid references and resource semantics.
sys.path.insert(0,str(ROOT))
from reference.core import validate_document
validate_document(samples['session:'],ROOT/'examples')
files=[p for p in ROOT.rglob('*.md') if not any(x in p.parts for x in ('.venv','node_modules','__pycache__'))]
def anchors(text):
 text=re.sub(r'```.*?```','',text,flags=re.S)
 out=set(re.findall(r'<a\s+id="([^"]+)"',text));seen={}
 for heading in re.findall(r'^#{1,6}\s+(.+)$',text,re.M):
  value=re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-')
  n=seen.get(value,0);seen[value]=n+1;out.add(value+('-'+str(n) if n else ''))
 return out
links=0;errors=[]
for file in files:
 for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
  if target.startswith(('https:','http:','mailto:')):continue
  path,_,fragment=target.partition('#');destination=(file.parent/path).resolve() if path else file
  links+=1
  if not destination.exists():errors.append((str(file.relative_to(ROOT)),target,'missing file'))
  elif fragment and destination.suffix=='.md' and fragment not in anchors(destination.read_text()):errors.append((str(file.relative_to(ROOT)),target,'missing anchor'))
assert not errors,json.dumps(errors,indent=2)
result={'asif_version':'0.3','scope':'Object reference schema coverage, examples, generated-field freshness and local Markdown links','objects':len(OBJECTS),'validated_examples':count,'local_links':links,'passed':True}
(ROOT/'tests/documentation-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
