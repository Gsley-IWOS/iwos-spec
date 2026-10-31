# Governance

**Document ID:** GOV-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-10-31

## Purpose

The governance policies define who holds authority in IWOS, how a change is proposed and decided, which classes of change require which approval, and how versions communicate compatibility. They define authority and process for this repository.

## Policies

| Document | ID | Defines |
| --- | --- | --- |
| [Roles and Authority](roles-and-authority.md) | GOV-002 | The roles that hold authority, what each may approve, and how authority is delegated. |
| [Decision Process](decision-process.md) | GOV-003 | The Request for Comments, Architecture Improvement Proposal and Architecture Decision Record lifecycle. |
| [Change Control Policy](change-control-policy.md) | GOV-004 | Classes of change, required traceability, approval and the ratification rule. |
| [Versioning Policy](versioning-policy.md) | GOV-005 | Semantic versioning of documents and releases, deprecation and supersession. |
| [Request for Comments register](rfc/README.md) | GOV-006 | Register and location of RFCs. |

## Relationship to Other Artefacts

Architecture Decision Records are kept in `adr/` and Architecture Improvement Proposals in `aip/`, as the Repository Standard requires. Requests for Comments are kept in `governance/rfc/`. The standards in `standards/` define quality; the policies here define authority and process.

## Changing a Policy

Governance policies are protected documents. A policy must change only through an accepted Architecture Improvement Proposal, merge by the Constitutional Authority and regeneration of the constitutional integrity lock in the same change. See the Decision Process and the Change Control Policy.

## Ratification

This index is ratified under the Engineering Constitution. It is effective on merge to `main` by an authorised human maintainer.
