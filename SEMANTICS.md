# ASIF session semantics

[Specification](SPEC.md) · [Object reference](docs/objects.md)

Version: **0.4**, 2026-10-05. Status: review draft of the session data model; not a released standard. This draft replaces the preservation-only experiment and develops the session model in the earlier v0.1 document. It is independent of any application, agent vendor, execution location, or transfer mechanism.

## 1. What a session is

A session is a persistent, identifiable record of an interaction among people, agents, and tools, together with the context and recorded state needed to interpret it and assess whether work can continue.

An ASIF session answers six questions:

1. Who participated, and what were they trying to do?
2. What happened, in what order, and on which branch?
3. What information, instructions, and capabilities did each agent receive?
4. Which actions, answers, and results are known, and which remain unresolved?
5. Which resources and environmental dependencies give those records meaning?
6. What is preserved, missing, transformed, or unsupported by the receiving implementation?

A transcript supplies part of that information. A native database can preserve more information without making its meaning interoperable. ASIF defines shared meanings for session data; source files can additionally preserve information outside those shared meanings.

**Interchange** means another implementation can ingest and export those records without silently losing their identities, relationships, content, or declared limitations. **Interoperability** means it interprets supported records with the same semantics. **Continuation** means a particular implementation can construct a usable next interaction from a specified checkpoint after resolving its prerequisites. These are separate capabilities; identical future model output is not a guarantee.

## 2. Required contents and optional detail

An ASIF document contains `asif_version`, `capture`, `session`, `participants`, `events`, `branches`, `executions`, `contexts`, `configurations`, `tools`, `resources`, `environments`, `checkpoints`, `coverage`, `losses`, and `required_features`.

Every collection is present, even when empty. Empty means **no records supplied**. The corresponding coverage declaration distinguishes known absence from missing or uninspected data. Domain-specific detail is conditional; an ordinary chat needs neither a workspace nor invented tool activity.

| Session component | Shared meaning | Required when |
|---|---|---|
| Identity and lineage | Logical session, immutable capture, predecessor/fork relationships. | Always; lineage can be empty. |
| Participants | Stable identities of people, agents, tools, and services; identities separate from message roles. | Every referenced actor must be declared. |
| Conversation and content | Ordered message parts, attribution, causality, edits, multimodal references. | Present in the captured interaction; otherwise explain coverage. |
| Branches | Explicit selected history and branch head; forks preserve their source boundary. | At least one, including an empty initial branch. |
| Executions | Recorded agent activity intervals, model requests, lifecycle and failures. | When observed or required for a capability claim. |
| Contexts | Ordered inputs actually supplied to a model or prepared for the next request. | Required to claim exact request-context reconstruction. |
| Configuration | Effective instructions, capabilities, model settings, policy and their origins. | When known; unresolved configuration blocks equivalent continuation claims. |
| Tools | Tool definitions, invocation arguments, results, errors, streaming boundaries and correlation. | Whenever tool activity appears. |
| Decisions and tasks | Questions, approvals, versioned plans/tasks, outcomes and pending work. | When recorded; unresolved outcomes remain explicit. |
| Memory and working notes | Recorded session facts, summaries, preferences and scratchpads as versioned resources with provenance. | When retained or supplied to the agent; their use is explicit in context. |
| Resources | Inputs, attachments, outputs and dependencies with availability and integrity. | Whenever referenced, including unavailable content. |
| Environment | Workspace or service context, logical roots, snapshots and prerequisites. | When relevant; not restricted to coding or Git. |
| Checkpoints | Recorded state at a branch boundary and requirements for further work. | One at each captured branch head; unknown state is valid. |
| Coverage, provenance and losses | What was observed, reported, derived, omitted, changed or unknown. | Always. |

`MUST`, `MUST NOT`, `SHOULD`, and `MAY` express this draft's requirements. The [session schema](schemas/session.schema.json) validates structure. The semantic rules below are additionally required; schema validation alone does not establish ASIF conformance.

## 3. Identity, capture and references

`session` requires `id`, optional `title`, optional `objective` as content parts, `native_ids[]`, and `lineage[]`. A native ID contains `provider`, `namespace`, and opaque `value`. A lineage entry contains `relation` (`continuation`, `fork`, `translation`, `copy`), `session_id`, `capture_id`, and optional `event_id` with `inclusive`. Fork and translation entries MUST name their source boundary. A fork gets a new session ID; another capture of the same session retains its ID.

`capture` requires a unique `id`, `producer` name/version, `consistency` (`consistent`, `partial`, `unknown`), and `boundary` text explaining what was observed. Optional timestamps describe capture activity, not invented event timing. Captures are immutable. Continuing or correcting a capture creates another capture. No merge or distributed writer protocol is defined.

Every entity has an opaque, case-sensitive ID unique within its entity collection and stable across captures where it denotes the same entity. Event IDs are unique within the logical session. Identical content does not imply identical identity. Splitting one source record into several events requires separate stable IDs. Adapters retain their identity mapping and report discontinuities.

References resolve by their named entity type. Event references use `{ "event_id": "..." }` for included events, or additionally name `session_id` and `capture_id` for explicitly external boundaries. External references MUST NOT be treated as included history. Missing local references are invalid. No consumer fetches an external reference merely by reading a session.

## 4. Participants and executions

A participant requires `id`, `kind` (`human`, `agent`, `tool`, `service`, `unknown`), and optional display name, provider, native ID, and parent participant. Delegation identifies both the participating agent and any child session reference. A child's separate history is not implicitly present in its parent's transcript.

An execution requires `id`, `participant_id`, `status` (`running`, `completed`, `failed`, `cancelled`, `interrupted`, `unknown`), and `context_ids[]`. Start/end times, model/provider/version/parameters, usage, and error evidence are optional. Status describes the observed capture boundary; it does not assert that a process is still alive. Missing lifecycle events do not establish completion.

Execution records and their transition events MUST agree at the captured boundary where lifecycle coverage is declared complete. Multiple executions can occur in one logical session; multiple agents can act concurrently. ASIF preserves concurrency and does not invent a global clock.

## 5. Event envelope, ordering and content

An event requires `id`, `sequence`, `actor_id`, `kind`, `causes[]`, `provenance`, and a kind-specific `data` object. Optional fields are `time`, `execution_id`, `supersedes`, and namespaced `extensions`.

`sequence` is a unique nonnegative integer defining serialization order in this capture. It does not establish causality or wall-clock ordering. `causes` identifies causal predecessors; local edges MUST be acyclic and point to earlier serialized events. Branch order selects conversation history; context order selects model input. Consumers MUST NOT substitute one of these orders for another.

Events are immutable. A correction names `supersedes`; the original remains available. Task updates use the revision mechanism in [§16](#16-task-revisions-and-dependencies) instead of event supersession. The branch or context explicitly selects which version applies. Supersession MUST be acyclic and MUST NOT silently remove evidence from history. A timestamp is optional and cannot break an ordering tie by itself.

Every provenance record declares `mode` (`observed`, `reported`, `derived`, `synthetic`) and `producer`. Optional source entries identify `resource_id` and a locator. Byte locators use zero-based `offset` and `length`; structured locators use an explicitly named syntax and value. Derived/synthetic records MUST name their method and inputs, including an empty input list for newly authored synthetic data. Direct ASIF instrumentation can be observed evidence without a native source file. Hidden reasoning and unobserved policy MUST NOT be fabricated.

Content is an ordered array of parts:

| Part kind | Fields and meaning |
|---|---|
| `text` | Exact `text`; optional declared media type. |
| `resource` | `resource_id`; optional description. Images, audio, video and files use resources. |
| `structured` | JSON `value` with a namespaced `schema` identifier. Unknown schemas remain opaque. |
| `opaque` | `resource_id`, `semantic_type`, and reason portable interpretation is unavailable. |

Part order is significant. An unavailable image is a referenced unavailable resource, never invented text. Recorded private reasoning, when legitimately exportable, is distinguished by an explicit semantic type; it is not required for ASIF and must not be inferred from a visible answer.

## 6. Core event meanings

| `kind` | Required `data` and interpretation |
|---|---|
| `message` | `role` (`user`, `assistant`, `system`, `developer`, `tool`, `unknown`), `parts[]`. Role does not replace actor identity. |
| `tool_call` | `call_id`, `tool_id`, `arguments` and `arguments_status` (`complete`, `partial`, `unknown`). Preserve the exact known argument value; a partial stream is not an executable completed call. |
| `tool_result` | `call_id`, `result_index`, `terminal`, `outcome` (`success`, `error`, `cancelled`, `unknown`), `parts[]`. Nonterminal chunks use `unknown` outcome. |
| `decision_request` | `request_id`, `decision_kind` (`approval`, `question`, `plan_review`), `prompt[]`, `options[]`; optional call/task/version bindings. |
| `decision_resolution` | `request_id`, `outcome` (`allowed`, `denied`, `answered`, `cancelled`, `expired`, `unknown`), `answer[]`; optional exact selected option ID. |
| `task_update` | `task_id`, `revision`, `status` (`proposed`, `pending`, `in_progress`, `completed`, `failed`, `cancelled`, `superseded`, `unknown`), `parts[]`; optional prior revision and dependencies. |
| `context_checkpoint` | `context_id`, `reason` (`initial`, `request`, `compaction`, `manual`, `unknown`); optional replaced context ID. |
| `configuration_change` | `configuration_id`; effective scope is the referencing execution/context, not global retroactive history. |
| `execution_transition` | `execution_id`, `status`; optional error or explanatory parts. |
| `resource_change` | `resource_id`, `operation` (`created`, `modified`, `deleted`, `observed`); optional previous resource ID. |
| `note` | `parts[]`, `category`; explanatory evidence with no implicit execution meaning. |
| `extension` | Namespaced `type`, arbitrary `value`, and `interpretation_required`. Required semantics also appear in `required_features`. |

A tool definition requires `id`, namespaced `name`, `description`, `input_schema` (JSON Schema 2020-12), and optional output schema, server identity, revision, and resource references. A native tool with an unknown input contract uses the permissive schema `true` and records the limitation. Naming a tool is not a portable implementation of its behavior.

`call_id` is session-scoped and identifies exactly one logical invocation. Retries use new IDs and may reference the prior call. Results correlate by ID, never by adjacency or tool name. Result indexes are unique and increasing per call; at most one terminal result is allowed in a selected history. Calls/results can cross capture boundaries only with declared external call bindings. The optional `asif.external-bindings/0.1` feature supplies those bindings under the [external binding rules](STREAMING.md#external-bindings); consumers MUST NOT fabricate a missing invocation. The optional `asif.streams/0.1` feature preserves incremental bytes under the [assembly rules](STREAMING.md).

No terminal result means outcome unresolved, not proof of failure or permission to rerun a side effect. A late result is new evidence. A caller can have several outstanding calls.

A decision resolution binds the exact request and, where relevant, call or task revision. No recorded resolution means unknown outcome. Historical approval is evidence; a receiving runtime must make its own authorization decision. A task completion record is a reported state, not proof that its objective was achieved.

### Tool-call progression across captures

An invocation can be observed before its arguments are complete. Further knowledge of that **same invocation** is recorded as a new `tool_call` event with a new event ID and a local `supersedes` reference to its earlier version. The original event remains unchanged and included in the document, even when copied from an earlier capture. The session and `call_id` stay the same; a later capture has a new capture ID. Repeating a `call_id` without this amendment relationship is invalid.

A call amendment MUST preserve `call_id`, `tool_id`, event `actor_id`, event `execution_id` (including absence), and `retry_of` (including absence). Its predecessor MUST be an earlier local `tool_call`. Argument knowledge may stay `unknown`, progress from `unknown` to `partial` or `complete`, or progress from `partial` to `partial` or `complete`. It MUST NOT regress from `partial` to `unknown`, and a `complete` call MUST NOT be amended through this mechanism. Each event carries its own exact known `arguments` value; consumers MUST NOT merge those values or concatenate them to guess complete arguments. Protocol fragments are recorded separately using [streams](STREAMING.md).

A selected history may select only the final call version while retaining its predecessors elsewhere in the document. If it selects multiple versions of the invocation, each later selected version MUST directly supersede the preceding selected version. Conflicting successors may exist on different branches but MUST NOT both be selected in one history. A selected history cannot skip an intermediate amendment while selecting versions on both sides of it. A branch selecting only the original retains its original argument knowledge.

State derivation processes selected call versions in branch order and updates the known arguments for that invocation. It preserves call/result/decision correlation already established at the first selected version. An amendment recorded after a result changes captured argument knowledge; it does not remove the result, reopen a terminal invocation, or authorize execution. At an earlier checkpoint, later amendments do not apply. A model context explicitly selects one typed call input per invocation at its declared boundary; it does not replay the amendment history as several calls.

A retry is a different invocation and MUST receive a new `call_id`, even when its arguments are identical. Optional `retry_of` identifies the prior invocation and MUST NOT equal the retry's own ID. A retry MUST NOT supersede the earlier invocation. Amendments do not establish whether an operation ran, and complete arguments do not establish authorization to run it.

An external call descriptor alone is insufficient to verify an amendment's event identity, actor and execution. To amend a call from an earlier capture, include the authentic predecessor event and its required references locally, preserving its event ID, contents and provenance; remove any external binding for that same invocation. A call amendment with an external-only `supersedes` reference is invalid. If the predecessor cannot be included, preserve the new evidence as a note or opaque resource with an explicit limitation rather than inventing a local observed call. External bindings still support correlation of a late result with an unchanged external invocation.

See the [two-capture example](examples/README.md#tool-call-progression-across-captures). These rules use existing fields; they add inter-event semantic checks, not a new JSON representation.

## 7. Branches and selected history

A branch requires `id`, ordered `event_ids[]`, `head_event_id` (nullable for an empty branch), and optional `fork` with source session/capture/branch/event and inclusive choice. A branch contains no duplicate event IDs. Its head MUST equal its final selected event. An included causal predecessor MUST occur earlier if it appears in the same selected branch; cross-branch causality remains explicit and does not automatically import another branch's history.

A branch's list is the selected history supplied in this capture, not necessarily all history ever created. Partial prefixes and missing ancestors require coverage and boundary declarations. A fork explicitly states where histories diverge; it does not imply a workspace rewind.

Edits, retries and alternative answers can create branches. Combining branches creates a new explicitly selected history and context; consumers MUST NOT union two histories and call that the original model context. Native-only branch relationships remain a declared limitation until mapped.

## 8. Context and compaction

A context requires `id`, `branch_id`, `at_event_id` (nullable), `purpose` (`model_request`, `continuation`, `summary`), `fidelity` (`exact`, `reconstructed`, `partial`, `unknown`), ordered `inputs[]`, and `tool_ids[]`. Optional `configuration_id`, model settings and request parameters describe that exact context.

Each input requires `id`, `kind`, `role`, `parts[]`, and `source_events[]`. `kind` is `message`, `tool_call`, or `tool_result`. A tool call additionally carries `call_id`, `tool_id`, `arguments` and `arguments_status`, with assistant role. A tool result carries `call_id`, `result_index`, `terminal` and `outcome`, with tool role. Nonterminal results have unknown outcome. Calls/results retain the correlation semantics of §6; message text cannot silently replace them. The [typed-context rules](CONTINUATION.md#4-typed-request-context) define their continuation use.

This explicit resolved list specifies what the model saw or is proposed to see; event references provide provenance rather than an instruction to guess content selection. A source event can contribute only part of its content. A transformed input states `transformation`; summary inputs identify their source ranges/events. Exactness refers to the captured structured inputs and settings, not undocumented provider-side processing.

Instructions supplied as input are represented in this ordered list. `configuration_id` describes their origin and rules; consumers MUST NOT prepend them a second time. `tool_ids` is the exact available tool set when fidelity is `exact`. An exact context requires known configuration and declared request settings; unknown hidden platform additions are reported as a limitation and cannot be included in the exactness claim.

Compaction creates a new context and a checkpoint event linking the prior context. Preserve the summary's exact content, selected retained inputs, and known covered/replaced source events. A summary is not a byte-preserving substitute for discarded history. Conversation coverage and request-context fidelity are independent: a complete transcript can still have unknown effective context.

## 9. Configuration and environment

A configuration is an immutable snapshot requiring `id`, ordered `instructions[]`, `capabilities[]`, `policies[]`, `secret_requirements[]`, and `knowledge` (`effective`, `declared`, `partial`, `unknown`). Optional model settings and environment IDs attach recorded execution requirements.

An instruction requires `id`, content `parts[]`, `scope` and `activation`, plus source provenance. Array order represents recorded application order only when knowledge is `effective`; unknown precedence MUST be disclosed. Scope/activation retain their source dialect and values. Consumers must not silently turn conditional, directory-scoped, or platform instructions into universal instructions.

A capability describes a skill, plugin, hook, service connection or other runtime facility with namespaced `type`, ID, definition, resource IDs, and `required` flag. Tool schemas describe callable interfaces; capabilities describe additional dependencies and behavior. Policies record namespaced definitions and whether they enforce restrictions. Unsupported required capabilities or enforcing policies block equivalent continuation. They do not block read-only inspection.

Secret requirements contain logical handles and purpose, never credential values. They are unresolved prerequisites on import. Raw preserved source resources may contain sensitive material; producers disclose redaction and cannot claim original-byte preservation for modified resources.

An environment requires `id`, `kind` (`workspace`, `service`, `runtime`, `other`), `description`, `resource_ids[]`, and `requirements[]`. Workspace-specific data can name logical roots, snapshots, selected files, revisions and checkpoints through namespaced definitions. Plain folders and non-coding environments are valid. A recorded filesystem path is metadata, not permission to read or write that destination.

The optional [portable-continuation profile](CONTINUATION.md#5-workspace-snapshots-roots-and-paths) defines workspace snapshots, deltas, Git/index prerequisites and path mappings. The core describes dependency identity and availability; it does not assert a complete filesystem from a patch, repository URL, or commit ID. Actual restoration remains an adapter capability requiring tests.

Session memory, working notes and retained preferences use resources with `purpose: session_memory`, content and provenance. Changes create new resource identities and `resource_change` events. Their contents can be reported beliefs or summaries; capture does not establish factual truth. Context inputs explicitly include any memory supplied to a model, with resource parts and source-event references. A receiver MUST NOT automatically inject every memory resource into future context. External user/organization memory is not implicitly included in a session; its absence and dependencies belong in resource/configuration coverage.

## 10. Resources and availability

A resource requires `id`, `media_type`, `availability` (`embedded`, `external`, `unavailable`, `excluded`, `redacted`, `unknown`), and `purpose`. Optional metadata includes name, original location, length, digest and provenance.

An embedded resource requires exactly one of `text`, base64 `data`, or relative `path`, plus `bytes` and `sha256`. Hash and length cover decoded bytes; text uses UTF-8. External resources require a locator and explanation and are not fetched automatically. Missing/excluded/redacted/unknown resources require an explanation. A sanitized replacement is a new embedded resource with its own digest and a loss record; it is not the original redacted resource.

Multiple references may share one immutable resource. Changed content receives a new resource ID. Attachments and generated outputs are independent of workspace selection rules. Required resources are assessed per capability and checkpoint, not by assuming every recorded attachment must exist for every use.

Relative payload paths MUST remain within the session directory, use forward slashes, and reject absolute/drive paths, backslashes, empty/dot/parent segments, links, special files and destination-normalization collisions. No path is used for native-store installation automatically. Implementations disclose size/depth/count limits. This draft does not select an archive, encryption, or signature wire format.

For standalone JSON examples, the session directory is the directory containing that document. The [worked examples](examples/README.md) demonstrate file-backed images/PDFs, inline audio/text, generated outputs, unavailable resources, redacted replacements and attachments preserved across compaction. Their content and agent activity are synthetic; the embedded attachment bytes and digests are concrete.

## 11. Checkpoints and unresolved work

Each captured branch head has one checkpoint requiring `id`, `branch_id`, `at_event_id`, `knowledge` (`observed`, `derived`, `unknown`), `status` (`idle`, `active`, `waiting`, `stopped`, `ended`, `unknown`), nullable `context_id`, nullable `configuration_id`, `open_calls[]`, `open_decisions[]`, `tasks[]`, and `requirements[]`.

Open-call/decision entries identify their call/request and `state` (`pending`, `outcome_unknown`). `pending` needs recorded evidence; lack of a result alone yields `outcome_unknown`. Task entries bind `task_id` and exact revision. Empty arrays do not prove no outstanding work unless the relevant coverage and checkpoint knowledge support that conclusion.

Requirements identify `id`, namespaced `kind`, `description`, `required_for[]` (`read`, `context`, `continue`), and `status` (`available`, `unresolved`, `unavailable`, `unsupported`). Optional resource, capability, environment or secret handles identify their subject. Availability is observed for the capture; a destination rechecks it.

A continuation consumer chooses a checkpoint and reports: selected context and history, supported/unsupported semantics, configuration translation, unresolved calls/decisions, missing resources, and destination prerequisites. It MUST NOT rerun an unresolved side effect automatically, reuse approval as authorization, or claim equivalence after dropping a required restriction. A session may be interoperably readable while continuation is blocked.

## 12. Coverage, losses and unknown extensions

Exactly one coverage record is required for each domain: `participants`, `conversation`, `branches`, `executions`, `contexts`, `configuration`, `tools`, `decisions`, `tasks`, `resources`, `environment`, `native`, and `usage`.

Each requires `scope`, `status` (`complete`, `partial`, `known_empty`, `unavailable`, `excluded`, `not_inspected`, `not_applicable`), and `detail`. Completeness is limited to the stated capture boundary and selection, not a promise that all original system state was discovered. `known_empty` requires evidence that the domain had no records in scope. `not_applicable` requires a reason. Empty collection plus `not_inspected` is unknown, not absence.

Losses require ID, stage (`capture`, `normalization`, `redaction`, `translation`), kind, affected typed references or domain, and explanation. Record truncation, omitted media, unsupported policy, changed arguments, synthesized context, identity changes and unknown mappings. An empty loss array means none reported, not proven perfect fidelity.

Optional usage records identify measurement scope, unit, value, provenance and whether the value is a delta or cumulative counter. Consumers MUST NOT sum repeated cumulative counters as independent usage. Timing claims identify observed versus derived boundaries; absent timestamps do not imply zero duration.

Unknown optional properties MUST survive interchange, either directly or as recoverable original source data with a mapping receipt. They cannot override known semantics. Unknown required features block semantic acceptance for their stated use. Core event kinds are fixed; vendor events use `extension`. An extension with `interpretation_required: true` MUST list its exact namespaced type in `required_features`.

Native stores, transcripts and unknown records can be embedded resources. They support preservation and specialized adapters. Carrying only native bytes does not satisfy ASIF conversation interoperability; the normalized ASIF records and their coverage are the common contract.

## 13. Conformance and next work

Capabilities are independent claims, each tied to a version, scopes, limitations and evidence:

| Capability | Required proof |
|---|---|
| Structure | Schema, references, IDs, graphs, conditional fields, coverage, content integrity and declared limits validate. |
| Read | Supported roles, content, branches, correlation and unresolved states have the prescribed interpretation; unknowns stay visible. |
| Interchange | Producer → consumer → export preserves IDs, selected order, parts, links, states, unknown optional data and declared losses. |
| Context | A selected context reconstructs the declared ordered request inputs, instructions, tool interfaces and settings, at its stated fidelity. |
| Continue | Destination prerequisites and policies are checked and a real next interaction is demonstrated; limitations are reported. |

The schemas and synthetic examples in this package are review aids. There is no complete semantic validator or conforming runtime implementation of this session draft yet. Profile checks exercise selected continuation invariants and report outcomes. Earlier preservation-only prototype results do not apply to it.

Remaining release work: complete semantic validation; implementation and testing of configuration/tool dialect bindings, workspace/native import and destination checks; source-to-ASIF adapters with loss reports; two independently authored implementations exchanging fixtures and demonstrating real continuation; public governance and versioning adoption. The [conformance plan](CONFORMANCE.md) records concrete acceptance cases. The [governance proposal](GOVERNANCE.md) remains a proposal until participants adopt it.

## 14. Portable continuation

The [portable-continuation profile](CONTINUATION.md) adds contracts for another computer, cloud runtime or agent: consistent checkpoint bindings; typed request context; workspace and path mappings; runtime/tool/model dependencies; effective instructions and policy; service/authentication bindings; in-flight operation recovery; native import; and destination assessment/import receipts.

A document opting in includes `continuation` and `asif.portable-continuation/0.2` in `required_features`. Both are mandatory for that profile. Consumers unable to interpret it cannot claim continuation support. Source declarations are immutable; destination assessments bind the exact source bytes and runtime capabilities. Readiness, import and demonstrated continuation remain independent outcomes.

Draft.3 requires explicit `kind` on context inputs; draft.2 documents are not silently reinterpreted. Migrating ordinary message inputs adds `kind: message`. Migrating tool exchanges requires recovering their actual call/result fields or declaring incomplete context. A producer must not label an opaque tool exchange as plain text and claim equivalent continuation.

## 15. Selected-history state transitions

A correction applies only where a selected history includes the correcting event. A selected correction supersedes its named predecessor for derived current state while both records remain available as evidence. It MUST name an earlier event of the same kind; a corrected decision resolution MUST retain the same request identity. Two effective resolutions of the same request are contradictory and MUST NOT be resolved by choosing the latest timestamp.

A task revision MUST name its selected predecessor when one exists and increase its revision number. Reopening a completed, failed, cancelled or superseded task as proposed, pending or in progress MUST include a nonempty `reopen_reason`. A partial history lacking its task predecessor cannot claim a fully reconstructed task transition. [§16](#16-task-revisions-and-dependencies) defines dependency selection and partial-history handling.

Within a selected history, a terminal tool result closes that invocation; another result for that invocation requires an explicit correction rather than silently reopening it. Terminal execution transitions cannot return to running under the same execution identity. These rules describe recorded state, not permission to execute, approve or repeat an action.

## 16. Task revisions and dependencies

### Identity and revision selection

`task_id` identifies a logical task within the session. The pair `(task_id, revision)` MUST identify at most one event in a capture and remains stable across captures. Revision numbers need not be contiguous. Divergent revisions of the same task on different branches still use different revision numbers. A task update is a complete recorded state at that revision, not a patch: absent optional fields do not inherit values from earlier revisions.

At a branch boundary, process the selected task updates through that boundary in branch order. The last selected revision of each task is its current recorded state. A later revision MUST name the preceding selected revision in `previous_revision`, and the number MUST be strictly smaller than the new `revision`. A first selected revision may have any nonnegative revision number. Omission of `previous_revision` means no predecessor is declared; it does not imply revision zero or manufacture a creation event. Producers MUST retain a known predecessor relationship when exporting a partial selection.

Task updates MUST NOT carry event-envelope `supersedes`. Corrections and changes append a new task revision using `previous_revision`, preserving the earlier task definition, decision bindings and transition evidence. Status `superseded` records that the task was retired; it does not select a replacement task or redirect references. Reopening terminal tasks follows §15. Other status changes record what the source reported; core ASIF does not impose a scheduler's lifecycle. An `unknown` state does not establish success, failure or permission to restart work.

### Dependency references and their meaning

`dependencies`, when present, is the complete declared list of prerequisite **task IDs in the same session**, not event IDs, revision IDs or continuation-profile dependency IDs. Omission means the dependency list is unknown; `[]` explicitly declares none for that revision. Every listed ID MUST have a `task_update` somewhere in the capture, even with partial task coverage. Self-dependencies and duplicate entries are invalid. IDs are opaque: strings resembling external paths or URLs remain local task IDs and MUST NOT trigger fetching.

At each assessed branch/checkpoint boundary, each dependency binds to that task's latest selected revision through the boundary. It is not pinned to the revision that existed when the dependent task was written. A task present only on another branch, or later in the selected history, has no selected state at that boundary: its dependency state is unknown. Consumers MUST NOT import another branch's state or use a future revision to fill that gap. Forward declarations are permitted when the referenced task identity is included in the capture.

| Selected prerequisite state | Dependency interpretation |
|---|---|
| `completed` | Satisfied according to the recorded state; not proof that the objective was achieved. |
| `proposed`, `pending`, `in_progress`, `failed`, `cancelled`, `superseded` | Unsatisfied according to the recorded state. |
| `unknown`, or no selected revision | Unknown; never silently satisfied. |

Dependencies are descriptive prerequisites. An unsatisfied or unknown dependency does not make a reported `in_progress` or `completed` dependent task invalid and does not authorize or prohibit execution. Reopening, failing, cancelling or retiring a prerequisite changes its dependency interpretation at later boundaries but MUST NOT silently change dependent task statuses, invalidate historical approvals, or rewrite earlier checkpoints. A changed dependent task requires its own revision; an approval still binds its exact named revision. Exact-revision dependencies, replacement-task substitution and scheduling rules need a separately specified required feature or workflow contract.

### Graphs and incomplete histories

The graph of declared dependency edges among selected current task revisions MUST be acyclic after **each selected task update**, not merely at the branch head. Replacing a dependency list removes the earlier revision's edges for subsequent states. Consumers MUST NOT union edges from different revisions or branches and reject a cycle that exists only in that union. Tasks without selected state or without a known dependency list contribute no known outgoing edges; an acyclic known graph does not establish that unknown dependency information is complete.

When a first selected task update names a predecessor that is not selected, the task coverage record MUST have `status: partial`, and its detail and capture boundary MUST explain the omitted history. The declared predecessor number still MUST be smaller than the current revision. Consumers retain that unresolved transition as a reconstruction gap, even if later revisions form a complete suffix. A predecessor elsewhere in the document or on another branch is not implicitly selected. Partial coverage does not permit skipping a predecessor when an earlier revision of that same task is already selected: the next revision must directly name it.

Partial coverage also does not excuse a dangling dependency ID. To preserve an external or unavailable task that cannot be represented as a local task with honest provenance, retain its native evidence and a coverage/loss explanation rather than inventing a local task or claiming that core `dependencies` resolves it. External task references require a separately specified feature; the external call/request bindings do not bind tasks. A valid partial record can support inspection without proving a complete transition history or continuation readiness.

See the [task examples](examples/README.md#task-revisions-and-dependencies) for branch selection, reopening, retirement and explicit predecessor gaps.
