# ASIF session conformance plan

The schemas validate structure. The fixture checkers additionally exercise embedded resource integrity and selected core/profile semantic rules. They do not provide a complete semantic validator, actual provider request reconstruction or real continuation.

## Reproduce current structural checks

Requires Python 3.11+ and the pinned dependencies in requirements.txt:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tests/check_schema.py
.venv/bin/python tests/check_examples.py
.venv/bin/python tests/check_continuation.py
.venv/bin/python tests/check_reference.py
.venv/bin/python tests/check_documentation.py
```

The checks verify the schema itself, the synthetic example, and selected structural rejection cases. Results name this limited scope explicitly.

The [example corpus](examples/README.md) adds six attachment-focused sessions to the existing approval example. Its separate checker validates document shape, embedded lengths/digests, selected local references and branch/context boundaries, plus targeted rejection cases. External locators are never fetched. These fixture checks do not implement every semantic rule or establish interoperability.

The [continuation scenarios](examples/continuation/README.md) add three complete session/profile documents and three destination reports. Tests cover typed tool context, exact checkpoint/configuration bindings, dependency closure and resources, path selectors/collisions, authority, service identity, native version gating, unsafe restart refusal, report source hashes/expiry, model fit, missing assessments and adaptation acceptance. All destination evidence is synthetic. No tests install tools, obtain credentials, mutate a native store or start an agent.

The checker conservatively assesses every selected dependency/resource as required. More selective `required_for` evaluation, cryptographic runtime-evidence validation and complete Git restoration are not implemented. The local reference now adds bounded parsing, exact-byte package signatures, neutral context/configuration interpretation, stream assembly and staged selected-tree restoration; its supported scope and limitations are listed in [REFERENCE.md](REFERENCE.md). Profile schema validity alone cannot establish those capabilities.

## Required acceptance cases

| Capability | Fixture | Required interpretation |
|---|---|---|
| Read | Simple chat, no timestamps | Keep content/roles/order; do not invent time or tools. |
| Read | Empty tools with `not_inspected` coverage | Tool history is unknown, not known absent. |
| Read | Repeated identical messages | Preserve separate event identities. |
| Read | Multimodal input with unavailable bytes | Keep resource identity/type and explain absence. |
| Interchange | Unknown optional data | Survives export or is recoverable through preserved source plus receipt. |
| Interchange | Required unknown event extension | Refuse the unsupported semantic capability. |
| Interchange | Branch, edit, retry, merge | Preserve each selected history, fork boundaries and explicit context. |
| Interchange | Parallel tool calls and streamed results | Match call IDs and chunk indexes; terminal state is explicit. |
| Interchange | Missing terminal tool result | Outcome unknown; no automatic repeat of a possible side effect. |
| Interchange | Approval without answer | Pending only with evidence; otherwise outcome unknown. |
| Interchange | Task revisions and plan approval | Resolution applies to the exact named revision. |
| Context | Transcript includes records absent from request | Reconstruct ordered context inputs without replaying every event. |
| Context | Compaction | Preserve summary, retained inputs, source coverage and prior context. |
| Context | Scoped instructions and unknown policy | Report unresolved equivalence; do not claim exact configuration. |
| Continue | Example awaiting approval | Readable; continuation blocked until outcome/policy/configuration are resolved. |
| Continue | Missing required skill, secret or media | Name the prerequisite and block the affected capability. |
| Continue | Complete checkpoint on supported runtime | Demonstrate a next interaction, record destination versions and transformation report. |
| Continue | Same agent on another computer/OS | Restore the selected root, resolve paths/dependencies, discover the intended native session and use a relative file path in a real next interaction. |
| Continue | Another agent | Map typed calls/results, instructions, tool behavior, native identities and model/media requirements; account for and accept adaptations before execution. |
| Continue | Operation with unknown external outcome | Reconcile its scoped identity; do not repeat a possible side effect. |
| Continue | Wrong account, expired login or unsupported enforcement | Keep the plan blocked and identify the exact subject. |
| Continue | Changed capture or destination after preflight | Invalidate the earlier assessment and re-evaluate affected requirements. |
| Continue | Partial native import or target writer conflict | Refuse/roll back without damaging original source or conflicting destination state. |
| Integrity | Duplicate IDs, cycles, wrong head, missing references | Reject as semantic invalidity. |
| Integrity | Resource hash mismatch or unsafe path | Reject; never resolve arbitrary host paths. |

These are **acceptance requirements**, not claims that the tests already exist. Real fixtures must include non-coding sessions, multi-agent participation and partial captures.

## Evidence record

Each implementation report identifies authorship/affiliation, code revision, ASIF/schema/profile versions, fixture digest, supported limits, commands, passes/failures/unsupported cases, and capability claims. Bidirectional exchange requires independently produced input as well as consumption of the shared corpus.

Current session implementations: **Python and TypeScript ports of one locally authored reference subset**. Current independent interoperability results: **none**. The examples, schemas, documentation checks and local runtime checks are reproducible review evidence, not a complete conformance certification.

## TypeScript and cross-language checks

On Node.js 24+, run `npm ci`, `npm run typecheck`, and `npm test`. The TypeScript suite includes the 44 continuation outcomes exported from the Python checks plus its own parser, state, workspace, package and CLI cases. It explicitly tests unsupported numeric and ZIP representations.

With the Python environment and Node available, run `.venv/bin/python tests/check_typescript_exchange.py` to verify packages/signatures produced by each CLI using the other CLI. The checker also compares request/report/redaction outputs and restored bytes. Use `.venv/bin/python tests/build_typescript_parity.py` to refresh shared expected results when the Python continuation tests change.

Results: [TypeScript checks](tests/typescript-results.json) and [cross-language exchange](tests/typescript-exchange-results.json). Shared authorship means independent interoperability remains unproven.
