# Core object reference

Version: **0.3**. [Specification](../SPEC.md) · [Core](objects.md) · [Continuation](continuation-objects.md) · [Reports](report-objects.md)

Every example below is JSON Schema checked. Object fragments use IDs resolved by an enclosing session or report; they are not standalone session documents. Full scenarios are in [examples](../examples/README.md). Required means unconditionally required; conditional rules follow each table. Normative [session semantics](../SEMANTICS.md) and [continuation rules](../CONTINUATION.md) also apply.

## Contents

- [ASIF Document Object](objects.md#asif-document-object)
- [Capture Object](objects.md#capture-object)
- [Producer Object](objects.md#producer-object)
- [Session Object](objects.md#session-object)
- [Native Identifier Object](objects.md#native-identifier-object)
- [Lineage Object](objects.md#lineage-object)
- [Event Reference Object](objects.md#event-reference-object)
- [Text Part Object](objects.md#text-part-object)
- [Resource Part Object](objects.md#resource-part-object)
- [Structured Part Object](objects.md#structured-part-object)
- [Opaque Part Object](objects.md#opaque-part-object)
- [Provenance Object](objects.md#provenance-object)
- [Provenance Source Object](objects.md#provenance-source-object)
- [Source Locator Object](objects.md#source-locator-object)
- [Participant Object](objects.md#participant-object)
- [Participant Child Session Object](objects.md#participant-child-session-object)
- [Execution Object](objects.md#execution-object)
- [Execution Model Object](objects.md#execution-model-object)
- [Tool Object](objects.md#tool-object)
- [Instruction Object](objects.md#instruction-object)
- [Instruction Scope Object](objects.md#instruction-scope-object)
- [Instruction Activation Object](objects.md#instruction-activation-object)
- [Capability Object](objects.md#capability-object)
- [Policy Object](objects.md#policy-object)
- [Configuration Object](objects.md#configuration-object)
- [Configuration Secret Requirements Object](objects.md#configuration-secret-requirements-object)
- [Configuration Model Object](objects.md#configuration-model-object)
- [Requirement Object](objects.md#requirement-object)
- [Environment Object](objects.md#environment-object)
- [Environment Definition Object](objects.md#environment-definition-object)
- [Resource Object](objects.md#resource-object)
- [Context Input Object](objects.md#context-input-object)
- [Context Object](objects.md#context-object)
- [Context Model Object](objects.md#context-model-object)
- [Context Request Parameters Object](objects.md#context-request-parameters-object)
- [Branch Object](objects.md#branch-object)
- [Branch Fork Object](objects.md#branch-fork-object)
- [Checkpoint Object](objects.md#checkpoint-object)
- [Open Call Object](objects.md#open-call-object)
- [Open Decision Object](objects.md#open-decision-object)
- [Task State Object](objects.md#task-state-object)
- [Usage Object](objects.md#usage-object)
- [Event Object](objects.md#event-object)
- [Event Data Object](objects.md#event-data-object)
- [Extension Map Object](objects.md#extension-map-object)
- [Message Data Object](objects.md#message-data-object)
- [Tool Call Data Object](objects.md#tool-call-data-object)
- [Tool Result Data Object](objects.md#tool-result-data-object)
- [Decision Request Data Object](objects.md#decision-request-data-object)
- [Decision Request Option Object](objects.md#decision-request-option-object)
- [Decision Resolution Data Object](objects.md#decision-resolution-data-object)
- [Task Update Data Object](objects.md#task-update-data-object)
- [Context Checkpoint Data Object](objects.md#context-checkpoint-data-object)
- [Configuration Change Data Object](objects.md#configuration-change-data-object)
- [Execution Transition Data Object](objects.md#execution-transition-data-object)
- [Resource Change Data Object](objects.md#resource-change-data-object)
- [Note Data Object](objects.md#note-data-object)
- [Extension Data Object](objects.md#extension-data-object)
- [Coverage Object](objects.md#coverage-object)
- [Loss Object](objects.md#loss-object)
- [Loss References Object](objects.md#loss-references-object)
- [Stream Segment Object](objects.md#stream-segment-object)
- [Stream Object](objects.md#stream-object)
- [External Binding Object](objects.md#external-binding-object)
- [External Binding Source Object](objects.md#external-binding-source-object)
- [External Binding Descriptor Object](objects.md#external-binding-descriptor-object)
- [External Call Descriptor Object](objects.md#external-call-descriptor-object)
- [External Request Descriptor Object](objects.md#external-request-descriptor-object)
- [External Request Option Object](objects.md#external-request-option-object)

<a id="asif-document-object"></a>

## ASIF Document Object

Root of an immutable session capture. Collections describe identity, history, effective context, resources and known state; coverage explains their limits.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="asif-document-object-asif_version"></a>`asif_version` | `"0.3"` | Yes | Exact ASIF draft version used by this document. |
| <a id="asif-document-object-capture"></a>`capture` | [Capture Object](objects.md#capture-object) | Yes | Immutable capture identity and observation boundary. |
| <a id="asif-document-object-session"></a>`session` | [Session Object](objects.md#session-object) | Yes | Logical session identity, objective and lineage. |
| <a id="asif-document-object-participants"></a>`participants` | array of [Participant Object](objects.md#participant-object) | Yes | Declared actors referenced by the captured interaction. |
| <a id="asif-document-object-events"></a>`events` | array of [Event Object](objects.md#event-object) | Yes | Immutable captured occurrences in serialization order. |
| <a id="asif-document-object-branches"></a>`branches` | array of [Branch Object](objects.md#branch-object) | Yes | Explicit selections of conversation history. Minimum items: `1`. |
| <a id="asif-document-object-executions"></a>`executions` | array of [Execution Object](objects.md#execution-object) | Yes | Observed agent activity intervals. |
| <a id="asif-document-object-contexts"></a>`contexts` | array of [Context Object](objects.md#context-object) | Yes | Resolved or proposed model inputs. |
| <a id="asif-document-object-configurations"></a>`configurations` | array of [Configuration Object](objects.md#configuration-object) | Yes | Immutable configuration snapshots. |
| <a id="asif-document-object-tools"></a>`tools` | array of [Tool Object](objects.md#tool-object) | Yes | Callable tool definitions referenced by activity or context. |
| <a id="asif-document-object-resources"></a>`resources` | array of [Resource Object](objects.md#resource-object) | Yes | Attachments, artifacts, memory and supporting resources. |
| <a id="asif-document-object-environments"></a>`environments` | array of [Environment Object](objects.md#environment-object) | Yes | Workspace, service or runtime descriptions. |
| <a id="asif-document-object-checkpoints"></a>`checkpoints` | array of [Checkpoint Object](objects.md#checkpoint-object) | Yes | State observations at branch boundaries, including each captured head. Minimum items: `1`. |
| <a id="asif-document-object-coverage"></a>`coverage` | array of [Coverage Object](objects.md#coverage-object) | Yes | One completeness declaration for every required session domain. Minimum items: `13`. Maximum items: `13`. |
| <a id="asif-document-object-losses"></a>`losses` | array of [Loss Object](objects.md#loss-object) | Yes | Explicit information changes or omissions; empty means none declared. |
| <a id="asif-document-object-required_features"></a>`required_features` | array of string | Yes | Feature identifiers whose semantics a consumer must understand for its capability claim. Items MUST be unique. |
| <a id="asif-document-object-usage"></a>`usage` | array of [Usage Object](objects.md#usage-object) | No | Recorded counters with scope, units and provenance. |
| <a id="asif-document-object-continuation"></a>`continuation` | [Continuation Profile Object](continuation-objects.md#continuation-profile-object) | No | Optional portable-continuation profile, gated by its required feature identifier. |
| <a id="asif-document-object-streams"></a>`streams` | array of [Stream Object](objects.md#stream-object) | No | Optional byte-fragment assemblies, gated by `asif.streams/0.1`. |
| <a id="asif-document-object-external_bindings"></a>`external_bindings` | array of [External Binding Object](objects.md#external-binding-object) | No | Optional prior-capture call/request descriptors, gated by `asif.external-bindings/0.1`. |

### Rules

See [session semantics](../SEMANTICS.md).

- When `continuation` is present, `required_features` MUST contain `asif.portable-continuation/0.1`.
- When `required_features` contains `asif.portable-continuation/0.1`, require `continuation`.
- When `streams` is present, `required_features` MUST contain `asif.streams/0.1`.
- When `required_features` contains `asif.streams/0.1`, require `streams`.
- When `external_bindings` is present, `required_features` MUST contain `asif.external-bindings/0.1`.
- When `required_features` contains `asif.external-bindings/0.1`, require `external_bindings`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "asif_version": "0.3",
  "capture": {
    "id": "capture-hello",
    "producer": {
      "name": "ASIF examples",
      "version": "0.3"
    },
    "consistency": "consistent",
    "boundary": "One authored greeting; no agent request was captured."
  },
  "session": {
    "id": "session-hello",
    "title": "Greeting",
    "native_ids": [],
    "lineage": []
  },
  "participants": [
    {
      "id": "human-1",
      "kind": "human"
    }
  ],
  "events": [
    {
      "id": "e1",
      "sequence": 0,
      "actor_id": "human-1",
      "kind": "message",
      "causes": [],
      "provenance": {
        "mode": "synthetic",
        "producer": "ASIF examples",
        "method": "Authored greeting example.",
        "inputs": []
      },
      "data": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Hello."
          }
        ]
      }
    }
  ],
  "branches": [
    {
      "id": "main",
      "event_ids": [
        "e1"
      ],
      "head_event_id": "e1"
    }
  ],
  "executions": [],
  "contexts": [],
  "configurations": [],
  "tools": [],
  "resources": [],
  "environments": [],
  "checkpoints": [
    {
      "id": "checkpoint-1",
      "branch_id": "main",
      "at_event_id": "e1",
      "knowledge": "unknown",
      "status": "unknown",
      "context_id": null,
      "configuration_id": null,
      "open_calls": [],
      "open_decisions": [],
      "tasks": [],
      "requirements": []
    }
  ],
  "coverage": [
    {
      "scope": "participants",
      "status": "complete",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "conversation",
      "status": "complete",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "branches",
      "status": "complete",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "executions",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "contexts",
      "status": "not_inspected",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "configuration",
      "status": "not_inspected",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "tools",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "decisions",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "tasks",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "resources",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "environment",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "native",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    },
    {
      "scope": "usage",
      "status": "known_empty",
      "detail": "Scope of this authored example."
    }
  ],
  "losses": [],
  "required_features": []
}
```

<a id="capture-object"></a>

## Capture Object

Identifies this immutable observation of a logical session and explains its capture boundary.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="capture-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="capture-object-producer"></a>`producer` | [Producer Object](objects.md#producer-object) | Yes | Software or instrumentation responsible for the capture or evidence. |
| <a id="capture-object-consistency"></a>`consistency` | enum | Yes | Whether the captured boundary is known to be consistent. One of `"consistent"`, `"partial"`, `"unknown"`. |
| <a id="capture-object-boundary"></a>`boundary` | string | Yes | Explanation or structured declaration of the observation boundary. Minimum length: `1`. |
| <a id="capture-object-started_at"></a>`started_at` | string | No | Recorded start time; omitted when unknown. Minimum length: `1`. |
| <a id="capture-object-ended_at"></a>`ended_at` | string | No | Recorded end time; omitted when unknown. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#3-identity-capture-and-references).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "capture-image-and-document",
  "producer": {
    "name": "asif-examples",
    "version": "1"
  },
  "consistency": "consistent",
  "boundary": "Invented example through e2; no real model or tool ran."
}
```

<a id="producer-object"></a>

## Producer Object

Identifies the software that created the capture, including its version.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="producer-object-name"></a>`name` | string | Yes | Recorded name; identity is carried separately by the ID. Minimum length: `1`. |
| <a id="producer-object-version"></a>`version` | string | Yes | Implementation or format version. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#3-identity-capture-and-references).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "name": "asif-example",
  "version": "1"
}
```

<a id="session-object"></a>

## Session Object

Identifies the logical interaction across captures, with its objective and lineage.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="session-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="session-object-title"></a>`title` | string | No | Human-readable session title. |
| <a id="session-object-objective"></a>`objective` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | No | Recorded session objective as ordered content parts. |
| <a id="session-object-native_ids"></a>`native_ids` | array of [Native Identifier Object](objects.md#native-identifier-object) | Yes | Original IDs, each qualified by provider and namespace. |
| <a id="session-object-lineage"></a>`lineage` | array of [Lineage Object](objects.md#lineage-object) | Yes | Explicit relationships to source sessions and captures. |

### Rules

See [normative session rules](../SEMANTICS.md#3-identity-capture-and-references).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "session-image-and-document",
  "title": "Image and PDF attachments",
  "native_ids": [],
  "lineage": []
}
```

<a id="native-identifier-object"></a>

## Native Identifier Object

Preserves an opaque identifier in a provider's namespace without making it an ASIF identity.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="native-identifier-object-provider"></a>`provider` | string | Yes | Provider identity for the named object or account. Minimum length: `1`. |
| <a id="native-identifier-object-namespace"></a>`namespace` | string | Yes | Namespace in which the opaque value is meaningful. Minimum length: `1`. |
| <a id="native-identifier-object-value"></a>`value` | string | Yes | Value interpreted according to the enclosing schema, dialect or counter. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#3-identity-capture-and-references).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example-agent-a",
  "namespace": "source-runtime",
  "value": "source-native"
}
```

<a id="lineage-object"></a>

## Lineage Object

Relates this session to the source of a continuation, fork, translation or copy.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="lineage-object-relation"></a>`relation` | enum | Yes | Relationship to the referenced source session. One of `"continuation"`, `"fork"`, `"translation"`, `"copy"`. |
| <a id="lineage-object-session_id"></a>`session_id` | string | Yes | Logical session ID of the referenced boundary. Minimum length: `1`. |
| <a id="lineage-object-capture_id"></a>`capture_id` | string | Yes | Immutable capture ID of the referenced boundary. Minimum length: `1`. |
| <a id="lineage-object-event_id"></a>`event_id` | string | No | Event identity, resolved locally unless an external capture is explicit. Minimum length: `1`. |
| <a id="lineage-object-inclusive"></a>`inclusive` | boolean | No | Whether the referenced boundary event is included. |

### Rules

See [normative session rules](../SEMANTICS.md#3-identity-capture-and-references).

- When `relation` is `"fork"`, require `event_id`, `inclusive`.
- When `relation` is `"translation"`, require `event_id`, `inclusive`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "relation": "fork",
  "session_id": "session-parent",
  "capture_id": "capture-parent",
  "event_id": "e2",
  "inclusive": true
}
```

<a id="event-reference-object"></a>

## Event Reference Object

Names a local event or explicitly names an event in another session capture. It never causes an automatic fetch.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="event-reference-object-event_id"></a>`event_id` | string | Yes | Event identity, resolved locally unless an external capture is explicit. Minimum length: `1`. |
| <a id="event-reference-object-session_id"></a>`session_id` | string | No | Logical session ID of the referenced boundary. Minimum length: `1`. |
| <a id="event-reference-object-capture_id"></a>`capture_id` | string | No | Immutable capture ID of the referenced boundary. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#3-identity-capture-and-references).

- When `session_id` is present, `capture_id` MUST also be present.
- When `capture_id` is present, `session_id` MUST also be present.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "event_id": "e1"
}
```

<a id="text-part-object"></a>

## Text Part Object

Carries exact Unicode text at one position in ordered content.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="text-part-object-kind"></a>`kind` | `"text"` | Yes | Discriminator selecting this object's interpretation. |
| <a id="text-part-object-text"></a>`text` | string | Yes | Exact Unicode text; embedded-resource bytes use UTF-8. |
| <a id="text-part-object-media_type"></a>`media_type` | string | No | Declared media type of the content or resource. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#5-event-envelope-ordering-and-content).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "text",
  "text": "The total is 5."
}
```

<a id="resource-part-object"></a>

## Resource Part Object

Places an attachment or other resource at one position in ordered content; availability belongs to the Resource Object.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="resource-part-object-kind"></a>`kind` | `"resource"` | Yes | Discriminator selecting this object's interpretation. |
| <a id="resource-part-object-resource_id"></a>`resource_id` | string | Yes | ID of the referenced Resource Object. Minimum length: `1`. |
| <a id="resource-part-object-description"></a>`description` | string | No | Human-readable description of this declaration. |

### Rules

See [normative session rules](../SEMANTICS.md#5-event-envelope-ordering-and-content).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "resource",
  "resource_id": "image",
  "description": "Original image."
}
```

<a id="structured-part-object"></a>

## Structured Part Object

Carries JSON whose interpretation is defined by a named schema. Unknown schemas remain opaque.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="structured-part-object-kind"></a>`kind` | `"structured"` | Yes | Discriminator selecting this object's interpretation. |
| <a id="structured-part-object-schema"></a>`schema` | string | Yes | Identifier of the schema that gives the structured value meaning. Minimum length: `1`. |
| <a id="structured-part-object-value"></a>`value` | JSON value | Yes | Value interpreted according to the enclosing schema, dialect or counter. |

### Rules

See [normative session rules](../SEMANTICS.md#5-event-envelope-ordering-and-content).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "structured",
  "schema": "example.table/1",
  "value": {
    "columns": [
      "item",
      "count"
    ],
    "rows": [
      [
        "books",
        3
      ]
    ]
  }
}
```

<a id="opaque-part-object"></a>

## Opaque Part Object

Preserves a resource whose semantic interpretation is unavailable to this reader.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="opaque-part-object-kind"></a>`kind` | `"opaque"` | Yes | Discriminator selecting this object's interpretation. |
| <a id="opaque-part-object-resource_id"></a>`resource_id` | string | Yes | ID of the referenced Resource Object. Minimum length: `1`. |
| <a id="opaque-part-object-semantic_type"></a>`semantic_type` | string | Yes | Namespaced meaning of content whose interpretation is unavailable. Minimum length: `1`. |
| <a id="opaque-part-object-reason"></a>`reason` | string | Yes | Reason for the recorded operation or unavailable interpretation. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#5-event-envelope-ordering-and-content).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "opaque",
  "resource_id": "native-state",
  "semantic_type": "example.agent-state/1",
  "reason": "No portable decoder is defined."
}
```

<a id="provenance-object"></a>

## Provenance Object

Distinguishes observed, reported, derived and synthetic evidence and identifies its sources.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="provenance-object-mode"></a>`mode` | enum | Yes | Representation or interpretation mode selected by the enclosing object. One of `"observed"`, `"reported"`, `"derived"`, `"synthetic"`. |
| <a id="provenance-object-producer"></a>`producer` | string | Yes | Software or instrumentation responsible for the capture or evidence. Minimum length: `1`. |
| <a id="provenance-object-sources"></a>`sources` | array of [Provenance Source Object](objects.md#provenance-source-object) | No | Original resource locations supporting this provenance. |
| <a id="provenance-object-method"></a>`method` | string | No | Method used to derive, synthesize or capture this record. Minimum length: `1`. |
| <a id="provenance-object-inputs"></a>`inputs` | array of [Event Reference Object](objects.md#event-reference-object) | No | Ordered inputs; provenance inputs identify supporting events. |

### Rules

See [normative session rules](../SEMANTICS.md#5-event-envelope-ordering-and-content).

- When `mode` is `"derived"`, require `method`, `inputs`.
- When `mode` is `"synthetic"`, require `method`, `inputs`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "mode": "reported",
  "producer": "example-meter"
}
```

<a id="provenance-source-object"></a>

## Provenance Source Object

Identifies a source resource and, optionally, a specific span or structured location within it.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="provenance-source-object-resource_id"></a>`resource_id` | string | Yes | ID of the referenced Resource Object. Minimum length: `1`. |
| <a id="provenance-source-object-locator"></a>`locator` | [Source Locator Object](objects.md#source-locator-object) | No | Location interpreted according to its declared syntax or availability. |

### Rules

See [normative session rules](../SEMANTICS.md#5-event-envelope-ordering-and-content).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "resource_id": "audio"
}
```

<a id="source-locator-object"></a>

## Source Locator Object

Selects bytes or a structured location within a provenance source; unknown syntaxes remain uninterpreted.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="source-locator-object-syntax"></a>`syntax` | string | Yes | Locator syntax, such as `bytes` or `json_pointer`. Minimum length: `1`. |
| <a id="source-locator-object-value"></a>`value` | JSON value | No | Value interpreted according to the enclosing schema, dialect or counter. |
| <a id="source-locator-object-offset"></a>`offset` | integer | No | Zero-based byte offset into the referenced resource. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="source-locator-object-length"></a>`length` | integer | No | Number of bytes in the selected span. Minimum: `0`. Maximum: `9007199254740991`. |

### Rules

See [normative session rules](../SEMANTICS.md#5-event-envelope-ordering-and-content).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "syntax": "bytes",
  "offset": 0,
  "length": 19
}
```

<a id="participant-object"></a>

## Participant Object

Identifies a person, agent, tool or service independently of the role used in a particular message.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="participant-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="participant-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"human"`, `"agent"`, `"tool"`, `"service"`, `"unknown"`. |
| <a id="participant-object-name"></a>`name` | string | No | Recorded name; identity is carried separately by the ID. |
| <a id="participant-object-provider"></a>`provider` | string | No | Provider identity for the named object or account. Minimum length: `1`. |
| <a id="participant-object-native_id"></a>`native_id` | string | No | Opaque participant identity in its source system. Minimum length: `1`. |
| <a id="participant-object-parent_participant_id"></a>`parent_participant_id` | string | No | ID of the parent or delegating participant. Minimum length: `1`. |
| <a id="participant-object-child_session"></a>`child_session` | [Participant Child Session Object](objects.md#participant-child-session-object) | No | Explicit reference to a delegated session capture. |

### Rules

See [normative session rules](../SEMANTICS.md#4-participants-and-executions).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "agent",
  "kind": "agent"
}
```

<a id="participant-child-session-object"></a>

## Participant Child Session Object

Names a delegated participant's separate session capture; its history is not implicitly included.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="participant-child-session-object-session_id"></a>`session_id` | string | Yes | Logical session ID of the referenced boundary. Minimum length: `1`. |
| <a id="participant-child-session-object-capture_id"></a>`capture_id` | string | Yes | Immutable capture ID of the referenced boundary. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#4-participants-and-executions).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "session_id": "session-1",
  "capture_id": "capture-1"
}
```

<a id="execution-object"></a>

## Execution Object

Records an agent activity interval and its observed state, model contexts and optional usage.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="execution-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="execution-object-participant_id"></a>`participant_id` | string | Yes | ID of the participant responsible for the execution. Minimum length: `1`. |
| <a id="execution-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"running"`, `"completed"`, `"failed"`, `"cancelled"`, `"interrupted"`, `"unknown"`. |
| <a id="execution-object-context_ids"></a>`context_ids` | array of string | Yes | IDs of contexts associated with this execution. Items MUST be unique. |
| <a id="execution-object-started_at"></a>`started_at` | string | No | Recorded start time; omitted when unknown. Minimum length: `1`. |
| <a id="execution-object-ended_at"></a>`ended_at` | string | No | Recorded end time; omitted when unknown. Minimum length: `1`. |
| <a id="execution-object-model"></a>`model` | [Execution Model Object](objects.md#execution-model-object) | No | Recorded model identity or settings for this scope. |
| <a id="execution-object-usage"></a>`usage` | array of [Usage Object](objects.md#usage-object) | No | Recorded counters with scope, units and provenance. |
| <a id="execution-object-error"></a>`error` | JSON value | No | Captured error evidence; its contents do not establish a recovery action. |

### Rules

See [normative session rules](../SEMANTICS.md#4-participants-and-executions).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "run-1",
  "participant_id": "agent",
  "status": "running",
  "context_ids": [
    "context-1"
  ]
}
```

<a id="execution-model-object"></a>

## Execution Model Object

Retains the model settings recorded for an execution. Provider-specific values require a declared interpretation before reuse.

### Fixed fields

No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.

### Rules

This is an open map. Preserve unknown values. Reuse requires support for their declared semantics; an empty map does not prove that the source had no hidden settings.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example",
  "id": "model-1",
  "temperature": 0.2
}
```

<a id="tool-object"></a>

## Tool Object

Defines a callable interface, including its JSON Schema input contract. A definition does not implement the tool.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="tool-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="tool-object-name"></a>`name` | string | Yes | Recorded name; identity is carried separately by the ID. Minimum length: `1`. |
| <a id="tool-object-description"></a>`description` | string | Yes | Human-readable description of this declaration. |
| <a id="tool-object-input_schema"></a>`input_schema` | object / boolean | Yes | JSON Schema 2020-12 contract for tool arguments; `true` declares no known restriction. |
| <a id="tool-object-output_schema"></a>`output_schema` | object / boolean | No | Optional JSON Schema contract for tool output. |
| <a id="tool-object-server_identity"></a>`server_identity` | string | No | Recorded identity of the tool server. Minimum length: `1`. |
| <a id="tool-object-revision"></a>`revision` | string | No | Versioned definition or task revision within its identity. Minimum length: `1`. |
| <a id="tool-object-resource_ids"></a>`resource_ids` | array of string | No | IDs of supporting resources; their availability is declared separately. Items MUST be unique. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "read-notes",
  "name": "example.notes.read",
  "description": "Read a meeting document by logical identifier.",
  "input_schema": {
    "type": "object",
    "properties": {
      "document_id": {
        "type": "string"
      }
    },
    "required": [
      "document_id"
    ],
    "additionalProperties": false
  }
}
```

<a id="instruction-object"></a>

## Instruction Object

Records instruction content, source, scope and activation without inventing unknown precedence.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="instruction-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="instruction-object-parts"></a>`parts` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content parts. Order is semantically significant. |
| <a id="instruction-object-scope"></a>`scope` | [Instruction Scope Object](objects.md#instruction-scope-object) | Yes | Domain or activation scope to which this declaration applies. |
| <a id="instruction-object-activation"></a>`activation` | [Instruction Activation Object](objects.md#instruction-activation-object) | Yes | Conditions under which an instruction or rule applies. |
| <a id="instruction-object-provenance"></a>`provenance` | [Provenance Object](objects.md#provenance-object) | Yes | Evidence classification and source attribution. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "workspace-rule",
  "parts": [
    {
      "kind": "text",
      "text": "Use the declared workspace for file operations."
    }
  ],
  "scope": {
    "dialect": "example.scope/1",
    "value": "workspace"
  },
  "activation": {
    "dialect": "example.activation/1",
    "value": "always"
  },
  "provenance": {
    "mode": "synthetic",
    "producer": "asif-examples",
    "method": "Authored configuration fixture.",
    "inputs": []
  }
}
```

<a id="instruction-scope-object"></a>

## Instruction Scope Object

Preserves a source dialect's scope declaration. Portable scope bindings are defined by the continuation profile.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="instruction-scope-object-dialect"></a>`dialect` | string | Yes | Identifier of the language used to interpret the associated value. Minimum length: `1`. |
| <a id="instruction-scope-object-value"></a>`value` | JSON value | Yes | Value interpreted according to the enclosing schema, dialect or counter. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "dialect": "example.scope/1",
  "value": "workspace"
}
```

<a id="instruction-activation-object"></a>

## Instruction Activation Object

Preserves a source dialect's activation declaration. Portable activation bindings are defined by the continuation profile.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="instruction-activation-object-dialect"></a>`dialect` | string | Yes | Identifier of the language used to interpret the associated value. Minimum length: `1`. |
| <a id="instruction-activation-object-value"></a>`value` | JSON value | Yes | Value interpreted according to the enclosing schema, dialect or counter. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "dialect": "example.scope/1",
  "value": "workspace"
}
```

<a id="capability-object"></a>

## Capability Object

Describes a skill, plugin, hook, connection or other runtime facility and its supporting resources.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="capability-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="capability-object-type"></a>`type` | string | Yes | Namespaced semantic type or entity type, as defined by the enclosing object. Minimum length: `1`. |
| <a id="capability-object-definition"></a>`definition` | JSON value | Yes | Dialect-specific definition retained without guessing unknown semantics. |
| <a id="capability-object-resource_ids"></a>`resource_ids` | array of string | Yes | IDs of supporting resources; their availability is declared separately. Items MUST be unique. |
| <a id="capability-object-required"></a>`required` | boolean | Yes | Whether this subject is required for the selected capability. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "summary-skill",
  "type": "example.skill",
  "definition": {
    "id": "inventory-summary",
    "version": "1"
  },
  "resource_ids": [
    "skill-template"
  ],
  "required": true
}
```

<a id="policy-object"></a>

## Policy Object

Records a named policy dialect and whether its restrictions were enforced.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="policy-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="policy-object-type"></a>`type` | string | Yes | Namespaced semantic type or entity type, as defined by the enclosing object. Minimum length: `1`. |
| <a id="policy-object-definition"></a>`definition` | JSON value | Yes | Dialect-specific definition retained without guessing unknown semantics. |
| <a id="policy-object-enforcing"></a>`enforcing` | boolean | Yes | Whether this policy enforces restrictions rather than providing advice. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "workspace-only",
  "type": "example.policy/1",
  "definition": {
    "file_access": "declared-workspace"
  },
  "enforcing": true
}
```

<a id="configuration-object"></a>

## Configuration Object

An immutable snapshot of instructions, capabilities, policies and credential prerequisites.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="configuration-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="configuration-object-instructions"></a>`instructions` | array of [Instruction Object](objects.md#instruction-object) | Yes | Recorded instruction sequence; effective order must be known before equivalent continuation. |
| <a id="configuration-object-capabilities"></a>`capabilities` | array of [Capability Object](objects.md#capability-object) | Yes | Required or declared abilities for this configuration or model. |
| <a id="configuration-object-policies"></a>`policies` | array of [Policy Object](objects.md#policy-object) | Yes | Recorded policy declarations. |
| <a id="configuration-object-secret_requirements"></a>`secret_requirements` | array of [Configuration Secret Requirements Object](objects.md#configuration-secret-requirements-object) | Yes | Logical credential handles and purposes; no credential values. |
| <a id="configuration-object-knowledge"></a>`knowledge` | enum | Yes | How much of the effective state or configuration is known. One of `"effective"`, `"declared"`, `"partial"`, `"unknown"`. |
| <a id="configuration-object-model"></a>`model` | [Configuration Model Object](objects.md#configuration-model-object) | No | Recorded model identity or settings for this scope. |
| <a id="configuration-object-environment_ids"></a>`environment_ids` | array of string | No | IDs of environments required by this configuration. Items MUST be unique. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "config-1",
  "instructions": [],
  "capabilities": [],
  "policies": [],
  "secret_requirements": [],
  "knowledge": "partial"
}
```

<a id="configuration-secret-requirements-object"></a>

## Configuration Secret Requirements Object

Names a credential prerequisite using a logical handle and purpose. Credential values do not belong here.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="configuration-secret-requirements-object-handle"></a>`handle` | string | Yes | Logical credential name to resolve at the destination. Minimum length: `1`. |
| <a id="configuration-secret-requirements-object-purpose"></a>`purpose` | string | Yes | Intended use of the record or resource. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "handle": "publisher-login",
  "purpose": "Authenticate to the target publishing account."
}
```

<a id="configuration-model-object"></a>

## Configuration Model Object

Retains configuration-level model settings; a context can identify the settings used for a particular request.

### Fixed fields

No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.

### Rules

This is an open map. Preserve unknown values. Reuse requires support for their declared semantics; an empty map does not prove that the source had no hidden settings.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example",
  "id": "model-1",
  "temperature": 0.2
}
```

<a id="requirement-object"></a>

## Requirement Object

States a prerequisite and the capabilities for which it matters, including whether its resolution is known.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="requirement-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="requirement-object-kind"></a>`kind` | string | Yes | Discriminator selecting this object's interpretation. Minimum length: `1`. |
| <a id="requirement-object-description"></a>`description` | string | Yes | Human-readable description of this declaration. Minimum length: `1`. |
| <a id="requirement-object-required_for"></a>`required_for` | array of enum | Yes | Capabilities that depend on this prerequisite. Items MUST be unique. |
| <a id="requirement-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"available"`, `"unresolved"`, `"unavailable"`, `"unsupported"`. |
| <a id="requirement-object-resource_id"></a>`resource_id` | string | No | ID of the referenced Resource Object. Minimum length: `1`. |
| <a id="requirement-object-capability_id"></a>`capability_id` | string | No | Referenced capability identity within the applicable configuration. Minimum length: `1`. |
| <a id="requirement-object-environment_id"></a>`environment_id` | string | No | Referenced Environment Object ID. Minimum length: `1`. |
| <a id="requirement-object-secret_handle"></a>`secret_handle` | string | No | Logical credential handle referenced by this requirement. Minimum length: `1`. |

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "req-1",
  "kind": "asif.decision",
  "description": "Resolve approval-1 under destination policy before any tool execution.",
  "required_for": [
    "continue"
  ],
  "status": "unresolved"
}
```

<a id="environment-object"></a>

## Environment Object

Describes a workspace, service or runtime environment and its dependencies without granting access to it.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="environment-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="environment-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"workspace"`, `"service"`, `"runtime"`, `"other"`. |
| <a id="environment-object-description"></a>`description` | string | Yes | Human-readable description of this declaration. Minimum length: `1`. |
| <a id="environment-object-resource_ids"></a>`resource_ids` | array of string | Yes | IDs of supporting resources; their availability is declared separately. Items MUST be unique. |
| <a id="environment-object-requirements"></a>`requirements` | array of [Requirement Object](objects.md#requirement-object) | Yes | Prerequisites for the stated capability. |
| <a id="environment-object-definition"></a>`definition` | [Environment Definition Object](objects.md#environment-definition-object) | No | Dialect-specific definition retained without guessing unknown semantics. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "project-env",
  "kind": "workspace",
  "description": "Synthetic project directory at the captured boundary.",
  "resource_ids": [
    "source-csv",
    "output-csv",
    "report"
  ],
  "requirements": [],
  "definition": {
    "dialect": "example.workspace/1",
    "value": {
      "cwd": "/Users/example/project"
    }
  }
}
```

<a id="environment-definition-object"></a>

## Environment Definition Object

Preserves environment-specific data under an explicit dialect identifier.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="environment-definition-object-dialect"></a>`dialect` | string | Yes | Identifier of the language used to interpret the associated value. Minimum length: `1`. |
| <a id="environment-definition-object-value"></a>`value` | JSON value | Yes | Value interpreted according to the enclosing schema, dialect or counter. |

### Rules

See [normative session rules](../SEMANTICS.md#9-configuration-and-environment).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "dialect": "example.scope/1",
  "value": "workspace"
}
```

<a id="resource-object"></a>

## Resource Object

Describes attachment or dependency identity, availability and integrity. Embedded text, base64 and file-backed resources share the same decoded-byte semantics.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="resource-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="resource-object-media_type"></a>`media_type` | string | Yes | Declared media type of the content or resource. Minimum length: `1`. |
| <a id="resource-object-availability"></a>`availability` | enum | Yes | Whether and how the referenced content is available. One of `"embedded"`, `"external"`, `"unavailable"`, `"excluded"`, `"redacted"`, `"unknown"`. |
| <a id="resource-object-purpose"></a>`purpose` | string | Yes | Intended use of the record or resource. Minimum length: `1`. |
| <a id="resource-object-name"></a>`name` | string | No | Recorded name; identity is carried separately by the ID. |
| <a id="resource-object-original_location"></a>`original_location` | string | No | Source location retained as metadata; not permission to access it. |
| <a id="resource-object-bytes"></a>`bytes` | integer | No | Exact decoded byte count. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="resource-object-sha256"></a>`sha256` | string | No | Lowercase SHA-256 digest of exact decoded resource bytes. Pattern: `^[0-9a-f]{64}(?![\s\S])`. |
| <a id="resource-object-text"></a>`text` | string | No | Exact Unicode text; embedded-resource bytes use UTF-8. |
| <a id="resource-object-data"></a>`data` | string | No | Base64 encoding of the embedded resource bytes. |
| <a id="resource-object-path"></a>`path` | string | No | Portable relative path resolved against the session document or package root. Minimum length: `1`. |
| <a id="resource-object-locator"></a>`locator` | string | No | External resource locator. Reading the document MUST NOT fetch it automatically. Minimum length: `1`. |
| <a id="resource-object-explanation"></a>`explanation` | string | No | Reason for the declaration or limitation. Minimum length: `1`. |
| <a id="resource-object-provenance"></a>`provenance` | [Provenance Object](objects.md#provenance-object) | No | Evidence classification and source attribution. |

### Rules

See [resource rules](../SEMANTICS.md#10-resources-and-availability). Embedded resources MUST select exactly one of `text`, `data` and `path`, with verified decoded `bytes` and `sha256`. Other availability states MUST explain the limitation; external resources also require a locator.

- When `availability` is `"embedded"`, require `bytes`, `sha256`; exactly one of `text`, `data`, `path`.
- When `availability` is `"external"`, require `locator`, `explanation`.
- When `availability` is `"unavailable"`, require `explanation`.
- When `availability` is `"excluded"`, require `explanation`.
- When `availability` is `"redacted"`, require `explanation`.
- When `availability` is `"unknown"`, require `explanation`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "unknown",
  "media_type": "image/png",
  "purpose": "input",
  "availability": "unknown",
  "explanation": "The exporter did not inspect attachment availability."
}
```

### Embedded UTF-8 attachment

The three embedded examples represent the same decoded bytes and therefore use the same length and digest. The path example assumes those bytes are supplied at `assets/items.csv`.

```json
{
  "id": "attachment-csv",
  "media_type": "text/csv",
  "purpose": "input",
  "availability": "embedded",
  "bytes": 19,
  "sha256": "de0c9962d43f7e783381c9f07d89c60589342163340cb53a55c2e0cf3f9859b6",
  "text": "item,count\nbooks,3\n"
}
```

### Embedded base64 attachment

The three embedded examples represent the same decoded bytes and therefore use the same length and digest. The path example assumes those bytes are supplied at `assets/items.csv`.

```json
{
  "id": "attachment-csv",
  "media_type": "text/csv",
  "purpose": "input",
  "availability": "embedded",
  "bytes": 19,
  "sha256": "de0c9962d43f7e783381c9f07d89c60589342163340cb53a55c2e0cf3f9859b6",
  "data": "aXRlbSxjb3VudApib29rcywzCg=="
}
```

### File-backed attachment

The three embedded examples represent the same decoded bytes and therefore use the same length and digest. The path example assumes those bytes are supplied at `assets/items.csv`.

```json
{
  "id": "attachment-csv",
  "media_type": "text/csv",
  "purpose": "input",
  "availability": "embedded",
  "bytes": 19,
  "sha256": "de0c9962d43f7e783381c9f07d89c60589342163340cb53a55c2e0cf3f9859b6",
  "path": "assets/items.csv"
}
```

### External attachment

The missing bytes are not replaced with invented text. The referring Resource Part retains this resource ID.

```json
{
  "id": "attachment-original",
  "media_type": "application/pdf",
  "purpose": "input",
  "availability": "external",
  "explanation": "The source only retained a remote locator.",
  "locator": "https://example.invalid/report.pdf"
}
```

### Unavailable attachment

The missing bytes are not replaced with invented text. The referring Resource Part retains this resource ID.

```json
{
  "id": "attachment-original",
  "media_type": "application/pdf",
  "purpose": "input",
  "availability": "unavailable",
  "explanation": "The source attachment was deleted before capture."
}
```

### Excluded attachment

The missing bytes are not replaced with invented text. The referring Resource Part retains this resource ID.

```json
{
  "id": "attachment-original",
  "media_type": "application/pdf",
  "purpose": "input",
  "availability": "excluded",
  "explanation": "The producer intentionally excluded these bytes."
}
```

### Redacted attachment

The missing bytes are not replaced with invented text. The referring Resource Part retains this resource ID.

```json
{
  "id": "attachment-original",
  "media_type": "application/pdf",
  "purpose": "input",
  "availability": "redacted",
  "explanation": "The original contains withheld content; sanitized content is a separate resource."
}
```

### Unknown attachment

The missing bytes are not replaced with invented text. The referring Resource Part retains this resource ID.

```json
{
  "id": "attachment-original",
  "media_type": "application/pdf",
  "purpose": "input",
  "availability": "unknown",
  "explanation": "The producer could not determine availability."
}
```

<a id="context-input-object"></a>

## Context Input Object

One resolved, ordered input to a model: a message, tool call or tool result, with source attribution.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="context-input-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="context-input-object-role"></a>`role` | enum | Yes | Message role used for this input, independently of participant identity. One of `"user"`, `"assistant"`, `"system"`, `"developer"`, `"tool"`, `"unknown"`. |
| <a id="context-input-object-parts"></a>`parts` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content parts. Order is semantically significant. |
| <a id="context-input-object-source_events"></a>`source_events` | array of [Event Reference Object](objects.md#event-reference-object) | Yes | Events from which this resolved input was obtained. |
| <a id="context-input-object-transformation"></a>`transformation` | string | No | Explanation of a known change from source content. Minimum length: `1`. |
| <a id="context-input-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"message"`, `"tool_call"`, `"tool_result"`. |
| <a id="context-input-object-call_id"></a>`call_id` | string | No | Session-scoped identity of one logical invocation. Minimum length: `1`. |
| <a id="context-input-object-tool_id"></a>`tool_id` | string | No | ID of the referenced tool definition. Minimum length: `1`. |
| <a id="context-input-object-arguments"></a>`arguments` | JSON value | No | Exact known JSON argument value; completeness is declared separately. |
| <a id="context-input-object-arguments_status"></a>`arguments_status` | enum | No | Whether the known arguments are complete, partial or unknown. One of `"complete"`, `"partial"`, `"unknown"`. |
| <a id="context-input-object-result_index"></a>`result_index` | integer | No | Monotonically increasing result position within the call's selected history. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="context-input-object-terminal"></a>`terminal` | boolean | No | Whether this is the final result or fragment in its declared scope. |
| <a id="context-input-object-outcome"></a>`outcome` | enum | No | Recorded result or assessment outcome; unknown remains explicit. One of `"success"`, `"error"`, `"cancelled"`, `"unknown"`. |

### Rules

See [normative session rules](../SEMANTICS.md#8-context-and-compaction).

- When `kind` is `"tool_call"`, require `call_id`, `tool_id`, `arguments`, `arguments_status`; `role` MUST be `"assistant"`.
- When `kind` is `"tool_result"`, require `call_id`, `result_index`, `terminal`, `outcome`; `role` MUST be `"tool"`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "input-1",
  "role": "user",
  "parts": [
    {
      "kind": "text",
      "text": "Summarize the selected meeting notes."
    }
  ],
  "source_events": [
    {
      "event_id": "e1"
    }
  ],
  "kind": "message"
}
```

### Message input

This is one resolved input from the complete another-computer example. Source references provide provenance, not instructions to guess the input.

```json
{
  "id": "input-instruction",
  "kind": "message",
  "role": "system",
  "parts": [
    {
      "kind": "text",
      "text": "Use the declared workspace for file operations."
    }
  ],
  "source_events": []
}
```

### Tool Call input

This is one resolved input from the complete another-computer example. Source references provide provenance, not instructions to guess the input.

```json
{
  "id": "input-e2",
  "kind": "tool_call",
  "role": "assistant",
  "parts": [],
  "source_events": [
    {
      "event_id": "e2"
    }
  ],
  "call_id": "call-1",
  "tool_id": "summarize",
  "arguments": {
    "resource_id": "source-csv"
  },
  "arguments_status": "complete"
}
```

### Tool Result input

This is one resolved input from the complete another-computer example. Source references provide provenance, not instructions to guess the input.

```json
{
  "id": "input-e3",
  "kind": "tool_result",
  "role": "tool",
  "parts": [
    {
      "kind": "resource",
      "resource_id": "output-csv",
      "description": "CSV with total row."
    },
    {
      "kind": "resource",
      "resource_id": "report",
      "description": "Markdown report."
    }
  ],
  "source_events": [
    {
      "event_id": "e3"
    }
  ],
  "call_id": "call-1",
  "result_index": 0,
  "terminal": true,
  "outcome": "success"
}
```

<a id="context-object"></a>

## Context Object

Records or proposes the actual ordered model input independently of conversation and branch order.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="context-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="context-object-branch_id"></a>`branch_id` | string | Yes | ID of the selected branch. Minimum length: `1`. |
| <a id="context-object-at_event_id"></a>`at_event_id` | string / null | Yes | Event at the recorded boundary, or null for an empty boundary. |
| <a id="context-object-purpose"></a>`purpose` | enum | Yes | Intended use of the record or resource. One of `"model_request"`, `"continuation"`, `"summary"`. |
| <a id="context-object-fidelity"></a>`fidelity` | enum | Yes | How closely this context represents the known model input. One of `"exact"`, `"reconstructed"`, `"partial"`, `"unknown"`. |
| <a id="context-object-inputs"></a>`inputs` | array of [Context Input Object](objects.md#context-input-object) | Yes | Ordered inputs; provenance inputs identify supporting events. |
| <a id="context-object-tool_ids"></a>`tool_ids` | array of string | Yes | IDs of tools made available to this context. Items MUST be unique. |
| <a id="context-object-configuration_id"></a>`configuration_id` | string | No | ID of the configuration snapshot used at this boundary. Minimum length: `1`. |
| <a id="context-object-model"></a>`model` | [Context Model Object](objects.md#context-model-object) | No | Recorded model identity or settings for this scope. |
| <a id="context-object-request_parameters"></a>`request_parameters` | [Context Request Parameters Object](objects.md#context-request-parameters-object) | No | Recorded request settings; unknown provider-specific semantics are not inferred. |

### Rules

See [normative session rules](../SEMANTICS.md#8-context-and-compaction).

- When `fidelity` is `"exact"`, require `configuration_id`, `request_parameters`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "context-1",
  "branch_id": "main",
  "at_event_id": "e1",
  "purpose": "model_request",
  "fidelity": "reconstructed",
  "inputs": [
    {
      "id": "input-1",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "Summarize the selected meeting notes."
        }
      ],
      "source_events": [
        {
          "event_id": "e1"
        }
      ],
      "kind": "message"
    }
  ],
  "tool_ids": [
    "read-notes"
  ],
  "configuration_id": "config-1"
}
```

<a id="context-model-object"></a>

## Context Model Object

Retains the model identity and settings associated with this context.

### Fixed fields

No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.

### Rules

This is an open map. Preserve unknown values. Reuse requires support for their declared semantics; an empty map does not prove that the source had no hidden settings.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example",
  "id": "model-1",
  "temperature": 0.2
}
```

<a id="context-request-parameters-object"></a>

## Context Request Parameters Object

Retains request settings associated with this exact context; unknown provider parameters are not silently translated.

### Fixed fields

No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.

### Rules

This is an open map. Preserve unknown values. Reuse requires support for their declared semantics; an empty map does not prove that the source had no hidden settings.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "max_output_tokens": 1024
}
```

<a id="branch-object"></a>

## Branch Object

Selects an ordered conversation history and its head within this capture.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="branch-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="branch-object-event_ids"></a>`event_ids` | array of string | Yes | Ordered, duplicate-free selection of included event IDs. Items MUST be unique. |
| <a id="branch-object-head_event_id"></a>`head_event_id` | string / null | Yes | Final selected event ID, or null for an empty branch. |
| <a id="branch-object-fork"></a>`fork` | [Branch Fork Object](objects.md#branch-fork-object) | No | Explicit source boundary for a branch fork. |

### Rules

See [normative session rules](../SEMANTICS.md#7-branches-and-selected-history).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "main",
  "event_ids": [
    "e1"
  ],
  "head_event_id": "e1"
}
```

<a id="branch-fork-object"></a>

## Branch Fork Object

Records the source branch boundary at which histories diverged. It does not imply a filesystem rewind.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="branch-fork-object-session_id"></a>`session_id` | string | Yes | Logical session ID of the referenced boundary. Minimum length: `1`. |
| <a id="branch-fork-object-capture_id"></a>`capture_id` | string | Yes | Immutable capture ID of the referenced boundary. Minimum length: `1`. |
| <a id="branch-fork-object-branch_id"></a>`branch_id` | string | Yes | ID of the selected branch. Minimum length: `1`. |
| <a id="branch-fork-object-event_id"></a>`event_id` | string / null | Yes | Event identity, resolved locally unless an external capture is explicit. |
| <a id="branch-fork-object-inclusive"></a>`inclusive` | boolean | Yes | Whether the referenced boundary event is included. |

### Rules

See [normative session rules](../SEMANTICS.md#7-branches-and-selected-history).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "session_id": "session-parent",
  "capture_id": "capture-parent",
  "branch_id": "main",
  "event_id": "e2",
  "inclusive": true
}
```

<a id="checkpoint-object"></a>

## Checkpoint Object

Records known state at a selected branch boundary, including unresolved calls, decisions and task revisions.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="checkpoint-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="checkpoint-object-branch_id"></a>`branch_id` | string | Yes | ID of the selected branch. Minimum length: `1`. |
| <a id="checkpoint-object-at_event_id"></a>`at_event_id` | string / null | Yes | Event at the recorded boundary, or null for an empty boundary. |
| <a id="checkpoint-object-knowledge"></a>`knowledge` | enum | Yes | How much of the effective state or configuration is known. One of `"observed"`, `"derived"`, `"unknown"`. |
| <a id="checkpoint-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"idle"`, `"active"`, `"waiting"`, `"stopped"`, `"ended"`, `"unknown"`. |
| <a id="checkpoint-object-context_id"></a>`context_id` | string / null | Yes | ID of the selected Context Object. |
| <a id="checkpoint-object-configuration_id"></a>`configuration_id` | string / null | Yes | ID of the configuration snapshot used at this boundary. |
| <a id="checkpoint-object-open_calls"></a>`open_calls` | array of [Open Call Object](objects.md#open-call-object) | Yes | Unresolved invocation identities at this checkpoint. |
| <a id="checkpoint-object-open_decisions"></a>`open_decisions` | array of [Open Decision Object](objects.md#open-decision-object) | Yes | Unresolved decision-request identities at this checkpoint. |
| <a id="checkpoint-object-tasks"></a>`tasks` | array of [Task State Object](objects.md#task-state-object) | Yes | Task revision selections at this checkpoint. |
| <a id="checkpoint-object-requirements"></a>`requirements` | array of [Requirement Object](objects.md#requirement-object) | Yes | Prerequisites for the stated capability. |

### Rules

See [normative session rules](../SEMANTICS.md#11-checkpoints-and-unresolved-work).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "head",
  "branch_id": "main",
  "at_event_id": "e4",
  "knowledge": "observed",
  "status": "idle",
  "context_id": "continue-context",
  "configuration_id": "effective",
  "open_calls": [],
  "open_decisions": [],
  "tasks": [],
  "requirements": []
}
```

<a id="open-call-object"></a>

## Open Call Object

Records a call whose outcome remains unresolved at the checkpoint; it does not authorize replay.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="open-call-object-call_id"></a>`call_id` | string | Yes | Session-scoped identity of one logical invocation. Minimum length: `1`. |
| <a id="open-call-object-state"></a>`state` | enum | Yes | Recorded pending or observed state; it is not a live process assertion. One of `"pending"`, `"outcome_unknown"`. |

### Rules

See [normative session rules](../SEMANTICS.md#11-checkpoints-and-unresolved-work).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "call_id": "call-1",
  "state": "outcome_unknown"
}
```

<a id="open-decision-object"></a>

## Open Decision Object

Records an unresolved decision at the checkpoint; absence of a resolution is not consent.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="open-decision-object-request_id"></a>`request_id` | string | Yes | Session-scoped identity of the exact decision request. Minimum length: `1`. |
| <a id="open-decision-object-state"></a>`state` | enum | Yes | Recorded pending or observed state; it is not a live process assertion. One of `"pending"`, `"outcome_unknown"`. |

### Rules

See [normative session rules](../SEMANTICS.md#11-checkpoints-and-unresolved-work).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "request_id": "approval-1",
  "state": "pending"
}
```

<a id="task-state-object"></a>

## Task State Object

Selects the current revision of a recorded task at a checkpoint.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="task-state-object-task_id"></a>`task_id` | string | Yes | Identity of the versioned task. Minimum length: `1`. |
| <a id="task-state-object-revision"></a>`revision` | integer | Yes | Versioned definition or task revision within its identity. Minimum: `0`. Maximum: `9007199254740991`. |

### Rules

See [normative session rules](../SEMANTICS.md#11-checkpoints-and-unresolved-work).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "task_id": "summary",
  "revision": 1
}
```

<a id="usage-object"></a>

## Usage Object

Attributes a measured or reported counter to an explicit scope, unit and provenance.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="usage-object-scope"></a>`scope` | enum | Yes | Domain or activation scope to which this declaration applies. One of `"event"`, `"turn"`, `"execution"`, `"session"`. |
| <a id="usage-object-scope_id"></a>`scope_id` | string | Yes | Identity of the entity to which the counter applies. Minimum length: `1`. |
| <a id="usage-object-unit"></a>`unit` | string | Yes | Unit of the reported counter; counters with different units cannot be summed directly. Minimum length: `1`. |
| <a id="usage-object-value"></a>`value` | number | Yes | Value interpreted according to the enclosing schema, dialect or counter. Minimum: `0`. |
| <a id="usage-object-counter"></a>`counter` | enum | Yes | Whether this value is a delta or a cumulative counter; cumulative observations MUST NOT be added as independent deltas. One of `"delta"`, `"cumulative"`. |
| <a id="usage-object-provenance"></a>`provenance` | [Provenance Object](objects.md#provenance-object) | Yes | Evidence classification and source attribution. |

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "scope": "execution",
  "scope_id": "execution-1",
  "unit": "tokens",
  "value": 120,
  "counter": "delta",
  "provenance": {
    "mode": "reported",
    "producer": "example-meter"
  }
}
```

<a id="event-object"></a>

## Event Object

Immutable envelope for a recorded occurrence, including identity, attribution, causality and kind-specific data.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="event-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="event-object-sequence"></a>`sequence` | integer | Yes | Unique nonnegative serialization position in this capture; not a causal or wall-clock timestamp. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="event-object-actor_id"></a>`actor_id` | string | Yes | ID of the participant responsible for the event. Minimum length: `1`. |
| <a id="event-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"message"`, `"tool_call"`, `"tool_result"`, `"decision_request"`, `"decision_resolution"`, `"task_update"`, `"context_checkpoint"`, `"configuration_change"`, `"execution_transition"`, `"resource_change"`, `"note"`, `"extension"`. |
| <a id="event-object-causes"></a>`causes` | array of [Event Reference Object](objects.md#event-reference-object) | Yes | Explicit causal predecessor event references. |
| <a id="event-object-provenance"></a>`provenance` | [Provenance Object](objects.md#provenance-object) | Yes | Evidence classification and source attribution. |
| <a id="event-object-data"></a>`data` | [Event Data Object](objects.md#event-data-object) | Yes | Kind-specific payload; for an embedded resource this is base64-encoded bytes. |
| <a id="event-object-time"></a>`time` | string | No | Recorded observation time; it does not define causality. Minimum length: `1`. |
| <a id="event-object-execution_id"></a>`execution_id` | string | No | ID of the associated execution. Minimum length: `1`. |
| <a id="event-object-supersedes"></a>`supersedes` | [Event Reference Object](objects.md#event-reference-object) | No | Reference to an earlier record corrected by this event; evidence remains preserved. |
| <a id="event-object-extensions"></a>`extensions` | [Extension Map Object](objects.md#extension-map-object) | No | Namespaced extension values. |

### Rules

See [event rules](../SEMANTICS.md#5-event-envelope-ordering-and-content). The enclosing `kind` selects one of the event-data objects below. Local causal edges MUST be acyclic and point to earlier serialized events.

- When `kind` is `"message"`, `data` requires `role`, `parts`.
- When `kind` is `"tool_call"`, `data` requires `call_id`, `tool_id`, `arguments`, `arguments_status`.
- When `kind` is `"tool_result"`, `data` requires `call_id`, `result_index`, `terminal`, `outcome`, `parts`.
- When `kind` is `"decision_request"`, `data` requires `request_id`, `decision_kind`, `prompt`, `options`.
- When `kind` is `"decision_resolution"`, `data` requires `request_id`, `outcome`, `answer`.
- When `kind` is `"task_update"`, `data` requires `task_id`, `revision`, `status`, `parts`.
- When `kind` is `"context_checkpoint"`, `data` requires `context_id`, `reason`.
- When `kind` is `"configuration_change"`, `data` requires `configuration_id`.
- When `kind` is `"execution_transition"`, `data` requires `execution_id`, `status`.
- When `kind` is `"resource_change"`, `data` requires `resource_id`, `operation`.
- When `kind` is `"note"`, `data` requires `parts`, `category`.
- When `kind` is `"extension"`, `data` requires `type`, `value`, `interpretation_required`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "e1",
  "sequence": 0,
  "actor_id": "person",
  "kind": "message",
  "causes": [],
  "provenance": {
    "mode": "synthetic",
    "producer": "asif-example",
    "method": "authored conformance example",
    "inputs": []
  },
  "data": {
    "role": "user",
    "parts": [
      {
        "kind": "text",
        "text": "Summarize the selected meeting notes."
      }
    ]
  }
}
```

<a id="event-data-object"></a>

## Event Data Object

Discriminated payload selected by the enclosing Event Object's `kind`. Use the corresponding event data object below.

### Fixed fields

No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "role": "user",
  "parts": [
    {
      "kind": "text",
      "text": "Summarize the attachment."
    }
  ]
}
```

<a id="extension-map-object"></a>

## Extension Map Object

Carries namespaced extension values without changing the meaning of core fields.

### Fixed fields

No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.

### Rules

This is an open map. Preserve unknown values. Reuse requires support for their declared semantics; an empty map does not prove that the source had no hidden settings.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "example.annotation/1": {
    "label": "reviewed"
  }
}
```

<a id="message-data-object"></a>

## Message Data Object

A conversation message whose role is separate from the event actor's identity.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="message-data-object-role"></a>`role` | enum | Yes | Message role used for this input, independently of participant identity. One of `"user"`, `"assistant"`, `"system"`, `"developer"`, `"tool"`, `"unknown"`. |
| <a id="message-data-object-parts"></a>`parts` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content parts. Order is semantically significant. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "role": "user",
  "parts": [
    {
      "kind": "text",
      "text": "Summarize the selected meeting notes."
    }
  ]
}
```

<a id="tool-call-data-object"></a>

## Tool Call Data Object

One logical invocation and its known arguments. Partial arguments cannot be executed as a completed call.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="tool-call-data-object-call_id"></a>`call_id` | string | Yes | Session-scoped identity of one logical invocation. Minimum length: `1`. |
| <a id="tool-call-data-object-tool_id"></a>`tool_id` | string | Yes | ID of the referenced tool definition. Minimum length: `1`. |
| <a id="tool-call-data-object-arguments"></a>`arguments` | JSON value | Yes | Exact known JSON argument value; completeness is declared separately. |
| <a id="tool-call-data-object-arguments_status"></a>`arguments_status` | enum | Yes | Whether the known arguments are complete, partial or unknown. One of `"complete"`, `"partial"`, `"unknown"`. |
| <a id="tool-call-data-object-retry_of"></a>`retry_of` | string | No | ID of an earlier invocation being retried; the retry has a new call ID. Minimum length: `1`. |

### Rules

See [tool-call progression rules](../SEMANTICS.md#tool-call-progression-across-captures). A partial or unknown invocation can gain arguments through a new event with local `supersedes`, retaining its call/tool/actor/execution/retry identity. Completed calls cannot be amended through this mechanism; retries use a new call ID. Selected histories must choose a single amendment chain. These are inter-event semantic checks beyond JSON Schema.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "call_id": "call-1",
  "tool_id": "summarize",
  "arguments": {
    "resource_id": "source-csv"
  },
  "arguments_status": "complete"
}
```

<a id="tool-result-data-object"></a>

## Tool Result Data Object

One indexed result for a correlated call, including its terminal marker and outcome.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="tool-result-data-object-call_id"></a>`call_id` | string | Yes | Session-scoped identity of one logical invocation. Minimum length: `1`. |
| <a id="tool-result-data-object-result_index"></a>`result_index` | integer | Yes | Monotonically increasing result position within the call's selected history. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="tool-result-data-object-terminal"></a>`terminal` | boolean | Yes | Whether this is the final result or fragment in its declared scope. |
| <a id="tool-result-data-object-outcome"></a>`outcome` | enum | Yes | Recorded result or assessment outcome; unknown remains explicit. One of `"success"`, `"error"`, `"cancelled"`, `"unknown"`. |
| <a id="tool-result-data-object-parts"></a>`parts` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content parts. Order is semantically significant. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

- When `terminal` is `false`, `outcome` MUST be `"unknown"`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "call_id": "call-1",
  "result_index": 0,
  "terminal": true,
  "outcome": "success",
  "parts": [
    {
      "kind": "resource",
      "resource_id": "output-csv",
      "description": "CSV with total row."
    },
    {
      "kind": "resource",
      "resource_id": "report",
      "description": "Markdown report."
    }
  ]
}
```

<a id="decision-request-data-object"></a>

## Decision Request Data Object

A question, approval or review request, optionally bound to a call or an exact task revision.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="decision-request-data-object-request_id"></a>`request_id` | string | Yes | Session-scoped identity of the exact decision request. Minimum length: `1`. |
| <a id="decision-request-data-object-decision_kind"></a>`decision_kind` | enum | Yes | Whether this request is an approval, question or plan review. One of `"approval"`, `"question"`, `"plan_review"`. |
| <a id="decision-request-data-object-prompt"></a>`prompt` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content presented for the decision. |
| <a id="decision-request-data-object-options"></a>`options` | array of [Decision Request Option Object](objects.md#decision-request-option-object) | Yes | Selectable options, with stable IDs within this request. |
| <a id="decision-request-data-object-call_id"></a>`call_id` | string | No | Session-scoped identity of one logical invocation. Minimum length: `1`. |
| <a id="decision-request-data-object-task_id"></a>`task_id` | string | No | Identity of the versioned task. Minimum length: `1`. |
| <a id="decision-request-data-object-task_revision"></a>`task_revision` | integer | No | Exact task revision to which the request applies. Minimum: `0`. Maximum: `9007199254740991`. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

- When `task_id` is present, `task_revision` MUST also be present.
- When `task_revision` is present, `task_id` MUST also be present.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "request_id": "approval-1",
  "decision_kind": "approval",
  "prompt": [
    {
      "kind": "text",
      "text": "Allow access to meeting-42?"
    }
  ],
  "options": [
    {
      "id": "allow",
      "label": "Allow"
    },
    {
      "id": "deny",
      "label": "Deny"
    }
  ],
  "call_id": "call-1"
}
```

<a id="decision-request-option-object"></a>

## Decision Request Option Object

A selectable answer with a stable ID within its decision request.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="decision-request-option-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="decision-request-option-object-label"></a>`label` | string | Yes | Human-readable option label. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "deny",
  "label": "Deny"
}
```

<a id="decision-resolution-data-object"></a>

## Decision Resolution Data Object

Records the outcome of the exact referenced request. Historical approval does not authorize a receiving runtime.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="decision-resolution-data-object-request_id"></a>`request_id` | string | Yes | Session-scoped identity of the exact decision request. Minimum length: `1`. |
| <a id="decision-resolution-data-object-outcome"></a>`outcome` | enum | Yes | Recorded result or assessment outcome; unknown remains explicit. One of `"allowed"`, `"denied"`, `"answered"`, `"cancelled"`, `"expired"`, `"unknown"`. |
| <a id="decision-resolution-data-object-answer"></a>`answer` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Recorded answer content, which may be empty for non-text outcomes. |
| <a id="decision-resolution-data-object-selected_option_id"></a>`selected_option_id` | string | No | ID of the exact selected option in the referenced request. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "request_id": "question-1",
  "outcome": "answered",
  "answer": [
    {
      "kind": "text",
      "text": "Use the attached CSV."
    }
  ]
}
```

<a id="task-update-data-object"></a>

## Task Update Data Object

A versioned task state, with optional predecessor and dependency declarations.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="task-update-data-object-task_id"></a>`task_id` | string | Yes | Identity of the versioned task. Minimum length: `1`. |
| <a id="task-update-data-object-revision"></a>`revision` | integer | Yes | Versioned definition or task revision within its identity. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="task-update-data-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"proposed"`, `"pending"`, `"in_progress"`, `"completed"`, `"failed"`, `"cancelled"`, `"superseded"`, `"unknown"`. |
| <a id="task-update-data-object-parts"></a>`parts` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content parts. Order is semantically significant. |
| <a id="task-update-data-object-previous_revision"></a>`previous_revision` | integer | No | Earlier selected revision of this task. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="task-update-data-object-dependencies"></a>`dependencies` | array of string | No | Declared dependencies; interpretation is determined by the enclosing object. Items MUST be unique. |
| <a id="task-update-data-object-reopen_reason"></a>`reopen_reason` | string | No | Required nonempty explanation when reopening a completed, failed or cancelled task as pending or in progress. Minimum length: `1`. |

### Rules

See [selected-history state transitions](../SEMANTICS.md#15-selected-history-state-transitions). Revisions increase and name their selected predecessor. Reopening a terminal task as pending or in progress requires `reopen_reason`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "task_id": "task-1",
  "revision": 1,
  "status": "pending",
  "parts": [
    {
      "kind": "text",
      "text": "Summarize the attached report."
    }
  ]
}
```

<a id="context-checkpoint-data-object"></a>

## Context Checkpoint Data Object

Records the selection or replacement of a context, including a compaction boundary.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="context-checkpoint-data-object-context_id"></a>`context_id` | string | Yes | ID of the selected Context Object. Minimum length: `1`. |
| <a id="context-checkpoint-data-object-reason"></a>`reason` | enum | Yes | Reason for the recorded operation or unavailable interpretation. One of `"initial"`, `"request"`, `"compaction"`, `"manual"`, `"unknown"`. |
| <a id="context-checkpoint-data-object-replaced_context_id"></a>`replaced_context_id` | string | No | ID of the context replaced by this checkpoint or compaction. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "context_id": "compacted",
  "reason": "compaction",
  "replaced_context_id": "before"
}
```

<a id="configuration-change-data-object"></a>

## Configuration Change Data Object

Records a new configuration snapshot; effective use is determined by referencing contexts and executions.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="configuration-change-data-object-configuration_id"></a>`configuration_id` | string | Yes | ID of the configuration snapshot used at this boundary. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "configuration_id": "configuration-1"
}
```

<a id="execution-transition-data-object"></a>

## Execution Transition Data Object

Records an observed execution lifecycle transition without claiming a process is still alive.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="execution-transition-data-object-execution_id"></a>`execution_id` | string | Yes | ID of the associated execution. Minimum length: `1`. |
| <a id="execution-transition-data-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"running"`, `"completed"`, `"failed"`, `"cancelled"`, `"interrupted"`, `"unknown"`. |
| <a id="execution-transition-data-object-error"></a>`error` | JSON value | No | Captured error evidence; its contents do not establish a recovery action. |
| <a id="execution-transition-data-object-parts"></a>`parts` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | No | Ordered content parts. Order is semantically significant. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "execution_id": "execution-1",
  "status": "completed",
  "parts": [
    {
      "kind": "text",
      "text": "The response was recorded."
    }
  ]
}
```

<a id="resource-change-data-object"></a>

## Resource Change Data Object

Records creation, modification, deletion or observation of a resource identity.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="resource-change-data-object-resource_id"></a>`resource_id` | string | Yes | ID of the referenced Resource Object. Minimum length: `1`. |
| <a id="resource-change-data-object-operation"></a>`operation` | enum | Yes | Kind of resource change recorded by the event. One of `"created"`, `"modified"`, `"deleted"`, `"observed"`. |
| <a id="resource-change-data-object-previous_resource_id"></a>`previous_resource_id` | string | No | ID of the prior immutable resource version. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "resource_id": "resource-1",
  "operation": "created"
}
```

<a id="note-data-object"></a>

## Note Data Object

Explanatory content with no implicit execution or authorization meaning.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="note-data-object-parts"></a>`parts` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content parts. Order is semantically significant. |
| <a id="note-data-object-category"></a>`category` | string | Yes | Names the explanatory note category. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "category": "redaction",
  "parts": [
    {
      "kind": "text",
      "text": "A sanitized replacement is supplied."
    },
    {
      "kind": "resource",
      "resource_id": "sanitized",
      "description": "Distinct replacement resource."
    }
  ]
}
```

<a id="extension-data-object"></a>

## Extension Data Object

An event with namespaced semantics; required interpretation is also advertised in `required_features`.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="extension-data-object-type"></a>`type` | string | Yes | Namespaced semantic type or entity type, as defined by the enclosing object. Minimum length: `1`. |
| <a id="extension-data-object-value"></a>`value` | JSON value | Yes | Value interpreted according to the enclosing schema, dialect or counter. |
| <a id="extension-data-object-interpretation_required"></a>`interpretation_required` | boolean | Yes | Whether understanding this event is required; its feature must also be declared. |

### Rules

See [normative session rules](../SEMANTICS.md#6-core-event-meanings).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "type": "example.annotation/1",
  "value": {
    "label": "reviewed"
  },
  "interpretation_required": false
}
```

<a id="coverage-object"></a>

## Coverage Object

Declares the completeness or known absence of one session domain. An empty collection alone makes no completeness claim.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="coverage-object-scope"></a>`scope` | enum | Yes | Domain or activation scope to which this declaration applies. One of `"participants"`, `"conversation"`, `"branches"`, `"executions"`, `"contexts"`, `"configuration"`, `"tools"`, `"decisions"`, `"tasks"`, `"resources"`, `"environment"`, `"native"`, `"usage"`. |
| <a id="coverage-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"complete"`, `"partial"`, `"known_empty"`, `"unavailable"`, `"excluded"`, `"not_inspected"`, `"not_applicable"`. |
| <a id="coverage-object-detail"></a>`detail` | string | Yes | Explanation of the stated status or evidence. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#12-coverage-losses-and-unknown-extensions).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "scope": "resources",
  "status": "complete",
  "detail": "All modeled input resources included."
}
```

<a id="loss-object"></a>

## Loss Object

Discloses information omitted or changed during capture, normalization, redaction or translation.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="loss-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="loss-object-stage"></a>`stage` | enum | Yes | Transformation stage; in a Git index entry, the conflict stage number. One of `"capture"`, `"normalization"`, `"redaction"`, `"translation"`. |
| <a id="loss-object-kind"></a>`kind` | string | Yes | Discriminator selecting this object's interpretation. Minimum length: `1`. |
| <a id="loss-object-scope"></a>`scope` | enum | No | Domain or activation scope to which this declaration applies. One of `"participants"`, `"conversation"`, `"branches"`, `"executions"`, `"contexts"`, `"configuration"`, `"tools"`, `"decisions"`, `"tasks"`, `"resources"`, `"environment"`, `"native"`, `"usage"`. |
| <a id="loss-object-references"></a>`references` | array of [Loss References Object](objects.md#loss-references-object) | No | Typed identities affected by this loss. |
| <a id="loss-object-explanation"></a>`explanation` | string | Yes | Reason for the declaration or limitation. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#12-coverage-losses-and-unknown-extensions).

- Supply at least one of: `scope`, `references`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "context-compaction",
  "stage": "normalization",
  "kind": "summarization",
  "scope": "contexts",
  "explanation": "The compacted input loses original detail; history and original attachment remain preserved."
}
```

<a id="loss-references-object"></a>

## Loss References Object

Identifies an entity affected by a loss using its entity type and ID.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="loss-references-object-type"></a>`type` | string | Yes | Namespaced semantic type or entity type, as defined by the enclosing object. Minimum length: `1`. |
| <a id="loss-references-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |

### Rules

See [normative session rules](../SEMANTICS.md#12-coverage-losses-and-unknown-extensions).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "type": "resource",
  "id": "missing"
}
```

<a id="stream-segment-object"></a>

## Stream Segment Object

Selects an exact byte slice of a captured resource and its position in a logical stream.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="stream-segment-object-index"></a>`index` | integer | Yes | Zero-based fragment position within its stream. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="stream-segment-object-resource_id"></a>`resource_id` | string | Yes | ID of the referenced Resource Object. Minimum length: `1`. |
| <a id="stream-segment-object-offset"></a>`offset` | integer | Yes | Zero-based byte offset into the referenced resource. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="stream-segment-object-length"></a>`length` | integer | Yes | Number of bytes in the selected span. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="stream-segment-object-terminal"></a>`terminal` | boolean | Yes | Whether this is the final result or fragment in its declared scope. |

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "index": 0,
  "resource_id": "argument-fragment",
  "offset": 0,
  "length": 19,
  "terminal": true
}
```

<a id="stream-object"></a>

## Stream Object

Binds incremental argument or text-result bytes to a core event. A complete stream must agree with that event's assembled value.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="stream-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="stream-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"tool_arguments"`, `"tool_result_text"`. |
| <a id="stream-object-event_id"></a>`event_id` | string | Yes | Event identity, resolved locally unless an external capture is explicit. Minimum length: `1`. |
| <a id="stream-object-call_id"></a>`call_id` | string | Yes | Session-scoped identity of one logical invocation. Minimum length: `1`. |
| <a id="stream-object-result_index"></a>`result_index` | integer | No | Monotonically increasing result position within the call's selected history. Minimum: `0`. Maximum: `9007199254740991`. |
| <a id="stream-object-status"></a>`status` | enum | Yes | Recorded state at the relevant boundary; see the allowed values. One of `"partial"`, `"complete"`. |
| <a id="stream-object-segments"></a>`segments` | array of [Stream Segment Object](objects.md#stream-segment-object) | Yes | Ordered byte-fragment declarations; gaps preserve partial status. |

### Rules

See [stream assembly rules](../STREAMING.md). `tool_result_text` requires `result_index`. Complete argument streams MUST decode as JSON equal to the bound call arguments; complete result streams MUST equal the bound text result.

- When `kind` is `"tool_result_text"`, require `result_index`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "stream-1",
  "kind": "tool_arguments",
  "event_id": "e-call",
  "call_id": "call-read",
  "status": "complete",
  "segments": [
    {
      "index": 0,
      "resource_id": "argument-fragment",
      "offset": 0,
      "length": 19,
      "terminal": true
    }
  ]
}
```

<a id="external-binding-object"></a>

## External Binding Object

Binds an invocation or decision request from an earlier capture to its immutable source boundary and descriptor.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="external-binding-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"call"`, `"request"`. |
| <a id="external-binding-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="external-binding-object-source"></a>`source` | [External Binding Source Object](objects.md#external-binding-source-object) | Yes | Source identity and boundary or report binding. |
| <a id="external-binding-object-descriptor"></a>`descriptor` | [External Binding Descriptor Object](objects.md#external-binding-descriptor-object) | Yes | Call or request declaration selected by the binding kind. |

### Rules

See [external binding rules](../STREAMING.md#external-bindings). `call` selects the External Call Descriptor; `request` selects the External Request Descriptor. Bindings do not synthesize events or authorize replay.

- When `kind` is `"call"`, `descriptor` requires `tool_id`, `arguments`, `arguments_status`.
- When `kind` is `"request"`, `descriptor` requires `decision_kind`, `prompt`, `options`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "call",
  "id": "call-previous",
  "source": {
    "session_id": "session-parent",
    "capture_id": "capture-parent",
    "event_id": "e2"
  },
  "descriptor": {
    "tool_id": "tool-read",
    "arguments": {
      "path": "notes.md"
    },
    "arguments_status": "complete"
  }
}
```

### External decision request

A later capture may contain the answer without including the original request event.

```json
{
  "kind": "request",
  "id": "question-earlier",
  "source": {
    "session_id": "session-1",
    "capture_id": "capture-earlier",
    "event_id": "e-question"
  },
  "descriptor": {
    "decision_kind": "question",
    "prompt": [
      {
        "kind": "text",
        "text": "Which report should I summarize?"
      }
    ],
    "options": [
      {
        "id": "annual",
        "label": "Annual report"
      }
    ]
  }
}
```

<a id="external-binding-source-object"></a>

## External Binding Source Object

Names the exact source event of an external call or request; no external data is fetched implicitly.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="external-binding-source-object-session_id"></a>`session_id` | string | Yes | Logical session ID of the referenced boundary. Minimum length: `1`. |
| <a id="external-binding-source-object-capture_id"></a>`capture_id` | string | Yes | Immutable capture ID of the referenced boundary. Minimum length: `1`. |
| <a id="external-binding-source-object-event_id"></a>`event_id` | string | Yes | Event identity, resolved locally unless an external capture is explicit. Minimum length: `1`. |

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "event_id": "e2",
  "session_id": "session-parent",
  "capture_id": "capture-parent"
}
```

<a id="external-binding-descriptor-object"></a>

## External Binding Descriptor Object

Discriminated descriptor selected by the enclosing external binding's `kind`.

### Fixed fields

No fixed fields. This object retains fields defined by its declared dialect or enclosing discriminator.

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "tool_id": "tool-read",
  "arguments": {
    "path": "notes.md"
  },
  "arguments_status": "complete"
}
```

<a id="external-call-descriptor-object"></a>

## External Call Descriptor Object

Preserves the tool and argument contract of an invocation outside the included event history.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="external-call-descriptor-object-tool_id"></a>`tool_id` | string | Yes | ID of the referenced tool definition. Minimum length: `1`. |
| <a id="external-call-descriptor-object-arguments"></a>`arguments` | JSON value | Yes | Exact known JSON argument value; completeness is declared separately. |
| <a id="external-call-descriptor-object-arguments_status"></a>`arguments_status` | enum | Yes | Whether the known arguments are complete, partial or unknown. One of `"complete"`, `"partial"`, `"unknown"`. |

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "tool_id": "tool-read",
  "arguments": {
    "path": "notes.md"
  },
  "arguments_status": "complete"
}
```

<a id="external-request-descriptor-object"></a>

## External Request Descriptor Object

Preserves the kind, prompt and options of a decision request outside the included event history.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="external-request-descriptor-object-decision_kind"></a>`decision_kind` | enum | Yes | Whether this request is an approval, question or plan review. One of `"approval"`, `"question"`, `"plan_review"`. |
| <a id="external-request-descriptor-object-prompt"></a>`prompt` | array of [Text Part Object](objects.md#text-part-object) / [Resource Part Object](objects.md#resource-part-object) / [Structured Part Object](objects.md#structured-part-object) / [Opaque Part Object](objects.md#opaque-part-object) | Yes | Ordered content presented for the decision. |
| <a id="external-request-descriptor-object-options"></a>`options` | array of [External Request Option Object](objects.md#external-request-option-object) | Yes | Selectable options, with stable IDs within this request. |

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "decision_kind": "approval",
  "prompt": [],
  "options": []
}
```

<a id="external-request-option-object"></a>

## External Request Option Object

One selectable option of an externally bound decision request.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="external-request-option-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="external-request-option-object-label"></a>`label` | string | Yes | Human-readable option label. |

### Rules

See [session semantics](../SEMANTICS.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "deny",
  "label": "Deny"
}
```
