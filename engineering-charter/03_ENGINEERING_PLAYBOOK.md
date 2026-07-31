# IWOS Engineering Playbook

**Document ID:** EP-001

**Version:** 1.0.0 (Genesis)

**Status:** Ratified

**Repository:** iwos-spec

**Classification:** Constitutional Engineering Operations

**Authority:** Mandatory Engineering Practice

**Parent Documents:**

- 00_FOUNDING_CHARTER.md
- 01_PROJECT_GENESIS.md
- 02_ARCHITECTURE_BASELINE.md
- 06_ENGINEERING_CONSTITUTION.md

**Last Updated:** 2026-07-31

---

# Purpose

The Engineering Playbook defines day-to-day engineering operations for IWOS contributors and AI agents.

It operationalises the Founding Charter, Project Genesis, Architecture Baseline, Engineering Constitution and AI Agent Contract without changing their authority.

---

# Authority

This playbook is mandatory practice for engineering work in IWOS repositories.

It is subordinate to the Founding Charter and Engineering Constitution, and it must be interpreted consistently with the Architecture Baseline and AI Agent Contract.

If this playbook conflicts with a higher-authority document, the higher-authority document prevails.

---

# Sections

## 1. Operating Model

IWOS engineering follows a disciplined sequence:

1. Load the mission and relevant parent documents.
2. Verify the current repository state.
3. Confirm scope and dependencies.
4. Produce or update the required design artefacts.
5. Implement only authorised changes.
6. Execute applicable validation.
7. Perform self-review.
8. Update required documentation and engineering memory.
9. Produce a clear handoff for review.

## 2. Mandatory Reading

Before beginning engineering work, contributors and AI agents shall read the documents required by the applicable task.

For AI agents, the mandatory baseline reading path is:

- engineering-charter/00_FOUNDING_CHARTER.md
- engineering-charter/01_PROJECT_GENESIS.md
- engineering-charter/02_ARCHITECTURE_BASELINE.md
- engineering-charter/06_ENGINEERING_CONSTITUTION.md

## 3. Scope Discipline

Work shall remain inside the stated work package or approved task boundary.

Unrelated changes are prohibited.

Architecture, governance, standards, schemas, templates, workflows, examples and implementation assets shall only be changed when the active work package explicitly authorises that category of work.

## 4. Design Before Implementation

Implementation work shall inherit from ratified architecture and approved specifications.

When architecture is unclear, contributors shall stop and request clarification through the appropriate governance process rather than inventing undocumented architecture.

## 5. Documentation Practice

Documentation is an engineering asset.

Documents shall use clear metadata, explicit authority, resolved parent references, stable versioning and complete sections.

Documentation changes shall be reviewed with the same seriousness as code changes.

## 6. Validation Practice

Validation shall be proportionate to the work performed and shall include, where applicable:

- Reference checks.
- Metadata checks.
- Version consistency checks.
- Authority hierarchy checks.
- Static analysis.
- Tests.
- Self-review against acceptance criteria.

## 7. Engineering State

Engineering work shall preserve an accurate account of current release, milestone, sprint, task, risks, decisions and completion evidence when those state mechanisms are available.

State shall be machine-readable when required by the relevant standard.

## 8. Decision Handling

Significant decisions shall be documented and traceable.

Implementation shall not be used to bypass architecture or governance.

Architectural evolution shall follow the RFC, AIP, ADR, Architecture Baseline Update, Implementation sequence defined by the Architecture Baseline.

## 9. AI Agent Operations

AI agents shall comply with the AI Agent Contract.

Agents shall verify repository state, respect constitutional authority, avoid prohibited actions, document changes and provide evidence for completion.

## 10. Completion Criteria

Engineering work is complete when:

- The stated objective is satisfied.
- Parent document alignment is verified.
- Required files and references exist.
- Validation has been executed or explicitly explained.
- Review-ready evidence is available.
- Every required section is finished.

## 11. Ratification

Engineering Playbook EP-001 is ratified as the mandatory operating playbook for day-to-day IWOS engineering work.

It remains in force until superseded by a formally ratified Engineering Playbook release.

---

**Document Status:** Ratified

**Version:** 1.0.0 (Genesis)

**Release:** EP-1.0
