# Examples

**Document ID:** EX-001  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** STD-TEST-001 Testing Standard  
**Parent Documents:** standards/testing-standard.md, schemas/README.md  
**Last Updated:** 2026-10-31

## Purpose

The Testing Standard requires schema changes to be validated against representative valid and invalid examples. This directory holds those examples. Every example is illustrative: it demonstrates a schema and carries no authority. Values are synthetic and are not records of the real repository state.

## Layout

```text
examples/<schema-name>/valid/*.yaml     must be accepted by schemas/<schema-name>.schema.json
examples/<schema-name>/invalid/*.yaml   must be rejected by schemas/<schema-name>.schema.json
```

The directory name for each schema is fixed by `schemas/bindings.yaml`. The validator's example check fails when a schema has no valid example, no invalid example, a valid example is rejected, or an invalid example is accepted.

## Writing an Example

1. Start every file with a comment stating what it demonstrates. An invalid example breaks exactly one rule and declares the expected error with a comment line `# expect: <text>`; the validator requires at least one schema error whose path or message contains that text. An invalid example without an `expect` line fails validation.
2. Keep examples minimal: the smallest document that exercises the rule.
3. Use clearly synthetic values. Digests in `constitution-lock` examples are not digests of real files. Never use a value that resembles a credential.
4. Run `make validate`.

## Ratification

This index is ratified under the Testing Standard. It is effective on merge to `main` by an authorised human maintainer.
