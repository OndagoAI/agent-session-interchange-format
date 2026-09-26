"""Exact-pattern audit over captured raw and decoded content; no secret discovery claim."""
import base64
from .common import need, decode, MAX_RESOURCE

def audit(raw,validated,patterns):
    need(patterns and all(isinstance(x,str) and x for x in patterns),'nonempty redaction patterns required')
    needles=[x.encode('utf8') for x in patterns];findings=[]
    def inspect(content,where):
        hits=[i for i,n in enumerate(needles) if n in content]
        if hits:findings.append({'location':where,'pattern_indexes':hits})
    inspect(raw,'document/raw')
    stack=[(decode(raw),'document')]
    while stack:
        value,where=stack.pop()
        if isinstance(value,dict):
            for index,(key,child) in enumerate(value.items()):inspect(key.encode('utf8'),where+'/key-index/'+str(index));stack.append((child,where+'/value-index/'+str(index)))
        elif isinstance(value,list):stack.extend((child,where+'/'+str(i)) for i,child in enumerate(value))
        elif isinstance(value,str):
            inspect(value.encode('utf8'),where)
            if len(value)<=((MAX_RESOURCE+2)//3)*4:
                try:decoded=base64.b64decode(value,validate=True)
                except ValueError:continue
                inspect(decoded,where+'/base64')
    for index,content in enumerate(validated['resources'].cache.values()):inspect(content,'resource-index/'+str(index))
    return {'status':'matches_found' if findings else 'no_exact_matches','findings':findings,'scope':'supplied patterns in raw/decoded JSON and available resource bytes; no discovery, compressed-media or OCR claim'}
