# IWOS Specification Repository

**Document ID:** ROOT-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** engineering-charter/06_ENGINEERING_CONSTITUTION.md  
**Last Updated:** 2026-10-31

## Purpose

`iwos-spec` is the constitutional repository of the Intelligent Work Orchestration System (IWOS). It holds the ratified mission, architecture, governance, standards, contracts, schemas and templates from which every IWOS implementation inherits.

The repository exists so that intent, architecture and decisions outlive any single implementation. It contains no product runtime code. Code appears here only where a ratified standard requires it for validation of the specification itself.

## Repository Hierarchy

| Path | Owns | Governing standard |
| --- | --- | --- |
| `engineering-charter/` | Constitutional documents: Founding Charter, Project Genesis, Architecture Baseline, Engineering Playbook, Code Review Playbook, AI Agent Contract, Engineering Constitution. | Engineering Constitution |
| `governance/` | Governance policies (protected): roles and authority, decision process, change control, versioning. | Engineering Constitution |
| `architecture/` | Architecture reference material derived from the Architecture Baseline: index, glossary, component catalogue. | STD-ARCH-001 |
| `standards/` | Ratified engineering standards. | Engineering Constitution |
| `schemas/` | Machine-readable JSON Schema definitions for governed YAML artefacts, plus the binding file that maps artefacts to schemas. | STD-TEST-001 |
| `templates/` | Approved templates for ADRs, AIPs, RFCs, standards, specifications and work packages. | STD-DOC-001 |
| `examples/` | Valid and invalid examples exercised by the validator. | STD-TEST-001 |
| `adr/` | Architecture Decision Records. | STD-ARCH-001 |
| `aip/` | Architecture Improvement Proposals. | governance/decision-process.md |
| `work-packages/` | Engineering Work Packages (EWP) that authorise bounded units of work. | engineering-charter/01_PROJECT_GENESIS.md |
| `tools/validate/` | Repository validator and its unit tests. | STD-TEST-001, STD-REPO-001 |
| `.github/` | Pull request template, issue forms and the continuous-integration workflow. | STD-REPO-001 |
| `.ai/` | Engineering memory: machine-readable engineering state, knowledge graph, decision graph, current state, next task and the constitutional integrity lock. | engineering-charter/05_AI_AGENT_CONTRACT.yaml |

Root files: `CLAUDE.md` and `AGENTS.md` onboard AI agents, `AI_BOOTSTRAP.yaml` is the machine-readable onboarding manifest, `CONTRIBUTING.md` and `SECURITY.md` apply to every contributor, and `CHANGELOG.md` records every ratified change.

## Relationship to the IWOS Repository

The Architecture Baseline divides the ecosystem into two repositories. `iwos-spec` owns architecture, standards, governance, specifications and contracts. The implementation repository `IWOS` owns the compiler, runtime, SDK, CLI and enterprise implementation.

Implementation conforms to this repository. It never redefines it. When implementation evidence shows that architecture or a standard must change, the change is proposed here through the decision process and becomes authoritative only after ratification. An implementation may call itself IWOS-compliant only when it conforms to the documents listed in the Compliance section of the Architecture Baseline.

## Authority Chain

This list is a summary of Article 1 of the Engineering Constitution, which is canonical. When two documents disagree, the higher document governs until the conflict is resolved through the decision process.

1. Founding Charter (`FC-001`)
2. Engineering Constitution (`EC-001`)
3. Project Genesis (`PG-001`)
4. Architecture Baseline (`AB-001`)
5. Constitutional operating documents: AI Agent Contract (`AAC-001`), Engineering Playbook (`EP-001`), Code Review Playbook (`CRP-001`)
6. Ratified governance policies and standards
7. Accepted Architecture Decision Records
8. Published specifications, schemas and templates
9. Approved work packages
10. Implementation
11. Verification evidence and release artefacts
12. Engineering memory

Architecture Improvement Proposals and Requests for Comments are proposal artefacts. They carry no authority of their own; their outcomes become authoritative through the documents above.

## Repository Philosophy

Knowledge is infrastructure. Every durable document carries explicit metadata, an explicit parent and an explicit ratification state, so that any reader can trace a rule back to the authority that permits it.

Architecture precedes code. Nothing in this repository may be changed by implementation. Constitutional documents and standards change only through the decision process defined in `governance/decision-process.md`.

Everything is verifiable. The validator in `tools/validate/` enforces the Testing Standard: structural checks on every governed document, schema checks on every governed YAML artefact, consistency checks on links, identifiers and authority references, example checks against the schemas, and an integrity check that every protected document matches the digest recorded in the constitutional integrity lock, so that any change to one is visible in the same reviewed diff as the lock.

Human authority is absolute. AI agents draft, verify and propose. Humans ratify by merging to `main`.

## Validating the Repository

```bash
make validate   # structural, schema, consistency, example and integrity checks
make test       # unit tests for the validator itself
make lock       # regenerate .ai/CONSTITUTION_LOCK.yaml after a ratified constitutional change
```

The validator requires Python 3.10 or later with the `PyYAML` and `jsonschema` packages. The same checks run in continuous integration on every pull request.

## Contributing

Read `CONTRIBUTING.md`. AI agents additionally read `CLAUDE.md`, `AGENTS.md` and `AI_BOOTSTRAP.yaml`, and complete the onboarding steps in `AGENTS.md` before changing anything.

## Ratification

This document is ratified under the Engineering Constitution as the entry point to the IWOS specification repository. It is effective on merge to `main` by an authorised human maintainer and remains in force until superseded by a later ratified version.
