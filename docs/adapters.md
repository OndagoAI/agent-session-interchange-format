# Building an ASIF adapter

An adapter maps a source session into ASIF or maps ASIF into a destination's representation. No vendor adapter is included in the local reference implementations. This guide is a starting workflow for experiments; the [specification](../SPEC.md), [semantics](../SEMANTICS.md) and activated profile rules define the contract.

## Start with a bounded export

Choose one source format and version, one complete example and a clear capture boundary. Describe the first claim you want to test, such as preserving conversation, participants and attachments for inspection. Native import and execution can be later capabilities.

| Source information | ASIF representation | Mapping question |
|---|---|---|
| Session and record identities | Session, capture and entity IDs | Can repeated exports preserve the same logical identities? |
| Authors and messages | Participants and events | Are actor identity and message role both preserved? |
| History selection | Branches and causal references | Which events belong to each selected history? |
| Actual or proposed model inputs | Contexts with explicit fidelity | Do you know the ordered inputs, or only the visible transcript? |
| Files and media | Resources and ordered content parts | Are original bytes present, transformed, redacted or unavailable? |
| Tool activity | Tool definitions, calls and correlated results | Is a terminal outcome known? Is an earlier invocation outside this capture? |
| Instructions and runtime needs | Configurations, environments and requirements | Which semantics are known, and which require a destination mapping? |
| Outstanding work | Checkpoints, tasks and decisions | What is known at this boundary, and what remains unresolved? |

Keep a mapping record and account for unsupported or omitted data using coverage and losses. Preserve unknown optional data directly or through recoverable source data and a mapping receipt. Missing effective inputs must not become an `exact` context. See the existing [field mapping](field-mapping.md) for comparisons of source representations.

## Validate and inspect the export

Use either CLI against the produced document:

```sh
node asif.ts validate /path/to/export.session.json
# Substitute an actual context ID from your document:
node asif.ts request /path/to/export.session.json CONTEXT_ID
```

The request command supports a neutral projection of reconstructed or exact inputs within its stated limits. An unsupported result is useful evidence to record; it is not permission to drop those semantics. Check resource bytes and stable IDs across repeat exports, preserve separate identities for repeated messages, and test missing inputs and unresolved tool outcomes.

## Assess a destination

For a continuation claim, build the [portable-continuation profile](../CONTINUATION.md) and a separate destination report. Bind the report to the source bytes and selected plan. Assess workspace mapping, dependencies, tool behavior, configuration, services, model fit and unresolved operations for the actual destination.

Account for each adaptation and its acceptance. A destination needs its own authorization and access. Follow the profile's native-import, writer-coordination and rollback requirements for changes to a native store. An unresolved side effect needs reconciliation before a repeat action can be considered.

The [synthetic scenarios](../examples/continuation/README.md) explain the record structure. Their invented checks and historical timestamps cannot substitute for live destination observations.

## The first live handoff

Aim for one small, reproducible task and retain evidence at each stage:

1. **Capture:** record a real source session, source/runtime version, adapter revision and export boundary. Keep a shareable fixture or explain the reproducible sanitization.
2. **Assess:** run destination checks and retain the report, explicit blockers, transformations and any required acceptance. Record destination versions and capability identity.
3. **Import:** under destination authorization, perform the supported import and preserve its receipt and identity mappings. Record failures or rollback outcomes.
4. **Continue:** demonstrate an actual next interaction that uses transferred information, such as answering a recorded unresolved question using a transferred file. Retain observed output and relevant tool results.
5. **Return:** export the updated session, check preserved identities and resources, and account for lost or adapted state.
6. **Reproduce:** publish the exact commands, revisions, fixture digests and outcomes so another developer can repeat the experiment without an Ondago product or account.

Keep a failed or blocked run as evidence of its actual outcome. Even a successful handoff between integrations with shared authorship does not satisfy the independent-implementation gate. Broader claims require additional sources, destinations, adverse cases and independent reports.

## Report the result

Use the [implementation evidence requirements](../IMPLEMENTERS.md) and link the report from a [GitHub issue](https://github.com/OndagoAI/agent-session-interchange-format/issues/new) or pull request. State read, interchange, context reconstruction and continuation results separately. The [compatibility matrix](compatibility.md) can then link to evidence for the exact scope demonstrated.
