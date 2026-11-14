# ADR-0008: Learning from Gate History and Recording Incidents, Without Telemetry

**Document ID:** ADR-0008  
**Version:** 1.0.0  
**Status:** Accepted  
**Date:** 2026-11-14  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** architecture/engineering-governance/SPEC-ENGGOV-001.md, engineering-charter/02_ARCHITECTURE_BASELINE.md, standards/security-standard.md, adr/ADR-0005-agent-attribution-by-disclosure.md, governance/decision-process.md  
**Last Updated:** 2026-11-14

## Purpose

This record decides how a governed repository learns from the changes its gate has judged, how exceptions to a rule are recorded, how security incidents are recorded and worked, and what data may leave the repository in the process.

## Context

The gate produced a report for each change and then forgot it. An agent starting work had no way to learn which rules changes in that repository break most often, and a maintainer who wanted to permit a recurring, justified exception could only weaken the rule for everyone. When `iwos validate` found a committed credential or an integrity failure, the toolchain printed a finding and offered nothing further: no record, no steps, no way to show that the matter was closed.

The Architecture Baseline requires every decision to be explainable and auditable. SPEC-ENGGOV-001 states that the implementation needs no network access and retains nothing outside the repository. Feeding repository history back to an agent opens a channel for instruction injection: text that a change places in a log could be read by the next agent as an instruction.

## Decision Drivers

- Feedback to an agent must not carry text an attacker can write.
- A toolchain that enforces accountability must not collect data silently.
- An exception must be owned, dated and visible, or it is a hole.
- An incident record must never become a second copy of the secret it describes.
- The records must survive without a service: they are files in the repository.

## Options Considered

1. **Local, structured records in the repository; feedback assembled from rule identifiers and the toolchain's own text; no transmission.**
2. **A hosted service that collects gate results across repositories.** Richer comparison, but it requires network access, an account and trust in the collector, and contradicts the specification's data handling.
3. **Free-text lessons written by agents or maintainers into the agent file.** Simple, but it is the injection channel described above, and it rots.
4. **No learning loop; rely on the report of each change.** Leaves the gaps stated in the context.

## Decision

Option 1.

1. **Rule identifiers.** Every finding carries a stable identifier. Reports, event records, waivers and lessons refer to it.
2. **Event record.** Each gate run can emit a structured record: rule identifiers, levels, paths, counts and the two revisions. It contains no commit subject, no description text, no author name and no e-mail address. Records are appended to an event log in the repository; existing lines are never rewritten.
3. **Lessons.** The toolchain summarises the event log for agents, through the command line and the authority interface. Every string in a lesson is a rule identifier, advice held in the toolchain's own rule catalogue, or a path made only of plain path characters. Nothing else from the repository is repeated.
4. **Waivers.** An exception names a waivable rule, the paths it covers, an owner, a reason and an expiry date, and is read from the base revision. The rules that protect artefacts and control files cannot be waived. A waived finding stays in the report. An expired or malformed waiver is ignored by the gate and fails validation.
5. **Incident ledger.** An incident has an identifier, a class, a severity, a status, a summary, the affected paths and a history. It moves forward only, each step is appended, and closing it may name the decision record that prevents a repeat. The toolchain refuses any text that matches a credential pattern, and prints a fixed playbook for the incident's class.
6. **Reporting outward.** Findings can be written as SARIF 2.1.0 so that a maintainer may upload them to a code-scanning service. The upload is a step the maintainer adds; the action does not request the permission it needs.
7. **No telemetry.** The toolchain transmits nothing. An anonymous summary, rule identifiers and counts only, can be printed for a maintainer who chooses to share it.
8. **Vulnerabilities in the toolchain** are reported privately to its maintainers under this repository's security policy, fixed with a regression test and published in a security advisory.

## Consequences

- Positive: an agent can ask what goes wrong here before it starts, and the answer cannot be poisoned with instructions.
- Positive: exceptions and incidents become reviewable records with owners and dates.
- Positive: the specification's statement that nothing leaves the repository stays true.
- Negative: the event log grows only where someone records events. On a hosted runner the record is a file in the run's workspace; keeping it means storing it as an artefact and appending it, or recording locally. Nothing learns across repositories unless maintainers share the anonymous summary by hand.
- Negative: a path can still carry words. The character and length limits reduce what a path can say; they do not make a path meaningless.
- Neutral: incident identifiers of the form `INC-####` and waiver identifiers of the form `WVR-####` are record identifiers inside a governed repository's own ledgers, in the same way as `DEC-####`. They are not document identifier families of this repository, and the Naming Standard is not amended.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
