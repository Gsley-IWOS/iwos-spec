#!/usr/bin/env python3
"""IWOS specification repository validator.

Implements the four check categories of the Testing Standard (STD-TEST-001) plus the
constitutional integrity check of the Change Control Policy (GOV-004):

  structural   required metadata and headings on every governed Markdown document
  schema       every governed YAML artefact validates against its bound JSON Schema
  consistency  links, parent documents, identifiers, cross-references, drafting markers, secrets
  example      every valid example validates; every invalid example is rejected
  integrity    protected documents match .ai/CONSTITUTION_LOCK.yaml

Design record: ADR-0002. Dependencies: Python 3.10+, PyYAML, jsonschema.
Exit codes: 0 all checks passed; 1 at least one check failed; 2 the validator could not run.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover - exercised only in misconfigured environments
    sys.stderr.write(f"validator cannot run: missing dependency ({exc}). Install PyYAML and jsonschema.\n")
    sys.exit(2)

CATEGORIES = ("structural", "schema", "consistency", "example", "integrity")

FENCE_RE = re.compile(r"^```.*?^```[ \t]*$", re.MULTILINE | re.DOTALL)
METADATA_RE = re.compile(r"^\*\*([A-Za-z][A-Za-z ]+?):\*\*[ \t]*(.*?)[ \t]*$")
HEADING_RE = re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SECTION_NUMBER_RE = re.compile(r"^(?:Article|Section)\s+\d+\.\s+|^\d+(?:\.\d+)*\.?\s+")


@dataclass
class Finding:
    category: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"[{self.category}] {self.path}: {self.message}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    checked: dict[str, int] = field(default_factory=lambda: {c: 0 for c in CATEGORIES})

    def fail(self, category: str, path: Path | str, message: str) -> None:
        self.findings.append(Finding(category, str(path), message))

    def count(self, category: str, n: int = 1) -> None:
        self.checked[category] = self.checked.get(category, 0) + n

    @property
    def ok(self) -> bool:
        return not self.findings


# --------------------------------------------------------------------------- helpers

def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def strip_fences(text: str) -> str:
    """Remove fenced code blocks so template bodies are not mistaken for document structure."""
    return FENCE_RE.sub("", text)


def parse_metadata(text: str) -> dict[str, str | list[str]]:
    """Parse bold metadata lines. A key whose value is empty collects the bullet list that follows."""
    lines = text.splitlines()
    metadata: dict[str, str | list[str]] = {}
    i = 0
    while i < len(lines):
        match = METADATA_RE.match(lines[i].strip())
        if match:
            key, value = match.group(1).strip(), match.group(2).strip()
            if key in metadata:
                i += 1
                continue
            if value:
                metadata[key] = value
            else:
                items: list[str] = []
                j = i + 1
                while j < len(lines):
                    stripped = lines[j].strip()
                    if not stripped:
                        j += 1
                        continue
                    if stripped.startswith("- "):
                        items.append(stripped[2:].strip())
                        j += 1
                        continue
                    break
                metadata[key] = items
        i += 1
    return metadata


def headings(text: str) -> list[str]:
    found = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            found.append(match.group(1).strip())
    return found


def normalise_heading(value: str) -> str:
    """Drop numbering such as 'Article 1. ' or 'Section 3. ' or '2.1 ' before comparing."""
    return SECTION_NUMBER_RE.sub("", value).strip().lower()


def has_heading(doc_headings: list[str], wanted: str) -> bool:
    wanted_norm = wanted.lower()
    return any(normalise_heading(h) == wanted_norm or normalise_heading(h).startswith(wanted_norm + ":") for h in doc_headings)


def split_values(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return value
    return [v.strip() for v in value.split(",") if v.strip()]


def resolve_reference(root: Path, doc: Path, ref: str) -> Path | None:
    """Resolve a reference relative to the repository root, then relative to the document."""
    ref = ref.split("#", 1)[0].strip().strip("`")
    if not ref or "://" in ref or ref.startswith("mailto:"):
        return None
    candidates = [root / ref, doc.parent / ref]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return root / ref


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


ALWAYS_SKIP = {"__pycache__", ".git"}


def excluded(rel: Path, exclude_dirs: set[str]) -> bool:
    """A path is excluded when its top-level directory is listed, or any ancestor is always skipped."""
    parts = rel.parts[:-1]
    return bool(parts) and (parts[0] in exclude_dirs or any(p in ALWAYS_SKIP for p in parts))


def iter_markdown(root: Path, config: dict) -> list[Path]:
    exclude_dirs = set(config["markdown"]["exclude_dirs"])
    exclude_files = set(config["markdown"]["exclude_files"])
    files = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if excluded(rel, exclude_dirs):
            continue
        if rel.name in exclude_files:
            continue
        files.append(path)
    return files


def iter_text_files(root: Path, exclude_dirs: set[str]) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if excluded(rel, exclude_dirs):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".pyc"}:
            continue
        files.append(path)
    return files


def protected_paths(root: Path, config: dict) -> list[Path]:
    paths: set[Path] = set()
    for pattern in config["protected_documents"]["patterns"]:
        for path in root.glob(pattern):
            if path.is_file():
                paths.add(path)
    return sorted(paths)


def build_lock(root: Path, config: dict, today: str | None = None) -> dict:
    today = today or _dt.date.today().isoformat()
    return {
        "schema_version": "1.0.0",
        "document": {
            "id": "MEM-008",
            "version": "1.0.0",
            "status": "Active",
            "authority": "governance/change-control-policy.md",
            "last_updated": today,
        },
        "algorithm": "sha256",
        "generated_by": "tools/validate/validate.py --write-lock",
        "entries": [
            {"path": str(p.relative_to(root)).replace("\\", "/"), "sha256": sha256_of(p)}
            for p in protected_paths(root, config)
        ],
    }


def write_lock(root: Path, config: dict) -> Path:
    """Write the lock. The date is kept from the existing lock when the entries are unchanged, so the
    operation is idempotent and the lock only changes when a protected document changes."""
    lock_path = root / config["protected_documents"]["lock_file"]
    lock = build_lock(root, config)
    if lock_path.exists():
        try:
            previous = load_yaml(lock_path)
        except yaml.YAMLError:
            previous = None
        if isinstance(previous, dict) and previous.get("entries") == lock["entries"]:
            lock["document"]["last_updated"] = previous.get("document", {}).get("last_updated", lock["document"]["last_updated"])
    header = (
        "# Constitutional integrity lock. GENERATED by `make lock`; do not edit by hand.\n"
        "# Regenerate only in the same change that alters a protected document under an accepted proposal.\n"
        "# Schema: schemas/constitution-lock.schema.json\n"
    )
    lock_path.write_text(header + yaml.safe_dump(lock, sort_keys=False), encoding="utf-8")
    return lock_path


# --------------------------------------------------------------------------- checks

def check_structural(root: Path, config: dict, report: Report) -> dict[str, list[Path]]:
    """Return a map of Document ID -> paths for the identifier uniqueness check."""
    md_cfg = config["markdown"]
    exemptions = {e["path"]: e["reason"] for e in md_cfg.get("structural_exemptions", [])}
    metadata_exemptions = {e["path"]: set(e["keys"]) for e in md_cfg.get("metadata_exemptions", [])}
    ids: dict[str, list[Path]] = {}
    version_re = re.compile(md_cfg["version_pattern"])
    date_re = re.compile(md_cfg["date_pattern"])
    id_re = re.compile(config["identifiers"]["pattern"])
    rat_heading = md_cfg["ratification_heading"]
    rat_line_re = re.compile(md_cfg["ratification_line_pattern"], re.MULTILINE)

    for path in iter_markdown(root, config):
        rel = str(path.relative_to(root)).replace("\\", "/")
        report.count("structural")
        raw = path.read_text(encoding="utf-8")
        if not raw.strip():
            report.fail("structural", rel, "file is empty")
            continue
        text = strip_fences(raw)
        meta = parse_metadata(text)
        doc_headings = headings(text)
        if rel in exemptions:
            if "Document ID" in meta:
                ids.setdefault(str(meta["Document ID"]).strip(), []).append(path)
            continue

        if not doc_headings or not raw.lstrip().startswith("# "):
            report.fail("structural", rel, "document must start with a level-1 title")

        for key in md_cfg["required_metadata"]:
            if key in metadata_exemptions.get(rel, set()):
                continue
            if key not in meta or not meta[key]:
                report.fail("structural", rel, f"missing metadata '{key}'")

        authority = str(meta.get("Authority", "")).strip()
        has_parent = any(key in meta and meta[key] for key in md_cfg["parent_metadata_keys"])
        if not has_parent and authority not in md_cfg["parent_exempt_authorities"]:
            report.fail("structural", rel, "missing metadata 'Parent Document' or 'Parent Documents'")

        if "Document ID" in meta:
            doc_id = str(meta["Document ID"]).strip()
            if not id_re.match(doc_id):
                report.fail("structural", rel, f"Document ID '{doc_id}' does not match the identifier pattern")
            ids.setdefault(doc_id, []).append(path)
        if "Version" in meta and not version_re.match(str(meta["Version"]).strip()):
            report.fail("structural", rel, f"Version '{meta['Version']}' is not semantic")
        if "Status" in meta and str(meta["Status"]).strip() not in md_cfg["allowed_statuses"]:
            report.fail("structural", rel, f"Status '{meta['Status']}' is not an allowed status")
        if "Last Updated" in meta and not date_re.match(str(meta["Last Updated"]).strip()):
            report.fail("structural", rel, f"Last Updated '{meta['Last Updated']}' is not an ISO date")

        for wanted in md_cfg["required_headings"]:
            if not has_heading(doc_headings, wanted):
                report.fail("structural", rel, f"missing required heading '{wanted}'")

        if not has_heading(doc_headings, rat_heading) and not rat_line_re.search(text):
            report.fail("structural", rel, "missing ratification section or Document Status line")

        for family in md_cfg.get("families", []):
            if fnmatch.fnmatch(rel, family["match"]) and not path.name == "README.md":
                for wanted in family.get("headings", []):
                    if not has_heading(doc_headings, wanted):
                        report.fail("structural", rel, f"missing heading '{wanted}' required for {family['match']}")
                for key in family.get("metadata", []):
                    if key not in meta or not meta[key]:
                        report.fail("structural", rel, f"missing metadata '{key}' required for {family['match']}")
    return ids


def load_bindings(root: Path, config: dict, report: Report) -> list[dict]:
    bindings_path = root / config["bindings_file"]
    schema_path = root / config["bindings_schema"]
    report.count("schema")
    if not bindings_path.exists() or not schema_path.exists():
        report.fail("schema", config["bindings_file"], "bindings file or its schema is missing")
        return []
    try:
        bindings = load_yaml(bindings_path)
        schema = load_json(schema_path)
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(bindings), key=lambda e: list(e.path))
    except (yaml.YAMLError, json.JSONDecodeError, SchemaError) as exc:
        report.fail("schema", config["bindings_file"], f"cannot load bindings: {exc}")
        return []
    for error in errors:
        report.fail("schema", config["bindings_file"], f"{'/'.join(str(p) for p in error.path) or '<root>'}: {error.message}")
    return [] if errors else bindings["bindings"]


def validator_for(root: Path, schema_rel: str, report: Report) -> Draft202012Validator | None:
    schema_path = root / schema_rel
    if not schema_path.exists():
        report.fail("schema", schema_rel, "schema file does not exist")
        return None
    try:
        schema = load_json(schema_path)
        Draft202012Validator.check_schema(schema)
    except (json.JSONDecodeError, SchemaError) as exc:
        report.fail("schema", schema_rel, f"invalid schema: {exc}")
        return None
    meta = schema.get("x-iwos-document")
    required = {"id", "version", "status", "authority", "parent_document"}
    if not isinstance(meta, dict) or not required.issubset(meta):
        report.fail("schema", schema_rel, "schema must carry x-iwos-document with id, version, status, authority, parent_document")
    elif not str(schema.get("$id", "")).endswith("/" + str(meta["version"])):
        report.fail("schema", schema_rel, "final segment of $id must equal x-iwos-document.version")
    return Draft202012Validator(schema)


def validate_instance(validator: Draft202012Validator, instance) -> list[str]:
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in errors]


def check_schema(root: Path, config: dict, report: Report, bindings: list[dict]) -> None:
    for binding in bindings:
        validator = validator_for(root, binding["schema"], report)
        if validator is None:
            continue
        for artefact in binding.get("artefacts", []):
            report.count("schema")
            path = root / artefact
            if not path.exists():
                report.fail("schema", artefact, "bound artefact does not exist")
                continue
            try:
                instance = load_yaml(path)
            except yaml.YAMLError as exc:
                report.fail("schema", artefact, f"invalid YAML: {exc}")
                continue
            for message in validate_instance(validator, instance)[:10]:
                report.fail("schema", artefact, message)


EXPECT_RE = re.compile(r"^#\s*expect:\s*(.+?)\s*$", re.MULTILINE)


def expected_errors(text: str) -> list[str]:
    """Return the `# expect: <text>` declarations at the top of an invalid example."""
    return EXPECT_RE.findall(text)


def check_examples(root: Path, config: dict, report: Report, bindings: list[dict]) -> None:
    validators = {b["schema"]: validator_for(root, b["schema"], Report()) for b in bindings}  # errors reported by check_schema
    for binding in bindings:
        validator = validators[binding["schema"]]
        if validator is None:
            continue
        example_dir = root / binding["examples"]
        valid_dir, invalid_dir = example_dir / "valid", example_dir / "invalid"
        for sub, expect_valid in ((valid_dir, True), (invalid_dir, False)):
            files = sorted(p for p in sub.glob("*.y*ml")) if sub.exists() else []
            if not files:
                report.fail("example", binding["examples"], f"no examples in {sub.name}/ for {binding['schema']}")
                continue
            for example in files:
                report.count("example")
                rel = str(example.relative_to(root)).replace("\\", "/")
                try:
                    instance = load_yaml(example)
                except yaml.YAMLError as exc:
                    report.fail("example", rel, f"example must be valid YAML that the schema evaluates: {exc}")
                    continue
                errors = validate_instance(validator, instance)
                if expect_valid:
                    if errors:
                        report.fail("example", rel, f"valid example rejected: {errors[0]}")
                    continue
                if not errors:
                    report.fail("example", rel, "invalid example was accepted by the schema")
                    continue
                expectations = expected_errors(example.read_text(encoding="utf-8"))
                if not expectations:
                    report.fail("example", rel, "invalid example must declare the expected error with a `# expect:` comment")
                for expectation in expectations:
                    if not any(expectation in error for error in errors):
                        report.fail("example", rel, f"expected error containing '{expectation}' but got: {errors[0]}")


def check_consistency(root: Path, config: dict, report: Report, ids: dict[str, list[Path]], bindings: list[dict]) -> None:
    md_cfg = config["markdown"]
    id_re = re.compile(config["identifiers"]["pattern"])
    sources = config.get("identifier_sources", {})

    def register_id(doc_id, rel: str) -> None:
        report.count("consistency")
        if not isinstance(doc_id, str) or not id_re.match(doc_id):
            report.fail("consistency", rel, f"document identifier '{doc_id}' does not match the identifier pattern")
            return
        ids.setdefault(doc_id, []).append(root / rel)

    for rel in sources.get("yaml_document_id", []):
        if (root / rel).exists():
            try:
                data = load_yaml(root / rel)
            except yaml.YAMLError:
                continue
            register_id((data or {}).get("document", {}).get("id"), rel)
    for rel in sources.get("contract_id", []):
        if (root / rel).exists():
            try:
                data = load_yaml(root / rel)
            except yaml.YAMLError:
                continue
            register_id((data or {}).get("contract", {}).get("id"), rel)
    for path in sorted(root.glob(sources.get("json_schema_glob", "schemas/*.schema.json"))):
        try:
            data = load_json(path)
        except json.JSONDecodeError:
            continue
        register_id((data.get("x-iwos-document") or {}).get("id"), str(path.relative_to(root)).replace("\\", "/"))

    # Identifier uniqueness.
    for doc_id, paths in sorted(ids.items()):
        report.count("consistency")
        if len(paths) > 1:
            listed = ", ".join(str(p.relative_to(root)) for p in paths)
            report.fail("consistency", listed, f"Document ID '{doc_id}' is used more than once")

    # Links and parent documents.
    exemptions = {e["path"] for e in md_cfg.get("structural_exemptions", [])}
    for path in iter_markdown(root, config):
        rel = str(path.relative_to(root)).replace("\\", "/")
        if rel in exemptions:
            continue
        text = strip_fences(path.read_text(encoding="utf-8"))
        meta = parse_metadata(text)
        for key in md_cfg["parent_metadata_keys"]:
            for parent in split_values(meta.get(key, [])):
                report.count("consistency")
                target = resolve_reference(root, path, parent)
                if target is not None and not target.exists():
                    report.fail("consistency", rel, f"parent document '{parent}' does not exist")
        for link in LINK_RE.findall(text):
            if link.startswith("#"):
                continue
            report.count("consistency")
            target = resolve_reference(root, path, link)
            if target is not None and not target.exists():
                report.fail("consistency", rel, f"link target '{link}' does not exist")

    # Drafting markers.
    markers = config["content"]["drafting_markers"]
    marker_res = [re.compile(r"(?<![A-Za-z0-9_])" + re.escape(m) + r"(?![A-Za-z0-9_])") for m in markers]
    exclude_dirs = set(config["content"]["drafting_marker_exclude_dirs"])
    for path in iter_text_files(root, exclude_dirs):
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".json"}:
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        report.count("consistency")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker, marker_re in zip(markers, marker_res):
            if marker_re.search(text):
                report.fail("consistency", rel, f"drafting marker '{marker}' present")

    # Secret shapes.
    secret_res = [re.compile(p) for p in config["content"]["secret_patterns"]]
    secret_exclude = set(config["content"].get("secret_scan_exclude_files", []))
    for path in iter_text_files(root, {".git"}):
        rel = str(path.relative_to(root)).replace("\\", "/")
        if rel in secret_exclude:
            continue
        report.count("consistency")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for secret_re in secret_res:
            if secret_re.search(text):
                report.fail("consistency", rel, "content matches a credential pattern")
                break

    # Cross-references in governed YAML artefacts.
    refs = config["cross_references"]

    def exists(ref: str) -> bool:
        return (root / ref).exists()

    def yaml_or_none(rel: str):
        path = root / rel
        if not path.exists():
            report.fail("consistency", rel, "required artefact does not exist")
            return None
        try:
            return load_yaml(path)
        except yaml.YAMLError as exc:
            report.fail("consistency", rel, f"invalid YAML: {exc}")
            return None

    bootstrap = yaml_or_none(refs["ai_bootstrap"])
    contract = yaml_or_none(refs["ai_agent_contract"])
    if isinstance(bootstrap, dict):
        for section in ("contract_mandatory_reading", "repository_onboarding_reading", "recommended_reading"):
            for item in bootstrap.get(section, []) or []:
                report.count("consistency")
                if not exists(item.get("path", "")):
                    report.fail("consistency", refs["ai_bootstrap"], f"{section} path '{item.get('path')}' does not exist")
        for key, value in (("document.authority", (bootstrap.get("document") or {}).get("authority")),
                           ("document.parent_document", (bootstrap.get("document") or {}).get("parent_document")),
                           ("protected_documents.lock_file", (bootstrap.get("protected_documents") or {}).get("lock_file")),
                           ("prohibited_actions_source", bootstrap.get("prohibited_actions_source")),
                           ("ratification.amendment_authority", (bootstrap.get("ratification") or {}).get("amendment_authority"))):
            report.count("consistency")
            if value and not exists(value):
                report.fail("consistency", refs["ai_bootstrap"], f"{key} '{value}' does not exist")
        declared = [i.get("path") for i in bootstrap.get("contract_mandatory_reading", []) or []]
        if isinstance(contract, dict):
            contract_list = list((contract.get("agent_requirements") or {}).get("mandatory_reading", []) or [])
            report.count("consistency")
            if sorted(declared) != sorted(contract_list):
                report.fail("consistency", refs["ai_bootstrap"], "contract_mandatory_reading does not match mandatory_reading in the AI Agent Contract")
        protected = bootstrap.get("protected_documents") or {}
        report.count("consistency")
        if sorted(protected.get("path_patterns", []) or []) != sorted(config["protected_documents"]["patterns"]):
            report.fail("consistency", refs["ai_bootstrap"], "protected_documents.path_patterns differ from protected_documents.patterns in the validator configuration")
        if protected.get("lock_file") != config["protected_documents"]["lock_file"]:
            report.fail("consistency", refs["ai_bootstrap"], "protected_documents.lock_file differs from the validator configuration")
        for key, value in (bootstrap.get("engineering_memory") or {}).items():
            report.count("consistency")
            if not exists(value):
                report.fail("consistency", refs["ai_bootstrap"], f"engineering_memory.{key} '{value}' does not exist")
        for key in ("template",):
            value = (bootstrap.get("handoff") or {}).get(key, "")
            if value and not exists(value):
                report.fail("consistency", refs["ai_bootstrap"], f"handoff.{key} '{value}' does not exist")
        ci = (bootstrap.get("validation") or {}).get("continuous_integration", "")
        if ci and not exists(ci):
            report.fail("consistency", refs["ai_bootstrap"], f"validation.continuous_integration '{ci}' does not exist")

    if isinstance(contract, dict):
        for ref in (contract.get("agent_requirements") or {}).get("mandatory_reading", []) or []:
            report.count("consistency")
            if not exists(ref):
                report.fail("consistency", refs["ai_agent_contract"], f"mandatory_reading '{ref}' does not exist")

    graph = yaml_or_none(refs["knowledge_graph"])
    if isinstance(graph, dict):
        node_ids: set[str] = set()
        for node in graph.get("nodes", []) or []:
            report.count("consistency")
            if node.get("id") in node_ids:
                report.fail("consistency", refs["knowledge_graph"], f"node id '{node.get('id')}' is declared more than once")
            node_ids.add(node.get("id"))
            if node.get("path") and not exists(node["path"]):
                report.fail("consistency", refs["knowledge_graph"], f"node '{node.get('id')}' path '{node['path']}' does not exist")
            if node.get("document_id") and node["document_id"] not in ids and not str(node.get("path", "")).endswith((".yaml", ".yml")):
                report.fail("consistency", refs["knowledge_graph"], f"node '{node.get('id')}' document_id '{node['document_id']}' is not declared by any Markdown document")
        for edge in graph.get("edges", []) or []:
            report.count("consistency")
            for end in ("from", "to"):
                if edge.get(end) not in node_ids:
                    report.fail("consistency", refs["knowledge_graph"], f"edge endpoint '{edge.get(end)}' is not a node")

    decisions = yaml_or_none(refs["decision_graph"])
    if isinstance(decisions, dict):
        for decision in decisions.get("decisions", []) or []:
            report.count("consistency")
            for ref in [decision.get("authority", "")] + list(decision.get("related_files", []) or []) + list(decision.get("related_records", []) or []):
                if ref and not exists(ref):
                    report.fail("consistency", refs["decision_graph"], f"{decision.get('id')} references '{ref}' which does not exist")

    state = yaml_or_none(refs["engineering_state"])
    if isinstance(state, dict):
        for decision in ((state.get("state") or {}).get("current_decisions") or []):
            report.count("consistency")
            if not exists(decision.get("record", "")):
                report.fail("consistency", refs["engineering_state"], f"decision '{decision.get('id')}' record '{decision.get('record')}' does not exist")
        for wp in state.get("work_packages", []) or []:
            report.count("consistency")
            if not exists(f"work-packages/{wp.get('id')}.md"):
                report.fail("consistency", refs["engineering_state"], f"work package '{wp.get('id')}' has no file")

    manifest = yaml_or_none(refs["memory_manifest"])
    if isinstance(manifest, dict):
        for entry in manifest.get("files", []) or []:
            report.count("consistency")
            if entry.get("required") and not exists(entry.get("path", "")):
                report.fail("consistency", refs["memory_manifest"], f"required memory file '{entry.get('path')}' does not exist")
            if entry.get("schema") and not exists(entry["schema"]):
                report.fail("consistency", refs["memory_manifest"], f"schema '{entry['schema']}' does not exist")

    for binding in bindings:
        report.count("consistency")
        if not exists(binding["examples"]):
            report.fail("consistency", config["bindings_file"], f"example directory '{binding['examples']}' does not exist")


def check_integrity(root: Path, config: dict, report: Report) -> None:
    lock_rel = config["protected_documents"]["lock_file"]
    lock_path = root / lock_rel
    report.count("integrity")
    if not lock_path.exists():
        report.fail("integrity", lock_rel, "constitutional integrity lock is missing; run `make lock` under valid authority")
        return
    try:
        lock = load_yaml(lock_path)
    except yaml.YAMLError as exc:
        report.fail("integrity", lock_rel, f"invalid YAML: {exc}")
        return
    if not isinstance(lock, dict) or not isinstance(lock.get("entries"), list):
        report.fail("integrity", lock_rel, "lock is not a mapping with an entries list")
        return
    recorded = {entry.get("path"): entry.get("sha256") for entry in lock["entries"] if isinstance(entry, dict)}
    current = {str(p.relative_to(root)).replace("\\", "/"): sha256_of(p) for p in protected_paths(root, config)}
    for path, digest in sorted(current.items()):
        report.count("integrity")
        if path not in recorded:
            report.fail("integrity", path, "protected document is not recorded in the lock")
        elif recorded[path] != digest:
            report.fail("integrity", path, "protected document differs from the ratified digest in the lock")
    for path in sorted(set(recorded) - set(current)):
        report.fail("integrity", path, "lock records a protected document that no longer exists")


# --------------------------------------------------------------------------- entry point

def run(root: Path, config: dict) -> Report:
    report = Report()
    ids = check_structural(root, config, report)
    bindings = load_bindings(root, config, report)
    check_schema(root, config, report, bindings)
    check_examples(root, config, report, bindings)
    check_consistency(root, config, report, ids, bindings)
    check_integrity(root, config, report)
    return report


def default_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=default_root(), help="repository root (default: inferred)")
    parser.add_argument("--config", type=Path, default=None, help="configuration file (default: tools/validate/config.yaml)")
    parser.add_argument("--write-lock", action="store_true", help="regenerate the constitutional integrity lock and exit")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    config_path = args.config or root / "tools" / "validate" / "config.yaml"
    if not config_path.exists():
        sys.stderr.write(f"validator cannot run: configuration {config_path} not found\n")
        return 2
    config = load_yaml(config_path)

    if args.write_lock:
        path = write_lock(root, config)
        print(f"wrote {path.relative_to(root)} covering {len(protected_paths(root, config))} protected documents")
        return 0

    report = run(root, config)
    for finding in report.findings:
        print(str(finding))
    summary = ", ".join(f"{c}={report.checked.get(c, 0)}" for c in CATEGORIES)
    if report.ok:
        print(f"PASS: all checks passed ({summary})")
        return 0
    print(f"FAIL: {len(report.findings)} finding(s) ({summary})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
