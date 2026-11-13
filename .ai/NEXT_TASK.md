# Next Task

**Document ID:** MEM-005  
**Version:** 1.0.0  
**Status:** Active  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-11-13

## Purpose

This document names the single recommended next task so that the next contributor, human or agent, starts without rediscovering context.

## Recommended Next Task

**Decide where IWOS Guard lives, then tag and launch.** Decision DEC-0009 records the question. The repository owner chooses one:

1. a dedicated repository for IWOS Guard before launch (recommended): its own README, its own version tags, its own constitution file, and the Action referenced by its own name; recorded as a decision record that supersedes ADR-0004;
2. launch from this repository under ADR-0004, with a tag scheme for the toolchain that does not collide with releases of the specification.

Then: tag the first release, enable branch protection, and publish the announcement built on `tools/iwos/CASE-STUDY.md`.

## Acceptance Criteria

- A decision record states where the toolchain lives, and ADR-0004 is accepted or superseded accordingly.
- A release tag exists that consumers can pin, and the quickstart references it.
- Branch protection requires the gate; a second Maintainer is named in `CODEOWNERS`.
- SPEC-ENGGOV-001 is ratified once its contracts name their final locations.

## After That

Ratify SPEC-ENGGOV-001, then build the first rule packs (change control for regulated software, ISO 42001 clauses, EU AI Act Annex IV documentation mapped to decision records) and extend the portal into the hosted, multi-repository view. Open an RFC on the specification order for the remaining components of the Architecture Baseline, beginning with the Enterprise Asset Registry and Knowledge Graph as AIP-0002 proposes. These are recommendations for human decision, not authorised tasks.

## Ratification

This document is an engineering memory record maintained under the AI Agent Contract. It carries no authority and is replaced whenever the recommended next task changes.
