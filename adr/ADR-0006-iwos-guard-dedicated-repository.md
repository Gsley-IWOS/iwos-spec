# ADR-0006: IWOS Guard Is Developed and Released from a Dedicated Repository

**Document ID:** ADR-0006  
**Version:** 1.0.0  
**Status:** Accepted  
**Date:** 2026-11-14  
**Authority:** Architecture Authority under GOV-002  
**Supersedes:** ADR-0004  
**Parent Documents:** engineering-charter/02_ARCHITECTURE_BASELINE.md, standards/repository-standard.md, governance/versioning-policy.md, adr/ADR-0002-repository-validation-tooling.md, governance/decision-process.md  
**Last Updated:** 2026-11-14

## Purpose

This record decides where the IWOS Guard toolchain lives, how it is versioned and how this repository uses it. It supersedes ADR-0004, which proposed keeping the toolchain under `tools/` until a second consumer existed.

## Context

ADR-0004 was drafted while the toolchain had one consumer, this repository. It was held at `Proposed` (DEC-0009) because two facts cut against it. First, announcing the toolchain creates consumers on the day of the announcement, so "move when a second consumer exists" means moving after the address has been published. Second, the Versioning Policy reserves tags of the form `v<MAJOR>.<MINOR>.<PATCH>` in this repository for releases of the specification; a tag for the toolchain would collide with them or need a second scheme in the same namespace.

The Architecture Baseline states that the IWOS ecosystem consists of multiple repositories and lists reference implementations among the future ones. This repository's own onboarding states that it is not an implementation repository. On 2026-11-14 the repository owner directed that the recommendation to give IWOS Guard its own repository be implemented.

## Decision Drivers

- A consumer pins `owner/repository@revision`. The address should name the product and should not change after launch.
- Releases of the specification and releases of the toolchain move at different speeds and must not share a tag namespace.
- A visitor to the toolchain should meet a short product README, not a constitutional repository.
- The specification and the constitution schema remain constitutional artefacts and stay under this repository's change control.
- The toolchain must keep proving itself on this repository on every pull request.

## Options Considered

1. **A dedicated repository, `Gsley-IWOS/iwos-guard`.** Own README, own tags, own constitution file, own continuous integration. This repository pins a released commit. Costs one more repository to maintain and a rule for keeping the bundled schema equal to the canonical one.
2. **Stay under `tools/` (ADR-0004).** No move, but the published address is a specification repository, the tag namespace is shared and the product cannot be versioned on its own.
3. **Stay under `tools/` with a prefixed tag scheme.** Avoids the tag collision but not the other costs, and adds a second scheme to the Versioning Policy, a protected document.

## Decision

Option 1. IWOS Guard is developed and released from a dedicated repository named `iwos-guard` in the `Gsley-IWOS` organisation.

1. The dedicated repository holds the package, its tests, the composite action at its root, the case study, its own security policy and its own constitution file, and is governed by the toolchain it contains.
2. Releases of the toolchain are tagged in the dedicated repository only. No tag for the toolchain is created in this repository.
3. This repository remains the home of SPEC-ENGGOV-001 and of `schemas/iwos-config.schema.json`, which is the canonical contract. The copy bundled with the toolchain must equal it, and the toolchain's tests assert that.
4. After the move this repository consumes the action by a pinned commit of the dedicated repository, and `tools/iwos/` and the root `action.yml` are removed here in the same change that adds the pin.
5. Until the dedicated repository exists and holds a release, the toolchain stays in `tools/iwos/` under the rules ADR-0002 sets for tooling, consumers are told to pin a commit of this repository, and the README of the toolchain says so.

Creating a repository in the organisation is an act of the organisation's owner. The automation that drafted this record was refused that permission by the hosting platform on 2026-11-14, so items 1, 2 and 4 are carried out when the owner has created the repository.

## Consequences

- Positive: the product has a stable address, its own version history and a README written for adopters.
- Positive: the specification's tags keep one meaning.
- Positive: the specification repository returns to holding law and its validator, as its onboarding says.
- Negative: two repositories must be kept in step. The schema equality test and the pinned commit make drift visible; they do not prevent it.
- Negative: until the move is made, the published address is this repository and will change once. Item 5 limits the cost by asking consumers to pin a commit, which keeps working after the move.
- Neutral: the `iwos-spec` profile of the toolchain, which reads `tools/validate/config.yaml`, remains until this repository's constitution file states its protected patterns itself; removing it is a later change.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
