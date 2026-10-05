# Destination report object reference

Version: **0.4**. [Specification](../SPEC.md) · [Core](objects.md) · [Continuation](continuation-objects.md) · [Reports](report-objects.md)

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
- [Evidence Object](report-objects.md#evidence-object)
- [Transformation Object](report-objects.md#transformation-object)
- [Result Object](report-objects.md#result-object)

<a id="destination-report-object"></a>

## Destination Report Object

An expiring assessment bound to exact source bytes and a particular destination. Synthetic reports cannot claim execution.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="destination-report-object-report_version"></a>`report_version` | `"0.2"` | Yes | Version of the destination-report format. |
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
  "report_version": "0.2",
  "evaluation_mode": "synthetic",
  "id": "assessment-pending-remote-operation",
  "source": {
    "session_id": "session-pending-remote-operation",
    "capture_id": "capture-pending-remote-operation",
    "plan_id": "continue-main",
    "document_sha256": "dc12ec7e916d78633e33355378f998f90097d6cc569eb04d93878c53df778187"
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
    "capabilities_sha256": "c65340514a2aa2fcddeb38c3fa589b94aa324245a18534cb92f5d9687bb55a54"
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
      ]
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
      ]
    },
    {
      "subject": {
        "kind": "feature",
        "id": "asif.portable-continuation/0.2"
      },
      "status": "supported",
      "required": true,
      "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
      "evidence_ids": [
        "scenario"
      ]
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
      ]
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
      }
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
  "document_sha256": "dc12ec7e916d78633e33355378f998f90097d6cc569eb04d93878c53df778187"
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
| <a id="destination-object-capabilities_sha256"></a>`capabilities_sha256` | string | Yes | Digest of the destination capability snapshot used for this assessment. Pattern: `^[0-9a-f]{64}(?![\s\S])`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example-agent-b-runtime",
  "runtime": {
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
  },
  "capabilities_sha256": "53ed9bdbb19f79e9237aec78918633f31252cc2d1b339ac38dd29a451dfcf60c"
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

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "subject": {
    "kind": "resource",
    "id": "report"
  },
  "status": "supported",
  "required": true,
  "detail": "Assumed supported in this synthetic example; no actual destination check occurred.",
  "evidence_ids": [
    "scenario"
  ]
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
