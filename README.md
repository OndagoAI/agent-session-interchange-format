# Agent Session Interchange Format (ASIF)

ASIF defines what an agent session contains and what another implementation must preserve and understand. The current design is **0.3**, a session data-model proposal.

New to ASIF? Follow the [getting started guide](docs/getting-started.md). The documentation includes a searchable GitHub Pages site; see [preview and publishing instructions](docs/site.md).

Start with the [specification](SPEC.md). It defines identity, participants, conversation, branches, executions, effective context, configuration, tool activity, decisions/tasks, memory, resources, environment, checkpoints, and coverage/losses.

The central distinction is between recorded history, selected branch history, and actual model input. Interchange preserves those distinctions; continuation additionally needs known state, supported capabilities, available resources and destination authorization.

- [Core object reference](docs/objects.md), [continuation objects](docs/continuation-objects.md), and [destination report objects](docs/report-objects.md): fixed fields, types, requirements, semantics and checked examples.
- [Session semantics](SEMANTICS.md)
- [Python CLI](asif.py) and [TypeScript CLI](asif.ts), with [installation and command documentation](REFERENCE.md): validation, context projection, selected-tree restoration, packaging/signatures and redaction audit.
- [Package transport](TRANSPORT.md) and [streaming/external bindings](STREAMING.md).
- [Structural JSON Schema](schemas/session.schema.json)
- [Portable-continuation profile](CONTINUATION.md): checkpoints, workspace/path mappings, runtime/tool/model dependencies, configuration, authentication, operation recovery, native import and destination assessment.
- [Continuation profile schema](schemas/continuation.schema.json) and [destination report schema](schemas/continuation-report.schema.json).
- [Seven worked examples](examples/README.md): images, PDF, audio, tool outputs, unavailable/redacted attachments, compaction, and pending approval.
- [Three continuation scenarios](examples/continuation/README.md): another computer, another agent, and an unresolved remote operation, each with a separate synthetic destination report.
- [Core versus optional profiles](PROFILES.md)
- [Remaining specification gaps](GAPS.md)
- [Conformance acceptance plan](CONFORMANCE.md)
- [Governance proposal](GOVERNANCE.md)
- [Structural check results](tests/results.json)
- [Example and attachment check results](tests/example-results.json)
- [Continuation check results](tests/continuation-results.json)

Version 0.3 includes a linked object reference with examples for every object, optional stream/external-call bindings, state-transition rules, and local vendor-neutral tools. The schemas and local checks cover structure and selected semantic invariants. Full semantic validation, real adapters and independent interoperability evidence remain outstanding. Synthetic destination reports cannot authorize execution.

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
