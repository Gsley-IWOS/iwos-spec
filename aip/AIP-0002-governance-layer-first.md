# AIP-0002: Reframe Milestone M2 Toward the Governance Layer

**Document ID:** AIP-0002  
**Version:** 1.0.0  
**Status:** Review  
**Date:** 2026-11-09  
**Authority:** Constitutional Authority under GOV-002 (affects Project Genesis, a protected document)  
**Parent Documents:** governance/decision-process.md, engineering-charter/01_PROJECT_GENESIS.md, engineering-charter/02_ARCHITECTURE_BASELINE.md  
**Last Updated:** 2026-11-09

## Purpose

This proposal asks the Constitutional Authority to re-sequence milestone M2 of Project Genesis so that the first components specified and implemented are the Verification Engine and the Decision Ledger, applied to the domain of AI-assisted engineering, and to authorise the specification and reference toolchain that realise them. It defers the Intelligent Work Language, Compiler, Kernel and Bytecode to a later milestone. It changes no architecture: every component named in Architecture Baseline AB-1.0 remains constitutional.

## Summary

1. Re-order milestone M2 so that the Verification Engine and Decision Ledger are specified first, in the domain of engineering governance.
2. Authorise specification `SPEC-ENGGOV-001`, Engineering Governance Verification, as the first published specification of the programme.
3. Authorise a reference toolchain, provisionally named IWOS Guard, that implements the specification: a command-line interface, a continuous-integration action and a Model Context Protocol server.
4. Defer the Intelligent Work Language, Intelligent Work Compiler, Intelligent Work Kernel and Intelligent Kernel Bytecode to milestone M3 or later, without removing them from the baseline.

## Motivation

Since the Founding Charter was ratified, the frontier model providers have shipped managed agent runtimes, agent identity and protocol standards under neutral governance. The runtime, orchestration and intent layers of the Architecture Baseline now overlap directly with those offerings. The programme cannot expect to lead there.

Three gaps remain open and are growing: vendor-neutral accountability for what agents change, institutional memory of why decisions were taken, and mechanical enforcement of governance rather than advisory text. This repository already demonstrates all three. Its protected documents are digest-locked, its validator runs in continuous integration, its decisions are recorded with lifecycles, and ratification is the act of merge. The repository's own history records an AI agent opening a pull request that would have deleted most of the Founding Charter and Architecture Baseline; the integrity check in this repository would have failed that change in seconds.

The Founding Charter commits IWOS to becoming an open engineering standard and a governance framework for AI-native development. Specifying the Verification Engine and Decision Ledger first, in a domain where the programme has a working reference, serves that commitment and produces evidence for every later component.

## Specification

The following changes are authorised on acceptance.

1. In `engineering-charter/01_PROJECT_GENESIS.md`, Section 2, replace the M2 row of the milestone table with:

   > M2 Specification | Specify the Verification Engine and Decision Ledger of the Architecture Baseline in the domain of AI-assisted engineering, publish the first specification and ship its reference toolchain. | `SPEC-ENGGOV-001`, the IWOS Guard toolchain (command-line interface, continuous-integration action, Model Context Protocol server), conformance criteria. |

   and replace the M3 row with:

   > M3 Platform Specification | Specify the remaining constitutional components and engines, beginning with the Enterprise Asset Registry and Knowledge Graph, then the Intelligent Work Language, Compiler, Kernel and Bytecode. | Component and engine specifications, contracts, schemas, compliance and certification criteria. |

   Increment Project Genesis to version 1.1.0 and regenerate the constitutional integrity lock.

2. Authorise `architecture/engineering-governance/SPEC-ENGGOV-001.md`, currently Draft, to proceed to ratification by the Architecture Authority once its Draft is complete and validated.

3. Authorise work package EWP-0004 to build the reference toolchain under the Repository Standard's allowance for validation tooling, as decided in ADR-0004.

4. Record in `architecture/component-catalogue.md` the specification status `Authorised` for the Verification Engine and the Decision Ledger, naming this proposal.

## Impact

- `engineering-charter/01_PROJECT_GENESIS.md`: one table edited, version incremented. Constitutional change.
- `.ai/CONSTITUTION_LOCK.yaml`: regenerated.
- `architecture/component-catalogue.md`: two status cells change.
- `architecture/engineering-governance/`: new specification directory.
- `tools/iwos/`, `action.yml`, `iwos.yaml`: new reference toolchain under EWP-0004.
- No component, layer, engine or contract of the Architecture Baseline is added, removed or redefined.

## Compatibility

Additive and re-sequencing only. No published artefact changes meaning. MINOR increment to Project Genesis under the Versioning Policy. No migration.

## Alternatives

1. **Continue with the original M2 order, beginning with the Intelligent Work Language.** Rejected: it competes directly with the model providers' intent and runtime layers, where the programme has no advantage and no working reference.
2. **Build the toolchain without a proposal, as ordinary validation tooling.** Rejected: re-sequencing milestones is a change to Project Genesis, a protected document, and the Decision Process requires a proposal. Doing it silently would contradict the method the toolchain exists to enforce.
3. **Remove the deferred components from the baseline.** Rejected: that is an architectural change requiring an Architecture Baseline release, and nothing in the evidence shows the components are wrong, only that their time is later.

## Governance Outcome

Review. Awaiting decision by the Constitutional Authority. On acceptance the Constitutional Authority applies the Specification section to Project Genesis, regenerates the lock and sets this proposal to `Accepted` in the same change.

## Ratification

This proposal carries no authority until a holder of Constitutional Authority merges it with status `Accepted`. Its acceptance authorises exactly the change in the Specification section.
