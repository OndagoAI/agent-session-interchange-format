import {
  type Obj,
  need,
  relative,
  Unsupported,
  equal,
  unique,
} from "./common.ts";
import type { Validated } from "./core.ts";
export function matchesScope(scope: Obj, environment: Obj): boolean {
  if (scope.kind === "global") return true;
  if (scope.root_id !== environment.root_id) return false;
  if (scope.kind === "root") return true;
  relative(scope.relative_path, true);
  const path = environment.relative_path ?? "";
  relative(path, true);
  const prefix = scope.relative_path.replace(/\/+$/, "");
  return !prefix || path === prefix || path.startsWith(prefix + "/");
}
export function predicate(
  expression: Obj,
  environment: Obj,
  depth = 0,
): boolean {
  need(
    depth <= 32 &&
      expression !== null &&
      typeof expression === "object" &&
      !Array.isArray(expression) &&
      Object.keys(expression).length === 1,
    "invalid predicate",
  );
  const [op, value] = Object.entries(expression)[0];
  if (["all", "any"].includes(op)) {
    need(Array.isArray(value), "predicate list required");
    const values = value.map((x) => predicate(x, environment, depth + 1));
    return op === "all" ? values.every(Boolean) : values.some(Boolean);
  }
  if (op === "not") return !predicate(value, environment, depth + 1);
  if (op === "event_kind_in") {
    need(
      Array.isArray(value) && value.every((x) => typeof x === "string"),
      "invalid event predicate",
    );
    return value.includes(environment.event_kind);
  }
  if (op === "root_is") {
    need(typeof value === "string", "invalid root predicate");
    return environment.root_id === value;
  }
  if (op === "path_prefix") {
    need(typeof value === "string", "invalid path predicate");
    relative(value, true);
    const path = environment.relative_path ?? "";
    relative(path, true);
    return (
      !value ||
      path === value ||
      path.startsWith(value.replace(/\/+$/, "") + "/")
    );
  }
  throw new Unsupported("unknown predicate operator");
}
function active(rule: Obj, environment: Obj): boolean {
  if (!matchesScope(rule.scope, environment)) return false;
  if (rule.activation.kind === "always") return true;
  if (rule.activation.dialect !== "asif.activation/0.1")
    throw new Unsupported("unsupported activation dialect");
  return predicate(rule.activation.expression, environment);
}
export function resolveConfiguration(
  doc: Obj,
  id: string,
  environment: Obj,
): Obj {
  const config = doc.configurations.find((c: Obj) => c.id === id);
  need(config, "unknown configuration");
  need(config.knowledge === "effective", "configuration not effective");
  const binding = doc.continuation?.configuration_bindings.find(
    (b: Obj) => b.configuration_id === id,
  );
  need(binding, "missing configuration binding");
  const instructions = unique(config.instructions),
    rules = unique(binding.instruction_rules, "instruction_id");
  let selected: string[] = [];
  for (const id of binding.effective_order) {
    const rule = rules[id];
    if (!active(rule, environment)) continue;
    if (rule.authority === "unknown" || rule.merge_behavior === "unknown")
      throw new Unsupported("unknown instruction interpretation");
    if (rule.authority === "untrusted")
      throw new Unsupported("untrusted content cannot become an instruction");
    const same = selected.filter((old) =>
      ["authority", "group_id", "scope"].every((k) =>
        equal(rules[old][k], rule[k]),
      ),
    );
    if (rule.merge_behavior === "replace_same_scope")
      selected = selected.filter((old) => !same.includes(old));
    else if (rule.merge_behavior === "reject_conflict")
      need(
        same.every((old) =>
          equal(instructions[old].parts, instructions[id].parts),
        ),
        "instruction group conflict",
      );
    selected.push(id);
  }
  return {
    configuration_id: id,
    instruction_ids: selected,
    instructions: selected.map((id) => structuredClone(instructions[id])),
    scope: "neutral declaration evaluation; no runtime application",
  };
}
export function evaluatePolicy(config: Obj, environment: Obj): Obj {
  const effects: string[] = [],
    considered: string[] = [];
  for (const p of config.policies) {
    if (!p.enforcing) continue;
    if (p.type !== "asif.policy/0.1")
      throw new Unsupported("unsupported enforcing policy");
    const d = p.definition;
    need(["allow", "deny", "ask"].includes(d.effect), "invalid policy effect");
    need(
      Array.isArray(d.tool_ids) &&
        d.tool_ids.every((x: any) => typeof x === "string"),
      "invalid policy tools",
    );
    if (!d.tool_ids.includes("*") && !d.tool_ids.includes(environment.tool_id))
      continue;
    if (active(d, environment)) {
      effects.push(d.effect);
      considered.push(p.id);
    }
  }
  return {
    decision: effects.includes("deny")
      ? "deny"
      : effects.includes("ask") || !effects.length
        ? "ask"
        : "allow",
    policy_ids: considered,
    scope:
      "declarative policy evaluation; destination authorization still required",
  };
}
export function reconstructRequest(doc: Obj, v: Validated, id: string): Obj {
  const ctx = doc.contexts.find((c: Obj) => c.id === id);
  need(ctx, "unknown context");
  if (["partial", "unknown"].includes(ctx.fidelity))
    throw new Unsupported("incomplete request context");
  if (v.unsupported_features.length)
    throw new Unsupported("required feature unsupported");
  const ids = new Set<string>();
  for (const item of ctx.inputs) {
    if (item.kind === "tool_call" && item.arguments_status !== "complete")
      throw new Unsupported("partial tool arguments");
    for (const part of item.parts) {
      if (["resource", "opaque"].includes(part.kind)) ids.add(part.resource_id);
      if (["opaque", "structured"].includes(part.kind))
        throw new Unsupported(
          "opaque/structured content requires a declared request encoder",
        );
    }
  }
  for (const id of ids) v.resources.bytes(id);
  return structuredClone({
    request_version: "0.1",
    source: {
      session_id: doc.session.id,
      capture_id: doc.capture.id,
      context_id: id,
    },
    fidelity: ctx.fidelity,
    inputs: ctx.inputs,
    tools: ctx.tool_ids.flatMap((id: string) =>
      doc.tools.filter((t: Obj) => t.id === id),
    ),
    model: ctx.model ?? null,
    request_parameters: ctx.request_parameters ?? {},
    configuration_id: ctx.configuration_id ?? null,
    resources: [...ids].sort().map((id) => v.resources.records[id]),
    provider_encoding: "not_selected",
    token_budget: "unmeasured",
    losses: [],
  });
}
