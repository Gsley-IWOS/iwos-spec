# Next Task

**Document ID:** MEM-005  
**Version:** 1.0.0  
**Status:** Active  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-10-31

## Purpose

This document names the single recommended next task so that the next contributor, human or agent, starts without rediscovering context.

## Recommended Next Task

**Ratify the foundation.** A human maintainer reviews the build-out pull request against the eight review gates and decides:

1. whether EWP-0002 and EWP-0003 are approved as written, amended or rejected;
2. whether ADR-0001 to ADR-0003 are accepted and whether AIP-0001 (registration of additional identifier families) is accepted;
3. whether pull requests 1 to 4 are closed as superseded.

## Acceptance Criteria

- The pull request is merged to `main` by an authorised human maintainer, or returned with findings labelled by review gate.
- `work-packages/README.md`, `aip/README.md` and `ENGINEERING_STATE.yaml` reflect the decisions taken.
- If AIP-0001 is rejected, a follow-up work package re-identifies the affected documents.

## After That

The first M2 task is to open a Request for Comments proposing the specification order for the constitutional components of the Architecture Baseline, starting with the Intelligent Work Language because every other component consumes its output. This is a recommendation for human decision, not an authorised task.

## Ratification

This document is an engineering memory record maintained under the AI Agent Contract. It carries no authority and is replaced whenever the recommended next task changes.
