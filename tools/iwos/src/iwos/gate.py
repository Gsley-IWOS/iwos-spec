"""The gate: evaluate a proposed change (a revision range) against the constitution."""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field

from .config import Config
from .lock import matches_architecture, matches_protected

REPORT_VERSION = "1.0.0"
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

    @property
    def passed(self) -> bool:
        return not self.blocking

    def to_json(self) -> dict:
        return {
            "report_version": REPORT_VERSION,
            "result": "pass" if self.passed else "fail",
            "base": self.base, "head": self.head,
            "changed": self.changed,
            "protected_changed": self.protected_changed,
            "architecture_changed": self.architecture_changed,
            "lock_changed": self.lock_changed,
            "citations": {"proposals": self.proposal_citations, "decisions": self.decision_citations, "traceability": self.traceability_citations},
            "commits": [{"sha": c.sha, "author": c.author, "subject": c.subject, "trailers": c.trailers} for c in self.commits],
            "agents": self.agents, "humans": self.humans,
            "blocking": self.blocking, "warnings": self.warnings,
        }

    def to_markdown(self) -> str:
        tick = lambda ok: "pass" if ok else "FAIL"  # noqa: E731
        lines = [f"## IWOS gate report: {'PASS' if self.passed else 'FAIL'}", "",
                 f"Range `{self.base[:12]}..{self.head[:12]}` · {len(self.changed)} file(s) changed · {len(self.commits)} commit(s) · report v{REPORT_VERSION}", "",
                 "### Protected artefacts", ""]
        if self.protected_changed:
            lines += [f"- `{p}`" for p in self.protected_changed]
            lines += ["", f"Proposal citation: {', '.join(self.proposal_citations) or 'none'} · lock regenerated: {'yes' if self.lock_changed else 'no'}"]
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
                  f"Agents detected: {', '.join(self.agents) or 'none'}", f"Human authors: {', '.join(self.humans) or 'none'}", ""]
        if self.commits:
            lines.append("| Commit | Author | Subject | Trailers |")
            lines.append("| --- | --- | --- | --- |")
            for c in self.commits:
                trailers = "; ".join(f"{k}: {', '.join(v)}" for k, v in c.trailers.items()) or ""
                lines.append(f"| `{c.sha[:8]}` | {c.author} | {c.subject.replace('|', '/')} | {trailers.replace('|', '/')} |")
        lines += ["", "### Result", ""]
        lines += [f"- {tick(False)}: {b}" for b in self.blocking] or ["- pass: every constitutional rule upheld"]
        lines += [f"- warning: {w}" for w in self.warnings]
        return "\n".join(lines) + "\n"


def _git(cfg: Config, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(cfg.root), *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise GateError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def changed_files(cfg: Config, base: str, head: str) -> list[str]:
    merge_base = _git(cfg, "merge-base", base, head).strip() or base
    out = _git(cfg, "diff", "--name-only", merge_base, head)
    return sorted(p for p in out.splitlines() if p.strip())


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


def run_gate(cfg: Config, base: str, head: str, body: str = "") -> GateResult:
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
    for c in commits:
        who = f"{c.author} <{c.email}>"
        is_agent = any(m in who.lower() for m in markers)
        (agents if is_agent else humans).append(who) if who not in agents + humans else None
        for key in ("Co-Authored-By", "Co-authored-by", "Generated-By", "Claude-Session", "Codex-Task"):
            for v in c.trailers.get(key, []):
                if any(m in v.lower() for m in markers) and v not in agents:
                    agents.append(v)

    blocking: list[str] = []
    warnings: list[str] = []
    if protected_changed:
        if not proposal_citations:
            blocking.append(f"{len(protected_changed)} protected artefact(s) changed without an accepted-proposal citation matching {cfg.proposal_pattern}")
        if cfg.lock_must_change_with_protected and not lock_changed:
            blocking.append(f"protected artefact(s) changed but the lock {cfg.lock_file} was not regenerated in the same change")
    if lock_changed and not protected_changed:
        warnings.append("the lock changed although no protected artefact did; confirm the regeneration was intended")
    if architecture_changed and not decision_citations:
        blocking.append(f"{len(architecture_changed)} architecture file(s) changed without a decision-record citation matching {cfg.decision_pattern}")
    if cfg.traceability_required and changed and not traceability_citations:
        blocking.append("no authority citation found in the pull request body or commit messages (traceability required)")
    if agents and not humans:
        warnings.append("every commit in this range is attributed to an agent; a human must review and merge")

    return GateResult(base, head, changed, protected_changed, architecture_changed, lock_changed, proposal_citations,
                      decision_citations, traceability_citations, commits, agents, humans, blocking, warnings)


def dumps(result: GateResult) -> str:
    return json.dumps(result.to_json(), indent=2)
