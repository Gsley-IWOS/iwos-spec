# IWOS Code Review Playbook

**Document ID:** CRP-001

**Version:** 1.0.0 (Genesis)

**Status:** Ratified

**Repository:** iwos-spec

**Classification:** Constitutional Review Standard

**Authority:** Mandatory Review Gate

**Parent Documents:**

- 00_FOUNDING_CHARTER.md
- 01_PROJECT_GENESIS.md
- 02_ARCHITECTURE_BASELINE.md
- 03_ENGINEERING_PLAYBOOK.md
- 06_ENGINEERING_CONSTITUTION.md

**Last Updated:** 2026-10-31

---

# Purpose

The Code Review Playbook defines the mandatory review gates and merge criteria for every change to an IWOS repository.

Review exists to ensure that a change is mission-aligned, constitutionally compliant, architecturally sound, verified, documented, traceable and approved by an accountable human.

---

# Authority

This playbook is mandatory for every review and merge decision. It is subordinate to the Founding Charter, the Engineering Constitution, Project Genesis and the Architecture Baseline, and operates together with the Engineering Playbook and the AI Agent Contract.

No change may be merged by bypassing a gate in this document.

---

# Section 1. Review Objectives

Review protects:

- mission alignment,
- architectural integrity,
- constitutional compliance,
- quality and maintainability,
- traceability and auditability,
- security and reliability,
- knowledge preservation.

---

# Section 2. Review Gates

Every change must pass all eight gates before merge. The reviewer must record the outcome of each gate in the review.

| Gate | Question the reviewer answers | Evidence |
| --- | --- | --- |
| 1 Scope | Does the change match the authorising work package, decision record, proposal or issue, with nothing unrelated? | Authority cited; diff matches scope. |
| 2 Authority | Does the change respect the hierarchy in Article 1 of the Engineering Constitution? Were protected documents changed only under an accepted proposal, with the integrity lock updated? | Validator integrity check; proposal linked. |
| 3 Architecture | Does the change conform to the Architecture Baseline and accepted Architecture Decision Records? Does it invent no architecture? | Reviewer statement. |
| 4 Quality | Is the change clear, proportionate, maintainable and free of drafting markers, empty files and unverifiable claims? | Validator structural checks; reviewer reading. |
| 5 Verification | Were `make validate` and `make test` run and did they pass, or is a limitation documented and accepted? | Continuous-integration result; handoff. |
| 6 Documentation | Is every affected document updated and does every new document satisfy the Documentation Standard? | Validator; reviewer reading. |
| 7 Traceability | Are decisions, risks and impacts visible? Is engineering memory updated? | `CHANGELOG.md`, `.ai/` diff, decision records. |
| 8 Human review | Has an authorised human reviewer approved the change? | Approval on the pull request. |

---

# Section 3. Merge Criteria

A change is mergeable only when:

- every gate in Section 2 passes,
- the continuous-integration workflow is green,
- every review comment is resolved or explicitly deferred with a recorded reason,
- the change introduces no known broken state,
- the reviewer determines that the change leaves the repository better than it found it.

---

# Section 4. Mandatory Reviewer Checks

The reviewer evaluates alignment with the Founding Charter, Project Genesis, the Architecture Baseline and the Engineering Constitution; compliance with the AI Agent Contract when an agent contributed; and the security, performance, operational and maintenance impact of the change.

For a security-relevant change the reviewer applies the review criteria of the Security Standard. For a schema change the reviewer confirms that valid and invalid examples were added or updated as the Testing Standard requires.

---

# Section 5. Prohibited Merge Conditions

A change must not be merged if it:

- redefines architecture without an accepted proposal and a ratified baseline update,
- introduces undocumented architectural behaviour,
- changes a protected document without an accepted proposal or without updating the integrity lock,
- contains unfinished required sections, drafting markers or empty files,
- skips required validation without a reviewer-accepted reason,
- includes unrelated work,
- deletes engineering history,
- weakens traceability, auditability or human authority,
- was approved only by its author or only by an AI agent.

---

# Section 6. Review Evidence: The Handoff

Every pull request contains the six handoff sections mandated by the AI Agent Contract plus a Validation section, which this playbook adds as the evidence for the Verification gate, in this order, using the pull request template in `.github/`:

1. Summary.
2. Files Changed.
3. Decisions.
4. Validation.
5. Risks.
6. Outstanding Work.
7. Recommended Next Task.

A pull request missing any section is returned without review.

---

# Section 7. AI-Assisted Review

AI agents may review and may post findings. AI review is advisory. Approval, rejection and merge are human acts.

An AI agent must not approve a change, must not merge, and must not resolve a human reviewer's comment on the human's behalf.

---

# Section 8. Reviewer Conduct

Reviewers prefer evidence over opinion, state the gate a finding belongs to, and distinguish blocking findings from suggestions. Authors respond to every finding. Disagreements that cannot be resolved in review are escalated through `governance/decision-process.md`.

---

# Ratification

Code Review Playbook CRP-001 is ratified as the mandatory review and merge gate standard for IWOS engineering work.

It is effective on merge to `main` by an authorised human maintainer and remains in force until superseded by a formally ratified Code Review Playbook release.

---

**Document Status:** Ratified

**Version:** 1.0.0 (Genesis)

**Release:** CRP-1.0
