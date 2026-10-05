# ASIF 0.4 review draft: changes and migration

Historical notes for the 0.4 contract. See [migration to the current 0.5 draft](MIGRATION.md) for the next compatibility boundary.

Published for review on 5 October 2026. This is a compatibility boundary for the evolving draft, not a stable-standard release or a claim of independent interoperability. The local Python and TypeScript implementations share authorship. [Governance](GOVERNANCE.md) still defines the review and evidence gates.

## Version matrix

| Contract | Previous | This draft |
|---|---|---|
| Core `asif_version` | `0.3` | `0.4` |
| Session schema ID | `urn:asif:0.3:session` | `urn:asif:0.4:session` |
| Required continuation feature | `asif.portable-continuation/0.1` | `asif.portable-continuation/0.2` |
| Continuation `profile_version` / schema ID | `0.1` / `urn:asif:portable-continuation:0.1` | `0.2` / `urn:asif:portable-continuation:0.2` |
| Destination `report_version` / schema ID | `0.1` / `urn:asif:continuation-report:0.1` | `0.2` / `urn:asif:continuation-report:0.2` |
| Local reference package | `0.3.0` | `0.4.0` |

The continuation profile and report advance because action-specific requiredness and report subjects changed. Streams, external bindings, package transport/signatures, and the local activation/policy dialects retain their `0.1` identifiers and contracts. Core and profile versions are independent: changing one does not implicitly reinterpret another.

## Changes since the earlier 0.3 draft

- [Tool-call progression](https://github.com/OndagoAI/agent-session-interchange-format/issues/1): immutable partial/unknown calls can progress through an explicit selected supersession chain, preserving logical call identity and previously recorded results. Complete calls cannot be amended this way; retries keep separate identities. Context must retain evidence of the original partial inputs.
- [Task revisions and dependencies](https://github.com/OndagoAI/agent-session-interchange-format/issues/2): dependencies name local tasks at the selected branch boundary. Revision snapshots replace prior dependency lists; omitted and empty have distinct meanings. Cycles are rejected, incomplete predecessor history needs explicit partial coverage, and terminal-task reopening needs an explanation. Task corrections use `previous_revision`, not event-envelope supersession.
- [Action-specific continuation](https://github.com/OndagoAI/agent-session-interchange-format/issues/3): a deterministic prerequisite closure computes exact assessment subjects and required flags for each next action. Environment and core requirement subjects, recovery evidence, optional deferral and action-scoped readiness now have defined interpretation. The [same-capture examples](examples/continuation/README.md#one-capture-five-next-actions) demonstrate the differences.

The rules and implementation changes were developed before this identifier bump; this PR separates the version boundary and migration material from their implementation. See [session semantics](SEMANTICS.md) and [continuation semantics](CONTINUATION.md) for the normative contract, and [reference limits](REFERENCE.md) for the implemented subset.

## Producer and consumer migration

1. Preserve original captures and their exact bytes. Do not relabel an existing capture or overwrite its report. Keep the previous reader/schema with archived data when needed; the current reference validators accept the exact current version and refuse earlier, future and missing versions.
2. Interpret a source under its declared version before translating it. Check tool-call progression, task references/revisions/coverage, context evidence and checkpoint state against the new rules. If the source lacks evidence, preserve the uncertainty or refuse the translation; a version-string replacement cannot repair invalid or ambiguous semantics.
3. Emit a new derived capture with a new capture ID and explicit provenance/lineage connecting it to the original. Preserve source evidence and immutable event identities where meanings remain unchanged. Record any transformed records and losses rather than silently changing their meaning. Update the core identifier only after validating the resulting 0.4 document.
4. For continuation, update both the required feature identifier and profile version to 0.2 after checking the new action-specific contract. Recompute the complete subject inventory, required flags, destination bindings, transformation acceptance and blockers. A previous all-required report is not automatically a valid 0.2 assessment.
5. Issue a new report with `report_version: 0.2`, binding the new capture's exact serialized bytes, plan and destination state. Refresh assessment evidence and expiry. Any changed source bytes invalidate the old report hash; imported or continued outcomes cannot be copied as evidence for a different action or capture.
6. Rebuild package manifests for changed bytes and produce new signatures through the appropriate signing authority. Old package signatures remain evidence for their original packages only. The transport and signature formats themselves stay at 0.1.

A consumer that does not understand the declared core version or a required feature MUST refuse interpretation and continuation claims. Opaque preservation does not confer support. The reference tools do not provide an automatic migration command or execute agents.

The checked-in examples are rebuilt synthetic fixtures for this draft, not migrated user captures. Their reports, package inventory, public-test-key signature and generated object examples are regenerated together. Their fixed historical assessment times remain test inputs, not live readiness statements.
