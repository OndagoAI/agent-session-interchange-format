# Agent Session Interchange Format (ASIF)

**Your agent's work should be portable across tools, computers and clouds.**

Changing environments can mean manually rebuilding the brief, finding the right files and explaining decisions an agent already made. Another agent needs those details to make a useful next step.

ASIF is a proposed open format for agent sessions. It records the conversation together with selected model inputs, instructions, files, tool results, decisions and unfinished work. The goal is to make that work portable and understandable to another implementation, so people can change environments or bring in another agent without rebuilding the session by hand.

[Documentation website](https://ondagoai.github.io/agent-session-interchange-format/) · [Try ASIF](docs/getting-started.md) · [Compatibility](docs/compatibility.md) · [Contribute](CONTRIBUTING.md) · [Specification](SPEC.md)

## Why ASIF?

### Move sessions between computers and clouds

Start a task on your laptop, move it to a cloud worker for a longer run, and bring the results back to your desktop. A useful handoff includes the working files, relevant conversation, instructions, completed tool calls and remaining tasks.

ASIF gives implementations a common way to describe that handoff: a checkpoint, the context to continue from, resource contents and the destination's prerequisites. Logical workspace roots can be mapped to new paths, and missing tools, files or access can be identified before work resumes.

The [another-computer example](examples/continuation/README.md) illustrates a macOS/ARM session assessed for a Linux/x86 destination. It includes a workspace mapping and a synthetic destination report.

### Let different agents contribute to the same session

A researcher from one provider could collect evidence, a writer from another could draft a proposal, and a reviewer could check it. Each contribution retains its author, and each execution can identify the context it received.

Agents can share the same task brief, source documents and recorded decisions while receiving instructions for different roles. Later agents can receive earlier contributions explicitly, so the review or handoff is part of the session's record.

Try the [writer, reviewer and editor example](examples/README.md#agents-with-different-roles). It models three fictional providers working on one workshop proposal, with a separate input context for each agent.

**Sharing context means sharing declared inputs.** Agents with different roles have different instructions, and later participants may see additional results. ASIF makes those differences visible. Provider adapters still need to account for model limits, tool behavior and instruction handling; shared inputs do not guarantee identical answers.

### More ways to use a portable session

| Situation | What ASIF helps preserve | Example |
|---|---|---|
| Switch agents midway through a task | Prior decisions, selected context, tool results and unresolved work, with any adaptations declared | [Another-agent handoff](examples/continuation/README.md) |
| Ask another model for a second opinion | An explicit common input and separately attributed responses; each model's actual inputs remain inspectable | [Compare approaches](docs/use-cases.md#compare-approaches-from-a-common-starting-point) |
| Hand a project to a teammate | The brief, supporting files, decisions and next steps, including gaps in the capture | [Team handoff](docs/use-cases.md#hand-work-to-a-teammate) |
| Move research or document work | Images, PDFs, audio, extracted text and their relationship to the model's inputs | [Attachment examples](examples/README.md) |
| Continue a long project after summarization | Original evidence, retained summaries and a record of what remains in active context | [Compaction example](examples/compaction-with-attachment.session.json) |
| Inspect an interrupted workflow | Known results, pending decisions and operations whose outcome still needs checking | [Unresolved remote operation](examples/continuation/README.md) |
| Keep a record that another tool can inspect | Stable identities, provenance, content digests and explicit missing or transformed data | [Archive and inspect](docs/use-cases.md#keep-an-inspectable-record-of-the-work) |

See the [use-case walkthroughs](docs/use-cases.md) for the handoff steps and what an integrating application needs to provide.

## What works today?

ASIF **0.5** is a review draft of the session data model. [Changes and migration from 0.4](MIGRATION.md) explain the compatibility boundary. This repository includes schemas, checked synthetic examples, and locally authored **Python and TypeScript CLIs** for validation, neutral request projection, selected file-tree restoration, packaging/signatures and redaction auditing.

The workflows above are integration goals. Real source/destination adapters, provider request encoding, live multi-agent coordination and independent interoperability evidence remain outstanding. ASIF describes shared session data; an application must implement agent scheduling, access control, synchronization and import. A valid session or a synthetic `ready` report does not establish that a destination can execute it. See the [compatibility and evidence matrix](docs/compatibility.md), [implementation scope](REFERENCE.md) and [remaining gaps](GAPS.md).

## Help test the handoff

If you build agents, coding tools, cloud runtimes or orchestration systems, bring a session that exposes a missing requirement. Useful contributions include a small sanitized example, a documented adapter limitation, or reproducible exchange results from an independent implementation. Start with the [contribution guide](CONTRIBUTING.md) or [adapter guide](docs/adapters.md).

The next integration milestone is a real source export, destination assessment, authorized next interaction and return export with recorded losses. It remains unproven; the [live-handoff checklist](docs/adapters.md#the-first-live-handoff) defines the evidence to collect.

The team behind Ondago started ASIF as a vendor-neutral proposal. You can implement it without an Ondago product or account. External implementers can contribute through this repository; the [governance charter](GOVERNANCE.md) remains proposed.

## Explore the format

The format distinguishes recorded events, selected branch history and actual model input. This lets a receiver understand both what happened and what information an agent used. The [specification](SPEC.md) defines these relationships and the rules for preserving them.

- [Core object reference](docs/objects.md), [continuation objects](docs/continuation-objects.md), and [destination report objects](docs/report-objects.md): fixed fields, types, requirements, semantics and checked examples.
- [Session semantics](SEMANTICS.md)
- [Python CLI](asif.py) and [TypeScript CLI](asif.ts), with [installation and command documentation](REFERENCE.md): validation, context projection, selected-tree restoration, packaging/signatures and redaction audit.
- [Package transport](TRANSPORT.md) and [streaming/external bindings](STREAMING.md).
- [Structural JSON Schema](schemas/session.schema.json)
- [Portable-continuation profile](CONTINUATION.md): checkpoints, workspace/path mappings, runtime/tool/model dependencies, configuration, authentication, operation recovery, native import and destination assessment.
- [Continuation profile schema](schemas/continuation.schema.json) and [destination report schema](schemas/continuation-report.schema.json).
- [Worked examples](examples/README.md): agents with different roles, images, PDF, audio, tool outputs, unavailable/redacted attachments, compaction, and pending approval.
- [Three continuation scenarios](examples/continuation/README.md): another computer, another agent, and an unresolved remote operation, each with a separate synthetic destination report.
- [Core versus optional profiles](PROFILES.md)
- [Remaining specification gaps](GAPS.md)
- [Conformance acceptance plan](CONFORMANCE.md)
- [Governance proposal](GOVERNANCE.md)
- [Structural check results](tests/results.json)
- [Example and attachment check results](tests/example-results.json)
- [Continuation check results](tests/continuation-results.json)

## Python quick start

With Python 3.11+, run from the project directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python asif.py validate examples/image-and-document.session.json
.venv/bin/python tests/check_schema.py
.venv/bin/python tests/check_examples.py
.venv/bin/python tests/check_continuation.py
.venv/bin/python tests/check_reference.py
.venv/bin/python tests/check_documentation.py
```

See [REFERENCE.md](REFERENCE.md#installation-and-commands) for all nine commands and their supported scope.

## TypeScript quick start

With Node.js 24+:

```sh
npm ci
node asif.ts validate examples/image-and-document.session.json
npm run typecheck
npm test
```

The TypeScript CLI supports all nine Python commands. Its supported numeric, ZIP and workspace-pattern ranges are documented in [REFERENCE.md](REFERENCE.md#typescript-differences-and-compatibility-evidence).

## License

[MIT](LICENSE), covering this project's specification, schemas, examples and reference implementations. See [third-party notices](THIRD-PARTY-NOTICES.md) for retained dependency/data licenses.
