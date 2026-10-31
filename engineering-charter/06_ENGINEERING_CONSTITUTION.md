# IWOS Engineering Constitution

**Document ID:** EC-001

**Version:** 1.0.0 (Genesis)

**Status:** Ratified

**Repository:** iwos-spec

**Classification:** Constitutional Engineering Law

**Authority:** Supreme Engineering Law beneath the Founding Charter

**Parent Documents:**

- 00_FOUNDING_CHARTER.md

**Last Updated:** 2026-10-31

---

# Purpose

The Engineering Constitution is the supreme engineering law of IWOS beneath the Founding Charter.

It converts the seven principles of the Founding Charter into enforceable rules: the order of authority among documents, the duties of every contributor, the conditions under which architecture may change, the role of AI agents, and the conditions under which a change may be merged.

---

# Authority

The Engineering Constitution is subordinate only to the Founding Charter.

Every programme document, architecture document, playbook, contract, governance policy, standard, specification, schema, template, example, work package and implementation is subordinate to this Constitution.

Where a subordinate document conflicts with this Constitution, this Constitution prevails. Where this Constitution conflicts with the Founding Charter, the Founding Charter prevails.

---

# Definitions

**Constitutional document.** A document in `engineering-charter/`.

**Protected document.** A constitutional document in `engineering-charter/`, a ratified standard matching `standards/*-standard.md`, or a governance policy matching `governance/*.md`. Protected documents are recorded in the constitutional integrity lock and change only through the decision process.

**Decision process.** The governed sequence Request for Comments, Architecture Improvement Proposal, Architecture Decision Record, document update, implementation, release, as defined by the Founding Charter and the Architecture Baseline and operated under `governance/decision-process.md`.

**Ratification.** The act by which a document becomes authoritative. In this repository a document is ratified when an authorised human maintainer merges it to `main` with status `Ratified`, `Accepted` or `Approved`.

**Engineering memory.** The persistent, machine-readable record of engineering state, knowledge, decisions and change history maintained under `.ai/` and in `CHANGELOG.md`.

---

# Article 1. Hierarchy of Authority

Engineering authority in IWOS follows this order:

1. Founding Charter.
2. Engineering Constitution.
3. Project Genesis.
4. Architecture Baseline.
5. Constitutional operating documents: the AI Agent Contract, the Engineering Playbook and the Code Review Playbook.
6. Ratified governance policies and standards.
7. Accepted Architecture Decision Records.
8. Published specifications, schemas and templates.
9. Approved work packages.
10. Implementation.
11. Verification evidence and release artefacts.
12. Engineering memory.

A document may bind only documents below it. A document below may clarify, but never redefine, a document above.

Architecture Improvement Proposals and Requests for Comments are proposal artefacts. They hold no authority of their own. Their outcomes become binding only when recorded in a document that does.

---

# Article 2. Supreme Engineering Principles

All engineering work must uphold the seven principles of the Founding Charter:

1. Intent before implementation.
2. Architecture before code.
3. Knowledge is a first-class asset.
4. Intelligence must be verifiable.
5. Systems must learn.
6. Human authority is absolute.
7. Excellence over convenience.

No rule in any subordinate document may be read so as to weaken any of these principles.

---

# Article 3. Architecture Supremacy

Architecture is a governing asset, not a by-product of implementation.

No contributor and no AI agent may redefine architecture through implementation, through examples, through tooling or through documentation that is not itself an architectural authority.

The Architecture Baseline changes only through a ratified Architecture Baseline release produced by the decision process. Documents in `architecture/` describe, index and explain the baseline and, where an accepted proposal authorises, specify a component within it; they do not extend it.

When architecture is unclear, work stops and the question enters the decision process. Inventing undocumented architecture is prohibited.

---

# Article 4. Human Authority

Humans define purpose, approve changes to authority, and remain accountable for every merge, release and governance decision.

AI agents may research, draft, verify, implement and recommend within an authorised scope. An AI agent never holds final authority. An AI agent must not merge, must not approve its own work, and must not describe an unmerged document as ratified.

---

# Article 5. Duty of Verification

Every engineering activity must produce evidence proportionate to its risk and scope.

Evidence includes, as applicable: repository validation, schema validation, reference and link checks, tests, static analysis, security review, performance review and maintainability review.

Work that has not been verified is not complete. A check that cannot run must be recorded with the reason.

---

# Article 6. Duty of Knowledge

Knowledge is preserved as infrastructure.

Every completed engineering activity must update engineering memory: the change log, the current state, the engineering state, the knowledge graph and the decision graph.

Significant decisions must be recorded as Architecture Decision Records or in the decision graph. Rationale must not be lost in conversations, issues or pull-request comments alone.

Engineering history is never deleted. Superseded documents are marked superseded and retained.

---

# Article 7. Scope and Change Control

Work remains inside the scope of the artefact that authorises it.

Every change must be traceable to a work package, an accepted Architecture Decision Record, an accepted Architecture Improvement Proposal, or an issue opened through the repository's issue forms. A proposed work package authorises work to proceed as a proposal; its outputs become authoritative only when the package is approved.

Changes to protected documents require an accepted proposal and must update the constitutional integrity lock in the same change. Unrelated changes must not be bundled.

The creation of the founding documents under EWP-0001 and EWP-0002 precedes this Article. It is ratified by the merge of the founding release, as the Change Control Policy records.

The classes of change, their required traceability and their approval requirements are defined in `governance/change-control-policy.md`.

---

# Article 8. Compatibility and Integrity

Engineering optimises for long-term correctness, clarity, maintainability, observability, reliability, extensibility, testability and performance.

Breaking changes to any published artefact must identify the artefacts affected and the migration expected, and must follow `governance/versioning-policy.md`.

Short-term convenience never justifies compromising architectural integrity.

---

# Article 9. Agent Compliance

Every AI agent participating in IWOS engineering is bound by the AI Agent Contract.

An agent must complete the onboarding steps in `AGENTS.md` before changing anything, must verify the constitutional integrity lock, must respect the hierarchy in Article 1, must avoid every prohibited action in the AI Agent Contract, and must produce a handoff containing every mandatory section.

---

# Article 10. Review and Merge

No change is merged without passing every gate in the Code Review Playbook and every automated check in the repository's continuous-integration workflow.

Merge is performed only by an authorised human maintainer. Merge to `main` constitutes ratification of any document in the change whose status is `Ratified`, `Accepted` or `Approved`.

---

# Article 11. Amendment

This Constitution is amended only by a ratified Engineering Constitution release produced through the decision process and approved by a human maintainer with constitutional authority as defined in `governance/roles-and-authority.md`.

An amendment must preserve the Founding Charter, must state the Articles affected, and must update the constitutional integrity lock.

---

# Ratification

Engineering Constitution EC-001 is ratified as the supreme engineering law of IWOS beneath the Founding Charter.

It is effective on merge to `main` by an authorised human maintainer and remains in force until superseded by a formally ratified Engineering Constitution release.

---

**Document Status:** Ratified

**Version:** 1.0.0 (Genesis)

**Release:** EC-1.0
