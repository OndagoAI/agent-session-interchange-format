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

# Good work<br>should travel.

<p class="asif-lead">Take an agent's work to another computer, another cloud, or another agent. Bring the context with it.</p>

ASIF is a proposed open format for the conversation, inputs, files and decisions that make a session useful beyond its original environment.

<div class="asif-actions" markdown="1">

[Get started <span aria-hidden="true">↗</span>](getting-started.md){ .asif-button .asif-button-primary }
[Read the specification <span aria-hidden="true">→</span>](../SPEC.md){ .asif-text-link }

</div>

<p class="asif-hero-note">Open specification <span aria-hidden="true">·</span> JSON <span aria-hidden="true">·</span> Python &amp; TypeScript</p>

</div>

<div class="asif-session-demo" aria-label="Illustration of a portable agent session" markdown="0">
<div class="asif-demo-caption"><span>ONE SESSION. MORE POSSIBILITIES.</span><span aria-hidden="true">↗</span></div>
<div class="asif-session-card">
<div class="asif-session-heading"><span class="asif-file-icon" aria-hidden="true">{ }</span><div><strong>workshop-plan</strong><span>Agent session / ASIF 0.3</span></div><span class="asif-file-type">JSON</span></div>
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

<span class="asif-draft-label">A proposal you can inspect.</span>

ASIF 0.3 includes schemas, synthetic examples and local reference tools. Live adapters and independent interoperability remain open work. [See the current scope](../REFERENCE.md) and [help close the gaps](../GAPS.md).

</aside>
