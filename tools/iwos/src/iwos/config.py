"""Load and validate the constitution file (iwos.yaml) of a governed repository."""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

CONFIG_NAME = "iwos.yaml"
SPEC_VALIDATOR_CONFIG = "tools/validate/config.yaml"
EVENTS_FILE = ".iwos/events.jsonl"
WAIVERS_FILE = ".iwos/waivers.yaml"
INCIDENT_LEDGER = ".iwos/incidents.yaml"
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
    events_file: str = EVENTS_FILE
    waivers_file: str = WAIVERS_FILE
    incident_ledger: str = INCIDENT_LEDGER

    @property
    def spec_validator_config(self) -> Path | None:
        path = self.root / SPEC_VALIDATOR_CONFIG
        return path if self.profile == "iwos-spec" and path.exists() else None

    @property
    def control_files(self) -> list[str]:
        """Files that define the rules. They are protected whatever the constitution file says (ADR-0007)."""
        files = [CONFIG_NAME, self.waivers_file]
        if self.profile == "iwos-spec":
            files.append(SPEC_VALIDATOR_CONFIG)
        return files

    @property
    def automation_paths(self) -> list[str]:
        """Paths holding the automation that runs the gate. A change here makes the gate result non-independent."""
        paths = [".github/workflows/**"]
        if self.profile == "iwos-spec":
            paths += ["action.yml", "tools/iwos/**", "tools/validate/**"]
        return paths


def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_document(data) -> list[str]:
    errors = sorted(Draft202012Validator(schema()).iter_errors(data), key=lambda e: list(e.path))
    return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in errors]


def _parse_yaml(text: str, label: str) -> dict:
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        from .redact import describe_yaml_error
        raise ConfigError(f"{label}: {describe_yaml_error(exc)}") from exc


def load_config(root: Path) -> Config:
    """The constitution as it stands in the working tree."""
    root = Path(root).resolve()
    path = root / CONFIG_NAME
    if not path.exists():
        raise ConfigError(f"{CONFIG_NAME} not found in {root}. Run `iwos init` to create a constitution.")
    spec_path = root / SPEC_VALIDATOR_CONFIG
    spec_text = spec_path.read_text(encoding="utf-8") if spec_path.exists() else None
    return parse_config(root, path.read_text(encoding="utf-8"), spec_text, CONFIG_NAME)


def _show(root: Path, revision: str, rel_path: str) -> str | None:
    """The content of a file at a revision, or None when the revision does not hold it."""
    proc = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{rel_path}"], capture_output=True, text=True, check=False)
    return proc.stdout if proc.returncode == 0 else None


def load_config_at(root: Path, revision: str) -> Config | None:
    """The constitution in force at a revision, or None when that revision has none (an adoption change).

    The gate judges a change against the constitution of its base, never against the constitution the
    change itself proposes: otherwise a change could unprotect a file and rewrite it in one step.
    """
    root = Path(root).resolve()
    text = _show(root, revision, CONFIG_NAME)
    if text is None:
        return None
    return parse_config(root, text, _show(root, revision, SPEC_VALIDATOR_CONFIG), f"{CONFIG_NAME} at {revision[:12]}")


def read_at(root: Path, revision: str, rel_path: str) -> str | None:
    return _show(Path(root).resolve(), revision, rel_path)


def parse_config(root: Path, text: str, spec_text: str | None, label: str = CONFIG_NAME) -> Config:
    data = _parse_yaml(text, label)
    problems = validate_document(data)
    if problems:
        raise ConfigError(f"{label} does not conform to the constitution schema: " + "; ".join(problems))

    profile = data["profile"]
    constitution = data.get("constitution", {}) or {}
    authority = data.get("authority", {}) or {}
    agents = data.get("agents", {}) or {}
    checks = data.get("checks", {}) or {}

    protected = list(constitution.get("protected", []))
    lock_file = constitution.get("lock_file")
    ledger = constitution.get("decision_ledger")

    if profile == "iwos-spec":
        if spec_text is None:
            raise ConfigError(f"profile iwos-spec requires {SPEC_VALIDATOR_CONFIG} in the repository")
        spec_cfg = _parse_yaml(spec_text, SPEC_VALIDATOR_CONFIG)
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
