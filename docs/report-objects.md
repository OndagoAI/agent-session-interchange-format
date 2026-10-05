# Destination report object reference

Version: **0.3**. [Specification](../SPEC.md) · [Core](objects.md) · [Continuation](continuation-objects.md) · [Reports](report-objects.md)

Every example below is JSON Schema checked. Object fragments use IDs resolved by an enclosing session or report; they are not standalone session documents. Full scenarios are in [examples](../examples/README.md). Required means unconditionally required; conditional rules follow each table. Normative [session semantics](../SEMANTICS.md) and [continuation rules](../CONTINUATION.md) also apply.

## Contents

- [Destination Report Object](report-objects.md#destination-report-object)
- [Source Object](report-objects.md#source-object)
- [Destination Object](report-objects.md#destination-object)
- [Path Bindings Object](report-objects.md#path-bindings-object)
- [Identity Mappings Object](report-objects.md#identity-mappings-object)
- [Model Assessment Object](report-objects.md#model-assessment-object)
- [Blocking Reasons Object](report-objects.md#blocking-reasons-object)
- [Import Result Object](report-objects.md#import-result-object)
- [Continuation Result Object](report-objects.md#continuation-result-object)
- [Runtime Object](report-objects.md#runtime-object)
- [Runtime Adapter Object](report-objects.md#runtime-adapter-object)
- [Agent Object](report-objects.md#agent-object)
- [Model Object](report-objects.md#model-object)
- [Subject Object](report-objects.md#subject-object)
- [Assessment Object](report-objects.md#assessment-object)
- [Assessment Resolved Object](report-objects.md#assessment-resolved-object)
- [Assessment Resolved Account Object](report-objects.md#assessment-resolved-account-object)
- [Assessment Resolved External Identity Object](report-objects.md#assessment-resolved-external-identity-object)
- [Capability Component Object](report-objects.md#capability-component-object)
- [Capability Snapshot Object](report-objects.md#capability-snapshot-object)
- [Snapshot Evidence Object](report-objects.md#snapshot-evidence-object)
- [Evidence Object](report-objects.md#evidence-object)
- [Transformation Object](report-objects.md#transformation-object)
- [Result Object](report-objects.md#result-object)

<a id="destination-report-object"></a>

## Destination Report Object

An expiring assessment bound to exact source bytes and a particular destination. Synthetic reports cannot claim execution.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="destination-report-object-report_version"></a>`report_version` | `"0.1"` | Yes | Version of the destination-report format. |
| <a id="destination-report-object-evaluation_mode"></a>`evaluation_mode` | enum | Yes | Whether evidence is observed or synthetic; synthetic results cannot claim execution. One of `"synthetic"`, `"observed"`. |
| <a id="destination-report-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="destination-report-object-source"></a>`source` | [Source Object](report-objects.md#source-object) | Yes | Source identity and boundary or report binding. |
| <a id="destination-report-object-destination"></a>`destination` | [Destination Object](report-objects.md#destination-object) | Yes | Identity and capability snapshot of the assessed destination. |
| <a id="destination-report-object-assessed_at"></a>`assessed_at` | string | Yes | Time at which the assessment was made, including timezone. Minimum length: `1`. |
| <a id="destination-report-object-expires_at"></a>`expires_at` | string | Yes | Exclusive expiry time after which the assessment must be refreshed. Minimum length: `1`. |
| <a id="destination-report-object-outcome"></a>`outcome` | enum | Yes | Recorded result or assessment outcome; unknown remains explicit. One of `"ready"`, `"blocked"`, `"adaptation_required"`. |
| <a id="destination-report-object-assessments"></a>`assessments` | array of [Assessment Object](report-objects.md#assessment-object) | Yes | Subject-specific support, adaptation and blocker declarations. Minimum items: `1`. |
| <a id="destination-report-object-path_bindings"></a>`path_bindings` | array of [Path Bindings Object](report-objects.md#path-bindings-object) | Yes | Destination paths and comparison rules for selected logical roots. Minimum items: `0`. |
| <a id="destination-report-object-identity_mappings"></a>`identity_mappings` | array of [Identity Mappings Object](report-objects.md#identity-mappings-object) | Yes | Explicit mappings of source IDs into destination namespaces. Minimum items: `0`. |
| <a id="destination-report-object-transformations"></a>`transformations` | array of [Transformation Object](report-objects.md#transformation-object) | Yes | Declared adaptations and their acceptance state. Minimum items: `0`. |
| <a id="destination-report-object-model_assessment"></a>`model_assessment` | [Model Assessment Object](report-objects.md#model-assessment-object) | Yes | Target-model selection and context-fit measurement. |
| <a id="destination-report-object-blocking_reasons"></a>`blocking_reasons` | array of [Blocking Reasons Object](report-objects.md#blocking-reasons-object) | Yes | Reasons tied to subjects that prevent readiness. Minimum items: `0`. |
| <a id="destination-report-object-evidence"></a>`evidence` | array of [Evidence Object](report-objects.md#evidence-object) | Yes | Recorded evidence referenced by assessments, transformations and results. Minimum items: `0`. |
| <a id="destination-report-object-import_result"></a>`import_result` | [Import Result Object](report-objects.md#import-result-object) | Yes | Observed or explicitly unattempted native import outcome. |
| <a id="destination-report-object-continuation_result"></a>`continuation_result` | [Continuation Result Object](report-objects.md#continuation-result-object) | Yes | Observed or explicitly untested continuation outcome. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "report_version": "0.1",
  "evaluation_mode": "synthetic",
  "id": "assessment-pending-remote-operation",
  "source": {
    "session_id": "session-pending-remote-operation",
    "capture_id": "capture-pending-remote-operation",
    "plan_id": "continue-main",
    "document_sha256": "966361de8e573d9c451c09f108e695de169d9a8736956b34ec9c93a0b3ed3837"
  },
  "destination": {
    "id": "example-cloud-runtime",
    "runtime": {
      "agent": {
        "id": "example-agent-a",
        "version": "1",
        "state_format": "example-native/1"
      },
      "adapter": {
        "id": "example-adapter",
        "version": "1"
      },
      "os": "linux",
      "architecture": "x86_64"
    },
    "capabilities_sha256": "1a659c7d45e049f81c1207e093efa003486c4849ba9725005b7feacc159bb4a5",
    "capabilities_snapshot": {
      "format": "asif.destination-capabilities/0.1",
      "availability": "supplied",
      "data": "ewogICJzbmFwc2hvdF92ZXJzaW9uIjogIjAuMSIsCiAgImlkIjogInNuYXBzaG90LWFzc2Vzc21lbnQtcGVuZGluZy1yZW1vdGUtb3BlcmF0aW9uIiwKICAiZGVzdGluYXRpb25faWQiOiAiZXhhbXBsZS1jbG91ZC1ydW50aW1lIiwKICAicHJvZHVjZXIiOiAiYXNpZi1leGFtcGxlcyIsCiAgImV2YWx1YXRpb25fbW9kZSI6ICJzeW50aGV0aWMiLAogICJvYnNlcnZlZF9hdCI6ICIyMDI2LTA5LTI2VDEyOjAwOjAwWiIsCiAgImV4cGlyZXNfYXQiOiAiMjAyNi0wOS0yNlQxMzowMDowMFoiLAogICJydW50aW1lIjogewogICAgImFnZW50IjogewogICAgICAiaWQiOiAiZXhhbXBsZS1hZ2VudC1hIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJzdGF0ZV9mb3JtYXQiOiAiZXhhbXBsZS1uYXRpdmUvMSIKICAgIH0sCiAgICAiYWRhcHRlciI6IHsKICAgICAgImlkIjogImV4YW1wbGUtYWRhcHRlciIsCiAgICAgICJ2ZXJzaW9uIjogIjEiCiAgICB9LAogICAgIm9zIjogImxpbnV4IiwKICAgICJhcmNoaXRlY3R1cmUiOiAieDg2XzY0IgogIH0sCiAgInJ1bnRpbWVfcmV2aXNpb24iOiAic3ludGhldGljLXJ1bnRpbWUtMSIsCiAgInN1cHBvcnRlZF9mZWF0dXJlcyI6IFsKICAgICJhc2lmLnBvcnRhYmxlLWNvbnRpbnVhdGlvbi8wLjEiCiAgXSwKICAiY29tcG9uZW50cyI6IFsKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0xIiwKICAgICAgImtpbmQiOiAibW9kZWwiLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS9tb2RlbC1hIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIiwKICAgICAgIm1vZGVsIjogewogICAgICAgICJwcm92aWRlciI6ICJleGFtcGxlIiwKICAgICAgICAiaWQiOiAibW9kZWwtYSIsCiAgICAgICAgInJldmlzaW9uIjogIjEiCiAgICAgIH0sCiAgICAgICJ0b2tlbml6ZXIiOiAiZXhhbXBsZS10b2tlbml6ZXIvMSIsCiAgICAgICJpbnB1dF9saW1pdCI6IDgwMDAsCiAgICAgICJtZWRpYV90eXBlcyI6IFsKICAgICAgICAidGV4dC9jc3YiLAogICAgICAgICJ0ZXh0L21hcmtkb3duIgogICAgICBdLAogICAgICAiY2FwYWJpbGl0aWVzIjogWwogICAgICAgICJ0ZXh0IiwKICAgICAgICAidG9vbF9jYWxscyIKICAgICAgXQogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0yIiwKICAgICAgImtpbmQiOiAibW9kZWwiLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS9tb2RlbC1hIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIiwKICAgICAgIm1vZGVsIjogewogICAgICAgICJwcm92aWRlciI6ICJleGFtcGxlIiwKICAgICAgICAiaWQiOiAibW9kZWwtYSIsCiAgICAgICAgInJldmlzaW9uIjogIjEiCiAgICAgIH0sCiAgICAgICJ0b2tlbml6ZXIiOiAiZXhhbXBsZS10b2tlbml6ZXIvMSIsCiAgICAgICJpbnB1dF9saW1pdCI6IDgwMDAsCiAgICAgICJtZWRpYV90eXBlcyI6IFsKICAgICAgICAidGV4dC9jc3YiLAogICAgICAgICJ0ZXh0L21hcmtkb3duIgogICAgICBdLAogICAgICAiY2FwYWJpbGl0aWVzIjogWwogICAgICAgICJ0ZXh0IiwKICAgICAgICAidG9vbF9jYWxscyIKICAgICAgXQogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0zIiwKICAgICAgImtpbmQiOiAiY29uZmlndXJhdGlvbiIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLmNvbmZpZ3VyYXRpb24uZWZmZWN0aXZlIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIgogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC00IiwKICAgICAgImtpbmQiOiAiZGVwZW5kZW5jeSIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLmludmVudG9yeS5wdWJsaXNoIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIgogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC01IiwKICAgICAgImtpbmQiOiAic2VydmljZSIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLnNlcnZpY2UucHVibGlzaGVyLXNlcnZpY2UiLAogICAgICAidmVyc2lvbiI6ICIxIiwKICAgICAgInJldmlzaW9uIjogInN5bnRoZXRpYy1zdGF0ZS0xIiwKICAgICAgInN0YXR1cyI6ICJ1bmtub3duIiwKICAgICAgImFjY291bnQiOiB7CiAgICAgICAgInByb3ZpZGVyIjogImV4YW1wbGUiLAogICAgICAgICJzdWJqZWN0IjogImFjY291bnQtQSIKICAgICAgfSwKICAgICAgImF1ZGllbmNlIjogImV4YW1wbGUucHVibGlzaGVyIiwKICAgICAgInNjb3BlcyI6IFtdLAogICAgICAic2VjcmV0X2hhbmRsZXMiOiBbXSwKICAgICAgImVuZHBvaW50IjogImh0dHBzOi8vcHVibGlzaGVyLmV4YW1wbGUuaW52YWxpZCIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtNiIsCiAgICAgICJraW5kIjogIm9wZXJhdGlvbiIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLm9wZXJhdGlvbi5wdWJsaXNoLW9wZXJhdGlvbiIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogInVua25vd24iLAogICAgICAicmVjb3Zlcnlfc3RyYXRlZ3kiOiAicmVjb25jaWxlIiwKICAgICAgImV4dGVybmFsX2lkZW50aXR5IjogewogICAgICAgICJuYW1lc3BhY2UiOiAiZXhhbXBsZS5wdWJsaXNoZXIvYWNjb3VudC1BIiwKICAgICAgICAidmFsdWUiOiAib3BlcmF0aW9uLTQyIgogICAgICB9CiAgICB9CiAgXQp9Cg==",
      "bytes": 2923,
      "evidence_id": "snapshot-inspection"
    }
  },
  "assessed_at": "2026-09-26T12:00:00Z",
  "expires_at": "2026-09-26T13:00:00Z",
  "outcome": "blocked",
  "assessments": [
    {
      "subject": {
        "kind": "plan",
        "id": "continue-main"
      },
      "status": "supported",
      "required": true,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": []
    },
    {
      "subject": {
        "kind": "context",
        "id": "continue-context"
      },
      "status": "supported",
      "required": false,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": [
        "component-1"
      ]
    },
    {
      "subject": {
        "kind": "model",
        "id": "continue-main"
      },
      "status": "supported",
      "required": false,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": [
        "component-2"
      ]
    },
    {
      "subject": {
        "kind": "configuration",
        "id": "effective"
      },
      "status": "supported",
      "required": true,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": [
        "component-3"
      ]
    },
    {
      "subject": {
        "kind": "feature",
        "id": "asif.portable-continuation/0.1"
      },
      "status": "supported",
      "required": true,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": []
    },
    {
      "subject": {
        "kind": "resource",
        "id": "source-csv"
      },
      "status": "supported",
      "required": false,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": []
    },
    {
      "subject": {
        "kind": "dependency",
        "id": "publisher"
      },
      "status": "supported",
      "required": true,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ],
      "resolved": {
        "identity": "example.inventory.publish",
        "version": "1"
      },
      "component_ids": [
        "component-4"
      ]
    },
    {
      "subject": {
        "kind": "service",
        "id": "publisher-service"
      },
      "status": "unresolved",
      "required": true,
      "detail": "Remote outcome or destination login must be verified before any continuation.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": [
        "component-5"
      ]
    },
    {
      "subject": {
        "kind": "operation",
        "id": "publish-operation"
      },
      "status": "unresolved",
      "required": true,
      "detail": "Remote outcome or destination login must be verified before any continuation.",
      "evidence_ids": [
        "scenario"
      ],
      "component_ids": [
        "component-6"
      ]
    }
  ],
  "path_bindings": [],
  "identity_mappings": [],
  "transformations": [],
  "model_assessment": {
    "source": {
      "provider": "example",
      "id": "model-a",
      "revision": "1"
    },
    "target": {
      "provider": "example",
      "id": "model-a",
      "revision": "1"
    },
    "tokenizer": "example-tokenizer/1",
    "input_tokens": 700,
    "input_limit": 8000,
    "output_reserve": 1000,
    "fit": "fits"
  },
  "blocking_reasons": [
    {
      "subject": {
        "kind": "service",
        "id": "publisher-service"
      },
      "reason": "Remote outcome or destination login must be verified before any continuation."
    },
    {
      "subject": {
        "kind": "operation",
        "id": "publish-operation"
      },
      "reason": "Remote outcome or destination login must be verified before any continuation."
    }
  ],
  "evidence": [
    {
      "id": "scenario",
      "producer": "asif-examples",
      "time": "2026-09-26T12:00:00Z",
      "kind": "synthetic",
      "detail": "Authored assumptions only. This receipt cannot authorize import or continuation."
    },
    {
      "id": "snapshot-inspection",
      "producer": "asif-examples",
      "time": "2026-09-26T12:00:00Z",
      "kind": "synthetic",
      "detail": "Authored destination snapshot; no live inspection or credential lookup."
    }
  ],
  "import_result": {
    "status": "not_attempted",
    "evidence_ids": [],
    "detail": "No import was executed."
  },
  "continuation_result": {
    "status": "not_tested",
    "evidence_ids": [],
    "detail": "No agent was started."
  }
}
```

<a id="source-object"></a>

## Source Object

Binds this report to a source session, capture, continuation plan and exact document digest.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="source-object-session_id"></a>`session_id` | string | Yes | Logical session ID of the referenced boundary. Minimum length: `1`. |
| <a id="source-object-capture_id"></a>`capture_id` | string | Yes | Immutable capture ID of the referenced boundary. Minimum length: `1`. |
| <a id="source-object-plan_id"></a>`plan_id` | string | Yes | ID of the exact continuation plan being assessed. Minimum length: `1`. |
| <a id="source-object-document_sha256"></a>`document_sha256` | string | Yes | SHA-256 of the exact source session JSON bytes, not a reserialized equivalent. Pattern: `^[0-9a-f]{64}(?![\s\S])`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "session_id": "session-pending-remote-operation",
  "capture_id": "capture-pending-remote-operation",
  "plan_id": "continue-main",
  "document_sha256": "966361de8e573d9c451c09f108e695de169d9a8736956b34ec9c93a0b3ed3837"
}
```

<a id="destination-object"></a>

## Destination Object

Identifies the assessed destination runtime and the digest of its capability snapshot.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="destination-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="destination-object-runtime"></a>`runtime` | [Runtime Object](report-objects.md#runtime-object) | Yes | Agent, adapter and platform of the assessed runtime. |
| <a id="destination-object-capabilities_sha256"></a>`capabilities_sha256` | string | Yes | Lowercase SHA-256 of the exact decoded snapshot bytes, with no reserialization or canonicalization. Pattern: `^[0-9a-f]{64}(?![\s\S])`. |
| <a id="destination-object-capabilities_snapshot"></a>`capabilities_snapshot` | [Snapshot Evidence Object](report-objects.md#snapshot-evidence-object) | Yes | Supplied immutable snapshot bytes, format, availability and evidence binding. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example-cloud-runtime",
  "runtime": {
    "agent": {
      "id": "example-agent-a",
      "version": "1",
      "state_format": "example-native/1"
    },
    "adapter": {
      "id": "example-adapter",
      "version": "1"
    },
    "os": "linux",
    "architecture": "x86_64"
  },
  "capabilities_sha256": "1a659c7d45e049f81c1207e093efa003486c4849ba9725005b7feacc159bb4a5",
  "capabilities_snapshot": {
    "format": "asif.destination-capabilities/0.1",
    "availability": "supplied",
    "data": "ewogICJzbmFwc2hvdF92ZXJzaW9uIjogIjAuMSIsCiAgImlkIjogInNuYXBzaG90LWFzc2Vzc21lbnQtcGVuZGluZy1yZW1vdGUtb3BlcmF0aW9uIiwKICAiZGVzdGluYXRpb25faWQiOiAiZXhhbXBsZS1jbG91ZC1ydW50aW1lIiwKICAicHJvZHVjZXIiOiAiYXNpZi1leGFtcGxlcyIsCiAgImV2YWx1YXRpb25fbW9kZSI6ICJzeW50aGV0aWMiLAogICJvYnNlcnZlZF9hdCI6ICIyMDI2LTA5LTI2VDEyOjAwOjAwWiIsCiAgImV4cGlyZXNfYXQiOiAiMjAyNi0wOS0yNlQxMzowMDowMFoiLAogICJydW50aW1lIjogewogICAgImFnZW50IjogewogICAgICAiaWQiOiAiZXhhbXBsZS1hZ2VudC1hIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJzdGF0ZV9mb3JtYXQiOiAiZXhhbXBsZS1uYXRpdmUvMSIKICAgIH0sCiAgICAiYWRhcHRlciI6IHsKICAgICAgImlkIjogImV4YW1wbGUtYWRhcHRlciIsCiAgICAgICJ2ZXJzaW9uIjogIjEiCiAgICB9LAogICAgIm9zIjogImxpbnV4IiwKICAgICJhcmNoaXRlY3R1cmUiOiAieDg2XzY0IgogIH0sCiAgInJ1bnRpbWVfcmV2aXNpb24iOiAic3ludGhldGljLXJ1bnRpbWUtMSIsCiAgInN1cHBvcnRlZF9mZWF0dXJlcyI6IFsKICAgICJhc2lmLnBvcnRhYmxlLWNvbnRpbnVhdGlvbi8wLjEiCiAgXSwKICAiY29tcG9uZW50cyI6IFsKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0xIiwKICAgICAgImtpbmQiOiAibW9kZWwiLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS9tb2RlbC1hIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIiwKICAgICAgIm1vZGVsIjogewogICAgICAgICJwcm92aWRlciI6ICJleGFtcGxlIiwKICAgICAgICAiaWQiOiAibW9kZWwtYSIsCiAgICAgICAgInJldmlzaW9uIjogIjEiCiAgICAgIH0sCiAgICAgICJ0b2tlbml6ZXIiOiAiZXhhbXBsZS10b2tlbml6ZXIvMSIsCiAgICAgICJpbnB1dF9saW1pdCI6IDgwMDAsCiAgICAgICJtZWRpYV90eXBlcyI6IFsKICAgICAgICAidGV4dC9jc3YiLAogICAgICAgICJ0ZXh0L21hcmtkb3duIgogICAgICBdLAogICAgICAiY2FwYWJpbGl0aWVzIjogWwogICAgICAgICJ0ZXh0IiwKICAgICAgICAidG9vbF9jYWxscyIKICAgICAgXQogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0yIiwKICAgICAgImtpbmQiOiAibW9kZWwiLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS9tb2RlbC1hIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIiwKICAgICAgIm1vZGVsIjogewogICAgICAgICJwcm92aWRlciI6ICJleGFtcGxlIiwKICAgICAgICAiaWQiOiAibW9kZWwtYSIsCiAgICAgICAgInJldmlzaW9uIjogIjEiCiAgICAgIH0sCiAgICAgICJ0b2tlbml6ZXIiOiAiZXhhbXBsZS10b2tlbml6ZXIvMSIsCiAgICAgICJpbnB1dF9saW1pdCI6IDgwMDAsCiAgICAgICJtZWRpYV90eXBlcyI6IFsKICAgICAgICAidGV4dC9jc3YiLAogICAgICAgICJ0ZXh0L21hcmtkb3duIgogICAgICBdLAogICAgICAiY2FwYWJpbGl0aWVzIjogWwogICAgICAgICJ0ZXh0IiwKICAgICAgICAidG9vbF9jYWxscyIKICAgICAgXQogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0zIiwKICAgICAgImtpbmQiOiAiY29uZmlndXJhdGlvbiIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLmNvbmZpZ3VyYXRpb24uZWZmZWN0aXZlIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIgogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC00IiwKICAgICAgImtpbmQiOiAiZGVwZW5kZW5jeSIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLmludmVudG9yeS5wdWJsaXNoIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIgogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC01IiwKICAgICAgImtpbmQiOiAic2VydmljZSIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLnNlcnZpY2UucHVibGlzaGVyLXNlcnZpY2UiLAogICAgICAidmVyc2lvbiI6ICIxIiwKICAgICAgInJldmlzaW9uIjogInN5bnRoZXRpYy1zdGF0ZS0xIiwKICAgICAgInN0YXR1cyI6ICJ1bmtub3duIiwKICAgICAgImFjY291bnQiOiB7CiAgICAgICAgInByb3ZpZGVyIjogImV4YW1wbGUiLAogICAgICAgICJzdWJqZWN0IjogImFjY291bnQtQSIKICAgICAgfSwKICAgICAgImF1ZGllbmNlIjogImV4YW1wbGUucHVibGlzaGVyIiwKICAgICAgInNjb3BlcyI6IFtdLAogICAgICAic2VjcmV0X2hhbmRsZXMiOiBbXSwKICAgICAgImVuZHBvaW50IjogImh0dHBzOi8vcHVibGlzaGVyLmV4YW1wbGUuaW52YWxpZCIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtNiIsCiAgICAgICJraW5kIjogIm9wZXJhdGlvbiIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLm9wZXJhdGlvbi5wdWJsaXNoLW9wZXJhdGlvbiIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogInVua25vd24iLAogICAgICAicmVjb3Zlcnlfc3RyYXRlZ3kiOiAicmVjb25jaWxlIiwKICAgICAgImV4dGVybmFsX2lkZW50aXR5IjogewogICAgICAgICJuYW1lc3BhY2UiOiAiZXhhbXBsZS5wdWJsaXNoZXIvYWNjb3VudC1BIiwKICAgICAgICAidmFsdWUiOiAib3BlcmF0aW9uLTQyIgogICAgICB9CiAgICB9CiAgXQp9Cg==",
    "bytes": 2923,
    "evidence_id": "snapshot-inspection"
  }
}
```

<a id="path-bindings-object"></a>

## Path Bindings Object

Maps one logical root to a destination path and declares the destination's path comparison rules.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="path-bindings-object-root_id"></a>`root_id` | string | Yes | Logical workspace root identity, independent of source and destination absolute paths. Minimum length: `1`. |
| <a id="path-bindings-object-destination_path"></a>`destination_path` | string | Yes | Absolute path selected by the destination for the logical root. Minimum length: `1`. |
| <a id="path-bindings-object-case_sensitive"></a>`case_sensitive` | boolean | Yes | Whether the destination distinguishes path spelling by case. |
| <a id="path-bindings-object-unicode_normalization"></a>`unicode_normalization` | enum | Yes | Normalization applied when checking destination path collisions. One of `"none"`, `"NFC"`, `"NFD"`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "root_id": "project",
  "destination_path": "/work/project",
  "case_sensitive": true,
  "unicode_normalization": "none"
}
```

<a id="identity-mappings-object"></a>

## Identity Mappings Object

Records an explicit mapping of a source entity identity into the destination namespace.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="identity-mappings-object-entity_type"></a>`entity_type` | string | Yes | Type of the entity containing or identified by this reference. Minimum length: `1`. |
| <a id="identity-mappings-object-source_id"></a>`source_id` | string | Yes | Original entity identity. Minimum length: `1`. |
| <a id="identity-mappings-object-target_id"></a>`target_id` | string | Yes | Mapped destination identity. Minimum length: `1`. |
| <a id="identity-mappings-object-target_namespace"></a>`target_namespace` | string | Yes | Namespace containing the mapped destination identity. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "entity_type": "native_session",
  "source_id": "source-native",
  "target_id": "source-native",
  "target_namespace": "example-cloud-runtime"
}
```

<a id="model-assessment-object"></a>

## Model Assessment Object

Reports the target model and measured or unknown context fit, including reserved output capacity.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="model-assessment-object-source"></a>`source` | [Model Object](report-objects.md#model-object) | Yes | Source identity and boundary or report binding. |
| <a id="model-assessment-object-target"></a>`target` | [Model Object](report-objects.md#model-object) | Yes | Declared target value, model or symbolic-link target according to context. |
| <a id="model-assessment-object-tokenizer"></a>`tokenizer` | string / null | Yes | Tokenizer identity used for input measurement, or null when unmeasured. |
| <a id="model-assessment-object-input_tokens"></a>`input_tokens` | integer / null | Yes | Measured input token count, or null when unknown. |
| <a id="model-assessment-object-input_limit"></a>`input_limit` | integer / null | Yes | Destination input capacity, or null when unknown. |
| <a id="model-assessment-object-output_reserve"></a>`output_reserve` | integer | Yes | Capacity reserved for the next output. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="model-assessment-object-fit"></a>`fit` | enum | Yes | Whether the measured context fits the destination budget. One of `"fits"`, `"exceeds"`, `"unknown"`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "source": {
    "provider": "example",
    "id": "model-a",
    "revision": "1"
  },
  "target": {
    "provider": "example",
    "id": "model-b",
    "revision": "2"
  },
  "tokenizer": "example-tokenizer/1",
  "input_tokens": 700,
  "input_limit": 8000,
  "output_reserve": 1000,
  "fit": "fits"
}
```

<a id="blocking-reasons-object"></a>

## Blocking Reasons Object

Explains a subject-specific condition preventing the selected continuation plan from being ready.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="blocking-reasons-object-subject"></a>`subject` | [Subject Object](report-objects.md#subject-object) | Yes | Account identity or assessed subject, as defined by the containing object. |
| <a id="blocking-reasons-object-reason"></a>`reason` | string | Yes | Reason for the recorded operation or unavailable interpretation. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "subject": {
    "kind": "service",
    "id": "publisher-service"
  },
  "reason": "Remote outcome or destination login must be verified before any continuation."
}
```

<a id="import-result-object"></a>

## Import Result Object

Records whether native import was attempted and the evidence for its outcome.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="import-result-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"not_attempted"`, `"imported"`, `"failed"`, `"rolled_back"`. |
| <a id="import-result-object-evidence_ids"></a>`evidence_ids` | array of string | Yes | IDs of evidence records supporting this declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="import-result-object-detail"></a>`detail` | string | Yes | Explanation of the stated status or evidence. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "status": "not_attempted",
  "evidence_ids": [],
  "detail": "No import was executed."
}
```

<a id="continuation-result-object"></a>

## Continuation Result Object

Records whether continuation was tested and the evidence for its outcome.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="continuation-result-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"not_tested"`, `"continued"`, `"blocked"`, `"failed"`. |
| <a id="continuation-result-object-evidence_ids"></a>`evidence_ids` | array of string | Yes | IDs of evidence records supporting this declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="continuation-result-object-detail"></a>`detail` | string | Yes | Explanation of the stated status or evidence. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "status": "not_tested",
  "evidence_ids": [],
  "detail": "No agent was started."
}
```

<a id="runtime-object"></a>

## Runtime Object

Identifies the agent, adapter and operating platform involved in a continuation assessment.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="runtime-object-agent"></a>`agent` | [Agent Object](report-objects.md#agent-object) | Yes | Agent implementation, version and state format. |
| <a id="runtime-object-adapter"></a>`adapter` | [Runtime Adapter Object](report-objects.md#runtime-adapter-object) | Yes | Adapter implementation and version interpreting the source or destination. |
| <a id="runtime-object-os"></a>`os` | string | Yes | Operating-system identifier or accepted identifiers. Minimum length: `1`. |
| <a id="runtime-object-architecture"></a>`architecture` | string | Yes | Runtime CPU architecture identifier. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "agent": {
    "id": "example-agent-b",
    "version": "2",
    "state_format": "example-b/2"
  },
  "adapter": {
    "id": "example-a-to-b",
    "version": "1"
  },
  "os": "linux",
  "architecture": "x86_64"
}
```

<a id="runtime-adapter-object"></a>

## Runtime Adapter Object

Names the adapter implementation and version used to interpret native state.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="runtime-adapter-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="runtime-adapter-object-version"></a>`version` | string / null | Yes | Implementation or format version. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example-a-to-b",
  "version": "1"
}
```

<a id="agent-object"></a>

## Agent Object

Names an agent implementation, version and native state format.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="agent-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="agent-object-version"></a>`version` | string / null | Yes | Implementation or format version. |
| <a id="agent-object-state_format"></a>`state_format` | string / null | Yes | Native state-format identifier. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example-agent-b",
  "version": "2",
  "state_format": "example-b/2"
}
```

<a id="model-object"></a>

## Model Object

Identifies a model provider, model ID and optional known revision without assuming equivalence to another model.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="model-object-provider"></a>`provider` | string | Yes | Provider identity for the named object or account. Minimum length: `1`. |
| <a id="model-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="model-object-revision"></a>`revision` | string / null | Yes | Versioned definition or task revision within its identity. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example",
  "id": "model-a",
  "revision": "1"
}
```

<a id="subject-object"></a>

## Subject Object

Identifies the exact entity or capability being assessed, including its owner where IDs are scoped.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="subject-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"plan"`, `"context"`, `"model"`, `"workspace"`, `"dependency"`, `"service"`, `"configuration"`, `"instruction"`, `"capability"`, `"policy"`, `"resource"`, `"operation"`, `"native_import"`, `"feature"`, `"environment"`, `"checkpoint_requirement"`, `"environment_requirement"`. |
| <a id="subject-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="subject-object-owner_id"></a>`owner_id` | string | No | Configuration owner for instruction/capability/policy subjects, checkpoint owner for checkpoint_requirement, or environment owner for environment_requirement. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "resource",
  "id": "report"
}
```

<a id="assessment-object"></a>

## Assessment Object

Records support, adaptation or a blocker for one subject, with evidence and any resolved binding.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="assessment-object-subject"></a>`subject` | [Subject Object](report-objects.md#subject-object) | Yes | Account identity or assessed subject, as defined by the containing object. |
| <a id="assessment-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"supported"`, `"adapted"`, `"omitted"`, `"unresolved"`, `"unsupported"`. |
| <a id="assessment-object-required"></a>`required` | boolean | Yes | Whether the action-specific prerequisite closure requires this subject; reports must match the computed flag exactly. |
| <a id="assessment-object-detail"></a>`detail` | string | Yes | Explanation of the stated status or evidence. Minimum length: `1`. |
| <a id="assessment-object-evidence_ids"></a>`evidence_ids` | array of string | Yes | IDs of evidence records supporting this declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="assessment-object-resolved"></a>`resolved` | [Assessment Resolved Object](report-objects.md#assessment-resolved-object) | No | Destination-resolved dependency or service values. |
| <a id="assessment-object-component_ids"></a>`component_ids` | array of string | Yes | Unique references to destination snapshot components used by this assessment. Minimum items: `0`. Items MUST be unique. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "subject": {
    "kind": "plan",
    "id": "continue-main"
  },
  "status": "supported",
  "required": true,
  "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
  "evidence_ids": [
    "scenario"
  ],
  "component_ids": []
}
```

<a id="assessment-resolved-object"></a>

## Assessment Resolved Object

Destination dependency, service, operation recovery or core requirement binding, checked against its source declaration.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="assessment-resolved-object-identity"></a>`identity` | string | No | Namespaced dependency identity to resolve. Minimum length: `1`. |
| <a id="assessment-resolved-object-version"></a>`version` | string / null | No | Implementation or format version. |
| <a id="assessment-resolved-object-account"></a>`account` | [Assessment Resolved Account Object](report-objects.md#assessment-resolved-account-object) | No | Expected or resolved service-account identity. |
| <a id="assessment-resolved-object-scopes"></a>`scopes` | array of string | No | Required or resolved service access scopes. Minimum items: `0`. Items MUST be unique. |
| <a id="assessment-resolved-object-audience"></a>`audience` | string | No | Intended service audience for access credentials. Minimum length: `1`. |
| <a id="assessment-resolved-object-endpoint"></a>`endpoint` | string | No | Recorded or resolved endpoint declaration. Minimum length: `1`. |
| <a id="assessment-resolved-object-secret_handles"></a>`secret_handles` | array of string | No | Logical credential handles to resolve separately at the destination. Minimum items: `0`. Items MUST be unique. |
| <a id="assessment-resolved-object-status"></a>`status` | enum | No | Recorded state at the relevant boundary; see the allowed values. One of `"available"`. |
| <a id="assessment-resolved-object-recovery_strategy"></a>`recovery_strategy` | enum | No | Resolved reconcile or reconnect strategy; must match the selected source operation. One of `"reconcile"`, `"reconnect"`. |
| <a id="assessment-resolved-object-external_identity"></a>`external_identity` | [Assessment Resolved External Identity Object](report-objects.md#assessment-resolved-external-identity-object) | No | Identifier used to reconcile this operation in its external system. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{}
```

<a id="assessment-resolved-account-object"></a>

## Assessment Resolved Account Object

Identifies the resolved destination account for comparison with the expected service account.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="assessment-resolved-account-object-provider"></a>`provider` | string | Yes | Provider identity for the named object or account. Minimum length: `1`. |
| <a id="assessment-resolved-account-object-subject"></a>`subject` | string | Yes | Account identity or assessed subject, as defined by the containing object. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example",
  "subject": "account-A"
}
```

<a id="assessment-resolved-external-identity-object"></a>

## Assessment Resolved External Identity Object

Identifies the exact remote operation being reconciled; must match its source namespace and identity.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="assessment-resolved-external-identity-object-namespace"></a>`namespace` | string | Yes | Namespace in which the opaque value is meaningful. Minimum length: `1`. |
| <a id="assessment-resolved-external-identity-object-value"></a>`value` | string | Yes | Value interpreted according to the enclosing schema, dialect or counter. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "namespace": "example.jobs/account-A",
  "value": "job-42"
}
```

<a id="capability-component-object"></a>

## Capability Component Object

A destination component with identity, revision, availability and kind-specific facts. Its revision is an opaque non-secret token, not a digest.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="capability-component-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="capability-component-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"dependency"`, `"configuration"`, `"policy"`, `"capability"`, `"model"`, `"service"`, `"workspace"`, `"operation"`, `"native_import"`, `"environment"`. |
| <a id="capability-component-object-identity"></a>`identity` | string | Yes | Namespaced dependency identity to resolve. Minimum length: `1`. |
| <a id="capability-component-object-version"></a>`version` | string / null | Yes | Implementation or format version. |
| <a id="capability-component-object-revision"></a>`revision` | string | Yes | Versioned definition or task revision within its identity. Minimum length: `1`. |
| <a id="capability-component-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"available"`, `"unavailable"`, `"unknown"`. |
| <a id="capability-component-object-model"></a>`model` | [Model Object](report-objects.md#model-object) | No | Recorded model identity or settings for this scope. |
| <a id="capability-component-object-tokenizer"></a>`tokenizer` | string / null | No | Tokenizer identity used for input measurement, or null when unmeasured. |
| <a id="capability-component-object-input_limit"></a>`input_limit` | integer / null | No | Destination input capacity, or null when unknown. |
| <a id="capability-component-object-media_types"></a>`media_types` | array of string | No | Media types the target must accept or explicitly adapt. Minimum items: `0`. Items MUST be unique. |
| <a id="capability-component-object-capabilities"></a>`capabilities` | array of string | No | Required or declared abilities for this configuration or model. Minimum items: `0`. Items MUST be unique. |
| <a id="capability-component-object-account"></a>`account` | [Assessment Resolved Account Object](report-objects.md#assessment-resolved-account-object) | No | Expected or resolved service-account identity. |
| <a id="capability-component-object-audience"></a>`audience` | string | No | Intended service audience for access credentials. Minimum length: `1`. |
| <a id="capability-component-object-scopes"></a>`scopes` | array of string | No | Required or resolved service access scopes. Minimum items: `0`. Items MUST be unique. |
| <a id="capability-component-object-secret_handles"></a>`secret_handles` | array of string | No | Logical credential handles to resolve separately at the destination. Minimum items: `0`. Items MUST be unique. |
| <a id="capability-component-object-endpoint"></a>`endpoint` | string / null | No | Recorded or resolved endpoint declaration. |
| <a id="capability-component-object-root_id"></a>`root_id` | string | No | Logical workspace root identity, independent of source and destination absolute paths. Minimum length: `1`. |
| <a id="capability-component-object-destination_path"></a>`destination_path` | string | No | Absolute path selected by the destination for the logical root. Minimum length: `1`. |
| <a id="capability-component-object-case_sensitive"></a>`case_sensitive` | boolean | No | Whether the destination distinguishes path spelling by case. |
| <a id="capability-component-object-unicode_normalization"></a>`unicode_normalization` | enum | No | Normalization applied when checking destination path collisions. One of `"none"`, `"NFC"`, `"NFD"`. |
| <a id="capability-component-object-recovery_strategy"></a>`recovery_strategy` | enum | No | Resolved reconcile or reconnect strategy; must match the selected source operation. One of `"reconcile"`, `"reconnect"`, `"restart"`, `"refuse"`. |
| <a id="capability-component-object-external_identity"></a>`external_identity` | [Assessment Resolved External Identity Object](report-objects.md#assessment-resolved-external-identity-object) / null | No | Identifier used to reconcile this operation in its external system. |

### Rules

See the [destination capability snapshot contract](../CAPABILITIES.md) for exact bytes, required inventory, component bindings, evidence, currentness and refusal rules.

- When `kind` is `"model"`, require `model`, `tokenizer`, `input_limit`, `media_types`, `capabilities`.
- When `kind` is `"service"`, require `account`, `audience`, `scopes`, `secret_handles`, `endpoint`.
- When `kind` is `"workspace"`, require `root_id`, `destination_path`, `case_sensitive`, `unicode_normalization`.
- When `kind` is `"operation"`, require `recovery_strategy`, `external_identity`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "component-1",
  "kind": "model",
  "identity": "example/model-a",
  "version": "1",
  "revision": "synthetic-state-1",
  "status": "available",
  "model": {
    "provider": "example",
    "id": "model-a",
    "revision": "1"
  },
  "tokenizer": "example-tokenizer/1",
  "input_limit": 8000,
  "media_types": [
    "text/csv",
    "text/markdown"
  ],
  "capabilities": [
    "text",
    "tool_calls"
  ]
}
```

<a id="capability-snapshot-object"></a>

## Capability Snapshot Object

Immutable, versioned destination state declarations, hashed over their exact supplied JSON bytes.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="capability-snapshot-object-snapshot_version"></a>`snapshot_version` | `"0.1"` | Yes | Exact version of the destination capability snapshot contract. |
| <a id="capability-snapshot-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="capability-snapshot-object-destination_id"></a>`destination_id` | string | Yes | Identity of the assessed destination; must match the report. Minimum length: `1`. |
| <a id="capability-snapshot-object-producer"></a>`producer` | string | Yes | Software or instrumentation responsible for the capture or evidence. Minimum length: `1`. |
| <a id="capability-snapshot-object-evaluation_mode"></a>`evaluation_mode` | enum | Yes | Whether evidence is observed or synthetic; synthetic results cannot claim execution. One of `"synthetic"`, `"observed"`. |
| <a id="capability-snapshot-object-observed_at"></a>`observed_at` | string | Yes | Snapshot observation instant, no later than report assessment. Minimum length: `1`. |
| <a id="capability-snapshot-object-expires_at"></a>`expires_at` | string | Yes | Exclusive expiry time after which the assessment must be refreshed. Minimum length: `1`. |
| <a id="capability-snapshot-object-runtime"></a>`runtime` | [Runtime Object](report-objects.md#runtime-object) | Yes | Agent, adapter and platform of the assessed runtime. |
| <a id="capability-snapshot-object-runtime_revision"></a>`runtime_revision` | string | Yes | Opaque non-secret generation for the runtime deployment and effective global settings. Minimum length: `1`. |
| <a id="capability-snapshot-object-supported_features"></a>`supported_features` | array of string | Yes | Exact feature identifiers supported in this assessed snapshot. Minimum items: `0`. Items MUST be unique. |
| <a id="capability-snapshot-object-components"></a>`components` | array of [Capability Component Object](report-objects.md#capability-component-object) | Yes | Destination component inventory covering all claimed assessment support. Minimum items: `0`. |

### Rules

See the [destination capability snapshot contract](../CAPABILITIES.md) for exact bytes, required inventory, component bindings, evidence, currentness and refusal rules.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "snapshot_version": "0.1",
  "id": "snapshot-assessment-another-computer",
  "destination_id": "example-cloud-runtime",
  "producer": "asif-examples",
  "evaluation_mode": "synthetic",
  "observed_at": "2026-09-26T12:00:00Z",
  "expires_at": "2026-09-26T13:00:00Z",
  "runtime": {
    "agent": {
      "id": "example-agent-a",
      "version": "1",
      "state_format": "example-native/1"
    },
    "adapter": {
      "id": "example-adapter",
      "version": "1"
    },
    "os": "linux",
    "architecture": "x86_64"
  },
  "runtime_revision": "synthetic-runtime-1",
  "supported_features": [
    "asif.portable-continuation/0.1"
  ],
  "components": [
    {
      "id": "component-1",
      "kind": "model",
      "identity": "example/model-a",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available",
      "model": {
        "provider": "example",
        "id": "model-a",
        "revision": "1"
      },
      "tokenizer": "example-tokenizer/1",
      "input_limit": 8000,
      "media_types": [
        "text/csv",
        "text/markdown"
      ],
      "capabilities": [
        "text",
        "tool_calls"
      ]
    },
    {
      "id": "component-2",
      "kind": "model",
      "identity": "example/model-a",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available",
      "model": {
        "provider": "example",
        "id": "model-a",
        "revision": "1"
      },
      "tokenizer": "example-tokenizer/1",
      "input_limit": 8000,
      "media_types": [
        "text/csv",
        "text/markdown"
      ],
      "capabilities": [
        "text",
        "tool_calls"
      ]
    },
    {
      "id": "component-3",
      "kind": "configuration",
      "identity": "example.configuration.effective",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-4",
      "kind": "configuration",
      "identity": "example.instruction.workspace-rule",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-5",
      "kind": "capability",
      "identity": "example.capability.summary-skill",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-6",
      "kind": "policy",
      "identity": "example.policy.workspace-only",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-7",
      "kind": "dependency",
      "identity": "example-agent-a",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-8",
      "kind": "dependency",
      "identity": "example.inventory.summarize",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-9",
      "kind": "dependency",
      "identity": "example.inventory-summary",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-10",
      "kind": "workspace",
      "identity": "example.workspace.workspace-head",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available",
      "root_id": "project",
      "destination_path": "/work/project",
      "case_sensitive": true,
      "unicode_normalization": "none"
    },
    {
      "id": "component-11",
      "kind": "environment",
      "identity": "example.environment.project-env",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    },
    {
      "id": "component-12",
      "kind": "native_import",
      "identity": "example-adapter",
      "version": "1",
      "revision": "synthetic-state-1",
      "status": "available"
    }
  ]
}
```

<a id="snapshot-evidence-object"></a>

## Snapshot Evidence Object

Supplies exact snapshot bytes and links their observation evidence; unavailable evidence cannot establish report validity.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="snapshot-evidence-object-format"></a>`format` | string | Yes | Exact versioned snapshot format identifier. Minimum length: `1`. |
| <a id="snapshot-evidence-object-availability"></a>`availability` | enum | Yes | Whether and how the referenced content is available. One of `"supplied"`, `"unavailable"`. |
| <a id="snapshot-evidence-object-data"></a>`data` | string | No | Kind-specific payload; for an embedded resource this is base64-encoded bytes. Minimum length: `1`. |
| <a id="snapshot-evidence-object-bytes"></a>`bytes` | integer | No | Exact decoded byte count. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="snapshot-evidence-object-evidence_id"></a>`evidence_id` | string | Yes | Reference to the snapshot observation evidence in the containing report. Minimum length: `1`. |
| <a id="snapshot-evidence-object-explanation"></a>`explanation` | string | No | Reason for the declaration or limitation. Minimum length: `1`. |

### Rules

See the [destination capability snapshot contract](../CAPABILITIES.md) for exact bytes, required inventory, component bindings, evidence, currentness and refusal rules.

- When `availability` is `"supplied"`, require `data`, `bytes`.
- When `availability` is `"unavailable"`, require `explanation`; omit `data`, `bytes`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "format": "asif.destination-capabilities/0.1",
  "availability": "supplied",
  "data": "ewogICJzbmFwc2hvdF92ZXJzaW9uIjogIjAuMSIsCiAgImlkIjogInNuYXBzaG90LWFzc2Vzc21lbnQtYW5vdGhlci1jb21wdXRlciIsCiAgImRlc3RpbmF0aW9uX2lkIjogImV4YW1wbGUtY2xvdWQtcnVudGltZSIsCiAgInByb2R1Y2VyIjogImFzaWYtZXhhbXBsZXMiLAogICJldmFsdWF0aW9uX21vZGUiOiAic3ludGhldGljIiwKICAib2JzZXJ2ZWRfYXQiOiAiMjAyNi0wOS0yNlQxMjowMDowMFoiLAogICJleHBpcmVzX2F0IjogIjIwMjYtMDktMjZUMTM6MDA6MDBaIiwKICAicnVudGltZSI6IHsKICAgICJhZ2VudCI6IHsKICAgICAgImlkIjogImV4YW1wbGUtYWdlbnQtYSIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAic3RhdGVfZm9ybWF0IjogImV4YW1wbGUtbmF0aXZlLzEiCiAgICB9LAogICAgImFkYXB0ZXIiOiB7CiAgICAgICJpZCI6ICJleGFtcGxlLWFkYXB0ZXIiLAogICAgICAidmVyc2lvbiI6ICIxIgogICAgfSwKICAgICJvcyI6ICJsaW51eCIsCiAgICAiYXJjaGl0ZWN0dXJlIjogIng4Nl82NCIKICB9LAogICJydW50aW1lX3JldmlzaW9uIjogInN5bnRoZXRpYy1ydW50aW1lLTEiLAogICJzdXBwb3J0ZWRfZmVhdHVyZXMiOiBbCiAgICAiYXNpZi5wb3J0YWJsZS1jb250aW51YXRpb24vMC4xIgogIF0sCiAgImNvbXBvbmVudHMiOiBbCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtMSIsCiAgICAgICJraW5kIjogIm1vZGVsIiwKICAgICAgImlkZW50aXR5IjogImV4YW1wbGUvbW9kZWwtYSIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogImF2YWlsYWJsZSIsCiAgICAgICJtb2RlbCI6IHsKICAgICAgICAicHJvdmlkZXIiOiAiZXhhbXBsZSIsCiAgICAgICAgImlkIjogIm1vZGVsLWEiLAogICAgICAgICJyZXZpc2lvbiI6ICIxIgogICAgICB9LAogICAgICAidG9rZW5pemVyIjogImV4YW1wbGUtdG9rZW5pemVyLzEiLAogICAgICAiaW5wdXRfbGltaXQiOiA4MDAwLAogICAgICAibWVkaWFfdHlwZXMiOiBbCiAgICAgICAgInRleHQvY3N2IiwKICAgICAgICAidGV4dC9tYXJrZG93biIKICAgICAgXSwKICAgICAgImNhcGFiaWxpdGllcyI6IFsKICAgICAgICAidGV4dCIsCiAgICAgICAgInRvb2xfY2FsbHMiCiAgICAgIF0KICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtMiIsCiAgICAgICJraW5kIjogIm1vZGVsIiwKICAgICAgImlkZW50aXR5IjogImV4YW1wbGUvbW9kZWwtYSIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogImF2YWlsYWJsZSIsCiAgICAgICJtb2RlbCI6IHsKICAgICAgICAicHJvdmlkZXIiOiAiZXhhbXBsZSIsCiAgICAgICAgImlkIjogIm1vZGVsLWEiLAogICAgICAgICJyZXZpc2lvbiI6ICIxIgogICAgICB9LAogICAgICAidG9rZW5pemVyIjogImV4YW1wbGUtdG9rZW5pemVyLzEiLAogICAgICAiaW5wdXRfbGltaXQiOiA4MDAwLAogICAgICAibWVkaWFfdHlwZXMiOiBbCiAgICAgICAgInRleHQvY3N2IiwKICAgICAgICAidGV4dC9tYXJrZG93biIKICAgICAgXSwKICAgICAgImNhcGFiaWxpdGllcyI6IFsKICAgICAgICAidGV4dCIsCiAgICAgICAgInRvb2xfY2FsbHMiCiAgICAgIF0KICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtMyIsCiAgICAgICJraW5kIjogImNvbmZpZ3VyYXRpb24iLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS5jb25maWd1cmF0aW9uLmVmZmVjdGl2ZSIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogImF2YWlsYWJsZSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtNCIsCiAgICAgICJraW5kIjogImNvbmZpZ3VyYXRpb24iLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS5pbnN0cnVjdGlvbi53b3Jrc3BhY2UtcnVsZSIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogImF2YWlsYWJsZSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtNSIsCiAgICAgICJraW5kIjogImNhcGFiaWxpdHkiLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS5jYXBhYmlsaXR5LnN1bW1hcnktc2tpbGwiLAogICAgICAidmVyc2lvbiI6ICIxIiwKICAgICAgInJldmlzaW9uIjogInN5bnRoZXRpYy1zdGF0ZS0xIiwKICAgICAgInN0YXR1cyI6ICJhdmFpbGFibGUiCiAgICB9LAogICAgewogICAgICAiaWQiOiAiY29tcG9uZW50LTYiLAogICAgICAia2luZCI6ICJwb2xpY3kiLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS5wb2xpY3kud29ya3NwYWNlLW9ubHkiLAogICAgICAidmVyc2lvbiI6ICIxIiwKICAgICAgInJldmlzaW9uIjogInN5bnRoZXRpYy1zdGF0ZS0xIiwKICAgICAgInN0YXR1cyI6ICJhdmFpbGFibGUiCiAgICB9LAogICAgewogICAgICAiaWQiOiAiY29tcG9uZW50LTciLAogICAgICAia2luZCI6ICJkZXBlbmRlbmN5IiwKICAgICAgImlkZW50aXR5IjogImV4YW1wbGUtYWdlbnQtYSIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogImF2YWlsYWJsZSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJjb21wb25lbnQtOCIsCiAgICAgICJraW5kIjogImRlcGVuZGVuY3kiLAogICAgICAiaWRlbnRpdHkiOiAiZXhhbXBsZS5pbnZlbnRvcnkuc3VtbWFyaXplIiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIgogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC05IiwKICAgICAgImtpbmQiOiAiZGVwZW5kZW5jeSIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLmludmVudG9yeS1zdW1tYXJ5IiwKICAgICAgInZlcnNpb24iOiAiMSIsCiAgICAgICJyZXZpc2lvbiI6ICJzeW50aGV0aWMtc3RhdGUtMSIsCiAgICAgICJzdGF0dXMiOiAiYXZhaWxhYmxlIgogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0xMCIsCiAgICAgICJraW5kIjogIndvcmtzcGFjZSIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLndvcmtzcGFjZS53b3Jrc3BhY2UtaGVhZCIsCiAgICAgICJ2ZXJzaW9uIjogIjEiLAogICAgICAicmV2aXNpb24iOiAic3ludGhldGljLXN0YXRlLTEiLAogICAgICAic3RhdHVzIjogImF2YWlsYWJsZSIsCiAgICAgICJyb290X2lkIjogInByb2plY3QiLAogICAgICAiZGVzdGluYXRpb25fcGF0aCI6ICIvd29yay9wcm9qZWN0IiwKICAgICAgImNhc2Vfc2Vuc2l0aXZlIjogdHJ1ZSwKICAgICAgInVuaWNvZGVfbm9ybWFsaXphdGlvbiI6ICJub25lIgogICAgfSwKICAgIHsKICAgICAgImlkIjogImNvbXBvbmVudC0xMSIsCiAgICAgICJraW5kIjogImVudmlyb25tZW50IiwKICAgICAgImlkZW50aXR5IjogImV4YW1wbGUuZW52aXJvbm1lbnQucHJvamVjdC1lbnYiLAogICAgICAidmVyc2lvbiI6ICIxIiwKICAgICAgInJldmlzaW9uIjogInN5bnRoZXRpYy1zdGF0ZS0xIiwKICAgICAgInN0YXR1cyI6ICJhdmFpbGFibGUiCiAgICB9LAogICAgewogICAgICAiaWQiOiAiY29tcG9uZW50LTEyIiwKICAgICAgImtpbmQiOiAibmF0aXZlX2ltcG9ydCIsCiAgICAgICJpZGVudGl0eSI6ICJleGFtcGxlLWFkYXB0ZXIiLAogICAgICAidmVyc2lvbiI6ICIxIiwKICAgICAgInJldmlzaW9uIjogInN5bnRoZXRpYy1zdGF0ZS0xIiwKICAgICAgInN0YXR1cyI6ICJhdmFpbGFibGUiCiAgICB9CiAgXQp9Cg==",
  "bytes": 3895,
  "evidence_id": "snapshot-inspection"
}
```

<a id="evidence-object"></a>

## Evidence Object

Identifies the producer, time and kind of evidence supporting an assessment or execution result.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="evidence-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="evidence-object-producer"></a>`producer` | string | Yes | Software or instrumentation responsible for the capture or evidence. Minimum length: `1`. |
| <a id="evidence-object-time"></a>`time` | string | Yes | Recorded observation time; it does not define causality. Minimum length: `1`. |
| <a id="evidence-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"inspection"`, `"compatibility_test"`, `"authorization"`, `"acceptance"`, `"import"`, `"continuation"`, `"synthetic"`. |
| <a id="evidence-object-detail"></a>`detail` | string | Yes | Explanation of the stated status or evidence. Minimum length: `1`. |
| <a id="evidence-object-reference"></a>`reference` | string | No | Opaque evidence or resolution locator; no implicit fetch is permitted. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "scenario",
  "producer": "asif-examples",
  "time": "2026-09-26T12:00:00Z",
  "kind": "synthetic",
  "detail": "Authored assumptions only. This receipt cannot authorize import or continuation."
}
```

<a id="transformation-object"></a>

## Transformation Object

Declares a proposed or accepted adaptation, its target, rule, losses and acceptance evidence.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="transformation-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="transformation-object-subject"></a>`subject` | [Subject Object](report-objects.md#subject-object) | Yes | Account identity or assessed subject, as defined by the containing object. |
| <a id="transformation-object-target"></a>`target` | string | Yes | Declared target value, model or symbolic-link target according to context. Minimum length: `1`. |
| <a id="transformation-object-rule"></a>`rule` | string | Yes | Explicit transformation rule rather than an implicit substitution. Minimum length: `1`. |
| <a id="transformation-object-losses"></a>`losses` | array of string | Yes | Explicit information changes or omissions; empty means none declared. Minimum items: `0`. |
| <a id="transformation-object-accepted"></a>`accepted` | boolean | Yes | Whether the declared transformation has been accepted with the required evidence. |
| <a id="transformation-object-evidence_ids"></a>`evidence_ids` | array of string | Yes | IDs of evidence records supporting this declaration. Minimum items: `0`. Items MUST be unique. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "adapt-native_import-native",
  "subject": {
    "kind": "native_import",
    "id": "native"
  },
  "target": "example-b/2",
  "rule": "Create a target-native representation with mapped identities and target ordering/index rules.",
  "losses": [
    "Behavioral equivalence remains an explicit acceptance decision."
  ],
  "accepted": false,
  "evidence_ids": [
    "scenario"
  ]
}
```

<a id="result-object"></a>

## Result Object

Common result shape for an attempted import or continuation operation, including explanatory evidence.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="result-object-status"></a>`status` | string | Yes | Recorded state at the relevant boundary; see the allowed values. Minimum length: `1`. |
| <a id="result-object-evidence_ids"></a>`evidence_ids` | array of string | Yes | IDs of evidence records supporting this declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="result-object-detail"></a>`detail` | string | Yes | Explanation of the stated status or evidence. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "status": "not_tested",
  "evidence_ids": [],
  "detail": "No agent was started."
}
```
