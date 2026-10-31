# Engineering Work Packages

**Document ID:** EWP-INDEX  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** PG-001 Project Genesis  
**Parent Document:** engineering-charter/01_PROJECT_GENESIS.md  
**Last Updated:** 2026-10-31

## Purpose

An Engineering Work Package (EWP) is the smallest unit of authorised work in IWOS. It names an objective, a bounded scope, inputs, outputs, validation criteria and completion evidence. Every change to this repository must be traceable to a work package, an accepted decision record, an accepted proposal or an issue, as Article 7 of the Engineering Constitution requires.

## Lifecycle

| Status | Meaning |
| --- | --- |
| Proposed | Drafted and awaiting human approval. Work may begin as a proposal, but its outputs are not authoritative until the package is approved (Engineering Constitution Article 7). |
| Approved | Approved by a human maintainer. Work proceeds under its scope. |
| In Progress | At least one pull request implementing the package is open. |
| Complete | Every output exists, validation has passed and engineering memory has been updated. |
| Superseded | Replaced by a later package; retained for traceability. |

A package is approved by merging it to `main` with status `Approved`, or by a maintainer changing its status to `Approved` in a later change. EWP-0001 predates this index and carries no status field; its commit to `main` by the maintainer is its approval.

## Index

| ID | Name | Sprint | Status |
| --- | --- | --- | --- |
| [EWP-0001](EWP-0001.md) | Bootstrap the Constitutional Repository | 0 | In Progress |
| [EWP-0002](EWP-0002.md) | Governance Processes, Decision Records and Templates | 1 | Proposed |
| [EWP-0003](EWP-0003.md) | Schemas, Examples, Validation Tooling and Engineering Memory | 1 | Proposed |

## Authoring

Use `templates/work-package-template.md`. Identifiers must follow the Naming Standard family `EWP-####` and must be allocated sequentially. A package must not be renumbered after it is referenced by a pull request.

## Ratification

This index is ratified under Project Genesis as the register of IWOS engineering work packages. It is effective on merge to `main` by an authorised human maintainer.
