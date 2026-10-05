# Field comparison: ASIF v0.1 and existing specifications

Research date: 2026-09-26. This compares the earlier ASIF design's requirements against specific source revisions. It is a document/schema review, not runtime certification or a proof of ecosystem adoption.

The comparison columns retain that research snapshot. The **ASIF 0.4 disposition** column now refers to the active [0.4 session specification](../SPEC.md), superseding the preservation-only experiment. Linked field names lead to their definitions; future profiles are explicitly identified.

Legend: **D** directly modeled; **P** partially modeled or different semantics; **E** possible via extension/custom payload, without a portable core contract; **N** no equivalent core contract found. E/N means extension work, not impossibility. “Native” below refers to the captured vendor representation, not merely a model API item.

| Earlier ASIF field/requirement | Agent Session Format | ATIF | VAC / vCon | ASIF 0.4 disposition |
|---|---|---|---|---|
| Format version | D `format` | D `schema_version` | D `version` | [`asif_version`](../docs/objects.md#asif-document-object-asif_version) identifies the session contract. |
| Logical session identity | D header `id` | P run `session_id` | D `session-id` | [`session.id` and `session.native_ids`](../docs/objects.md#session-object) separate logical and provider-scoped identities. |
| Capture/document identity | P session file | D `trajectory_id` | D record `id` | [`capture.id`](../docs/objects.md#capture-object-id) identifies an immutable capture, distinct from the session. |
| Producer/vendor version | D `harness` | D `agent` | D `recording-agent` | [`capture.producer`](../docs/objects.md#capture-object-producer) records exporter name/version; [participants and executions](../SEMANTICS.md#4-participants-and-executions) carry known provider/model facts. |
| Several models per session | D `config`/`response` | D step override | D `models` | [Execution model settings](../docs/objects.md#execution-object-model) and [context model settings](../docs/objects.md#context-object-model) are scoped per use. |
| Message parts | D `item` | D `message` | D message content | Ordered [`parts`](../docs/objects.md#message-data-object-parts): text, resource, structured or opaque. |
| Opaque reasoning | D payload items | P reasoning/`extra` | D reasoning entry | [`opaque` parts and `semantic_type`](../docs/objects.md#opaque-part-object) preserve legitimately exportable recorded content without inventing hidden reasoning. |
| Tool-call/result linkage | D payload call ID | D call/observation IDs | D `call-id` | [`tool_call` / `tool_result` and `call_id`](../docs/objects.md#tool-call-data-object), including result indexes and terminal status. |
| Branch structure | D `parent` | P separate trajectories | P parent/children | [`branches`, `event_ids`, `head_event_id` and `fork`](../docs/objects.md#branch-object) define selected history explicitly. |
| Multiple causal predecessors | P `parents` provenance | E `extra` | E additional metadata | Event [`causes`](../docs/objects.md#event-object-causes) retain causal links independently of serialized and branch order. |
| Subagent links | D `link` | D subagent references | P parties/branches | [Participant parent and child-session references](../docs/objects.md#participant-object) identify delegation; child history is not implicitly included. |
| Execution boundaries | D `run` | P run scope | E system events | [`executions`](../docs/objects.md#execution-object) and [`execution_transition`](../docs/objects.md#execution-transition-data-object) record observed lifecycle. |
| Pending call/decision | D `dispatch`/`decision` | E `extra` | E system events | Checkpoint [`open_calls` and `open_decisions`](../docs/objects.md#checkpoint-object) distinguish evidenced pending state from unknown outcome. |
| Decision observer/confidence | E decision detail | E `extra` | E event data | Event [`actor_id` and `provenance.mode`](../docs/objects.md#event-object) distinguish attribution and observed/reported/derived evidence; no separate confidence scale is defined. |
| Compaction | D `compaction` | P copied-context flag | E system events | [`contexts` and `context_checkpoint`](../docs/objects.md#context-object) retain selected inputs, summary provenance and prior-context linkage. |
| Effective request settings | D `config` | P agent/tool definitions | E metadata | Context [`inputs`, `tool_ids`, `configuration_id` and request parameters](../docs/objects.md#context-object), with explicit fidelity. |
| Request reconstruction proof | D `request_hash` | E `extra` | P record signature | [Context conformance evidence](../SEMANTICS.md#13-conformance-and-next-work) is separate from authenticity; no standardized request hash or cryptographic proof is defined. |
| Usage and costs | D `response` | D metrics | D token usage | [`usage` scope, unit, value and delta/cumulative classification](../docs/objects.md#usage-object); no universal pricing model is defined. |
| External media | D `media` | D path references | D attachments | [`resources.availability` and `locator`](../docs/objects.md#resource-object-availability); external content is not fetched automatically. |
| Working-directory context | D `env` | E `extra` | D environment | [`environments`](../docs/objects.md#environment-object) describe logical roots/dependencies; paths do not authorize destination access. |
| Native transcript/store bytes | E custom/sidecar | E `extra` | P trace/attachments | [Native resources and coverage](../SEMANTICS.md#12-coverage-losses-and-unknown-extensions) preserve opaque evidence; [native import contracts](../CONTINUATION.md#10-native-import-and-identity) are specified, with real adapter testing still required. |
| Exact artifact inventory/digests | P media layout | P media paths | P attachments/signing | Embedded [`resources.bytes`, `sha256` and `text` / `data` / `path`](../docs/objects.md#resource-object) bind declared content; the optional [package inventory](../TRANSPORT.md#package-manifest-object) binds transported members. |
| Native record byte provenance | E custom metadata | E `extra` | E entry metadata | [`provenance.sources` and byte locators](../docs/objects.md#provenance-source-object) identify source resources, offsets and lengths. |
| Capture coverage/unknowns | P header `records` | P notes | E metadata | [`coverage`](../docs/objects.md#coverage-object) declares complete, partial, known-empty, unavailable, excluded, uninspected or inapplicable scope. |
| Redaction/transformation ledger | P export behavior | E `extra` | P redaction discussion | [`losses`](../docs/objects.md#loss-object) identify affected scope/references; [sanitized resources](../docs/objects.md#resource-object) have separate identities. |
| Complete portable configuration | E `custom` | E `extra` | E attachments | [`configurations`](../docs/objects.md#configuration-object) capture instructions/capabilities/policies; [cross-runtime equivalence](../GAPS.md) remains unresolved. |
| Workspace state/checkpoints | E `env` detail | E observations | P file artifacts | [`environments`](../docs/objects.md#environment-object) describe dependencies; [`checkpoints`](../docs/objects.md#checkpoint-object) describe session state. [Workspace/path rules](../CONTINUATION.md#5-workspace-snapshots-roots-and-paths) are now specified; the reference restores selected plain file trees; full Git/link fidelity remains open. |
| Unknown-field retention | D reader rule | P extension points | P extensible maps | [Unknown optional fields and `required_features`](../SEMANTICS.md#12-coverage-losses-and-unknown-extensions) define retention and refusal behavior. |
| Source-to-target import contract | P resume model | N | N | [Continuation consumers](../SEMANTICS.md#11-checkpoints-and-unresolved-work) assess prerequisites and report mappings; [continuation conformance](../SEMANTICS.md#13-conformance-and-next-work) needs real runtime evidence. |
| Cryptographic authenticity | P request hash | N | D signing | [Resource digests](../SEMANTICS.md#10-resources-and-availability) bind content; the optional [detached signature convention](../TRANSPORT.md#detached-signature-object) authenticates package bytes under a trusted key. |

## Source definitions and reproducibility

- [Agent Session Format — pinned RFC](https://github.com/ChristopherDavenport/agentsession/blob/dfc9ec67ec22de5e7946d0b75673fc34bcf2a824/docs/rfcs/0001-agent-session-format.md), sections Header, Entry envelope, Core entry types, Context building, Projections, Conformance. The fetched source says draft 0.4, but its header example still says 0.3. Treat this as an upstream clarification request; do not claim a conforming 0.4 exporter from the heading alone.
- [ATIF — pinned RFC](https://github.com/harbor-framework/harbor/blob/74cc6312018c349c6bd2400c89a0ac4983ac1085/rfcs/0001-trajectory-format.md), sections Root-Level Metadata, StepObject, Observation, SubagentTrajectoryRef, Implementation. Its run-scoped `session_id` is not a capture ID. That difference prevents a mechanical rename.
- [VAC revision 01](https://www.ietf.org/archive/id/draft-birkholz-verifiable-agent-conversations-01.txt), sections 3–4, especially session-trace, entries, and signed-agent-record. [vCon Agent Session revision 00](https://www.ietf.org/archive/id/draft-howe-vcon-agent-session-00.txt), sections 4–7, supplies the containing parties/dialog/analysis/attachments model. These are individual Internet-Drafts, not approved standards.
- [Agent Session Protocol — pinned types](https://github.com/kevin-dp/agent-session-protocol/blob/0c554624eb8c4d0a5dc68172fc0aed8d8c5eb2dd/src/types.ts) is a secondary compatibility target, including permission request/response records. Its [README](https://github.com/kevin-dp/agent-session-protocol) documents normalized and native-sidecar paths. Native-sidecar architecture is existing prior art; this review did not execute its migration claims.

[sources.json](sources.json) records fetched-document SHA-256 values and immutable URLs. Upstream texts were inspected locally but are not copied into this package.

## Gap assessment

The comparison establishes no requirement that is impossible to carry in the existing formats' extension mechanisms. The actual gap is agreement: common meanings for source-artifact preservation, coverage, loss, resource closure, and consumer capability claims.

The earlier preservation-only design treated these agreements as a companion package. The active [0.4 specification](../SPEC.md) instead defines ASIF session semantics directly, including events, branches, context and checkpoints. Its [remaining gaps](../GAPS.md) distinguish defined records from unresolved portability and implementation evidence. The comparison above does not establish conformance to that newer contract.

A signature authenticates a record under a key; it does not prove that the recorder observed all behavior. A request hash checks a reconstructed request; it does not prove that a native store will resume. These distinctions remain in ASIF regardless of the final container.
