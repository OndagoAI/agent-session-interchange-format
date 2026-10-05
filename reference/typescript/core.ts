/** Core schema, identity, graph, provenance and selected-history checks. */
import * as fs from "node:fs";
import { Ajv2020 } from "ajv/dist/2020.js";
import {
  type Obj,
  need,
  own,
  unique,
  acyclic,
  Resources,
  pointer,
  decode,
  equal,
  subset,
  setEqual,
  object,
  SchemaInvalid,
  MAX_RESOURCE,
  utf8,
} from "./common.ts";
const ajv = new Ajv2020({
  strict: false,
  allErrors: false,
  ownProperties: true,
  validateFormats: false,
});
const schema = JSON.parse(
  fs.readFileSync(
    new URL("../../schemas/session.schema.json", import.meta.url),
    "utf8",
  ),
);
// Schemas live two directories above this module's directory.
const sessionValidator = ajv.compile(schema);
const reportValidator = ajv.compile(
  JSON.parse(
    fs.readFileSync(
      new URL("../../schemas/continuation-report.schema.json", import.meta.url),
      "utf8",
    ),
  ),
);
const snapshotValidator = ajv.compile({
  $ref:
    String(reportValidator.schema && (reportValidator.schema as Obj).$id) +
    "#/$defs/capability_snapshot",
});
export function snapshotShape(doc: Obj): void {
  if (!snapshotValidator(doc))
    throw new SchemaInvalid(
      (snapshotValidator.errors?.[0].schemaPath ?? "").split("/").slice(1),
    );
}
export function shape(doc: Obj, report = false): void {
  const v = report ? reportValidator : sessionValidator;
  if (!v(doc))
    throw new SchemaInvalid(
      (v.errors?.[0].schemaPath ?? "").split("/").slice(1),
    );
}
export const SUPPORTED = new Set([
  "asif.portable-continuation/0.2",
  "asif.streams/0.1",
  "asif.external-bindings/0.1",
]);
export interface Validated {
  collections: Obj;
  resources: Resources;
  unsupported_features: string[];
  streams: Obj;
}
export function effective(events: Obj[]): Obj[] {
  const replaced = new Set(
    events
      .filter((e) => e.supersedes && !own(e.supersedes, "capture_id"))
      .map((e) => e.supersedes.event_id),
  );
  return events.filter((e) => !replaced.has(e.id));
}
export function historyState(
  events: Obj[],
  externalCalls: Obj = object(),
  externalRequests: Obj = object(),
  partialTasks = false,
): Obj {
  const calls = Object.assign(object(), externalCalls),
    requests = Object.assign(object(), externalRequests),
    closed = object(),
    decisions = object(),
    tasks = object(),
    indices = object(),
    executions = object(),
    callEvents = object(),
    taskGaps = object();
  const selected = new Set(effective(events).map((e) => e.id));
  for (const event of events) {
    // Keep calls in their recorded positions so late amendments do not orphan
    // results or decisions. The fold updates knowledge, not execution state.
    if (event.kind !== "tool_call" && !selected.has(event.id)) continue;
    const d = event.data,
      id = d.call_id;
    switch (event.kind) {
      case "tool_call":
        if (own(calls, id)) {
          const prior = event.supersedes ?? object();
          need(
            own(callEvents, id) &&
              !own(prior, "capture_id") &&
              prior.event_id === callEvents[id],
            "conflicting selected call versions",
          );
        }
        calls[id] = d;
        callEvents[id] = event.id;
        break;
      case "tool_result":
        need(own(calls, id), "orphan tool result");
        need(!own(closed, id), "tool result after terminal");
        need(d.result_index > (indices[id] ?? -1), "tool result index order");
        indices[id] = d.result_index;
        if (d.terminal) closed[id] = d.outcome;
        break;
      case "decision_request":
        need(!own(requests, d.request_id), "duplicate decision request");
        requests[d.request_id] = d;
        if (own(d, "call_id")) need(own(calls, id), "decision call missing");
        if (own(d, "task_id"))
          need(
            own(tasks, d.task_id) &&
              tasks[d.task_id].revision === d.task_revision,
            "decision task revision mismatch",
          );
        break;
      case "decision_resolution":
        need(own(requests, d.request_id), "orphan decision resolution");
        need(
          !own(decisions, d.request_id),
          "contradictory decision resolutions",
        );
        if (own(d, "selected_option_id"))
          need(
            requests[d.request_id].options.some(
              (x: Obj) => x.id === d.selected_option_id,
            ),
            "unknown decision option",
          );
        decisions[d.request_id] = d;
        break;
      case "task_update": {
        const prior = tasks[d.task_id];
        need(
          !own(event, "supersedes"),
          "task revisions use previous_revision, not supersedes",
        );
        if (own(d, "previous_revision"))
          need(
            d.previous_revision < d.revision,
            "task predecessor revision must be earlier",
          );
        if (prior) {
          need(
            d.previous_revision === prior.revision &&
              d.revision > prior.revision,
            "task revision transition",
          );
          if (
            ["completed", "failed", "cancelled", "superseded"].includes(
              prior.status,
            ) &&
            ["proposed", "pending", "in_progress"].includes(d.status)
          )
            need(d.reopen_reason, "task reopen reason missing");
        } else if (own(d, "previous_revision")) {
          need(partialTasks, "task predecessor not in selected history");
          taskGaps[d.task_id] = d.previous_revision;
        }
        tasks[d.task_id] = d;
        const pending = [...(d.dependencies ?? [])],
          seen = new Set<string>();
        while (pending.length) {
          const dependency = pending.pop()!;
          need(dependency !== d.task_id, "task dependency cycle");
          if (!seen.has(dependency)) {
            seen.add(dependency);
            pending.push(...(tasks[dependency]?.dependencies ?? []));
          }
        }
        break;
      }
      case "execution_transition":
        need(
          !["completed", "failed", "cancelled", "interrupted"].includes(
            executions[d.execution_id],
          ),
          "terminal execution reopened",
        );
        executions[d.execution_id] = d.status;
        break;
    }
  }
  const dependencyStates = object();
  for (const [id, task] of Object.entries<Obj>(tasks)) {
    dependencyStates[id] = own(task, "dependencies") ? object() : null;
    for (const dependency of task.dependencies ?? []) {
      const target = tasks[dependency] ?? object();
      const status = target.status ?? "unknown";
      dependencyStates[id][dependency] = {
        revision: target.revision ?? null,
        state:
          status === "completed"
            ? "satisfied"
            : status === "unknown"
              ? "unknown"
              : "unsatisfied",
      };
    }
  }
  return {
    calls,
    closed_calls: closed,
    requests,
    decisions,
    tasks,
    executions,
    task_history_gaps: taskGaps,
    task_dependencies: dependencyStates,
  };
}
export function validateDocument(doc: Obj, folder: string): Validated {
  shape(doc);
  const partialTasks =
    doc.coverage.find((c: Obj) => c.scope === "tasks").status === "partial";
  const collections = object();
  for (const name of [
    "participants",
    "events",
    "branches",
    "executions",
    "contexts",
    "configurations",
    "tools",
    "resources",
    "environments",
    "checkpoints",
    "losses",
  ])
    collections[name] = unique(doc[name]);
  const resources = new Resources(doc, folder),
    events = collections.events,
    participants = collections.participants;
  const parents: Record<string, string[]> = object();
  for (const [id, p] of Object.entries<Obj>(participants))
    parents[id] = own(p, "parent_participant_id")
      ? [p.parent_participant_id]
      : [];
  acyclic(parents, "participant");
  const sequences = Object.values<Obj>(events).map((e) => e.sequence);
  need(
    new Set(sequences).size === sequences.length,
    "duplicate event sequence",
  );
  need(
    equal(
      sequences,
      [...sequences].sort((a, b) => a - b),
    ),
    "events not serialized in sequence order",
  );
  for (const branch of Object.values<Obj>(collections.branches)) {
    need(subset(branch.event_ids, Object.keys(events)), "missing branch event");
    need(
      branch.head_event_id === (branch.event_ids.at(-1) ?? null),
      "wrong branch head",
    );
    const positions = new Map<string, number>(
      branch.event_ids.map((id: string, i: number) => [id, i]),
    );
    for (const id of branch.event_ids)
      for (const cause of events[id].causes)
        if (!own(cause, "capture_id") && positions.has(cause.event_id))
          need(
            positions.get(cause.event_id)! < positions.get(id)!,
            "branch causal order",
          );
  }
  const eventRef = (r: Obj) => {
    if (!own(r, "capture_id"))
      need(own(events, r.event_id), "missing local event reference");
  };
  const parts = (values: Obj[]) => {
    for (const p of values)
      if (["resource", "opaque"].includes(p.kind)) resources.ref(p.resource_id);
  };
  const provenance = (v: Obj) => {
    for (const i of v.inputs ?? []) eventRef(i);
    for (const source of v.sources ?? []) {
      resources.ref(source.resource_id);
      const loc = source.locator;
      if (!loc) continue;
      if (loc.syntax === "bytes") {
        need(
          Number.isInteger(loc.offset) && loc.offset >= 0,
          "invalid source offset",
        );
        need(
          Number.isInteger(loc.length) && loc.length >= 0,
          "invalid source length",
        );
        const r = resources.records[source.resource_id];
        need(
          own(r, "bytes") && loc.offset + loc.length <= r.bytes,
          "source span outside resource",
        );
      } else if (loc.syntax === "json_pointer") {
        need(
          typeof loc.value === "string",
          "invalid structured source locator",
        );
        if (resources.cache.has(source.resource_id))
          pointer(decode(resources.bytes(source.resource_id)), loc.value);
      }
    }
  };
  const calls = object(),
    requests = object(),
    taskRevisions = new Set<string>(),
    causes: Record<string, string[]> = object(),
    supersessions: Record<string, string[]> = object(),
    externalCalls = object(),
    externalRequests = object();
  for (const binding of doc.external_bindings ?? []) {
    const target = binding.kind === "call" ? externalCalls : externalRequests;
    need(!own(target, binding.id), "duplicate external binding");
    target[binding.id] = binding.descriptor;
  }
  for (const [id, e] of Object.entries<Obj>(events)) {
    need(own(participants, e.actor_id), "missing actor");
    if (own(e, "execution_id"))
      need(own(collections.executions, e.execution_id), "missing execution");
    provenance(e.provenance);
    causes[id] = [];
    supersessions[id] = [];
    for (const cause of e.causes) {
      eventRef(cause);
      if (!own(cause, "capture_id")) {
        need(
          events[cause.event_id].sequence < e.sequence,
          "noncausal event order",
        );
        causes[id].push(cause.event_id);
      }
    }
    need(new Set(causes[id]).size === causes[id].length, "duplicate cause");
    if (e.supersedes) {
      eventRef(e.supersedes);
      if (!own(e.supersedes, "capture_id")) {
        const prior = events[e.supersedes.event_id];
        need(
          prior.sequence < e.sequence && prior.kind === e.kind,
          "invalid supersession",
        );
        if (e.kind === "decision_resolution")
          need(
            prior.data.request_id === e.data.request_id,
            "decision correction changed request",
          );
        supersessions[id].push(prior.id);
      }
    }
    const d = e.data;
    for (const name of ["parts", "prompt", "answer"])
      if (own(d, name)) parts(d[name]);
    if (e.kind === "tool_call") {
      need(!own(externalCalls, d.call_id), "duplicate call identity");
      if (e.supersedes) {
        need(
          !own(e.supersedes, "capture_id"),
          "call amendment requires local predecessor",
        );
        const prior = events[e.supersedes.event_id],
          previous = prior.data;
        need(
          d.call_id === previous.call_id && d.tool_id === previous.tool_id,
          "call amendment changed invocation",
        );
        need(
          d.retry_of === previous.retry_of,
          "call amendment changed retry relationship",
        );
        need(
          e.actor_id === prior.actor_id &&
            e.execution_id === prior.execution_id,
          "call amendment changed actor or execution",
        );
        need(
          previous.arguments_status !== "complete",
          "completed call cannot be amended",
        );
        need(
          previous.arguments_status !== "partial" ||
            d.arguments_status !== "unknown",
          "call argument knowledge regressed",
        );
      } else need(!own(calls, d.call_id), "duplicate call identity");
      need(d.retry_of !== d.call_id, "retry must use new call identity");
      need(own(collections.tools, d.tool_id), "missing tool definition");
      calls[d.call_id] = d;
    } else if (e.kind === "decision_request") {
      need(
        !own(requests, d.request_id) && !own(externalRequests, d.request_id),
        "duplicate decision request",
      );
      unique(d.options);
      requests[d.request_id] = d;
    } else if (e.kind === "task_update") {
      const key = JSON.stringify([d.task_id, d.revision]);
      need(!taskRevisions.has(key), "duplicate task revision");
      taskRevisions.add(key);
      need(
        !own(e, "supersedes"),
        "task revisions use previous_revision, not supersedes",
      );
      need(!(d.dependencies ?? []).includes(d.task_id), "task self dependency");
      if (own(d, "previous_revision"))
        need(
          d.previous_revision < d.revision,
          "task predecessor revision must be earlier",
        );
    } else if (
      [
        "context_checkpoint",
        "configuration_change",
        "execution_transition",
        "resource_change",
      ].includes(e.kind)
    ) {
      const map: Record<string, string[]> = {
        context_checkpoint: ["context_id", "contexts"],
        configuration_change: ["configuration_id", "configurations"],
        execution_transition: ["execution_id", "executions"],
        resource_change: ["resource_id", "resources"],
      };
      const [field, group] = map[e.kind];
      need(own(collections[group], d[field]), "missing " + field);
      for (const f of ["replaced_context_id", "previous_resource_id"])
        if (own(d, f))
          need(
            own(
              collections[
                f === "replaced_context_id" ? "contexts" : "resources"
              ],
              d[f],
            ),
            "missing predecessor",
          );
    } else if (e.kind === "extension" && d.interpretation_required)
      need(
        doc.required_features.includes(d.type),
        "ungated required extension",
      );
  }
  acyclic(causes, "causal");
  acyclic(supersessions, "supersession");
  const taskIds = new Set(
    Object.values<Obj>(events)
      .filter((e) => e.kind === "task_update")
      .map((e) => e.data.task_id),
  );
  for (const e of Object.values<Obj>(events)) {
    if (e.kind === "task_update") {
      need(
        (e.data.dependencies ?? []).every((id: string) => taskIds.has(id)),
        "missing task dependency",
      );
      if (own(e.data, "previous_revision"))
        need(
          taskRevisions.has(
            JSON.stringify([e.data.task_id, e.data.previous_revision]),
          ) || partialTasks,
          "task predecessor absent without partial coverage",
        );
    }
    if (e.kind === "tool_result")
      need(
        own(calls, e.data.call_id) || own(externalCalls, e.data.call_id),
        "orphan tool result",
      );
    if (e.kind === "decision_resolution")
      need(
        own(requests, e.data.request_id) ||
          own(externalRequests, e.data.request_id),
        "orphan decision resolution",
      );
  }
  for (const b of doc.external_bindings ?? []) {
    if (b.kind === "call")
      need(
        own(collections.tools, b.descriptor.tool_id),
        "missing external tool",
      );
    else {
      parts(b.descriptor.prompt);
      unique(b.descriptor.options);
    }
  }
  for (const t of Object.values<Obj>(collections.tools)) {
    for (const name of ["input_schema", "output_schema"])
      if (own(t, name) && !ajv.validateSchema(t[name]))
        throw new SchemaInvalid(["tools", name]);
    for (const id of t.resource_ids ?? []) resources.ref(id);
  }
  for (const c of Object.values<Obj>(collections.configurations)) {
    for (const name of ["instructions", "capabilities", "policies"])
      unique(c[name]);
    unique(c.secret_requirements, "handle");
    for (const i of c.instructions) {
      parts(i.parts);
      provenance(i.provenance);
    }
    for (const cap of c.capabilities)
      for (const id of cap.resource_ids) resources.ref(id);
    for (const id of c.environment_ids ?? [])
      need(
        own(collections.environments, id),
        "missing configuration environment",
      );
  }
  for (const e of Object.values<Obj>(collections.environments))
    for (const id of e.resource_ids) resources.ref(id);
  for (const e of Object.values<Obj>(collections.executions)) {
    need(own(participants, e.participant_id), "missing execution participant");
    need(
      subset(e.context_ids, Object.keys(collections.contexts)),
      "missing execution context",
    );
  }
  for (const r of Object.values<Obj>(resources.records)) {
    if (r.purpose === "session_memory")
      need(own(r, "provenance"), "memory provenance missing");
    if (r.provenance) provenance(r.provenance);
  }
  for (const context of Object.values<Obj>(collections.contexts)) {
    need(
      own(collections.branches, context.branch_id),
      "missing context branch",
    );
    const boundary = context.at_event_id;
    if (boundary !== null)
      need(
        collections.branches[context.branch_id].event_ids.includes(boundary),
        "context boundary outside branch",
      );
    if (own(context, "configuration_id"))
      need(
        own(collections.configurations, context.configuration_id),
        "missing context configuration",
      );
    need(
      subset(context.tool_ids, Object.keys(collections.tools)),
      "missing context tool",
    );
    unique(context.inputs);
    const typed: Obj[] = [];
    for (const item of context.inputs) {
      parts(item.parts);
      for (const source of item.source_events) {
        eventRef(source);
        if (!own(source, "capture_id") && boundary !== null)
          need(
            events[source.event_id].sequence <= events[boundary].sequence,
            "context uses future event",
          );
      }
      if (["tool_call", "tool_result"].includes(item.kind)) {
        if (item.kind === "tool_call")
          need(
            own(collections.tools, item.tool_id),
            "missing context call tool",
          );
        typed.push({ id: item.id, kind: item.kind, data: item });
      }
    }
    historyState(typed);
  }
  const heads: Record<string, Obj[]> = object();
  for (const id of Object.keys(collections.branches)) heads[id] = [];
  for (const cp of Object.values<Obj>(collections.checkpoints)) {
    need(own(collections.branches, cp.branch_id), "missing checkpoint branch");
    const branch = collections.branches[cp.branch_id];
    need(
      (cp.at_event_id === null && !branch.event_ids.length) ||
        branch.event_ids.includes(cp.at_event_id),
      "checkpoint boundary outside branch",
    );
    if (cp.at_event_id === branch.head_event_id) heads[branch.id].push(cp);
    if (cp.context_id) {
      need(
        own(collections.contexts, cp.context_id),
        "missing checkpoint context",
      );
      const ctx = collections.contexts[cp.context_id];
      need(
        ctx.branch_id === cp.branch_id,
        "checkpoint context branch mismatch",
      );
      if (ctx.at_event_id !== null)
        need(
          cp.at_event_id !== null &&
            events[ctx.at_event_id].sequence <= events[cp.at_event_id].sequence,
          "checkpoint context is newer than boundary",
        );
    }
    if (cp.configuration_id)
      need(
        own(collections.configurations, cp.configuration_id),
        "missing checkpoint configuration",
      );
    const ids = cp.at_event_id
        ? branch.event_ids.slice(
            0,
            branch.event_ids.indexOf(cp.at_event_id) + 1,
          )
        : [],
      state = historyState(
        ids.map((id: string) => events[id]),
        externalCalls,
        externalRequests,
        partialTasks,
      );
    unique(cp.open_calls, "call_id");
    unique(cp.open_decisions, "request_id");
    unique(cp.tasks, "task_id");
    for (const c of cp.open_calls)
      need(
        own(state.calls, c.call_id) && !own(state.closed_calls, c.call_id),
        "checkpoint call not open",
      );
    for (const q of cp.open_decisions)
      need(
        own(state.requests, q.request_id) &&
          !own(state.decisions, q.request_id),
        "checkpoint decision not open",
      );
    for (const t of cp.tasks)
      need(
        own(state.tasks, t.task_id) &&
          t.revision === state.tasks[t.task_id].revision,
        "checkpoint task revision mismatch",
      );
    const cov = Object.fromEntries(
      doc.coverage.map((c: Obj) => [c.scope, c.status]),
    );
    if (cp.knowledge !== "unknown") {
      if (cov.tools === "complete")
        need(
          setEqual(
            cp.open_calls.map((x: Obj) => x.call_id),
            Object.keys(state.calls).filter(
              (id) => !own(state.closed_calls, id),
            ),
          ),
          "unaccounted open call",
        );
      if (cov.decisions === "complete")
        need(
          setEqual(
            cp.open_decisions.map((x: Obj) => x.request_id),
            Object.keys(state.requests).filter(
              (id) => !own(state.decisions, id),
            ),
          ),
          "unaccounted open decision",
        );
    }
  }
  for (const cps of Object.values(heads))
    need(cps.length === 1, "branch requires exactly one head checkpoint");
  for (const b of Object.values<Obj>(collections.branches))
    historyState(
      b.event_ids.map((id: string) => events[id]),
      externalCalls,
      externalRequests,
      partialTasks,
    );
  const nonempty = object();
  for (const name of [
    "participants",
    "branches",
    "executions",
    "contexts",
    "resources",
  ])
    nonempty[name] = doc[name].length > 0;
  Object.assign(nonempty, {
    configuration: !!doc.configurations.length,
    environment: !!doc.environments.length,
    conversation: doc.events.some((e: Obj) => e.kind === "message"),
    tools: !!doc.tools.length || !!Object.keys(calls).length,
    decisions: !!Object.keys(requests).length,
    tasks: !!taskRevisions.size,
    native: doc.resources.some((r: Obj) => r.purpose === "native"),
    usage: !!doc.usage?.length,
  });
  for (const c of doc.coverage)
    if (c.status === "known_empty")
      need(!nonempty[c.scope], "known-empty coverage contains data");
  for (const loss of Object.values<Obj>(collections.losses))
    for (const r of loss.references ?? []) {
      const group: Record<string, string> = {
        event: "events",
        resource: "resources",
        context: "contexts",
        configuration: "configurations",
        participant: "participants",
        execution: "executions",
        branch: "branches",
        checkpoint: "checkpoints",
        tool: "tools",
        environment: "environments",
      };
      if (own(group, r.type))
        need(own(collections[group[r.type]], r.id), "missing loss reference");
    }
  const result: Validated = {
    collections,
    resources,
    unsupported_features: doc.required_features
      .filter((f: string) => !SUPPORTED.has(f))
      .sort(),
    streams: object(),
  };
  result.streams = assembleStreams(doc, result);
  return result;
}
export function assembleStreams(doc: Obj, v: Validated): Obj {
  const outputs = object();
  for (const stream of doc.streams ?? []) {
    need(!own(outputs, stream.id), "duplicate stream ID");
    need(own(v.collections.events, stream.event_id), "missing stream event");
    const event = v.collections.events[stream.event_id];
    need(event.data.call_id === stream.call_id, "stream call mismatch");
    if (stream.kind === "tool_result_text")
      need(
        event.kind === "tool_result" &&
          event.data.result_index === stream.result_index,
        "stream result mismatch",
      );
    const segments: Obj[] = stream.segments,
      indices = segments.map((s) => s.index);
    need(
      new Set(indices).size === indices.length &&
        equal(
          indices,
          [...indices].sort((a, b) => a - b),
        ),
      "duplicate/unordered stream segment",
    );
    need(
      segments.filter((s) => s.terminal).length <= 1,
      "multiple stream terminal segments",
    );
    if (segments.some((s) => s.terminal))
      need(segments.at(-1)!.terminal, "stream terminal before final segment");
    let expected = 0,
      gap = false,
      total = 0;
    const chunks: Buffer[] = [];
    for (const segment of segments) {
      const raw = v.resources.bytes(segment.resource_id),
        end = segment.offset + segment.length;
      need(end <= raw.length, "stream span outside resource");
      if (segment.index !== expected) gap = true;
      if (!gap) {
        chunks.push(raw.subarray(segment.offset, end));
        expected++;
        total += segment.length;
      }
      need(total <= MAX_RESOURCE, "stream assembly byte limit");
    }
    const complete = !gap && segments.length > 0 && segments.at(-1)!.terminal,
      raw = Buffer.concat(chunks);
    need(
      stream.status === (complete ? "complete" : "partial"),
      "stream completeness mismatch",
    );
    if (complete && stream.kind === "tool_arguments") {
      need(
        event.kind === "tool_call" &&
          event.data.arguments_status === "complete",
        "stream final call mismatch",
      );
      need(
        equal(decode(raw), event.data.arguments),
        "assembled arguments mismatch",
      );
    } else if (complete)
      need(
        equal(event.data.parts, [{ kind: "text", text: utf8(raw) }]),
        "assembled result mismatch",
      );
    else if (stream.kind === "tool_arguments")
      need(
        event.kind === "tool_call" && event.data.arguments_status === "partial",
        "partial stream presented as executable call",
      );
    outputs[stream.id] = {
      status: complete ? "complete" : "partial",
      contiguous_bytes: raw.length,
      executable: false,
    };
  }
  return outputs;
}
