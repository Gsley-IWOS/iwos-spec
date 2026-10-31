# Engineering Work Package Template

**Document ID:** TPL-007  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** PG-001 Project Genesis  
**Parent Documents:** engineering-charter/01_PROJECT_GENESIS.md, work-packages/README.md  
**Last Updated:** 2026-10-31

## Purpose

This template produces an Engineering Work Package containing every element Project Genesis Section 4 requires: objective, scope and non-scope, inputs, outputs, validation criteria, completion evidence and authority. Copy the fenced block below into `work-packages/EWP-####.md`; the fence is not part of the package.

## Template

```markdown
# EWP-<####>: <Name>

**Document ID:** EWP-<####>  
**Version:** 1.0.0  
**Status:** Proposed  
**Sprint:** <number>  
**Milestone:** <M0 | M1 | M2 | M3>  
**Authority:** PG-001 Project Genesis  
**Parent Documents:** engineering-charter/01_PROJECT_GENESIS.md, <ratified document or accepted proposal that motivates this package>  
**Last Updated:** <YYYY-MM-DD>

## Purpose

<One paragraph: why this package exists and what the programme gains when it is complete.>

## Objective

<The single outcome this package delivers, stated so that completion is unambiguous.>

## Scope

<The artefact families and files this package authorises the team to create or change.>

## Non-Scope

<What this package explicitly does not authorise, especially protected documents.>

## Inputs

- <Ratified document, accepted record or existing artefact this package depends on.>

## Outputs

| Output | Path | Acceptance |
| --- | --- | --- |
| <Artefact> | `<path>` | <What makes it acceptable.> |

## Validation Criteria

- `make validate` passes.
- `make test` passes.
- <Package-specific criterion.>

## Completion Evidence

- <Pull request with every handoff section.>
- <Engineering memory updated: CHANGELOG.md and .ai/ records.>

## Ratification

This package is approved by a Maintainer on merge to `main` with status `Approved`, or by a later change that sets its status to `Approved`. Work performed before approval is a proposal.
```

## Ratification

This template is ratified under Project Genesis. It is effective on merge to `main` by an authorised human maintainer.
