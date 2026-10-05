/** A direct port of the Python reference's selected continuation invariants. */
import {
  type Obj,
  need,
  own,
  unique,
  relative,
  pointer,
  Invalid,
  object,
  subset,
  setEqual,
  equal,
  hash,
  casefold,
} from "./common.ts";
import { validateDocument, shape, SUPPORTED, type Validated } from "./core.ts";
import { planRequirements } from "./requirements.ts";
import { workspaceStates, checkGit } from "./workspace.ts";
const FEATURE = "asif.portable-continuation/0.1";
export const subject = (kind: string, id: string, owner?: string): Obj =>
  owner === undefined ? { kind, id } : { kind, id, owner_id: owner };
const key = (s: Obj): string =>
  JSON.stringify([s.kind, s.owner_id ?? null, s.id]);
export function date(value: string): number {
  need(
    typeof value === "string" && /(Z|[+-]\d\d:\d\d)$/.test(value),
    "time needs timezone",
  );
  const out = Date.parse(value);
  need(Number.isFinite(out), "invalid assessment time");
  return out;
}
export function inspectSession(
  doc: Obj,
  folder: string,
  validated?: Validated,
): Obj {
  const v = validated ?? validateDocument(doc, folder);
  need(own(doc, "continuation"), "continuation profile absent");
  const p = doc.continuation,
    core = v.collections,
    resources = core.resources;
  for (const name of [
    "workspaces",
    "dependencies",
    "service_bindings",
    "operations",
    "native_imports",
    "plans",
  ])
    unique(p[name]);
  const deps = unique(p.dependencies),
    workspaces = unique(p.workspaces),
    operations = unique(p.operations),
    bindings = unique(p.configuration_bindings, "configuration_id"),
    services = unique(p.service_bindings),
    native = unique(p.native_imports),
    states = workspaceStates(p);
  const pending = new Set(Object.keys(deps));
  while (pending.size) {
    const roots = [...pending].filter(
      (id) => !deps[id].depends_on.some((x: string) => pending.has(x)),
    );
    need(roots.length, "dependency cycle");
    for (const id of roots) pending.delete(id);
  }
  for (const d of Object.values<Obj>(deps)) {
    need(subset(d.depends_on, Object.keys(deps)), "missing dependency");
    need(
      subset(d.resource_ids, Object.keys(resources)),
      "missing dependency resource",
    );
    if (d.kind === "tool")
      need(own(core.tools, d.tool_id), "missing dependency tool");
  }
  for (const w of Object.values<Obj>(workspaces)) {
    checkGit(w, v.resources, deps);
    need(
      own(core.environments, w.environment_id),
      "missing workspace environment",
    );
    if (w.base_snapshot_id !== null)
      need(own(workspaces, w.base_snapshot_id), "missing workspace base");
    const paths = new Set<string>();
    for (const e of w.entries) {
      relative(e.path);
      need(!paths.has(e.path), "duplicate workspace path");
      paths.add(e.path);
      if (e.kind === "file")
        need(own(resources, e.resource_id), "missing workspace resource");
    }
    for (const deletion of w.deletions) relative(deletion);
    if (w.git) {
      const g = w.git;
      need(
        subset(g.bundle_resource_ids, Object.keys(resources)),
        "missing Git bundle",
      );
      for (const e of g.index_entries) {
        relative(e.path);
        if (e.resource_id)
          need(own(resources, e.resource_id), "missing index blob");
      }
      need(
        subset(g.lfs_dependency_ids, Object.keys(deps)),
        "missing LFS dependency",
      );
      for (const m of g.submodules) {
        relative(m.path);
        need(own(deps, m.dependency_id), "missing submodule dependency");
      }
    }
  }
  for (const op of Object.values<Obj>(operations)) {
    const handler = op.recovery.handler_dependency_id;
    need(handler === null || own(deps, handler), "missing recovery handler");
    need(
      subset(
        [...op.evidence_resource_ids, ...op.recovery.evidence_resource_ids],
        Object.keys(resources),
      ),
      "missing operation evidence",
    );
    if (op.recovery.strategy === "restart")
      need(
        op.replay === "idempotent" &&
          op.recovery.idempotency_ref &&
          op.recovery.evidence_resource_ids.length,
        "unsafe restart declaration",
      );
  }
  const planSubjects = object();
  for (const plan of p.plans) {
    need(own(core.checkpoints, plan.checkpoint_id), "missing checkpoint");
    const cp = core.checkpoints[plan.checkpoint_id];
    need(
      plan.context_id === cp.context_id &&
        plan.configuration_id === cp.configuration_id,
      "checkpoint binding mismatch",
    );
    need(
      own(core.contexts, plan.context_id) &&
        own(core.configurations, plan.configuration_id),
      "missing context/configuration",
    );
    const ctx = core.contexts[plan.context_id],
      config = core.configurations[plan.configuration_id];
    need(
      ctx.purpose === "continuation" &&
        ctx.at_event_id === cp.at_event_id &&
        ctx.branch_id === cp.branch_id,
      "stale continuation context",
    );
    need(ctx.configuration_id === config.id, "context configuration mismatch");
    const branch = core.branches[cp.branch_id];
    need(
      branch.head_event_id === cp.at_event_id,
      "checkpoint is not branch head",
    );
    for (const [field, group, label] of [
      ["workspace_ids", workspaces, "workspace"],
      ["dependency_ids", deps, "dependency"],
      ["service_binding_ids", services, "service"],
      ["operation_ids", operations, "operation"],
    ] as [string, Obj, string][])
      need(
        subset(plan[field], Object.keys(group)),
        "missing selected " + label,
      );
    const selectedDeps = new Set<string>(plan.dependency_ids);
    for (const id of selectedDeps)
      need(
        subset(deps[id].depends_on, selectedDeps),
        "incomplete dependency closure",
      );
    const roots = new Set<string>(
      plan.workspace_ids.map((id: string) => workspaces[id].root_id),
    );
    need(
      roots.size === plan.workspace_ids.length,
      "multiple selected states for root",
    );
    for (const id of plan.workspace_ids)
      need(
        workspaces[id].at_event_id === cp.at_event_id,
        "workspace boundary mismatch",
      );
    if (plan.cwd) {
      need(roots.has(plan.cwd.root_id), "missing cwd root");
      relative(plan.cwd.relative_path, true);
    }
    for (const path of plan.path_references) {
      need(roots.has(path.root_id), "missing mapped root");
      relative(path.relative_path, true);
      const groups: Obj = {
          event: "events",
          resource: "resources",
          environment: "environments",
          configuration: "configurations",
        },
        entities =
          path.entity_type === "dependency"
            ? deps
            : core[groups[path.entity_type]];
      need(own(entities, path.entity_id), "missing path mapping entity");
      need(path.json_pointer.startsWith("/"), "invalid JSON pointer");
      let value: any;
      try {
        value = pointer(entities[path.entity_id], path.json_pointer);
      } catch (e) {
        throw new Invalid(
          "path mapping pointer missing: " + (e as Error).message,
        );
      }
      need(typeof value === "string", "path mapping does not address a string");
    }
    const accounting = unique(plan.context_accounting, "event_id"),
      inputs = unique(ctx.inputs);
    need(
      setEqual(Object.keys(accounting), branch.event_ids),
      "incomplete context accounting",
    );
    for (const a of Object.values<Obj>(accounting))
      need(subset(a.input_ids, Object.keys(inputs)), "missing accounted input");
    const calls = object(),
      terminal = new Set<string>(),
      indexes = object();
    for (const item of ctx.inputs) {
      for (const source of item.source_events)
        if (!own(source, "capture_id"))
          need(own(core.events, source.event_id), "missing context source");
      if (item.kind === "tool_call") {
        need(!own(calls, item.call_id), "duplicate context call");
        need(own(core.tools, item.tool_id), "unknown context tool");
        calls[item.call_id] = item;
      }
      if (item.kind === "tool_result") {
        need(own(calls, item.call_id), "orphan context result");
        need(!terminal.has(item.call_id), "result after terminal");
        need(item.result_index > (indexes[item.call_id] ?? -1), "result order");
        indexes[item.call_id] = item.result_index;
        if (item.terminal) terminal.add(item.call_id);
      }
      if (["tool_call", "tool_result"].includes(item.kind))
        for (const source of item.source_events)
          if (!own(source, "capture_id")) {
            const ev = core.events[source.event_id];
            need(
              ev.kind === item.kind && ev.data.call_id === item.call_id,
              "context tool correlation changed",
            );
            if (!own(item, "transformation")) {
              const fields =
                item.kind === "tool_call"
                  ? ["tool_id", "arguments", "arguments_status"]
                  : ["parts", "result_index", "terminal", "outcome"];
              need(
                fields.every((f) => equal(item[f], ev.data[f])),
                "unreported tool context transformation",
              );
            }
          }
    }
    const selectedOps: Obj[] = plan.operation_ids.map(
        (id: string) => operations[id],
      ),
      boundCalls = selectedOps
        .filter((o) => own(o, "call_id"))
        .map((o) => o.call_id);
    need(
      new Set(boundCalls).size === boundCalls.length,
      "duplicate operation call binding",
    );
    need(
      subset(
        cp.open_calls.map((x: Obj) => x.call_id),
        boundCalls,
      ),
      "unbound open call",
    );
    need(
      setEqual(
        cp.open_calls.map((x: Obj) => x.call_id),
        Object.keys(calls).filter((id) => !terminal.has(id)),
      ),
      "open call state disagrees with context",
    );
    for (const op of selectedOps) {
      if (own(op, "call_id"))
        need(own(calls, op.call_id), "operation call absent from context");
      need(
        op.recovery.handler_dependency_id === null ||
          selectedDeps.has(op.recovery.handler_dependency_id),
        "recovery dependency not selected",
      );
    }
    const next = plan.next_action;
    if (next.kind === "reconcile_operation")
      need(
        plan.operation_ids.includes(next.operation_id),
        "next operation not selected",
      );
    if (next.kind === "await_decision")
      need(
        cp.open_decisions.some((x: Obj) => x.request_id === next.request_id),
        "next decision not pending",
      );
    if (next.kind === "resume_native")
      need(
        next.native_import_id === plan.native_import_id &&
          plan.native_import_id !== null,
        "next native import mismatch",
      );
    need(own(bindings, config.id), "missing effective configuration binding");
    const cb = bindings[config.id],
      instructions = unique(config.instructions),
      rules = unique(cb.instruction_rules, "instruction_id");
    need(
      setEqual(cb.effective_order, Object.keys(instructions)) &&
        setEqual(Object.keys(instructions), Object.keys(rules)),
      "incomplete instruction bindings",
    );
    const priorities = cb.effective_order.map(
      (id: string) => rules[id].priority,
    );
    need(
      equal(
        priorities,
        [...priorities].sort((a, b) => a - b),
      ),
      "instruction precedence mismatch",
    );
    need(
      setEqual(
        cb.policy_ids,
        config.policies.map((x: Obj) => x.id),
      ),
      "incomplete policy bindings",
    );
    for (const rule of Object.values<Obj>(rules)) {
      if (rule.scope.kind !== "global")
        need(roots.has(rule.scope.root_id), "instruction root not selected");
      if (rule.scope.kind === "path_prefix")
        relative(rule.scope.relative_path, true);
    }
    for (const id of plan.service_binding_ids) {
      const svc = services[id];
      need(
        subset(svc.dependency_ids, selectedDeps),
        "service dependency not selected",
      );
      need(
        subset(
          svc.secret_handles,
          config.secret_requirements.map((x: Obj) => x.handle),
        ),
        "undeclared secret handle",
      );
    }
    if (plan.native_import_id)
      need(own(native, plan.native_import_id), "missing native import");
    planSubjects[plan.id] = planRequirements(doc, plan, states);
  }
  return planSubjects;
}
export function inspectReport(
  doc: Obj,
  raw: Buffer,
  report: Obj,
  folder: string,
  now = Date.now(),
  validated?: Validated,
): Obj {
  const expected = inspectSession(doc, folder, validated);
  shape(report, true);
  const source = report.source;
  need(
    source.session_id === doc.session.id &&
      source.capture_id === doc.capture.id,
    "report source mismatch",
  );
  need(source.document_sha256 === hash(raw), "report digest mismatch");
  need(own(expected, source.plan_id), "report plan missing");
  need(
    date(report.assessed_at) <= now && now < date(report.expires_at),
    "stale assessment",
  );
  need(
    date(report.assessed_at) < date(report.expires_at),
    "invalid assessment interval",
  );
  const assessments = new Map<string, Obj>(
    report.assessments.map((a: Obj) => [key(a.subject), a]),
  );
  need(assessments.size === report.assessments.length, "duplicate assessment");
  const requirements = new Map<string, boolean>(
    expected[source.plan_id].map((item: Obj) => [
      key(item.subject),
      item.required,
    ]),
  );
  const needed = new Set(requirements.keys());
  need(subset(needed, assessments.keys()), "missing subject assessment");
  need(setEqual(needed, assessments.keys()), "unexpected subject assessment");
  for (const [k, required] of requirements)
    need(
      assessments.get(k)!.required === required,
      required
        ? "selected subject downgraded to optional"
        : "optional subject marked required",
    );
  const evidence = unique(report.evidence);
  for (const a of report.assessments)
    need(
      subset(a.evidence_ids, Object.keys(evidence)),
      "missing assessment evidence",
    );
  for (const t of report.transformations) {
    need(needed.has(key(t.subject)), "unexpected transformation subject");
    need(
      subset(t.evidence_ids, Object.keys(evidence)),
      "missing acceptance evidence",
    );
    if (assessments.get(key(t.subject))!.status === "omitted")
      need(t.losses.length, "omission transformation requires loss");
  }
  for (const r of [report.import_result, report.continuation_result])
    need(
      subset(r.evidence_ids, Object.keys(evidence)),
      "missing result evidence",
    );
  if (report.evaluation_mode === "synthetic")
    need(
      report.import_result.status === "not_attempted" &&
        report.continuation_result.status === "not_tested",
      "synthetic execution claim",
    );
  else {
    need(
      Object.values<Obj>(evidence).every((e) => e.kind !== "synthetic"),
      "synthetic evidence in observed report",
    );
    for (const [result, success, kind] of [
      [report.import_result, "imported", "import"],
      [report.continuation_result, "continued", "continuation"],
    ] as [Obj, string, string][])
      if (result.status === success)
        need(
          result.evidence_ids.some((id: string) => evidence[id].kind === kind),
          "missing runtime evidence",
        );
  }
  const p = doc.continuation,
    plan = p.plans.find((x: Obj) => x.id === source.plan_id),
    assessed = (kind: string, id: string, owner?: string) =>
      assessments.get(key(subject(kind, id, owner)))!,
    blocker = (kind: string, id: string, owner?: string) =>
      need(
        ["unresolved", "unsupported", "omitted"].includes(
          assessed(kind, id, owner).status,
        ),
        "known blocker marked supported",
      );
  const action = plan.next_action.kind,
    agent = ["model_request", "resume_native"].includes(action);
  const cp = doc.checkpoints.find((x: Obj) => x.id === plan.checkpoint_id);
  if (report.import_result.status === "imported")
    need(agent, "import claim exceeds assessed action");
  if (report.continuation_result.status === "continued")
    need(
      agent || action === "reconcile_operation",
      "continuation claim exceeds assessed action",
    );
  const config = doc.configurations.find(
    (c: Obj) => c.id === plan.configuration_id,
  );
  if (config.knowledge !== "effective") blocker("configuration", config.id);
  const binding = p.configuration_bindings.find(
    (b: Obj) => b.configuration_id === config.id,
  );
  for (const r of binding.instruction_rules)
    if (r.authority === "unknown" || r.merge_behavior === "unknown")
      blocker("instruction", r.instruction_id, config.id);
  if (
    plan.boundary.consistency !== "consistent" ||
    plan.boundary.method === "best_effort"
  )
    blocker("plan", plan.id);
  if (agent && cp.open_decisions.length) blocker("plan", plan.id);
  const ctx = doc.contexts.find((c: Obj) => c.id === plan.context_id);
  if (["partial", "unknown"].includes(ctx.fidelity)) blocker("context", ctx.id);
  if (plan.context_accounting.some((a: Obj) => a.disposition === "unavailable"))
    blocker("context", ctx.id);
  for (const r of doc.resources)
    if (
      needed.has(key(subject("resource", r.id))) &&
      ["unavailable", "excluded", "redacted", "unknown"].includes(
        r.availability,
      )
    )
      blocker("resource", r.id);
  for (const op of p.operations) {
    if (!plan.operation_ids.includes(op.id)) continue;
    const reconciling =
      action === "reconcile_operation" &&
      op.id === plan.next_action.operation_id;
    if (reconciling) {
      if (!["reconcile", "reconnect"].includes(op.recovery.strategy))
        blocker("operation", op.id);
      const a = assessed("operation", op.id);
      if (a.status === "supported") {
        const resolved = a.resolved ?? {};
        need(
          a.evidence_ids.length &&
            resolved.recovery_strategy === op.recovery.strategy &&
            op.external_identity !== null &&
            equal(resolved.external_identity, op.external_identity),
          "unverified operation recovery",
        );
      }
    } else if (["pending", "running", "outcome_unknown"].includes(op.state))
      blocker("operation", op.id);
  }
  for (const [ownerKind, owners] of [
    ["checkpoint_requirement", [cp]],
    ["environment_requirement", doc.environments],
  ] as [string, Obj[]][]) {
    for (const owner of owners)
      for (const requirement of owner.requirements) {
        const k = key(subject(ownerKind, requirement.id, owner.id));
        if (!needed.has(k)) continue;
        const a = assessments.get(k)!;
        if (a.status === "supported") {
          const resolved = a.resolved ?? {};
          need(
            a.evidence_ids.length && resolved.status === "available",
            "unverified core requirement",
          );
          if (own(requirement, "secret_handle"))
            need(
              (resolved.secret_handles ?? []).includes(
                requirement.secret_handle,
              ),
              "unresolved requirement secret",
            );
        }
      }
  }
  for (const d of p.dependencies)
    if (plan.dependency_ids.includes(d.id)) {
      const a = assessed("dependency", d.id);
      if (a.status === "supported") {
        const resolved = a.resolved ?? {},
          runtime = report.destination.runtime;
        need(
          resolved.identity === d.identity &&
            d.accepted_versions.includes(resolved.version),
          "unverified dependency binding",
        );
        need(
          d.platform.os.includes(runtime.os) &&
            d.platform.architectures.includes(runtime.architecture),
          "unsupported dependency platform",
        );
      }
    }
  for (const svc of p.service_bindings)
    if (plan.service_binding_ids.includes(svc.id)) {
      const a = assessed("service", svc.id);
      if (a.status === "supported") {
        const r = a.resolved ?? {};
        need(
          equal(r.account, svc.account) && r.audience === svc.audience,
          "wrong service identity",
        );
        need(
          subset(svc.scopes, r.scopes ?? []) &&
            subset(svc.secret_handles, r.secret_handles ?? []),
          "unresolved service access",
        );
        need(r.endpoint, "unresolved service endpoint");
      }
    }
  if (plan.native_import_id) {
    const n = p.native_imports.find((x: Obj) => x.id === plan.native_import_id);
    if (assessed("native_import", n.id).status === "supported")
      need(
        n.accepted_target_agent_versions.includes(
          report.destination.runtime.agent.version,
        ),
        "unsupported native target version",
      );
  }
  for (const f of doc.required_features)
    if (!SUPPORTED.has(f)) blocker("feature", f);
  const selectedRoots = new Set(
    p.workspaces
      .filter((w: Obj) => plan.workspace_ids.includes(w.id))
      .map((w: Obj) => w.root_id),
  );
  const roots = new Set(
      p.workspaces
        .filter(
          (w: Obj) =>
            plan.workspace_ids.includes(w.id) &&
            (assessed("workspace", w.id).required ||
              ["supported", "adapted"].includes(
                assessed("workspace", w.id).status,
              )),
        )
        .map((w: Obj) => w.root_id),
    ),
    mappings = unique(report.path_bindings, "root_id");
  need(
    subset(roots, Object.keys(mappings)) &&
      subset(Object.keys(mappings), selectedRoots),
    "incomplete path bindings",
  );
  const flattened = workspaceStates(p);
  for (const w of p.workspaces)
    if (plan.workspace_ids.includes(w.id) && own(mappings, w.root_id)) {
      const mapping = mappings[w.root_id],
        paths = new Set<string>();
      for (const e of Object.values<Obj>(flattened[w.id])) {
        let value = e.path;
        if (mapping.unicode_normalization !== "none")
          value = value.normalize(mapping.unicode_normalization);
        if (!mapping.case_sensitive) value = casefold(value);
        need(!paths.has(value), "destination path collision");
        paths.add(value);
      }
    }
  const model = report.model_assessment;
  need(
    equal(model.source, plan.model_requirements.source_model),
    "model source mismatch",
  );
  if (model.fit === "fits") {
    need(
      model.tokenizer !== null &&
        model.input_tokens !== null &&
        model.input_limit !== null,
      "unmeasured context fit",
    );
    need(
      model.input_tokens + model.output_reserve <= model.input_limit,
      "context exceeds budget",
    );
  } else blocker("model", plan.id);
  if (!equal(model.source, model.target))
    need(
      assessed("model", plan.id).status !== "supported",
      "silent model substitution",
    );
  const required: Obj[] = report.assessments.filter((a: Obj) => a.required),
    blockers = required.filter((a) =>
      ["omitted", "unresolved", "unsupported"].includes(a.status),
    );
  let pending = false;
  for (const a of report.assessments)
    if (a.status === "adapted") {
      const ts: Obj[] = report.transformations.filter(
        (t: Obj) => key(t.subject) === key(a.subject),
      );
      need(ts.length, "adaptation without mapping");
      if (a.required) pending ||= ts.some((t) => !t.accepted);
    }
  pending ||= report.transformations.some(
    (t: Obj) => requirements.get(key(t.subject)) && !t.accepted,
  );
  const predicted = blockers.length
    ? "blocked"
    : pending
      ? "adaptation_required"
      : "ready";
  need(report.outcome === predicted, "incorrect readiness outcome");
  const reasons = new Set(
    report.blocking_reasons.map((r: Obj) => key(r.subject)),
  );
  need(
    setEqual(
      blockers.map((a) => key(a.subject)),
      reasons,
    ),
    "missing or extraneous blocking reason",
  );
  if (!blockers.length)
    need(!reasons.size, "nonblocking report has blocking reasons");
  return {
    outcome: predicted,
    operational_authorization: false,
    evaluation_mode: report.evaluation_mode,
  };
}
