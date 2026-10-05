/** Exact-byte supplied evidence. Does not probe or authorize a destination. */
import {
  type Obj,
  need,
  Invalid,
  Unsupported,
  decode,
  unique,
  equal,
  subset,
  hash,
} from "./common.ts";
import { snapshotShape } from "./core.ts";
export const SNAPSHOT_FORMAT = "asif.destination-capabilities/0.1";
export const MAX_SNAPSHOT = 1024 * 1024;
const kinds: Obj = {
  dependency: "dependency",
  configuration: "configuration",
  instruction: "configuration",
  capability: "capability",
  policy: "policy",
  model: "model",
  context: "model",
  workspace: "workspace",
  service: "service",
  operation: "operation",
  native_import: "native_import",
  environment: "environment",
  checkpoint_requirement: "environment",
  environment_requirement: "environment",
};
function time(value: string): number {
  need(/(Z|[+-]\d\d:\d\d)$/.test(value), "snapshot time needs timezone");
  const match =
    /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,3})?(?:Z|([+-])(\d{2}):(\d{2}))$/.exec(
      value,
    );
  need(match, "invalid snapshot time");
  const [year, month, day, hour, minute, second] = match
    .slice(1, 7)
    .map(Number);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  need(
    year >= 1 &&
      month >= 1 &&
      month <= 12 &&
      day >= 1 &&
      day <= days[month - 1] &&
      hour < 24 &&
      minute < 60 &&
      second < 60 &&
      Number(match[8] ?? 0) < 24 &&
      Number(match[9] ?? 0) < 60,
    "invalid snapshot time",
  );
  const result = Date.parse(value);
  need(Number.isFinite(result), "invalid snapshot time");
  return result;
}
export function snapshotBytes(report: Obj): Buffer {
  const envelope = report.destination.capabilities_snapshot;
  if (envelope.format !== SNAPSHOT_FORMAT)
    throw new Unsupported("unsupported capability snapshot format");
  if (envelope.availability !== "supplied")
    throw new Unsupported("capability snapshot unavailable");
  need(
    envelope.data.length <= 4 * Math.ceil(MAX_SNAPSHOT / 3),
    "capability snapshot byte limit",
  );
  need(
    /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(
      envelope.data,
    ),
    "invalid snapshot base64",
  );
  const raw = Buffer.from(envelope.data, "base64");
  need(
    raw.toString("base64") === envelope.data,
    "noncanonical snapshot base64",
  );
  need(
    raw.length > 0 &&
      raw.length <= MAX_SNAPSHOT &&
      raw.length === envelope.bytes,
    "capability snapshot byte count",
  );
  need(
    hash(raw) === report.destination.capabilities_sha256,
    "capability snapshot digest mismatch",
  );
  return raw;
}
export function inspectCapabilities(
  report: Obj,
  plan: Obj,
  now: number,
  currentSnapshot: Buffer | undefined,
  doc: Obj,
): boolean {
  const raw = snapshotBytes(report);
  need(
    !raw.subarray(0, 3).equals(Buffer.from([0xef, 0xbb, 0xbf])),
    "snapshot UTF-8 BOM forbidden",
  );
  const snapshot = decode(raw);
  need(
    snapshot && typeof snapshot === "object" && !Array.isArray(snapshot),
    "snapshot must be an object",
  );
  need(
    typeof snapshot.snapshot_version === "string",
    "missing or invalid snapshot version",
  );
  if (snapshot.snapshot_version !== "0.1")
    throw new Unsupported("unsupported capability snapshot version");
  snapshotShape(snapshot);
  const destination = report.destination,
    envelope = destination.capabilities_snapshot;
  need(
    snapshot.destination_id === destination.id &&
      equal(snapshot.runtime, destination.runtime),
    "snapshot destination mismatch",
  );
  need(
    snapshot.evaluation_mode === report.evaluation_mode,
    "snapshot evaluation mode mismatch",
  );
  need(
    time(snapshot.observed_at) <= time(report.assessed_at) &&
      time(report.assessed_at) < time(report.expires_at) &&
      time(report.expires_at) <= time(snapshot.expires_at),
    "snapshot assessment interval mismatch",
  );
  need(
    time(snapshot.observed_at) <= now && now < time(snapshot.expires_at),
    "stale capability snapshot",
  );
  const evidence = unique(report.evidence),
    e = evidence[envelope.evidence_id];
  need(e, "missing snapshot evidence");
  need(
    e.producer === snapshot.producer &&
      time(e.time) === time(snapshot.observed_at),
    "snapshot evidence mismatch",
  );
  need(
    e.kind ===
      (snapshot.evaluation_mode === "synthetic" ? "synthetic" : "inspection"),
    "snapshot evidence kind mismatch",
  );
  const components = unique(snapshot.components);
  for (const a of report.assessments) {
    const ids: string[] = a.component_ids;
    need(subset(ids, Object.keys(components)), "missing snapshot component");
    if (!["supported", "adapted"].includes(a.status)) continue;
    const kind = a.subject.kind,
      expected = Object.hasOwn(kinds, kind) ? kinds[kind] : undefined;
    const bound: Obj[] = ids.map((id) => components[id]);
    need(
      bound.every((c) => c.status === "available"),
      "unavailable snapshot component claimed supported",
    );
    if (!expected) {
      if (kind === "feature")
        need(
          snapshot.supported_features.includes(a.subject.id),
          "snapshot feature unsupported",
        );
      continue;
    }
    const selected = bound.filter((c) => c.kind === expected);
    need(
      selected.length === 1,
      "missing or ambiguous destination component binding",
    );
    const c = selected[0];
    if (kind === "dependency" && a.status === "supported") {
      const r = a.resolved ?? {};
      need(
        r.identity === c.identity && r.version === c.version,
        "snapshot dependency mismatch",
      );
    } else if (["model", "context"].includes(kind)) {
      const m = report.model_assessment;
      need(equal(m.target, c.model), "snapshot model mismatch");
      if (m.fit === "fits")
        need(
          m.tokenizer === c.tokenizer && m.input_limit === c.input_limit,
          "snapshot model budget mismatch",
        );
      if (kind === "model" && a.status === "supported")
        need(
          subset(plan.model_requirements.capabilities, c.capabilities) &&
            subset(plan.model_requirements.media_types, c.media_types),
          "snapshot model capability mismatch",
        );
    } else if (kind === "service" && a.status === "supported") {
      const r = a.resolved ?? {};
      need(
        ["account", "audience", "endpoint"].every((k) => equal(r[k], c[k])) &&
          subset(r.scopes ?? [], c.scopes) &&
          subset(r.secret_handles ?? [], c.secret_handles),
        "snapshot service mismatch",
      );
    } else if (kind === "workspace") {
      const workspace = doc.continuation.workspaces.find(
        (w: Obj) => w.id === a.subject.id,
      );
      need(c.root_id === workspace.root_id, "snapshot workspace root mismatch");
      const b = report.path_bindings.find((b: Obj) => b.root_id === c.root_id);
      need(
        b &&
          ["destination_path", "case_sensitive", "unicode_normalization"].every(
            (k) => b[k] === c[k],
          ),
        "snapshot workspace mismatch",
      );
    } else if (
      kind === "operation" &&
      a.status === "supported" &&
      plan.next_action.kind === "reconcile_operation"
    ) {
      const r = a.resolved ?? {};
      need(
        ["recovery_strategy", "external_identity"].every((k) =>
          equal(r[k], c[k]),
        ),
        "snapshot operation mismatch",
      );
    }
  }
  if (currentSnapshot !== undefined)
    need(
      currentSnapshot.equals(raw),
      "destination capabilities changed; reassessment required",
    );
  return currentSnapshot !== undefined;
}
