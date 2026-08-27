# IWOS Project Genesis

**Purpose:** Define the origin, repository role, and initial scope boundaries for IWOS.

**Authority:** engineering-charter/00_FOUNDING_CHARTER.md

**Version:** 1.0.0

**Status:** Ratified bootstrap baseline

**Parent document:** engineering-charter/00_FOUNDING_CHARTER.md

---

## Purpose

Project Genesis records the initial engineering context for IWOS and establishes the distinction between specification authority and implementation activity.

## Repository Role

`iwos-spec` is the constitutional specification repository for IWOS. It defines the durable documents used to govern architecture, standards, schemas, review, and AI-agent participation.

## Implementation Relationship

The `IWOS` implementation repository consumes the specifications defined here. Implementation evidence may inform future proposals, but approved specifications remain authoritative until changed through governance.

## Initial Scope

Sprint 0 establishes the repository foundation:

- Root onboarding and authority documents.
- Engineering charter documents.
- Required top-level directories for governance, architecture, standards, schemas, templates, examples, ADRs, AIPs, GitHub configuration, and AI metadata.
- Machine-readable AI onboarding and contract files.

## Boundary Conditions

This repository does not bootstrap product runtime code, deployment automation, production services, or customer-facing product assets. Those concerns belong to implementation repositories unless a ratified specification requires otherwise.

## Ratification

This document is ratified as the Sprint 0 project genesis record. Amendments require review under the Engineering Constitution.
