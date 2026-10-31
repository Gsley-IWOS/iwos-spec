# Contributing to the IWOS Specification Repository

**Document ID:** ROOT-002  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-10-31

## Purpose

This document tells a human or AI contributor how to make a change to `iwos-spec` that will pass review. It summarises the Engineering Playbook and Code Review Playbook; where this summary and those documents differ, the playbooks govern.

## Scope

This document applies to every change to this repository: documents, schemas, templates, examples, validation tooling and repository configuration.

## Before You Start

1. Read `README.md`, then the mandatory documents listed in `engineering-charter/05_AI_AGENT_CONTRACT.yaml` under `mandatory_reading`.
2. Identify the authority for your change. Every change must be traceable to an approved work package in `work-packages/`, an accepted Architecture Decision Record, an accepted Architecture Improvement Proposal, or an issue opened with one of the forms in `.github/ISSUE_TEMPLATE/`.
3. Check `.ai/CURRENT_STATE.md` and `.ai/NEXT_TASK.md` for the current engineering state and the recommended next task.

## What You May Change

| Artefact family | Who may change it | Required authority |
| --- | --- | --- |
| `engineering-charter/` | Human maintainers only | Accepted AIP, then ratification by merge |
| `standards/*-standard.md` | Human maintainers only | Accepted AIP |
| `governance/*.md` | Human maintainers only | Accepted AIP |
| `architecture/`, `schemas/`, `templates/`, `examples/`, `adr/`, `aip/`, `tools/`, `.github/`, `.ai/`, root onboarding files | Any contributor, including AI agents | Approved work package or issue |

An AI agent may draft a change in a human-only family, but must mark the pull request as requiring human authorship review and must not describe the change as ratified.

## Making a Change

1. Branch from `main`.
2. Keep the change inside the scope of its authorising artefact. Do not bundle unrelated work.
3. Follow the Documentation Standard: every durable document states its title, version, status, authority, parent document, last-updated date, purpose and ratification state. This repository additionally requires a Document ID, a rule beyond the standard that the validator enforces. Use the templates in `templates/`.
4. Use requirement language consistently: **must**, **must not**, **should**, **should not**, **may**.
5. Run `make validate` and `make test`. Both must pass. If a check cannot run in your environment, say so in the pull request and explain why.
6. Update engineering memory when the change completes an engineering activity: `CHANGELOG.md`, `.ai/CURRENT_STATE.md`, `.ai/ENGINEERING_STATE.yaml`, `.ai/KNOWLEDGE_GRAPH.yaml`, `.ai/DECISION_GRAPH.yaml` and `.ai/NEXT_TASK.md`.
7. If you changed a protected constitutional document or standard under valid authority, run `make lock` and commit the regenerated `.ai/CONSTITUTION_LOCK.yaml` in the same change.
8. Commit in logical units with descriptive messages. Do not squash commits that represent distinct engineering steps.
9. Open a pull request using the template. Fill in every section of the handoff.

## Review and Merge

Review follows the eight gates in `engineering-charter/04_CODE_REVIEW_PLAYBOOK.md`. Continuous integration must be green. A pull request is merged only by an authorised human maintainer. Merge to `main` is the act of ratification for any document whose status is `Ratified` or `Accepted`.

## Prohibited

- Modifying the Founding Charter, Architecture Baseline, AI Agent Contract, Engineering Constitution or any standard without an accepted proposal.
- Introducing drafting markers, empty files or unverifiable claims.
- Committing secrets, credentials or realistic-looking fake credentials.
- Deleting engineering history. Superseded documents are marked superseded, not removed.
- Adding product runtime code to this repository.

## Ratification

This document is ratified under the Engineering Constitution as the contributor guide for the IWOS specification repository. It is effective on merge to `main` by an authorised human maintainer.
