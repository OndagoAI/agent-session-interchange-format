# Contributing to ASIF

Help test whether a session record contains enough information for another person, agent or runtime to understand the work and assess a handoff. Contributions can begin with a concrete use case, a small fixture or an implementation experiment.

Start with the [current compatibility matrix](docs/compatibility.md). The format is a proposal and the local tools cover a subset. A contribution should state which capability it improves and how someone else can check it.

## Share a use case

Open a [GitHub issue](https://github.com/OndagoAI/agent-session-interchange-format/issues/new) with:

- The source and destination, including relevant versions.
- The next task the recipient should be able to perform.
- Information that needs to survive: selected inputs, files, decisions, instructions, tools or unresolved operations.
- A minimal sanitized example and the expected interpretation.
- What is missing or ambiguous in the current format or implementation.

Use invented data if a source record cannot be shared, and label it synthetic. Do not include credentials or private transcripts in a public issue.

## Choose a starting contribution

| Contribution | A reviewable result |
|---|---|
| Clarify a confusing field | A concrete ambiguity, proposed wording and the affected object links |
| Improve semantic coverage | A named normative requirement, a positive fixture and a rejection case where applicable |
| Document an adapter mapping | A source field mapped to ASIF, with identity, coverage and loss handling explained |
| Test an unfamiliar session type | A small non-coding or multi-agent example with honest context fidelity |
| Supply independent evidence | A versioned implementation report with commands, input digests and supported/unsupported outcomes |

These are suggestions for small contributions, not assigned issues or claims that maintainers have accepted a design. Check [existing issues](https://github.com/OndagoAI/agent-session-interchange-format/issues) and the [gap list](GAPS.md) before proposing larger changes.

## Work on an adapter

Follow the [adapter-development guide](docs/adapters.md). Begin with an explicit source mapping and a narrow capability claim. Publish preservation limits before attempting native import or continuation.

The most useful integration evidence is a real session exported, assessed at a destination, continued under that destination's authorization and exported again. The [handoff evidence checklist](docs/adapters.md#the-first-live-handoff) describes what to retain. A local port of the reference implementation does not by itself establish independent interoperability.

## Prepare a pull request

Explain the problem, resulting behavior and affected ASIF/profile versions. Include reproducible commands and distinguish passed, failed and unsupported cases. For semantic changes, identify schema, documentation and fixture changes together.

Follow [getting started](docs/getting-started.md) to install the reference tools. Use checks relevant to the change:

```sh
# Python examples and reference implementation
.venv/bin/python tests/check_examples.py
.venv/bin/python tests/check_reference.py

# TypeScript implementation
npm run typecheck
npm test

# Documentation (requires requirements-docs.txt)
.venv/bin/python tests/check_documentation.py
.venv/bin/python -m mkdocs build --strict
```

Schema/profile changes also need the [structural and continuation checks](REFERENCE.md#reproducing-evidence-and-documentation). Regenerate object pages from their schemas and authored metadata with `docs/build_reference.py`; do not edit generated tables directly. Refresh the shared TypeScript parity corpus when continuation expectations change.

Keep discussion focused on reproducible behavior and treat contributors respectfully. The repository uses the [MIT license](LICENSE); the proposed [governance process](GOVERNANCE.md) and remaining contribution/release terms are documented separately. This guide does not establish a governing body or independent review roster.

## Open to independent implementations

ASIF began with the team behind Ondago. Implementers can use the format in their own applications, including competing products, without an Ondago account or runtime. Record actual implementation authorship and affiliation in [IMPLEMENTERS.md](IMPLEMENTERS.md) when submitting evidence; do not infer endorsements or independence from a project name.
