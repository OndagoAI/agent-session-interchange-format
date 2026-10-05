# ASIF local reference implementations

ASIF **0.3** includes locally authored [Python](asif.py) and [TypeScript](asif.ts) reference CLIs implementing a documented subset. Both are vendor-neutral and expose the same nine commands. The TypeScript CLI runs directly on Node.js without invoking Python. Neither imports native agent stores, encodes provider requests, obtains credentials, calls external services or executes an agent. The two implementations share authorship and do not count as independent interoperability evidence.

## Installation and commands

### Python

Python 3.11 or newer is required. Dependencies are pinned in [requirements.txt](requirements.txt).

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python asif.py validate examples/image-and-document.session.json
.venv/bin/python asif.py validate-report examples/continuation/another-computer.session.json examples/continuation/another-computer.report.json --at 2026-09-26T12:30:00Z
.venv/bin/python asif.py request examples/continuation/another-computer.session.json continue-context
.venv/bin/python asif.py pack examples/image-and-document.session.json /tmp/asif-example.zip
.venv/bin/python asif.py verify-package /tmp/asif-example.zip
```

### TypeScript

Requires Node.js 24 or newer with `node` and `npm` on PATH. Dependencies are pinned in [package-lock.json](package-lock.json). Node runs the `.ts` sources directly using its [built-in TypeScript support](https://nodejs.org/api/typescript.html); type checking is a separate command.

```sh
npm ci
npm run typecheck
node asif.ts --help
node asif.ts validate examples/image-and-document.session.json
node asif.ts validate-report examples/continuation/another-computer.session.json examples/continuation/another-computer.report.json --at 2026-09-26T12:30:00Z
node asif.ts request examples/continuation/another-computer.session.json continue-context
node asif.ts restore-workspace examples/continuation/another-computer.session.json workspace-head /tmp/asif-ts-restored
node asif.ts pack examples/image-and-document.session.json /tmp/asif-ts-example.zip
node asif.ts verify-package /tmp/asif-ts-example.zip
node asif.ts sign /tmp/asif-ts-example.zip --private-key /path/to/private.key --output /tmp/asif-ts-example.sig.json
node asif.ts verify-signature /tmp/asif-ts-example.zip --signature /tmp/asif-ts-example.sig.json --trusted-public-key /path/to/trusted-public.key
node asif.ts audit-redaction examples/redacted-attachment.session.json --patterns /path/to/patterns.json
```

The key and pattern paths above are caller-supplied files, as described below. Package/signature output paths and restore destinations must be new. `npm run asif -- <command> ...` is an alternative to `node asif.ts <command> ...`. Read-only commands can run from another working directory when given absolute input paths.

### Shared command contract

Use the context and workspace IDs recorded in the document. Output is JSON. Exit codes: `0` for completed checks, `1` for exact redaction matches, `2` for invalid input or an operation failure, and `3` for unsupported semantics. A successful check is limited to the reported scope, not full conformance.

## Implemented checks and operations

| Area | Implemented | Limits |
|---|---|---|
| Parsing | Bounded UTF-8 JSON and duplicate-key rejection; Python preserves decimal values, while TypeScript refuses numbers outside its supported exact round-trip range. | No unbounded-size or streaming parser claim. See language differences below. |
| Core semantics | IDs/references, causal and supersession graphs, selected-history state, incomplete-call amendments and retry identity, checkpoint consistency, provenance spans, resource hashes. | Some lifecycle, requirement, task-dependency and coverage semantics still need complete validation. |
| Continuation | Selected dependency closure, configuration bindings, typed calls/results, workspace bases, Git declaration checks, report source hash/expiry and readiness consistency. | Reports remain declarations; no live checks or complete cryptographic verification of runtime evidence. |
| Request projection | Ordered typed inputs, selected tool definitions, model settings and required content references. | JSON output is a neutral projection. Provider encoding, token measurement and adaptation are not implemented. |
| Configuration | Explicit order, scope matching, neutral predicates, merge groups and declarative policy precedence. | Only the neutral dialect below is evaluated. No equivalence claim for vendor dialects or runtime enforcement. |
| Streaming | Byte-slice assembly and agreement with complete argument/text events; partial-gap refusal. | Other incremental protocols and media require additional features. |
| Workspace | Flatten file/directory snapshot/delta chains, explicit deletions, modes, destination collision checks, staging and rollback into a fresh destination. | No Git administrative/index restoration, links, native agent state or existing-tree mutation. |
| Package | Deterministic ZIP_STORED, complete inventory, path and resource closure checks, detached Ed25519 signatures. | Package verification alone checks container integrity and session shape, not every session semantic rule. |
| Redaction | Exact-pattern audit of raw JSON, decoded strings/keys/base64 and embedded resource bytes. Findings omit matched values. | No automatic secret discovery, compressed-content inspection, OCR or unavailable-content guarantee. |

## TypeScript differences and compatibility evidence

The TypeScript port implements the same selected session/report checks and operations, with these explicit limitations:

| Area | TypeScript behavior |
|---|---|
| JSON numbers | Refuses numbers whose decimal value changes when parsed and serialized as a JavaScript number, nonfinite results, integers outside the safe-integer range, and numeric literals longer than 4,096 characters. Refusal uses exit `3`; no rounded document is emitted. Ordinary values such as `0.2` are accepted. Python can preserve higher-precision decimal extensions. |
| ZIP containers | Supports single-disk ZIP32/STORED with ASCII or flagged UTF-8 names. ZIP64, data descriptors and legacy non-ASCII filename encodings are explicitly unsupported. Both local writers produce the supported envelope. Compression and encryption remain rejected by the package convention. |
| Workspace exclusions | Supports literal, `*` and `?` exclusion patterns. Bracket-glob exclusions encountered during deletion checks are unsupported. The input already contains the selected tree; neither restorer walks source directories to reselect files. |
| Diagnostics | Exit codes and successful JSON results follow the same command contract. Error wording and schema-error paths are implementation-specific and are not a shared message-string contract. |
| Unicode | Path case folding uses the pinned Unicode mapping in [casefold.json](reference/typescript/casefold.json), with its [third-party notice](THIRD-PARTY-NOTICES.md). Unicode normalization uses the host Node runtime. |

The TypeScript [test results](tests/typescript-results.json) cover the existing 44 Python continuation outcomes, core fixtures, numeric refusal, parsing, state, streams, configuration, restoration, package integrity, signatures and all nine CLI commands. [Live local exchange checks](tests/typescript-exchange-results.json) invoke both CLIs, exchange newly generated packages/signatures in both directions, and compare request, report, redaction and restored-file outputs. These are local tests with shared authorship; no real agent or independent implementation is involved.

The port uses [Ajv's JSON Schema 2020-12 implementation](https://ajv.js.org/json-schema.html#draft-2020-12-breaking), Node's [crypto APIs](https://nodejs.org/api/crypto.html), and a bounded ZIP32 reader/writer based on the [ZIP format specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT). It performs no runtime schema downloads.

## Workspace restoration

```sh
.venv/bin/python asif.py restore-workspace examples/continuation/another-computer.session.json workspace-head /tmp/asif-restored
```

The destination MUST not exist. Its parent must be a controlled directory without uncooperating concurrent writers. The reference implementation uses staging and a lock to coordinate its own writers, checks that the destination remains absent, and publishes by rename. It does not provide cross-process exclusion against arbitrary external writers or a crash-durable filesystem transaction.

Use `--case-insensitive` and `--normalization NFC` or `NFD` to model destination path equivalence. Input entries are already the selected tree; the tool does not walk source directories to reevaluate selection globs. Excluded deletion targets are protected. Existing paths are never merged or overwritten. Git and symlink restoration are explicitly unsupported rather than silently reduced to plain files.

## Neutral configuration evaluation

The libraries' `reference.context.resolve_configuration` (Python) and `resolveConfiguration` in [context.ts](reference/typescript/context.ts) (TypeScript) consumes a validated configuration and its continuation binding. Scope is global, root, or a path-component prefix. `effective_order` is authoritative within the recorded binding; priorities must agree. Only instructions active in the supplied environment are selected.

The local draft dialect `asif.activation/0.1` uses a JSON object with exactly one operator: `all` or `any` with an array of predicates; `not` with a predicate; `event_kind_in` with an array of strings; `root_is` with a string; or `path_prefix` with a portable relative path. Empty `all` is true; empty `any` is false. Missing root/event values do not match. Unknown operators/dialects are unsupported. Predicates never execute code.

```json
{
  "kind": "predicate",
  "dialect": "asif.activation/0.1",
  "expression": {
    "all": [
      { "event_kind_in": ["tool_call"] },
      { "path_prefix": "src" }
    ]
  }
}
```

Within matching authority/group/scope, `replace_same_scope` removes prior selected members; `append` retains them; `reject_conflict` requires structurally identical content parts. This comparison does not determine whether different prose is logically equivalent. Unknown authority/merge rules and untrusted content are refused as executable instructions.

`reference.context.evaluate_policy` (Python) and `evaluatePolicy` (TypeScript) accept the local `asif.policy/0.1` definition with `effect` (`allow`, `deny`, `ask`), `tool_ids` (exact IDs or `*`), `scope` and `activation`. Only enforcing policies participate; unknown enforcing dialects are unsupported. Matching deny wins over ask, then allow; no match yields ask. This declarative result never replaces destination authorization.

```json
{
  "id": "review-writes",
  "type": "asif.policy/0.1",
  "enforcing": true,
  "definition": {
    "effect": "ask",
    "tool_ids": ["tool-write"],
    "scope": { "kind": "global" },
    "activation": { "kind": "always" }
  }
}
```

These are explicitly local draft dialects. They do not establish equivalent behavior for arbitrary vendor policies.

## Signatures and redaction audit

`sign` takes a raw 32-byte Ed25519 private key supplied by the caller. `verify-signature` takes a separately trusted raw public key. Output files use exclusive creation.

```sh
.venv/bin/python asif.py sign /tmp/asif-example.zip --private-key /path/to/private.key --output /tmp/asif-example.sig.json
.venv/bin/python asif.py verify-signature /tmp/asif-example.zip --signature /tmp/asif-example.sig.json --trusted-public-key /path/to/trusted-public.key
.venv/bin/python asif.py audit-redaction examples/redacted-attachment.session.json --patterns /path/to/patterns.json
```

The pattern file is a nonempty JSON array of exact strings. The audit reports indexes and locations, including repeated and base64-encoded matches, without echoing patterns or source property names. A clean result means only that the supplied patterns were not found within the stated scope.

## Input limits

| Limit | Value |
|---|---|
| Session, report or manifest JSON | 16 MiB |
| Single decoded resource | 64 MiB |
| Total decoded embedded resources | 256 MiB |
| JSON nesting | 128 levels |
| JSON nodes | 2,000,000 |
| Records per indexed collection | 20,000 |
| Archive members | 1,024 |
| Total uncompressed archive members | 256 MiB |
| Archive bytes including envelope overhead | 272 MiB |
| Portable relative path | 4,096 characters |
| Activation predicate nesting | 32 levels |

Limits are checked with explicit refusal; data is not truncated. Filesystem inputs must be regular files, and resource traversal refuses symlinks. The controlled-input-directory requirement applies during reads as well as restoration: this reference is not a hardened concurrent filesystem service.

## Reproducing evidence and documentation

```sh
.venv/bin/python tests/check_schema.py
.venv/bin/python tests/check_examples.py
.venv/bin/python tests/check_continuation.py
.venv/bin/python tests/check_reference.py
.venv/bin/python tests/check_documentation.py
```

TypeScript checks run without Python:

```sh
npm ci
npm run typecheck
npm test
```

To refresh the shared parity corpus or exercise both CLIs together, use the Python environment plus Node.js 24+ on PATH:

```sh
.venv/bin/python tests/build_typescript_parity.py
.venv/bin/python tests/check_typescript_exchange.py
```

`ASIF_NODE=/absolute/path/to/node` can select a Node executable for the exchange checker. Refresh [typescript-parity-cases.json](tests/typescript-parity-cases.json) whenever the Python continuation expectations change, then rerun `npm test`. This corpus records expected outputs; it does not invoke Python during TypeScript tests.

The object reference is generated from schemas, authored descriptions and checked examples:

```sh
.venv/bin/python docs/build_reference.py
```

When rebuilding schemas, run `schemas/build_continuation_schema.py` followed by `schemas/build_core_extensions.py`. Rebuild continuation examples when source JSON changes because reports bind exact source bytes. Documentation checks detect example, table and link drift. Current evidence and remaining scope are listed in [GAPS.md](GAPS.md).

## License

The specification, schemas, examples and both reference implementations use the [MIT license](LICENSE). Third-party data and dependencies retain their own [notices](THIRD-PARTY-NOTICES.md).
