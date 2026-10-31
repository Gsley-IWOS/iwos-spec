# Claude Onboarding Instructions

**Document ID:** AIO-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-10-31

## Purpose

This file is the first document an AI agent reads when it opens this repository. It states the mandatory reading order, the rules that bind every agent, and the actions an agent must never take. It is written for Claude and applies to every AI system that reads it as working context.

`AGENTS.md` defines the workflows an agent follows. `AI_BOOTSTRAP.yaml` is the machine-readable form of both. Where this file and the AI Agent Contract differ, the Contract governs.

## What This Repository Is

`iwos-spec` is the constitutional repository of the Intelligent Work Orchestration System. It holds ratified architecture, governance, standards and contracts. It is not an implementation repository. You are here to preserve and extend a body of law, not to write product code.

## Reading Order

The AI Agent Contract makes four documents mandatory: the Founding Charter, Project Genesis, the Architecture Baseline and the Engineering Constitution. This repository requires the fuller list below, in this order, before you change anything. Do not skim. The validator checks structure and references; a contradiction with these documents is caught by human review and blocks merge.

1. `README.md`
2. `engineering-charter/00_FOUNDING_CHARTER.md`
3. `engineering-charter/06_ENGINEERING_CONSTITUTION.md`
4. `engineering-charter/01_PROJECT_GENESIS.md`
5. `engineering-charter/02_ARCHITECTURE_BASELINE.md`
6. `engineering-charter/05_AI_AGENT_CONTRACT.yaml`
7. `engineering-charter/03_ENGINEERING_PLAYBOOK.md`
8. `engineering-charter/04_CODE_REVIEW_PLAYBOOK.md`
9. `AGENTS.md`
10. `.ai/CURRENT_STATE.md` and `.ai/NEXT_TASK.md`
11. The work package, decision record, proposal or issue that authorises your task.

Read the standards in `standards/` and the governance policies in `governance/` when your task touches the artefact families they govern.

## Repository Rules

1. **Work from written authority, not inference.** Every change cites the work package, Architecture Decision Record, Architecture Improvement Proposal or issue that authorises it. If no authority exists, open one; do not proceed on assumption.
2. **Verify before you act.** Run `make validate` before and after your change. The integrity check must pass before you start; if it fails, a protected document and the lock disagree and you must stop and report rather than regenerate the lock.
3. **Respect the hierarchy.** Article 1 of the Engineering Constitution orders every document. A lower document may clarify a higher one, never redefine it.
4. **Follow the templates.** New documents start from `templates/`. Every durable document carries Document ID, Version, Status, Authority, Parent Document, Last Updated, a Purpose section and a Ratification section.
5. **Use requirement language precisely.** **must**, **must not**, **should**, **should not**, **may**.
6. **Keep scope tight.** One authorising artefact, one coherent change. Unrelated work goes in another pull request.
7. **Leave memory better than you found it.** When your activity completes, update `CHANGELOG.md`, `.ai/CURRENT_STATE.md`, `.ai/ENGINEERING_STATE.yaml`, `.ai/KNOWLEDGE_GRAPH.yaml`, `.ai/DECISION_GRAPH.yaml` and `.ai/NEXT_TASK.md`.
8. **Hand off completely.** The pull request contains every section that Section 6 of the Code Review Playbook requires.
9. **Say what you did not do.** A skipped check, an unverifiable claim or an incomplete section is reported, never hidden.
10. **Prefer evidence over opinion.** Quote the document and line that supports a claim about this repository.

## Forbidden Actions

You must not:

- modify any protected document (`engineering-charter/*`, `standards/*-standard.md`, `governance/*.md`) or `.ai/CONSTITUTION_LOCK.yaml`, except when a human maintainer has explicitly directed the change under an accepted Architecture Improvement Proposal;
- invent architecture, components, engines, layers or contracts that the Architecture Baseline does not define;
- describe an unmerged document as ratified, accepted or approved;
- approve, merge or close a pull request, or resolve a human reviewer's comment on the human's behalf;
- delete, rewrite or squash engineering history on a shared branch;
- leave drafting markers, empty files, placeholder text or unverifiable claims in the repository;
- commit secrets, credentials or realistic-looking fake credentials;
- add product runtime code to this repository;
- skip tests or validation, or report checks as passed that did not run;
- bypass the decision process in `governance/decision-process.md` for any change it covers.

## When You Are Unsure

Stop. Record the question in the pull request under Outstanding Work, or open a Request for Comments using the issue form. An unanswered question is acceptable. An invented answer is not.

## Ratification

This document is ratified under the AI Agent Contract as the primary onboarding instruction for AI agents in the IWOS specification repository. It is effective on merge to `main` by an authorised human maintainer.
