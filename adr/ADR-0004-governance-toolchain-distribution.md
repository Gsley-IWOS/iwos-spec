# ADR-0004: Distribute the Governance Toolchain from `tools/` Until a Dedicated Repository Exists

**Document ID:** ADR-0004  
**Version:** 1.0.0  
**Status:** Proposed  
**Date:** 2026-11-09  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** standards/repository-standard.md, adr/ADR-0002-repository-validation-tooling.md, governance/decision-process.md  
**Last Updated:** 2026-11-09

## Purpose

This record decides where the IWOS Guard reference toolchain lives, how it is packaged and how it is distributed, given that the Repository Standard permits code in this repository only for validation tooling and that the Architecture Baseline places runtime implementations in a separate implementation repository.

## Context

AIP-0002 authorises a reference toolchain: a command-line interface, a continuous-integration action and a Model Context Protocol server that verify a repository against its constitution. The Repository Standard requirement 3 forbids implementation-specific code here unless explicitly required for validation tooling. The Architecture Baseline assigns compiler, runtime, SDK and command-line implementation to the `IWOS` repository, which does not yet exist with content. The programme has one repository with continuous integration, a validator and an audience today.

## Decision Drivers

- The Repository Standard's allowance for validation tooling, and the boundary it implies.
- ADR-0002, which already fixed Python, PyYAML and jsonschema as the toolchain of this repository.
- Time to first external user: a GitHub Action is consumed by reference to a repository and ref, so the repository that holds it is the distribution channel.
- Dogfooding: the toolchain must pass against this repository on every change.

## Options Considered

1. **Package the toolchain under `tools/iwos/` in this repository, ship the composite action from the repository root, and move to a dedicated repository when a second consumer exists.** Everything the toolchain does is verification of a repository against its constitution, which the Repository Standard permits. One continuous-integration pipeline validates the toolchain and the constitution together.
2. **Create a dedicated `iwos-guard` repository now.** Clean boundary, but it splits the audience, duplicates continuous integration and governance scaffolding before there is a consumer, and the maintainers have not yet created it.
3. **Place the toolchain in the `IWOS` implementation repository.** Consistent with the baseline's repository model, but that repository is empty and the toolchain is verification, not runtime.

## Decision

Option 1. The toolchain lives at `tools/iwos/` as a Python package with a `pyproject.toml`, installable with `pip install ./tools/iwos`, exposing the `iwos` command. The composite GitHub Action is `action.yml` at the repository root so consumers reference `Gsley-IWOS/iwos-spec@<ref>`. The repository's own constitution file `iwos.yaml` uses the `iwos-spec` profile, which delegates full validation to `tools/validate`. The toolchain must never contain product runtime code; the moment it needs to, or a second repository consumes it, it moves to a dedicated repository under a new decision record and this record is superseded.

## Consequences

- Positive: shipping is immediate, dogfooded and governed by the existing continuous integration.
- Positive: the Repository Standard is respected by construction, because every command verifies and none executes work.
- Negative: the repository carries two Python packages for a time; `tools/validate` remains the engine for this repository's own checks and `tools/iwos` wraps it. This is recorded, not hidden.
- Neutral: the action's ref is this repository's history; consumers pinning a tag get a stable toolchain.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
