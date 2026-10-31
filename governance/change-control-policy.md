# Change Control Policy

**Document ID:** GOV-004  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-10-31

## Purpose

This policy defines how a change enters the IWOS specification repository, which class it belongs to, what traceability and approval it requires, and when it becomes authoritative. It gives effect to Article 7 (Scope and Change Control) and Article 10 (Review and Merge) of the Engineering Constitution.

## Scope

This policy applies to every change to every file in `iwos-spec`.

## Classes of Change

| Class | Definition | Required authority | Decision artefact |
| --- | --- | --- | --- |
| Editorial | Corrects spelling, grammar, formatting, a broken link or a factual slip without changing meaning. | Maintainer review and merge. | None. The pull request states that the change is editorial. |
| Clarifying | Explains existing intent without changing any normative statement. | Maintainer review and merge. A reviewer who finds that the clarification changes interpretation reclassifies it as Normative. | None, unless reclassified. |
| Normative | Adds, removes or alters a requirement, a rule, a boundary, a contract, a schema or a compatibility expectation in a non-protected artefact. | Maintainer review and merge, with the authorising work package, ADR or AIP cited. | Work package, ADR or AIP as the Decision Process requires. |
| Constitutional | Any change to a protected document: `engineering-charter/*`, `standards/*-standard.md` or `governance/*.md`. | Accepted AIP; Constitutional Authority merge; regenerated integrity lock in the same change. | AIP, and an ADR where the change embodies a technical decision. |
| Emergency | Corrects an urgent defect in correctness, security, compliance or repository integrity. | Two Maintainers, or one holder of Constitutional Authority. | Retrospective record within five working days with the traceability of the equivalent non-emergency class. |

The protected patterns are defined in `tools/validate/config.yaml` and mirrored in `AI_BOOTSTRAP.yaml` under `protected_documents`; the validator fails when the two disagree. Digests are recorded in `.ai/CONSTITUTION_LOCK.yaml`.

## Required Traceability

Every change that is not Editorial states, in the pull request:

- the reason for the change;
- the artefacts affected;
- the authorising work package, ADR, AIP or issue;
- the approving authority;
- the compatibility and migration impact, when the Versioning Policy requires it;
- the validation performed.

## The Ratification Rule

A document's Status field states the status it holds once merged to `main`. Merge to `main` by a human holding the required authority is the act of ratification, acceptance or approval. Until merge, a document whose status reads `Ratified`, `Accepted` or `Approved` is a request for that status and must not be described otherwise.

A contributor who merges a document therefore ratifies it. A contributor who lacks the required authority must not merge.

## Protection of Constitutional Documents

The validator computes the SHA-256 digest of every protected document and compares it with `.ai/CONSTITUTION_LOCK.yaml`. A mismatch fails validation and blocks merge. A Constitutional change regenerates the lock with `make lock` in the same change, so that the diff of the lock is reviewed together with the diff of the document.

## Supersession and Removal

A document must never be deleted to make a change. It is superseded: its status is set to `Superseded`, it names its successor, and it remains in the repository. Removal of a superseded document requires an accepted AIP.

An artefact with no content, such as an empty or accidentally created file, is not a document. A Maintainer may remove it in a Normative change recorded in the decision graph.

## Founding Exception

The founding release created the Engineering Charter pack (`engineering-charter/01`, `03`, `04`, `06`), the governance policies and the standards index under EWP-0001 and EWP-0002 before this policy or the Decision Process existed. No AIP could precede them. Their creation is ratified by the Constitutional Authority's merge of the founding release. From that merge onward this policy applies to them in full, and the exception is not available again.

## Retrospective Records

An Emergency change is followed within five working days by the decision artefact its underlying class requires and by an entry in `CHANGELOG.md` marked as retrospective.

## Ratification

This policy is ratified under the Engineering Constitution. It is effective on merge to `main` by an authorised human maintainer.
