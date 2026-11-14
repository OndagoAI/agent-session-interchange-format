# ASIF implementation evidence

Two locally authored reference implementations accompany **0.4**: [Python](asif.py) and [TypeScript](asif.ts). The TypeScript implementation ports the Python reference's documented subset and runs without Python. Both expose nine CLI commands; [scope and language differences](REFERENCE.md) remain explicit. Neither claims complete conformance or live agent continuation.

[TypeScript results](tests/typescript-results.json) include shared Python continuation expectations and local positive/negative tests. [Exchange results](tests/typescript-exchange-results.json) verify newly generated packages/signatures in both directions and compare CLI outputs and restored files. These implementations and tests share authorship; this does not satisfy the independent-implementation gate. Both reference implementations use the [MIT license](LICENSE).

**Independent implementations exchanging sessions: zero.**

Record actual participation only when an implementer supplies evidence:

- Project/repository, authors, affiliation, code revision and license terms.
- ASIF/profile versions, supported capabilities, limits and unsupported semantics.
- Fixture digests and reproducible commands/results.
- Independently produced sessions exchanged with another implementation.
- Results for structure, interpretation, interchange, context and continuation separately.
- Unresolved discrepancies and report location.

## Recorded implementation evidence

An implementer may supply a public record for the fields above. The record below is listed for
review. It is not an endorsement, a conformance certificate or an independent-exchange claim, and
it does not change the independent-implementation count above.

### `vowp-asif` 0.1.1

| Field | Value |
|---|---|
| Repository | [`syver777/vowp-asif`](https://github.com/syver777/vowp-asif) (MIT) |
| Revision | `0.1.1`, commit [`466ebb8`](https://github.com/syver777/vowp-asif/tree/466ebb81f58646febb80996874b46c11288d5a97), release [`v0.1.1`](https://github.com/syver777/vowp-asif/releases/tag/v0.1.1) |
| Author/maintainer | Syver-August Meyer (`syver777`), from the repository's MIT copyright notice. No organization affiliation is stated in the public repository. |
| ASIF | `0.4` review draft, pinned at [`652d9e2`](https://github.com/OndagoAI/agent-session-interchange-format/commit/652d9e23ddbe5656b9ceea311df7e09e93c1cd2f) |
| Source | VOWP v0.2 session directory, protocol version `1`, capsule version `1`; read as files only |
| Evidence issue | [#22](https://github.com/OndagoAI/agent-session-interchange-format/issues/22) |

**Supported scope**

- VOWP session directory → ASIF `session.json`, a directory or a deterministic `ZIP_STORED`
  `.asif.zip` package, with a preservation/loss report.
- ASIF package/session → a new VOWP session directory with a gapless `log.jsonl`, exact resource
  bytes and restored capsules where capsule provenance exists.
- Offline validation of the ASIF 0.4 schema, package inventory, ZIP member rules, references,
  coverage scopes and resource digests.
- All 17 VOWP protocol-version-1 event types are mapped. Export writes one linear `main` branch,
  keeps one-to-one event IDs where ASIF permits and retains the VOWP envelope in `vowp.*`
  extensions.

**Declared limits**

- Exact request context is not claimed. VOWP does not record the system prompt, provider request
  encoding or complete tool schemas; exported contexts are `partial` or `reconstructed`.
- Continuation is not implemented or claimed. No `asif.portable-continuation/0.2` object is
  emitted, and required continuation, streaming or external-binding features are refused.
- Native harness import is not claimed. `adapters.json` is native evidence, not a Claude Code or
  opencode store.
- A complete workspace snapshot is not claimed. VOWP records file changes and diffs, not a tree,
  Git commit or index.
- Capsule content is a model-written summary preserved as a `session_memory` resource; its bullets
  are not promoted to observed task or decision state.
- VOWP jobs, gates, leases and project rows are outside the session directory and are not emitted.
- This record does not claim ASIF conformance or independent interoperability.

**Fixtures and reproduction**

- [`fixtures/asif/`](https://github.com/syver777/vowp-asif/tree/466ebb81f58646febb80996874b46c11288d5a97/fixtures/asif)
  contains the pinned ASIF 0.4 `awaiting-approval` example (SHA-256
  `1737acca2729882335724734384dc3fc20b8f170373de4096444ff0bc65b6efd`, recorded in
  `fixtures/asif/PROVENANCE.md`) and an authored synthetic `minimal-chat` example.
- [`fixtures/vowp/`](https://github.com/syver777/vowp-asif/tree/466ebb81f58646febb80996874b46c11288d5a97/fixtures/vowp)
  contains eight authored synthetic VOWP sessions covering minimal chat, tool activity, capsules,
  blobs, all 17 event types, compaction, redaction and unsupported operations.
- Fixture-tree digest at `466ebb8`:
  `93e2d6222ed5ad09b482ba987e7be62bd5c423bf99ee84868aee1605e84c3a9c`, computed as
  `(cd fixtures && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum)`.
- Tests:
  [`tests/export.rs`](https://github.com/syver777/vowp-asif/blob/466ebb81f58646febb80996874b46c11288d5a97/tests/export.rs),
  `tests/import.rs`, `tests/package.rs` and `tests/roundtrip.rs`; `cargo test` passes 91 tests at
  this revision.

```sh
cargo test
cargo run -- export --session-dir fixtures/vowp/all-events \
  --out /tmp/all-events.asif.zip --json
cargo run -- validate /tmp/all-events.asif.zip --json
cargo run -- import --in /tmp/all-events.asif.zip \
  --out /tmp/all-events.session --cwd /synthetic/work --json
```

**Results**

- Structure: generated sessions and packages pass the adapter's offline checks against the pinned
  ASIF 0.4 schema and package rules.
- Interpretation: the source-to-ASIF mapping and every declared loss are documented in
  [`docs/MAPPING.md`](https://github.com/syver777/vowp-asif/blob/466ebb81f58646febb80996874b46c11288d5a97/docs/MAPPING.md)
  and
  [`docs/COMPATIBILITY.md`](https://github.com/syver777/vowp-asif/blob/466ebb81f58646febb80996874b46c11288d5a97/docs/COMPATIBILITY.md).
- Interchange: the adapter's own VOWP → ASIF → VOWP round trip preserves mapped identities, order,
  payloads and resource bytes and records deviations. No independently produced session has been
  exchanged.
- Context: reconstructed or partial only; no exact provider request is claimed.
- Continuation: not implemented and not claimed.
- Evaluation mode: `synthetic`. The fixtures are authored or public ASIF examples; no real source
  session, destination interaction or native import was observed.
