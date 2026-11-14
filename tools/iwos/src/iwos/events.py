"""The learning loop: a local, append-only event log and the lessons and statistics derived from it.

Nothing here leaves the repository. `stats` produces an anonymous summary a maintainer may choose to
share; the tool never sends it anywhere.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from . import rules
from .config import Config

SAFE_PATH = re.compile(r"^[A-Za-z0-9_./-]{1,120}$")


def log_path(cfg: Config) -> Path:
    return cfg.root / cfg.events_file


def append_event(cfg: Config, event: dict) -> Path:
    """Append one event as a JSON line. Existing lines are never rewritten."""
    if not isinstance(event, dict) or event.get("kind") not in ("gate", "validate") or not isinstance(event.get("findings", []), list):
        raise ValueError("not an IWOS event record")
    path = log_path(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
    return path


def read_events(cfg: Config) -> tuple[list[dict], int]:
    """Return the readable events and the number of lines skipped as malformed."""
    path = log_path(cfg)
    if not path.exists():
        return [], 0
    events, skipped = [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            skipped += 1
            continue
        if isinstance(event, dict) and isinstance(event.get("findings", []), list):
            events.append(event)
        else:
            skipped += 1
    return events, skipped


def _safe_path(value) -> str | None:
    """A path is repeated to an agent only when it is short and made of plain path characters."""
    return value if isinstance(value, str) and SAFE_PATH.match(value) and ".." not in value else None


def lessons(cfg: Config, limit: int = 5) -> dict:
    """What this repository's own history says agents get wrong, as structured fields only.

    Every string in the output is either a rule identifier, advice from the tool's own rule catalogue
    or a path that passed `_safe_path`. No free text from the repository is repeated.
    """
    events, skipped = read_events(cfg)
    counts: Counter[str] = Counter()
    paths: dict[str, Counter[str]] = {}
    runs = failed = 0
    for event in events:
        if event.get("kind") != "gate":
            continue
        runs += 1
        failed += event.get("result") == "fail"
        for f in event.get("findings", []):
            rule = f.get("rule") if isinstance(f, dict) else None
            if rule not in rules.RULES or rules.level(rule) != "error" or f.get("waived_by"):
                continue
            counts[rule] += 1
            for p in f.get("paths", []) or []:
                safe = _safe_path(p)
                if safe:
                    paths.setdefault(rule, Counter())[safe] += 1
    items = [{"rule": rule, "title": rules.title(rule), "occurrences": n, "advice": rules.advice(rule),
              "most_affected_paths": [p for p, _ in paths.get(rule, Counter()).most_common(3)]}
             for rule, n in counts.most_common(limit)]
    return {"gate_runs": runs, "failed_runs": failed, "malformed_lines_skipped": skipped, "lessons": items}


def stats(cfg: Config) -> dict:
    """An anonymous summary: rule identifiers and counts. No path, name, revision or repository name."""
    events, _ = read_events(cfg)
    by_rule: Counter[str] = Counter()
    results: Counter[str] = Counter()
    waived = 0
    for event in events:
        if event.get("kind") != "gate":
            continue
        results[str(event.get("result"))] += 1
        for f in event.get("findings", []):
            if isinstance(f, dict) and f.get("rule") in rules.RULES:
                by_rule[f["rule"]] += 1
                waived += bool(f.get("waived_by"))
    return {"schema_version": "1.0.0", "gate_runs": sum(results.values()), "passed": results.get("pass", 0), "failed": results.get("fail", 0),
            "waived_findings": waived, "findings_by_rule": dict(sorted(by_rule.items()))}
