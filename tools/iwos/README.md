# IWOS Guard

**Document ID:** TOOL-002  
**Version:** 0.1.0  
**Status:** Draft  
**Authority:** EWP-0004 (Approved); specification SPEC-ENGGOV-001 (Draft)  
**Parent Documents:** work-packages/EWP-0004.md, architecture/engineering-governance/SPEC-ENGGOV-001.md, adr/ADR-0004-governance-toolchain-distribution.md  
**Last Updated:** 2026-11-13

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
      - uses: Gsley-IWOS/iwos-spec@main
```

Point agents at the authority interface. For a Model Context Protocol client, register a stdio server:

```json
{ "mcpServers": { "iwos": { "command": "iwos", "args": ["--root", ".", "mcp"] } } }
```

## Commands

| Command | What it does | Exit code |
| --- | --- | --- |
| `iwos init` | Write the constitution, the first lock and the agent block. | 0, or 1 if a constitution exists (use `--force`). |
| `iwos validate` | Integrity of every protected artefact against the lock; decision-ledger structure; drafting markers and credential shapes; freshness of the agent block. In the `iwos-spec` profile, runs the repository's own validator as the engine. | 0 pass, 1 findings, 2 cannot run. |
| `iwos lock` | Regenerate the lock. Deterministic: unchanged artefacts produce an unchanged lock. Run only under valid authority, in the same change as the protected edit. | 0. |
| `iwos gate --base REF [--head REF] [--body FILE \| --body-env NAME] [--label L \| --labels-env NAME]` | Evaluate a revision range: protected changes need a proposal citation and a lock change; architecture changes need a decision citation; every change needs a traceability citation. Agents disclosed in commit identity, trailers, the description or labels are reported with their evidence source; reports print no e-mail addresses. `--format both --output report.md` writes Markdown and JSON; `--summary` appends to the GitHub step summary. | 0 pass, 1 blocking findings, 2 cannot run. |
| `iwos agents [--check]` | Regenerate the block between `<!-- iwos:begin -->` and `<!-- iwos:end -->` in each agent file, or fail if stale. | 0, or 1 when stale with `--check`. |
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

## The authority interface

Five tools, defined in SPEC-ENGGOV-001:

| Tool | Returns |
| --- | --- |
| `check_authority(path)` | Whether the path is protected or architectural, the patterns that matched, the process a change requires, and whether the lock currently matches. |
| `list_protected()` | Every protected artefact and its patterns. |
| `read_state()` | Profile, patterns, lock status, ledger size, latest decisions and, when present, the machine-readable engineering state. |
| `record_decision(title, context, decision, consequences, authority, related_files?)` | Appends a `proposed` entry to the ledger with the next `DEC-####` identifier. Never edits or deletes. |
| `validate()` | The findings of `iwos validate`. |

The server speaks JSON-RPC 2.0, one message per line, protocol versions 2025-06-18, 2025-03-26 and 2024-11-05. It never listens on a network port.

## What the gate cannot do

The gate fails a pull request; it cannot stop a merge. Configure branch protection so the `IWOS Guard` check is required and so that `CODEOWNERS` review covers protected paths. The integrity check proves that protected artefacts and the lock agree; it cannot tell an authorised regeneration from an unauthorised one, so the lock diff is reviewed by a human like any other diff.

Attribution rests on disclosure (ADR-0005). An agent that commits under a human identity and says nothing in the description or labels is invisible to the report, and the report says so. The blocking rules do not depend on who made the change.

## Development

```bash
make test-iwos    # end-to-end tests in throwaway git repositories
make guard        # iwos validate against this repository
```

## Ratification

This document is a Draft under EWP-0004 (Approved). It becomes Ratified when SPEC-ENGGOV-001 is ratified.
