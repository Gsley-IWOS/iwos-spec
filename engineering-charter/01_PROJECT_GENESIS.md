# IWOS Project Genesis

**Document ID:** PG-001

**Version:** 1.0.0 (Genesis)

**Status:** Ratified

**Repository:** iwos-spec

**Classification:** Constitutional Programme Charter

**Authority:** Constitutional Programme Standard

**Parent Documents:**

- 00_FOUNDING_CHARTER.md
- 06_ENGINEERING_CONSTITUTION.md

**Last Updated:** 2026-10-31

---

# Purpose

Project Genesis translates the Founding Charter into an executable engineering programme.

It defines how early IWOS work is sequenced, how work is authorised and bounded, what every unit of delivery must contain, and how the programme preserves traceability and quality. It does not define architecture, standards or implementation.

---

# Authority

Project Genesis is subordinate to the Founding Charter and the Engineering Constitution. It is a parent document of the Architecture Baseline and is interpreted together with the Engineering Playbook, the Code Review Playbook and the AI Agent Contract.

Where Project Genesis conflicts with a higher document, the higher document prevails.

---

# Section 1. The Programme

The IWOS engineering programme builds a Cognitive Operating System that transforms human intent into reliable, explainable, verifiable and continuously improving execution.

The programme is organised around three commitments:

1. Constitutional engineering: authority is written down before work begins.
2. Architecture-led delivery: implementation inherits from ratified architecture.
3. Evidence-based validation: nothing is complete until it is verified.

Early work prioritises durable foundations over speed.

---

# Section 2. Delivery Strategy

Delivery proceeds through controlled milestones. Each milestone is complete only when its outputs are ratified and engineering memory is updated.

| Milestone | Objective | Primary outputs |
| --- | --- | --- |
| M0 Constitutional Foundation | Establish authority. | Founding Charter, Engineering Constitution, Project Genesis, Architecture Baseline, playbooks, AI Agent Contract, onboarding files, engineering memory. |
| M1 Governance and Standards | Establish how change happens and what quality means. | Governance policies, standards, decision records, proposals, templates, schemas, examples, validation tooling. |
| M2 Specification | Specify each constitutional component and engine of the Architecture Baseline. | Component and engine specifications, contracts, schemas. |
| M3 Reference Implementation Readiness | Prepare the implementation repository to build against ratified specifications. | Compliance criteria, certification criteria, SDK contracts. |

Milestones M2 and M3 are sequenced here for programme planning. Their detailed scope is authorised by future work packages and proposals, not by this document.

---

# Section 3. Programme Principles

- Mission before implementation.
- Architecture before code.
- Knowledge as infrastructure.
- Evidence before recommendation.
- Verification before completion.
- Human accountability for every authority decision.
- Continuous improvement through engineering memory.

---

# Section 4. Units of Delivery

The programme is decomposed as follows. Each level is traceable to the level above it.

| Unit | Definition | Record |
| --- | --- | --- |
| Release | A ratified set of specification artefacts carrying a version under the versioning policy. | `CHANGELOG.md`, git tag |
| Milestone | A programme objective in Section 2. | `.ai/ENGINEERING_STATE.yaml` |
| Sprint | A bounded period in which one or more work packages are executed. | `.ai/ENGINEERING_STATE.yaml` |
| Epic | A coherent capability spanning several work packages. | `.ai/ENGINEERING_STATE.yaml` |
| Story | A reviewable outcome within a work package. | `.ai/ENGINEERING_STATE.yaml`, pull request |
| Task | A single engineering action within a story. | `.ai/ENGINEERING_STATE.yaml`, pull request |
| Engineering Work Package | The authorising artefact for a bounded unit of work. | `work-packages/EWP-####.md` |

Every work package must define: objective, scope and non-scope, inputs, outputs, validation criteria, completion evidence and the authority under which it is issued.

---

# Section 5. Scope Control

A work package authorises only the work it names. It must not introduce unrelated governance, standards, schemas, templates, workflows, examples or implementation work.

Scope is extended only by amending the work package or issuing a new one. Scope is never extended for convenience.

---

# Section 6. Traceability

Every significant output is traceable to:

- the mission it serves,
- the architectural authority it inherits,
- the work package, decision record or proposal that authorises it,
- the verification evidence that shows it is complete.

Traceability is recorded in pull-request handoffs, in `CHANGELOG.md` and in the decision graph.

---

# Section 7. Quality Strategy

Quality is designed in through four mechanisms: review gates, automated validation, complete documentation and controlled change.

A deliverable is complete only when its required documents exist, every reference resolves, metadata is consistent, the hierarchy of authority is respected, every required section is finished and the repository validator passes.

---

# Section 8. AI Collaboration

AI agents are first-class participants in the programme, as the Architecture Baseline requires. They may research, draft, review, verify and implement under the AI Agent Contract.

AI assistance never transfers authority away from human reviewers and maintainers. Every AI contribution is reviewed by a human before it becomes authoritative.

---

# Section 9. Engineering Memory

The programme preserves engineering memory in versioned documents, decision records, the knowledge graph, the decision graph and the engineering state. Memory is updated at the completion of every engineering activity.

Knowledge gained in one unit of delivery must improve the next.

---

# Ratification

Project Genesis PG-001 is ratified as the programme charter of IWOS engineering delivery.

It is effective on merge to `main` by an authorised human maintainer and remains in force until superseded by a formally ratified Project Genesis release.

---

**Document Status:** Ratified

**Version:** 1.0.0 (Genesis)

**Release:** PG-1.0
