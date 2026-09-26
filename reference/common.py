"""Bounded parsing and resource access shared by the reference tools."""
import base64
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import stat

MAX_DOCUMENT=16*1024*1024
MAX_RESOURCE=64*1024*1024
MAX_TOTAL=256*1024*1024
MAX_RECORDS=20000
MAX_DEPTH=128
class Invalid(ValueError):pass
class Unsupported(Invalid):pass

def need(condition,message):
    if not condition:raise Invalid(message)

def pairs(items):
    out={}
    for key,value in items:
        need(key not in out,'duplicate JSON key');out[key]=value
    return out

def reject(value):raise Invalid('non-JSON numeric constant')

def decode(raw):
    need(len(raw)<=MAX_DOCUMENT,'document byte limit')
    try:doc=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_float=Decimal,parse_constant=reject)
    except (ValueError,UnicodeError,RecursionError) as exc:raise Invalid('invalid JSON: '+str(exc)) from exc
    stack=[(doc,0)];count=0
    while stack:
        value,depth=stack.pop();count+=1
        need(depth<=MAX_DEPTH,'JSON nesting limit');need(count<=MAX_RECORDS*100,'JSON node limit')
        if isinstance(value,dict):stack.extend((child,depth+1) for child in value.values())
        elif isinstance(value,list):stack.extend((child,depth+1) for child in value)
    return doc

def read(path,limit=MAX_DOCUMENT):
    path=Path(path);need(not path.is_symlink(),'symlink input')
    st=path.stat();need(stat.S_ISREG(st.st_mode),'nonregular input');need(st.st_size<=limit,'input byte limit')
    with path.open('rb') as f:raw=f.read(limit+1)
    need(len(raw)<=limit,'input byte limit');return raw

def load(path):
    raw=read(path);return decode(raw),raw

def encode(value):
    """Serialize JSON values without rounding parsed decimal extensions."""
    def render(item):
        if isinstance(item,Decimal):
            need(item.is_finite(),'nonfinite JSON number');return str(item)
        if isinstance(item,dict):return '{'+','.join(json.dumps(k,ensure_ascii=False)+':'+render(v) for k,v in item.items())+'}'
        if isinstance(item,list):return '['+','.join(render(v) for v in item)+']'
        return json.dumps(item,ensure_ascii=False,allow_nan=False)
    return (render(value)+'\n').encode('utf8')

def relative(name,empty=False):
    need(isinstance(name,str) and (empty or bool(name)),'empty path')
    if name=='':return
    need(len(name)<=4096 and '\\' not in name and ':' not in name and not name.startswith('/'),'unsafe path')
    for part in name.split('/'):
        need(part not in ('','.','..') and not part.endswith((' ','.')),'unsafe path')
        need(not any(ord(c)<32 or c in '<>"|?*' for c in part),'nonportable path')
        need(not re.match(r'^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)',part,re.I),'reserved device path')

def contained(folder,name):
    relative(name);folder=Path(folder);current=folder
    need(not folder.is_symlink(),'symlink root')
    for part in name.split('/'):
        current=current/part;need(not current.is_symlink(),'symlink resource')
    need(current.resolve().is_relative_to(folder.resolve()),'escaping resource');return current

def unique(items,key='id'):
    need(len(items)<=MAX_RECORDS,'record count limit');out={}
    for item in items:
        need(item[key] not in out,'duplicate '+key);out[item[key]]=item
    return out

def pointer(value,selector):
    if selector=='':return value
    need(isinstance(selector,str) and selector.startswith('/'),'invalid JSON pointer')
    for component in selector[1:].split('/'):
        need(re.search(r'~(?![01])',component) is None,'invalid pointer escape')
        component=component.replace('~1','/').replace('~0','~')
        try:
            if isinstance(value,list):
                need(re.fullmatch(r'0|[1-9][0-9]*',component) is not None,'invalid array selector')
                value=value[int(component)]
            else:value=value[component]
        except (KeyError,IndexError,TypeError):raise Invalid('pointer target missing')
    return value

def acyclic(edges,label):
    parents={key:set(values) for key,values in edges.items()};children={key:[] for key in parents}
    for key,values in parents.items():
        need(values<=parents.keys(),'missing '+label+' reference')
        for value in values:children[value].append(key)
    ready=[key for key,values in parents.items() if not values];seen=0
    while ready:
        key=ready.pop();seen+=1
        for child in children[key]:
            parents[child].remove(key)
            if not parents[child]:ready.append(child)
    need(seen==len(parents),label+' cycle')

class Resources:
    def __init__(self,document,folder):
        self.records=unique(document['resources']);self.folder=Path(folder);self.cache={};total=0;paths={}
        for id,r in self.records.items():
            if r['availability']!='embedded':continue
            if 'text' in r:raw=r['text'].encode('utf-8')
            elif 'data' in r:
                need(len(r['data'])<=((MAX_RESOURCE+2)//3)*4,'base64 byte limit')
                try:raw=base64.b64decode(r['data'],validate=True)
                except ValueError as exc:raise Invalid('invalid base64') from exc
            else:
                file=contained(self.folder,r['path']);raw=read(file,MAX_RESOURCE)
                folded=r['path'].casefold();need(folded not in paths or paths[folded]==r['path'],'resource path collision');paths[folded]=r['path']
            need(len(raw)<=MAX_RESOURCE,'resource byte limit');total+=len(raw);need(total<=MAX_TOTAL,'resource total limit')
            need(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'resource integrity')
            self.cache[id]=raw
    def ref(self,id):need(id in self.records,'missing resource reference')
    def bytes(self,id):
        self.ref(id);need(id in self.cache,'resource bytes unavailable');return self.cache[id]
