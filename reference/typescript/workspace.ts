import * as fs from "node:fs";
import * as path from "node:path";
import {
  type Obj,
  need,
  own,
  unique,
  acyclic,
  relative,
  Unsupported,
  Invalid,
  casefold,
  lexists,
  hash,
  subset,
  type Resources,
  object,
} from "./common.ts";
import type { Validated } from "./core.ts";
function matches(value: string, pattern: string): boolean {
  // Python fnmatch's slash-independent glob semantics; reject ambiguous bracket dialects.
  if (pattern.includes("[") || pattern.includes("]"))
    throw new Unsupported(
      "workspace bracket-glob selection is not implemented in TypeScript",
    );
  const expression = pattern
    .split("")
    .map((c) =>
      c === "*"
        ? ".*"
        : c === "?"
          ? "."
          : c.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
    )
    .join("");
  return new RegExp("^" + expression + "$", "su").test(value);
}
export function workspaceStates(profile: Obj): Obj {
  const records = unique(profile.workspaces),
    edges: Record<string, string[]> = object(),
    result = object();
  for (const [id, w] of Object.entries<Obj>(records))
    edges[id] = w.base_snapshot_id ? [w.base_snapshot_id] : [];
  acyclic(edges, "workspace base");
  const remaining = new Set(Object.keys(records));
  while (remaining.size)
    for (const id of [...remaining].filter(
      (id) => !edges[id].length || own(result, edges[id][0]),
    )) {
      const w = records[id],
        base = w.base_snapshot_id,
        entries = Object.assign(object(), base ? result[base] : {});
      if (base)
        need(
          records[base].root_id === w.root_id,
          "workspace base root mismatch",
        );
      for (const deletion of w.deletions) {
        relative(deletion);
        need(
          !w.selection.exclude.some(
            (p: string) =>
              matches(deletion, p) ||
              deletion === p.replace(/\/+$/, "") ||
              deletion.startsWith(p.replace(/\/+$/, "") + "/"),
          ),
          "deleting excluded path",
        );
        const targets = Object.keys(entries).filter(
          (p) => p === deletion || p.startsWith(deletion + "/"),
        );
        need(targets.length, "deletion absent from base");
        for (const p of targets) delete entries[p];
      }
      for (const entry of w.entries) {
        relative(entry.path);
        entries[entry.path] = entry;
      }
      for (const p of Object.keys(entries)) {
        const parts = p.split("/");
        for (let i = 1; i < parts.length; i++) {
          const parent = parts.slice(0, i).join("/");
          need(
            !own(entries, parent) || entries[parent].kind === "directory",
            "workspace file/directory collision",
          );
        }
      }
      result[id] = entries;
      remaining.delete(id);
    }
  return result;
}
export function checkGit(
  w: Obj,
  resources: Resources,
  dependencies: Obj,
): void {
  if (!w.git) return;
  const g = w.git;
  need(
    ["sha1", "sha256"].includes(g.object_format),
    "unsupported Git object format",
  );
  const length = g.object_format === "sha1" ? 40 : 64;
  const oid = (v: any) => {
    if (v !== null)
      need(
        typeof v === "string" && v.length === length && /^[0-9a-f]+$/.test(v),
        "invalid Git object ID",
      );
  };
  oid(g.head);
  const paths = new Map<string, Set<number>>();
  for (const e of g.index_entries) {
    relative(e.path);
    oid(e.object_id);
    const stages = paths.get(e.path) ?? new Set<number>();
    need(!stages.has(e.stage), "duplicate Git index stage");
    stages.add(e.stage);
    paths.set(e.path, stages);
    need(
      !(stages.has(0) && stages.size > 1),
      "mixed resolved/unmerged Git index",
    );
    need(
      ["100644", "100755", "120000", "160000"].includes(e.mode),
      "unsupported Git index mode",
    );
    need(
      e.resource_id !== null || e.object_id !== null,
      "Git index entry has no content",
    );
    if (e.resource_id) {
      resources.ref(e.resource_id);
      if (resources.cache.has(e.resource_id) && e.object_id) {
        const raw = resources.bytes(e.resource_id);
        need(
          hash(
            Buffer.concat([Buffer.from("blob " + raw.length + "\0"), raw]),
            g.object_format,
          ) === e.object_id,
          "Git index blob mismatch",
        );
      }
    }
  }
  for (const p of g.prerequisites) {
    oid(p.object_id);
    if (p.availability === "embedded")
      need(own(p, "resource_id"), "embedded Git prerequisite missing resource");
    if (own(p, "resource_id")) resources.ref(p.resource_id);
  }
  for (const s of g.submodules) {
    relative(s.path);
    oid(s.object_id);
    need(own(dependencies, s.dependency_id), "missing submodule dependency");
  }
  need(
    subset(g.lfs_dependency_ids, Object.keys(dependencies)),
    "missing LFS dependency",
  );
}
export function restore(
  doc: Obj,
  v: Validated,
  id: string,
  destination: string,
  options: {
    case_sensitive?: boolean;
    normalization?: string;
    fail_after?: number;
  } = {},
): Obj {
  const records = unique(doc.continuation.workspaces);
  need(own(records, id), "unknown workspace");
  const w = records[id],
    entries = workspaceStates(doc.continuation)[id],
    chain: Obj[] = [];
  let current = w;
  while (true) {
    chain.push(current);
    if (!current.base_snapshot_id) break;
    current = records[current.base_snapshot_id];
  }
  if (chain.some((x) => x.mode === "refs" || own(x, "git")))
    throw new Unsupported(
      "Git administration/index restoration is not implemented; use a verified Git adapter",
    );
  need(
    chain.every((x) => x.selection.complete_for_selection),
    "incomplete selected-tree snapshot",
  );
  const norm = options.normalization ?? "none";
  need(["none", "NFC", "NFD"].includes(norm), "unsupported normalization");
  const seen = new Map<string, string>();
  for (const [p, e] of Object.entries<Obj>(entries)) {
    if (e.kind === "symlink")
      throw new Unsupported(
        "workspace symlink restoration requires an explicit link policy",
      );
    relative(p);
    need(
      !p.split("/").some((c) => casefold(c) === ".git"),
      "workspace cannot inject Git administrative files",
    );
    let folded = norm === "none" ? p : p.normalize(norm);
    if (options.case_sensitive === false) folded = casefold(folded);
    need(!seen.has(folded), "destination path collision");
    seen.set(folded, e.kind);
    if (e.kind === "file") v.resources.bytes(e.resource_id);
  }
  for (const p of seen.keys()) {
    const parts = p.split("/");
    for (let i = 1; i < parts.length; i++)
      need(
        (seen.get(parts.slice(0, i).join("/")) ?? "directory") === "directory",
        "destination prefix collision",
      );
  }
  need(!lexists(destination), "destination already exists");
  const parent = path.dirname(destination);
  need(
    fs.statSync(parent).isDirectory() && !fs.lstatSync(parent).isSymbolicLink(),
    "destination parent must be a controlled directory",
  );
  const lock = path.join(
    parent,
    "." + path.basename(destination) + ".asif-lock",
  );
  fs.closeSync(fs.openSync(lock, "wx", 0o600));
  let staging: string | undefined,
    published = false;
  const cleanup = (p: string) => {
    fs.chmodSync(p, 0o700);
    for (const d of fs.readdirSync(p, { withFileTypes: true }))
      if (d.isDirectory()) cleanup(path.join(p, d.name));
  };
  try {
    need(!lexists(destination), "destination appeared before staging");
    staging = fs.mkdtempSync(
      path.join(parent, "." + path.basename(destination) + ".asif-stage-"),
    );
    let count = 0;
    const pairs = Object.entries<Obj>(entries).sort(
      ([a], [b]) =>
        a.split("/").length - b.split("/").length ||
        (a < b ? -1 : a > b ? 1 : 0),
    );
    for (const [p, e] of pairs) {
      const target = path.join(staging, p);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      if (e.kind === "directory") fs.mkdirSync(target, { recursive: true });
      else {
        const fd = fs.openSync(target, "wx");
        try {
          fs.writeFileSync(fd, v.resources.bytes(e.resource_id));
          fs.fsyncSync(fd);
        } finally {
          fs.closeSync(fd);
        }
        fs.chmodSync(target, e.mode);
      }
      count++;
      if (options.fail_after !== undefined && count >= options.fail_after)
        throw new Invalid("injected staging failure");
    }
    for (const [p, e] of pairs.reverse())
      if (e.kind === "directory") fs.chmodSync(path.join(staging, p), e.mode);
    need(!lexists(destination), "destination appeared before publication");
    fs.renameSync(staging, destination);
    published = true;
    return {
      status: "restored",
      workspace_id: id,
      entries: Object.keys(entries).length,
      destination,
      scope: "selected file tree; no native agent import",
    };
  } finally {
    if (staging && !published) {
      cleanup(staging);
      fs.rmSync(staging, { recursive: true, force: true });
    }
    fs.unlinkSync(lock);
  }
}
