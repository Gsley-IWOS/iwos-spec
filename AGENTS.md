# IWOS Agent Operating Guide

**Document ID:** AIO-002  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-10-31

## Purpose

This guide defines the four workflows every AI coding agent or automation agent follows in `iwos-spec`: onboarding, engineering, review and documentation. It applies to any agent regardless of vendor. `CLAUDE.md` states the rules; this guide states the procedure.

## Onboarding Sequence

Complete every step before changing a file. These steps are the first seven steps of `execution_sequence` in the AI Agent Contract, expanded; the Engineering Playbook covers all thirteen.

| Step | Action | Done when |
| --- | --- | --- |
| 1 | Confirm repository, branch and clean working tree with `git status`. | You know which branch you are on and that it is not `main`. |
| 2 | Read the mandatory documents in the order given in `CLAUDE.md`. | You can state the mission, the hierarchy of authority and the prohibited actions without looking. |
| 3 | Run `make validate`. | Every check passes on the untouched repository. If the integrity check fails, a protected document and the lock disagree: stop and report; never regenerate the lock to make it pass. |
| 4 | Read `.ai/CURRENT_STATE.md`, `.ai/ENGINEERING_STATE.yaml` and `.ai/NEXT_TASK.md`. | You know the current sprint, the open risks and the recommended next task. |
| 5 | Read the authorising artefact for your task in full. | You can list its outputs, validation criteria and completion evidence. |
| 6 | Confirm every input exists and every dependency is satisfied. | Nothing you need is missing or unratified. |
| 7 | Write the plan: artefacts to create or change, authority for each, checks to run. | The plan fits inside the authorised scope. |

## Engineering Workflow

1. Create or change only the artefacts in the plan. Start new documents from `templates/`.
2. Keep each document's metadata consistent: Document ID unique within its family, Version under `governance/versioning-policy.md`, Status accurate, Authority and Parent Document resolvable, Last Updated set to the date of the change.
3. When you add or change a schema, add or change valid and invalid examples under `examples/` and bind the schema in `schemas/bindings.yaml`.
4. When you add a governed YAML artefact, bind it to its schema in `schemas/bindings.yaml`.
5. Run `make validate` and `make test`. Fix every failure. Do not suppress, exempt or weaken a check to make it pass; if a check is wrong, change it under its own authority and say so.
6. Record every decision that constrains future work: as an Architecture Decision Record if it is architectural, otherwise in `.ai/DECISION_GRAPH.yaml`.
7. Update engineering memory and `CHANGELOG.md` as the last step of the change.
8. Commit in logical units. A commit message states what changed and under which authority.

## Review Workflow

Before handoff, self-review against the eight gates of the Code Review Playbook and record the result in the pull request.

| Gate | Self-review question |
| --- | --- |
| Scope | Does the diff contain only what the authorising artefact permits? |
| Authority | Did I touch a protected document? If so, is there an accepted proposal and an updated lock? |
| Architecture | Did I describe only what the Architecture Baseline defines? |
| Quality | Are there drafting markers, empty files, duplicated definitions or unverifiable claims? |
| Verification | Did `make validate` and `make test` run and pass? Is the output in the handoff? |
| Documentation | Does every new or changed document meet the Documentation Standard and its template? |
| Traceability | Are decisions, risks and memory updates present? |
| Human review | Have I requested review from a human maintainer and avoided approving or merging? |

When you review another contributor's change, post findings labelled by gate, distinguish blocking findings from suggestions, and do not approve or merge.

## Documentation Workflow

1. Choose the template for the artefact family.
2. Write the metadata block first, then Purpose, then Scope and Authority where the template requires them, then the body, then Ratification.
3. Define every abbreviation on first use unless it is listed in `architecture/glossary.md`.
4. Link to canonical definitions rather than restating them. If you summarise, say that it is a summary.
5. Mark anything that is not ratified as Proposed, Draft or Illustrative.
6. Run `make validate`. The validator enforces steps 2 and 6; steps 3, 4 and 5 are review gates.

## Handoff

The pull request uses `.github/pull_request_template.md` and contains every section that Section 6 of the Code Review Playbook requires, in order. A handoff with a missing section is incomplete.

## Ratification

This guide is ratified under the AI Agent Contract as the operating procedure for AI agents in the IWOS specification repository. It is effective on merge to `main` by an authorised human maintainer.
