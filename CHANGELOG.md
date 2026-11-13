# Change Log

**Document ID:** ROOT-004  
**Version:** 1.0.0  
**Status:** Active  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-11-13

## Purpose

This log records every artefact added, changed, superseded or removed in the IWOS specification repository, grouped by release and by the work package, decision record or proposal that authorised it. It is the Release Memory required by the Architecture Baseline and the Changelog named in the AI Agent Contract. Entries follow the class of change defined in `governance/change-control-policy.md`.

## Unreleased (target: 1.0.0 Genesis)

### EWP-0005 Launch Readiness for IWOS Guard (Normative, Proposed)

Added:

- `tools/iwos/CASE-STUDY.md` (TOOL-003): pull request 1 replayed through the gate, with a reproducible report.
- `adr/ADR-0005-agent-attribution-by-disclosure.md` (Proposed).
- `.github/CODEOWNERS`: the repository owner owns protected paths, the lock, the constitution file, the validator configuration and automation.
- `.mcp.json`: registers `iwos mcp` for Model Context Protocol clients opened on this repository.
- `work-packages/EWP-0005.md` (Proposed).

Changed:

- `tools/iwos/src/iwos/gate.py`, `cli.py`: agents disclosed in the pull request description or labels are reported with their evidence source; reports print no e-mail addresses; revisions are shown resolved; report version 1.1.0; `--label` and `--labels-env` options. Tests extended.
- `architecture/engineering-governance/SPEC-ENGGOV-001.md` (Draft, 0.1.0-draft.2): attribution and data-handling clauses clarified per ADR-0005.
- `action.yml`: passes pull request labels to the gate. `.github/workflows/validate.yml`: a second job runs the composite action from the working tree; the hand-written gate step is removed.
- `README.md`, `tools/iwos/README.md`: case study, install from a git URL, attribution limits.

Unchanged: every protected document.

### AIP-0002 accepted: Project Genesis 1.1.0 (Constitutional)

Changed:

- `engineering-charter/01_PROJECT_GENESIS.md`: Section 2 milestone table, M2 and M3 rows replaced as AIP-0002 specifies; version 1.1.0; release PG-1.1. Applied at the Constitutional Authority's direction on 2026-11-10.
- `.ai/CONSTITUTION_LOCK.yaml`: regenerated for the amended Project Genesis.
- `aip/AIP-0002-governance-layer-first.md`: Review to Accepted. `work-packages/EWP-0004.md`: Proposed to Approved (authorised by AIP-0002 item 3). `architecture/component-catalogue.md`: Verification Engine and Decision Ledger marked Authorised.

### EWP-0004 IWOS Guard Reference Toolchain (Normative, Approved) and AIP-0002 (Accepted)

Added:

- `aip/AIP-0002-governance-layer-first.md` (Review): re-sequence milestone M2 toward the Verification Engine and Decision Ledger in the domain of AI-assisted engineering; defer IWL, IWC, IWK and IKB.
- `architecture/engineering-governance/SPEC-ENGGOV-001.md` (Draft): Engineering Governance Verification specification.
- `adr/ADR-0004-governance-toolchain-distribution.md` (Proposed): the toolchain ships from `tools/` until a dedicated repository exists.
- `work-packages/EWP-0004.md` (Proposed).
- `tools/iwos/`: the `iwos` package (init, validate, lock, gate, agents, mcp), 24 end-to-end tests, README (TOOL-002).
- `iwos.yaml`: this repository's constitution (profile `iwos-spec`); `action.yml`: composite GitHub Action `Gsley-IWOS/iwos-spec`.
- `schemas/iwos-config.schema.json` (SCH-011), `examples/iwos-config/`, binding added.
- `AGENTS.md`: generated constitution block maintained by `iwos agents`.
- `.github/workflows/validate.yml`: runs the toolchain tests, `iwos validate` and `iwos gate` on pull requests.
- `Makefile`: `test-validator`, `test-iwos`, `guard` targets.

Changed (Clarifying): `README.md` gains an IWOS Guard section; registers in `aip/`, `adr/`, `work-packages/`, `architecture/` and `schemas/` list the new documents.

Protected documents: only Project Genesis changed, under accepted AIP-0002. Every other protected document is unchanged.

### EWP-0001 Bootstrap the Constitutional Repository (Normative)

Added:

- `README.md` (ROOT-001) rewritten from a two-line stub into the repository entry point.
- `CONTRIBUTING.md` (ROOT-002), `SECURITY.md` (ROOT-003), `.editorconfig`, `.gitignore`.
- `engineering-charter/01_PROJECT_GENESIS.md` (PG-001), `03_ENGINEERING_PLAYBOOK.md` (EP-001), `04_CODE_REVIEW_PLAYBOOK.md` (CRP-001), `06_ENGINEERING_CONSTITUTION.md` (EC-001).
- `CLAUDE.md` (AIO-001), `AGENTS.md` (AIO-002), `AI_BOOTSTRAP.yaml` (AIO-003).
- `.ai/` engineering memory workspace: `README.md` (MEM-001), `MANIFEST.yaml` (MEM-002), `ENGINEERING_STATE.yaml` (MEM-003), `CURRENT_STATE.md` (MEM-004), `NEXT_TASK.md` (MEM-005), `KNOWLEDGE_GRAPH.yaml` (MEM-006), `DECISION_GRAPH.yaml` (MEM-007).

Founding exception: the Engineering Charter pack was created under EWP-0001 before the Decision Process existed; see the Founding Exception section of `governance/change-control-policy.md`.
- `work-packages/README.md` (EWP-INDEX).

Removed:

- `engineering-charter/Repository bootstrap (README.md, CLAUDE.md, AGENTS.md, AI_BOOTSTRAP.yaml)`: a one-byte file created by accident, removed under the Change Control Policy rule that an artefact with no content is not a document. Recorded as DEC-0005.

Unchanged, by design: `engineering-charter/00_FOUNDING_CHARTER.md`, `02_ARCHITECTURE_BASELINE.md`, `05_AI_AGENT_CONTRACT.yaml` and every file in `standards/` other than the new index.

### EWP-0002 Governance Processes, Decision Records and Templates (Normative, Proposed)

Added:

- `governance/README.md` (GOV-001), `roles-and-authority.md` (GOV-002), `decision-process.md` (GOV-003), `change-control-policy.md` (GOV-004), `versioning-policy.md` (GOV-005), `rfc/README.md` (GOV-006).
- `adr/README.md` (ADR-INDEX), `ADR-0001-architecture-decision-records.md`, `ADR-0002-repository-validation-tooling.md`, `ADR-0003-machine-readable-engineering-memory.md` (all Proposed).
- `aip/README.md` (AIP-INDEX), `AIP-0001-identifier-families.md` (Review; affects STD-NAME-001).

Founding exception: the governance policies are protected documents created under EWP-0002 before the Decision Process existed; see the Founding Exception section of `governance/change-control-policy.md`.
- `templates/README.md` (TPL-001) and templates TPL-002 to TPL-007 for ADR, AIP, RFC, standard, specification and work package.
- `architecture/README.md` (AS-001), `glossary.md` (AS-002), `component-catalogue.md` (AS-003).
- `standards/README.md` (STD-INDEX).
- `work-packages/EWP-0002.md` (Proposed).

### EWP-0003 Schemas, Examples, Validation Tooling and Engineering Memory (Normative, Proposed)

Added:

- `schemas/README.md` (SCH-001); JSON Schemas SCH-002 to SCH-009; `bindings.yaml` (SCH-010).
- `examples/README.md` (EX-001) and valid and invalid examples for every schema.
- `tools/validate/validate.py`, `config.yaml`, `test_validate.py`, `README.md` (TOOL-001).
- `Makefile` with `validate`, `test`, `lock` and `install-deps` targets.
- `.ai/CONSTITUTION_LOCK.yaml` (MEM-008), generated by the validator.
- `.github/workflows/validate.yml`, `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/` forms for work package, RFC and defect.
- `CHANGELOG.md` (ROOT-004).
- `work-packages/EWP-0003.md` (Proposed).

### Pre-existing on `main` before this release

- `engineering-charter/00_FOUNDING_CHARTER.md` (FC-001), `02_ARCHITECTURE_BASELINE.md` (AB-001), `05_AI_AGENT_CONTRACT.yaml` (AAC-001): committed to `main` 2026-07-31.
- `standards/` seven standards (STD-ARCH-001, STD-DOC-001, STD-ENG-001, STD-NAME-001, STD-REPO-001, STD-SEC-001, STD-TEST-001): Last Updated 2026-07-31, merged to `main` 2026-08-27 (pull request 5).
- `work-packages/EWP-0001.md`: Sprint 0 work package.
- `LICENSE`: Apache License 2.0.

## Ratification

This log is an engineering memory record maintained under the Engineering Constitution. It carries no authority and is updated in every change that completes an engineering activity.
