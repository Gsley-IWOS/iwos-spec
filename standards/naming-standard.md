# Naming Standard

**Document ID:** STD-NAME-001  
**Version:** 1.1.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-11-13

## Purpose

This standard defines naming conventions for IWOS repository artifacts so that identifiers remain predictable, searchable and stable.

## Scope

This standard applies to directories, files, document identifiers, schema identifiers, examples, ADRs, AIPs and templates.

## Requirements

1. Directory and file names must be descriptive and stable.
2. Markdown standard files must use lowercase kebab-case names ending in `-standard.md`.
3. Constitutional engineering-charter files may use numbered uppercase names when preserving charter ordering.
4. Document identifiers must be unique within their artifact family.
5. Identifiers must not be renamed after ratification unless a migration note preserves traceability.
6. Abbreviations must be defined before use unless they are established IWOS identifiers.

## Identifier Families

| Family | Pattern | Artefacts |
| --- | --- | --- |
| Founding Charter | `FC-###` | `engineering-charter/00_FOUNDING_CHARTER.md` |
| Project Genesis | `PG-###` | `engineering-charter/01_PROJECT_GENESIS.md` |
| Architecture Baseline | `AB-###` | `engineering-charter/02_ARCHITECTURE_BASELINE.md` |
| Engineering Playbook | `EP-###` | `engineering-charter/03_ENGINEERING_PLAYBOOK.md` |
| Code Review Playbook | `CRP-###` | `engineering-charter/04_CODE_REVIEW_PLAYBOOK.md` |
| AI Agent Contract | `AAC-###` | `engineering-charter/05_AI_AGENT_CONTRACT.yaml` |
| Engineering Constitution | `EC-###` | `engineering-charter/06_ENGINEERING_CONSTITUTION.md` |
| Standard | `STD-<AREA>-###` | `standards/*-standard.md` |
| Governance policy | `GOV-###` | `governance/*.md`, `governance/rfc/README.md` |
| Request for Comments | `RFC-####` | `governance/rfc/RFC-####.md` |
| Architecture Improvement Proposal | `AIP-####` | `aip/AIP-####-*.md` |
| Architecture Decision Record | `ADR-####` | `adr/ADR-####-*.md` |
| Architecture reference | `AS-###` | `architecture/*.md` |
| Specification | `SPEC-<COMPONENT>-###` | Component and engine specifications published under milestone M2 |
| Schema | `SCH-###` | `schemas/*.schema.json`, `schemas/bindings.yaml` |
| Template | `TPL-###` | `templates/*.md` |
| Example register | `EX-###` | `examples/README.md` |
| Engineering Work Package | `EWP-####` | `work-packages/EWP-####.md` |
| Root document | `ROOT-###` | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md` |
| AI onboarding | `AIO-###` | `CLAUDE.md`, `AGENTS.md`, `AI_BOOTSTRAP.yaml` |
| Engineering memory | `MEM-###` | `.ai/*` |
| Tooling | `TOOL-###` | `tools/*/README.md` |

A register or index document for a family uses the family prefix with the suffix `-INDEX` in place of a number (`ADR-INDEX`, `AIP-INDEX`, `EWP-INDEX`, `STD-INDEX`).

## Ratification

This standard is ratified as the naming baseline for IWOS specification artifacts.
