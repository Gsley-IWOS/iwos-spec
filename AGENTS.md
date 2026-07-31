# IWOS Agent Operating Guide

**Purpose:** Define repository operating instructions for AI coding agents and automation agents.

**Authority:** engineering-charter/05_AI_AGENT_CONTRACT.yaml

**Version:** 1.0.0

**Status:** Ratified bootstrap baseline

**Parent document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml

---

## Purpose

This guide establishes the onboarding, engineering, review, and documentation workflow for agents working in `iwos-spec`.

## AI Onboarding Sequence

1. Confirm repository state and active branch.
2. Read the active work package completely.
3. Read the mandatory constitutional documents referenced by the work package.
4. Identify the documents and directories in scope.
5. Prepare a detailed implementation plan.
6. Execute only the approved scope.
7. Validate changed files.
8. Commit using the required logical commit structure.
9. Open a pull request for human review.

## Engineering Workflow

- Work from written authority, not inference.
- Preserve document hierarchy and authority metadata.
- Keep each change small enough to review.
- Separate repository bootstrap work, constitutional charter work, and AI-governance work when requested.
- Prefer explicit tables and numbered rules for governance content.
- Use stable names, versions, statuses, and parent-document references.

## Review Workflow

Every agent-authored change must be self-reviewed before handoff. The review must verify:

- Scope matches the work package.
- Required documents exist.
- Required directories exist.
- Markdown documents contain title, purpose, authority, version, status, parent document, sections, and ratification.
- YAML files parse successfully.
- No unresolved draft markers or incomplete-action statements are present.
- Pull request summary identifies human-review items.

## Documentation Workflow

Documentation changes must be written as durable governance assets. The preferred structure is:

1. Title.
2. Required metadata.
3. Purpose.
4. Normative sections.
5. Operating rules or responsibilities.
6. Ratification.

## Ratification

This document is ratified as part of the Sprint 0 repository bootstrap. Amendments require review under the AI Agent Contract and Engineering Constitution.
