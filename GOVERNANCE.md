# Proposed ASIF governance

Status: draft charter for implementer review, 2026-09-26. No governing body, elected maintainers, membership, or upstream affiliation is asserted by this document.

## Purpose

Maintain the shared session data model, its extension process, and public evidence of correct interpretation and interchange. Governance must serve implementers and session owners across vendors, including non-coding use cases.

## Roles and independence

- Editors prepare specifications and resolve editorial issues; they do not certify their own implementations as independent evidence.
- Implementers maintain readers/writers and publish versioned conformance reports, limitations, and supported profiles.
- Maintainers accept normative changes through the process below.

Before candidate-standard status, recruit at least three named maintainers from at least two independent organizations or unaffiliated projects. No single employer may hold a majority. Affiliations and conflicts of interest are public. A local author may maintain the prototype during incubation, but cannot waive the independence gate.

## Decisions

Normative changes require a numbered RFC: problem, alternatives, schema impact, privacy implications, compatibility/migration, fixtures, and implementation evidence. Publish the proposal for at least 14 calendar days, resolve recorded objections, and require two maintainer approvals from different affiliations. Record dissent and rationale. Editorial corrections may use one approval if they do not change semantics.

Seek rough consensus. If maintainers cannot resolve a substantive objection, retain the existing behavior and document the dispute for a second review rather than silently changing the contract. Security-sensitive issues may be handled privately until a coordinated fix is ready; their eventual specification changes and compatibility effects must be public.

## Maturity levels

1. **Experimental:** editor drafts, prototype schemas, fixtures; no interoperability promise.
2. **Review draft:** named editors, proposed rights/license terms, public issues/RFC process, pinned schemas, reproducible tests, and at least one implementation.
3. **Candidate standard:** maintainer independence above; at least two independently authored implementations from separate organizations/projects; bidirectional exchange against frozen fixtures; documented profile coverage and negative cases; no unresolved P0 semantic contradictions.
4. **Stable community specification:** public review complete, compatibility policy adopted, external reports published, required independent implementers approve the same release.

Calling a community specification “stable” does not imply approval by IETF or another standards organization. If adopted upstream, that organization's process governs the resulting standard; this charter must not claim authority over upstream names or registries.

## Change and extension policy

Breaking meanings or interpretation requirements require a new major version. Optional additions must preserve old meanings and unknown data. Required extensions use versioned names and a documented refusal path. A profile registration needs a stable owner, exact schema/semantics, privacy considerations, fixtures, and two implementation reports before stable status.

Do not register extensions solely because a vendor uses a field. Require a use case and specify how a reader behaves without support. Profiles can advance separately from the core. Deprecations carry a migration plan and retained fixtures; no retroactive relabeling of old records.

## Publication, rights, and accountability

The ASIF specification, schemas, examples and reference implementations in this package use the [MIT license](LICENSE). Third-party components retain their own licenses; see [third-party notices](THIRD-PARTY-NOTICES.md). Contribution terms and any additional requirements of a future publication venue remain release work. Contributors disclose relevant restrictions through the venue's adopted policy.

Release artifacts include source revision, schema digest, fixture digest, test reports, known limitations, and a changelog. Maintainer affiliations and implementation affiliations are recorded separately. Anyone may report conformance failures; disputed claims link to a reproducible fixture and remain labeled disputed until resolved.

## Current roster

No external maintainers recruited. No affiliations or endorsements assigned. The local reference implements a documented subset; full conformance is not claimed. Use [IMPLEMENTERS.md](IMPLEMENTERS.md) to record actual participants and evidence when available.
