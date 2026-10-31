# Component Catalogue

**Document ID:** AS-003  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-ARCH-001 Architecture Standard  
**Parent Document:** engineering-charter/02_ARCHITECTURE_BASELINE.md  
**Last Updated:** 2026-10-31

## Purpose

This catalogue lists every constitutional component and intelligence engine that Architecture Baseline AB-1.0 requires of a compliant implementation, with its purpose as the baseline states it and the status of its specification. It is the register against which milestone M2 Specification is tracked.

This document is a summary. Purposes are quoted or condensed from the baseline and add nothing to it. The baseline does not assign components or engines to its seven layers, so this catalogue does not either; any such assignment is architecture and requires the Decision Process.

## Constitutional Components

| Component | Abbreviation | Purpose in the baseline | Specification |
| --- | --- | --- | --- |
| Intelligent Work Language | IWL | Intent representation. | Not yet authorised |
| Intelligent Work Compiler | IWC | Transforms structured intent into executable representations. | Not yet authorised |
| Intelligent Work Kernel | IWK | Runtime execution engine; coordinates workflows, schedules execution, maintains context. | Not yet authorised |
| Intelligent Kernel Bytecode | IKB | Portable execution representation independent of implementation language. | Not yet authorised |
| Enterprise Asset Registry | EAR | Canonical registry of systems, people, processes, knowledge, policies and resources. | Not yet authorised |
| Decision Ledger | | Immutable record of significant decisions; supports explainability and auditing. | Not yet authorised |
| Knowledge Graph | | Organisational knowledge as connected entities; supports reasoning, discovery and context reconstruction. | Not yet authorised |
| Mission Graph | | Strategic objectives and execution dependencies. | Not yet authorised |
| Digital Twin | | Executable representation of organisational reality. | Not yet authorised |

## Core Intelligence Engines

The baseline requires each engine to expose well-defined contracts.

| Engine | Specification |
| --- | --- |
| Strategy Intelligence Engine | Not yet authorised |
| Decision Intelligence Engine | Not yet authorised |
| Verification Engine | Not yet authorised |
| Knowledge Intelligence Engine | Not yet authorised |
| Execution Intelligence Engine | Not yet authorised |
| Evolution Intelligence Engine | Not yet authorised |
| Risk Intelligence Engine | Not yet authorised |
| Communication Intelligence Engine | Not yet authorised |
| Measurement Intelligence Engine | Not yet authorised |

## Specification Status Values

| Status | Meaning |
| --- | --- |
| Not yet authorised | No accepted Architecture Improvement Proposal authorises a specification. |
| Authorised | An accepted proposal authorises the specification; it names the proposal. |
| Draft | A specification exists with a pre-release version. |
| Published | A specification is ratified; it names its path and version. |
| Superseded | A later published specification replaces it. |

## Future Capabilities

The Founding Charter lists further capabilities IWOS will include: Enterprise SDKs, a Marketplace and a Developer Platform. They are programme intent, not architecture, until the Architecture Baseline defines them. They are therefore not catalogued here.

## Ratification

This catalogue is ratified under the Architecture Standard. It is effective on merge to `main` by an authorised human maintainer.
