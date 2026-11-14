# IWOS Guard

**Document ID:** TOOL-002  
**Version:** 0.2.0  
**Status:** Draft  
**Authority:** EWP-0004 and EWP-0006 (Approved); specification SPEC-ENGGOV-001 (Draft)  
**Parent Documents:** work-packages/EWP-0004.md, work-packages/EWP-0006.md, architecture/engineering-governance/SPEC-ENGGOV-001.md, adr/ADR-0006-iwos-guard-dedicated-repository.md, adr/ADR-0007-gate-judges-against-base-constitution.md  
**Last Updated:** 2026-11-14

## Purpose

IWOS Guard is constitution-as-code for repositories that AI agents change. You declare which documents are protected and which paths are architecture. The toolchain locks the protected documents with SHA-256 digests, fails any pull request that changes them without an accepted proposal, requires a decision record for architecture changes, reports which agents touched the change, and lets any agent that speaks the Model Context Protocol ask for authority before it edits a file.

It is the reference implementation of the Verification Engine and Decision Ledger of Architecture Baseline AB-1.0 in the domain of AI-assisted engineering, as specified in SPEC-ENGGOV-001. Every command verifies or records. None executes work, and none writes to a protected artefact.

## Why

Coding agents from every provider read `AGENTS.md` and then do what they think best. They rewrite architecture documents, skip decision records and lose the reason a choice was made. This repository's own history holds a pull request in which an agent replaced the ratified Founding Charter and Architecture Baseline with summaries, removing 1,266 lines, and sat mergeable for 92 days. The gate fails that change in seconds. Read the [case study](CASE-STUDY.md); the report in it is reproducible. Advice tells an agent the rules. A gate proves they were followed.

## Install

```bash
pip install "git+https://github.com/Gsley-IWOS/iwos-spec.git#subdirectory=tools/iwos"
pip install ./tools/iwos          # or, from a checkout of Gsley-IWOS/iwos-spec
iwos --version
```

Requires Python 3.10 or later, PyYAML and jsonschema.

## Quickstart for any repository

```bash
cd your-repo
iwos init --protected "docs/architecture/**" --protected "GOVERNANCE.md" --architecture "src/core/**"
git add iwos.yaml .iwos AGENTS.md && git commit -m "Adopt an IWOS constitution (#1)"
```

`init` writes `iwos.yaml` (the constitution), `.iwos/lock.yaml` (the integrity lock) and a generated block in `AGENTS.md` that tells agents the rules and how to ask for authority. Then add the Action to a pull-request workflow:

```yaml
on: [pull_request]
permissions: { contents: read }
jobs:
  guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }      # the gate needs the base revision
      - uses: Gsley-IWOS/iwos-spec@<commit>   # pin a full commit SHA and move the pin deliberately
```

Pin a commit, not a branch. A branch reference runs whatever the branch holds on the day; a pinned commit runs what you reviewed.

Point agents at the authority interface. For a Model Context Protocol client, register a stdio server:

```json
{ "mcpServers": { "iwos": { "command": "iwos", "args": ["--root", ".", "mcp"] } } }
```

## Commands

| Command | What it does | Exit code |
| --- | --- | --- |
| `iwos init` | Write the constitution, the first lock and the agent block. | 0, or 1 if a constitution exists (use `--force`). |
| `iwos validate [--sarif FILE]` | Integrity of every protected artefact against the lock; structure of the decision ledger, the waiver register and the incident ledger; drafting markers and credential shapes; freshness of the agent block. In the `iwos-spec` profile, runs the repository's own validator as the engine. | 0 pass, 1 findings, 2 cannot run. |
| `iwos lock` | Regenerate the lock. Deterministic: unchanged artefacts produce an unchanged lock. Run only under valid authority, in the same change as the protected edit. | 0. |
| `iwos gate --base REF [--head REF] [--body FILE \| --body-env NAME] [--label L \| --labels-env NAME] [--event-out FILE] [--record] [--sarif FILE]` | Evaluate a revision range against the constitution of the base revision: protected changes need a proposal citation and a lock change; architecture changes need a decision citation; every change needs a traceability citation. Agents disclosed in commit identity, trailers, the description or labels are reported with their evidence source; reports print no e-mail addresses. `--format both --output report.md` writes Markdown and JSON; `--summary` appends to the GitHub step summary. | 0 pass, 1 blocking findings, 2 cannot run. |
| `iwos agents [--check]` | Regenerate the block between `<!-- iwos:begin -->` and `<!-- iwos:end -->` in each agent file, or fail if stale. | 0, or 1 when stale with `--check`. |
| `iwos lessons [--format json]` | What the event log says changes in this repository break most often: rule identifiers, counts, the tool's own advice and the most affected paths. | 0. |
| `iwos stats` | An anonymous summary of the event log: rule identifiers and counts, nothing else. Printed, never sent. | 0. |
| `iwos events append FILE...` | Append event records written by `iwos gate --event-out` to `.iwos/events.jsonl`. | 0, 2 on a malformed record. |
| `iwos incident open --class C --severity S --summary TEXT [--path P]` | Open an incident in `.iwos/incidents.yaml` and print the playbook for its class. Refuses text that matches a credential pattern. | 0, 2 when refused. |
| `iwos incident update ID --status S --note TEXT [--decision REF]` / `list` / `playbook CLASS` | Move an incident forward (open, mitigated, closed), list incidents or print a playbook. | 0, 2 when refused. |
| `iwos mcp` | Serve the authority interface over standard input and output. | Runs until input closes. |

## The constitution file

`iwos.yaml` validates against `schemas/iwos-config.schema.json`.

| Key | Meaning |
| --- | --- |
| `profile` | `generic` for any repository; `iwos-spec` for this one, which takes protected patterns and the lock location from `tools/validate/config.yaml`. |
| `constitution.protected` | Globs of protected artefacts. `*` stays within a path segment; `**` spans segments. |
| `constitution.architecture` | Globs whose changes require a decision-record citation. |
| `constitution.lock_file`, `constitution.decision_ledger` | Where the lock and the ledger live. |
| `authority.proposal_pattern`, `authority.decision_pattern` | Regular expressions a citation must match (defaults `AIP-\d{4}`, `ADR-\d{4}`). |
| `authority.traceability_patterns`, `authority.traceability_required` | What counts as an authority citation for an ordinary change, and whether one is required. |
| `authority.lock_must_change_with_protected` | Whether a protected change must regenerate the lock in the same range. |
| `agents.files`, `agents.known_agent_markers` | Which files carry the generated block; which substrings identify an agent in authors and trailers. |
| `checks.*` | Drafting markers, credential patterns and exclusions for the content scan. |

## Rules

Every finding carries a stable rule identifier. Reports, event records, waivers and lessons refer to it.

| Rule | Blocks | Meaning |
| --- | --- | --- |
| `IWOS-G001` | yes | A protected artefact changed without a proposal citation. |
| `IWOS-G002` | yes | A protected artefact changed without the lock being regenerated in the same change. |
| `IWOS-G003` | yes, waivable | An architecture path changed without a decision-record citation. |
| `IWOS-G004` | yes, waivable | No authority citation in the description or commit messages. |
| `IWOS-G005` | yes | A control file changed without a proposal citation. |
| `IWOS-W001` to `IWOS-W007` | no | Lock changed alone; every commit from an agent; attribution by disclosure only; no agent disclosed; constitution adopted in this change; waiver ignored; gate automation changed. |
| `IWOS-V001`, `IWOS-V002`, `IWOS-V003` | fail `validate` | Integrity violation; credential pattern in content; any other validation finding. |

## The base constitution and control files

The gate judges a change against the constitution on the base revision, never against the constitution the change proposes (ADR-0007). A change cannot remove a protection and use the gap in the same step. The constitution file `iwos.yaml`, the waiver register `.iwos/waivers.yaml` and, in the `iwos-spec` profile, `tools/validate/config.yaml` are control files: a change to any of them needs a proposal citation whatever the constitution file says. Only when the base revision holds no valid constitution is the change judged against its own, and the report says so with `IWOS-W005`.

## Waivers

A waiver is a recorded, owned and dated exception to `IWOS-G003` or `IWOS-G004`. It is read from the base revision, so a change cannot waive itself. The protection rules cannot be waived.

```yaml
# .iwos/waivers.yaml
schema_version: "1.0.0"
waivers:
  - id: WVR-0001
    rule: IWOS-G003
    paths: ["src/core/generated/**"]
    owner: platform-team
    reason: Generated code is rebuilt weekly from the schema.
    expires: 2027-03-31
```

A waived finding stays in the report, marked with the waiver. An expired or malformed waiver is ignored by the gate (`IWOS-W006`) and fails `iwos validate` until it is removed or renewed.

## The learning loop

Each gate run produces a structured event record: rule identifiers, levels, paths, counts and revisions. It holds no commit subject, no description text, no author name and no e-mail address. `iwos gate --record` appends it to `.iwos/events.jsonl`; the action writes it to `iwos-gate-event.json` so that a workflow can keep it as an artefact and a maintainer can fold it in with `iwos events append`.

`iwos lessons` and the `read_lessons` tool turn that log into feedback for the next agent. Every string in the output is a rule identifier, advice from the tool's own rule catalogue or a path made only of plain path characters. Text found in the repository is never repeated, so the log cannot be used to plant instructions for an agent. The tool sends nothing anywhere; `iwos stats` prints an anonymous summary that a maintainer may choose to share.

## Incidents

`iwos incident open` records a security incident in `.iwos/incidents.yaml` with the next `INC-####` identifier, a class, a severity and the affected paths, and prints the playbook for the class. Classes: `secret-exposure`, `integrity-violation`, `unauthorised-protected-change`, `gate-bypass`, `agent-misattribution`, `other`. An incident moves forward only (open, mitigated, closed); each step is appended to its history, and closing it can name the decision record that prevents a repeat. The ledger never holds the sensitive value: text that matches a credential pattern is refused.

To show findings in GitHub code scanning, upload the SARIF file the action writes. This needs `security-events: write`, so it is a step in your workflow and not part of the action:

```yaml
    permissions: { contents: read, security-events: write }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - id: guard
        uses: Gsley-IWOS/iwos-spec@<commit>
      - if: always() && github.event_name == 'pull_request'
        uses: github/codeql-action/upload-sarif@v4
        with: { sarif_file: iwos-gate.sarif, category: iwos-guard }
```

## The authority interface

Eight tools, defined in SPEC-ENGGOV-001:

| Tool | Returns |
| --- | --- |
| `check_authority(path)` | Whether the path is protected, a control file or architectural, the patterns that matched, the process a change requires, and whether the lock currently matches. |
| `list_protected()` | Every protected artefact and its patterns. |
| `read_state()` | Profile, patterns, lock status, ledger size, latest decisions and, when present, the machine-readable engineering state. |
| `record_decision(title, context, decision, consequences, authority, related_files?)` | Appends a `proposed` entry to the ledger with the next `DEC-####` identifier. Never edits or deletes. |
| `validate()` | The findings of `iwos validate`. |
| `read_lessons(limit?)` | The lessons of the event log, as structured fields. |
| `report_incident(incident_class, severity, summary, paths?)` | Opens an incident and returns the playbook for its class. Refuses text that matches a credential pattern. |
| `list_incidents()` | The incidents that are not closed. |

The server speaks JSON-RPC 2.0, one message per line, protocol versions 2025-06-18, 2025-03-26 and 2024-11-05. It never listens on a network port.

## What the gate cannot do

The gate fails a pull request; it cannot stop a merge. Configure branch protection so the `IWOS Guard` check is required and so that `CODEOWNERS` review covers protected paths. The integrity check proves that protected artefacts and the lock agree; it cannot tell an authorised regeneration from an unauthorised one, so the lock diff is reviewed by a human like any other diff.

The gate checks that a citation is present. It does not check that the cited proposal exists or was accepted; that is the reviewer's check, and the report lists the citations so that the reviewer can make it.

A pull request can edit the workflow that runs the gate, and on a pull request GitHub runs the edited workflow. The gate reports a change to `.github/workflows/` with `IWOS-W007`, but a workflow edited to skip the gate never produces that report. Require the check by name in branch protection, keep `.github/` under `CODEOWNERS`, and treat a pull request that touches the workflow as one a human reads in full.

Attribution rests on disclosure (ADR-0005). An agent that commits under a human identity and says nothing in the description or labels is invisible to the report, and the report says so. The blocking rules do not depend on who made the change.

## Development

```bash
make test-iwos    # end-to-end tests in throwaway git repositories
make guard        # iwos validate against this repository
```

## Ratification

This document is a Draft under EWP-0004 and EWP-0006 (Approved). It becomes Ratified when SPEC-ENGGOV-001 is ratified.
