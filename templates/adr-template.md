# Architecture Decision Record Template

**Document ID:** TPL-002  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-ARCH-001 Architecture Standard  
**Parent Documents:** standards/architecture-standard.md, governance/decision-process.md  
**Last Updated:** 2026-10-31

## Purpose

This template produces an Architecture Decision Record that satisfies the Architecture Standard's required content (status, date, authority, decision drivers, selected decision, consequences, context and alternatives) and the Decision Process lifecycle. Copy the fenced block below into `adr/ADR-####-<kebab-title>.md`; the fence is not part of the record.

## Template

```markdown
# ADR-<####>: <Title in sentence case>

**Document ID:** ADR-<####>  
**Version:** 1.0.0  
**Status:** Proposed  
**Date:** <YYYY-MM-DD>  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** <ratified document this decision operates within>, governance/decision-process.md  
**Last Updated:** <YYYY-MM-DD>

## Purpose

<One paragraph: what this record decides and why a record is needed.>

## Context

<The situation that requires a decision. Cite the ratified documents, work package or proposal that give rise to it. State what happens if no decision is taken.>

## Decision Drivers

- <Driver: a requirement, constraint or quality attribute, with its source.>
- <Driver.>

## Options Considered

1. **<Option 1.>** <Strengths and weaknesses against the drivers.>
2. **<Option 2.>** <Strengths and weaknesses.>
3. **<Option 3.>** <Strengths and weaknesses.>

## Decision

<The option selected, stated as a rule future work must follow. Name the artefacts it binds.>

## Consequences

- Positive: <consequence>.
- Negative: <consequence and how it is mitigated>.
- Neutral: <consequence>.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
```

## Rules

- Status on first submission is `Proposed`; the Architecture Authority sets `Accepted` on merge.
- A record that would require a change to a protected document, policy or standard stays `Proposed` until the corresponding Architecture Improvement Proposal is accepted.
- A superseding record adds the line `**Supersedes:** ADR-<####>` to its metadata, and the superseded record gains `**Superseded By:** ADR-<####>` and status `Superseded`.

## Ratification

This template is ratified under the Architecture Standard. It is effective on merge to `main` by an authorised human maintainer.
