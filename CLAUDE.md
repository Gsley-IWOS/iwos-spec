# CLAUDE Onboarding Instructions

**Purpose:** Provide mandatory onboarding instructions for Claude and compatible AI assistants working in the IWOS specification repository.

**Authority:** engineering-charter/05_AI_AGENT_CONTRACT.yaml

**Version:** 1.0.0

**Status:** Ratified bootstrap baseline

**Parent document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml

---

## Purpose

This file defines the required operating rules for AI assistants in `iwos-spec`. It is designed for Claude-style assistants, but its instructions apply to any AI system that reads it as working context.

## Mandatory Reading Order

Before making repository changes, an AI assistant must read these documents in order:

1. `README.md`.
2. `engineering-charter/00_FOUNDING_CHARTER.md`.
3. `engineering-charter/01_PROJECT_GENESIS.md`.
4. `engineering-charter/02_ARCHITECTURE_BASELINE.md`.
5. `engineering-charter/03_ENGINEERING_PLAYBOOK.md`.
6. `engineering-charter/04_CODE_REVIEW_PLAYBOOK.md`.
7. `engineering-charter/05_AI_AGENT_CONTRACT.yaml`.
8. `engineering-charter/06_ENGINEERING_CONSTITUTION.md`.
9. The active work package or issue.

## Repository Rules

- Treat `iwos-spec` as a constitutional specification repository.
- Preserve the documented authority chain.
- Write professional Markdown and valid YAML.
- Make changes that are traceable to an approved work package, issue, ADR, or AIP.
- Keep architecture changes separate from implementation examples and process documentation.
- Validate affected YAML before completion.
- Summarize changes with affected files, decisions, verification, and review needs.

## Forbidden Actions

AI assistants must not:

- Redefine approved architecture without a governed ADR or AIP.
- Add unresolved draft markers or incomplete-action statements.
- Introduce implementation runtime code into this specification repository unless an approved work package explicitly requires it.
- Treat examples as normative architecture.
- Bypass human review for constitutional, governance, or architecture changes.
- Merge pull requests on behalf of maintainers.

## Ratification

This document is ratified as part of the Sprint 0 repository bootstrap. Changes require review against the AI Agent Contract and Engineering Constitution.
