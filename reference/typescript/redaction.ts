import { type Obj, need, decode, MAX_RESOURCE, base64 } from "./common.ts";
import type { Validated } from "./core.ts";
export function audit(raw: Buffer, v: Validated, patterns: string[]): Obj {
  need(
    Array.isArray(patterns) &&
      patterns.length &&
      patterns.every((x) => typeof x === "string" && x.length),
    "nonempty redaction patterns required",
  );
  const needles = patterns.map((x) => Buffer.from(x)),
    findings: Obj[] = [];
  const inspect = (content: Buffer, location: string) => {
    const hits = needles.flatMap((n, i) => (content.includes(n) ? [i] : []));
    if (hits.length) findings.push({ location, pattern_indexes: hits });
  };
  inspect(raw, "document/raw");
  const stack: [any, string][] = [[decode(raw), "document"]];
  while (stack.length) {
    const [value, where] = stack.pop()!;
    if (Array.isArray(value))
      value.forEach((child, i) => stack.push([child, where + "/" + i]));
    else if (value && typeof value === "object")
      Object.entries(value).forEach(([key, child], i) => {
        inspect(Buffer.from(key), where + "/key-index/" + i);
        stack.push([child, where + "/value-index/" + i]);
      });
    else if (typeof value === "string") {
      inspect(Buffer.from(value), where);
      if (value.length <= Math.ceil(MAX_RESOURCE / 3) * 4)
        try {
          inspect(base64(value), where + "/base64");
        } catch {
          /* Not base64 content. */
        }
    }
  }
  let i = 0;
  for (const content of v.resources.cache.values())
    inspect(content, "resource-index/" + i++);
  return {
    status: findings.length ? "matches_found" : "no_exact_matches",
    findings,
    scope:
      "supplied patterns in raw/decoded JSON and available resource bytes; no discovery, compressed-media or OCR claim",
  };
}
