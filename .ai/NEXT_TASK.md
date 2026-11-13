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

**Owner decisions for launch.** The engineering for launch is in review under EWP-0005. What remains is the repository owner's:

1. confirm the product name (IWOS Guard is provisional) and tag `v0.1.0` so consumers can pin `Gsley-IWOS/iwos-spec@v0.1.0`;
2. confirm the repository is public, and enable branch protection on `main`: require the `validate` and `IWOS Guard composite action` checks and review from code owners;
3. publish the announcement built on `tools/iwos/CASE-STUDY.md`;
4. decide the open items: EWP-0005, EWP-0002 and EWP-0003 (Proposed); ADR-0001 to ADR-0005 (Proposed); AIP-0001 (Review); and ratify SPEC-ENGGOV-001.

## Acceptance Criteria

- A release tag `v0.1.0` exists and the README quickstart references it.
- Branch protection requires the gate and code-owner review; a second Maintainer is named in `CODEOWNERS`.
- The launch post is published and its traction is measured by repositories running the Action, not stars.
- Registers and `ENGINEERING_STATE.yaml` reflect every decision taken.

## After That

Ratify SPEC-ENGGOV-001, then build the first rule packs (change control for regulated software, ISO 42001 clauses, EU AI Act Annex IV documentation mapped to decision records) and extend the portal into the hosted, multi-repository view. Open an RFC on the specification order for the remaining components of the Architecture Baseline, beginning with the Enterprise Asset Registry and Knowledge Graph as AIP-0002 proposes. These are recommendations for human decision, not authorised tasks.

## Ratification

This document is an engineering memory record maintained under the AI Agent Contract. It carries no authority and is replaced whenever the recommended next task changes.
