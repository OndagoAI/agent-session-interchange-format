# ASIF 0.5 review draft: changes and migration

Review draft dated 5 October 2026. Version 0.5 adds a reproducible destination capability fingerprint contract to the [0.4 baseline](MIGRATION-0.4.md). This is a breaking draft update, not a stable-standard release or a claim of independent interoperability.

## Version matrix

| Contract | Previous | This draft |
|---|---|---|
| Core `asif_version` | `0.4` | `0.5` |
| Session schema ID | `urn:asif:0.4:session` | `urn:asif:0.5:session` |
| Required continuation feature | `asif.portable-continuation/0.2` | `asif.portable-continuation/0.3` |
| Continuation `profile_version` / schema ID | `0.2` / `urn:asif:portable-continuation:0.2` | `0.3` / `urn:asif:portable-continuation:0.3` |
| Destination `report_version` / schema ID | `0.2` / `urn:asif:continuation-report:0.2` | `0.3` / `urn:asif:continuation-report:0.3` |
| Destination snapshot contract | Not defined | `asif.destination-capabilities/0.1`, `snapshot_version: 0.1` |
| Local reference package | `0.4.0` | `0.5.0` |

The continuation contract advances with its destination report requirements. Streams, external bindings, package transport/signatures and local activation/policy dialects retain their existing 0.1 identifiers. Core and profile versions remain exact, independent interpretation contracts. Before 1.0, breaking draft changes increment the minor version under the [governance policy](GOVERNANCE.md).

## Changes from 0.4

[Issue #4](https://github.com/OndagoAI/agent-session-interchange-format/issues/4) replaces unspecified destination fingerprints with [supplied capability snapshots](CAPABILITIES.md):

- Every report supplies immutable snapshot evidence, its exact decoded byte count and SHA-256. The snapshot declares destination/runtime identity, observation/expiry, supported features and component state. No canonicalization or implicit reserialization occurs.
- Every assessment records `component_ids`. Claimed destination support must bind to available components and agree with their typed facts, including model limits, account/access, workspace mapping and recovery identity.
- Unsupported or unavailable snapshots cannot establish report validity. Missing evidence, mismatched bytes, invalid bindings and expired reports are refused.
- Any destination state change invalidates the whole report. Caller-supplied current bytes can be checked with `validate-report --current-capabilities`; this does not probe or authorize a live runtime.

The core tool-call and task semantics introduced for 0.4 remain in effect. See the [earlier migration](MIGRATION-0.4.md) when translating older captures.

## Migration procedure

1. Preserve original capture, snapshot, report and package bytes with their declared versions. Current validators refuse earlier or future contracts; retain the earlier reader/schema for archived data. Do not relabel an immutable historical record.
2. Interpret the source under its original contract, then emit a new derived 0.5 capture with a new capture ID and explicit provenance/lineage. Preserve unchanged source evidence, event identities and uncertainty. Record actual transformations and losses. This update does not require inventing new source history.
3. If using continuation, update both its feature identifier and profile version to 0.3 after validating the resulting document. Do not pair an older continuation contract with a new report and assume equivalent interpretation.
4. Reinspect the destination and supply a snapshot under `asif.destination-capabilities/0.1`. Record the required identities, revisions, capabilities and non-secret access facts. A previous placeholder fingerprint cannot recover this evidence or prove the destination still has its earlier state.
5. Produce a new report at version 0.3, binding the new capture's exact bytes, selected plan, current destination snapshot and refreshed evidence/expiry. Recompute the action-specific inventory, component bindings, required flags, blockers and transformation acceptance. Do not carry old import/continuation success into the new report as evidence of a new action.
6. Rebuild manifests and obtain new signatures for changed package bytes. The unchanged 0.1 package/signature formats still bind exact bytes; old signatures remain evidence only for the original packages.

Consumers without support for the declared core version, required feature or snapshot format must refuse the corresponding interpretation and continuation claims. Opaque preservation does not establish compatibility. No automatic migration command or agent execution is added.

Current examples are rebuilt synthetic fixtures, not migrated user captures. Reports, supplied snapshot copies, object examples, manifests and the public-test-key package signature are regenerated together. Fixed snapshot hash vectors retain their original exact bytes and expected hashes; their declared supported-feature strings are test data, not claims about the current reader. Historical fixture assessment times remain test inputs, not live readiness statements.
