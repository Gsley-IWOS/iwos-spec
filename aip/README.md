# Architecture Improvement Proposals

**Document ID:** AIP-INDEX  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** GOV-003 Decision Process  
**Parent Document:** governance/decision-process.md  
**Last Updated:** 2026-10-31

## Purpose

This index registers every Architecture Improvement Proposal (AIP) in the IWOS specification repository and allocates AIP identifiers. An AIP is the required proposal for any change to a protected document, a governance policy, a standard or a published specification. When accepted, it authorises exactly the change its Specification section describes.

## Register

| ID | Title | Affects | Status | Date |
| --- | --- | --- | --- | --- |
| [AIP-0001](AIP-0001-identifier-families.md) | Register additional identifier families in the Naming Standard | STD-NAME-001 | Review | 2026-10-31 |

The next identifier is `AIP-0002`.

## Authoring

Copy `templates/aip-template.md` to `aip/AIP-####-<kebab-title>.md`. Complete every section: Summary, Motivation, Specification, Impact, Compatibility, Alternatives, Governance Outcome. Open a pull request. The proposal remains in `Review` for at least five working days. The authority that may accept it is defined in `governance/roles-and-authority.md`: the Constitutional Authority when a protected document is affected, otherwise the Architecture Authority.

## Lifecycle

`Draft`, `Review`, `Accepted`, `Rejected`, `Deferred`, `Superseded`, `Withdrawn`, as defined in the Decision Process. The status in the register is updated in the same change that changes the proposal's status.

## Ratification

This index is ratified under the Decision Process. It is effective on merge to `main` by an authorised human maintainer.
