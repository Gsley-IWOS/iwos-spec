# Current State

**Document ID:** MEM-004  
**Version:** 1.0.0  
**Status:** Active  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-11-13

## Purpose

This document states the current state of the IWOS specification repository in prose for a reader who is about to start work. The machine-readable form is `ENGINEERING_STATE.yaml`; where the two disagree, the YAML file is corrected to match the repository and this file is corrected to match the YAML.

## Where the Repository Stands

Milestone M0 Constitutional Foundation has every output EWP-0001 required: the seven engineering-charter documents, the root onboarding files, the engineering memory and the directory structure. They are in review and become ratified when the founding release is merged.

Milestone M1 Governance and Standards is in progress. The seven standards are ratified. Governance policies, the first Architecture Decision Records, the first Architecture Improvement Proposal, templates, schemas, examples, the validator and continuous integration exist and are awaiting human review under work packages EWP-0002 and EWP-0003.

The founding release was merged on 2026-10-31 (pull request 6). On 2026-11-09 the repository owner accepted a strategic pivot: specify and ship the Verification Engine and Decision Ledger first, in the domain of AI-assisted engineering. The pivot was proposed as AIP-0002 because it re-sequences Project Genesis, a protected document, and was accepted by the Constitutional Authority on 2026-11-10: Project Genesis is at version 1.1.0 and milestone M2 is in progress. Its first specification, SPEC-ENGGOV-001, is a Draft awaiting ratification by the Architecture Authority, and its reference toolchain, IWOS Guard, is built under EWP-0004 (Approved) and runs against this repository on every pull request. No component has a ratified specification yet; `architecture/component-catalogue.md` records this.

On 2026-11-13 the repository owner confirmed the product name IWOS Guard, approved EWP-0002, EWP-0003 and EWP-0005, accepted ADR-0001, ADR-0002, ADR-0003 and ADR-0005, and accepted AIP-0001, which amended the Naming Standard to version 1.1.0. Launch readiness was delivered under EWP-0005. Replaying pull request 1 through the gate produced the case study in `tools/iwos/CASE-STUDY.md` and showed that the agent had committed under the owner's identity, which led to ADR-0005: attribution rests on disclosure and reports print no addresses. `.github/CODEOWNERS` now names the owner for protected paths, continuous integration runs the composite action from the working tree, and `.mcp.json` registers the authority interface for agents working here.

## Protected Documents

The Founding Charter, Architecture Baseline and AI Agent Contract are unchanged from their ratified versions. Project Genesis was amended once, to 1.1.0, under AIP-0002, and the Naming Standard once, to 1.1.0, under AIP-0001. The constitutional integrity lock covers every file in `engineering-charter/`, every standard matching `standards/*-standard.md` and every governance policy matching `governance/*.md`.

## Open Risks

See `current_risks` in `ENGINEERING_STATE.yaml`. In summary: ADR-0004 and the first release tag are held until the home of IWOS Guard is decided (DEC-0009); SPEC-ENGGOV-001 is a Draft; branch protection does not yet require the gate; agent attribution rests on disclosure; IWOS Guard enters a field where GitHub Spec Kit and AGENTS.md already have adoption; pull requests 1 to 4 overlap with the build-out and pull request 1 must not be merged; no CODEOWNERS file exists yet.

## Validation State

`make validate`, `make test` and `make guard` pass on this revision. Continuous integration runs the same checks on every pull request.

## Ratification

This document is an engineering memory record maintained under the AI Agent Contract. It carries no authority and is updated at the completion of every engineering activity.
