# IWOS Version Policy

**Document ID:** GOV-VERSION-POLICY  
**Version:** 1.0.0  
**Status:** Ratified  
**Last Updated:** 2026-07-31  
**Authority:** IWOS Governance Authority

---

## Purpose

This policy defines how IWOS specification artifacts are versioned and how version changes communicate compatibility expectations.

Versioning exists to make change understandable. A version must signal whether consumers can safely adopt an update, need to review changed behavior, or must perform migration work.

## Version Format

IWOS specification releases use semantic versioning in the form:

```text
MAJOR.MINOR.PATCH
```

Individual documents may also carry document-local versions using the same format when independent document history is useful.

## Version Meaning

### Major Version

Increment the major version when a release introduces incompatible changes to normative architecture, governance, schemas, or standards.

Major versions require migration notes and explicit approval from the appropriate governance authority.

### Minor Version

Increment the minor version when a release introduces backward-compatible normative additions, new standards, new schemas, or substantial new guidance.

Minor versions require review for consistency with existing architecture and governance.

### Patch Version

Increment the patch version when a release includes editorial fixes, non-normative clarifications, formatting improvements, or corrections that do not alter compatibility expectations.

Patch versions require normal repository review.

## Pre-Release and Draft Versions

Draft or pre-release artifacts may use labels such as `0.1.0-draft` or `1.0.0-rc.1` when the artifact is not yet ratified.

Draft versions are not authoritative unless a governing document explicitly states otherwise.

## Compatibility Requirements

Every release that changes normative content must document:

- affected artifacts;
- compatibility impact;
- migration requirements;
- superseded or deprecated content;
- related AIPs, ADRs, or change-control records.

## Deprecation

Deprecated content remains valid until a stated removal version or superseding artifact takes effect. Deprecation notices must identify the replacement path and expected migration timeline.

## Release Authority

A version is official only after it is reviewed, approved, tagged, and recorded according to repository governance. Version numbers must not be used to imply ratification before approval is complete.
