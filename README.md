# IWOS Specification Repository

**Purpose:** Define the authoritative specification and governance foundation for the Intelligent Work Orchestration System.

**Authority:** IWOS Founding Charter and Engineering Constitution.

**Version:** 1.0.0

**Status:** Ratified bootstrap baseline

**Parent document:** engineering-charter/00_FOUNDING_CHARTER.md

---

## Purpose

This repository is the constitutional repository for the Intelligent Work Orchestration System (IWOS). It contains the governing documents, architecture baselines, standards, schemas, templates, examples, Architecture Decision Records, Architecture Improvement Proposals, and AI-agent onboarding rules that define how IWOS is specified and evolved.

The repository exists to preserve the approved architecture and engineering operating model for IWOS. It is not an implementation repository and does not contain product runtime code.

## Repository Hierarchy

| Path | Responsibility |
| --- | --- |
| `engineering-charter/` | Constitutional engineering documents that define mission, authority, governance, review, and AI-agent conduct. |
| `governance/` | Governance processes, approval models, lifecycle rules, and stewardship procedures. |
| `architecture/` | System architecture specifications derived from the approved architecture baseline. |
| `standards/` | Engineering, documentation, interoperability, and quality standards. |
| `schemas/` | Machine-readable schemas for IWOS specifications and governed artifacts. |
| `templates/` | Approved templates for repeatable specification, review, and governance work. |
| `examples/` | Conforming examples that clarify specifications without redefining them. |
| `adr/` | Architecture Decision Records documenting approved architectural decisions. |
| `aip/` | Architecture Improvement Proposals for governed architectural evolution. |
| `.github/` | Repository automation and collaboration configuration. |
| `.ai/` | AI-assistant operating context and repository automation metadata. |

## Relationship to the IWOS Repository

`iwos-spec` is the source of constitutional and architectural authority for IWOS. The implementation repository, `IWOS`, must conform to this repository.

Implementation work may discover new constraints or improvement opportunities, but it does not redefine architecture by implication. Any architectural change required by implementation evidence must be proposed through the governed improvement process in this repository before it becomes authoritative.

## Authority Chain

IWOS repository authority is interpreted in the following order:

1. Founding Charter.
2. Engineering Constitution.
3. Architecture Baseline.
4. Approved Architecture Decision Records.
5. Ratified standards and schemas.
6. Approved templates and examples.
7. Implementation guidance and work-package instructions.

When two documents conflict, the higher-authority document governs until the conflict is resolved through formal review.

## Repository Philosophy

IWOS treats knowledge as durable infrastructure. Specifications are expected to be precise, reviewable, versioned, and suitable for long-term operation. The repository favors explicit governance over informal convention, evidence over preference, and continuity over short-term convenience.

No document in this repository should use speculative marketing language, unresolved draft text, or implementation shortcuts. Every change should improve clarity, traceability, and operational reliability.

## Ratification

This document is ratified as part of the Sprint 0 repository bootstrap. Amendments require review under the Engineering Constitution and must preserve the authority chain defined above.
