---
title: Agent sessions that travel
description: Carry work across computers, clouds and providers. ASIF is a proposed open format for portable agent sessions and shared context.
template: home.html
hide:
  - navigation
  - toc
  - footer
---

<section class="asif-hero" markdown="1">
<div class="asif-hero-copy" markdown="1">

<p class="asif-eyebrow">Agent Session Interchange Format</p>

# Your agent's work<br>shouldn't be locked<br>inside one tool.

<p class="asif-lead">Changing computers, clouds or providers can mean rebuilding context by hand. The work should be able to come with you.</p>

ASIF records the conversation, selected inputs, files, decisions and unfinished work, together with the prerequisites another environment needs to assess before continuing.

<div class="asif-actions" markdown="1">

[Try ASIF <span aria-hidden="true">↗</span>](getting-started.md){ .asif-button .asif-button-primary }
[Contribute on GitHub <span aria-hidden="true">→</span>](https://github.com/OndagoAI/agent-session-interchange-format){ .asif-text-link }

</div>

<p class="asif-hero-note">Open proposal <span aria-hidden="true">·</span> MIT licensed <span aria-hidden="true">·</span> Python &amp; TypeScript</p>

</div>

<div class="asif-session-demo" aria-label="Illustration of a portable agent session" markdown="0">
<div class="asif-demo-caption"><span>ONE SESSION. MORE POSSIBILITIES.</span><span aria-hidden="true">↗</span></div>
<div class="asif-session-card">
<div class="asif-session-heading"><span class="asif-file-icon" aria-hidden="true">{ }</span><div><strong>workshop-plan</strong><span>Agent session / ASIF 0.4</span></div><span class="asif-file-type">JSON</span></div>
<div class="asif-demo-tabs" role="tablist" aria-label="Explore the session">
<button type="button" role="tab" id="tab-context" aria-selected="true" aria-controls="demo-context">Context</button>
<button type="button" role="tab" id="tab-agents" aria-selected="false" aria-controls="demo-agents" tabindex="-1">Agents</button>
<button type="button" role="tab" id="tab-handoff" aria-selected="false" aria-controls="demo-handoff" tabindex="-1">Handoff</button>
</div>
<div class="asif-demo-panel" role="tabpanel" id="demo-context" aria-labelledby="tab-context" tabindex="0">
<div class="asif-demo-label">THE WORK, WITH ITS CONTEXT</div>
<div class="asif-context-row"><span class="asif-row-icon" aria-hidden="true">01</span><div><strong>The shared brief</strong><span>A 90-minute workshop for 12 people.</span></div><span class="asif-row-tag">input</span></div>
<div class="asif-context-row"><span class="asif-row-icon" aria-hidden="true">02</span><div><strong>Every contribution</strong><span>The draft, review and revised plan.</span></div><span class="asif-row-tag">history</span></div>
<div class="asif-context-row"><span class="asif-row-icon" aria-hidden="true">03</span><div><strong>Who saw what</strong><span>Explicit inputs for each agent.</span></div><span class="asif-row-tag">context</span></div>
<div class="asif-demo-footnote"><span aria-hidden="true">↳</span> A common brief. A traceable handoff.</div>
</div>
<div class="asif-demo-panel" role="tabpanel" id="demo-agents" aria-labelledby="tab-agents" tabindex="0" hidden>
<div class="asif-demo-label">DIFFERENT ROLES. SHARED STARTING POINT.</div>
<div class="asif-context-row"><span class="asif-agent-initial" aria-hidden="true">A</span><div><strong>Writer</strong><span>Brief → initial plan</span></div><span class="asif-row-tag">Provider A</span></div>
<div class="asif-context-row"><span class="asif-agent-initial" aria-hidden="true">B</span><div><strong>Reviewer</strong><span>Brief + plan → corrections</span></div><span class="asif-row-tag">Provider B</span></div>
<div class="asif-context-row"><span class="asif-agent-initial" aria-hidden="true">C</span><div><strong>Editor</strong><span>Brief + review → revised plan</span></div><span class="asif-row-tag">Provider C</span></div>
<div class="asif-demo-footnote"><span aria-hidden="true">↳</span> Fictional providers. Inspectable inputs.</div>
</div>
<div class="asif-demo-panel" role="tabpanel" id="demo-handoff" aria-labelledby="tab-handoff" tabindex="0" hidden>
<div class="asif-demo-label">A PLAN FOR THE NEXT ENVIRONMENT</div>
<div class="asif-context-row"><span class="asif-row-icon" aria-hidden="true">01</span><div><strong>Capture the boundary</strong><span>Select a checkpoint and context.</span></div></div>
<div class="asif-context-row"><span class="asif-row-icon" aria-hidden="true">02</span><div><strong>Check the destination</strong><span>Account for files, tools and access.</span></div></div>
<div class="asif-context-row"><span class="asif-row-icon" aria-hidden="true">03</span><div><strong>Prepare the next interaction</strong><span>Use a compatible runtime adapter.</span></div></div>
<div class="asif-demo-footnote"><span aria-hidden="true">↳</span> Integration workflow; adapters required.</div>
</div>
</div>
<div class="asif-travel-path"><span>Laptop</span><span aria-hidden="true">⟷</span><span>Cloud</span><span aria-hidden="true">⟷</span><span>Another agent</span></div>
<p class="asif-demo-disclaimer">Illustrative workflow · no agents are running here</p>
</div>
</section>

<section class="asif-handoff" aria-labelledby="from-one-environment-to-the-next" markdown="1">
<div class="asif-section-heading" markdown="1">

<p class="asif-eyebrow">How a handoff fits together</p>

## From one environment to the next.

</div>
<figure class="asif-handoff-flow" aria-label="A local agent exports an ASIF record; a compatible destination assesses it before import" markdown="0">
<div class="asif-flow-stages">
<div class="asif-flow-node"><span class="asif-flow-label">SOURCE</span><strong>Local agent</strong><p>Conversation, decisions<br>and working files</p></div>
<div class="asif-flow-edge"><span>Export</span><span aria-hidden="true">→</span></div>
<div class="asif-flow-node asif-flow-record"><span class="asif-flow-label">PORTABLE RECORD</span><strong>ASIF</strong><p>Inputs · events · checkpoints<br>Resources · dependencies</p></div>
<div class="asif-flow-edge"><span>Assess &amp; import</span><span aria-hidden="true">→</span></div>
<div class="asif-flow-destinations"><div class="asif-flow-node"><span class="asif-flow-label">DESTINATION</span><strong>Cloud worker</strong><p>Resolve the environment</p></div><div class="asif-flow-node"><span class="asif-flow-label">DESTINATION</span><strong>Another agent</strong><p>Account for context adaptations</p></div></div>
</div>
<figcaption>Conceptual flow. Compatible adapters and destination authorization are required; live provider handoffs are not yet demonstrated.</figcaption>
</figure>

[Inspect the synthetic handoff scenario <span aria-hidden="true">→</span>](../examples/continuation/README.md)

</section>

<section class="asif-benefits" aria-labelledby="your-next-step-shouldnt-need-a-fresh-start" markdown="1">
<div class="asif-section-heading" markdown="1">

<p class="asif-eyebrow">Built for the handoff</p>

## Your next step shouldn't need a fresh start.

</div>
<div class="asif-benefit-grid" markdown="1">
<div class="asif-benefit" markdown="1">

<span class="asif-section-number">01 / PORTABILITY</span>

### Change the environment.<br>Carry the work.

Start on a laptop, assess a cloud destination, and bring the results back. Preserve the relevant files, context and unfinished work along the way.

[Explore session portability <span aria-hidden="true">↗</span>](use-cases.md#move-between-a-laptop-desktop-and-cloud)

</div>
<div class="asif-benefit" markdown="1">

<span class="asif-section-number">02 / COLLABORATION</span>

### Different agents.<br>A shared starting point.

Let a writer, reviewer and editor contribute to one session. Keep the shared brief, their distinct instructions and the source of each contribution visible.

[Meet the multi-agent example <span aria-hidden="true">↗</span>](../examples/README.md#agents-with-different-roles)

</div>
<div class="asif-benefit" markdown="1">

<span class="asif-section-number">03 / CONTINUITY</span>

### Keep the decisions.<br>Make the gaps visible.

Preserve what happened, what an agent received and what remains unresolved. Give the next person or tool an inspectable record to work from.

[See more use cases <span aria-hidden="true">↗</span>](use-cases.md)

</div>
</div>
</section>

<section class="asif-start" aria-labelledby="start-with-a-real-document" markdown="1">
<div class="asif-start-copy" markdown="1">

<p class="asif-eyebrow">Try the reference tools</p>

## Start with a real document.

Validate an example, then inspect the inputs selected for its reviewer. The local tools let you explore the format without connecting a provider.

[Installation and quick start <span aria-hidden="true">→</span>](getting-started.md)

</div>
<div class="asif-terminal" markdown="1">

<div class="asif-terminal-title"><span>Terminal</span><span>Node.js 24+ · from the repository</span></div>

```sh
npm ci
node asif.ts validate \
  examples/multi-agent-review.session.json
node asif.ts request \
  examples/multi-agent-review.session.json \
  reviewer-context
```

<div class="asif-terminal-note">Also available in Python. Examples are synthetic.</div>

</div>
</section>

<section class="asif-evidence" aria-labelledby="what-you-can-test-today" markdown="1">
<div class="asif-section-heading" markdown="1">

<p class="asif-eyebrow">Progress you can verify</p>

## What you can test today.

</div>

| Capability | Current evidence |
|---|---|
| Validate documents, inspect selected inputs, package resources | Local Python and TypeScript reference checks for a documented subset |
| Describe a move to another computer or agent | Synthetic continuation scenarios with explicit prerequisite assessments |
| Import a native session and continue on a real destination | Integration work; no live handoff demonstrated by this repository |

[See the compatibility and evidence matrix <span aria-hidden="true">→</span>](compatibility.md)

</section>

<section class="asif-contribute" aria-labelledby="bring-a-sessionfind-a-gap" markdown="1">
<div class="asif-contribute-copy" markdown="1">

<p class="asif-eyebrow">Build with us</p>

## Bring a session.<br>Find a gap.

Building an agent, a coding tool or a cloud runtime? Help test whether ASIF captures the information your application needs for a useful handoff.

[Start contributing <span aria-hidden="true">↗</span>](../CONTRIBUTING.md){ .asif-button .asif-button-primary }

</div>
<div class="asif-contribution-paths" markdown="1">

[<strong>Share a missing-state example</strong><span>Show what your next agent would need to know.</span><span aria-hidden="true">↗</span>](../CONTRIBUTING.md#share-a-use-case)

[<strong>Try an adapter</strong><span>Map a real source and make its limits explicit.</span><span aria-hidden="true">↗</span>](adapters.md)

[<strong>Provide exchange evidence</strong><span>Reproduce a handoff outside the local reference tools.</span><span aria-hidden="true">↗</span>](adapters.md#the-first-live-handoff)

</div>
</section>

<section class="asif-explore" aria-labelledby="find-your-way-in" markdown="1">
<div class="asif-section-heading" markdown="1">

<p class="asif-eyebrow">Inside the documentation</p>

## Find your way in.

</div>
<div class="asif-link-grid" markdown="1">

[<span class="asif-link-kicker">UNDERSTAND</span><strong>The specification</strong><span>Identity, history, context and the rules that connect them.</span><span class="asif-link-arrow" aria-hidden="true">↗</span>](../SPEC.md){ .asif-link-card }

[<span class="asif-link-kicker">BUILD</span><strong>Object reference</strong><span>Fields, types and checked examples for implementers.</span><span class="asif-link-arrow" aria-hidden="true">↗</span>](objects.md){ .asif-link-card }

[<span class="asif-link-kicker">EXPLORE</span><strong>Worked examples</strong><span>Shared context, attachments and continuation scenarios.</span><span class="asif-link-arrow" aria-hidden="true">↗</span>](../examples/README.md){ .asif-link-card }

</div>
</section>

<aside class="asif-draft-note" markdown="1">

<span class="asif-draft-label">Started at Ondago.<br>Open to every implementer.</span>

The team behind Ondago initiated ASIF as a vendor-neutral proposal. Implementing the format requires no Ondago product or account. The code and specification are MIT licensed, and external implementers are invited to shape the draft. [Read the proposed governance](../GOVERNANCE.md).

</aside>
