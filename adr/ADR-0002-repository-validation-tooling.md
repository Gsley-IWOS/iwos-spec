# ADR-0002: Repository Validation Tooling in Python under `tools/validate/`

**Document ID:** ADR-0002  
**Version:** 1.0.0  
**Status:** Proposed  
**Date:** 2026-10-31  
**Authority:** Architecture Authority under GOV-002  
**Parent Documents:** standards/testing-standard.md, standards/repository-standard.md  
**Last Updated:** 2026-10-31

## Purpose

This record decides how the Testing Standard is enforced automatically in the IWOS specification repository: the language, dependencies, location and scope of the validator, and how it runs in continuous integration.

## Context

The Testing Standard requires four categories of check on every change: structural, schema, consistency and example. The Engineering Standard requires work to pass applicable checks before review. The Repository Standard prohibits implementation code except where explicitly required for validation tooling. Earlier pull requests validated by hand with ad-hoc inline scripts that were not committed, so their checks could not be reproduced.

## Decision Drivers

- Every check must be deterministic, reproducible and runnable locally and in continuous integration, as the Testing Standard requires.
- Dependencies must be minimal and widely available so that any contributor or agent can run the checks.
- The tool must be small enough to be reviewed in full and must itself be tested.
- The tool must not grow into an implementation of IWOS; it validates the specification only.

## Options Considered

1. **Python 3.10+ with PyYAML and jsonschema, in `tools/validate/`, invoked through `make validate`, with unit tests run through `make test`.** Python is present in every mainstream continuous-integration image; the two dependencies are the reference implementations for YAML parsing and JSON Schema 2020-12 validation.
2. **Node.js with ajv and markdownlint.** Comparable capability; heavier dependency tree; two ecosystems to maintain if Python is later needed for other tooling.
3. **Shell scripts with grep and yq.** Not portable across shells and operating systems; hard to test; poor error reporting.
4. **Hosted documentation linting service.** External dependency and trust boundary; checks not reproducible offline.

## Decision

Option 1. The validator is `tools/validate/validate.py`, configured by `tools/validate/config.yaml`, with unit tests in `tools/validate/test_validate.py`. It implements the four categories of the Testing Standard plus the constitutional integrity check defined by the Change Control Policy, and it generates the integrity lock on request. It is invoked through a root `Makefile` and by `.github/workflows/validate.yml` on every pull request and push to `main`. Its dependencies are Python 3.10 or later, PyYAML and jsonschema. It must not import, execute or depend on any IWOS implementation.

Exemptions from a check are recorded in `config.yaml` with a reason and are reviewed like any other change. The tool never silently skips a file.

## Consequences

- Positive: every check in the Testing Standard runs identically for every contributor and in continuous integration; a failing check blocks merge.
- Positive: `tools/` is the only place program code is permitted in this repository, and this record says why. The root `Makefile` and `.github/workflows/validate.yml` are invocation glue, not program code.
- Negative: contributors need Python and two packages; the README and workflow document the installation.
- Neutral: `tools/` is an addition to the directory list in the Repository Standard. The standard permits validation tooling; the directory's existence is recorded here and in `README.md`.

## Ratification

This record is accepted by the Architecture Authority on merge to `main`. It is immutable thereafter except as the Decision Process permits.
