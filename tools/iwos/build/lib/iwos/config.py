"""Load and validate the constitution file (iwos.yaml) of a governed repository."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

CONFIG_NAME = "iwos.yaml"
SCHEMA_PATH = Path(__file__).with_name("iwos_config.schema.json")

DEFAULT_DRAFTING_MARKERS = ["TODO", "TBD", "FIXME", "XXX", "lorem ipsum", "PLACEHOLDER"]
DEFAULT_SECRET_PATTERNS = [
    "AKIA[0-9A-Z]{16}",
    "-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "ghp_[A-Za-z0-9]{36}",
    "github_pat_[A-Za-z0-9_]{22,}",
    "xox[baprs]-[A-Za-z0-9-]{10,}",
    "sk-[A-Za-z0-9]{32,}",
    "AIza[0-9A-Za-z_-]{35}",
]
DEFAULT_AGENT_MARKERS = ["claude", "codex", "copilot", "cursor", "gemini", "devin", "aider", "openhands", "[bot]", "noreply@anthropic.com"]
DEFAULT_EXCLUDE_DIRS = [".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".pytest_cache"]


class ConfigError(Exception):
    """The constitution file is missing or invalid. Every command fails closed on it."""


@dataclass
class Config:
    root: Path
    profile: str
    name: str
    protected: list[str]
    architecture: list[str]
    lock_file: str
    decision_ledger: str
    proposal_pattern: str
    decision_pattern: str
    traceability_patterns: list[str]
    traceability_required: bool
    lock_must_change_with_protected: bool
    agent_files: list[str]
    agent_markers: list[str]
    drafting_markers: list[str]
    secret_patterns: list[str]
    exclude_dirs: list[str]
    exclude_files: list[str]
    raw: dict = field(default_factory=dict)

    @property
    def spec_validator_config(self) -> Path | None:
        path = self.root / "tools" / "validate" / "config.yaml"
        return path if self.profile == "iwos-spec" and path.exists() else None


def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_document(data) -> list[str]:
    errors = sorted(Draft202012Validator(schema()).iter_errors(data), key=lambda e: list(e.path))
    return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in errors]


def load_config(root: Path) -> Config:
    root = Path(root).resolve()
    path = root / CONFIG_NAME
    if not path.exists():
        raise ConfigError(f"{CONFIG_NAME} not found in {root}. Run `iwos init` to create a constitution.")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"{CONFIG_NAME} is not valid YAML: {exc}") from exc
    problems = validate_document(data)
    if problems:
        raise ConfigError(f"{CONFIG_NAME} does not conform to the constitution schema: " + "; ".join(problems))

    profile = data["profile"]
    constitution = data.get("constitution", {}) or {}
    authority = data.get("authority", {}) or {}
    agents = data.get("agents", {}) or {}
    checks = data.get("checks", {}) or {}

    protected = list(constitution.get("protected", []))
    lock_file = constitution.get("lock_file")
    ledger = constitution.get("decision_ledger")

    if profile == "iwos-spec":
        spec_cfg_path = root / "tools" / "validate" / "config.yaml"
        if not spec_cfg_path.exists():
            raise ConfigError("profile iwos-spec requires tools/validate/config.yaml in the repository")
        spec_cfg = yaml.safe_load(spec_cfg_path.read_text(encoding="utf-8"))
        protected = protected or list(spec_cfg["protected_documents"]["patterns"])
        lock_file = lock_file or spec_cfg["protected_documents"]["lock_file"]
        ledger = ledger or spec_cfg.get("cross_references", {}).get("decision_graph", ".ai/DECISION_GRAPH.yaml")
        markers = checks.get("drafting_markers") or spec_cfg.get("content", {}).get("drafting_markers", DEFAULT_DRAFTING_MARKERS)
        secrets = checks.get("secret_patterns") or spec_cfg.get("content", {}).get("secret_patterns", DEFAULT_SECRET_PATTERNS)
    else:
        markers = checks.get("drafting_markers", DEFAULT_DRAFTING_MARKERS)
        secrets = checks.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        lock_file = lock_file or ".iwos/lock.yaml"
        ledger = ledger or ".iwos/decisions.yaml"

    for name, pattern in (("proposal_pattern", authority.get("proposal_pattern", r"AIP-\d{4}")),
                          ("decision_pattern", authority.get("decision_pattern", r"ADR-\d{4}"))):
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ConfigError(f"authority.{name} is not a valid regular expression: {exc}") from exc

    return Config(
        root=root,
        profile=profile,
        name=data.get("name", root.name),
        protected=protected,
        architecture=list(constitution.get("architecture", [])),
        lock_file=lock_file,
        decision_ledger=ledger,
        proposal_pattern=authority.get("proposal_pattern", r"AIP-\d{4}"),
        decision_pattern=authority.get("decision_pattern", r"ADR-\d{4}"),
        traceability_patterns=list(authority.get("traceability_patterns", [r"EWP-\d{4}", r"ADR-\d{4}", r"AIP-\d{4}", r"#\d+"])),
        traceability_required=bool(authority.get("traceability_required", True)),
        lock_must_change_with_protected=bool(authority.get("lock_must_change_with_protected", True)),
        agent_files=list(agents.get("files", ["AGENTS.md"])),
        agent_markers=list(agents.get("known_agent_markers", DEFAULT_AGENT_MARKERS)),
        drafting_markers=list(markers),
        secret_patterns=list(secrets),
        exclude_dirs=list(checks.get("exclude_dirs", DEFAULT_EXCLUDE_DIRS)),
        exclude_files=list(checks.get("exclude_files", [])),
        raw=data,
    )


def default_config_text(name: str, protected: list[str], architecture: list[str]) -> str:
    """The iwos.yaml written by `iwos init` for a generic repository."""
    def yaml_list(items: list[str]) -> str:
        return "\n".join(f"    - {json.dumps(i)}" for i in items) if items else "    []"
    return f"""# IWOS constitution file. Schema: https://github.com/Gsley-IWOS/iwos-spec/blob/main/schemas/iwos-config.schema.json
# Everything matched by `protected` changes only with an authority citation and a regenerated lock.
# Everything matched by `architecture` changes only with a decision-record citation.
schema_version: "1.0.0"
profile: generic
name: {json.dumps(name)}
constitution:
  protected:
{yaml_list(protected)}
  architecture:
{yaml_list(architecture)}
  lock_file: .iwos/lock.yaml
  decision_ledger: .iwos/decisions.yaml
authority:
  proposal_pattern: "AIP-\\\\d{{4}}"
  decision_pattern: "ADR-\\\\d{{4}}"
  traceability_patterns: ["EWP-\\\\d{{4}}", "ADR-\\\\d{{4}}", "AIP-\\\\d{{4}}", "#\\\\d+"]
  traceability_required: true
  lock_must_change_with_protected: true
agents:
  files: [AGENTS.md]
"""
