"""Repository validation: integrity, decision ledger, drafting markers, credential shapes, agent block."""
from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import agents_block
from .config import Config
from .lock import check_lock

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".toml", ".py", ".js", ".ts", ".cfg", ".ini", ".env", ".sh"}


@dataclass
class Finding:
    category: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"[{self.category}] {self.path}: {self.message}"


def iter_text_files(cfg: Config):
    exclude_dirs = set(cfg.exclude_dirs)
    exclude_files = set(cfg.exclude_files)
    for path in sorted(cfg.root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(cfg.root)
        if any(part in exclude_dirs for part in rel.parts[:-1]):
            continue
        if str(rel).replace("\\", "/") in exclude_files or rel.name in exclude_files:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        yield path, str(rel).replace("\\", "/")


def check_ledger(cfg: Config) -> list[Finding]:
    path = cfg.root / cfg.decision_ledger
    if not path.exists():
        return []  # a repository may have no decisions yet; the ledger is created on first record
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [Finding("ledger", cfg.decision_ledger, f"invalid YAML: {exc}")]
    findings = []
    decisions = (data or {}).get("decisions")
    if not isinstance(decisions, list):
        return [Finding("ledger", cfg.decision_ledger, "expected a mapping with a decisions list")]
    seen = set()
    for i, d in enumerate(decisions):
        if not isinstance(d, dict):
            findings.append(Finding("ledger", cfg.decision_ledger, f"decisions[{i}] is not a mapping"))
            continue
        for key in ("id", "date", "status", "title", "decision"):
            if not d.get(key):
                findings.append(Finding("ledger", cfg.decision_ledger, f"{d.get('id', f'decisions[{i}]')} lacks '{key}'"))
        if d.get("id") in seen:
            findings.append(Finding("ledger", cfg.decision_ledger, f"duplicate decision id {d.get('id')}"))
        seen.add(d.get("id"))
        for ref in list(d.get("related_files", []) or []):
            if not (cfg.root / ref).exists():
                findings.append(Finding("ledger", cfg.decision_ledger, f"{d.get('id')} references '{ref}' which does not exist"))
    return findings


def check_content(cfg: Config) -> list[Finding]:
    findings = []
    marker_res = [(m, re.compile(r"(?<![A-Za-z0-9_])" + re.escape(m) + r"(?![A-Za-z0-9_])")) for m in cfg.drafting_markers]
    secret_res = [re.compile(p) for p in cfg.secret_patterns]
    for path, rel in iter_text_files(cfg):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix.lower() in {".md", ".yaml", ".yml"} and rel != cfg.lock_file:
            for marker, marker_re in marker_res:
                if marker_re.search(text):
                    findings.append(Finding("content", rel, f"drafting marker '{marker}' present"))
        for secret_re in secret_res:
            if secret_re.search(text):
                findings.append(Finding("content", rel, "content matches a credential pattern"))
                break
    return findings


def run_spec_validator(cfg: Config) -> tuple[int, str]:
    """iwos-spec profile: the repository's own validator is the engine; run it and relay its output."""
    proc = subprocess.run([sys.executable, str(cfg.root / "tools" / "validate" / "validate.py"), "--root", str(cfg.root)],
                          capture_output=True, text=True, check=False)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def validate(cfg: Config) -> tuple[list[Finding], str]:
    """Run every check. Returns findings and a human summary line."""
    findings: list[Finding] = []
    if not cfg.protected:
        findings.append(Finding("constitution", "iwos.yaml", "no protected patterns declared; a constitution that protects nothing verifies nothing"))
    findings += [Finding("integrity", cfg.lock_file, m) for m in check_lock(cfg)]
    findings += check_ledger(cfg)
    stale = agents_block.stale_files(cfg)
    findings += [Finding("agents", f, "generated block is missing or stale; run `iwos agents`") for f in stale]
    extra = ""
    if cfg.spec_validator_config is not None:
        code, out = run_spec_validator(cfg)
        extra = out
        if code != 0:
            findings.append(Finding("spec-validator", "tools/validate/validate.py", "repository validator reported failures (see output)"))
    else:
        findings += check_content(cfg)
    summary = "PASS: constitution upheld" if not findings else f"FAIL: {len(findings)} finding(s)"
    if extra:
        summary += "\n" + extra
    return findings, summary
