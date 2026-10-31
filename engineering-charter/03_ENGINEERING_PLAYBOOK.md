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

**Last Updated:** 2026-10-31

---

# Purpose

The Engineering Playbook defines how engineering work is performed day to day in IWOS repositories by human contributors and AI agents.

It operationalises the Founding Charter, Project Genesis, Architecture Baseline, Engineering Constitution and AI Agent Contract without changing their authority.

---

# Authority

This playbook is mandatory practice for engineering work in IWOS repositories. It is subordinate to the Founding Charter, the Engineering Constitution, Project Genesis and the Architecture Baseline. Where it conflicts with a higher document, the higher document prevails.

---

# Section 1. Operating Sequence

Every unit of engineering work follows the execution sequence of the AI Agent Contract. The sequence applies equally to human contributors.

| Step | Action | Evidence |
| --- | --- | --- |
| 1 | Load the mission: read the Founding Charter. | Handoff states mission alignment. |
| 2 | Verify the constitution: confirm the constitutional integrity lock matches the protected documents. | `make validate` passes the integrity check. |
| 3 | Load the Architecture Baseline. | Handoff states architectural alignment. |
| 4 | Verify engineering state: read `.ai/CURRENT_STATE.md` and `.ai/ENGINEERING_STATE.yaml`. | State referenced in handoff. |
| 5 | Load the current task: the work package, decision record, proposal or issue that authorises the work. | Authority cited in pull request. |
| 6 | Validate dependencies: confirm every input exists and every parent document resolves. | Validator consistency checks pass. |
| 7 | Produce a design: list the artefacts to create or change and the authority for each. | Plan recorded in pull request or work package. |
| 8 | Implement only the authorised scope. | Diff matches plan. |
| 9 | Execute tests: `make validate` and `make test`. | Output quoted or summarised in handoff. |
| 10 | Perform self-review against the Code Review Playbook gates. | Self-review recorded in handoff. |
| 11 | Update documentation affected by the change. | Documentation gate passes. |
| 12 | Update engineering memory. | `CHANGELOG.md` and `.ai/` updated. |
| 13 | Produce the handoff. | Pull request contains every mandatory section. |

---

# Section 2. Mandatory Reading

Before beginning work, every contributor reads the documents required by the task. The mandatory baseline for AI agents is `mandatory_reading` in the AI Agent Contract:

1. `engineering-charter/00_FOUNDING_CHARTER.md`
2. `engineering-charter/01_PROJECT_GENESIS.md`
3. `engineering-charter/02_ARCHITECTURE_BASELINE.md`
4. `engineering-charter/06_ENGINEERING_CONSTITUTION.md`

`AI_BOOTSTRAP.yaml` lists the further onboarding reading this repository requires of agents, and the authorising work package may add more.

---

# Section 3. Scope Discipline

Work stays inside the stated work package, decision record, proposal or issue. Unrelated changes are prohibited.

Protected documents are changed only by human maintainers under an accepted proposal. Other artefact families are changed only when the authorising artefact names that family.

---

# Section 4. Design Before Implementation

Implementation inherits from ratified architecture and published specifications.

When architecture is unclear, the contributor stops and opens a Request for Comments under `governance/decision-process.md`. Inventing undocumented architecture is prohibited.

---

# Section 5. Documentation Practice

Documentation is an engineering artefact and is reviewed with the same rigour as code.

Every durable document follows the Documentation Standard and the matching template in `templates/`: explicit metadata, explicit authority, resolved parent references, stable versioning under the versioning policy, complete sections and a ratification statement.

Documents must not duplicate canonical definitions. They summarise and link.

---

# Section 6. Validation Practice

Validation is proportionate to the work and always includes running the repository validator. The validator implements the four categories of the Testing Standard:

- Structural checks: required metadata and headings on every governed document.
- Schema checks: every governed YAML artefact validates against its bound JSON Schema.
- Consistency checks: relative links resolve, parent documents exist, Document IDs are unique, mandatory reading paths exist, no drafting markers remain, no credential-shaped strings are present.
- Example checks: every valid example validates, every invalid example is rejected.

The validator additionally performs the integrity check on protected documents. A check that cannot run is recorded in the handoff with its reason.

---

# Section 7. Engineering State

Engineering state is machine-readable and is kept in `.ai/ENGINEERING_STATE.yaml`, which conforms to `schemas/engineering-state.schema.json`. It records the current release, milestone, sprint, epic, story, task, risks and decisions as the Architecture Baseline requires.

State is updated at the completion of every engineering activity, in the same change.

---

# Section 8. Decision Handling

Decisions that constrain future work are recorded.

Architecture decisions within the Architecture Baseline are recorded as Architecture Decision Records in `adr/`. Changes to the Architecture Baseline, to a protected document or to a standard are proposed as Architecture Improvement Proposals in `aip/`. Exploratory questions are raised as Requests for Comments. Lesser decisions are recorded in `.ai/DECISION_GRAPH.yaml`.

Implementation is never used to bypass a decision.

---

# Section 9. Version Control Practice

Work must be performed on a branch from `main`. Commits must be logical units with descriptive messages. Distinct engineering steps must not be squashed together. History must not be rewritten on a shared branch. Engineering history must not be deleted.

---

# Section 10. AI Agent Operations

AI agents comply with the AI Agent Contract, `CLAUDE.md`, `AGENTS.md` and `AI_BOOTSTRAP.yaml`.

An agent verifies the repository state and the constitutional integrity lock before acting, respects the hierarchy of authority, avoids every prohibited action, records its decisions, and produces a handoff with every mandatory section. An agent that cannot complete a step records the gap rather than working around it.

---

# Section 11. Completion Criteria

Work is complete when:

- the stated objective is satisfied in full,
- alignment with parent documents is verified,
- every required file and reference exists,
- `make validate` and `make test` pass, or a documented limitation is accepted by a reviewer,
- documentation and engineering memory are updated,
- the handoff is complete and the pull request is open.

---

# Ratification

Engineering Playbook EP-001 is ratified as the mandatory operating playbook for IWOS engineering work.

It is effective on merge to `main` by an authorised human maintainer and remains in force until superseded by a formally ratified Engineering Playbook release.

---

**Document Status:** Ratified

**Version:** 1.0.0 (Genesis)

**Release:** EP-1.0
