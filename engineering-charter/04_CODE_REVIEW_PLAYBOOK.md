# IWOS Code Review Playbook

**Purpose:** Define review expectations for specification, governance, and repository changes.

**Authority:** engineering-charter/06_ENGINEERING_CONSTITUTION.md

**Version:** 1.0.0

**Status:** Ratified bootstrap baseline

**Parent document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md

---

## Purpose

The Code Review Playbook establishes the review model for `iwos-spec`. In this repository, review applies primarily to specifications, governance documents, schemas, templates, examples, and repository metadata.

## Review Principles

1. Review for authority alignment before preference.
2. Review for clarity, durability, and future maintainability.
3. Require evidence for architectural changes.
4. Distinguish normative requirements from examples.
5. Confirm machine-readable files are valid.

## Required Review Checks

Reviewers should confirm that:

- Scope matches the approved work package or issue.
- Authority metadata is present and accurate.
- Documents include purpose, status, version, parent document, sections, and ratification.
- YAML files validate.
- No unresolved draft markers or incomplete-action statements are introduced.
- Architectural changes follow ADR or AIP governance.

## Approval Standard

A change is reviewable when a maintainer can understand its authority, purpose, content, validation evidence, and expected downstream impact without relying on private context.

## Ratification

This playbook is ratified for Sprint 0. Amendments require review under the Engineering Constitution.
