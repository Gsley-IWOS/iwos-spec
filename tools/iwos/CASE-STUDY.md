# Case Study: The Pull Request That Replaced the Constitution

**Document ID:** TOOL-003  
**Version:** 1.1.0  
**Status:** Active  
**Authority:** EWP-0005  
**Parent Documents:** tools/iwos/README.md, work-packages/EWP-0005.md, adr/ADR-0005-agent-attribution-by-disclosure.md  
**Last Updated:** 2026-11-14

## Purpose

This is the incident that IWOS Guard exists to prevent, told from the history of this repository. Every fact below can be checked against that history, and the gate report can be reproduced with one command.

## What Happened

On 31 July 2026 this repository held three ratified constitutional documents: the Founding Charter, the Architecture Baseline and the AI Agent Contract. A work package, EWP-0001, asked an engineering team to bootstrap the rest of the repository. Under the heading "Create" it listed every charter file, including the three that already existed.

An AI coding agent took the work package and opened pull request 1 the same day. It did what the list said. It created the missing files, and it replaced the three ratified ones.

| Document | Lines before | Lines added | Lines removed |
| --- | --- | --- | --- |
| Founding Charter | 433 | 22 | 413 |
| Architecture Baseline | 658 | 21 | 641 |
| AI Agent Contract | 213 | 55 | 212 |

The 433-line Founding Charter became a 42-line summary. The seven architectural layers, the constitutional components and the nine intelligence engines of the baseline were gone. In all, 1,266 lines of ratified text were removed.

The pull request description said the change added the engineering charter set. It did not say that ratified documents had been rewritten. Its testing section reported that YAML parsed and that no drafting markers were present, both true.

The commit carried the repository owner's name. Nothing in the commit said an agent had written it. The only signs were a task link at the foot of the description and a label.

The pull request would have merged without conflict. It stayed open for 92 days. It was closed, unmerged, on 31 October 2026, after a second agent reading the repository cold reported what it contained.

## Why It Matters

Nobody was careless. The work package was ambiguous, the agent followed it, and the checks it ran passed. The failure is structural: the repository had rules about who may change the constitution, and nothing that could tell a change to the constitution from any other change. Instructions in `AGENTS.md` would not have helped, because the agent was following instructions.

Three things were missing, and each is one rule in a constitution file:

1. A way to say which documents are protected.
2. A check that fails when a protected document changes without a cited, accepted proposal.
3. A record, kept with the documents, of what they contained when they were ratified.

## The Replay

The repository now has a constitution. Running the gate over the same revision range, with the same description and label, gives this report. The base of that pull request predates the constitution, so the gate applies the constitution of the checkout it runs in and says so in the report (ADR-0007).

```bash
git fetch origin pull/1/head
PR_BODY='Bootstrap IWOS specification repository. Added the full engineering charter set.

[Codex Task](https://chatgpt.com/codex/cloud/tasks/task_e_6a6d141168f083318c7cb88ce34d63ef)' \
iwos gate --base c912ed32f308 --head 92fa42e5458a --body-env PR_BODY --label codex
```

```text
## IWOS gate report: FAIL

Range `c912ed32f308..92fa42e5458a` · 22 file(s) changed · 1 commit(s) · report v1.2.0

The base revision holds no valid constitution: judged against the constitution in the working tree (on a pull request, the one the change proposes).

### Protected artefacts

- `engineering-charter/00_FOUNDING_CHARTER.md`
- `engineering-charter/01_PROJECT_GENESIS.md`
- `engineering-charter/02_ARCHITECTURE_BASELINE.md`
- `engineering-charter/03_ENGINEERING_PLAYBOOK.md`
- `engineering-charter/04_CODE_REVIEW_PLAYBOOK.md`
- `engineering-charter/05_AI_AGENT_CONTRACT.yaml`
- `engineering-charter/06_ENGINEERING_CONSTITUTION.md`
- `engineering-charter/Repository bootstrap (README.md, CLAUDE.md, AGENTS.md, AI_BOOTSTRAP.yaml)`

Proposal citation: none · lock regenerated: no

### Control files

None changed.

### Architecture

- `architecture/.gitkeep`

Decision citation: none

### Authority citations

Traceability: none found

### Agents

Agents disclosed: OpenAI Codex (pull request description), codex (pull request label)
Human commit authors: chudeway89

| Commit | Author | Subject | Trailers |
| --- | --- | --- | --- |
| `92fa42e5` | chudeway89 | Add AI governance onboarding |  |

### Result

- FAIL `IWOS-G001`: 8 protected artefact(s) changed without an accepted-proposal citation matching AIP-\d{4}
- FAIL `IWOS-G002`: protected artefact(s) changed but the lock .ai/CONSTITUTION_LOCK.yaml was not regenerated in the same change
- FAIL `IWOS-G003`: 1 architecture file(s) changed without a decision-record citation matching ADR-\d{4}
- FAIL `IWOS-G004`: no authority citation found in the pull request body or commit messages (traceability required)
- warning `IWOS-W005`: the base revision holds no valid constitution, so this change was judged against the constitution in the working tree, which on a pull request is the one the change proposes; review the constitution file by hand
- warning `IWOS-W003`: an agent is disclosed in the pull request description or labels, but every commit carries a human identity; attribution here rests on disclosure alone
```

The command exits with status 1. On a pull request, the check is red before a reviewer opens the diff.

## What the Gate Did Not Know

The report says "agents disclosed", not "agents detected". The agent in this incident committed under a human identity. Had the description and label said nothing, the report would have named no agent, and it would have said that this proves nothing. ADR-0005 records why: repository data cannot prove an agent was absent. The blocking rules do not depend on the answer. A protected document changed without authority fails whoever changed it.

The gate also cannot stop a merge by itself. The hosting platform must require the check. And the lock can be regenerated by anyone with a checkout, so the lock's diff is reviewed by a human like any other diff.

## Ratification

This document is a factual record maintained under EWP-0005. It carries no authority. Where it and the repository history disagree, the history is correct.
