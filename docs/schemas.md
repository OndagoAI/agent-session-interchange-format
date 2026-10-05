# JSON schemas

These ASIF **0.4** schemas validate document structure. Semantic requirements in the [session rules](../SEMANTICS.md) and [continuation profile](../CONTINUATION.md) also apply.

| Schema | Use | Object reference |
|---|---|---|
| [Session schema](../schemas/session.schema.json) | Complete session documents, including declared optional features | [Core objects](objects.md) |
| [Continuation schema](../schemas/continuation.schema.json) | Portable-continuation profile objects | [Continuation objects](continuation-objects.md) |
| [Destination report schema](../schemas/continuation-report.schema.json) | Destination assessments and declared outcomes | [Report objects](report-objects.md) |

The [local reference CLIs](../REFERENCE.md) combine schema validation with selected semantic checks. The [conformance plan](../CONFORMANCE.md) describes the broader acceptance requirements, and [gaps](../GAPS.md) records what remains unimplemented or unproven.

Schema downloads and [complete example documents](../examples/README.md) are published at their repository-relative paths. Example attachment bytes are preserved, including Markdown resources whose content is covered by resource digests.
