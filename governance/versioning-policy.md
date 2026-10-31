# Versioning Policy

**Document ID:** GOV-005  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-10-31

## Purpose

This policy defines how documents, schemas and releases of the IWOS specification repository are versioned, so that a version number tells a consumer whether an update is safe to adopt, requires review or requires migration. It gives effect to Article 8 (Compatibility and Integrity) of the Engineering Constitution.

## Scope

This policy applies to every artefact that carries a Version field and to releases of the repository as a whole.

## Version Format

Versions use semantic versioning: `MAJOR.MINOR.PATCH`. Constitutional documents may append a release name in parentheses, as in `1.0.0 (Genesis)`; the name is descriptive and carries no ordering.

Pre-release versions use a hyphenated label: `1.1.0-draft.1`, `2.0.0-rc.1`. A pre-release version is never authoritative.

## Document Versions

Each document carries its own version.

| Increment | When |
| --- | --- |
| MAJOR | A normative statement is removed or changed so that a conforming consumer may no longer conform; a schema change rejects a previously valid artefact. |
| MINOR | A normative statement, section, schema property or capability is added and every previously conforming consumer still conforms. |
| PATCH | Editorial or Clarifying change under the Change Control Policy. |

The Last Updated field must change with every increment. A document whose content changes without a version increment must not pass review.

## Schema Versions

JSON Schema files carry their version in the `x-iwos-document` object and in the final path segment of their `$id`. Governed YAML artefacts declare the `schema_version` they conform to. A MAJOR schema change requires a migration note in `CHANGELOG.md` and updated examples under `examples/`.

## Repository Releases

A release is a ratified set of artefacts identified by a git tag `v<MAJOR>.<MINOR>.<PATCH>` and a section in `CHANGELOG.md`. The release version increments by the highest increment class among the documents it contains.

A release requires:

- `make validate` and `make test` passing on the tagged revision;
- a `CHANGELOG.md` section listing every artefact changed since the previous release with its class of change;
- for a MAJOR release, a migration note for every incompatible change;
- approval by a Maintainer under the Roles and Authority policy.

## Deprecation and Supersession

A deprecated artefact remains valid until the release named in its deprecation notice. The notice names the replacement and the removal release. A superseded document keeps its final version, is marked `Superseded` and links to its successor.

## Compatibility Statement

Implementations claim conformance to a release of this repository, not to `main`. A claim names the release tag.

## Ratification

This policy is ratified under the Engineering Constitution. It is effective on merge to `main` by an authorised human maintainer.
