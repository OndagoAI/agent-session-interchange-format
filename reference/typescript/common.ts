/** Bounded input helpers. Dynamic records are checked by the bundled schemas before use. */
import * as fs from "node:fs";
import * as path from "node:path";
import { createHash } from "node:crypto";
export type Obj = Record<string, any>;
export const MAX_DOCUMENT = 16 * 1024 * 1024,
  MAX_RESOURCE = 64 * 1024 * 1024,
  MAX_TOTAL = 256 * 1024 * 1024,
  MAX_RECORDS = 20000,
  MAX_DEPTH = 128;
export class Invalid extends Error {}
export class Unsupported extends Invalid {}
export class SchemaInvalid extends Invalid {
  schema_path: string[];
  constructor(p: string[]) {
    super("schema validation failed");
    this.schema_path = p;
  }
}
export function need(value: unknown, message: string): asserts value {
  if (!value) throw new Invalid(message);
}
export const own = (o: Obj, k: string): boolean => Object.hasOwn(o, k);
export const hash = (b: Uint8Array, algorithm = "sha256"): string =>
  createHash(algorithm).update(b).digest("hex");
export const equal = (a: any, b: any): boolean => {
  if (a === b) return true;
  if (
    !a ||
    !b ||
    typeof a !== "object" ||
    typeof b !== "object" ||
    Array.isArray(a) !== Array.isArray(b)
  )
    return false;
  const keys = Object.keys(a);
  return (
    keys.length === Object.keys(b).length &&
    keys.every((k) => own(b, k) && equal(a[k], b[k]))
  );
};
export const subset = (a: Iterable<any>, b: Iterable<any>): boolean => {
  const set = new Set(b);
  return [...a].every((x) => set.has(x));
};
export const setEqual = (a: Iterable<any>, b: Iterable<any>): boolean =>
  subset(a, b) && subset(b, a);
export const object = (): Obj => Object.create(null);
export function utf8(raw: Uint8Array): string {
  try {
    return new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(
      raw,
    );
  } catch {
    throw new Invalid("invalid UTF-8");
  }
}
// Compare decimal values before accepting JavaScript's numeric representation.
function decimal(s: string): string {
  const m = /^(-?)(\d+)(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/.exec(s)!;
  let digits = (m[2] + (m[3] ?? "")).replace(/^0+/, "");
  if (!digits) return "0";
  let exponent = BigInt(m[4] ?? "0") - BigInt((m[3] ?? "").length);
  const stripped = digits.replace(/0+$/, "");
  exponent += BigInt(digits.length - stripped.length);
  digits = stripped;
  return m[1] + digits + "e" + exponent;
}
export function decode(raw: Uint8Array): any {
  need(raw.length <= MAX_DOCUMENT, "document byte limit");
  const text = utf8(raw);
  let i = 0,
    nodes = 0;
  const ws = () => {
    while (/[\x20\t\r\n]/.test(text[i] ?? "x")) i++;
  };
  function string(): string {
    const start = i++;
    while (i < text.length) {
      const c = text[i++];
      if (c === '"') {
        try {
          return JSON.parse(text.slice(start, i));
        } catch {
          throw new Invalid("invalid JSON string");
        }
      }
      if (c === "\\") i++;
    }
    throw new Invalid("invalid JSON string");
  }
  function value(depth: number): any {
    need(depth <= MAX_DEPTH, "JSON nesting limit");
    need(++nodes <= MAX_RECORDS * 100, "JSON node limit");
    ws();
    const c = text[i];
    if (c === '"') return string();
    if (c === "{") {
      i++;
      ws();
      const out = object();
      if (text[i] === "}") {
        i++;
        return out;
      }
      while (true) {
        ws();
        need(text[i] === '"', "invalid JSON object");
        const k = string();
        need(!own(out, k), "invalid JSON: duplicate JSON key");
        ws();
        need(text[i++] === ":", "invalid JSON object");
        out[k] = value(depth + 1);
        ws();
        const end = text[i++];
        if (end === "}") return out;
        need(end === ",", "invalid JSON object");
      }
    }
    if (c === "[") {
      i++;
      ws();
      const out: any[] = [];
      if (text[i] === "]") {
        i++;
        return out;
      }
      while (true) {
        out.push(value(depth + 1));
        ws();
        const end = text[i++];
        if (end === "]") return out;
        need(end === ",", "invalid JSON array");
      }
    }
    for (const [token, v] of [
      ["true", true],
      ["false", false],
      ["null", null],
    ] as const)
      if (text.startsWith(token, i)) {
        i += token.length;
        return v;
      }
    const m = /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/y;
    m.lastIndex = i;
    const match = m.exec(text);
    need(match, "invalid JSON value");
    i = m.lastIndex;
    const token = match[0];
    if (token.length > 4096)
      throw new Unsupported(
        "JSON numeric literal length exceeds 4096 characters",
      );
    const number = Number(token);
    if (
      !Number.isFinite(number) ||
      decimal(token) !== decimal(String(number)) ||
      (Number.isInteger(number) && !Number.isSafeInteger(number))
    )
      throw new Unsupported(
        "JSON number exceeds lossless JavaScript numeric range",
      );
    return number;
  }
  const out = value(0);
  ws();
  need(i === text.length, "invalid trailing JSON data");
  return out;
}
export const encode = (value: any): Buffer =>
  Buffer.from(JSON.stringify(value) + "\n");
export function read(file: string, limit = MAX_DOCUMENT): Buffer {
  const st = fs.lstatSync(file);
  need(!st.isSymbolicLink(), "symlink input");
  need(st.isFile(), "nonregular input");
  need(st.size <= limit, "input byte limit");
  const fd = fs.openSync(file, "r");
  try {
    const chunks: Buffer[] = [];
    let total = 0;
    while (true) {
      const b = Buffer.alloc(Math.min(65536, limit + 1 - total));
      const n = fs.readSync(fd, b, 0, b.length, null);
      if (!n) break;
      chunks.push(b.subarray(0, n));
      total += n;
      need(total <= limit, "input byte limit");
    }
    return Buffer.concat(chunks);
  } finally {
    fs.closeSync(fd);
  }
}
export function load(file: string): [Obj, Buffer] {
  const raw = read(file);
  return [decode(raw), raw];
}
export const lexists = (file: string): boolean => {
  try {
    fs.lstatSync(file);
    return true;
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw e;
  }
};
export function relative(name: string, empty = false): void {
  need(typeof name === "string" && (empty || name.length > 0), "empty path");
  if (name === "") return;
  need(
    [...name].length <= 4096 && !/[\\:]/.test(name) && !name.startsWith("/"),
    "unsafe path",
  );
  for (const p of name.split("/")) {
    need(!["", ".", ".."].includes(p) && !/[ .]$/.test(p), "unsafe path");
    need(!/[\x00-\x1f<>"|?*]/.test(p), "nonportable path");
    need(
      !/^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(p),
      "reserved device path",
    );
  }
}
export function contained(folder: string, name: string): string {
  relative(name);
  need(!fs.lstatSync(folder).isSymbolicLink(), "symlink root");
  let current = folder;
  for (const p of name.split("/")) {
    current = path.join(current, p);
    need(!fs.lstatSync(current).isSymbolicLink(), "symlink resource");
  }
  const rel = path.relative(fs.realpathSync(folder), fs.realpathSync(current));
  need(
    !rel.startsWith(".." + path.sep) && rel !== ".." && !path.isAbsolute(rel),
    "escaping resource",
  );
  return current;
}
export function unique(items: Obj[], key = "id"): Obj {
  need(items.length <= MAX_RECORDS, "record count limit");
  const out = object();
  for (const item of items) {
    need(!own(out, item[key]), "duplicate " + key);
    out[item[key]] = item;
  }
  return out;
}
export function pointer(value: any, selector: string): any {
  if (selector === "") return value;
  need(
    typeof selector === "string" && selector.startsWith("/"),
    "invalid JSON pointer",
  );
  for (let c of selector.slice(1).split("/")) {
    need(!/~(?![01])/.test(c), "invalid pointer escape");
    c = c.replaceAll("~1", "/").replaceAll("~0", "~");
    if (Array.isArray(value))
      need(/^(0|[1-9]\d*)$/.test(c), "invalid array selector");
    need(
      value !== null && typeof value === "object" && own(value, c),
      "pointer target missing",
    );
    value = value[c];
  }
  return value;
}
export function acyclic(edges: Record<string, string[]>, label: string): void {
  const parents = new Map(
      Object.entries(edges).map(([k, v]) => [k, new Set(v)]),
    ),
    children = new Map([...parents.keys()].map((k) => [k, [] as string[]]));
  for (const [k, values] of parents)
    for (const v of values) {
      need(parents.has(v), "missing " + label + " reference");
      children.get(v)!.push(k);
    }
  const ready = [...parents.keys()].filter((k) => !parents.get(k)!.size);
  let seen = 0;
  while (ready.length) {
    const k = ready.pop()!;
    seen++;
    for (const c of children.get(k)!) {
      parents.get(c)!.delete(k);
      if (!parents.get(c)!.size) ready.push(c);
    }
  }
  need(seen === parents.size, label + " cycle");
}
// Unicode case folding table is generated once from Python's Unicode data; no Python runtime is used.
const folds: Record<string, string> = JSON.parse(
  fs.readFileSync(new URL("./casefold.json", import.meta.url), "utf8"),
).mapping;
export const casefold = (s: string): string =>
  [...s].map((c) => folds[c] ?? c).join("");
export function base64(s: string): Buffer {
  need(
    typeof s === "string" &&
      /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(
        s,
      ),
    "invalid base64",
  );
  return Buffer.from(s, "base64");
}
export class Resources {
  records: Obj;
  cache = new Map<string, Buffer>();
  folder: string;
  constructor(document: Obj, folder: string) {
    this.records = unique(document.resources);
    this.folder = folder;
    let total = 0;
    const paths = new Map<string, string>();
    for (const [id, r] of Object.entries(this.records)) {
      if (r.availability !== "embedded") continue;
      let raw: Buffer;
      if (own(r, "text")) raw = Buffer.from(r.text);
      else if (own(r, "data")) {
        need(
          r.data.length <= Math.ceil(MAX_RESOURCE / 3) * 4,
          "base64 byte limit",
        );
        raw = base64(r.data);
      } else {
        raw = read(contained(folder, r.path), MAX_RESOURCE);
        const folded = casefold(r.path);
        need(
          !paths.has(folded) || paths.get(folded) === r.path,
          "resource path collision",
        );
        paths.set(folded, r.path);
      }
      need(raw.length <= MAX_RESOURCE, "resource byte limit");
      total += raw.length;
      need(total <= MAX_TOTAL, "resource total limit");
      need(
        raw.length === r.bytes && hash(raw) === r.sha256,
        "resource integrity",
      );
      this.cache.set(id, raw);
    }
  }
  ref(id: string): void {
    need(own(this.records, id), "missing resource reference");
  }
  bytes(id: string): Buffer {
    this.ref(id);
    need(this.cache.has(id), "resource bytes unavailable");
    return this.cache.get(id)!;
  }
}
