# Standard Template

**Document ID:** TPL-005  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-DOC-001 Documentation Standard  
**Parent Documents:** standards/documentation-standard.md, standards/naming-standard.md  
**Last Updated:** 2026-10-31

## Purpose

This template produces an engineering standard in the structure the Documentation Standard prescribes and the form the existing standards use. Copy the fenced block below into `standards/<area>-standard.md`; the fence is not part of the standard. A new standard requires an accepted Architecture Improvement Proposal.

## Template

```markdown
# <Area> Standard

**Document ID:** STD-<AREA>-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** <YYYY-MM-DD>

## Purpose

<What this standard governs and the outcome it protects.>

## Scope

<The artefacts and activities this standard applies to, and any it excludes.>

## Authority

<The documents this standard inherits from, and the proposal that authorised it.>

## Definitions

<Terms used in this standard that are not in architecture/glossary.md.>

## Requirements

1. <Requirement using must, must not, should, should not or may.>
2. <Requirement.>

## Review Criteria

<How a reviewer decides that a change conforms to this standard.>

## Ratification

This standard is ratified under the Engineering Constitution by <AIP-####>. It is effective on merge to `main` by the Constitutional Authority and remains in force until superseded by a later ratified version.
```

## Ratification

This template is ratified under the Documentation Standard. It is effective on merge to `main` by an authorised human maintainer.
