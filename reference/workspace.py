"""Vendor-neutral selected-tree restoration into a fresh destination."""
import fnmatch
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import unicodedata
from .common import Invalid, Unsupported, need, relative, unique, acyclic


def workspace_states(profile):
    records=unique(profile['workspaces']);edges={id:[w['base_snapshot_id']] if w['base_snapshot_id'] else [] for id,w in records.items()}
    acyclic(edges,'workspace base');result={};remaining=set(records)
    while remaining:
        ready=[id for id in remaining if not edges[id] or edges[id][0] in result]
        for id in ready:
            w=records[id];base=w['base_snapshot_id'];entries=dict(result[base]) if base else {}
            if base:need(records[base]['root_id']==w['root_id'],'workspace base root mismatch')
            for deletion in w['deletions']:
                relative(deletion)
                targets=[p for p in entries if p==deletion or p.startswith(deletion+'/')]
                need(not any(fnmatch.fnmatchcase(target,p) or target==p.rstrip('/') or target.startswith(p.rstrip('/')+'/') for target in [deletion,*targets] for p in w['selection']['exclude']),'deleting excluded path')
                need(targets,'deletion absent from base')
                for p in targets:del entries[p]
            for entry in w['entries']:
                relative(entry['path']);entries[entry['path']]=entry
            for path,entry in entries.items():
                parts=path.split('/')
                for index in range(1,len(parts)):
                    parent='/'.join(parts[:index])
                    need(parent not in entries or entries[parent]['kind']=='directory','workspace file/directory collision')
            result[id]=entries;remaining.remove(id)
    return result


def check_git(workspace,resources,dependencies):
    if 'git' not in workspace:return
    g=workspace['git'];need(g['object_format'] in ('sha1','sha256'),'unsupported Git object format')
    length=40 if g['object_format']=='sha1' else 64
    def oid(value):
        if value is not None:need(len(value)==length and all(c in '0123456789abcdef' for c in value),'invalid Git object ID')
    oid(g['head']);paths={}
    for entry in g['index_entries']:
        relative(entry['path']);oid(entry['object_id']);stages=paths.setdefault(entry['path'],set())
        need(entry['stage'] not in stages,'duplicate Git index stage');stages.add(entry['stage'])
        need(not (0 in stages and len(stages)>1),'mixed resolved/unmerged Git index')
        need(entry['mode'] in ('100644','100755','120000','160000'),'unsupported Git index mode')
        need(entry['resource_id'] is not None or entry['object_id'] is not None,'Git index entry has no content')
        if entry['resource_id']:
            resources.ref(entry['resource_id'])
            if entry['resource_id'] in resources.cache and entry['object_id']:
                raw=resources.bytes(entry['resource_id']);git_bytes=b'blob '+str(len(raw)).encode()+b'\0'+raw
                digest=hashlib.new(g['object_format'],git_bytes).hexdigest();need(digest==entry['object_id'],'Git index blob mismatch')
    for prerequisite in g['prerequisites']:
        oid(prerequisite['object_id'])
        if prerequisite['availability']=='embedded':need('resource_id' in prerequisite,'embedded Git prerequisite missing resource')
        if 'resource_id' in prerequisite:resources.ref(prerequisite['resource_id'])
    for submodule in g['submodules']:relative(submodule['path']);oid(submodule['object_id']);need(submodule['dependency_id'] in dependencies,'missing submodule dependency')
    need(set(g['lfs_dependency_ids'])<=dependencies.keys(),'missing LFS dependency')


def validate_destination_paths(entries,*,case_sensitive=True,normalization='none'):
    """Check the selected tree under the destination's path equivalence rules."""
    need(normalization in ('none','NFC','NFD'),'unsupported normalization')
    seen={}
    for path,entry in entries.items():
        folded=unicodedata.normalize(normalization,path) if normalization!='none' else path
        if not case_sensitive:folded=folded.casefold()
        need(folded not in seen,'destination path collision');seen[folded]=entry['kind']
    for path in seen:
        pieces=path.split('/')
        for i in range(1,len(pieces)):need(seen.get('/'.join(pieces[:i]),'directory')=='directory','destination prefix collision')


def restore(document,validated,workspace_id,destination,*,case_sensitive=True,normalization='none',fail_after=None):
    profile=document['continuation'];records=unique(profile['workspaces']);need(workspace_id in records,'unknown workspace')
    w=records[workspace_id];states=workspace_states(profile);entries=states[workspace_id];resources=validated['resources']
    # Refuse unsupported restoration semantics explicitly, even if a profile can describe them.
    chain=[];current=w
    while True:
        chain.append(current)
        if not current['base_snapshot_id']:break
        current=records[current['base_snapshot_id']]
    if any(x['mode']=='refs' or 'git' in x for x in chain):raise Unsupported('Git administration/index restoration is not implemented; use a verified Git adapter')
    need(all(x['selection']['complete_for_selection'] for x in chain),'incomplete selected-tree snapshot')
    validate_destination_paths(entries,case_sensitive=case_sensitive,normalization=normalization)
    for path,entry in entries.items():
        if entry['kind']=='symlink':raise Unsupported('workspace symlink restoration requires an explicit link policy')
        relative(path);need('.git' not in [p.casefold() for p in path.split('/')],'workspace cannot inject Git administrative files')
        if entry['kind']=='file':resources.bytes(entry['resource_id'])
    destination=Path(destination);need(not os.path.lexists(destination),'destination already exists')
    parent=destination.parent;need(parent.is_dir() and not parent.is_symlink(),'destination parent must be a controlled directory')
    # This lock coordinates this implementation's writers. The parent must not be
    # concurrently modified by uncooperating processes; this is documented, not hidden.
    lock=parent/('.'+destination.name+'.asif-lock')
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
    staging=None;published=False
    try:
        need(not os.path.lexists(destination),'destination appeared before staging')
        staging=Path(tempfile.mkdtemp(prefix='.'+destination.name+'.asif-stage-',dir=parent))
        count=0
        for path,entry in sorted(entries.items(),key=lambda item:(item[0].count('/'),item[0])):
            target=staging/path;target.parent.mkdir(parents=True,exist_ok=True)
            if entry['kind']=='directory':target.mkdir(exist_ok=True)
            else:
                with target.open('xb') as stream:stream.write(resources.bytes(entry['resource_id']));stream.flush();os.fsync(stream.fileno())
                target.chmod(entry['mode'])
            count+=1
            if fail_after is not None and count>=fail_after:raise Invalid('injected staging failure')
        # Apply restrictive directory modes after populating descendants.
        for path,entry in sorted(entries.items(),key=lambda item:item[0].count('/'),reverse=True):
            if entry['kind']=='directory':(staging/path).chmod(entry['mode'])
        need(not os.path.lexists(destination),'destination appeared before publication')
        staging.rename(destination);published=True
        return {'status':'restored','workspace_id':workspace_id,'entries':len(entries),'destination':str(destination),'scope':'selected file tree; no native agent import'}
    finally:
        if staging is not None and not published:
            # Undo modes we set so cleanup can remove our own staging tree.
            for root,dirs,files in os.walk(staging,topdown=True):
                os.chmod(root,0o700)
                for name in dirs:os.chmod(Path(root)/name,0o700)
            shutil.rmtree(staging,ignore_errors=True)
        lock.unlink()
