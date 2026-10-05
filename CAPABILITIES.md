# Destination capability snapshots 0.1

Contract: `asif.destination-capabilities/0.1`. Status: normative review proposal in the ASIF 0.5 draft, with portable continuation and destination reports at 0.3. This snapshot format begins at 0.1.

A destination report binds both the immutable source capture and the destination state against which its assessments were made. `destination.capabilities_sha256` is SHA-256 over the exact supplied snapshot bytes defined here. It is not a digest of a runtime name, selected fields, a parsed object or an unspecified adapter cache. Fingerprints bind evidence; they do not authenticate its producer or prove the destination still has that state.

## Snapshot and supplied evidence

The [Capability Snapshot Object](docs/report-objects.md#capability-snapshot-object) has `snapshot_version: "0.1"`, a snapshot ID, destination ID, producer, evaluation mode, observation time, expiry, runtime, runtime revision, supported feature identifiers and component inventory. The schema lives at `#/$defs/capability_snapshot` in the [destination report schema](schemas/continuation-report.schema.json). The snapshot does not contain its own digest or the report digest.

The destination ID and runtime MUST equal the report's declarations. Runtime includes agent identity/version/state format, adapter identity/version, OS and architecture. `runtime_revision` is an opaque, non-secret revision token for the assessed runtime deployment and its global settings. It MUST change when any runtime state affecting interpretation, permissions or execution changes, even if the software version remains the same. A missing version remains unknown and cannot establish version compatibility.

Each [Capability Component Object](docs/report-objects.md#capability-component-object) names a destination-local ID, kind, implementation identity, version or explicit unknown, non-secret revision token, and status (`available`, `unavailable`, `unknown`). Component IDs MUST be unique within the snapshot. A revision is not a content digest: its producer MUST change it whenever relevant state changes. Consumers compare tokens as opaque, case-sensitive strings and MUST NOT infer capabilities from their spelling. In particular, an arbitrary token cannot substitute for inspection/compatibility evidence establishing the assessment.

Additional fields are mandatory for model, service, workspace and operation components. The full inventory used by the assessed plan MUST be supplied, including transitive prerequisites. It need not disclose unrelated installed software or accounts. An empty inventory or feature list means none is declared for this snapshot, not universal support. The report's component bindings enforce coverage for claimed support; omitted components cannot justify it.

| Component | Required contents and changes that require a new revision/snapshot |
|---|---|
| `dependency` | Implementation identity/version; revision covers executable/package/skill/plugin/hook/tool behavior, argument/result schemas, effects, replay semantics, dependencies and effective settings. |
| `configuration`, `policy`, `capability` | Identity/version plus revision of the actual effective instructions, scope/activation/precedence, enforcing rules or capability implementation. Any behavior or enforcement change invalidates the assertion. |
| `model` | Exact provider/model/revision, tokenizer or unknown, input limit or unknown, supported media types and capabilities. Model routing, tokenizer, budgeting rules and actual limit changes require a new revision. |
| `service` | Non-secret account identity, audience, granted scopes, logical secret handles and endpoint or unknown. Account/tenant/endpoint changes, granted-access changes, login expiry/revocation and credential rotation affecting access require a new revision. |
| `workspace` | Logical root ID, destination path, case sensitivity and Unicode normalization. Revision covers selected file bytes, modes, symlinks, Git/index/submodule/LFS state, mount/access state and path bindings. |
| `operation` | Recovery strategy and external namespace/identity or explicit unknown. Remote outcome, recovery/reconnect availability and authorization changes require a new revision. |
| `native_import` | Adapter/format identity/version; revision covers target-store baseline, indexes, writer coordination and applicable import permissions. |
| `environment` | Identity/version and revision of the resolved environment or core prerequisite, including prerequisite availability and access. |

Credentials, cookies, bearer tokens, private keys, authorization headers and secret-bearing URLs MUST NOT appear in the snapshot or revision tokens. `secret_handles` are logical references only. Credential rotation is represented by a changed access revision, never credential bytes or a hash of a credential. Producers may use random opaque revision tokens to avoid exposing sensitive state. Unknown extensions are preserved; they do not silently grant support. Extensions essential to interpretation require a new snapshot format contract.

The report includes a [Snapshot Evidence Object](docs/report-objects.md#snapshot-evidence-object) at `destination.capabilities_snapshot`, with the format identifier, availability and `evidence_id`. For `supplied`, `data` contains the exact snapshot bytes as canonical padded base64 and `bytes` gives their decoded length. For `unavailable`, an explanation is mandatory and neither `data` nor `bytes` is permitted. A locator or digest without supplied bytes is insufficient under this contract; consumers MUST NOT fetch an arbitrary URL to complete verification.

The referenced report evidence MUST exist, name the same producer, have the same observation instant and use kind `synthetic` for a synthetic snapshot or `inspection` for an observed one. Snapshot and report evaluation modes MUST match. Synthetic snapshots cannot justify observed execution. Evidence remains an assertion whose authenticity and trust must be established outside this fingerprint contract.

## Exact bytes and verification

1. Check the supported format and supplied evidence. Missing required fields are invalid. An explicitly unavailable snapshot or unknown format/version is unsupported: refuse verification and reuse of the report, regardless of its claimed outcome. This is not an optional assessment that can be dropped to make the report ready.
2. Decode strict, canonical padded base64. Verify decoded length and lowercase SHA-256 against `capabilities_sha256` before interpreting the JSON. This format limits snapshots to 1 MiB of decoded bytes. Oversized inputs, malformed encodings, wrong lengths and mismatched digests are invalid.
3. Parse those exact bytes as UTF-8 JSON, without a byte-order mark, duplicate member names or non-JSON constants. Whitespace, line endings, key ordering, Unicode spelling/escaping and any trailing whitespace are included in the digest. No canonicalization, Unicode normalization or implicit reserialization is performed. Unsupported numeric representations must be refused rather than rounded by an implementation.
4. Validate the snapshot object and all component IDs, kind-specific fields, bindings and destination identity. Report assessment, snapshot observation/expiry and referenced evidence timestamps use ISO 8601 calendar timestamps with seconds, at most millisecond precision, and `Z` or an explicit `±hh:mm` offset; timezone-less values and leap seconds are invalid. Require `observed_at <= assessed_at < report.expires_at <= snapshot.expires_at`, and observation at or before the evaluation time. Both the report and snapshot must remain unexpired.
5. Validate report component references and their supported facts as described below. The original source-byte hash and action-specific prerequisite rules still apply independently.

The [fixed hash vectors](tests/capability-snapshot-vectors.json) encode the same valid object with literal UTF-8, JSON escapes, different key order and CRLF whitespace. Their expected digests differ. Python and TypeScript test the exact bytes against the committed lengths and digests; the digests were also checked with `shasum -a 256`. These are reproducible shared-author fixtures, not independent interoperability evidence.

## Assessment bindings

Every assessment includes `component_ids`, even when empty. IDs MUST exist in the supplied snapshot and MUST be unique within that list. For a `supported` or `adapted` assessment, every referenced component MUST be available and exactly one MUST have the matching kind below. Additional prerequisite components may be named, but cannot replace the matching component.

| Assessment subject | Matching component kind |
|---|---|
| Dependency | `dependency` |
| Configuration or instruction | `configuration` |
| Capability or policy | `capability` or `policy`, respectively |
| Model or context | `model` |
| Workspace, service, operation, native import, environment | Corresponding kind |
| Checkpoint or environment requirement | `environment` describing the resolved prerequisite |
| Plan/boundary or resource | No destination component required; source evidence still applies |
| Required feature | No component required; the exact identifier must occur in `supported_features` when claimed supported/adapted |

Supported dependency identity/version and service account/audience/endpoint/access MUST agree with their snapshot components. Granted scopes and resolved logical handles cannot exceed those recorded in the snapshot. Model/context bindings MUST match the assessed target model and, when fit is measured, its tokenizer and input limit. A supported model must also declare the requested capabilities and media types. Workspace components MUST identify the assessed source workspace's logical root and its exact report path binding. Supported reconciliation MUST match the component's recovery strategy and external identity. An unavailable or unknown component cannot establish support, even for an optional subject.

Revision tokens identify the configuration or behavior assessed; they do not encode equivalence algorithms. Adapters must provide the existing assessment/compatibility evidence for that named revision. Adapted targets still require explicit mappings, recorded losses and the acceptance rules in the [continuation contract](CONTINUATION.md). A fingerprint does not turn unknown access, model fit or source resources into supported facts.

## Changes, expiry and report reuse

Version 0.1 deliberately uses **whole-report invalidation**. Any changed snapshot bytes invalidate reuse of every assessment, including previously accepted transformations and optional subjects. Changes in the table above MUST produce a new snapshot/revision and a new report. There is no implicit per-field or per-component reuse algorithm in this version. Producers may collect fresh evidence for unchanged components, but MUST issue a newly bound report and re-establish the complete assessed plan.

Before operational use, a consumer MUST obtain current snapshot evidence from its trusted destination integration, verify its provenance, check expiry, and compare its exact bytes with the report-bound bytes. Inability to obtain current evidence means currentness is unverified, not that nothing changed. Destination state must remain unchanged between checking and acting; an integration must coordinate writers or recheck its generation/revisions at use. Expiry is an upper bound and never excuses a known state change. Reformatting identical JSON also changes the fingerprint and requires a newly bound report.

The reference `validate-report` command verifies the supplied archive by default and returns `current_snapshot_matches: false`. `--current-capabilities <snapshot.json>` additionally compares caller-supplied current bytes and returns `true` only on an exact match. Changed bytes are invalid for reuse (exit 2); unavailable/unsupported snapshot contracts produce exit 3. The flag does not probe a destination, authenticate evidence, grant permission or execute an agent. `operational_authorization` remains false in both cases.

## Draft compatibility

Old reports containing only an invented or unspecified fingerprint cannot meet this contract. Reinspect the destination, supply a snapshot and component bindings, and issue a new report; do not retrofit new claims into an immutable historical report. Captured event and task semantics are unchanged by this destination contract; adopting the new core version still requires a derived capture under the migration rules. The [0.5 migration](MIGRATION.md) advances the continuation and report contracts to 0.3 for these changes. Existing archived reports may be preserved under their original interpretation, but must not be reused as current validated evidence.
