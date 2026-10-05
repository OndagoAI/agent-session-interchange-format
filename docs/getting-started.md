# Getting started

ASIF describes an agent session as a portable JSON document. Start by validating a worked example, then explore the records behind it. Version **0.4** is a proposal with local reference implementations; a valid document does not establish that an agent can continue it.

## Choose a reading path

| Goal | Start with |
|---|---|
| See what ASIF is for | [Benefits and use cases](use-cases.md) |
| Check demonstrated support | [Compatibility and evidence](compatibility.md) |
| Understand the format | [Specification](../SPEC.md) and [session semantics](../SEMANTICS.md) |
| Find a field or object | [Core object reference](objects.md) and [JSON schemas](schemas.md) |
| Run local checks | [Reference CLI installation and commands](../REFERENCE.md) |
| Build an adapter | [Adapter guide](adapters.md), [field mapping](field-mapping.md) and [conformance cases](../CONFORMANCE.md) |
| Understand continuation | [Portable-continuation profile](../CONTINUATION.md) and [worked scenarios](../examples/continuation/README.md) |
| Help close the remaining gaps | [Gaps and priorities](../GAPS.md) |
| Share a use case or contribute | [Contribution guide](../CONTRIBUTING.md) |

## Run a first validation

Clone the repository and enter its directory:

```sh
git clone https://github.com/OndagoAI/agent-session-interchange-format.git
cd agent-session-interchange-format
```

With **Node.js 24 or newer**:

```sh
npm ci
node asif.ts validate examples/image-and-document.session.json
```

Or with **Python 3.11 or newer**:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python asif.py validate examples/image-and-document.session.json
```

The command reports JSON results for the reference implementation's supported checks. Exit `0` means those checks passed; invalid input uses exit `2`, and unsupported semantics use exit `3`. See the [shared command contract](../REFERENCE.md#shared-command-contract) for details.

Open the [image and document session](../examples/image-and-document.session.json) alongside the [worked examples guide](../examples/README.md). Look at `events` for recorded occurrences, `branches` for selected history, and `contexts` for ordered model inputs. These collections serve different purposes and must remain distinct.

## Explore a continuation plan

The another-computer scenario includes a checkpoint, configuration, workspace snapshot and synthetic destination report. Inspect its neutral request projection:

```sh
node asif.ts request examples/continuation/another-computer.session.json continue-context
```

For Python, replace `node asif.ts` with `.venv/bin/python asif.py`. The projection preserves the selected typed inputs, tools and settings. It is not a provider request and does not run an agent.

Read the [continuation scenarios](../examples/continuation/README.md) for the matching reports and limitations. Runtime identity, credentials, native import and actual next-interaction evidence remain separate requirements.

## Check changes

For specification and object-reference edits, run the [documentation checks](site.md#validate-and-preview-locally). For implementation changes, use the [reference verification commands](../REFERENCE.md#reproducing-evidence-and-documentation) and state the supported scope in any results.
