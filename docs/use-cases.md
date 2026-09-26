# What ASIF makes possible

Work with an agent often outlives a browser tab, a computer or a particular provider. ASIF proposes a shared record of that work: the participants, conversation, selected inputs, files, decisions, tool activity and known state. That record gives an integrating application a basis for moving work or involving another agent.

These are illustrative workflows. The linked JSON examples are synthetic and can be inspected with the local reference tools. Live provider adapters and agent coordination are still integration work; the [implementation scope](../REFERENCE.md) describes what runs today.

## Move between a laptop, desktop and cloud

You begin a data analysis on a laptop, move the longer processing step to a cloud machine, then inspect the result on a desktop.

1. The source captures a checkpoint, the selected model context, input data, current outputs and required tools.
2. The destination maps the logical workspace to a local path and assesses files, tool versions, model capabilities and access requirements.
3. If the destination can support the plan and has authorization, its adapter imports the session and constructs the next interaction.
4. A later export records the cloud agent's work and resulting checkpoint for the next handoff.

**The benefit:** the handoff can preserve both the work products and the state of the task. The receiving agent can be told which analysis already ran and which question remains.

The [another-computer fixture](../examples/continuation/another-computer.session.json) and its [synthetic report](../examples/continuation/another-computer.report.json) illustrate a macOS/ARM to Linux/x86 mapping. Moving between cloud providers uses the same destination-assessment model. A captured process status does not transfer a running process; destination credentials, services and dependencies must be resolved there.

## Give agents from different providers different roles

You are preparing a community workshop. A writer drafts a plan, a reviewer checks it against the brief, and an editor incorporates the feedback. Each could use a different provider while contributing to one logical session.

| Participant | Shared information | Additional input | Contribution |
|---|---|---|---|
| Writer, Provider A | Workshop brief and constraints | Writer instructions | Initial plan |
| Reviewer, Provider B | The same brief and constraints | Reviewer instructions and the initial plan | Specific corrections |
| Editor, Provider C | The same brief and constraints | Editor instructions, plan and review | Revised plan |

**The benefit:** specialization without manually reconstructing the brief for each handoff. The record attributes each contribution and shows the inputs behind it.

Inspect the [complete session](../examples/multi-agent-review.session.json) and its [walkthrough](../examples/README.md#agents-with-different-roles). It uses core participant identities, execution-to-context references, ordered inputs and event provenance. The job labels are expressed in instructions; each agent's output still has the ordinary `assistant` message role.

An agent sees the inputs selected for its execution. Presence in the same session does not give it automatic access to every record or file. An orchestrator must select inputs, enforce access and coordinate writes. ASIF does not define a distributed writer or live synchronization protocol.

## Switch providers during a task

An agent has investigated an issue and identified two possible fixes. You want a different agent to implement the selected fix without repeating the investigation.

The handoff can carry the investigation, chosen approach, relevant files, tool results and remaining tasks. The destination records how it maps tools, instructions and model requirements, including anything it cannot preserve.

**The benefit:** changing providers can retain useful work and expose the cost of the change. The [another-agent scenario](../examples/continuation/README.md) illustrates an `adaptation_required` report when mappings have not yet been accepted. It does not claim compatibility with any real provider.

## Compare approaches from a common starting point

You want two agents to propose alternative designs from the same requirements and evidence. Select a common checkpoint and supply the same ordered brief and supporting resources to each execution. Preserve their responses on separate branches, then explicitly select what a later reviewer receives.

**The benefit:** you can inspect whether differences came with different inputs, instructions, tools or model settings. Shared input content is a useful comparison baseline; it does not prove equivalent provider processing or establish a controlled benchmark by itself.

The [branch rules](../SEMANTICS.md#7-branches-and-selected-history) and [context rules](../SEMANTICS.md#8-context-and-compaction) describe how to retain those distinctions. This comparison workflow is illustrative; the sequential writer/reviewer/editor fixture is not a parallel branch fixture.

## Hand work to a teammate

A teammate takes over a research project after several days of discussion. The session can preserve the objective, decisions, supporting PDFs, generated tables, rejected ideas that were recorded, and questions still awaiting an answer.

**The benefit:** the teammate and their agent get a traceable starting point, with missing information identified. The [image and document](../examples/image-and-document.session.json) and [tool-generated files](../examples/tool-generated-files.session.json) examples illustrate the supporting materials.

The exporter must choose what the recipient may receive. [Redaction](../examples/redacted-attachment.session.json) records a distinct sanitized resource and the resulting loss; historical approvals and source credentials do not grant the recipient new authority.

## Keep a long project understandable after summarization

A session grows too large for the next model request. A summary replaces some material in active context while the original notes remain available in the captured history.

**The benefit:** a later agent can distinguish the retained summary from the original evidence and identify detail that was omitted. The [compaction fixture](../examples/compaction-with-attachment.session.json) records both contexts and the transformation between them. A destination still needs to measure its own context budget and account for any further changes.

## Recover an interrupted workflow

A remote publish operation was requested, but the connection failed before its result was captured. A new agent needs to know whether to wait, inspect the remote system or ask for help.

**The benefit:** the handoff preserves uncertainty instead of treating a missing result as proof that the action failed. The [pending-operation scenario](../examples/continuation/pending-remote-operation.session.json) carries operation identity and recovery prerequisites. Its [report](../examples/continuation/pending-remote-operation.report.json) remains blocked while the outcome and access are unresolved.

ASIF records what needs reconciliation. A destination integration must perform that reconciliation before deciding whether another action is appropriate.

## Keep an inspectable record of the work

Months later, you want to understand which documents informed a recommendation, which agent made it, and whether a tool actually returned a result.

**The benefit:** stable references connect inputs, participants, outputs and recorded evidence across the session. Coverage and loss declarations distinguish missing information from known absence. The [package convention](../TRANSPORT.md) can carry exact document and attachment bytes with integrity checks.

An archive supports inspection of what was recorded. It does not prove that recorded claims are true, recover uncaptured information or guarantee that old runtimes can still execute the session.

## Try the local examples

Follow [getting started](getting-started.md) to install a reference CLI. Then validate the collaboration example and inspect one participant's proposed input:

```sh
node asif.ts validate examples/multi-agent-review.session.json
node asif.ts request examples/multi-agent-review.session.json reviewer-context
```

Replace `node asif.ts` with `.venv/bin/python asif.py` for Python. These commands validate and project the authored data locally; they make no model calls. See [gaps and priorities](../GAPS.md) for the implementation and independent evidence needed to turn these workflows into demonstrated integrations.
