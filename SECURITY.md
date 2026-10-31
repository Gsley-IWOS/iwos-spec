# Security Policy

**Document ID:** ROOT-003  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-SEC-001 Security Standard  
**Parent Document:** standards/security-standard.md  
**Last Updated:** 2026-10-31

## Purpose

This policy states how security concerns in the IWOS specification repository are reported and handled, and which security rules bind every artefact committed here.

## Scope

This policy covers the contents of `iwos-spec`: documents, schemas, examples, templates, validation tooling and repository automation. Security of IWOS implementations is governed by the specifications those implementations conform to and is reported to the implementation repository.

## Reporting a Concern

Report a security concern by opening an issue with the `Defect` form in `.github/ISSUE_TEMPLATE/` and selecting the security classification. Do not include secrets, exploit payloads or personal data in the report. If the concern involves a committed secret, say only which file and commit are affected; maintainers will rotate and purge.

Maintainers acknowledge security reports within five working days and record the disposition in the issue.

## Rules That Bind Every Change

1. Secrets, credentials, tokens and private keys **must never** be committed. The continuous-integration workflow runs the repository validator; the validator rejects files that match common credential patterns.
2. Security-sensitive examples **must** use values that are clearly fake and cannot be mistaken for real credentials.
3. Any specification that describes execution **must** state its trust boundaries and the authority required to act.
4. Any specification that describes data handling **must** address confidentiality, integrity, retention and auditability.
5. Default behaviour described in any specification **must** prefer least privilege, explicit authorisation and safe failure.
6. Repository automation **must** run with the least privilege required. Workflows in `.github/workflows/` request read-only repository permissions unless a documented need requires more.

## Supported Versions

Only the content of `main` is supported. Historical tags remain available for traceability but are not maintained.

## Ratification

This policy is ratified under the Security Standard. It is effective on merge to `main` by an authorised human maintainer.
