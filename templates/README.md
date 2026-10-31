# Templates

**Document ID:** TPL-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-DOC-001 Documentation Standard  
**Parent Document:** standards/documentation-standard.md  
**Last Updated:** 2026-10-31

## Purpose

Templates make every document of a family start from the same structure, so that the Documentation Standard, the Architecture Standard and the Decision Process are satisfied by construction and the validator's structural checks pass on first run.

## Templates

| Template | ID | Produces | Governing requirements |
| --- | --- | --- | --- |
| [ADR template](adr-template.md) | TPL-002 | `adr/ADR-####-<kebab-title>.md` | STD-ARCH-001 Decision Records; GOV-003 |
| [AIP template](aip-template.md) | TPL-003 | `aip/AIP-####-<kebab-title>.md` | GOV-003 |
| [RFC template](rfc-template.md) | TPL-004 | `governance/rfc/RFC-####.md` | GOV-003 |
| [Standard template](standard-template.md) | TPL-005 | `standards/<area>-standard.md` | STD-DOC-001; STD-NAME-001 |
| [Specification template](specification-template.md) | TPL-006 | Component and engine specifications under milestone M2 | STD-ARCH-001; STD-SEC-001; STD-DOC-001 |
| [Work package template](work-package-template.md) | TPL-007 | `work-packages/EWP-####.md` | PG-001 Section 4 |

## Using a Template

1. Copy the fenced block of the template into the new file. The fence delimiters are not part of the document.
2. Replace every token in angle brackets. No token may remain.
3. Set Version to `1.0.0` for a new document, or `0.1.0-draft.1` for a draft that is not yet ready for ratification.
4. Set Status to the initial state the family defines: `Ratified` for standards and specifications on ratification, `Proposed` for ADRs and work packages, `Draft` for AIPs, `Open` for RFCs. The deciding authority sets the final state.
5. Run `make validate`.

## Changing a Template

A template change is a Normative change under the Change Control Policy when it adds or removes a required section, otherwise Clarifying. A change that adds a required section must also update the validator configuration in `tools/validate/config.yaml` so the new section is checked.

## Ratification

This index is ratified under the Documentation Standard. It is effective on merge to `main` by an authorised human maintainer.
