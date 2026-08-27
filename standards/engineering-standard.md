# Engineering Standard

**Document ID:** STD-ENG-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-07-31

## Purpose

This standard defines the baseline engineering expectations for IWOS work so that every change is intentional, reviewable, testable and aligned with the mission of reliable, explainable and verifiable execution.

## Scope

This standard applies to specifications, schemas, templates, examples, architecture records and supporting repository assets.

## Principles

- Prefer clarity over cleverness.
- Preserve architectural intent before optimizing local implementation detail.
- Make every change reviewable in isolation.
- Treat tests, documentation and schemas as engineering artifacts, not afterthoughts.
- Keep governance, architecture and implementation concerns separate.

## Requirements

1. Each change must have a clear objective and bounded scope.
2. New behavior must be represented in documentation or schema before it is treated as canonical.
3. Breaking changes must identify affected artifacts and migration expectations.
4. Work must not introduce placeholder files, unresolved TODOs or unverifiable claims.
5. Generated artifacts must declare their source or generation process when committed.
6. Reviewers must be able to determine why the change exists, what authority permits it and how it was validated.

## Quality Gates

Engineering work must pass applicable formatting, linting, schema validation and documentation consistency checks before review. If a check cannot run, the limitation must be recorded with the change.

## Ratification

This standard is ratified as the default engineering quality baseline for IWOS specification work.
