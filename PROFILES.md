# ASIF core and optional profiles

The core defines the shared session record and explicit coverage of every domain. A profile adds exact semantics to a specialized capability; it cannot redefine core records or conceal missing data.

The [portable-continuation profile](CONTINUATION.md), `asif.portable-continuation/0.1`, is now specified in draft form with schemas and synthetic checks. Its fields cover the previously undeclared continuation contracts below. This is specification coverage, not a claim of working runtime adapters.

| Area | Core requirement | Additional profile work |
|---|---|---|
| Conversation | Participants, roles, ordered parts, immutable events, causal references. | Specialized media annotations and rendering. |
| Branches/context | Selected history, typed message/call/result inputs, compaction provenance, context fidelity. | Continuation profile binds a checkpoint and accounts for consumed history; provider mappings require implementation. |
| Tools | Definitions, calls/results, correlation, terminal status, unknown outcomes. | Continuation profile defines implementation/behavior bindings and operation recovery; optional [stream-fragment and external-binding features](STREAMING.md) define captured partial-protocol evidence. |
| Configuration | Instruction content, scope/activation dialect, capability/policy declarations, secret handles. | Continuation profile defines effective ordering, authority, scope, merge rules and destination policy/authentication assessment. |
| Decisions/tasks | Requests, outcomes, task revisions, branch-selected task dependencies and explicit partial-history gaps. | Domain-specific scheduling, exact-revision dependencies and external-task binding contracts. |
| Resources | Content, integrity, availability and typed references. | The optional [package convention](TRANSPORT.md) defines exact-byte inventory/signatures; large-object streaming remains separate. |
| Environment | Logical dependency identity and prerequisites. | Continuation profile defines workspace/Git declarations, roots, path mappings, service/runtime dependencies and model constraints; the local reference restores selected plain file trees; full Git/link restore requires further implementation. |
| Native evidence | Opaque resources with provenance and coverage. | Continuation profile defines native adapter/version/identity/index requirements and receipts; vendor restoration still requires real tests. |

Profile activation requires both the `continuation` object and its exact feature identifier in `required_features`. An unsupported consumer cannot silently treat continuation metadata as optional. Destination reports are separate from source captures and are invalidated by changes to their bound source or destination.

Profiles require a versioned identifier, normative rules, schema, negative/positive fixtures, consumer refusal behavior, and evidence for any advertised capability. Until defined and implemented, their required semantics are unsupported. A label alone does not establish conformance.
