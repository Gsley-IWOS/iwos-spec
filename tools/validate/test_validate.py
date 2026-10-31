"""Unit tests for the IWOS repository validator.

Run with: python3 -m unittest discover -s tools/validate -p 'test_*.py'
Tests are deterministic and build small fixture repositories in temporary directories.
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as v  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG = yaml.safe_load((REPO_ROOT / "tools" / "validate" / "config.yaml").read_text(encoding="utf-8"))

GOOD_DOC = """# Example Document

**Document ID:** GOV-999  
**Version:** 1.0.0  
**Status:** Ratified  
**Authority:** IWOS Engineering Constitution  
**Parent Document:** parent.md  
**Last Updated:** 2026-10-31

## Purpose

Example.

## Ratification

Effective on merge.
"""


ADR_HEADINGS = ["Context", "Decision Drivers", "Options Considered", "Decision", "Consequences"]
WP_HEADINGS = ["Objective", "Scope", "Non-Scope", "Inputs", "Outputs", "Validation Criteria", "Completion Evidence"]


def family_doc(doc_id: str, extra_headings: list[str], extra_meta: dict[str, str]) -> str:
    """Build a document that satisfies the family rules for the given headings and metadata."""
    meta_lines = "".join(f"**{k}:** {v}  \n" for k, v in extra_meta.items())
    body = "".join(f"## {h}\n\nExample.\n\n" for h in extra_headings)
    return GOOD_DOC.replace("GOV-999", doc_id).replace("**Last Updated:**", meta_lines + "**Last Updated:**").replace("## Ratification", body + "## Ratification")


class ParsingTests(unittest.TestCase):
    def test_parse_metadata_inline_and_list(self):
        text = "**Document ID:** AB-001\n\n**Parent Documents:**\n\n- a.md\n- b.md\n\n# Purpose\n"
        meta = v.parse_metadata(text)
        self.assertEqual(meta["Document ID"], "AB-001")
        self.assertEqual(meta["Parent Documents"], ["a.md", "b.md"])

    def test_parse_metadata_keeps_first_occurrence(self):
        text = "**Status:** Ratified\n**Status:** Draft\n"
        self.assertEqual(v.parse_metadata(text)["Status"], "Ratified")

    def test_strip_fences_removes_template_bodies(self):
        text = "# Title\n\n```markdown\n# Inner\n**Status:** Draft\n```\n\n## Purpose\n"
        stripped = v.strip_fences(text)
        self.assertNotIn("Inner", stripped)
        self.assertEqual(v.headings(stripped), ["Title", "Purpose"])

    def test_heading_normalisation_ignores_numbering(self):
        self.assertTrue(v.has_heading(["Article 7. Scope and Change Control"], "Scope and Change Control"))
        self.assertTrue(v.has_heading(["Section 2. Delivery Strategy"], "Delivery Strategy"))
        self.assertTrue(v.has_heading(["1. Purpose"], "Purpose"))
        self.assertFalse(v.has_heading(["Purposes"], "Purpose"))

    def test_split_values(self):
        self.assertEqual(v.split_values("a.md, b.md"), ["a.md", "b.md"])
        self.assertEqual(v.split_values(["x"]), ["x"])


class FixtureRepo:
    """A minimal repository that satisfies every check, for mutation in tests."""

    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="iwos-validate-"))
        self.config = copy.deepcopy(CONFIG)
        self.config["markdown"]["structural_exemptions"] = []
        self.config["protected_documents"]["patterns"] = ["protected/*"]
        self.config["identifier_sources"]["yaml_document_id"] = ["AI_BOOTSTRAP.yaml", ".ai/MANIFEST.yaml", ".ai/ENGINEERING_STATE.yaml", ".ai/KNOWLEDGE_GRAPH.yaml", ".ai/DECISION_GRAPH.yaml", "schemas/bindings.yaml"]
        self.write("protected/LAW.md", GOOD_DOC.replace("GOV-999", "FC-001").replace("**Parent Document:** parent.md  \n", "").replace("IWOS Engineering Constitution", "Supreme"))
        self.write("parent.md", GOOD_DOC.replace("GOV-999", "GOV-001").replace("parent.md", "protected/LAW.md"))
        self.write("README.md", GOOD_DOC.replace("GOV-999", "ROOT-001"))
        # Copy the real schemas, bindings and examples so schema checks are exercised end to end.
        shutil.copytree(REPO_ROOT / "schemas", self.root / "schemas")
        shutil.copytree(REPO_ROOT / "examples", self.root / "examples")
        # Index documents reference parents that the fixture does not reproduce.
        (self.root / "schemas" / "README.md").unlink()
        (self.root / "examples" / "README.md").unlink()
        shutil.rmtree(self.root / "examples" / "ai-agent-contract")
        shutil.rmtree(self.root / "examples" / "constitution-lock")
        shutil.rmtree(self.root / "examples" / "bindings")
        bindings = yaml.safe_load((self.root / "schemas" / "bindings.yaml").read_text(encoding="utf-8"))
        keep = {"schemas/ai-bootstrap.schema.json", "schemas/engineering-state.schema.json",
                "schemas/knowledge-graph.schema.json", "schemas/decision-graph.schema.json",
                "schemas/memory-manifest.schema.json"}
        bindings["bindings"] = [b for b in bindings["bindings"] if b["schema"] in keep]
        (self.root / "schemas" / "bindings.yaml").write_text(yaml.safe_dump(bindings, sort_keys=False), encoding="utf-8")
        # Governed YAML artefacts: reuse the valid examples as live artefacts.
        self.copy_example("ai-bootstrap", "AI_BOOTSTRAP.yaml")
        self.copy_example("engineering-state", ".ai/ENGINEERING_STATE.yaml")
        self.copy_example("knowledge-graph", ".ai/KNOWLEDGE_GRAPH.yaml")
        self.copy_example("decision-graph", ".ai/DECISION_GRAPH.yaml")
        self.copy_example("memory-manifest", ".ai/MANIFEST.yaml")
        plain = [".ai/README.md", ".ai/CURRENT_STATE.md", ".ai/NEXT_TASK.md", "CHANGELOG.md",
                 "engineering-charter/00_FOUNDING_CHARTER.md", "engineering-charter/01_PROJECT_GENESIS.md",
                 "engineering-charter/02_ARCHITECTURE_BASELINE.md", "engineering-charter/06_ENGINEERING_CONSTITUTION.md"]
        for n, rel in enumerate(plain):
            self.write(rel, GOOD_DOC.replace("GOV-999", f"X-{n + 100:03d}"))
        self.write("work-packages/EWP-0001.md", family_doc("EWP-0001", WP_HEADINGS, {"Sprint": "0", "Milestone": "M0"}))
        self.write("adr/ADR-0001-architecture-decision-records.md", family_doc("ADR-0001", ADR_HEADINGS, {"Date": "2026-10-31"}))
        self.write(".github/pull_request_template.md", "## Summary\n")
        self.write(".github/workflows/validate.yml", "name: ci\n")
        contract = (REPO_ROOT / "examples/ai-agent-contract/valid/minimal.yaml").read_text(encoding="utf-8")
        contract = contract.replace("  mandatory_reading:\n    - engineering-charter/00_FOUNDING_CHARTER.md\n",
                                    "  mandatory_reading:\n    - engineering-charter/00_FOUNDING_CHARTER.md\n    - engineering-charter/01_PROJECT_GENESIS.md\n    - engineering-charter/02_ARCHITECTURE_BASELINE.md\n    - engineering-charter/06_ENGINEERING_CONSTITUTION.md\n")
        self.write("engineering-charter/05_AI_AGENT_CONTRACT.yaml", contract)
        # The live bootstrap example mirrors the real repository's protected patterns; align the fixture.
        boot = self.root / "AI_BOOTSTRAP.yaml"
        data = yaml.safe_load(boot.read_text(encoding="utf-8"))
        data["protected_documents"]["path_patterns"] = ["protected/*"]
        boot.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        self.config["cross_references"]["ai_agent_contract"] = "engineering-charter/05_AI_AGENT_CONTRACT.yaml"
        v.write_lock(self.root, self.config)

    def copy_example(self, name: str, dest: str) -> None:
        src = REPO_ROOT / "examples" / name / "valid" / "minimal.yaml"
        self.write(dest, src.read_text(encoding="utf-8"))

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run(self) -> v.Report:
        return v.run(self.root, self.config)

    def cleanup(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.repo = FixtureRepo()
        self.addCleanup(self.repo.cleanup)

    def findings(self, category: str | None = None) -> list[str]:
        report = self.repo.run()
        return [str(f) for f in report.findings if category is None or f.category == category]

    def test_fixture_passes(self):
        self.assertEqual(self.findings(), [])

    def test_missing_metadata_is_structural_failure(self):
        self.repo.write("broken.md", GOOD_DOC.replace("**Status:** Ratified  \n", "").replace("GOV-999", "GOV-998"))
        self.assertTrue(any("missing metadata 'Status'" in f for f in self.findings("structural")))

    def test_empty_file_is_structural_failure(self):
        self.repo.write("empty.md", "")
        self.assertTrue(any("file is empty" in f for f in self.findings("structural")))

    def test_missing_ratification_is_structural_failure(self):
        self.repo.write("norat.md", GOOD_DOC.replace("## Ratification\n\nEffective on merge.\n", "").replace("GOV-999", "GOV-997"))
        self.assertTrue(any("ratification" in f for f in self.findings("structural")))

    def test_document_status_line_counts_as_ratification(self):
        doc = GOOD_DOC.replace("## Ratification\n\nEffective on merge.\n", "**Document Status:** Ratified\n").replace("GOV-999", "GOV-996")
        self.repo.write("status-line.md", doc)
        self.assertEqual(self.findings("structural"), [])

    def test_supreme_authority_needs_no_parent(self):
        self.assertEqual([f for f in self.findings("structural") if "LAW.md" in f], [])

    def test_family_headings_enforced(self):
        self.repo.write("adr/ADR-0002-example.md", GOOD_DOC.replace("GOV-999", "ADR-0002"))
        self.repo.write("adr/ADR-0003-good.md", family_doc("ADR-0003", ADR_HEADINGS, {"Date": "2026-10-31"}))
        failures = self.findings("structural")
        self.assertTrue(any("Decision Drivers" in f for f in failures))
        self.assertTrue(any("missing metadata 'Date'" in f for f in failures))
        self.assertEqual([f for f in failures if "ADR-0003-good.md" in f], [])

    def test_metadata_exemption_is_key_specific(self):
        self.repo.write("old.md", GOOD_DOC.replace("GOV-999", "GOV-990").replace("**Last Updated:** 2026-10-31\n", ""))
        self.repo.config["markdown"]["metadata_exemptions"] = [{"path": "old.md", "keys": ["Last Updated"], "reason": "test"}]
        self.assertEqual([f for f in self.findings("structural") if "old.md" in f], [])
        self.repo.write("old.md", GOOD_DOC.replace("GOV-999", "GOV-990").replace("**Status:** Ratified  \n", ""))
        self.assertTrue(any("old.md" in f and "'Status'" in f for f in self.findings("structural")))

    def test_structural_exemption_skips_checks_but_not_emptiness(self):
        self.repo.write("legacy.md", "LEGACY BANNER FORMAT\n")
        self.repo.config["markdown"]["structural_exemptions"] = [{"path": "legacy.md", "reason": "test"}]
        self.assertEqual(self.findings("structural"), [])
        self.repo.write("legacy.md", "")
        self.assertTrue(any("file is empty" in f for f in self.findings("structural")))

    def test_duplicate_identifier_is_consistency_failure(self):
        self.repo.write("dup.md", GOOD_DOC)  # GOV-999 already used by nothing; add twice
        self.repo.write("dup2.md", GOOD_DOC)
        self.assertTrue(any("used more than once" in f for f in self.findings("consistency")))

    def test_broken_link_and_parent_are_consistency_failures(self):
        self.repo.write("links.md", GOOD_DOC.replace("GOV-999", "GOV-995").replace("parent.md", "missing-parent.md").replace("Example.", "See [x](nowhere.md)."))
        failures = self.findings("consistency")
        self.assertTrue(any("parent document 'missing-parent.md'" in f for f in failures))
        self.assertTrue(any("link target 'nowhere.md'" in f for f in failures))

    def test_links_inside_fences_are_ignored(self):
        self.repo.write("fenced.md", GOOD_DOC.replace("GOV-999", "GOV-994").replace("Example.", "Example.\n\n```markdown\n[x](<path>)\n```"))
        self.assertEqual([f for f in self.findings("consistency") if "fenced.md" in f], [])

    def test_drafting_marker_is_consistency_failure(self):
        self.repo.write("marker.md", GOOD_DOC.replace("GOV-999", "GOV-993").replace("Example.", "Finish this TODO later."))
        self.assertTrue(any("drafting marker 'TODO'" in f for f in self.findings("consistency")))

    def test_marker_inside_word_is_not_flagged(self):
        self.repo.write("word.md", GOOD_DOC.replace("GOV-999", "GOV-992").replace("Example.", "No TODOs remain."))
        self.assertEqual([f for f in self.findings("consistency") if "word.md" in f], [])

    def test_credential_shape_is_consistency_failure(self):
        self.repo.write("secret.md", GOOD_DOC.replace("GOV-999", "GOV-991").replace("Example.", "Key AKIA" + "ABCDEFGHIJKLMNOP" + "."))
        self.assertTrue(any("credential pattern" in f for f in self.findings("consistency")))

    def test_schema_violation_in_bound_artefact(self):
        path = self.repo.root / ".ai" / "ENGINEERING_STATE.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["quality_gates"]["human_review"] = "optional"
        path.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.assertTrue(any("ENGINEERING_STATE.yaml" in f for f in self.findings("schema")))

    def test_invalid_example_that_validates_is_example_failure(self):
        src = self.repo.root / "examples" / "engineering-state" / "valid" / "minimal.yaml"
        self.repo.write("examples/engineering-state/invalid/actually-valid.yaml", src.read_text(encoding="utf-8"))
        self.assertTrue(any("invalid example was accepted" in f for f in self.findings("example")))

    def test_missing_examples_directory_is_example_failure(self):
        shutil.rmtree(self.repo.root / "examples" / "knowledge-graph" / "invalid")
        self.assertTrue(any("no examples in invalid/" in f for f in self.findings("example")))

    def test_knowledge_graph_dangling_edge(self):
        path = self.repo.root / ".ai" / "KNOWLEDGE_GRAPH.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["edges"].append({"from": "founding_charter", "to": "ghost", "relationship": "governs"})
        path.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.assertTrue(any("edge endpoint 'ghost'" in f for f in self.findings("consistency")))

    def test_ratification_heading_must_be_exact(self):
        doc = GOOD_DOC.replace("## Ratification\n\nEffective on merge.\n", "## Ratified Standards\n\nList.\n").replace("GOV-999", "GOV-989")
        self.repo.write("ratified-list.md", doc)
        self.assertTrue(any("ratified-list.md" in f and "ratification" in f for f in self.findings("structural")))

    def test_yaml_document_ids_join_uniqueness_check(self):
        self.repo.write("clash.md", GOOD_DOC.replace("GOV-999", "MEM-003"))  # same as ENGINEERING_STATE.yaml document.id
        self.assertTrue(any("'MEM-003' is used more than once" in f for f in self.findings("consistency")))

    def test_exempt_document_id_still_registered(self):
        self.repo.write("legacy.md", "# Legacy\n\n**Document ID:** GOV-001\n")
        self.repo.config["markdown"]["structural_exemptions"] = [{"path": "legacy.md", "reason": "test"}]
        self.assertTrue(any("'GOV-001' is used more than once" in f for f in self.findings("consistency")))

    def test_bootstrap_protected_patterns_must_match_config(self):
        boot = self.repo.root / "AI_BOOTSTRAP.yaml"
        data = yaml.safe_load(boot.read_text(encoding="utf-8"))
        data["protected_documents"]["path_patterns"] = ["somewhere-else/*"]
        boot.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        self.assertTrue(any("path_patterns differ" in f for f in self.findings("consistency")))

    def test_bootstrap_mandatory_reading_must_match_contract(self):
        boot = self.repo.root / "AI_BOOTSTRAP.yaml"
        data = yaml.safe_load(boot.read_text(encoding="utf-8"))
        data["contract_mandatory_reading"][0]["path"] = "README.md"
        boot.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        self.assertTrue(any("does not match mandatory_reading" in f for f in self.findings("consistency")))

    def test_invalid_example_requires_expect_comment_and_matching_error(self):
        src = (self.repo.root / "examples" / "knowledge-graph" / "invalid" / "unknown-relationship.yaml").read_text(encoding="utf-8")
        self.repo.write("examples/knowledge-graph/invalid/no-expect.yaml", src.replace("# expect: edges/0/relationship\n", ""))
        self.repo.write("examples/knowledge-graph/invalid/wrong-expect.yaml", src.replace("# expect: edges/0/relationship", "# expect: nodes/9/id"))
        failures = self.findings("example")
        self.assertTrue(any("no-expect.yaml" in f and "must declare the expected error" in f for f in failures))
        self.assertTrue(any("wrong-expect.yaml" in f and "expected error containing 'nodes/9/id'" in f for f in failures))

    def test_example_that_is_not_yaml_fails(self):
        self.repo.write("examples/knowledge-graph/invalid/broken.yaml", "key: [unclosed\n")
        self.assertTrue(any("broken.yaml" in f and "must be valid YAML" in f for f in self.findings("example")))

    def test_schema_id_version_mismatch_is_schema_failure(self):
        path = self.repo.root / "schemas" / "knowledge-graph.schema.json"
        data = v.load_json(path)
        data["$id"] = data["$id"].rsplit("/", 1)[0] + "/9.9.9"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("final segment of $id" in f for f in self.findings("schema")))

    def test_knowledge_graph_undeclared_document_id(self):
        path = self.repo.root / ".ai" / "KNOWLEDGE_GRAPH.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["nodes"].append({"id": "ghost_doc", "type": "standard", "label": "Ghost", "document_id": "STD-GHOST-001", "path": "README.md"})
        path.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.assertTrue(any("document_id 'STD-GHOST-001' is not declared" in f for f in self.findings("consistency")))

    def test_engineering_state_work_package_without_file(self):
        path = self.repo.root / ".ai" / "ENGINEERING_STATE.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["work_packages"].append({"id": "EWP-0099", "name": "Ghost", "status": "Proposed"})
        path.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.assertTrue(any("work package 'EWP-0099' has no file" in f for f in self.findings("consistency")))

    def test_secret_scan_exclusion(self):
        self.repo.write("notes/allowed.txt", "AKIA" + "ABCDEFGHIJKLMNOP")
        self.repo.config["content"]["secret_scan_exclude_files"] = ["notes/allowed.txt"]
        self.assertEqual([f for f in self.findings("consistency") if "allowed.txt" in f], [])

    def test_write_lock_is_idempotent_and_changes_with_content(self):
        lock_path = self.repo.root / ".ai" / "CONSTITUTION_LOCK.yaml"
        first = lock_path.read_text(encoding="utf-8")
        data = yaml.safe_load(first)
        data["document"]["last_updated"] = "2000-01-01"
        lock_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        v.write_lock(self.repo.root, self.repo.config)
        self.assertEqual(yaml.safe_load(lock_path.read_text(encoding="utf-8"))["document"]["last_updated"], "2000-01-01")
        law = self.repo.root / "protected" / "LAW.md"
        law.write_text(law.read_text(encoding="utf-8") + "\nAmended.\n", encoding="utf-8")
        v.write_lock(self.repo.root, self.repo.config)
        self.assertNotEqual(yaml.safe_load(lock_path.read_text(encoding="utf-8"))["document"]["last_updated"], "2000-01-01")

    def test_integrity_detects_protected_change(self):
        self.assertEqual(self.findings("integrity"), [])
        law = self.repo.root / "protected" / "LAW.md"
        law.write_text(law.read_text(encoding="utf-8") + "\nAn unauthorised amendment.\n", encoding="utf-8")
        self.assertTrue(any("differs from the ratified digest" in f for f in self.findings("integrity")))

    def test_integrity_detects_unrecorded_and_removed_documents(self):
        self.repo.write("protected/NEW.md", GOOD_DOC.replace("GOV-999", "FC-002"))
        self.assertTrue(any("not recorded in the lock" in f for f in self.findings("integrity")))
        v.write_lock(self.repo.root, self.repo.config)
        (self.repo.root / "protected" / "NEW.md").unlink()
        self.assertTrue(any("no longer exists" in f for f in self.findings("integrity")))

    def test_write_lock_output_validates_against_schema(self):
        lock = v.build_lock(REPO_ROOT, CONFIG, today="2026-10-31")
        schema = v.load_json(REPO_ROOT / "schemas" / "constitution-lock.schema.json")
        errors = list(v.Draft202012Validator(schema).iter_errors(lock))
        self.assertEqual(errors, [])

    def test_missing_lock_is_integrity_failure(self):
        (self.repo.root / ".ai" / "CONSTITUTION_LOCK.yaml").unlink()
        self.assertTrue(any("lock is missing" in f for f in self.findings("integrity")))


class EntryPointTests(unittest.TestCase):
    def test_main_returns_nonzero_on_failure_and_zero_on_success(self):
        repo = FixtureRepo()
        self.addCleanup(repo.cleanup)
        config_path = repo.write("tools/validate/config.yaml", yaml.safe_dump(repo.config))
        self.assertEqual(v.main(["--root", str(repo.root), "--config", str(config_path)]), 0)
        repo.write("bad.md", "")
        self.assertEqual(v.main(["--root", str(repo.root), "--config", str(config_path)]), 1)

    def test_write_lock_cli(self):
        repo = FixtureRepo()
        self.addCleanup(repo.cleanup)
        config_path = repo.write("tools/validate/config.yaml", yaml.safe_dump(repo.config))
        (repo.root / ".ai" / "CONSTITUTION_LOCK.yaml").unlink()
        self.assertEqual(v.main(["--root", str(repo.root), "--config", str(config_path), "--write-lock"]), 0)
        self.assertTrue((repo.root / ".ai" / "CONSTITUTION_LOCK.yaml").exists())
        self.assertEqual(v.main(["--root", str(repo.root), "--config", str(config_path)]), 0)

    def test_missing_config_is_exit_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(v.main(["--root", tmp]), 2)


if __name__ == "__main__":
    unittest.main()
