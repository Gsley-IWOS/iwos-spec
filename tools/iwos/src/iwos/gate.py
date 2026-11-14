"""The gate: evaluate a proposed change (a revision range) against the constitution."""
from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
from dataclasses import dataclass, field

import yaml

from . import rules
from .config import Config, read_at
from .lock import glob_to_regex, matches_architecture, matches_protected

REPORT_VERSION = "1.2.0"

# Disclosure signatures agents leave in a pull request description. Heuristics, not proof: an agent that
# commits under a human identity and discloses nothing cannot be detected from repository data.
BODY_SIGNATURES = [
    (r"chatgpt\.com/codex", "OpenAI Codex"),
    (r"Generated with \[Claude Code\]|claude\.ai/code/session", "Claude Code"),
    (r"copilot-swe-agent", "GitHub Copilot coding agent"),
    (r"app\.devin\.ai", "Devin"),
]
EMAIL_RE = re.compile(r"\s*<[^>]*>")
CONSTITUTION_FILE = "iwos.yaml"
TRAILER_RE = re.compile(r"^([A-Z][A-Za-z-]{1,40}):\s+(.+?)\s*$", re.MULTILINE)


class GateError(Exception):
    """The revision range could not be evaluated (not a git repository, unknown ref)."""


@dataclass
class Commit:
    sha: str
    author: str
    email: str
    subject: str
    body: str
    trailers: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class GateFinding:
    rule: str
    message: str
    paths: list[str] = field(default_factory=list)
    waived_by: str = ""

    @property
    def level(self) -> str:
        return "note" if self.waived_by else rules.level(self.rule)

    def to_json(self) -> dict:
        return {"rule": self.rule, "level": self.level, "message": self.message, "paths": self.paths, "waived_by": self.waived_by}


@dataclass
class Waiver:
    id: str
    rule: str
    paths: list[str]
    owner: str
    reason: str
    expires: _dt.date

    def covers(self, rule: str, paths: list[str]) -> bool:
        if rule != self.rule or not paths:
            return False
        regexes = [glob_to_regex(p) for p in self.paths]
        return all(any(rx.match(path) for rx in regexes) for path in paths)


def parse_waivers(text: str | None, today: _dt.date) -> tuple[list[Waiver], list[str]]:
    """Read a waiver register. Returns the waivers in force and the reasons others were ignored."""
    if not text:
        return [], []
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return [], ["the waiver register is not valid YAML; every waiver ignored"]
    entries = data.get("waivers") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return [], ["the waiver register has no waivers list; every waiver ignored"]
    active, ignored = [], []
    for i, e in enumerate(entries):
        ident = str(e.get("id", f"waivers[{i}]")) if isinstance(e, dict) else f"waivers[{i}]"
        if not isinstance(e, dict) or not re.fullmatch(r"WVR-\d{4}", str(e.get("id", ""))):
            ignored.append(f"{ident}: identifier must match WVR-####"); continue
        if not rules.waivable(str(e.get("rule", ""))):
            ignored.append(f"{ident}: rule {e.get('rule')} cannot be waived"); continue
        paths = e.get("paths")
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) and p for p in paths):
            ignored.append(f"{ident}: paths must be a non-empty list"); continue
        if not str(e.get("owner", "")).strip() or not str(e.get("reason", "")).strip():
            ignored.append(f"{ident}: owner and reason are required"); continue
        expires = e.get("expires")
        if isinstance(expires, str):
            try:
                expires = _dt.date.fromisoformat(expires)
            except ValueError:
                expires = None
        if isinstance(expires, _dt.datetime):
            expires = expires.date()
        if not isinstance(expires, _dt.date):
            ignored.append(f"{ident}: expires must be a date"); continue
        if expires < today:
            ignored.append(f"{ident}: expired on {expires.isoformat()}"); continue
        active.append(Waiver(ident, str(e["rule"]), list(paths), str(e["owner"]).strip(), str(e["reason"]).strip(), expires))
    return active, ignored


@dataclass
class GateResult:
    base: str
    head: str
    changed: list[str]
    protected_changed: list[str]
    architecture_changed: list[str]
    lock_changed: bool
    proposal_citations: list[str]
    decision_citations: list[str]
    traceability_citations: list[str]
    commits: list[Commit]
    agents: list[str]
    humans: list[str]
    blocking: list[str]
    warnings: list[str]
    base_sha: str = ""
    head_sha: str = ""
    control_changed: list[str] = field(default_factory=list)
    automation_changed: list[str] = field(default_factory=list)
    constitution_source: str = "base"
    findings: list[GateFinding] = field(default_factory=list)
    waivers_applied: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.blocking

    def to_json(self) -> dict:
        return {
            "report_version": REPORT_VERSION,
            "result": "pass" if self.passed else "fail",
            "base": self.base, "head": self.head, "base_sha": self.base_sha, "head_sha": self.head_sha,
            "changed": self.changed,
            "protected_changed": self.protected_changed,
            "architecture_changed": self.architecture_changed,
            "lock_changed": self.lock_changed,
            "control_changed": self.control_changed,
            "automation_changed": self.automation_changed,
            "constitution_source": self.constitution_source,
            "findings": [f.to_json() for f in self.findings],
            "waivers_applied": self.waivers_applied,
            "citations": {"proposals": self.proposal_citations, "decisions": self.decision_citations, "traceability": self.traceability_citations},
            "commits": [{"sha": c.sha, "author": c.author, "subject": c.subject,
                         "trailers": {k: [EMAIL_RE.sub("", v).strip() for v in vs] for k, vs in c.trailers.items()}} for c in self.commits],
            "agents": self.agents, "humans": self.humans,
            "blocking": self.blocking, "warnings": self.warnings,
        }

    def to_markdown(self) -> str:
        tick = lambda ok: "pass" if ok else "FAIL"  # noqa: E731
        lines = [f"## IWOS gate report: {'PASS' if self.passed else 'FAIL'}", "",
                 f"Range `{(self.base_sha or self.base)[:12]}..{(self.head_sha or self.head)[:12]}` · {len(self.changed)} file(s) changed · {len(self.commits)} commit(s) · report v{REPORT_VERSION}", "",
                 ("Judged against the constitution of the base revision." if self.constitution_source == "base" else
                  "The base revision holds no valid constitution: judged against the constitution in the working tree (on a pull request, the one the change proposes)."), "",
                 "### Protected artefacts", ""]
        if self.protected_changed:
            lines += [f"- `{p}`" for p in self.protected_changed]
            lines += ["", f"Proposal citation: {', '.join(self.proposal_citations) or 'none'} · lock regenerated: {'yes' if self.lock_changed else 'no'}"]
        else:
            lines.append("None changed.")
        lines += ["", "### Control files", ""]
        if self.control_changed:
            lines += [f"- `{p}`" for p in self.control_changed]
            lines += ["", f"Proposal citation: {', '.join(self.proposal_citations) or 'none'}"]
        else:
            lines.append("None changed.")
        lines += ["", "### Architecture", ""]
        if self.architecture_changed:
            lines += [f"- `{p}`" for p in self.architecture_changed]
            lines += ["", f"Decision citation: {', '.join(self.decision_citations) or 'none'}"]
        else:
            lines.append("None changed.")
        lines += ["", "### Authority citations", "", f"Traceability: {', '.join(self.traceability_citations) or 'none found'}", "",
                  "### Agents", "",
                  f"Agents disclosed: {', '.join(self.agents) or 'none'}", f"Human commit authors: {', '.join(self.humans) or 'none'}", ""]
        if self.commits:
            lines.append("| Commit | Author | Subject | Trailers |")
            lines.append("| --- | --- | --- | --- |")
            for c in self.commits:
                trailers = "; ".join(f"{k}: {', '.join(EMAIL_RE.sub('', x).strip() for x in v)}" for k, v in c.trailers.items()) or ""
                lines.append(f"| `{c.sha[:8]}` | {c.author} | {c.subject.replace('|', '/')} | {trailers.replace('|', '/')} |")
        lines += ["", "### Result", ""]
        failing = [f for f in self.findings if f.level == "error"]
        lines += [f"- {tick(False)} `{f.rule}`: {f.message}" for f in failing] or ["- pass: every constitutional rule upheld"]
        lines += [f"- waived `{f.rule}` by {f.waived_by}: {f.message}" for f in self.findings if f.waived_by]
        lines += [f"- warning `{f.rule}`: {f.message}" for f in self.findings if f.level in ("warning", "note") and not f.waived_by]
        return "\n".join(lines) + "\n"

    def to_event(self, tool_version: str, now: _dt.datetime | None = None) -> dict:
        """A structured record of this run for the learning loop: identifiers, counts and paths only.

        No commit subject, no description text, no author name and no e-mail address is included.
        """
        now = now or _dt.datetime.now(_dt.timezone.utc)
        return {
            "schema_version": "1.0.0", "kind": "gate", "at": now.replace(microsecond=0).isoformat(),
            "tool_version": tool_version, "result": "pass" if self.passed else "fail",
            "base_sha": self.base_sha, "head_sha": self.head_sha, "constitution_source": self.constitution_source,
            "changed": len(self.changed), "protected_changed": len(self.protected_changed),
            "architecture_changed": len(self.architecture_changed), "control_changed": len(self.control_changed),
            "agent_disclosed": bool(self.agents), "human_authors": len(self.humans),
            "findings": [{"rule": f.rule, "level": f.level, "paths": f.paths[:20], "waived_by": f.waived_by} for f in self.findings],
        }


def require_top_level(root) -> None:
    """Paths in a range are relative to the top of the work tree, so the gate must run from there."""
    import os
    proc = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise GateError(f"{root} is not a git work tree")
    if os.path.realpath(proc.stdout.strip()) != os.path.realpath(str(root)):
        raise GateError(f"the gate must run at the top of the work tree ({proc.stdout.strip()}), not in {root}")


def _git(cfg: Config, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(cfg.root), *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise GateError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def changed_files(cfg: Config, base: str, head: str) -> list[str]:
    merge_base = _git(cfg, "merge-base", base, head).strip() or base
    # --no-renames: a moved file is reported at its old path and its new one, so moving a protected
    # artefact or a control file away is seen as a change to it. -z: paths arrive unquoted.
    out = _git(cfg, "diff", "--name-only", "--no-renames", "-z", merge_base, head)
    return sorted(p for p in out.split("\x00") if p)


def commits_in_range(cfg: Config, base: str, head: str) -> list[Commit]:
    merge_base = _git(cfg, "merge-base", base, head).strip() or base
    sep = "\x1e"
    out = _git(cfg, "log", f"--format=%H%x1f%an%x1f%ae%x1f%s%x1f%b{sep}", f"{merge_base}..{head}")
    commits = []
    for chunk in out.split(sep):
        if not chunk.strip():
            continue
        sha, author, email, subject, body = (chunk.strip("\n").split("\x1f") + ["", "", "", "", ""])[:5]
        trailers: dict[str, list[str]] = {}
        for key, value in TRAILER_RE.findall(body):
            trailers.setdefault(key, []).append(value)
        commits.append(Commit(sha, author, email, subject, body, trailers))
    return commits


def find_citations(pattern: str, *texts: str) -> list[str]:
    found: list[str] = []
    rx = re.compile(pattern)
    for text in texts:
        for m in rx.findall(text or ""):
            value = m if isinstance(m, str) else m[0]
            if value not in found:
                found.append(value)
    return found


def _display(value: str) -> str:
    """A name without its e-mail address: reports never print addresses."""
    return EMAIL_RE.sub("", value).strip()


def run_gate(cfg: Config, base: str, head: str, body: str = "", labels: list[str] | None = None,
             adoption: bool = False, today: _dt.date | None = None) -> GateResult:
    """Evaluate the range against `cfg`, which the caller loads from the base revision (see `constitution_for`).

    `adoption` is true when the base revision holds no valid constitution and `cfg` is the proposed one.
    """
    changed = changed_files(cfg, base, head)
    commits = commits_in_range(cfg, base, head)
    messages = [c.subject + "\n" + c.body for c in commits]
    corpus = [body, *messages]

    protected_changed = [p for p in changed if matches_protected(cfg, p)]
    architecture_changed = [p for p in changed if matches_architecture(cfg, p)]
    lock_changed = cfg.lock_file in changed
    proposal_citations = find_citations(cfg.proposal_pattern, *corpus)
    decision_citations = find_citations(cfg.decision_pattern, *corpus)
    traceability_citations: list[str] = []
    for pat in cfg.traceability_patterns:
        for c in find_citations(pat, *corpus):
            if c not in traceability_citations:
                traceability_citations.append(c)

    markers = [m.lower() for m in cfg.agent_markers]
    agents: list[str] = []
    humans: list[str] = []

    def note(target: list[str], entry: str) -> None:
        if entry and entry not in target:
            target.append(entry)

    for c in commits:
        identity = f"{c.author} <{c.email}>".lower()
        if any(m in identity for m in markers):
            note(agents, f"{c.author} (commit author)")
        else:
            note(humans, c.author)
        for key, values in c.trailers.items():
            for v in values:
                if any(m in v.lower() for m in markers):
                    note(agents, f"{_display(v)} ({key} trailer)")
    disclosed_in_description = False
    for pattern, name in BODY_SIGNATURES:
        if re.search(pattern, body or ""):
            note(agents, f"{name} (pull request description)")
            disclosed_in_description = True
    for label in labels or []:
        if any(m in label.lower() for m in markers):
            note(agents, f"{label} (pull request label)")
            disclosed_in_description = True
    agent_commits = any(a.endswith("(commit author)") or a.endswith("trailer)") for a in agents)

    control_changed = [] if adoption else [p for p in changed if p in cfg.control_files]
    automation_res = [glob_to_regex(p) for p in cfg.automation_paths]
    automation_changed = [p for p in changed if any(rx.match(p) for rx in automation_res)]
    today = today or _dt.date.today()
    waivers, ignored = parse_waivers(None if adoption else read_at(cfg.root, base, cfg.waivers_file), today)

    findings: list[GateFinding] = []
    if protected_changed:
        if not proposal_citations:
            findings.append(GateFinding("IWOS-G001", f"{len(protected_changed)} protected artefact(s) changed without an accepted-proposal citation matching {cfg.proposal_pattern}", protected_changed))
        if cfg.lock_must_change_with_protected and not lock_changed:
            findings.append(GateFinding("IWOS-G002", f"protected artefact(s) changed but the lock {cfg.lock_file} was not regenerated in the same change", protected_changed))
    if control_changed and not proposal_citations:
        findings.append(GateFinding("IWOS-G005", f"{len(control_changed)} control file(s) changed without an accepted-proposal citation matching {cfg.proposal_pattern}: "
                                                 "the files that define the rules are protected whatever the constitution file says", control_changed))
    if architecture_changed and not decision_citations:
        findings.append(GateFinding("IWOS-G003", f"{len(architecture_changed)} architecture file(s) changed without a decision-record citation matching {cfg.decision_pattern}", architecture_changed))
    if cfg.traceability_required and changed and not traceability_citations:
        findings.append(GateFinding("IWOS-G004", "no authority citation found in the pull request body or commit messages (traceability required)", changed))
    waivers_applied: list[str] = []
    for f in findings:
        for w in waivers:
            if w.covers(f.rule, f.paths):
                f.waived_by = w.id
                waivers_applied.append(f"{w.id} ({f.rule}, owner {w.owner}, expires {w.expires.isoformat()})")
                break

    if adoption:
        findings.append(GateFinding("IWOS-W005", "the base revision holds no valid constitution, so this change was judged against the constitution in the working tree, "
                                                 "which on a pull request is the one the change proposes; review the constitution file by hand", [CONSTITUTION_FILE]))
    if lock_changed and not protected_changed:
        findings.append(GateFinding("IWOS-W001", "the lock changed although no protected artefact did; confirm the regeneration was intended", [cfg.lock_file]))
    if automation_changed:
        findings.append(GateFinding("IWOS-W007", "the automation that runs this gate changed in this range; a result produced by a changed gate is not independent, "
                                                 "so review that change by hand", automation_changed))
    for reason in ignored:
        findings.append(GateFinding("IWOS-W006", f"waiver ignored: {reason}", [cfg.waivers_file]))
    if agents and not humans:
        findings.append(GateFinding("IWOS-W002", "every commit in this range is attributed to an agent; a human must review and merge"))
    if disclosed_in_description and not agent_commits:
        findings.append(GateFinding("IWOS-W003", "an agent is disclosed in the pull request description or labels, but every commit carries a human identity; "
                                                 "attribution here rests on disclosure alone"))
    if not agents:
        findings.append(GateFinding("IWOS-W004", "no agent disclosed; this does not show that no agent was involved, only that none identified itself"))
    blocking = [f.message for f in findings if f.level == "error"]
    warnings = [f.message for f in findings if f.level != "error"]

    def short(ref: str) -> str:
        try:
            return _git(cfg, "rev-parse", "--short=12", ref).strip()
        except GateError:
            return ""

    return GateResult(base, head, changed, protected_changed, architecture_changed, lock_changed, proposal_citations,
                      decision_citations, traceability_citations, commits, agents, humans, blocking, warnings,
                      base_sha=short(base), head_sha=short(head), control_changed=control_changed,
                      automation_changed=automation_changed, constitution_source="working-tree" if adoption else "base",
                      findings=findings, waivers_applied=waivers_applied)


def constitution_for(root, base: str) -> tuple[Config, bool]:
    """The constitution a change is judged against: the one on the base revision.

    Falls back to the working tree, flagged as an adoption, only when the base revision holds no
    constitution or an invalid one. Returns (config, adoption).
    """
    from .config import ConfigError, load_config, load_config_at
    require_top_level(root)
    if subprocess.run(["git", "-C", str(root), "rev-parse", "-q", "--verify", f"{base}^{{commit}}"], capture_output=True, check=False).returncode != 0:
        raise GateError(f"base revision {base} is not a commit in this repository")
    try:
        cfg = load_config_at(root, base)
    except ConfigError:
        cfg = None
    if cfg is not None:
        return cfg, False
    return load_config(root), True


def dumps(result: GateResult) -> str:
    return json.dumps(result.to_json(), indent=2)
