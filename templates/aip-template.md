# Architecture Improvement Proposal Template

**Document ID:** TPL-003  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** GOV-003 Decision Process  
**Parent Document:** governance/decision-process.md  
**Last Updated:** 2026-10-31

## Purpose

This template produces an Architecture Improvement Proposal with the seven sections the Decision Process requires. Copy the fenced block below into `aip/AIP-####-<kebab-title>.md`; the fence is not part of the proposal.

## Template

```markdown
# AIP-<####>: <Title in sentence case>

**Document ID:** AIP-<####>  
**Version:** 1.0.0  
**Status:** Draft  
**Date:** <YYYY-MM-DD>  
**Authority:** <Constitutional Authority under GOV-002 if a protected document is affected; otherwise Architecture Authority under GOV-002>  
**Parent Documents:** governance/decision-process.md, <document this proposal changes>  
**Last Updated:** <YYYY-MM-DD>

## Purpose

<One paragraph: what this proposal asks the deciding authority to approve.>

## Summary

<The proposed change in at most three sentences.>

## Motivation

<The problem or opportunity. Cite evidence: ratified documents, implementation findings, review findings.>

## Specification

<The exact normative change: the document, the section, the text to replace or add, and the version increment. This section is what acceptance authorises; nothing outside it is authorised.>

## Impact

<Every artefact, system, stakeholder and workflow affected, with the nature of the effect.>

## Compatibility

<Backward compatibility, migration requirements, deprecation notices, and the Versioning Policy increment class.>

## Alternatives

1. **<Alternative.>** <Why it was not chosen.>
2. **<Alternative.>** <Why it was not chosen.>

## Governance Outcome

<Draft | Review | Accepted | Rejected | Deferred | Superseded | Withdrawn, with the date and the deciding authority once decided.>

## Ratification

This proposal carries no authority until a holder of the required authority merges it with status `Accepted`. Its acceptance authorises exactly the change in the Specification section.
```

## Rules

- A proposal enters `Review` by pull request and stays there for at least five working days.
- The Governance Outcome section and the Status field change together, and the register in `aip/README.md` changes in the same commit.
- If the Specification changes a protected document, the same change that sets `Accepted` applies the Specification and regenerates `.ai/CONSTITUTION_LOCK.yaml`.

## Ratification

This template is ratified under the Decision Process. It is effective on merge to `main` by an authorised human maintainer.
