# ADR-0007: The Gate Judges a Change Against the Constitution of Its Base

**Document ID:** ADR-0007  
**Version:** 1.0.0  
**Status:** Accepted  
**Date:** 2026-11-14  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** architecture/engineering-governance/SPEC-ENGGOV-001.md, standards/security-standard.md, governance/change-control-policy.md, governance/decision-process.md  
**Last Updated:** 2026-11-14

## Purpose

This record decides which copy of the constitution the gate applies to a proposed change, which files are protected regardless of what the constitution file says, and what the gate reports when the automation that runs it is itself changed. It closes a way round the gate found on 2026-11-14.

## Context

Until this record, the gate read the constitution file from the working tree, which on a pull request is the head of the change. A single change could therefore remove a pattern from `iwos.yaml`, rewrite the file that pattern had protected, regenerate the lock and the agent block, and pass. The working tree was consistent with itself, so `iwos validate` passed; the rewritten file was no longer protected under the constitution the gate read, so `iwos gate` passed with one warning about the lock. The steps were reproduced in a throwaway repository on 2026-11-14 with toolchain version 0.1.0 and are kept as a regression test. In this repository the same exposure existed through `tools/validate/config.yaml`, where the `iwos-spec` profile reads its protected patterns.

An independent adversarial review of the first fix, on the same day, found that a rename or a symbolic link could still hide a protected artefact from the gate, that paths the version-control system quotes never matched a pattern, and that the lock and the gate disagreed on some globs. Items 6 and 7 of the decision answer those findings, and each has a regression test.

No change that used this path was merged here. The history of `iwos.yaml` and `tools/validate/config.yaml` holds two commits, made under EWP-0003 and EWP-0004, and the protected patterns are the same in both: `engineering-charter/*`, `standards/*-standard.md` and `governance/*.md`. No pattern has ever been removed.

## Decision Drivers

- The Security Standard requires default behaviour to prefer least privilege, explicit authorisation and safe failure.
- A rule that the governed party can rewrite in the act it governs is not a rule.
- A repository must still be able to adopt a constitution, and to amend one through its own process.
- The gate must not claim more than it can check.

## Options Considered

1. **Judge against the constitution on the base revision, and treat the files that define the rules as protected whatever they say.** Closes the path; adoption needs a stated exception.
2. **Judge against the stricter of base and head.** Also closes the path, but makes the result depend on a merge of two rule sets that no reviewer has read as one document.
3. **Keep reading the head and add the constitution file to its own protected patterns by default.** A change can still remove that default in the same step.
4. **Leave the gate as it was and rely on code-owner review of `iwos.yaml`.** Review is necessary but is the control the gate exists to back up.

## Decision

Option 1.

1. The gate reads the constitution file, and in the `iwos-spec` profile the validator configuration, from the base revision of the range it evaluates. The constitution a change proposes takes effect for the changes that follow it.
2. The constitution file, the waiver register and, in the `iwos-spec` profile, the validator configuration are control files. A change to a control file requires a proposal citation of the kind the base constitution declares, whatever patterns the constitution file contains. This rule cannot be waived.
3. When the base revision holds no constitution, or one that does not parse or validate, the gate judges the change against the constitution the change proposes and says so in the report. This is the adoption case. A constitution that fails to parse at the head never disables the gate while the base holds a valid one.
4. Waivers are read from the base revision, so a change cannot waive itself.
5. The gate reports, as a warning, any change to the automation that runs it: workflow files, and in this repository the toolchain, the validator and the action definition. A result produced by a changed gate is not independent, and the report says so.
6. A moved or renamed file is a change at its old path and at its new one. The gate does not follow renames, so moving a protected artefact or a control file away, or replacing it with a symbolic link, is judged as a change to it. The lock and the gate use one matcher, so a path the gate protects is a path the lock records.
7. The base revision is the target branch as it stands. A stale base lets commits already merged there lend their citations to the change, so the action judges against the first parent of the pull request's merge commit when the checkout is that commit. The gate runs only at the top of the work tree.
8. The gate checks that a citation is present. It does not check that the cited proposal exists or was accepted. That remains a reviewer's check, and conforming documentation says so.

## Consequences

- Positive: a change cannot remove a protection and use the gap in the same step.
- Positive: amending the constitution becomes a visible, cited act, separate from the changes it enables.
- Negative: a change that both tightens the constitution and relies on the tightened rule is judged by the older rule. The tightening merges first.
- Negative: a pull request can still edit the workflow so that the gate never runs. The gate cannot report on a run that did not happen. Requiring the check by name in branch protection, and code-owner review of `.github/`, are the controls for that, and they are settings on the hosting platform.
- Neutral: the report format gains a statement of which constitution was applied, a control-files section and rule identifiers; `report_version` becomes 1.2.0.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
