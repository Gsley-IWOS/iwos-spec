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
from .lock import matches_architecture, matches_protected

SAFE_PATH = re.compile(r"^[A-Za-z0-9_./-]{1,120}$")
MAX_EVENT_BYTES = 64_000


def log_path(cfg: Config) -> Path:
    return cfg.root / cfg.events_file


def append_event(cfg: Config, event: dict) -> Path:
    """Append one event as a JSON line. Existing lines are never rewritten."""
    if not isinstance(event, dict) or event.get("kind") not in ("gate", "validate") or not isinstance(event.get("findings", []), list):
        raise ValueError("not an IWOS event record")
    line = json.dumps(event, sort_keys=True, separators=(",", ":"))
    if len(line) > MAX_EVENT_BYTES or _normalise(event) is None:
        raise ValueError("not an IWOS event record")
    path = log_path(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return path


def _normalise(event) -> dict | None:
    """Reduce a parsed log line to the fields the summaries use, or None when it is not an event."""
    if not isinstance(event, dict) or not isinstance(event.get("findings", []), list):
        return None
    if not isinstance(event.get("kind"), str) or not isinstance(event.get("result", ""), str):
        return None
    findings = []
    for f in event.get("findings", []):
        if not isinstance(f, dict) or not isinstance(f.get("rule"), str):
            continue
        paths = f.get("paths") if isinstance(f.get("paths"), list) else []
        findings.append({"rule": f["rule"], "paths": [p for p in paths if isinstance(p, str)], "waived": bool(f.get("waived_by"))})
    return {"kind": event["kind"], "result": event.get("result", ""), "findings": findings}


def read_events(cfg: Config) -> tuple[list[dict], int]:
    """Return the readable events, normalised, and the number of lines skipped as malformed."""
    path = log_path(cfg)
    if not path.exists():
        return [], 0
    events, skipped = [], 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = _normalise(json.loads(line))
        except (ValueError, RecursionError):  # JSONDecodeError is a ValueError; so is an over-long integer
            event = None
        if event is None:
            skipped += 1
        else:
            events.append(event)
    return events, skipped


def _governed_path(cfg: Config, value: str) -> str | None:
    """A path is repeated to an agent only when the constitution already names it.

    It must be made of plain path characters, exist in the working tree, and be a control file or match
    a protected or architecture pattern. A path that a rejected change merely proposed never qualifies,
    so a change cannot use its own file names to speak to the next agent.
    """
    if not SAFE_PATH.match(value) or ".." in value or not (cfg.root / value).exists():
        return None
    if value in cfg.control_files or matches_protected(cfg, value) or matches_architecture(cfg, value):
        return value
    return None


def lessons(cfg: Config, limit: int = 5) -> dict:
    """What this repository's own history says agents get wrong, as structured fields only.

    Every string in the output is a rule identifier, advice from the tool's own rule catalogue or a
    path that passed `_governed_path`. No free text from the repository is repeated.
    """
    events, skipped = read_events(cfg)
    counts: Counter[str] = Counter()
    paths: dict[str, Counter[str]] = {}
    runs = failed = 0
    for event in events:
        if event["kind"] != "gate":
            continue
        runs += 1
        failed += event["result"] == "fail"
        for f in event["findings"]:
            rule = f["rule"]
            if rule not in rules.RULES or rules.level(rule) != "error" or f["waived"]:
                continue
            counts[rule] += 1
            for p in f["paths"]:
                safe = _governed_path(cfg, p)
                if safe:
                    paths.setdefault(rule, Counter())[safe] += 1
    limit = max(1, min(int(limit), 20))
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
        if event["kind"] != "gate":
            continue
        results[event["result"]] += 1
        for f in event["findings"]:
            if f["rule"] in rules.RULES:
                by_rule[f["rule"]] += 1
                waived += f["waived"]
    return {"schema_version": "1.0.0", "gate_runs": sum(results.values()), "passed": results.get("pass", 0), "failed": results.get("fail", 0),
            "waived_findings": waived, "findings_by_rule": dict(sorted(by_rule.items()))}
