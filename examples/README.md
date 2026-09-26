# ASIF session examples

These are complete, synthetic ASIF documents. All conversation, tool activity and model context are authored examples; no real agent run, private transcript or user attachment is represented. The small media files are actual fixture bytes with matching lengths and SHA-256 digests.

For destination reconstruction, see the additional [three portable-continuation scenarios](continuation/README.md): another computer/cloud runtime, another agent, and an unresolved remote operation. Each includes a separate, explicitly synthetic assessment report.

For the benefits behind these records, see [use cases](../docs/use-cases.md): moving work between computers and clouds, collaborating across providers, comparing approaches and handing a project to a teammate.

| Example | What to inspect |
|---|---|
| [Agents with different roles](multi-agent-review.session.json) | Three fictional providers contribute to one session; writer, reviewer and editor contexts share the same brief while selecting different instructions and prior contributions. |
| [Image and PDF](image-and-document.session.json) | Ordered text/image/document parts; one image referenced twice; original PDF preserved while extracted text appears in the reconstructed model input. |
| [Audio and transcript](audio-and-transcript.session.json) | A WAV stored as inline base64; a separate inline text annotation. The sample is 0.1 seconds of silence; the annotation explicitly says there is no speech. |
| [Tool-generated files](tool-generated-files.session.json) | Inline CSV input, correlated tool call/result, CSV and Markdown outputs referenced again by the assistant. |
| [Attachment availability](attachment-availability.session.json) | Unavailable PDF, external video, deliberately excluded ZIP and uninspected image. The missing PDF is an explicit continuation prerequisite. |
| [Redacted attachment](redacted-attachment.session.json) | Original content marked redacted; a distinct sanitized resource with its own bytes/hash; loss report and explicit substitution in model input. |
| [Compaction with an attachment](compaction-with-attachment.session.json) | Original notes retained in history; a summary memory selected into a separate continuation context. |
| [Awaiting approval](awaiting-approval.session.json) | Tool call and approval request without a recorded answer or tool result. |

## Agents with different roles

The [multi-agent review session](multi-agent-review.session.json) follows a workshop organizer working with three agents. The writer proposes a plan that exceeds the time limit, the reviewer identifies the error, and the editor revises the plan. All provider names and outputs are invented.

| Context ID | Participant | Selected inputs, in order |
|---|---|---|
| `writer-context` | Writer, `example.provider-a` | Writer instructions; shared brief |
| `reviewer-context` | Reviewer, `example.provider-b` | Reviewer instructions; shared brief; draft |
| `editor-context` | Editor, `example.provider-c` | Editor instructions; shared brief; draft; review |

Each context contains an identical `shared-brief` input referencing the same `workshop-brief` resource. Role instructions are separate, declared configuration records and are explicitly included once in each context. The later inputs reference the earlier contribution events, so you can see what the reviewer and editor were given.

Participants retain distinct IDs and provider labels. Executions bind each participant to its input context; event `actor_id` and `execution_id` attribute each response. Writer, reviewer and editor are job assignments expressed by instructions, while their messages all use `role: assistant`. Execution status remains `unknown` because no actual runtime lifecycle was observed.

Inspect the proposed inputs with either CLI:

```sh
node asif.ts validate examples/multi-agent-review.session.json
node asif.ts request examples/multi-agent-review.session.json writer-context
node asif.ts request examples/multi-agent-review.session.json reviewer-context
node asif.ts request examples/multi-agent-review.session.json editor-context
```

Replace `node asif.ts` with `.venv/bin/python asif.py` for Python. These commands run from the repository root and produce neutral JSON projections. They do not contact providers. The example records a sequential collaboration; scheduling agents, enforcing permissions and coordinating concurrent writes belong to an integrating application.

## Attachment representation

There are three layers:

1. **A message part** refers to a resource and fixes its place among the message's other parts.
2. **The resource** identifies the content, media type, purpose, availability and, for embedded content, bytes and digest.
3. **A context input** records whether the original attachment, a derivative, or neither was selected for the model.

For example, these are actual excerpts from the image/PDF example, not stand-alone session documents:

```json
{
  "kind": "resource",
  "resource_id": "document",
  "description": "One-page invented meeting notes."
}
```

The original resource has `media_type: application/pdf` and `path: assets/meeting-notes.pdf`. Its extracted text has a separate resource ID, `document-text`, and provenance naming `document`. The context explicitly selects that derivative:

```json
{
  "kind": "resource",
  "resource_id": "document-text",
  "description": "Text extracted from the PDF."
}
```

The input also records the transformation. Preserving a PDF therefore does not imply the model received its original bytes or saw every visual feature in it.

## Storage and availability

| Form | Example | Interpretation |
|---|---|---|
| `text` | Input CSV, extracted PDF text, sanitized text, summary memory | Hash the exact UTF-8 encoding, including newlines. |
| `data` | Inline WAV | Strictly decode base64, then verify length and digest. |
| `path` | PNG, PDF, output CSV/Markdown, original notes | Resolve relative to the session document's directory; verify before exposing content. |
| `external` | Video locator | Record location only; this example must not fetch it. The `.invalid` host is deliberately nonfunctional. |
| `unavailable` | Missing PDF | A reference exists but the source bytes could not be recovered. |
| `excluded` | ZIP | Deliberately omitted from the export. |
| `redacted` | Original contact document | Original content is withheld; a sanitized derivative is a different resource. |
| `unknown` | Uninspected image | The exporter did not establish availability. |

Content type does not determine storage: an image could use either base64 or a file path. Original names are descriptive metadata, not automatic extraction destinations. Referencing a resource twice does not duplicate its payload. Different transformed bytes must not reuse the original resource identity.

## Physical attachments

- [color-grid.png](assets/color-grid.png): synthetic 16 × 16 RGB grid.
- [meeting-notes.pdf](assets/meeting-notes.pdf): one-page synthetic text document.
- [totals.csv](assets/totals.csv): generated-output fixture with total row.
- [summary.md](assets/summary.md): generated-output report fixture.
- [project-notes.md](assets/project-notes.md): notes retained after context compaction.

To copy an example elsewhere, copy its JSON document and all resources referenced by `path`, preserving their relative paths. Inline resources need no extra files. The examples share this directory only for convenience; there is no implied relationship among their distinct session IDs.

## Checks and regeneration

From the project root:

```sh
.venv/bin/python tests/check_schema.py
.venv/bin/python tests/check_examples.py
```

The second check validates all eight documents against the schema, verifies embedded resource bytes and references, and checks selected event/branch/context relationships. It also checks that corrupt digests, missing resources and unsafe paths are rejected by the fixture checker. It is not a complete ASIF semantic validator or an interoperability test.

`python3 examples/build_examples.py` deterministically rebuilds the six attachment examples, their five file assets, and the collaboration example. It does not replace the existing approval example. All contexts remain explicitly reconstructed; none claims a real provider request or successful continuation.
