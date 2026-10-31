# ADR-0001: Record Architecture Decisions as ADRs in `adr/`

**Document ID:** ADR-0001  
**Version:** 1.0.0  
**Status:** Proposed  
**Date:** 2026-10-31  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** standards/architecture-standard.md, governance/decision-process.md  
**Last Updated:** 2026-10-31

## Purpose

This record establishes Architecture Decision Records as the mechanism for durable technical decisions in IWOS, fixes their location, format and lifecycle, and is itself the first such record.

## Context

The Founding Charter requires every decision to be traceable and every action auditable. The Architecture Baseline makes a Decision Ledger a constitutional component of IWOS and names Decision Memory a category of engineering memory. The Architecture Standard requires decision records with status, date, authority, decision drivers, selected decision and consequences, and the Repository Standard reserves `adr/` for them.

Earlier drafts placed a decision record in `governance/`, used a format without the required metadata and did not define a lifecycle. Without a fixed location and format, decisions scatter across pull requests and conversations and are lost.

## Decision Drivers

- Traceability and auditability required by the Founding Charter and Architecture Baseline.
- Conformance to the Architecture Standard's required content and to the Repository Standard's layout.
- Machine-checkability: the validator must be able to confirm that every record is complete.
- Immutability of accepted decisions so that history is never rewritten.

## Options Considered

1. **Dedicated records in `adr/`, one file per decision, fixed template, index as allocation register.** Conforms to both standards; checkable; conventional.
2. **Decision records inside `governance/`.** Mixes authority policy with technical decisions; contradicts the Repository Standard.
3. **Decisions recorded only in `.ai/DECISION_GRAPH.yaml`.** Machine-readable but poorly suited to long rationale and review; the graph is memory, not authority.
4. **Decisions recorded in pull request descriptions only.** Not versioned with the repository; lost when hosting changes.

## Decision

Option 1. Every durable technical decision within the Architecture Baseline is recorded as a file `adr/ADR-####-<kebab-title>.md` created from `templates/adr-template.md`, with the metadata Status, Date and Authority and the sections Context, Decision Drivers, Options Considered, Decision and Consequences. `adr/README.md` is the allocation register. Lifecycle states are Proposed, Accepted, Rejected, Deprecated and Superseded as defined in the Decision Process. An accepted record is immutable except for administrative correction or a supersession note. Non-architectural decisions are recorded in `.ai/DECISION_GRAPH.yaml` and reference any related record.

## Consequences

- Positive: decisions are discoverable, reviewable, versioned and checkable; the register makes identifier allocation unambiguous.
- Positive: decision memory, a category of engineering memory named by the Architecture Baseline, exists from the first decision onward.
- Negative: every durable decision costs a file and a review; this is the intended price of traceability.
- Neutral: the decision graph and the ADR register must be kept consistent; the validator checks that every record path named in the graph exists.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
