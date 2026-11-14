# Next Task

**Document ID:** MEM-005  
**Version:** 1.0.0  
**Status:** Active  
**Authority:** AAC-001 AI Agent Contract  
**Parent Document:** engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-11-14

## Purpose

This document names the single recommended next task so that the next contributor, human or agent, starts without rediscovering context.

## Recommended Next Task

**Create the `iwos-guard` repository, move the toolchain into it, tag it and launch.** ADR-0006 records the decision. The first step is the owner's: create an empty public repository named `iwos-guard` in the `Gsley-IWOS` organisation. The hosting platform refuses that act to automation.

Then, under a new work package:

1. move `tools/iwos/` and `action.yml` to the root of the dedicated repository, with its own README built on the case study, its own `iwos.yaml`, lock, security policy, code owners and continuous integration that runs the action from the working tree;
2. tag the first release there;
3. in this repository, replace `uses: ./` with a pinned commit of the dedicated repository and remove `tools/iwos/` and `action.yml` in the same change;
4. keep `schemas/iwos-config.schema.json` here as the canonical contract.

Three settings on the hosting platform are also the owner's, and none needs the move: enable private vulnerability reporting (Settings, then the security section), require the two checks of the `validate` workflow by name in branch protection for `main`, and leave "Require review from Code Owners" off until a second Maintainer is named, because every pull request is opened under the owner's account.

## Acceptance Criteria

- `Gsley-IWOS/iwos-guard` exists, passes its own gate and holds a release tag that consumers can pin.
- This repository consumes that release by commit and no longer contains the toolchain.
- The **Report a vulnerability** button is shown on this repository and on the dedicated one.
- Branch protection requires the gate.

## After That

Ratify SPEC-ENGGOV-001, then build the first rule packs (change control for regulated software, ISO 42001 clauses, EU AI Act Annex IV documentation mapped to decision records) and extend the portal into the hosted, multi-repository view. Open an RFC on the specification order for the remaining components of the Architecture Baseline, beginning with the Enterprise Asset Registry and Knowledge Graph as AIP-0002 proposes. These are recommendations for human decision, not authorised tasks.

## Ratification

This document is an engineering memory record maintained under the AI Agent Contract. It carries no authority and is replaced whenever the recommended next task changes.
