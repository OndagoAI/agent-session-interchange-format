# Portable-continuation scenarios

These examples use ASIF **0.3** and `asif.portable-continuation/0.1`. All agent names, native formats, dependency behavior and destination checks are invented. Each report has `evaluation_mode: synthetic`, `import_result: not_attempted`, and `continuation_result: not_tested`. Even the example with outcome `ready` cannot authorize a real import or execution.

| Scenario | Source document | Destination report | Main behavior |
|---|---|---|---|
| Another computer/cloud runtime | [Session](another-computer.session.json) | [Report](another-computer.report.json) | macOS/ARM source to Linux/x86 destination; logical project root maps to `/work/project`; selected files, skill resource, native-state requirements and typed tool history are carried. The report illustrates a simulated `ready` outcome for native-resume preflight. |
| Another agent | [Session](another-agent.session.json) | [Report](another-agent.report.json) | Agent/runtime, tool, model and native format change. Mappings and loss descriptions are explicit; `adaptation_required` prevents those unaccepted transformations from silently becoming continuation. |
| Unresolved remote operation | [Session](pending-remote-operation.session.json) | [Report](pending-remote-operation.report.json) | A publish call has no result. Operation identity, service account/scopes and secret handle are retained. Unknown effect and unresolved login leave the plan `blocked`; no automatic retry occurs. |

## Follow the bindings

1. The plan selects a checkpoint, continuation context and effective configuration.
2. The checkpoint and selected workspace refer to the same branch boundary.
3. Context inputs retain explicit `message`, `tool_call` and `tool_result` kinds, including call IDs. Configuration instructions are already present in the selected input list and must not be appended again.
4. Context accounting names how every selected event contributes to the next input. Tool history is not reconstructed by guessing from prose.
5. Dependencies include skill resources and tool behavior, not just tool argument schemas.
6. The report binds exact source JSON bytes and destination capability identity, with an assessment for each applicable subject, including optional subjects.

The source environment records its original working directory descriptively. A typed JSON Pointer identifies the corresponding path field for target mapping. Source bytes stay unchanged; any target-native representation is a separate product of import.

## Test expectations

- Changing source JSON bytes invalidates its report hash, even if the JSON remains structurally valid.
- Moving the selected context/workspace to an older event invalidates the checkpoint binding.
- A missing required skill file, unknown authority, wrong service account or unresolved operation cannot be marked supported.
- A supported dependency needs a resolved implementation/version and platform match.
- An adapted model/tool/runtime needs a mapping and acceptance; context limits are assessed using the destination model.
- Synthetic evidence cannot establish actual import or continuation success.

The reports intentionally contain historical fixture times. `tests/check_continuation.py` evaluates them at the fixed time `2026-09-26T12:30:00Z`. Operational consumers would compare with the actual current time and destination state; these fixtures are not live readiness statements.

Run `.venv/bin/python tests/check_continuation.py` from the project root. Regenerate with `.venv/bin/python examples/build_continuation_examples.py`. The original three documents use inline resources; no file attachments, network retrieval or credentials are required to read them. The earlier attachment examples remain separate.

## One capture, five next actions

[One unchanged capture](action-specific.session.json) contains missing model media, an optional formatting asset, a pending decision and an unknown remote job outcome. Each report binds the same source bytes and a different plan.

| Action | Report | Expected outcome |
|---|---|---|
| Await user | [Report](action-specific.report.json) | Ready; execution prerequisites deferred |
| Await decision | [Report](action-specific-await_decision.report.json) | Ready; decision prompt available |
| Reconcile operation | [Report](action-specific-reconcile_operation.report.json) | Ready; target identity and recovery prerequisites assessed |
| Model request | [Report](action-specific-model_request.report.json) | Blocked by required media, unknown model fit, pending decision and operation |
| Resume native | [Report](action-specific-resume_native.report.json) | Blocked by the same agent prerequisites |

Regenerate this capture and its five reports with `examples/build_action_examples.py` after the original generator. Missing media remains explicitly unavailable; none of these synthetic outcomes demonstrates real execution.

## Supplied destination snapshots

Every report now embeds an exact-byte capability snapshot and binds assessments to its components. The corresponding `.capabilities.json` file is a readable copy of those same bytes, for example [another computer](another-computer.capabilities.json), [another agent](another-agent.capabilities.json) and [remote operation](pending-remote-operation.capabilities.json). Both example generators rebuild reports and snapshots together. Snapshot declarations and revision tokens are invented; they contain no credentials or live observations.

The [snapshot contract](../../CAPABILITIES.md) defines exact hashing, currentness, component coverage and invalidation. [Fixed hash vectors](../../tests/capability-snapshot-vectors.json) cover different byte representations of the same object. The current fixture hashes are reproducible; they are not stand-ins for unspecified capability data.
