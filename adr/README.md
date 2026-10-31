# Architecture Decision Records

**Document ID:** ADR-INDEX  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-ARCH-001 Architecture Standard  
**Parent Documents:** standards/architecture-standard.md, governance/decision-process.md  
**Last Updated:** 2026-10-31

## Purpose

This index registers every Architecture Decision Record (ADR) in the IWOS specification repository and allocates ADR identifiers. An ADR records a durable technical decision taken within the bounds of Architecture Baseline AB-1.0, with its context, drivers, options, decision and consequences, as the Architecture Standard requires.

## Register

| ID | Title | Status | Date |
| --- | --- | --- | --- |
| [ADR-0001](ADR-0001-architecture-decision-records.md) | Record architecture decisions as ADRs in `adr/` | Proposed | 2026-10-31 |
| [ADR-0002](ADR-0002-repository-validation-tooling.md) | Repository validation tooling in Python under `tools/validate/` | Proposed | 2026-10-31 |
| [ADR-0003](ADR-0003-machine-readable-engineering-memory.md) | Machine-readable engineering memory with JSON Schema contracts | Proposed | 2026-10-31 |

The next identifier is `ADR-0004`.

## Authoring

Copy `templates/adr-template.md` to `adr/ADR-####-<kebab-title>.md`. Complete every section. Open a pull request citing the work package or proposal that gave rise to the decision. The Architecture Authority accepts the record by setting its status to `Accepted`, in the register and in the record, before or in the merge.

## Boundaries

An ADR decides within the Architecture Baseline. It never changes the baseline, a constitutional document, a standard or a governance policy; those changes require an Architecture Improvement Proposal. An ADR that would require such a change is held in `Proposed` until the proposal is accepted.

## Ratification

This index is ratified under the Architecture Standard. It is effective on merge to `main` by an authorised human maintainer.
