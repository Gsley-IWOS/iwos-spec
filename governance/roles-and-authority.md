# Roles and Authority

**Document ID:** GOV-002  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-10-31

## Purpose

This policy names the roles that hold authority in the IWOS specification repository, states what each role may approve, and defines how authority is delegated and recorded. It gives effect to Article 4 (Human Authority) and Article 11 (Amendment) of the Engineering Constitution.

## Scope

This policy applies to every decision that changes the content of `iwos-spec`: ratification, acceptance, approval, merge and release.

## Roles

| Role | Held by | Authority |
| --- | --- | --- |
| Constitutional Authority | Human maintainers named by the repository owner as constitutional maintainers. | Ratify constitutional documents; accept Architecture Improvement Proposals that change protected documents; approve Architecture Baseline releases; approve amendments to this policy. |
| Architecture Authority | Human maintainers designated as architects by the Constitutional Authority. | Accept Architecture Decision Records; accept Architecture Improvement Proposals that do not change protected documents; approve architecture reference documents. |
| Maintainer | Human contributors with write access granted by the Constitutional Authority. | Approve and merge changes to governance-permitted artefact families; approve work packages; close Requests for Comments; cut releases under the Versioning Policy. |
| Reviewer | Any human contributor. | Review changes against the Code Review Playbook; block merge by requesting changes. |
| Contributor | Any human or AI agent. | Propose changes, open Requests for Comments, draft proposals and records, implement approved work packages. |
| AI Agent | Any artificial intelligence system acting in the repository. | The authority of a Contributor, bound additionally by the AI Agent Contract. An AI agent never ratifies, accepts, approves or merges. |

The mandatory roles named in the AI Agent Contract (Systems Architect, Software Engineer, Technical Writer, Reviewer, Quality Engineer) are functional roles that a Contributor performs within a work package. They confer no approval authority.

## Authority Matrix

| Action | Minimum authority |
| --- | --- |
| Ratify a document in `engineering-charter/` | Constitutional Authority |
| Ratify or change a standard in `standards/` | Constitutional Authority |
| Ratify or change a governance policy | Constitutional Authority |
| Accept an Architecture Improvement Proposal touching protected documents | Constitutional Authority |
| Accept any other Architecture Improvement Proposal | Architecture Authority |
| Accept an Architecture Decision Record | Architecture Authority |
| Approve a work package | Maintainer |
| Merge a change to `architecture/`, `schemas/`, `templates/`, `examples/`, `tools/`, `.github/`, `.ai/` or root onboarding files | Maintainer |
| Regenerate the constitutional integrity lock | Constitutional Authority, in the same change as the protected-document change |
| Tag a release | Maintainer, after the Versioning Policy requirements are met |
| Close a Request for Comments | Maintainer |

## Delegation and Record

Authority is granted and revoked by the Constitutional Authority. The current holders of each role are recorded in `.github/CODEOWNERS` once named; until then the repository owner holds every role. A grant or revocation is recorded in `CHANGELOG.md`.

A person must not approve their own change. An approval by an AI agent carries no authority.

Interim rule: until a second human holder of Maintainer authority is named in `.github/CODEOWNERS`, the repository owner may approve and merge changes they authored, including the founding release. This rule expires when `CODEOWNERS` names a second Maintainer and must not be used after that.

## Conflicts

Where two holders of the same authority disagree, the question is escalated to the Constitutional Authority through a Request for Comments. The Constitutional Authority's decision is recorded as an Architecture Decision Record when architectural, otherwise in the decision graph.

## Ratification

This policy is ratified under the Engineering Constitution. It is effective on merge to `main` by an authorised human maintainer and is amended only by the Constitutional Authority.
