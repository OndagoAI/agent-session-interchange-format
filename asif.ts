#!/usr/bin/env node
/** Standalone TypeScript companion to asif.py. No Python subprocesses or agent execution. */
import * as path from "node:path";
import { pathToFileURL } from "node:url";
import {
  type Obj,
  Invalid,
  Unsupported,
  SchemaInvalid,
  load,
  read,
  encode,
  need,
  MAX_TOTAL,
  MAX_DOCUMENT,
} from "./reference/typescript/common.ts";
import { validateDocument } from "./reference/typescript/core.ts";
import {
  inspectSession,
  inspectReport,
  date,
} from "./reference/typescript/continuation.ts";
import { reconstructRequest } from "./reference/typescript/context.ts";
import { restore } from "./reference/typescript/workspace.ts";
import { audit } from "./reference/typescript/redaction.ts";
import {
  packageBytes,
  inspectPackage,
  signature,
  verifySignature,
  writeNew,
} from "./reference/typescript/package.ts";
const commands: Record<
  string,
  { count: number; options?: string[]; required?: string[] }
> = {
  validate: { count: 1 },
  request: { count: 2 },
  "restore-workspace": {
    count: 3,
    options: ["--case-insensitive", "--normalization"],
  },
  "audit-redaction": {
    count: 1,
    options: ["--patterns"],
    required: ["--patterns"],
  },
  "validate-report": { count: 2, options: ["--at", "--current-capabilities"] },
  pack: { count: 2 },
  "verify-package": { count: 1 },
  sign: {
    count: 1,
    options: ["--private-key", "--output"],
    required: ["--private-key", "--output"],
  },
  "verify-signature": {
    count: 1,
    options: ["--signature", "--trusted-public-key"],
    required: ["--signature", "--trusted-public-key"],
  },
};
const HELP = `ASIF 0.3 TypeScript reference (Node.js 24+)\n\nUsage: node asif.ts <command> [arguments]\n\n  validate <session>\n  validate-report <session> <report> [--at <ISO timestamp>] [--current-capabilities <snapshot>]\n  request <session> <context_id>\n  restore-workspace <session> <workspace_id> <destination> [--case-insensitive] [--normalization none|NFC|NFD]\n  audit-redaction <session> --patterns <JSON file>\n  pack <session> <output>\n  verify-package <package>\n  sign <package> --private-key <raw key> --output <signature file>\n  verify-signature <package> --signature <file> --trusted-public-key <raw key>\n\nJSON output; exit 0 checked/completed, 1 redaction matches, 2 invalid/failure, 3 unsupported.\n`;
export function run(argv: string[]): {
  code: number;
  result?: Obj;
  help?: string;
} {
  if (!argv.length || argv[0] === "--help" || argv[0] === "-h")
    return { code: 0, help: HELP };
  try {
    const [command, ...args] = argv;
    need(Object.hasOwn(commands, command), "unknown command");
    if (args.includes("--help") || args.includes("-h"))
      return { code: 0, help: HELP };
    const def = commands[command],
      pos: string[] = [],
      opts: Record<string, string | boolean> = Object.create(null);
    let literal = false;
    for (let i = 0; i < args.length; i++) {
      const a = args[i];
      if (a === "--" && !literal) {
        literal = true;
        continue;
      }
      if (!literal && a.startsWith("-")) {
        need(def.options?.includes(a), "unknown option");
        need(!Object.hasOwn(opts, a), "duplicate option");
        if (a === "--case-insensitive") opts[a] = true;
        else {
          need(
            i + 1 < args.length && !args[i + 1].startsWith("--"),
            "missing option value",
          );
          opts[a] = args[++i];
        }
      } else pos.push(a);
    }
    need(pos.length === def.count, "wrong number of arguments");
    for (const key of def.required ?? [])
      need(Object.hasOwn(opts, key), "missing required option");
    const option = (name: string) => opts[name] as string;
    let result: Obj;
    if (
      ["pack", "verify-package", "sign", "verify-signature"].includes(command)
    ) {
      if (command === "pack") {
        const raw = packageBytes(pos[0]);
        inspectPackage(raw);
        writeNew(pos[1], raw);
        result = { status: "packed", bytes: raw.length, output: pos[1] };
      } else {
        const raw = read(pos[0], MAX_TOTAL + MAX_DOCUMENT);
        if (command === "verify-package")
          result = {
            status: "integrity_verified",
            members: inspectPackage(raw).size,
            scope:
              "container, inventory, session shape and file-backed resource integrity; no authenticity or continuation claim",
          };
        else if (command === "sign") {
          writeNew(
            option("--output"),
            signature(raw, read(option("--private-key"), 32)),
          );
          result = { status: "signed", output: option("--output") };
        } else
          result = verifySignature(
            raw,
            read(option("--signature")),
            read(option("--trusted-public-key"), 32),
          );
      }
    } else {
      const [doc, raw] = load(pos[0]),
        folder = path.dirname(pos[0]),
        v = validateDocument(doc, folder);
      if (doc.continuation) inspectSession(doc, folder, v);
      if (command === "validate")
        result = {
          status: "checked",
          scope:
            "structure and implemented semantic checks; not full conformance",
          unsupported_features: v.unsupported_features,
          streams: v.streams,
          operational_authorization: false,
        };
      else if (command === "validate-report")
        result = inspectReport(
          doc,
          raw,
          load(pos[1])[0],
          folder,
          opts["--at"] ? date(option("--at")) : Date.now(),
          v,
          opts["--current-capabilities"]
            ? read(option("--current-capabilities"), 1024 * 1024)
            : undefined,
        );
      else if (command === "request")
        result = reconstructRequest(doc, v, pos[1]);
      else if (command === "restore-workspace") {
        need(doc.continuation, "continuation profile absent");
        if (v.unsupported_features.length)
          throw new Unsupported("required feature unsupported");
        result = restore(doc, v, pos[1], pos[2], {
          case_sensitive: !opts["--case-insensitive"],
          normalization: option("--normalization") ?? "none",
        });
      } else
        result = audit(
          raw,
          v,
          load(option("--patterns"))[0] as unknown as string[],
        );
    }
    return {
      code:
        command === "validate" && result.unsupported_features.length
          ? 3
          : command === "audit-redaction" && result.findings.length
            ? 1
            : 0,
      result,
    };
  } catch (e) {
    if (e instanceof Unsupported)
      return { code: 3, result: { status: "unsupported", reason: e.message } };
    if (e instanceof SchemaInvalid)
      return {
        code: 2,
        result: {
          status: "invalid",
          reason: e.message,
          schema_path: e.schema_path,
        },
      };
    return {
      code: 2,
      result: {
        status: "invalid",
        reason: e instanceof Invalid ? e.message : "operation failed",
      },
    };
  }
}
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  const output = run(process.argv.slice(2));
  if (output.help) process.stdout.write(output.help);
  else process.stdout.write(encode(output.result));
  process.exitCode = output.code;
}
