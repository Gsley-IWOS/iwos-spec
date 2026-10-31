# AIP-0001: Register Additional Identifier Families in the Naming Standard

**Document ID:** AIP-0001  
**Version:** 1.0.0  
**Status:** Review  
**Date:** 2026-10-31  
**Authority:** Constitutional Authority under GOV-002 (affects a protected document)  
**Parent Documents:** governance/decision-process.md, standards/naming-standard.md  
**Last Updated:** 2026-10-31

## Purpose

This proposal asks the Constitutional Authority to extend the Identifier Families section of the Naming Standard so that every durable artefact in the repository has a registered identifier family.

## Summary

Add eleven identifier families to STD-NAME-001 and define the `-INDEX` suffix convention for register documents. Increment the Naming Standard to version 1.1.0 and regenerate the constitutional integrity lock.

## Motivation

The Naming Standard registers six families: `FC-###`, `AB-###`, `STD-<AREA>-###`, `EWP-####`, `ADR-####` and `AIP-####`. The Documentation Standard expects every durable document to be identifiable, and the Naming Standard requires identifiers to be unique within their family. The repository now contains governance policies, architecture reference documents, schemas, templates, examples, onboarding files, engineering memory records and tooling documentation, none of which has a registered family.

The constitutional documents use the families `PG-###`, `EC-###`, `EP-###`, `CRP-###` and `AAC-###` by the practice established in the ratified Founding Charter (`FC-001`), Architecture Baseline (`AB-001`) and AI Agent Contract (`AAC-001`). Those identifiers are not provisional; this proposal registers them retrospectively.

An AI agent may not modify a standard. The documents introduced by EWP-0002 and EWP-0003 therefore carry provisional identifiers from the families proposed here, recorded as decision DEC-0003 in the decision graph.

## Specification

Replace the Identifier Families section of `standards/naming-standard.md` with the following list.

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

Add the rule: a register or index document for a family uses the family prefix with the suffix `-INDEX` in place of a number (`ADR-INDEX`, `AIP-INDEX`, `EWP-INDEX`, `STD-INDEX`).

Set the Naming Standard's Version to `1.1.0` and Last Updated to the date of merge.

## Impact

- `standards/naming-standard.md`: one section replaced, version incremented.
- `.ai/CONSTITUTION_LOCK.yaml`: regenerated.
- Every document already carrying a provisional identifier becomes conformant without change.
- The validator's identifier-uniqueness check is unchanged; it enforces global uniqueness of identifiers across Markdown, YAML and JSON documents, which implies uniqueness within every family.

## Compatibility

Additive. No existing identifier changes. MINOR increment under the Versioning Policy. No migration.

## Alternatives

1. **Omit Document IDs from documents outside the six registered families.** Permitted by the Documentation Standard, which does not list Document ID among mandatory metadata, but it would make these documents the only ones in the repository without a stable identifier and would weaken the knowledge graph and the validator's cross-reference checks.
2. **Reuse `STD-<AREA>-###` for everything.** Would misrepresent governance policies, templates and memory records as standards.
3. **Register families incrementally as each artefact type is introduced.** Produces many small constitutional changes; a single registration is cheaper to review.

## Governance Outcome

Review. Awaiting decision by the Constitutional Authority. If accepted, the Constitutional Authority applies the Specification to the Naming Standard, regenerates the lock and sets this proposal to `Accepted` in the same change. If rejected, decision DEC-0003 is reopened and a work package re-identifies the affected documents under the Naming Standard as it stands.

## Ratification

This proposal carries no authority until a holder of Constitutional Authority merges it with status `Accepted`. Its acceptance authorises exactly the change in the Specification section.
