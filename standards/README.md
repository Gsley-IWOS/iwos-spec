# Standards

**Document ID:** STD-INDEX  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-10-31

## Purpose

This index lists the ratified engineering standards of IWOS and states what each governs. Standards define quality. In the hierarchy of authority they sit below the constitutional documents and above accepted Architecture Decision Records, specifications, schemas and templates.

## Ratified Standards

| Standard | ID | Governs |
| --- | --- | --- |
| [Architecture Standard](architecture-standard.md) | STD-ARCH-001 | How architectural concepts, constraints and decisions are expressed; the required content of Architecture Decision Records. |
| [Documentation Standard](documentation-standard.md) | STD-DOC-001 | Metadata, structure, requirement language and review criteria for every durable document. |
| [Engineering Standard](engineering-standard.md) | STD-ENG-001 | Baseline expectations for every change: bounded scope, no placeholders, declared generation, quality gates. |
| [Naming Standard](naming-standard.md) | STD-NAME-001 | File, directory and identifier conventions and identifier families. |
| [Repository Standard](repository-standard.md) | STD-REPO-001 | Repository layout, artefact ownership and the limits on code in this repository. |
| [Security Standard](security-standard.md) | STD-SEC-001 | Secret handling, trust boundaries, least privilege and security review criteria. |
| [Testing Standard](testing-standard.md) | STD-TEST-001 | The four categories of validation and the evidence every change must provide. |

## Changing a Standard

Standards are protected documents. A standard changes only through an accepted Architecture Improvement Proposal, merge by the Constitutional Authority and regeneration of the constitutional integrity lock in the same change. See `governance/change-control-policy.md`.

## Proposed Changes

| Proposal | Affects | Status |
| --- | --- | --- |
| [AIP-0001 Identifier Families](../aip/AIP-0001-identifier-families.md) | STD-NAME-001 | Review |

## Ratification

This index is ratified under the Engineering Constitution. It is effective on merge to `main` by an authorised human maintainer.
