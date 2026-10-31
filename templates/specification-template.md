# Specification Template

**Document ID:** TPL-006  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-ARCH-001 Architecture Standard  
**Parent Documents:** standards/architecture-standard.md, standards/security-standard.md, standards/documentation-standard.md  
**Last Updated:** 2026-10-31

## Purpose

This template produces a specification of a constitutional component or intelligence engine named in Architecture Baseline AB-1.0. It enforces the Architecture Standard's requirement that system boundaries name ownership, inputs, outputs and failure expectations, and the Security Standard's requirement that execution and data-handling specifications state trust boundaries, authority, confidentiality, integrity, retention and auditability. Copy the fenced block below into the location the authorising proposal names, by default `architecture/<component>/SPEC-<COMPONENT>-001.md`; the fence is not part of the specification. A specification requires an accepted Architecture Improvement Proposal.

## Template

```markdown
# <Component Name> Specification

**Document ID:** SPEC-<COMPONENT>-001  
**Version:** 0.1.0-draft.1  
**Status:** Draft  
**Authority:** <AIP-#### that authorised this specification>  
**Parent Documents:** engineering-charter/02_ARCHITECTURE_BASELINE.md, aip/AIP-<####>-<title>.md  
**Last Updated:** <YYYY-MM-DD>

## Purpose

<The component's purpose as the Architecture Baseline states it, and what this specification adds.>

## Scope

<What this specification defines, and what it leaves to other specifications or to implementation.>

## Authority

<The baseline section that names this component, the accepted proposal, and the layer the component serves.>

## Definitions

<Terms introduced by this specification that are not in architecture/glossary.md.>

## Boundary

| Aspect | Definition |
| --- | --- |
| Owner | <The subsystem or role accountable for the component.> |
| Inputs | <Every input, its source and its contract.> |
| Outputs | <Every output, its consumer and its contract.> |
| Failure expectations | <How the component fails, what it guarantees on failure, and how failure is observed.> |

## Contracts

<Every interface the component exposes, each with a stable identifier, versioning rule and a reference to its schema in schemas/.>

## Behaviour

<Normative behaviour using must, must not, should, should not and may. Include invariants.>

## Context Requirements

<Which of the seven context categories of the Architecture Baseline the component requires validated before execution.>

## Trust Boundaries and Authority

<Where trust changes; what authority is required for each action; least-privilege defaults; safe failure modes.>

## Data Handling

<Confidentiality, integrity, retention and auditability of every class of data the component handles.>

## Observability and Verification

<What the component records so that every recommendation, decision and action is explainable and auditable; how conformance is tested.>

## Compatibility

<Versioning of this specification and its contracts under governance/versioning-policy.md.>

## Decisions

<Architecture Decision Records that shaped this specification.>

## Ratification

This specification is ratified under the Architecture Standard on merge to `main` with status `Ratified` by the Architecture Authority. It remains in force until superseded by a later ratified version.
```

## Ratification

This template is ratified under the Architecture Standard. It is effective on merge to `main` by an authorised human maintainer.
