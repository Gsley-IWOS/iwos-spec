# Schemas

**Document ID:** SCH-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-TEST-001 Testing Standard  
**Parent Documents:** standards/testing-standard.md, adr/ADR-0003-machine-readable-engineering-memory.md  
**Last Updated:** 2026-10-31

## Purpose

This directory holds the machine-readable contracts of the IWOS specification repository. Every governed YAML artefact is bound to a JSON Schema here, and the validator checks the binding on every change. Schemas are written in JSON Schema draft 2020-12, the implementation-neutral contract language chosen in ADR-0003.

## Schemas

| Schema | ID | Validates | Examples |
| --- | --- | --- | --- |
| `ai-bootstrap.schema.json` | SCH-002 | `AI_BOOTSTRAP.yaml` | `examples/ai-bootstrap/` |
| `ai-agent-contract.schema.json` | SCH-003 | `engineering-charter/05_AI_AGENT_CONTRACT.yaml` | `examples/ai-agent-contract/` |
| `engineering-state.schema.json` | SCH-004 | `.ai/ENGINEERING_STATE.yaml` | `examples/engineering-state/` |
| `knowledge-graph.schema.json` | SCH-005 | `.ai/KNOWLEDGE_GRAPH.yaml` | `examples/knowledge-graph/` |
| `decision-graph.schema.json` | SCH-006 | `.ai/DECISION_GRAPH.yaml` | `examples/decision-graph/` |
| `memory-manifest.schema.json` | SCH-007 | `.ai/MANIFEST.yaml` | `examples/memory-manifest/` |
| `constitution-lock.schema.json` | SCH-008 | `.ai/CONSTITUTION_LOCK.yaml` | `examples/constitution-lock/` |
| `bindings.schema.json` | SCH-009 | `schemas/bindings.yaml` | `examples/bindings/` |
| `bindings.yaml` | SCH-010 | The binding file itself: maps artefacts and example directories to schemas. | |

## Conventions

1. Every schema declares `$schema` as draft 2020-12 and an `$id` whose final path segment is the schema version.
2. Every schema carries an `x-iwos-document` object with `id`, `version`, `status`, `authority` and `parent_document`. The validator treats this object as the schema's document metadata.
3. Every object is closed with `additionalProperties: false` unless the schema states why it is open. Closed objects make drift visible.
4. Every governed YAML artefact declares `schema_version`; a schema accepts only the versions it is written for. Tooling configuration under `tools/` is not a governed artefact.
5. Every schema has at least one valid and one invalid example. An invalid example states in a leading comment which rule it breaks.
6. The schema for the AI Agent Contract is derived from the ratified contract and never drives a change to it. If the contract changes under governance, the schema follows.

## Changing a Schema

A change that rejects a previously valid artefact is a MAJOR increment under the Versioning Policy and requires a migration note in `CHANGELOG.md`. Additive changes are MINOR. Every change updates the examples and the `$id` version segment.

## Ratification

This index is ratified under the Testing Standard. It is effective on merge to `main` by an authorised human maintainer.
