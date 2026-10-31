# Glossary

**Document ID:** AS-002  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-ARCH-001 Architecture Standard  
**Parent Documents:** engineering-charter/02_ARCHITECTURE_BASELINE.md, standards/naming-standard.md  
**Last Updated:** 2026-10-31

## Purpose

The Naming Standard requires abbreviations to be defined before use unless they are established IWOS identifiers. This glossary is the register of established IWOS terms and abbreviations. A term listed here may be used anywhere in the repository without local definition. Definitions are summaries of the ratified source named in each row.

## Terms

| Term | Abbreviation | Definition | Source |
| --- | --- | --- | --- |
| Intelligent Work Orchestration System | IWOS | The Enterprise Cognitive Operating System that transforms human intent into reliable, explainable, verifiable and continuously improving execution. | FC-001, AB-001 |
| Cognitive Operating System | | The computing paradigm IWOS introduces: a platform that plans, verifies, coordinates, executes, learns and improves from natural-language objectives. | FC-001 |
| Intelligent Work Language | IWL | The constitutional component that represents intent. | AB-001 |
| Intelligent Work Compiler | IWC | The constitutional component that transforms structured intent into executable representations. | AB-001 |
| Intelligent Work Kernel | IWK | The runtime execution engine that coordinates workflows, schedules execution and maintains context. | AB-001 |
| Intelligent Kernel Bytecode | IKB | The portable execution representation, independent of implementation language. | AB-001 |
| Enterprise Asset Registry | EAR | The canonical registry of enterprise assets: systems, people, processes, knowledge, policies, resources. | AB-001 |
| Decision Ledger | | The immutable record of significant decisions supporting explainability and auditing. | AB-001 |
| Knowledge Graph | | The representation of organisational knowledge as connected entities, supporting reasoning, discovery and context reconstruction. The repository file `.ai/KNOWLEDGE_GRAPH.yaml` is named by analogy and is not this component. | AB-001 |
| Mission Graph | | The representation of strategic objectives and execution dependencies. | AB-001 |
| Digital Twin | | The executable representation of organisational reality. | AB-001 |
| Intelligence Engine | | One of the nine engines every compliant implementation includes: Strategy, Decision, Verification, Knowledge, Execution, Evolution, Risk, Communication and Measurement. | AB-001 |
| Context | | The validated inputs every execution operates on: mission, business, technical, execution, knowledge, historical and environmental context. | AB-001 |
| Engineering State | | The single machine-readable state of a project: current release, milestone, sprint, epic, story, task, risks and decisions. | AB-001 |
| Engineering Memory | | The persistent record of architecture, decisions, knowledge, implementation, testing, release and operations, updated after every completed activity. | AB-001, AAC-001 |
| Founding Charter | FC | The supreme constitutional document of IWOS. | FC-001 |
| Engineering Constitution | EC | The supreme engineering law beneath the Founding Charter. | EC-001 |
| Project Genesis | PG | The programme charter that sequences and bounds IWOS engineering delivery. | PG-001 |
| Architecture Baseline | AB | The immutable architectural foundation; AB-1.0 is the current release. | AB-001 |
| Engineering Playbook | EP | The mandatory day-to-day operating sequence. | EP-001 |
| Code Review Playbook | CRP | The mandatory review gates and merge criteria. | CRP-001 |
| AI Agent Contract | AAC | The mandatory behaviour of every AI agent in the ecosystem. | AAC-001 |
| Request for Comments | RFC | The non-binding exploratory step of the Decision Process. | GOV-003 |
| Architecture Improvement Proposal | AIP | The proposal that, when accepted, authorises a change to a protected document, policy, standard or specification. | GOV-003 |
| Architecture Decision Record | ADR | The durable record of a technical decision within the Architecture Baseline. | STD-ARCH-001, GOV-003 |
| Engineering Work Package | EWP | The authorising artefact for a bounded unit of work. | PG-001 |
| Protected Document | | A constitutional document or ratified standard whose digest is recorded in the constitutional integrity lock. | EC-001 |
| Constitutional Integrity Lock | | `.ai/CONSTITUTION_LOCK.yaml`: the generated record of SHA-256 digests of every protected document, checked by the validator. | GOV-004 |
| Ratification | | The act by which a document becomes authoritative: merge to `main` by a human holding the required authority. | EC-001, GOV-004 |
| Constitutional Authority | | The human maintainers who may ratify constitutional documents and standards. | GOV-002 |
| Architecture Authority | | The human maintainers who may accept Architecture Decision Records. | GOV-002 |
| Maintainer | | A human contributor with write access who may approve and merge non-protected changes. | GOV-002 |
| Standard | STD | A ratified engineering standard in `standards/`. | STD-INDEX |
| JSON Schema | | The schema language, draft 2020-12, used for every machine-readable contract in `schemas/`. | ADR-0003 (Proposed) |
| Continuous Integration | CI | The automated execution of the validator on every pull request, defined in `.github/workflows/validate.yml`. | ADR-0002 (Proposed) |

## Adding a Term

Add a row when a term is used in more than one document or an abbreviation is introduced. Cite the ratified source. A term whose source is not ratified is marked `Proposed` in the Source column.

## Ratification

This glossary is ratified under the Architecture Standard. It is effective on merge to `main` by an authorised human maintainer.
