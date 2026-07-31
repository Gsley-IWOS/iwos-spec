# IWOS Change Control Policy

**Document ID:** GOV-CHANGE-CONTROL  
**Version:** 1.0.0  
**Status:** Ratified  
**Last Updated:** 2026-07-31  
**Authority:** IWOS Governance Authority

---

## Purpose

This policy defines how changes enter, move through, and become authoritative within the IWOS Specification Repository.

IWOS treats specifications, architecture, governance, schemas, and standards as durable system assets. Changes must be reviewable, traceable, reversible when practical, and consistent with the Founding Charter.

## Change Classes

### Editorial Changes

Editorial changes improve grammar, formatting, spelling, references, or clarity without changing meaning.

Editorial changes require normal review but do not require an RFC, AIP, or ADR.

### Clarification Changes

Clarification changes explain existing intent without changing normative behavior.

Clarification changes require review and may require an ADR or AIP if reviewers determine that the clarification changes interpretation.

### Normative Changes

Normative changes alter requirements, governance rules, architecture, standards, schemas, or compatibility expectations.

Normative changes require explicit approval and must be linked to an accepted AIP, ADR, or other governing artifact.

### Emergency Changes

Emergency changes address urgent correctness, security, compliance, or repository integrity issues.

Emergency changes may be expedited, but they must be documented after the fact with the same level of traceability required for equivalent non-emergency changes.

## Required Traceability

Every substantive change must identify:

- the reason for the change;
- the affected documents or contracts;
- the approving authority;
- any related RFC, AIP, ADR, work package, issue, or pull request;
- compatibility and migration implications when applicable.

## Review Expectations

Reviewers must evaluate whether a proposed change:

- aligns with the IWOS Founding Charter;
- preserves architectural coherence;
- maintains backward compatibility or documents a justified break;
- updates related documents consistently;
- can be audited after merge.

## Authority Chain

When artifacts conflict, the following authority order applies unless a higher authority explicitly delegates precedence:

1. Founding Charter and constitutional documents;
2. ratified governance policies;
3. accepted ADRs and AIPs;
4. ratified standards and schemas;
5. work packages and implementation guidance;
6. examples and explanatory documentation.

## Merge Standard

A change is mergeable only when it is complete, internally consistent, reviewed by the appropriate authority, and free of placeholder content.
