# Naming Standard

**Document ID:** STD-NAME-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-07-31

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

- Founding Charter: `FC-###`
- Architecture Baseline: `AB-###`
- Standard: `STD-<AREA>-###`
- Engineering Work Package: `EWP-####`
- Architecture Decision Record: `ADR-####`
- Architecture Improvement Proposal: `AIP-####`

## Ratification

This standard is ratified as the naming baseline for IWOS specification artifacts.
