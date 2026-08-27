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

**Last Updated:** 2026-07-31

---

# Purpose

The Code Review Playbook defines mandatory review gates and merge criteria for IWOS engineering work.

It ensures changes are mission-aligned, architecture-compliant, traceable, tested and ready for responsible human review.

---

# Authority

This playbook is mandatory for review and merge decisions.

It is subordinate to the Founding Charter and Engineering Constitution and operates in alignment with the Project Genesis, Architecture Baseline, Engineering Playbook and AI Agent Contract.

No change may be merged by bypassing the review gates in this document.

---

# Sections

## 1. Review Objectives

Code review exists to protect:

- Mission alignment.
- Architectural integrity.
- Constitutional compliance.
- Quality and maintainability.
- Traceability and auditability.
- Security and reliability.
- Knowledge preservation.

## 2. Required Review Gates

Every change shall pass these gates before merge:

1. Scope gate: the change matches the approved task.
2. Authority gate: the change respects document hierarchy.
3. Architecture gate: the change conforms to the Architecture Baseline.
4. Quality gate: the change is clear, maintainable and proportionate.
5. Verification gate: required checks are executed and reported.
6. Documentation gate: affected documentation is updated.
7. Traceability gate: decisions, risks and impacts are visible.
8. Human review gate: an authorised human reviewer approves the change.

## 3. Merge Criteria

A change is mergeable only when:

- The objective is complete.
- No unrelated work is included.
- Required references resolve.
- Metadata and versions are consistent.
- Tests or validation checks have passed or documented environment limitations are accepted by reviewers.
- No known broken state is introduced.
- Review comments are resolved.
- The reviewer determines that the change protects long-term architectural integrity.

## 4. Mandatory Reviewer Checks

Reviewers shall evaluate:

- Alignment with the Founding Charter.
- Alignment with Project Genesis.
- Alignment with the Architecture Baseline.
- Alignment with the Engineering Constitution.
- Compliance with the AI Agent Contract when AI agents contributed.
- Security impact.
- Performance impact when applicable.
- Operational and maintenance impact.

## 5. Prohibited Merge Conditions

A change shall not be merged if it:

- Redefines architecture without approved governance.
- Introduces undocumented architectural behaviour.
- Contains unfinished required sections.
- Contains unresolved drafting markers.
- Skips required validation without reviewer-accepted rationale.
- Includes unrelated work.
- Weakens traceability, auditability or human authority.

## 6. Review Evidence

Each pull request shall provide:

- Summary of changes.
- Files changed.
- Architectural decisions.
- Validation performed.
- Known risks or unresolved questions.
- Recommendations for follow-up work.

## 7. AI-Assisted Review

AI agents may assist with review, but AI review is advisory.

Human authority remains absolute for approval, rejection and merge decisions.

## 8. Ratification

Code Review Playbook CRP-001 is ratified as the mandatory review and merge gate standard for IWOS engineering work.

It remains in force until superseded by a formally ratified Code Review Playbook release.

---

**Document Status:** Ratified

**Version:** 1.0.0 (Genesis)

**Release:** CRP-1.0
