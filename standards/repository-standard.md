# Repository Standard

**Document ID:** STD-REPO-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-07-31

## Purpose

This standard defines how the IWOS specification repository is organized and maintained as the constitutional source of truth for IWOS.

## Scope

This standard applies to repository layout, artifact ownership, change hygiene, review expectations and relationship to implementation repositories.

## Requirements

1. The specification repository must remain the canonical source for ratified IWOS governance, architecture and standards.
2. Repository structure must separate governance, architecture, standards, schemas, templates, examples, ADRs and AIPs.
3. Implementation-specific code must not be introduced into the specification repository unless explicitly required for validation tooling.
4. Each committed change must be coherent, reviewable and associated with an engineering objective.
5. Repository metadata and onboarding files must remain consistent with current governance documents.
6. Deprecated artifacts must remain traceable until an approved removal process is completed.

## Repository Areas

- `engineering-charter/` contains constitutional and governance authority documents.
- `standards/` contains ratified engineering standards.
- `schemas/` contains machine-readable specifications.
- `templates/` contains approved document and workflow templates.
- `examples/` contains representative examples tied to specifications.
- `adr/` contains architecture decision records.
- `aip/` contains architecture improvement proposals.

## Ratification

This standard is ratified as the repository governance baseline for IWOS specification work.
