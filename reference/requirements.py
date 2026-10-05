"""Deterministic assessment subjects and action-specific prerequisite closure."""
from .common import need, unique


def plan_requirements(doc, plan, states):
    p=doc['continuation'];action=plan['next_action']['kind']
    agent=action in ('model_request','resume_native')
    active=agent or action=='reconcile_operation'
    scopes={'read'} | ({'continue'} if active else set()) | ({'context'} if agent else set())
    cp=next(x for x in doc['checkpoints'] if x['id']==plan['checkpoint_id'])
    ctx=next(x for x in doc['contexts'] if x['id']==plan['context_id'])
    config=next(x for x in doc['configurations'] if x['id']==plan['configuration_id'])
    deps=unique(p['dependencies']);workspaces=unique(p['workspaces'])
    environments=unique(doc['environments']);resources=unique(doc['resources']);tools=unique(doc['tools'])
    capabilities=unique(config['capabilities']);handles={x['handle'] for x in config['secret_requirements']}
    nodes={};edges={};env_queue=[];seen_envs=set()

    def node(kind,id,required=False,owner=None):
        key=(kind,owner,id)
        if key not in nodes:
            subject={'kind':kind,'id':id}
            if owner is not None:subject['owner_id']=owner
            nodes[key]={'subject':subject,'required':False};edges[key]=[]
        nodes[key]['required'] |= required
        return key

    def link(parent,child):edges[parent].append(child)
    def resource(parent,id):
        need(id in resources,'missing assessed resource');link(parent,node('resource',id))
    def parts(parent,values):
        for value in values:
            if value['kind'] in ('resource','opaque'):resource(parent,value['resource_id'])
    def environment(id,required=False):
        need(id in environments,'missing requirement environment')
        if id not in seen_envs:seen_envs.add(id);env_queue.append(id)
        return node('environment',id,required)
    def requirements(parent,values,kind,owner):
        unique(values)
        for value in values:
            key=node(kind,value['id'],owner=owner)
            if scopes.intersection(value['required_for']):link(parent,key)
            if 'resource_id' in value:resource(key,value['resource_id'])
            if 'capability_id' in value:
                need(value['capability_id'] in capabilities,'missing requirement capability')
                link(key,node('capability',value['capability_id'],owner=config['id']))
            if 'environment_id' in value:link(key,environment(value['environment_id']))
            if 'secret_handle' in value:need(value['secret_handle'] in handles,'undeclared requirement secret')

    root=node('plan',plan['id'],True)
    context=node('context',ctx['id'],agent)
    node('model',plan['id'],agent);node('configuration',config['id'],True)
    for feature in doc['required_features']:node('feature',feature,True)
    for id in plan['boundary']['evidence_resource_ids']:resource(root,id)
    for item in ctx['inputs']:parts(context,item['parts'])
    for id in ctx['tool_ids']:
        for rid in tools[id].get('resource_ids',[]):resource(context,rid)
    for instruction in config['instructions']:
        key=node('instruction',instruction['id'],agent,config['id']);parts(key,instruction['parts'])
    for capability in config['capabilities']:
        key=node('capability',capability['id'],agent and capability['required'],config['id'])
        for id in capability['resource_ids']:resource(key,id)
    for policy in config['policies']:node('policy',policy['id'],policy['enforcing'],config['id'])
    for id in config.get('environment_ids',[]):environment(id,active)
    for id in plan['dependency_ids']:
        d=deps[id];key=node('dependency',id,bool(scopes.intersection(d['required_for'])))
        for other in d['depends_on']:link(key,node('dependency',other))
        for rid in d['resource_ids']:resource(key,rid)
    for id in plan['workspace_ids']:
        w=workspaces[id];key=node('workspace',id,active)
        link(key,environment(w['environment_id']))
        for entry in states[id].values():
            if entry['kind']=='file':resource(key,entry['resource_id'])
        # Base Git prerequisites are inherited even when no current file uses them.
        while w is not None:
            if 'git' in w:
                git=w['git']
                for rid in git['bundle_resource_ids']:resource(key,rid)
                for entry in git['index_entries']+git['prerequisites']:
                    if entry.get('resource_id'):resource(key,entry['resource_id'])
                for dep in git['lfs_dependency_ids']+[x['dependency_id'] for x in git['submodules']]:
                    need(dep in plan['dependency_ids'],'unselected Git dependency')
                    link(key,node('dependency',dep))
            w=workspaces[w['base_snapshot_id']] if w['base_snapshot_id'] is not None else None
    for service in p['service_bindings']:
        if service['id'] in plan['service_binding_ids']:
            key=node('service',service['id'],active)
            for dep in service['dependency_ids']:link(key,node('dependency',dep))
    for operation in p['operations']:
        if operation['id'] in plan['operation_ids']:
            selected=agent or action=='reconcile_operation' and operation['id']==plan['next_action']['operation_id']
            key=node('operation',operation['id'],selected)
            handler=operation['recovery']['handler_dependency_id']
            if handler is not None:link(key,node('dependency',handler))
            for rid in operation['evidence_resource_ids']+operation['recovery']['evidence_resource_ids']:resource(key,rid)
    if plan['native_import_id'] is not None:
        native=next(x for x in p['native_imports'] if x['id']==plan['native_import_id'])
        key=node('native_import',native['id'],agent)
        for id in native['resource_ids']:resource(key,id)
    if action=='await_decision':
        request=next((e['data'] for e in doc['events'] if e['kind']=='decision_request' and e['data']['request_id']==plan['next_action']['request_id']),None)
        if request is None:request=next(b['descriptor'] for b in doc.get('external_bindings',[]) if b['kind']=='request' and b['id']==plan['next_action']['request_id'])
        parts(root,request['prompt'])
    requirements(root,cp['requirements'],'checkpoint_requirement',cp['id'])
    for id in env_queue:
        env=environments[id];key=node('environment',id)
        for rid in env['resource_ids']:resource(key,rid)
        requirements(key,env['requirements'],'environment_requirement',id)
    pending=[key for key,value in nodes.items() if value['required']]
    while pending:
        for child in edges[pending.pop()]:
            if not nodes[child]['required']:nodes[child]['required']=True;pending.append(child)
    return list(nodes.values())
