# Testing Standard

**Document ID:** STD-TEST-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-07-31

## Purpose

This standard defines how IWOS work is validated so that specifications, schemas and implementation guidance remain reliable and verifiable.

## Scope

This standard applies to repository checks, schema validation, documentation validation, examples and implementation-facing acceptance criteria.

## Requirements

1. Every change must identify the validation performed.
2. Schema changes must include validation against representative valid and invalid examples when examples exist.
3. Documentation changes must be checked for structural completeness and internal consistency.
4. Tests must be deterministic and suitable for automated execution where practical.
5. Failures must be reported with enough detail for another engineer to reproduce them.
6. Skipped or unavailable checks must be documented with the reason.

## Test Categories

- **Structural checks:** validate file presence, required headings and metadata.
- **Schema checks:** validate YAML, JSON and formal schemas.
- **Consistency checks:** verify links, identifiers and authority references.
- **Example checks:** confirm examples match the specifications they demonstrate.

## Ratification

This standard is ratified as the minimum validation baseline for IWOS specification work.
