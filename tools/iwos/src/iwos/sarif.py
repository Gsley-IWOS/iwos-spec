"""SARIF 2.1.0 output, so that findings can be uploaded to a code-scanning service."""
from __future__ import annotations

from urllib.parse import quote

from . import __version__, rules
from .redact import redact

SCHEMA = "https://json.schemastore.org/sarif-2.1.0.json"
LEVELS = {"error": "error", "warning": "warning", "note": "note"}


def build(results: list[dict], fallback_uri: str = "iwos.yaml", secret_patterns: list[str] | None = None) -> dict:
    """`results` items: {"rule": id, "level": error|warning|note, "message": str, "paths": [str]}.

    Messages and paths are redacted against the credential patterns, and paths are percent-encoded so
    that every location is a valid relative URI.
    """
    patterns = secret_patterns or []
    used = sorted({r["rule"] for r in results if r["rule"] in rules.RULES})
    driver_rules = [{"id": rid, "name": rid.replace("-", ""), "shortDescription": {"text": rules.title(rid)},
                     "help": {"text": rules.advice(rid)}, "defaultConfiguration": {"level": LEVELS[rules.level(rid)]}} for rid in used]
    out = []
    for r in results:
        if r["rule"] not in rules.RULES:
            continue
        for uri in (r.get("paths") or [fallback_uri])[:50]:
            out.append({"ruleId": r["rule"], "ruleIndex": used.index(r["rule"]), "level": LEVELS.get(r.get("level", "warning"), "warning"),
                        "message": {"text": redact(r["message"], patterns)},
                        "locations": [{"physicalLocation": {"artifactLocation": {"uri": quote(redact(uri, patterns), safe="/")},
                                                            "region": {"startLine": 1}}}]})
    return {"$schema": SCHEMA, "version": "2.1.0",
            "runs": [{"tool": {"driver": {"name": "IWOS Guard", "version": __version__,
                                          "informationUri": "https://github.com/Gsley-IWOS/iwos-spec", "rules": driver_rules}},
                      "results": out}]}


def from_gate(result, secret_patterns: list[str] | None = None) -> dict:
    return build([f.to_json() for f in result.findings], secret_patterns=secret_patterns)


def from_validation(findings, lock_file: str, secret_patterns: list[str] | None = None) -> dict:
    """Validation findings. Messages are the tool's own; a matched credential is never included."""
    mapped = []
    for f in findings:
        rule = {"integrity": "IWOS-V001"}.get(f.category, "IWOS-V002" if "credential pattern" in f.message else "IWOS-V003")
        path = lock_file if f.category == "integrity" else f.path
        mapped.append({"rule": rule, "level": rules.level(rule), "message": f"[{f.category}] {f.message}", "paths": [path]})
    return build(mapped, secret_patterns=secret_patterns)
