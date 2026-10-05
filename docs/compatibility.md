# Compatibility and evidence

ASIF **0.5** is a proposal with two locally authored reference implementations. This page separates executable checks, authored scenarios and integration work. It is not a list of certified providers. Both reference implementations share authorship; independent exchange evidence remains **zero**.

## Capability matrix

| Capability | Python reference | TypeScript reference | Evidence and limits |
|---|---|---|---|
| Parse and validate ASIF sessions | Implemented subset | Implemented subset | Structure and selected semantic invariants; [Python results](../tests/reference-results.json), [TypeScript results](../tests/typescript-results.json). Full semantic coverage remains open. |
| Project a selected request context | Implemented | Implemented | Ordered typed inputs, resource references, tools and settings; no provider encoding or measured token budget. |
| Exchange packages and signatures | Locally checked | Locally checked | [Bidirectional local checks](../tests/typescript-exchange-results.json); shared authorship, no independent interoperability claim. |
| Restore selected plain file trees | Implemented subset | Implemented subset | Fresh destination only; Git administration, symlinks and native stores are unsupported. |
| Assess continuation declarations | Implemented subset | Implemented subset | [Synthetic reports](../examples/continuation/README.md); no live capability, credential or account verification. |
| Represent agents with different roles | Synthetic fixture checked | Synthetic fixture checked | [Shared-brief example](../examples/README.md#agents-with-different-roles); no real providers or live coordination. |
| Export real native agent sessions | Not implemented | Not implemented | Requires a source adapter and stable identity mappings. |
| Import into a native agent and continue | Not implemented | Not implemented | Requires a destination adapter, authorization and observed next-interaction evidence. |
| Independent session exchange | Not demonstrated | Not demonstrated | Requires independently authored implementations and independently produced sessions. |

The [reference guide](../REFERENCE.md#typescript-differences-and-compatibility-evidence) describes numeric, archive and path-pattern differences. Successful validation establishes only the stated check scope.

## What a provider support claim needs

A named provider or runtime belongs in a compatibility report only after an implementer supplies reproducible evidence. Record source and destination versions, adapter revision, ASIF/profile versions, transferred fields, unsupported state and results for each direction. A successful export does not establish import or continuation support.

An adapter can start with a narrow claim such as readable conversation and resource export. If effective model inputs are unknown, label their fidelity accordingly. Expand the claim as additional capabilities are demonstrated. Use the [adapter guide](adapters.md) and [implementation evidence record](../IMPLEMENTERS.md).

## Next evidence milestones

1. Export a real source session with a documented mapping and a sanitized, reproducible fixture.
2. Assess it for a named destination; make supported, adapted and blocked subjects explicit.
3. Demonstrate an authorized next interaction and export its results back with stable identities and recorded losses.
4. Have an independently authored implementation repeat the exchange with its own source session.

These are desired evidence milestones, not scheduled releases or completed work. [GAPS.md](../GAPS.md) tracks outstanding implementation and release requirements; [governance](../GOVERNANCE.md#maturity-levels) defines proposed maturity gates.
