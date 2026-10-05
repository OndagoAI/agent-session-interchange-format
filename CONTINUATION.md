# ASIF portable-continuation profile

Profile: `asif.portable-continuation/0.1`. ASIF version: **0.3**. Status: normative proposal with structural schemas and synthetic validation fixtures; no real agent interoperability or runtime restoration is claimed.

Object reference: [profile objects](docs/continuation-objects.md) · [report objects](docs/report-objects.md). Each object has a field table, rules and a checked JSON example.

## 1. Scope and activation

This profile specifies the data and checks needed to continue on another computer, in a cloud runtime, or in another agent. A session using it contains `continuation` and includes the exact profile identifier in `required_features`. Both declarations are required. A consumer without this profile can preserve the document but MUST NOT claim to interpret its continuation contract.

The source document remains immutable. A destination produces a separate assessment/import report. The session schema embeds the [profile schema](schemas/continuation.schema.json); the [report schema](schemas/continuation-report.schema.json) describes the destination receipt. Schema validity is necessary but does not establish readiness.

The profile does not implement transport, cloud placement, credential forwarding, live leases or distributed locks. A host must coordinate ownership of active execution. Captured evidence of a paused writer is not a transferable lease, and a source process ID is never a destination process identity.

## 2. Continuation records and reference scope

`continuation` requires `profile_version`, `source_runtime`, `workspaces[]`, `dependencies[]`, `configuration_bindings[]`, `service_bindings[]`, `operations[]`, `native_imports[]`, and `plans[]`. Empty collections explicitly declare no supplied records, subject to the source session's coverage. At least one plan is required.

Collection IDs are unique in their own type. Core entity references resolve in the enclosing ASIF document. Dependency and workspace references resolve in this profile. Dependencies form an acyclic graph. A plan selects the exact subset to assess, including all transitive prerequisites; unselected historic resources need not block it.

`source_runtime` records agent identity/version/native state-format version, adapter identity/version, OS and architecture. An unknown version is represented by `null`, not a guessed compatibility range. Runtime identity does not imply that its source paths, logins or installed programs exist at the destination.

## 3. Consistent checkpoint and next action

A plan names `checkpoint_id`, `context_id`, `configuration_id`, `workspace_ids[]`, `dependency_ids[]`, `service_binding_ids[]`, `operation_ids[]`, and nullable `native_import_id`. It also carries `boundary`, `context_accounting[]`, `cwd`, `path_references[]`, `model_requirements`, and `next_action`.

The checkpoint fixes branch and head. Its context and configuration MUST match the plan. The selected context MUST be for `continuation`, with `at_event_id` equal to the checkpoint boundary. A previous model-request context is not automatically the next continuation context.

`boundary` declares `method` (`quiesced`, `transactional`, `bounded_read`, `best_effort`), `consistency` (`consistent`, `partial`, `unknown`), evidence resource IDs, and explanation. It binds the selected conversation head, context, configuration and workspace snapshots. Each selected workspace names that boundary. `best_effort`, partial or unknown captures cannot be reported ready until a new consistent capture or an explicit reconstruction establishes the required state; describing them as consistent is insufficient evidence.

For every event in selected branch history through the head, `context_accounting` records `event_id`, `disposition` (`included`, `summarized`, `not_input`, `unavailable`), `input_ids[]`, and explanation. Included/summarized entries name actual input IDs. An event excluded from input remains preserved in history. Summarization records a transformation/loss. Unavailable required input blocks readiness. Accounting prevents a consumer from silently using stale context or appending the same tool result twice.

`next_action.kind` is `model_request`, `await_user`, `await_decision`, `reconcile_operation`, or `resume_native`. The latter three bind their request, operation or native-import ID. Pending approvals and unresolved operations MUST be reconciled before an incompatible next action. `await_user` describes a ready waiting state, not permission to invent another user message.

## 4. Typed request context

ASIF 0.3 adds mandatory `kind` to each context input:

| Kind | Additional fields and semantics |
|---|---|
| `message` | Existing role, ordered parts and source events. |
| `tool_call` | Assistant role, `call_id`, `tool_id`, `arguments`, `arguments_status`. Parts may retain associated text. |
| `tool_result` | Tool role, `call_id`, `result_index`, `terminal`, `outcome`, ordered result parts. |

Calls and results correlate by ID in the selected context. Results follow their call; indexes are unique/increasing, and terminal results close the call. A result cannot be matched by adjacent text. Parallel calls retain their identities. Partial arguments cannot become an executable completed invocation. For this profile, every selected result requires its selected call; an unresolved external invocation must first be materialized with provenance or remain blocked.

Source-event mappings MUST agree with call identity and result meaning or report an explicit transformation. Different agents may encode these inputs differently. The assessment must record argument/result conversions, role changes, dropped opaque content and any loss of correlation. A tool name or identical input schema alone does not establish equivalent behavior.

## 5. Workspace snapshots, roots and paths

A workspace record requires `id`, `environment_id`, `root_id`, `at_event_id`, descriptive `source_root`, `mode`, `selection`, `entries[]`, `deletions[]`, and nullable `base_snapshot_id`. Multiple roots are allowed; every root is bound independently at the destination.

`mode` is `snapshot`, `delta`, or `refs`. A snapshot explicitly lists the selected tree. A delta requires an available immutable base and explicit deletions. Refs require named repository prerequisites; a URL or commit alone is not a self-contained workspace. Missing selected files never imply deletion. Excluded paths are protected from implicit deletion.

`selection` records inclusion rules, exclusion rules, and completeness for that selection. Each entry has a portable relative path and `kind`: a file references an immutable resource and mode; a directory has mode; a symlink records its target as data. Payload symlinks remain forbidden. Destination creation of a modeled workspace symlink requires an explicit supported policy; absolute, escaping or unsupported link targets block that restore. No consumer silently dereferences the link into unrelated files.

Optional `git` records object format, nullable HEAD/branch, bundle resources, prerequisites, index entries, submodules and LFS dependencies. Index entries retain stage (including conflicts), mode and blob resource/object identity. A worktree snapshot alone does not establish index fidelity. Unborn repositories have null HEAD; detached HEAD has null branch. Git prerequisites identify immutable objects and their availability. Missing submodule/LFS content lowers completeness and blocks uses that require it.

`cwd` is null or `{root_id, relative_path}`; the empty relative path means the root. `path_references` names the entity type/ID, JSON Pointer to a known path field, root ID and relative path. This authorizes a typed mapping in a newly produced target representation, never mutation of the source document. Free text and shell commands are not rewritten by global substring replacement. Any adapter-specific transformation must identify its exact rule and losses.

Destination `path_bindings` name root, destination path, case sensitivity and Unicode normalization behavior. Importers validate collisions, modes, path containment, drive/UNC differences, dependencies and host filesystem behavior before writes. A path valid on the source is not automatically safe or meaningful on the target.

## 6. Runtime, model and tool dependencies

A dependency identifies kind, implementation identity, accepted versions, platform constraints, `required_for[]`, dependencies, resource IDs and implementation binding. Supported kinds include agent runtime, model, executable, package, skill, plugin, hook, tool, policy, service and resource. Version lists contain exact acceptable versions; an empty list means compatibility is unknown, not unrestricted. A destination can establish another version through explicit compatibility evidence and an adaptation assessment.

Bindings identify `builtin`, `package`, `command`, `service`, or `opaque` implementation and a reference. Command/package references are installation/execution requirements, not instructions to execute during inspection. Required resources include non-code assets used by skills, plugins and hooks. Dependency closure is evaluated before changing source execution or destination files.

Tool dependencies name `tool_id` and a behavior contract: identity, revision, effect class (`none`, `local`, `remote`, `unknown`) and replay classification (`never`, `idempotent`, `reconcile`, `unknown`). These are source declarations that the target must verify. Tool substitutions require argument/result mapping and behavior evidence, including working-directory interpretation, errors, side effects and permission enforcement.

Model requirements identify source provider/model/revision, required capabilities/media types, and overflow policy (`block` or `propose_compaction`). The target records its exact model, tokenizer, input count, supported input limit and reserved output budget. Counting uses the destination's rules and includes instructions, tool definitions and multimodal input. Unknown fit cannot pass a required model assessment. An optional model may be explicitly deferred for waiting or reconciliation.

Changing models, dropping unsupported media, summarizing to fit, or discarding provider-bound opaque state is an explicit adaptation. Proposed compaction creates a new context/capture and loss record; it does not edit the original. The new capture requires a new assessment. A model alias or successful API connection is not evidence of equivalent behavior or identical future answers.

## 7. Effective instructions and policy

A configuration binding names a core `configuration_id`, `effective_order[]`, `instruction_rules[]`, and `policy_ids[]`. Every source instruction occurs exactly once in effective order and has a rule. Every captured policy is accounted for. Scope is `global`, `root`, or `path_prefix`; root and path scopes bind logical roots. Prefix matching uses path components, not string prefixes.

Each rule declares `authority` (`system`, `developer`, `user`, `untrusted`, `unknown`), `group_id`, `merge_behavior`, priority, scope and activation. Authority records the source interpretation; translating its meaning requires a supported target mapping. Unknown authority blocks equivalent continuation. Untrusted material never acquires instruction authority merely by being imported.

Merge behavior is `append`, `replace_same_scope`, `reject_conflict`, or `unknown`. Replacement affects only earlier instructions in the same group with identical authority and scope; it cannot erase broader or higher-authority rules. Reject-conflict requires a supported dialect's conflict evaluation; unknown evaluation blocks equivalence. Activation is `always` or a namespaced `predicate` with expression. Effective order governs evaluation when priorities tie; priority sorts ascending, with later entries applied later. It does not grant lower-authority instructions permission to override higher-authority or destination-enforced restrictions. Resolved instructions already in context are not appended again from configuration metadata.

The destination assesses every instruction, capability and policy separately, including authority, merge/override behavior and enforcing restrictions in the source dialect. Unknown activation predicates or precedence cannot be flattened to unconditional instructions. Unsupported enforcing policy is blocking. A stricter destination restriction is reported and may limit continuation; a weaker destination policy cannot be silently accepted as equivalent.

An effective configuration is required for a ready report. A partial/declared configuration remains assessable but is not equivalent continuation. If an application elects a materially different configuration, it produces a derived capture with explicit changes and assesses that capture. Prior approvals remain evidence and are re-authorized under the target policy.

## 8. Credentials and service bindings

A service binding identifies service, endpoint kind/locator, source account identity, auth method, audience, required scopes, logical secret handles and dependencies. Account IDs must be non-secret identifiers. Tokens, passwords, cookies and signed access URLs do not belong in these fields.

Destination assessment resolves each handle through its credential provider, verifies identity/audience/scopes and connectivity, and records outcome/time/expiry without credential values. A different account is an explicit change, even if its API key works. A localhost endpoint or local socket requires a destination binding; copying its source address is not resolution. Expired evidence and changed endpoints/credentials require reassessment.

Service availability does not authorize an operation. Destination permissions and operation-specific authorization are separate. A missing required login, scope or service blocks only the capabilities that depend on it, and MUST be listed in the report.

## 9. In-flight operations and side effects

An operation records stable ID, optional call ID, kind (`tool`, `process`, `service_job`, `agent`), source-scoped external identity, state (`pending`, `running`, `succeeded`, `failed`, `cancelled`, `outcome_unknown`), effect/replay classification, evidence resources and recovery strategy.

Recovery is `reconcile`, `reconnect`, `restart`, or `refuse`. A recovery record identifies handler dependency, scoped operation/idempotency reference where available, and evidence. An idempotency reference is not a promise that an arbitrary destination can enforce it. Tool retries keep the operation relationship but receive a new invocation ID.

No result means outcome unknown. An importer MUST NOT infer that a command never ran. Reconnect requires verified remote job identity and authorization. Restart requires evidence that previous effects did not occur or that a recognized idempotency mechanism covers them, plus fresh authorization. Unknown replay safety blocks restart. Lost local process memory, PTYs, browser state or child-agent execution cannot be reconstructed merely from a PID or transcript; record unsupported state explicitly.

Each checkpoint open call has an operation binding. Required child sessions/agents are dependencies with explicit resource/identity references. A selected operation can be ready for assessment while the plan remains blocked for model execution. Unresolved side effects are never resolved by a successful file copy.

## 10. Native import and identity

A native-import descriptor names adapter identity/version, source state-format version, accepted target agent versions, required resource IDs and import mode (`copy`, `continue`, `translate`). It declares identity policy, ordering/index contracts and conflict policy. Every required resource is verified before import.

`copy` creates a new target native identity. `continue` may retain native identity only when the destination supports it and conflict/writer checks pass. `translate` records source/target native identities and maps semantic records. Logical session identity and lineage follow core ASIF rules independently of native IDs.

Importers preserve native ordering fields, parent relationships, pagination and index/file consistency according to the named adapter contract. Atomic publication or rollback is required. Existing target state is not overwritten unless an explicit replacement policy and matching baseline digest allow it; conflict or uncertain ownership blocks replacement. This profile does not prescribe a universal native database layout.

The report includes entity identity mappings, target-native identities, path transformations, losses, and actual import outcome. An imported session is not yet a successfully continued session. Verification must discover the intended target identity and complete a real next interaction using expected prior context and any required relative workspace path. A UI opening or generated resume command is insufficient evidence.

## 10a. Action-specific assessment closure

Consumers MUST derive the exact inventory and `required` flags below before interpreting a report. Plan selection inventories a subject; it does not by itself require every selected subject. “Agent action” means `model_request` or `resume_native`; “active action” also includes `reconcile_operation`.

| Next action | Active `required_for` scopes | Directly required action subjects |
|---|---|---|
| `await_user` | `read` | No execution subjects |
| `await_decision` | `read` | Resources in the target request's typed prompt parts |
| `reconcile_operation` | `read`, `continue` | Selected workspaces, services, configuration environments and target operation |
| `model_request` | `read`, `context`, `continue` | Context, model, all instructions, capabilities with `required: true`, selected workspaces/services/operations, configuration environments and selected native import |
| `resume_native` | `read`, `context`, `continue` | Same as `model_request`, including the selected native import |

For every action the plan/boundary, effective configuration, declared required features, enforcing policies and boundary evidence resources are required. Non-enforcing policies remain optional. Every selected dependency is initially required exactly when its `required_for` intersects the active scopes. An empty list supplies no initial requirement; it does not opt out of transitive prerequisites.

1. Inventory the plan, context, model, configuration, its instructions/capabilities/policies, declared required features, selected dependencies/workspaces/services/operations and selected native import. Inventory each selected checkpoint requirement. Inventory environments named by the configuration, selected workspace or any inventoried core requirement, and each of those environments' requirements. IDs are typed; instruction/capability/policy subjects carry their configuration `owner_id`, `checkpoint_requirement` subjects their checkpoint owner, and `environment_requirement` subjects their environment owner.
2. Add directed prerequisite edges: dependency to each `depends_on` dependency; workspace to its environment and flattened file resources, inherited Git bundle/index/prerequisite resources and Git LFS/submodule dependencies; service to its dependencies; operation to its recovery handler and operation/recovery evidence; native import to its resources; context to typed input resources and selected tool-definition resources; instruction to typed part resources; capability, environment and dependency to their resource lists. All referenced dependency IDs MUST be selected and their transitive closure complete.
3. Add an edge from the required plan to each checkpoint requirement whose `required_for` intersects the active scopes. Add an edge from each inventoried environment to each of its requirements with intersecting scopes. Each core requirement points to its declared resource, capability and environment. Requirement secret handles MUST be declared by the selected configuration. Inventory the target of every edge, recursively, even when the parent remains optional.
4. Seed required flags from the table and unconditional subjects above, then repeatedly mark every prerequisite of a required subject required until no flags change. This monotonic union means a resource shared by optional and required consumers is required. Optional capabilities can become required through core requirements. Environment requirements require both a required parent and an applicable scope unless another required edge reaches them.

Only typed references above select resources. Arbitrary JSON inside capability definitions, structured parts or extensions does not select resources merely because a key resembles `resource_id`. Historical resources outside this inventory remain preserved and do not block this action. Invalid references, inconsistent snapshots and malformed declarations still invalidate the source; optionality never repairs invalid structure.

Every inventoried subject MUST have exactly one assessment with the computed flag, including optional subjects. Missing, duplicate, extraneous or incorrectly flagged assessments invalidate the report. A present required assessment with status `omitted`, `unresolved` or `unsupported` is valid but blocks readiness. An optional assessment with those statuses does not block readiness. Deferring an optional subject while retaining its source information needs an explanation, not a fabricated loss. An actual omission transformation MUST record its losses. Adaptations always need transformation mappings; only transformations of required subjects gate this action's readiness.

A supported core requirement MUST include destination evidence and `resolved.status: available`; secret requirements also include the matching handle in `resolved.secret_handles`. A supported reconciliation target MUST have a `reconcile` or `reconnect` recovery strategy, destination evidence, and matching `resolved.recovery_strategy` and non-null `resolved.external_identity`. Its unknown prior outcome does not block reconciliation itself. Pending decisions and pending/running/unknown operations block agent actions. Unsupported recovery cannot be made ready by labeling it reconciliation. Optional subjects claimed supported must pass the same truthfulness checks as required subjects; unavailable source resources cannot be claimed supported.

Required workspaces and optional workspaces claimed supported/adapted need path bindings. Deferred optional workspaces need none. Unknown model fit can be deferred only when the model is optional. Waiting readiness authorizes no native import or agent execution; reconciliation readiness applies only to its target recovery. Successful import claims require an agent action, and successful continuation claims require an active action. Reports remain bound to their specific plan and exact source bytes.

## 11. Destination assessment and receipt

A report is a separate immutable document. It binds the exact source JSON byte SHA-256, session/capture/plan IDs, destination runtime and capability fingerprint, assessment time and expiry. The source hash excludes the report; referenced resource hashes remain verified through the source document. This binding prevents a report for one capture or environment being reused for another. A hash binds bytes, not author authenticity.

`assessments[]` identify typed subjects, `status` (`supported`, `adapted`, `omitted`, `unresolved`, `unsupported`), whether required, explanation, and evidence IDs. Subjects cover the plan/boundary, context, model, selected workspaces, transitive dependencies, service bindings, configuration, every instruction/capability/policy, selected resources, operations, native import and required features. Every applicable subject must occur once. Missing assessment records invalidate the report; a present required assessment with status `omitted` blocks readiness. Optional omissions record losses when information changes.

A supported dependency assessment includes `resolved.identity` and exact `resolved.version`, checked against its allowed versions and destination platform. A supported service assessment includes resolved account, audience, granted scopes, endpoint and resolved secret-handle names. These contain no secret values. Instruction/capability/policy subjects use `owner_id` to identify their configuration, so equal local IDs in different configurations remain distinct. Requiredness is computed from the selected plan and dependency closure; a report cannot downgrade a required subject to optional.

Reports also contain path bindings, identity mappings, transformations, model assessment, blocking reasons, `import_result` and `continuation_result`. Transformations name exact source/target subjects, rule, losses and acceptance evidence; a report cannot rewrite the source or retroactively manufacture evidence. Evidence entries identify producer, time, kind, detail and any immutable report/resource reference. `evaluation_mode` is `synthetic` or `observed`. A synthetic report may illustrate a computed `ready` outcome, but it cannot establish actual readiness, authorize execution or report actual import/continuation success. Consumers MUST refuse its use as operational authorization.

Outcome rules:

- `blocked`: any required subject is unresolved, unsupported or omitted; required context fit is unknown/fails; checkpoint consistency is unknown; configuration is incomplete; required resources are unavailable; or required operation recovery is unresolved. Blocking reasons must identify the subjects.
- `adaptation_required`: no hard blocker, but at least one transformation of a required subject remains unaccepted. No continuation is authorized by this outcome.
- `ready`: every required subject is supported or has a specifically accepted adaptation, required context fits, evidence is current, and no blocking reasons remain. Readiness is specific to the selected next action, destination and unchanged capture.

`import_result` is `not_attempted`, `imported`, `failed`, or `rolled_back`; `continuation_result` is `not_tested`, `continued`, `blocked`, or `failed`. Verified import/continuation claims require corresponding evidence and exact runtime/adapter versions. Readiness is a preflight result, not a continuation test. Any source/destination change invalidates dependent checks and requires reassessment.

## 12. Conformance and evidence limits

Acceptance cases must cover machine-to-machine import, a different OS/path layout, dependency omissions, missing/wrong-account credentials, conditional instructions, unsupported enforcement, in-flight side effects, model/media adaptation, context overflow, native index/ordering requirements, writer conflicts, and rollback after partial import.

The supplied profile checker validates selected semantic invariants and report blocker rules for synthetic fixtures. It does not install tools, resolve credentials, enforce real policies, import vendor stores, coordinate writers or run an agent. Full adapters, broader semantic validation, and independently authored implementations with real continuation tests remain required release evidence.
