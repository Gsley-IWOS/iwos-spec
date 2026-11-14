"""The incident ledger: an append-only record of security incidents in a governed repository.

The ledger says what happened, where, and how it was mitigated. It never holds the sensitive value
itself: text that matches a credential pattern is refused.
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

import yaml

from .config import Config

CLASSES = {
    "secret-exposure": "A credential or other secret was committed or printed.",
    "integrity-violation": "A protected artefact and the integrity lock disagree.",
    "unauthorised-protected-change": "A protected artefact or control file changed without authority.",
    "gate-bypass": "A change evaded the gate or the automation that runs it.",
    "agent-misattribution": "Agent work was recorded under a human identity or not disclosed.",
    "other": "A security event that fits no other class.",
}
SEVERITIES = ("low", "medium", "high", "critical")
STATUSES = ("open", "mitigated", "closed")

PLAYBOOKS = {
    "secret-exposure": [
        "Revoke or rotate the credential at its issuer first. Removing it from the repository does not make it safe.",
        "Record the file and commit in the incident. Never copy the value into the ledger, an issue or a chat.",
        "Remove the value from the working tree; decide with a maintainer whether history must be purged.",
        "Check the issuer's access logs for use of the credential since the commit date.",
        "Close the incident with the rotation reference and add a secret pattern if the shape was not detected.",
    ],
    "integrity-violation": [
        "Stop. Do not regenerate the lock: the lock is the evidence.",
        "Identify the commit that changed the protected artefact (`git log -- <path>`).",
        "If no accepted proposal authorised it, revert the artefact to the locked content.",
        "If a proposal authorised it, regenerate the lock in a change that cites the proposal.",
        "Close the incident with the commit and the proposal or the revert.",
    ],
    "unauthorised-protected-change": [
        "Revert the change or convert it into a proposal for review; do not leave it merged and unexplained.",
        "Establish how it merged: missing required check, administrator override or an edited workflow.",
        "Restore the missing control (branch protection, required status check, code-owner review).",
        "Close the incident with a decision record that states what now prevents a repeat.",
    ],
    "gate-bypass": [
        "Reproduce the bypass in a throwaway repository and keep the steps as a regression test.",
        "Audit merged history for changes that used the same path (changes to control files and workflows).",
        "Fix or upgrade the gate, pin the fixed version, and re-run the gate on the suspect changes.",
        "Report a defect in the tool privately to its maintainers; see the tool's security policy.",
        "Close the incident with the fix reference and a decision record.",
    ],
    "agent-misattribution": [
        "Record which change was attributed incorrectly and under which identity.",
        "Configure the agent to commit under its own identity or to add a co-author trailer.",
        "Add the disclosure to the pull request description so that the record is complete from now on.",
        "Close the incident when the next change from that agent is attributed correctly.",
    ],
    "other": [
        "Contain: stop the activity and preserve the evidence.",
        "Record what is known without sensitive values.",
        "Mitigate, then write a retrospective and a decision record for any rule that changes.",
    ],
}


class IncidentError(ValueError):
    """The incident could not be recorded as given."""


def ledger_path(cfg: Config) -> Path:
    return cfg.root / cfg.incident_ledger


def load(cfg: Config) -> dict:
    path = ledger_path(cfg)
    if not path.exists():
        return {"schema_version": "1.0.0", "incidents": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or not isinstance(data.get("incidents", []), list):
        raise IncidentError(f"{cfg.incident_ledger} is not an incident ledger")
    data.setdefault("incidents", [])
    return data


def _save(cfg: Config, data: dict) -> None:
    path = ledger_path(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    head = "# Incident ledger maintained by IWOS Guard. Append-only: entries are never edited or deleted, only extended.\n"
    path.write_text(head + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")


def _refuse_secrets(cfg: Config, *texts: str) -> None:
    for text in texts:
        for pattern in cfg.secret_patterns:
            if re.search(pattern, text or ""):
                raise IncidentError("the text matches a credential pattern; describe the incident without the sensitive value")


def _clean(text: str, limit: int = 500) -> str:
    return " ".join(str(text).split())[:limit]


def open_incident(cfg: Config, incident_class: str, severity: str, summary: str, paths: list[str] | None = None,
                  detected_by: str = "maintainer", today: _dt.date | None = None) -> dict:
    if incident_class not in CLASSES:
        raise IncidentError(f"unknown class '{incident_class}'; one of {', '.join(CLASSES)}")
    if severity not in SEVERITIES:
        raise IncidentError(f"unknown severity '{severity}'; one of {', '.join(SEVERITIES)}")
    summary = _clean(summary)
    if len(summary) < 10:
        raise IncidentError("the summary must say what happened in at least ten characters")
    paths = [_clean(p, 200) for p in (paths or [])]
    _refuse_secrets(cfg, summary, detected_by, *paths)
    data = load(cfg)
    numbers = [int(m.group(1)) for i in data["incidents"] if isinstance(i, dict) for m in [re.fullmatch(r"INC-(\d{4})", str(i.get("id", "")))] if m]
    date = (today or _dt.date.today()).isoformat()
    entry = {"id": f"INC-{(max(numbers) + 1) if numbers else 1:04d}", "opened": date, "class": incident_class, "severity": severity,
             "status": "open", "summary": summary, "paths": paths, "detected_by": _clean(detected_by, 80),
             "history": [{"date": date, "status": "open", "note": "Incident opened."}]}
    data["incidents"].append(entry)
    _save(cfg, data)
    return entry


def update_incident(cfg: Config, incident_id: str, status: str, note: str, decision: str = "", today: _dt.date | None = None) -> dict:
    if status not in STATUSES:
        raise IncidentError(f"unknown status '{status}'; one of {', '.join(STATUSES)}")
    note = _clean(note)
    if len(note) < 10:
        raise IncidentError("the note must say what was done in at least ten characters")
    _refuse_secrets(cfg, note, decision)
    data = load(cfg)
    for entry in data["incidents"]:
        if isinstance(entry, dict) and entry.get("id") == incident_id:
            if STATUSES.index(status) < STATUSES.index(entry.get("status", "open")):
                raise IncidentError(f"{incident_id} is {entry.get('status')}; an incident does not move backwards. Open a new incident if it recurred.")
            date = (today or _dt.date.today()).isoformat()
            entry["status"] = status
            entry.setdefault("history", []).append({"date": date, "status": status, "note": note})
            if decision:
                entry["decision"] = _clean(decision, 120)
            if status == "closed":
                entry["closed"] = date
            _save(cfg, data)
            return entry
    raise IncidentError(f"no incident {incident_id}")


def check(cfg: Config) -> list[str]:
    """Problems with the ledger as a document."""
    path = ledger_path(cfg)
    if not path.exists():
        return []
    try:
        data = load(cfg)
    except (IncidentError, yaml.YAMLError) as exc:
        return [str(exc)]
    problems, seen = [], set()
    for i, entry in enumerate(data["incidents"]):
        if not isinstance(entry, dict):
            problems.append(f"incidents[{i}] is not a mapping"); continue
        ident = str(entry.get("id", f"incidents[{i}]"))
        if not re.fullmatch(r"INC-\d{4}", ident):
            problems.append(f"{ident}: identifier must match INC-####")
        if ident in seen:
            problems.append(f"duplicate incident id {ident}")
        seen.add(ident)
        if entry.get("class") not in CLASSES:
            problems.append(f"{ident}: unknown class {entry.get('class')}")
        if entry.get("severity") not in SEVERITIES:
            problems.append(f"{ident}: unknown severity {entry.get('severity')}")
        if entry.get("status") not in STATUSES:
            problems.append(f"{ident}: unknown status {entry.get('status')}")
        if not entry.get("summary") or not entry.get("opened"):
            problems.append(f"{ident}: summary and opened are required")
        if entry.get("status") == "closed" and not entry.get("closed"):
            problems.append(f"{ident}: a closed incident records its closing date")
    return problems


def open_incidents(cfg: Config) -> list[dict]:
    try:
        return [i for i in load(cfg)["incidents"] if isinstance(i, dict) and i.get("status") != "closed"]
    except (IncidentError, yaml.YAMLError):
        return []
