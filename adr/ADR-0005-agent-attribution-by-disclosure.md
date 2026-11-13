# ADR-0005: Agent Attribution Rests on Disclosure, and Reports Print No Addresses

**Document ID:** ADR-0005  
**Version:** 1.0.0  
**Status:** Proposed  
**Date:** 2026-11-13  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** architecture/engineering-governance/SPEC-ENGGOV-001.md, standards/security-standard.md, governance/decision-process.md  
**Last Updated:** 2026-11-13

## Purpose

This record decides how the gate attributes a change to an AI agent, what it claims when it finds no agent, and what personal data its reports may contain.

## Context

SPEC-ENGGOV-001 requires the gate to report agent attribution found in commit trailers. Replaying this repository's first agent pull request through the gate showed the limit of that rule. The agent committed under the repository owner's identity with no trailer. The only evidence of an agent was a task link in the pull request description and a label. A report built from commit metadata alone said "agents detected: none", which a reader would take as a finding of fact. The same replay printed the commit author's e-mail address in the report.

## Decision Drivers

- The Founding Charter requires intelligence to be verifiable; a report must not assert more than its evidence supports.
- The Security Standard requires specifications that handle data to address confidentiality; an address in a build summary is disclosed more widely than in commit metadata.
- Repository data cannot prove the absence of an agent. Only a platform-level identity for agents could, and none is common to every provider.
- The gate's blocking rules do not depend on who made a change, so attribution can be honest about its limits without weakening enforcement.

## Options Considered

1. **Report what is disclosed, name the evidence source, and say plainly that silence proves nothing.** Sources: commit identity, commit trailers, known signatures in the pull request description, and pull request labels. Truthful, cheap and useful; cannot detect an agent that discloses nothing.
2. **Infer agents from style or diff shape.** Unreliable, unexplainable and likely to accuse humans; contradicts verifiable intelligence.
3. **Require a signed agent identity on every commit.** The right long-term answer, but no cross-provider standard exists today and a requirement nobody can meet would block every change.
4. **Drop attribution.** Loses the accountability view that distinguishes the gate from a linter.

## Decision

Option 1. The gate reports each agent with the source of the evidence: commit author, a named trailer, the pull request description, or a label. It labels the section "Agents disclosed". When nothing is disclosed it warns that this does not show no agent was involved. When an agent is disclosed only in the description or labels while every commit carries a human identity, it warns that attribution rests on disclosure alone. Blocking rules never depend on attribution. Reports, in every format, print names and never e-mail addresses. A conforming constitution may later require a signed agent identity when a cross-provider standard exists; that will be a new decision.

## Consequences

- Positive: the report's claims match its evidence, and the case that motivated the toolchain is reported correctly.
- Positive: build summaries and published reports carry no addresses.
- Negative: an agent that commits as a human and leaves no trace is invisible to attribution. The protected-artefact, architecture and traceability rules still apply to its change.
- Neutral: description signatures are heuristics maintained in the toolchain and will need additions as providers change their footers.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
