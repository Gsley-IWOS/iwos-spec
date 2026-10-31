# Current State

**Document ID:** MEM-004  
**Version:** 1.0.0  
**Status:** Active  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-10-31

## Purpose

This document states the current state of the IWOS specification repository in prose for a reader who is about to start work. The machine-readable form is `ENGINEERING_STATE.yaml`; where the two disagree, the YAML file is corrected to match the repository and this file is corrected to match the YAML.

## Where the Repository Stands

Milestone M0 Constitutional Foundation has every output EWP-0001 required: the seven engineering-charter documents, the root onboarding files, the engineering memory and the directory structure. They are in review and become ratified when the founding release is merged.

Milestone M1 Governance and Standards is in progress. The seven standards are ratified. Governance policies, the first Architecture Decision Records, the first Architecture Improvement Proposal, templates, schemas, examples, the validator and continuous integration exist and are awaiting human review under work packages EWP-0002 and EWP-0003.

Milestones M2 Specification and M3 Reference Implementation Readiness have not started. No component or engine of the Architecture Baseline has a published specification yet; `architecture/component-catalogue.md` records this.

## Protected Documents

The Founding Charter, Architecture Baseline and AI Agent Contract are unchanged from their ratified versions. The constitutional integrity lock covers every file in `engineering-charter/`, every standard matching `standards/*-standard.md` and every governance policy matching `governance/*.md`.

## Open Risks

See `current_risks` in `ENGINEERING_STATE.yaml`. In summary: EWP-0002 and EWP-0003 are proposed, not approved; ADR-0001 to ADR-0003 are proposed and AIP-0001 is in review, not accepted; pull requests 1 to 4 overlap with the build-out and pull request 1 must not be merged; no CODEOWNERS file exists yet.

## Validation State

`make validate` and `make test` pass on this revision. Continuous integration runs the same checks on every pull request.

## Ratification

This document is an engineering memory record maintained under the AI Agent Contract. It carries no authority and is updated at the completion of every engineering activity.
