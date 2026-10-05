import { test, after } from "node:test";
import assert from "node:assert/strict";
import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { run } from "../asif.ts";
import {
  type Obj,
  Invalid,
  Unsupported,
  SchemaInvalid,
  load,
  decode,
  encode,
  hash,
  pointer,
  relative,
  casefold,
  MAX_DOCUMENT,
} from "../reference/typescript/common.ts";
import {
  snapshotShape,
  validateDocument,
  historyState,
} from "../reference/typescript/core.ts";
import {
  inspectSession,
  inspectReport,
  date,
} from "../reference/typescript/continuation.ts";
import { restore, workspaceStates } from "../reference/typescript/workspace.ts";
import {
  predicate,
  resolveConfiguration,
  evaluatePolicy,
  reconstructRequest,
} from "../reference/typescript/context.ts";
import {
  packageBytes,
  inspectPackage,
  signature,
  verifySignature,
  zipStored,
} from "../reference/typescript/package.ts";
import { audit } from "../reference/typescript/redaction.ts";
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), ".."),
  folder = path.join(ROOT, "examples/continuation"),
  source = path.join(folder, "another-computer.session.json");
const [doc, raw] = load(source),
  v = validateDocument(doc, folder),
  temp = fs.mkdtempSync(path.join(os.tmpdir(), "asif-ts-")),
  results: Obj[] = [];
const check = (name: string, fn: () => void) =>
  test(name, () => {
    try {
      fn();
      results.push({ case: name, passed: true });
    } catch (error) {
      results.push({ case: name, passed: false });
      throw error;
    }
  });
const rejects = (fn: () => any, pattern: RegExp) => assert.throws(fn, pattern);
after(() => {
  fs.rmSync(temp, { recursive: true, force: true });
  fs.writeFileSync(
    path.join(ROOT, "tests/typescript-results.json"),
    JSON.stringify(
      {
        asif_version: "0.5",
        scope:
          "Local TypeScript port, shared Python expectations, CLI and package checks",
        checks: results.length,
        passed: results.filter((r) => r.passed).length,
        node_version: process.version,
        independent_implementations: 0,
        real_runtime_tests: 0,
        results,
      },
      null,
      2,
    ) + "\n",
  );
});
for (const location of ["examples", "examples/continuation"])
  for (const file of fs
    .readdirSync(path.join(ROOT, location))
    .filter((f) => f.endsWith(".session.json")))
    check("core fixture " + file, () => {
      const filePath = path.join(ROOT, location, file);
      validateDocument(load(filePath)[0], path.dirname(filePath));
    });
const corpus = JSON.parse(
  fs.readFileSync(
    path.join(ROOT, "tests/typescript-parity-cases.json"),
    "utf8",
  ),
);
const progression = JSON.parse(
  fs.readFileSync(
    path.join(ROOT, "tests/tool-call-progression-cases.json"),
    "utf8",
  ),
);
const taskCases = JSON.parse(
  fs.readFileSync(path.join(ROOT, "tests/task-semantics-cases.json"), "utf8"),
);
for (const group of [
  { name: "call progression", cases: progression.cases },
  { name: "task semantics", cases: taskCases.cases },
])
  for (const item of group.cases)
    check(group.name + ": " + item.name, () => {
      const d = load(path.join(ROOT, "examples", item.fixture))[0];
      for (const edit of item.edits) {
        let target = d;
        for (const key of edit.path.slice(0, -1)) target = target[key];
        const key = edit.path.at(-1);
        if (edit.remove) {
          if (Array.isArray(target)) target.splice(Number(key), 1);
          else delete target[key];
        } else target[key] = structuredClone(edit.value);
      }
      if (item.schema_error) {
        assert.throws(
          () => validateDocument(d, path.join(ROOT, "examples")),
          SchemaInvalid,
        );
      } else if (item.error) {
        assert.throws(
          () => validateDocument(d, path.join(ROOT, "examples")),
          (error) =>
            error instanceof Invalid && error.message.includes(item.error),
        );
      } else {
        const validated = validateDocument(d, path.join(ROOT, "examples"));
        if (item.task_states) {
          const partial =
            d.coverage.find((c: Obj) => c.scope === "tasks").status ===
            "partial";
          for (const branch of d.branches) {
            if (!Object.hasOwn(item.task_states, branch.id)) continue;
            const state = historyState(
              branch.event_ids.map(
                (id: string) => validated.collections.events[id],
              ),
              {},
              {},
              partial,
            );
            const actual = {
              tasks: Object.fromEntries(
                Object.entries<Obj>(state.tasks).map(([id, task]) => [
                  id,
                  { revision: task.revision, status: task.status },
                ]),
              ),
              task_dependencies: state.task_dependencies,
              task_history_gaps: state.task_history_gaps,
            };
            assert.deepEqual(
              JSON.parse(JSON.stringify(actual)),
              item.task_states[branch.id],
            );
          }
          return;
        }
        const externalCalls = Object.fromEntries(
          (d.external_bindings ?? [])
            .filter((b: Obj) => b.kind === "call")
            .map((b: Obj) => [b.id, b.descriptor]),
        );
        const state = historyState(
          d.branches[0].event_ids.map(
            (id: string) => validated.collections.events[id],
          ),
          externalCalls,
        );
        const actual = {
          calls: Object.fromEntries(
            Object.entries<Obj>(state.calls).map(([id, call]) => [
              id,
              {
                arguments: call.arguments,
                arguments_status: call.arguments_status,
              },
            ]),
          ),
          closed_calls: state.closed_calls,
        };
        assert.deepEqual(JSON.parse(JSON.stringify(actual)), item.expected);
      }
    });
check("call progression retains immutable evidence across captures", () => {
  const partial = load(
    path.join(ROOT, "examples/tool-call-partial.session.json"),
  )[0];
  const completed = load(
    path.join(ROOT, "examples/tool-call-completed.session.json"),
  )[0];
  assert.equal(partial.session.id, completed.session.id);
  assert.notEqual(partial.capture.id, completed.capture.id);
  for (const collection of ["events", "resources", "streams", "contexts"])
    for (const record of partial[collection])
      assert.deepEqual(
        completed[collection].find((r: Obj) => r.id === record.id),
        record,
      );
  const validated = validateDocument(completed, path.join(ROOT, "examples"));
  const inputs = reconstructRequest(
    completed,
    validated,
    "context-completed",
  ).inputs;
  const calls = inputs.filter((item: Obj) => item.kind === "tool_call");
  assert.equal(calls.length, 1);
  assert.deepEqual(JSON.parse(JSON.stringify(calls[0].arguments)), {
    document_id: "meeting-42",
  });
  assert.deepEqual(JSON.parse(JSON.stringify(calls[0].source_events)), [
    { event_id: "call-complete" },
  ]);
});
const snapshotVectors = JSON.parse(
  fs.readFileSync(
    path.join(ROOT, "tests/capability-snapshot-vectors.json"),
    "utf8",
  ),
);
for (const vector of snapshotVectors.vectors)
  check("capability hash vector: " + vector.name, () => {
    const raw = Buffer.from(vector.utf8, "utf8");
    assert.equal(raw.length, vector.bytes);
    assert.equal(hash(raw), vector.sha256);
    snapshotShape(decode(raw));
  });
for (const item of corpus.cases)
  check("Python parity: " + item.name, () => {
    const execute = () =>
      item.kind === "session"
        ? inspectSession(item.document, path.join(ROOT, item.folder))
        : inspectReport(
            item.document,
            Buffer.from(item.raw, "base64"),
            item.report,
            path.join(ROOT, item.folder),
            date(item.now),
            undefined,
            item.current_snapshot
              ? Buffer.from(item.current_snapshot, "base64")
              : undefined,
          );
    if (item.expected.accepted)
      assert.deepEqual(
        JSON.parse(JSON.stringify(execute())),
        item.expected.result,
      );
    else
      assert.throws(execute, (e) =>
        item.expected.schema_error
          ? e instanceof SchemaInvalid
          : item.expected.unsupported
            ? e instanceof Unsupported
            : e instanceof Invalid &&
              !(e instanceof SchemaInvalid) &&
              !(e instanceof Unsupported),
      );
  });
check("strict parser duplicate keys", () =>
  rejects(() => decode(Buffer.from('{"a":1,"a":2}')), /duplicate JSON key/),
);
check("strict parser invalid syntax and constants", () => {
  for (const s of [
    "NaN",
    "Infinity",
    "[1,]",
    '{"a":1,}',
    "01",
    "true false",
    "\ufeff{}",
  ])
    rejects(() => decode(Buffer.from(s)), /invalid/);
});
check("strict UTF-8", () =>
  rejects(() => decode(Buffer.from([0xff])), /UTF-8/),
);
check("bounded parser nesting and bytes", () => {
  rejects(
    () => decode(Buffer.from("[".repeat(130) + "0" + "]".repeat(130))),
    /nesting limit/,
  );
  rejects(() => decode(Buffer.alloc(MAX_DOCUMENT + 1)), /byte limit/);
});
check("lossy number refusal is explicit", () => {
  for (const s of [
    "9007199254740993",
    "1e400",
    "0.123456789012345678901234567890",
  ])
    assert.throws(() => decode(Buffer.from(s)), Unsupported);
  assert.equal(decode(Buffer.from("0.2")), 0.2);
  assert.equal(decode(Buffer.from("1e2")), 100);
});
check("prototype names are inert", () => {
  const parsed = decode(
    Buffer.from('{"__proto__":{"polluted":true},"constructor":2}'),
  );
  assert.equal(Object.getPrototypeOf(parsed), null);
  assert.equal(({} as Obj).polluted, undefined);
  assert.equal(parsed.constructor, 2);
});
check("pointer escape validation", () => {
  assert.equal(pointer({ "a/b": { "~": [2] } }, "/a~1b/~0/0"), 2);
  rejects(() => pointer({}, "/a~2"), /invalid pointer escape/);
  rejects(() => pointer([1], "/01"), /invalid array selector/);
});
check("portable path refusal", () => {
  for (const p of ["../a", "/tmp/a", "a\\b", "C:a", "NUL", "a/../b", "a."])
    rejects(() => relative(p), /path/);
});
check("Unicode case folding", () => {
  assert.equal(casefold("Straße"), casefold("STRASSE"));
  assert.equal(casefold("Σς"), casefold("σσ"));
});
check("typed request preserves model input", () =>
  assert.deepEqual(
    reconstructRequest(doc, v, doc.contexts[0].id).inputs,
    structuredClone(doc.contexts[0].inputs),
  ),
);
check("configuration effective order", () =>
  assert.deepEqual(
    resolveConfiguration(doc, doc.configurations[0].id, {
      root_id: doc.continuation.workspaces[0].root_id,
      relative_path: "",
    }).instruction_ids,
    doc.continuation.configuration_bindings[0].effective_order,
  ),
);
check("predicates and unsupported dialect", () => {
  assert.equal(
    predicate({ path_prefix: "src" }, { relative_path: "src-other/file" }),
    false,
  );
  assert.equal(
    predicate(
      {
        all: [{ event_kind_in: ["tool_call"] }, { not: { root_is: "other" } }],
      },
      { event_kind: "tool_call", root_id: "work" },
    ),
    true,
  );
  assert.throws(() => predicate({ execute: "code" }, {}), Unsupported);
});
check("policy deny and default ask", () => {
  const policy = (effect: string) => ({
    id: effect,
    type: "asif.policy/0.1",
    enforcing: true,
    definition: {
      effect,
      tool_ids: ["*"],
      scope: { kind: "global" },
      activation: { kind: "always" },
    },
  });
  assert.equal(
    evaluatePolicy({ policies: [policy("allow"), policy("deny")] }, {})
      .decision,
    "deny",
  );
  assert.equal(evaluatePolicy({ policies: [] }, {}).decision, "ask");
});
const event = (id: string, kind: string, data: Obj, extra: Obj = {}) => ({
  id,
  kind,
  data,
  ...extra,
});
check("decision corrections preserve evidence", () => {
  const q = event("q", "decision_request", { request_id: "q", options: [] }),
    a = event("a", "decision_resolution", {
      request_id: "q",
      outcome: "allowed",
    }),
    b = event("b", "decision_resolution", {
      request_id: "q",
      outcome: "denied",
    });
  rejects(() => historyState([q, a, b]), /contradictory decision/);
  assert.equal(
    historyState([q, a, { ...b, supersedes: { event_id: "a" } }]).decisions.q
      .outcome,
    "denied",
  );
});
check("task reopen requires reason", () => {
  const t = event("t1", "task_update", {
      task_id: "task",
      revision: 1,
      status: "completed",
    }),
    reopen = {
      task_id: "task",
      revision: 2,
      previous_revision: 1,
      status: "pending",
    };
  rejects(
    () => historyState([t, event("t2", "task_update", reopen)]),
    /reopen reason/,
  );
  historyState([
    t,
    event("t2", "task_update", { ...reopen, reopen_reason: "New work" }),
  ]);
});
check("terminal result cannot reopen", () => {
  const c = event("c", "tool_call", { call_id: "c" }),
    r = { call_id: "c", result_index: 0, terminal: true, outcome: "success" };
  rejects(
    () =>
      historyState([
        c,
        event("r", "tool_result", r),
        event("r2", "tool_result", { ...r, result_index: 1 }),
      ]),
    /after terminal/,
  );
});
function streamDoc(): Obj {
  const d = structuredClone(doc),
    e = d.events.find((e: Obj) => e.kind === "tool_call"),
    bytes = encode(e.data.arguments);
  d.resources.push({
    id: "stream-bytes",
    media_type: "application/json",
    purpose: "native",
    availability: "embedded",
    text: bytes.toString(),
    bytes: bytes.length,
    sha256: hash(bytes),
  });
  d.coverage.find((c: Obj) => c.scope === "native").status = "complete";
  d.required_features.push("asif.streams/0.1");
  d.streams = [
    {
      id: "s",
      kind: "tool_arguments",
      event_id: e.id,
      call_id: e.data.call_id,
      status: "complete",
      segments: [
        {
          index: 0,
          resource_id: "stream-bytes",
          offset: 0,
          length: 3,
          terminal: false,
        },
        {
          index: 1,
          resource_id: "stream-bytes",
          offset: 3,
          length: bytes.length - 3,
          terminal: true,
        },
      ],
    },
  ];
  return d;
}
check("stream assembly and missing fragment refusal", () => {
  const d = streamDoc();
  assert.equal(validateDocument(d, folder).streams.s.status, "complete");
  d.streams[0].segments[1].index = 2;
  rejects(() => validateDocument(d, folder), /completeness mismatch/);
});
check("missing actor and provenance span", () => {
  const d = structuredClone(doc);
  d.events[0].actor_id = "absent";
  rejects(() => validateDocument(d, folder), /missing actor/);
  d.events[0].actor_id = doc.events[0].actor_id;
  d.events[0].provenance.sources = [
    {
      resource_id: d.resources[0].id,
      locator: { syntax: "bytes", offset: 999999, length: 1 },
    },
  ];
  rejects(() => validateDocument(d, folder), /source span outside/);
});
check("restore bytes modes and no overwrite", () => {
  const w = doc.continuation.workspaces[0],
    destination = path.join(temp, "restored");
  restore(doc, v, w.id, destination);
  for (const e of w.entries)
    if (e.kind === "file") {
      assert.deepEqual(
        fs.readFileSync(path.join(destination, e.path)),
        v.resources.bytes(e.resource_id),
      );
      assert.equal(
        fs.statSync(path.join(destination, e.path)).mode & 0o777,
        e.mode,
      );
    }
  rejects(() => restore(doc, v, w.id, destination), /already exists/);
});
check("restore failure rolls back", () => {
  rejects(
    () =>
      restore(
        doc,
        v,
        doc.continuation.workspaces[0].id,
        path.join(temp, "failed"),
        { fail_after: 1 },
      ),
    /injected staging/,
  );
  assert.ok(!fs.readdirSync(temp).some((n) => n.includes("failed")));
});
check("workspace delta explicit deletion", () => {
  const w = doc.continuation.workspaces[0],
    delta = {
      ...structuredClone(w),
      id: "delta",
      mode: "delta",
      base_snapshot_id: w.id,
      entries: [],
      deletions: [w.entries[0].path],
    };
  assert.ok(
    !Object.hasOwn(
      workspaceStates({ workspaces: [w, delta] }).delta,
      w.entries[0].path,
    ),
  );
  delta.deletions = ["absent"];
  rejects(
    () => workspaceStates({ workspaces: [w, delta] }),
    /absent from base/,
  );
});
check("restore case and normalization collision", () => {
  const d = structuredClone(doc),
    w = d.continuation.workspaces[0];
  w.entries.push({ ...w.entries[0], path: w.entries[0].path.toUpperCase() });
  rejects(
    () =>
      restore(d, v, w.id, path.join(temp, "case"), { case_sensitive: false }),
    /path collision/,
  );
  w.entries = [
    { ...w.entries[0], path: "é.txt" },
    { ...w.entries[0], path: "e\u0301.txt" },
  ];
  rejects(
    () =>
      restore(d, v, w.id, path.join(temp, "unicode"), { normalization: "NFC" }),
    /path collision/,
  );
});
check("symlink input refusal", () => {
  const link = path.join(temp, "link.json");
  fs.symlinkSync(source, link);
  rejects(() => load(link), /symlink input/);
});
const imageSource = path.join(ROOT, "examples/image-and-document.session.json"),
  packed = packageBytes(imageSource),
  key = Buffer.from(Array.from({ length: 32 }, (_, i) => i)),
  publicKey = fs.readFileSync(
    path.join(ROOT, "examples/package-test-public.key"),
  );
check("deterministic package matches Python fixture", () => {
  assert.deepEqual(packed, packageBytes(imageSource));
  assert.deepEqual(
    packed,
    fs.readFileSync(path.join(ROOT, "examples/package-example.asif.zip")),
  );
  assert.deepEqual(
    inspectPackage(packed).get("session.json"),
    fs.readFileSync(imageSource),
  );
});
check("Python signature verifies in TypeScript", () =>
  assert.equal(
    verifySignature(
      packed,
      fs.readFileSync(path.join(ROOT, "examples/package-signature.json")),
      publicKey,
    ).status,
    "verified",
  ),
);
check("TypeScript signature matches Python signature", () =>
  assert.deepEqual(
    signature(packed, key),
    fs.readFileSync(path.join(ROOT, "examples/package-signature.json")),
  ),
);
check("wrong key and tampered signature rejected", () => {
  rejects(
    () => verifySignature(packed, signature(packed, key), Buffer.alloc(32)),
    /untrusted signing key/,
  );
  const sig = JSON.parse(signature(packed, key).toString());
  sig.signature = Buffer.alloc(64).toString("base64");
  rejects(
    () => verifySignature(packed, encode(sig), publicKey),
    /invalid package signature/,
  );
});
check("package tamper and traversal rejected", () => {
  const files = inspectPackage(packed);
  files.set("session.json", Buffer.from("{}"));
  rejects(() => inspectPackage(zipStored(files)), /inventory length mismatch/);
  files.delete("session.json");
  files.set("../outside", Buffer.alloc(0));
  rejects(() => inspectPackage(zipStored(files)), /unsafe path/);
});
check("ZIP bounds, flags, CRC and duplicate names rejected", () => {
  for (const field of [
    "truncated",
    "encrypted",
    "compression",
    "crc",
    "descriptor",
    "zip64",
  ]) {
    const b = Buffer.from(packed);
    let input = b;
    if (field === "truncated") input = b.subarray(0, -1);
    else if (field === "zip64") b.writeUInt16LE(65535, b.length - 12);
    else {
      const c = b.indexOf(Buffer.from("504b0102", "hex"));
      if (field === "encrypted") b.writeUInt16LE(1, c + 8);
      if (field === "compression") b.writeUInt16LE(8, c + 10);
      if (field === "crc") b[40] ^= 1;
      if (field === "descriptor") b.writeUInt16LE(8, c + 8);
    }
    assert.throws(() => inspectPackage(input), Invalid);
  }
  const f = inspectPackage(packed);
  f.set("SESSION.JSON", f.get("session.json")!);
  rejects(() => inspectPackage(zipStored(f)), /colliding package member/);
});
check("redaction duplicates and base64 do not echo values", () => {
  const d = structuredClone(doc);
  d.secret = "needle";
  d.encoded = Buffer.from("needle").toString("base64");
  d.needle = { needle: "needle" };
  const result = audit(encode(d), v, ["needle"]);
  assert.equal(result.status, "matches_found");
  assert.ok(!JSON.stringify(result).includes("needle"));
  assert.ok(result.findings.some((f: Obj) => f.location.endsWith("/base64")));
});
check("all nine CLI commands and exit statuses", () => {
  assert.equal(run(["validate", source]).code, 0);
  assert.equal(
    run([
      "validate-report",
      source,
      path.join(folder, "another-computer.report.json"),
      "--at",
      "2026-09-26T12:30:00Z",
    ]).code,
    0,
  );
  assert.equal(run(["request", source, doc.contexts[0].id]).code, 0);
  assert.equal(
    run([
      "restore-workspace",
      source,
      doc.continuation.workspaces[0].id,
      path.join(temp, "cli-restore"),
    ]).code,
    0,
  );
  const zip = path.join(temp, "cli.zip"),
    sig = path.join(temp, "cli.sig.json"),
    privateFile = path.join(temp, "test.key"),
    patterns = path.join(temp, "patterns.json");
  fs.writeFileSync(privateFile, key);
  fs.writeFileSync(patterns, encode(["asif_version"]));
  assert.equal(run(["pack", imageSource, zip]).code, 0);
  assert.equal(run(["verify-package", zip]).code, 0);
  assert.equal(
    run(["sign", zip, "--private-key", privateFile, "--output", sig]).code,
    0,
  );
  assert.equal(
    run([
      "verify-signature",
      zip,
      "--signature",
      sig,
      "--trusted-public-key",
      path.join(ROOT, "examples/package-test-public.key"),
    ]).code,
    0,
  );
  assert.equal(
    run(["audit-redaction", source, "--patterns", patterns]).code,
    1,
  );
  assert.equal(run(["pack", imageSource, zip]).code, 2);
  assert.equal(run(["validate", source, "--unknown"]).code, 2);
  const changed = structuredClone(doc);
  changed.required_features.push("example.unknown/1");
  const changedFile = path.join(temp, "unknown.json");
  fs.writeFileSync(changedFile, encode(changed));
  assert.equal(run(["validate", changedFile]).code, 3);
});
check("CLI works outside the project directory", () => {
  const result = spawnSync(
    process.execPath,
    [path.join(ROOT, "asif.ts"), "validate", imageSource],
    { cwd: temp, encoding: "utf8" },
  );
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).status, "checked");
});

check("prototype-like entity IDs remain valid", () => {
  const d = structuredClone(doc);
  const old = d.participants[0].id;
  d.participants[0].id = "__proto__";
  for (const e of d.events) if (e.actor_id === old) e.actor_id = "__proto__";
  for (const e of d.executions)
    if (e.participant_id === old) e.participant_id = "__proto__";
  validateDocument(d, folder);
});
