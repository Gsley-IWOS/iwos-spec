# ADR-0003: Machine-Readable Engineering Memory with JSON Schema Contracts

**Document ID:** ADR-0003  
**Version:** 1.0.0  
**Status:** Proposed  
**Date:** 2026-10-31  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** engineering-charter/02_ARCHITECTURE_BASELINE.md, engineering-charter/05_AI_AGENT_CONTRACT.yaml  
**Last Updated:** 2026-10-31

## Purpose

This record decides the form of engineering memory in the IWOS specification repository: which records exist, where they live, and how their structure is contracted and verified.

## Context

The Architecture Baseline requires that every project has exactly one engineering state, that the state is machine-readable, and that engineering memory is updated after every completed activity. The AI Agent Contract names the records to update: Current State, Changelog, Knowledge Graph, Decision Graph and Engineering State. The Architecture Baseline also requires every subsystem to expose well-defined contracts, and the Testing Standard requires schema checks with valid and invalid examples.

An earlier draft created a `.ai/` workspace with YAML files but no schemas, so their structure was convention only and could drift silently.

## Decision Drivers

- Machine-readability and a single source of engineering state, as the baseline requires.
- Verifiability: the structure of every memory record must be checkable by the validator.
- Portability: the contract language must be implementation-neutral so the implementation repository can consume the same records.
- Minimal duplication: memory summarises and indexes ratified documents; it does not restate them.

## Options Considered

1. **YAML records in `.ai/` with a JSON Schema (draft 2020-12) for each, bound in `schemas/bindings.yaml`, validated on every change, with valid and invalid examples in `examples/`.** YAML is readable by humans and agents; JSON Schema is the implementation-neutral contract language with reference validators in every ecosystem.
2. **Markdown records only.** Readable, but not machine-readable in the sense the baseline requires; structure cannot be contracted.
3. **A database or external service.** Not versioned with the repository; adds a trust boundary; contradicts the knowledge-as-infrastructure principle.
4. **YAML without schemas.** The status quo of the earlier draft; drift is undetectable.

## Decision

Option 1. Engineering memory consists of: `CHANGELOG.md` at the root; and in `.ai/`, `README.md`, `MANIFEST.yaml`, `ENGINEERING_STATE.yaml`, `CURRENT_STATE.md`, `NEXT_TASK.md`, `KNOWLEDGE_GRAPH.yaml`, `DECISION_GRAPH.yaml` and the generated `CONSTITUTION_LOCK.yaml`. Each YAML record declares `schema_version` and is bound to a JSON Schema in `schemas/` through `schemas/bindings.yaml`. `ENGINEERING_STATE.yaml` carries the eight state elements the baseline names: current release, milestone, sprint, epic, story, task, risks and decisions. The validator checks every record against its schema, checks that every path named in the knowledge graph and decision graph exists, and checks that the integrity lock matches the protected documents. `AI_BOOTSTRAP.yaml` and the AI Agent Contract are bound to schemas under the same mechanism.

## Consequences

- Positive: engineering state is a verified contract, not a convention; agents and the implementation repository can consume it without parsing prose.
- Positive: the AI Agent Contract, already ratified, gains a schema without being changed; the schema is derived from the contract, not the reverse.
- Negative: every change to a memory record's structure requires a schema change, a version increment and example updates. This is the intended cost.
- Neutral: the repository knowledge graph and decision graph are named by analogy with the Knowledge Graph and Decision Ledger components of the baseline. They are engineering memory of this repository and are not those components.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
