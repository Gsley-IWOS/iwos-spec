# Next Task

**Document ID:** MEM-005  
**Version:** 1.0.0  
**Status:** Active  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-11-09

## Purpose

This document names the single recommended next task so that the next contributor, human or agent, starts without rediscovering context.

## Recommended Next Task

**Decide AIP-0002 and launch IWOS Guard.** The Constitutional Authority reviews the pivot pull request and decides:

1. whether AIP-0002 is accepted; on acceptance, apply its Specification to Project Genesis, regenerate the lock and set the proposal to Accepted in the same change;
2. whether EWP-0004 is approved and ADR-0004 accepted, and whether the earlier open items (EWP-0002, EWP-0003, ADR-0001 to ADR-0003, AIP-0001) are approved or accepted;
3. whether to name the toolchain, tag `v0.1.0` so the Action can be pinned, and publish the launch: the pull request 1 story, a Show HN, and plugins for the agent ecosystems.

## Acceptance Criteria

- The pull request is merged to `main` by an authorised human maintainer, or returned with findings labelled by review gate.
- `work-packages/README.md`, `aip/README.md`, `adr/README.md` and `ENGINEERING_STATE.yaml` reflect the decisions taken.
- If AIP-0002 is accepted, Project Genesis 1.1.0 is on `main` with a regenerated lock and SPEC-ENGGOV-001 proceeds to ratification.
- A release tag exists so consumers can reference `Gsley-IWOS/iwos-spec@v0.1.0`.

## After That

Ratify SPEC-ENGGOV-001, then build the first rule packs (change control for regulated software, ISO 42001 clauses, EU AI Act Annex IV documentation mapped to decision records) and extend the portal into the hosted, multi-repository view. Open an RFC on the specification order for the remaining components of the Architecture Baseline, beginning with the Enterprise Asset Registry and Knowledge Graph as AIP-0002 proposes. These are recommendations for human decision, not authorised tasks.

## Ratification

This document is an engineering memory record maintained under the AI Agent Contract. It carries no authority and is replaced whenever the recommended next task changes.
