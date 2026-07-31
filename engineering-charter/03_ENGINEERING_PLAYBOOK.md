# IWOS Engineering Playbook

**Purpose:** Define the engineering operating model for changes to the IWOS specification repository.

**Authority:** engineering-charter/06_ENGINEERING_CONSTITUTION.md

**Version:** 1.0.0

**Status:** Ratified bootstrap baseline

**Parent document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md

---

## Purpose

The Engineering Playbook defines how contributors plan, make, validate, and hand off changes in `iwos-spec`.

## Work Intake

Every material change should be linked to one of the following authorities:

- Ratified work package.
- Approved issue.
- Approved ADR.
- Approved AIP.
- Maintainer instruction consistent with the authority chain.

## Planning

Before editing, contributors must identify scope, affected files, governing documents, validation needs, and review risks. Plans should be detailed enough that reviewers can compare intended work with delivered changes.

## Change Execution

Contributors must preserve document metadata, write durable Markdown or YAML, keep commits logical, and avoid combining unrelated governance, architecture, and process changes.

## Verification

Verification must be appropriate to the changed artifacts. At minimum, YAML files must parse successfully, required files must exist, and documents must be reviewed for required metadata and ratification sections.

## Handoff

Every pull request must summarize files changed, commits made, architectural decisions, validation performed, and any items requiring human review.

## Ratification

This playbook is ratified for Sprint 0. Amendments require review under the Engineering Constitution.
