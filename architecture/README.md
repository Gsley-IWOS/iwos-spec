# Architecture Reference

**Document ID:** AS-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-ARCH-001 Architecture Standard  
**Parent Documents:** engineering-charter/02_ARCHITECTURE_BASELINE.md, standards/architecture-standard.md  
**Last Updated:** 2026-10-31

## Purpose

This directory holds architecture reference material derived from Architecture Baseline AB-1.0: an index, a glossary and a catalogue of the constitutional components and engines. These documents describe and index the baseline so that readers and tooling can navigate it. They do not extend it.

## Authority

Architecture Baseline AB-1.0 is the sole normative source of IWOS architecture. Every document here is a summary of, or an index into, the baseline. Where a document here and the baseline disagree, the baseline is correct and the document here is corrected.

New architecture enters the baseline only through the Decision Process in `governance/decision-process.md`. Component and engine specifications authorised under milestone M2 are published at the location the authorising Architecture Improvement Proposal names; this directory is the default.

## Contents

| Document | ID | Content |
| --- | --- | --- |
| [Glossary](glossary.md) | AS-002 | Definitions of IWOS terms and abbreviations used across the repository. |
| [Component Catalogue](component-catalogue.md) | AS-003 | Every constitutional component and intelligence engine named in the baseline, with purpose and specification status. |

## The Seven Layers

The Architecture Baseline divides IWOS into seven layers. The table restates them for navigation; the baseline defines them.

| Layer | Name | Responsibility in the baseline |
| --- | --- | --- |
| 1 | Mission | Defines purpose. |
| 2 | Governance | Defines authority: standards, policies, contracts. |
| 3 | Knowledge | Stores institutional knowledge: architecture, decisions, specifications, engineering memory. |
| 4 | Intelligence | Reasoning, planning, verification, optimisation, learning. |
| 5 | Execution | Transforms plans into executable workflows; coordinates engines; schedules and tracks work. |
| 6 | Integration | Connects enterprise systems: APIs, SDKs, adapters, plugins. |
| 7 | Experience | Interfaces: CLI, console, developer tools, dashboards. |

The baseline does not assign components or engines to layers and this directory does not either.

## Ratification

This index is ratified under the Architecture Standard. It is effective on merge to `main` by an authorised human maintainer.
