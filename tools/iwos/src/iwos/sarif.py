"""SARIF 2.1.0 output, so that findings can be uploaded to a code-scanning service."""
from __future__ import annotations

from . import __version__, rules

SCHEMA = "https://json.schemastore.org/sarif-2.1.0.json"
LEVELS = {"error": "error", "warning": "warning", "note": "note"}


def build(results: list[dict], fallback_uri: str = "iwos.yaml") -> dict:
    """`results` items: {"rule": id, "level": error|warning|note, "message": str, "paths": [str]}."""
    used = sorted({r["rule"] for r in results if r["rule"] in rules.RULES})
    driver_rules = [{"id": rid, "name": rid.replace("-", ""), "shortDescription": {"text": rules.title(rid)},
                     "help": {"text": rules.advice(rid)}, "defaultConfiguration": {"level": LEVELS[rules.level(rid)]}} for rid in used]
    out = []
    for r in results:
        if r["rule"] not in rules.RULES:
            continue
        for uri in (r.get("paths") or [fallback_uri])[:50]:
            out.append({"ruleId": r["rule"], "ruleIndex": used.index(r["rule"]), "level": LEVELS.get(r.get("level", "warning"), "warning"),
                        "message": {"text": r["message"]},
                        "locations": [{"physicalLocation": {"artifactLocation": {"uri": uri}, "region": {"startLine": 1}}}]})
    return {"$schema": SCHEMA, "version": "2.1.0",
            "runs": [{"tool": {"driver": {"name": "IWOS Guard", "version": __version__,
                                          "informationUri": "https://github.com/Gsley-IWOS/iwos-spec", "rules": driver_rules}},
                      "results": out}]}


def from_gate(result) -> dict:
    return build([f.to_json() for f in result.findings])


def from_validation(findings, lock_file: str) -> dict:
    """Validation findings. Messages are the tool's own; a matched credential is never included."""
    mapped = []
    for f in findings:
        rule = {"integrity": "IWOS-V001"}.get(f.category, "IWOS-V002" if "credential pattern" in f.message else "IWOS-V003")
        path = lock_file if f.category == "integrity" else f.path
        mapped.append({"rule": rule, "level": rules.level(rule), "message": f"[{f.category}] {f.message}", "paths": [path]})
    return build(mapped)
