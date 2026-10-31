# Repository Validator

**Document ID:** TOOL-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-TEST-001 Testing Standard  
**Parent Documents:** standards/testing-standard.md, adr/ADR-0002-repository-validation-tooling.md  
**Last Updated:** 2026-10-31

## Purpose

`validate.py` enforces the Testing Standard and the Change Control Policy on the IWOS specification repository. Its design is recorded in ADR-0002. `tools/validate/` holds the only program code this repository contains, as the Repository Standard permits for validation tooling; the root `Makefile` and the continuous-integration workflow only invoke it. It validates this repository and nothing else.

## Running

```bash
make validate                         # all checks; exit 0 on pass, 1 on any finding
make test                             # unit tests for the validator
make lock                             # regenerate .ai/CONSTITUTION_LOCK.yaml (constitutional changes only)
python3 tools/validate/validate.py --root /path/to/repo --config /path/to/config.yaml
```

Requirements: Python 3.10 or later, `PyYAML`, `jsonschema` (4.x, with draft 2020-12 support).

## Checks

| Category | What is checked | Source of the rule |
| --- | --- | --- |
| structural | Every Markdown document outside excluded directories: non-empty; level-1 title; metadata Document ID, Version, Status, Authority, Last Updated; Parent Document unless Authority is `Supreme`; Document ID matches the identifier pattern; Version is semantic; Status is an allowed value; Last Updated is an ISO date; a Purpose heading; a Ratification heading or a Document Status line; family-specific headings and metadata for ADRs, AIPs, RFCs, work packages and standards. | STD-DOC-001, STD-ARCH-001, STD-NAME-001, GOV-003 |
| schema | `schemas/bindings.yaml` validates against its own schema; every schema is a valid draft 2020-12 schema carrying `x-iwos-document` whose version matches the final `$id` segment; every bound YAML artefact validates against its schema. | STD-TEST-001, ADR-0003 |
| consistency | Document identifiers from Markdown metadata, YAML `document.id`, the Contract's `contract.id` and JSON Schema `x-iwos-document.id` match the identifier pattern and are globally unique (exempt documents included); parent documents and relative links resolve (fenced code is ignored); no drafting markers in Markdown, YAML or JSON outside `tools/`; no credential-shaped strings anywhere outside `.git`; every path named in `AI_BOOTSTRAP.yaml` (reading lists, memory, handoff template, workflow, authority, lock file, prohibited-actions source, amendment authority), the Contract's mandatory reading, the knowledge graph, the decision graph, the engineering state and the memory manifest exists; `contract_mandatory_reading` equals the Contract's `mandatory_reading`; `protected_documents` in the bootstrap equals the validator configuration; knowledge-graph node ids are unique and edges reference declared nodes; every bound example directory exists. | STD-TEST-001, STD-SEC-001, STD-ENG-001 |
| example | Each binding has at least one valid and one invalid example; every example is valid YAML; valid examples validate; invalid examples are rejected and each declares, with a `# expect:` comment, text that at least one error's path or message must contain. | STD-TEST-001 |
| integrity | SHA-256 of every protected document matches `.ai/CONSTITUTION_LOCK.yaml`; no protected document is unrecorded; no recorded document is missing. The check proves consistency between documents and lock, not authorisation; see Design Limits. | GOV-004, EC-001 Article 7 |

## Configuration

`config.yaml` holds every rule parameter. It is tooling configuration, not a governed artefact, so it carries no schema binding. Keys:

| Key | Meaning |
| --- | --- |
| `schema_version` | Version of the configuration layout, for forward compatibility. Not read by the validator today. |
| `markdown.exclude_dirs`, `markdown.exclude_files` | Paths not treated as governed documents. |
| `markdown.required_metadata`, `markdown.parent_metadata_keys`, `markdown.parent_exempt_authorities` | Metadata rules. |
| `markdown.required_headings`, `markdown.ratification_heading`, `markdown.ratification_line_pattern` | Heading rules. The ratification heading must match exactly after numbering is removed. |
| `markdown.allowed_statuses`, `markdown.version_pattern`, `markdown.date_pattern` | Value rules. |
| `markdown.families` | Glob-matched families with extra required headings and metadata. Index files named `README.md` are exempt from family rules. |
| `markdown.metadata_exemptions` | Specific metadata keys a named ratified document may lack. Each carries a reason. |
| `markdown.structural_exemptions` | Documents exempt from structural checks other than emptiness. Each carries a reason. |
| `identifiers.pattern` | The Document ID pattern. |
| `identifier_sources.*` | YAML and JSON artefacts whose identifiers join the uniqueness check. |
| `content.drafting_markers`, `content.drafting_marker_exclude_dirs` | Marker scan. |
| `content.secret_patterns`, `content.secret_scan_exclude_files` | Credential scan. |
| `protected_documents.lock_file`, `protected_documents.patterns` | Integrity check inputs. |
| `bindings_file`, `bindings_schema` | Schema binding inputs. |
| `cross_references.*` | Paths of the governed YAML artefacts whose references are checked. |

Weakening a rule is a Normative change under the Change Control Policy and must cite its authority in the pull request.

## Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | Every check passed, or the lock was written. |
| 1 | At least one finding. Each finding is printed as `[category] path: message`. |
| 2 | The validator could not run: missing dependency or missing configuration. |

## Design Limits

The validator does not render Markdown, does not follow external URLs, and does not evaluate the truth of prose. It checks structure, references, contracts and integrity. Semantic review remains a human gate under the Code Review Playbook.

The integrity check cannot tell an authorised change from an unauthorised one: anyone can edit a protected document and run `make lock`. What it guarantees is that the two can never diverge silently, so a protected-document change always appears in the same reviewed diff as the lock. Authorisation is enforced by human review of that diff and by branch protection and `CODEOWNERS`, which maintainers configure outside this repository's content.

## Ratification

This document is ratified under the Testing Standard. It is effective on merge to `main` by an authorised human maintainer.
