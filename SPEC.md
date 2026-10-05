# Agent Session Interchange Format

**ASIF 0.3 — 26 September 2026**  
Status: proposed standard; not a released or independently validated standard.

## Introduction

ASIF defines a vendor-neutral document describing an agent session: who participated, what happened, what context was supplied, what resources were used, and what state remains known or unresolved. It supports exchange between implementations without assuming a particular agent, application, computer, execution location or transfer mechanism.

The specification separates three capabilities:

| Capability | Meaning |
|---|---|
| Interchange | Preserve identities, relationships, content and declared limitations during import and export. |
| Interoperability | Interpret supported records using the same semantics. |
| Continuation | Construct a usable next interaction from a specified checkpoint after resolving destination prerequisites. |

A session can be useful for interchange without being ready for continuation. Identical future model output is not guaranteed.

## How to read this specification

The reference is organized by named objects. Each object has a purpose, a fixed-field table, unconditional and conditional requirements, semantic rules, and a JSON example. Field types link to their object definitions. The object reference and semantic rules together define ASIF; examples are informative.

| Document | Contents |
|---|---|
| [Core object reference](docs/objects.md) | The ASIF document and every core, nested and event-data object. |
| [Session semantics](SEMANTICS.md) | Identity, ordering, branches, context, state, resources, coverage and preservation rules. |
| [Continuation object reference](docs/continuation-objects.md) | Optional workspace, dependency, configuration, service, recovery and plan objects. |
| [Continuation semantics](CONTINUATION.md) | Rules for selecting and assessing a continuation boundary. |
| [Destination report reference](docs/report-objects.md) | Assessment, evidence, transformation and result objects. |
| [Destination capability snapshots](CAPABILITIES.md) | Supplied destination state, exact-byte fingerprints, component bindings and report reuse. |
| [Streaming and external bindings](STREAMING.md) | Optional fragment assembly and earlier-capture invocation/request bindings. |
| [Package transport](TRANSPORT.md) | Optional exact-byte envelope, integrity inventory and detached signature convention. |
| [Profiles](PROFILES.md) | Core requirements versus optional capabilities. |
| [Worked examples](examples/README.md) | Complete sessions with images, documents, audio, generated files, unavailable content and compaction. |

## Terminology and requirement levels

A **session** is a persistent, identifiable interaction among people, agents and tools. A **capture** is an immutable observation of that session. An **event** records an occurrence. A **branch** selects conversation history. A **context** records or proposes actual model input. A **checkpoint** records state at a branch boundary. A **resource** describes content used by, produced by or needed to interpret the session.

`MUST`, `MUST NOT`, `SHOULD` and `MAY` indicate requirements of this draft. “Required” in a field table means the field is always present in that object. Conditional requirements are stated separately. Optional fields do not imply optional interpretation when a declared feature requires them.

## Document format and data types

An ASIF document is UTF-8 JSON. Object field names and IDs are case-sensitive. Duplicate object keys and non-JSON numeric constants are invalid. JSON member order has no semantic meaning; array order has the meaning specified for that field. A field may be null only where its type permits null. Absence, null, an empty collection and unknown state are distinct.

| Type | Meaning |
|---|---|
| `string` | JSON Unicode string; additional field-specific constraints apply. |
| `integer` | Integral JSON number. Core positions, lengths and revisions are nonnegative and at most 9,007,199,254,740,991 where the schema specifies that bound. |
| `number` | JSON number; consumers MUST NOT silently round preserved values. |
| `boolean` | JSON `true` or `false`. |
| `array of T` | Ordered collection of the specified values; uniqueness is field-specific. |
| `object` | Object with the linked fixed fields and permitted additional properties. |
| `JSON value` | Any JSON value; a declared schema or dialect can impose further requirements. |
| `enum` | One of the explicitly listed values; unknown values are not silently mapped. |

ASIF 0.3 defines JSON serialization. Other syntaxes require a separately specified mapping. Schema `$ref` links describe the specification's types; instance references use typed IDs rather than arbitrary JSON Schema references.

## Specification objects

The root [ASIF Document Object](docs/objects.md#asif-document-object) contains the following domains. Every core collection is present, even when empty. [Coverage](docs/objects.md#coverage-object) distinguishes known absence from uninspected or unavailable information.

| Domain | Objects |
|---|---|
| Identity | [Capture](docs/objects.md#capture-object), [Session](docs/objects.md#session-object), [Participant](docs/objects.md#participant-object), [Event Reference](docs/objects.md#event-reference-object) |
| Recorded history | [Event](docs/objects.md#event-object), [Branch](docs/objects.md#branch-object), [Execution](docs/objects.md#execution-object) |
| Content | [Text Part](docs/objects.md#text-part-object), [Resource Part](docs/objects.md#resource-part-object), [Structured Part](docs/objects.md#structured-part-object), [Opaque Part](docs/objects.md#opaque-part-object) |
| Model input | [Context](docs/objects.md#context-object), [Context Input](docs/objects.md#context-input-object) |
| Configuration | [Configuration](docs/objects.md#configuration-object), [Instruction](docs/objects.md#instruction-object), [Capability](docs/objects.md#capability-object), [Policy](docs/objects.md#policy-object) |
| Tool activity | [Tool](docs/objects.md#tool-object), [Tool Call Data](docs/objects.md#tool-call-data-object), [Tool Result Data](docs/objects.md#tool-result-data-object) |
| Decisions and tasks | [Decision Request Data](docs/objects.md#decision-request-data-object), [Decision Resolution Data](docs/objects.md#decision-resolution-data-object), [Task Update Data](docs/objects.md#task-update-data-object) |
| State and dependencies | [Checkpoint](docs/objects.md#checkpoint-object), [Environment](docs/objects.md#environment-object), [Requirement](docs/objects.md#requirement-object) |
| Evidence and completeness | [Resource](docs/objects.md#resource-object), [Provenance](docs/objects.md#provenance-object), [Coverage](docs/objects.md#coverage-object), [Loss](docs/objects.md#loss-object), [Usage](docs/objects.md#usage-object) |

All twelve event kinds have their own data-object definition and example in the [core reference](docs/objects.md#event-object).

## References, content and attachments

IDs are opaque and unique within their declared collection or scope. Local references MUST resolve. External event boundaries MUST name their source session and capture. Reading a reference never implies fetching, executing or authorizing anything.

Attachments use the same Resource Object as other content. A message or context includes a Resource Part at the intended position. The resource declares media type, purpose and availability. Embedded resources carry exact decoded length and SHA-256 plus exactly one representation: UTF-8 `text`, base64 `data`, or a relative `path`. External, unavailable, excluded, redacted and unknown resources retain explicit declarations rather than invented content.

See the [resource definition](docs/objects.md#resource-object), [multimodal session example](examples/image-and-document.session.json), [attachment availability example](examples/attachment-availability.session.json) and [redaction example](examples/redacted-attachment.session.json).

## Profiles and extensions

Optional semantic features are identified in `required_features`. A consumer that cannot interpret a required feature MUST report that limitation and MUST NOT claim the affected interoperability or continuation capability. Unknown optional properties are preserved without acquiring implicit meaning.

| Feature | Data and rules |
|---|---|
| `asif.portable-continuation/0.1` | Root `continuation`; [profile rules](CONTINUATION.md) and [objects](docs/continuation-objects.md). |
| `asif.streams/0.1` | Root `streams`; [assembly rules](STREAMING.md) and [Stream Object](docs/objects.md#stream-object). |
| `asif.external-bindings/0.1` | Root `external_bindings`; [binding rules](STREAMING.md#external-bindings) and [External Binding Object](docs/objects.md#external-binding-object). |

The presence of any of these fields requires its feature identifier, and declaring the feature requires its field. Namespace-specific extension events and dialects must disclose whether interpretation is required. They MUST NOT override core meanings.

## Validation and conformance

Validation has separate layers: JSON structure, entity references and semantic rules, resource integrity, supported feature interpretation, and capability-specific evidence. Passing JSON Schema alone does not establish conformance.

The machine-readable schemas are [session](schemas/session.schema.json), [continuation](schemas/continuation.schema.json), and [destination report](schemas/continuation-report.schema.json). Object examples are checked against these schemas by [the documentation check](tests/check_documentation.py). The [reference tools](REFERENCE.md) implement a documented subset of semantics and local operations.

The [conformance plan](CONFORMANCE.md), [implementation record](IMPLEMENTERS.md) and [remaining gaps](GAPS.md) state the limits of current evidence. Synthetic destination reports cannot authorize execution or establish real import success.

## Versioning and specification maintenance

This draft uses an exact `asif_version`. Profile and report versions are explicit and independently named. There is no implied compatibility with a different draft. Changes to required meaning require review of schemas, semantic rules, object examples and conformance fixtures together.

The current proposal and advancement criteria are in [governance](GOVERNANCE.md). Before claiming a released interoperable standard, ASIF needs independently authored implementations and actual exchange evidence.

## License

This specification and its accompanying schemas, examples and reference implementations are available under the [MIT license](LICENSE). Third-party material retains its own [notices](THIRD-PARTY-NOTICES.md).
