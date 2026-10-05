/** Action-specific subjects and prerequisite closure; no runtime execution. */
import { type Obj, need, unique, own } from "./common.ts";

export function planRequirements(doc: Obj, plan: Obj, states: Obj): Obj[] {
  const p = doc.continuation,
    action = plan.next_action.kind;
  const agent = ["model_request", "resume_native"].includes(action);
  const active = agent || action === "reconcile_operation";
  const scopes = new Set([
    "read",
    ...(active ? ["continue"] : []),
    ...(agent ? ["context"] : []),
  ]);
  const cp = doc.checkpoints.find((x: Obj) => x.id === plan.checkpoint_id);
  const ctx = doc.contexts.find((x: Obj) => x.id === plan.context_id);
  const config = doc.configurations.find(
    (x: Obj) => x.id === plan.configuration_id,
  );
  const deps = unique(p.dependencies),
    workspaces = unique(p.workspaces);
  const environments = unique(doc.environments),
    resources = unique(doc.resources),
    tools = unique(doc.tools);
  const capabilities = unique(config.capabilities),
    handles = new Set(config.secret_requirements.map((x: Obj) => x.handle));
  const nodes = new Map<string, Obj>(),
    edges = new Map<string, string[]>(),
    envQueue: string[] = [],
    seenEnvs = new Set<string>();
  const node = (
    kind: string,
    id: string,
    required = false,
    owner?: string,
  ): string => {
    const key = JSON.stringify([kind, owner ?? null, id]);
    if (!nodes.has(key)) {
      const subject: Obj = { kind, id };
      if (owner !== undefined) subject.owner_id = owner;
      nodes.set(key, { subject, required: false });
      edges.set(key, []);
    }
    nodes.get(key)!.required ||= required;
    return key;
  };
  const link = (parent: string, child: string) => {
    edges.get(parent)!.push(child);
  };
  const resource = (parent: string, id: string) => {
    need(own(resources, id), "missing assessed resource");
    link(parent, node("resource", id));
  };
  const parts = (parent: string, values: Obj[]) => {
    for (const value of values)
      if (["resource", "opaque"].includes(value.kind))
        resource(parent, value.resource_id);
  };
  const environment = (id: string, required = false) => {
    need(own(environments, id), "missing requirement environment");
    if (!seenEnvs.has(id)) {
      seenEnvs.add(id);
      envQueue.push(id);
    }
    return node("environment", id, required);
  };
  const requirements = (
    parent: string,
    values: Obj[],
    kind: string,
    owner: string,
  ) => {
    unique(values);
    for (const value of values) {
      const key = node(kind, value.id, false, owner);
      if (value.required_for.some((s: string) => scopes.has(s)))
        link(parent, key);
      if (own(value, "resource_id")) resource(key, value.resource_id);
      if (own(value, "capability_id")) {
        need(
          own(capabilities, value.capability_id),
          "missing requirement capability",
        );
        link(key, node("capability", value.capability_id, false, config.id));
      }
      if (own(value, "environment_id"))
        link(key, environment(value.environment_id));
      if (own(value, "secret_handle"))
        need(handles.has(value.secret_handle), "undeclared requirement secret");
    }
  };
  const root = node("plan", plan.id, true),
    context = node("context", ctx.id, agent);
  node("model", plan.id, agent);
  node("configuration", config.id, true);
  for (const feature of doc.required_features) node("feature", feature, true);
  for (const id of plan.boundary.evidence_resource_ids) resource(root, id);
  for (const item of ctx.inputs) parts(context, item.parts);
  for (const id of ctx.tool_ids)
    for (const rid of tools[id].resource_ids ?? []) resource(context, rid);
  for (const instruction of config.instructions)
    parts(
      node("instruction", instruction.id, agent, config.id),
      instruction.parts,
    );
  for (const capability of config.capabilities) {
    const key = node(
      "capability",
      capability.id,
      agent && capability.required,
      config.id,
    );
    for (const id of capability.resource_ids) resource(key, id);
  }
  for (const policy of config.policies)
    node("policy", policy.id, policy.enforcing, config.id);
  for (const id of config.environment_ids ?? []) environment(id, active);
  for (const id of plan.dependency_ids) {
    const d = deps[id],
      key = node(
        "dependency",
        id,
        d.required_for.some((s: string) => scopes.has(s)),
      );
    for (const other of d.depends_on) link(key, node("dependency", other));
    for (const rid of d.resource_ids) resource(key, rid);
  }
  for (const id of plan.workspace_ids) {
    let w: Obj | null = workspaces[id];
    const key = node("workspace", id, active);
    link(key, environment(w!.environment_id));
    for (const entry of Object.values<Obj>(states[id]))
      if (entry.kind === "file") resource(key, entry.resource_id);
    while (w !== null) {
      if (w.git) {
        const git = w.git;
        for (const rid of git.bundle_resource_ids) resource(key, rid);
        for (const entry of [...git.index_entries, ...git.prerequisites])
          if (entry.resource_id) resource(key, entry.resource_id);
        for (const dep of [
          ...git.lfs_dependency_ids,
          ...git.submodules.map((x: Obj) => x.dependency_id),
        ]) {
          need(plan.dependency_ids.includes(dep), "unselected Git dependency");
          link(key, node("dependency", dep));
        }
      }
      w = w.base_snapshot_id !== null ? workspaces[w.base_snapshot_id] : null;
    }
  }
  for (const service of p.service_bindings)
    if (plan.service_binding_ids.includes(service.id)) {
      const key = node("service", service.id, active);
      for (const dep of service.dependency_ids)
        link(key, node("dependency", dep));
    }
  for (const operation of p.operations)
    if (plan.operation_ids.includes(operation.id)) {
      const selected =
        agent ||
        (action === "reconcile_operation" &&
          operation.id === plan.next_action.operation_id);
      const key = node("operation", operation.id, selected),
        handler = operation.recovery.handler_dependency_id;
      if (handler !== null) link(key, node("dependency", handler));
      for (const rid of [
        ...operation.evidence_resource_ids,
        ...operation.recovery.evidence_resource_ids,
      ])
        resource(key, rid);
    }
  if (plan.native_import_id !== null) {
    const native = p.native_imports.find(
        (x: Obj) => x.id === plan.native_import_id,
      ),
      key = node("native_import", native.id, agent);
    for (const id of native.resource_ids) resource(key, id);
  }
  if (action === "await_decision") {
    const request =
      doc.events.find(
        (e: Obj) =>
          e.kind === "decision_request" &&
          e.data.request_id === plan.next_action.request_id,
      )?.data ??
      (doc.external_bindings ?? []).find(
        (b: Obj) =>
          b.kind === "request" && b.id === plan.next_action.request_id,
      ).descriptor;
    parts(root, request.prompt);
  }
  requirements(root, cp.requirements, "checkpoint_requirement", cp.id);
  for (const id of envQueue) {
    const env = environments[id],
      key = node("environment", id);
    for (const rid of env.resource_ids) resource(key, rid);
    requirements(key, env.requirements, "environment_requirement", id);
  }
  const pending = [...nodes.keys()].filter((key) => nodes.get(key)!.required);
  while (pending.length)
    for (const child of edges.get(pending.pop()!)!)
      if (!nodes.get(child)!.required) {
        nodes.get(child)!.required = true;
        pending.push(child);
      }
  return [...nodes.values()];
}
