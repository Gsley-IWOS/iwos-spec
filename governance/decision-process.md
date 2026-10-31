# Decision Process

**Document ID:** GOV-003  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Documents:** engineering-charter/06_ENGINEERING_CONSTITUTION.md, engineering-charter/02_ARCHITECTURE_BASELINE.md  
**Last Updated:** 2026-10-31

## Purpose

This policy operates the governance sequence that the Founding Charter and the Architecture Baseline prescribe: Request for Comments (RFC), Architecture Improvement Proposal (AIP), Architecture Decision Record (ADR), document update, implementation. It defines when each artefact is required, what it contains, where it lives, how it is numbered and how it moves between states.

## Scope

This policy applies to every change to architecture, governance, standards, contracts and published specifications, and to every durable technical decision in the IWOS ecosystem. Editorial changes are handled by the Change Control Policy without this process.

## Definitions

**Request for Comments (RFC).** A non-binding artefact that collects structured feedback on a question, concept or option before a proposal is written.

**Architecture Improvement Proposal (AIP).** A binding-when-accepted proposal to change a protected document or a published specification, or to publish a new specification. Acceptance authorises the change; the changed or new document records the result.

**Architecture Decision Record (ADR).** The durable record of a technical decision taken within the bounds of the Architecture Baseline, with its context, drivers, options, decision and consequences.

## When Each Artefact Is Required

| Situation | Required artefact |
| --- | --- |
| The answer to a question is unclear and more than one reasonable option exists. | RFC. |
| A change to a protected document: the Founding Charter, Engineering Constitution, Project Genesis, Architecture Baseline, a playbook, the AI Agent Contract, a standard or a governance policy. | AIP, then the document update, then an ADR if the change embodies a technical decision. |
| A durable technical decision within the Architecture Baseline: a boundary, a contract, a format, a tool, a convention that constrains future work. | ADR. |
| A specification of a component or engine named in the Architecture Baseline. | AIP authorising the specification; the specification itself; ADRs for its design decisions. |
| A decision that constrains future work but is not architectural. | Entry in `.ai/DECISION_GRAPH.yaml`. |

## Sequence

```text
RFC (optional, exploratory)
  -> AIP (required for protected documents, policies, standards, specifications)
    -> ADR (required for durable technical decisions)
      -> Document update (Architecture Baseline release, standard, policy or specification)
        -> Implementation
          -> Release
```

A step may be skipped only where the table above does not require it. Architecture never changes by skipping to implementation.

## Artefact Requirements

### Request for Comments

Location `governance/rfc/RFC-####.md`, template `templates/rfc-template.md`. Required sections: Question, Background and Constraints, Options, Requested Feedback, Review Period, Disposition.

States: `Open`, `Closed`, `Converted`, `Withdrawn`. A Maintainer closes an RFC and records its disposition. An RFC changes nothing by itself.

### Architecture Improvement Proposal

Location `aip/AIP-####-<kebab-title>.md`, template `templates/aip-template.md`, index `aip/README.md`. Required sections: Summary, Motivation, Specification, Impact, Compatibility, Alternatives, Governance Outcome.

States: `Draft`, `Review`, `Accepted`, `Rejected`, `Deferred`, `Superseded`, `Withdrawn`. The authority that may accept an AIP is defined in the Roles and Authority policy. Acceptance is recorded by merging the AIP with status `Accepted`. An accepted AIP authorises exactly the change its Specification section describes.

### Architecture Decision Record

Location `adr/ADR-####-<kebab-title>.md`, template `templates/adr-template.md`, index `adr/README.md`. Required sections, as the Architecture Standard requires: Context, Decision Drivers, Options Considered, Decision, Consequences. Required metadata: Status, Date, Authority.

States: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded`. A record is submitted as `Proposed`; the Architecture Authority sets `Accepted` in the record and the register before or in the merge. An accepted ADR is immutable except for an administrative correction or a supersession note. A superseding ADR names the record it supersedes, and the superseded record is marked `Superseded` with a link forward. Rejected and superseded records are retained.

## Numbering

Identifiers are four-digit, zero-padded, allocated sequentially within each family and never reused. The index file of each family is the allocation register.

## Review Periods

An RFC remains open for at least five working days unless closed earlier by consensus recorded in the RFC. An AIP remains in `Review` for at least five working days. An ADR may be accepted as soon as the Architecture Authority approves the pull request that contains it. Emergency changes follow the Change Control Policy.

## Ratification

This policy is ratified under the Engineering Constitution and the Architecture Baseline. It is effective on merge to `main` by an authorised human maintainer.
