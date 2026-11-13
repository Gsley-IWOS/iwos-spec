"""End-to-end tests for IWOS Guard. Each test builds a throwaway git repository.

Run: PYTHONPATH=tools/iwos/src python3 -m unittest discover -s tools/iwos/tests
"""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
SRC = HERE.parents[1] / "src"
REPO_ROOT = HERE.parents[3]
sys.path.insert(0, str(SRC))

from iwos import agents_block, checks, cli, gate, lock, mcp_server  # noqa: E402
from iwos.config import ConfigError, load_config  # noqa: E402


def git(root: Path, *args: str) -> str:
    env = {**os.environ, "GIT_AUTHOR_NAME": "Human Maintainer", "GIT_AUTHOR_EMAIL": "maintainer@example.test",
           "GIT_COMMITTER_NAME": "Human Maintainer", "GIT_COMMITTER_EMAIL": "maintainer@example.test"}
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True, env=env).stdout


class Fixture:
    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="iwos-guard-"))
        git(self.root, "init", "-q", "-b", "main")
        self.write("docs/architecture/baseline.md", "# Baseline\n\nThe ratified architecture.\n")
        self.write("GOVERNANCE.md", "# Governance\n\nRules.\n")
        self.write("src/core/engine.py", "print('core')\n")
        self.write("README.md", "# Example\n")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "-m", "Initial import")
        self.run_cli("init", "--protected", "docs/architecture/**", "--protected", "GOVERNANCE.md", "--architecture", "src/core/**")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "-m", "Adopt IWOS constitution (EWP-0001)")

    def write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def run_cli(self, *args: str) -> tuple[int, str]:
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            code = cli.main(["--root", str(self.root), *args])
        finally:
            sys.stdout = old
        return code, buf.getvalue()

    def cfg(self):
        return load_config(self.root)

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


class InitAndValidate(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)

    def test_init_writes_constitution_lock_and_agent_block(self):
        self.assertTrue((self.fx.root / "iwos.yaml").exists())
        lock_data = yaml.safe_load((self.fx.root / ".iwos/lock.yaml").read_text())
        self.assertEqual(sorted(e["path"] for e in lock_data["entries"]), ["GOVERNANCE.md", "docs/architecture/baseline.md"])
        self.assertIn(agents_block.BEGIN, (self.fx.root / "AGENTS.md").read_text())

    def test_validate_passes_on_fresh_repo(self):
        code, out = self.fx.run_cli("validate")
        self.assertEqual(code, 0, out)
        self.assertIn("PASS", out)

    def test_validate_fails_when_protected_changes_without_lock(self):
        self.fx.write("GOVERNANCE.md", "# Governance\n\nQuietly amended.\n")
        code, out = self.fx.run_cli("validate")
        self.assertEqual(code, 1)
        self.assertIn("differs from the digest", out)

    def test_lock_is_idempotent(self):
        before = (self.fx.root / ".iwos/lock.yaml").read_text()
        self.fx.run_cli("lock")
        self.assertEqual(before, (self.fx.root / ".iwos/lock.yaml").read_text())

    def test_missing_constitution_is_exit_two(self):
        (self.fx.root / "iwos.yaml").unlink()
        code, _ = self.fx.run_cli("validate")
        self.assertEqual(code, 2)

    def test_invalid_constitution_is_rejected(self):
        (self.fx.root / "iwos.yaml").write_text("schema_version: '1.0.0'\nprofile: whatever\n")
        with self.assertRaises(ConfigError):
            load_config(self.fx.root)

    def test_stale_agent_block_fails_check(self):
        (self.fx.root / "iwos.yaml").write_text((self.fx.root / "iwos.yaml").read_text().replace('    - "GOVERNANCE.md"\n', '    - "GOVERNANCE.md"\n    - "SECURITY.md"\n'))
        code, _ = self.fx.run_cli("agents", "--check")
        self.assertEqual(code, 1)
        self.fx.run_cli("agents")
        code, _ = self.fx.run_cli("agents", "--check")
        self.assertEqual(code, 0)

    def test_content_checks_flag_markers_and_secrets(self):
        self.fx.write("notes.md", "Finish this TODO.\n")
        self.fx.write("config.txt", "key = AKIA" + "ABCDEFGHIJKLMNOP" + "\n")
        findings, _ = checks.validate(self.fx.cfg())
        messages = [str(f) for f in findings]
        self.assertTrue(any("drafting marker" in m for m in messages))
        self.assertTrue(any("credential pattern" in m for m in messages))

    def test_ledger_problems_are_reported(self):
        self.fx.write(".iwos/decisions.yaml", "decisions:\n  - id: DEC-0001\n    title: x\n")
        findings, _ = checks.validate(self.fx.cfg())
        self.assertTrue(any("lacks 'date'" in str(f) for f in findings))


class Gate(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)
        self.base = git(self.fx.root, "rev-parse", "HEAD").strip()

    def commit_all(self, message: str, author: str = "Human Maintainer <maintainer@example.test>"):
        git(self.fx.root, "add", "-A")
        git(self.fx.root, "commit", "-q", f"--author={author}", "-m", message)
        return git(self.fx.root, "rev-parse", "HEAD").strip()

    def test_ordinary_change_with_citation_passes(self):
        self.fx.write("README.md", "# Example\n\nMore.\n")
        head = self.commit_all("Expand README (EWP-0002)")
        r = gate.run_gate(self.fx.cfg(), self.base, head)
        self.assertTrue(r.passed, r.blocking)
        self.assertEqual(r.traceability_citations, ["EWP-0002"])

    def test_ordinary_change_without_citation_fails_traceability(self):
        self.fx.write("README.md", "# Example\n\nMore.\n")
        head = self.commit_all("Expand README")
        r = gate.run_gate(self.fx.cfg(), self.base, head)
        self.assertFalse(r.passed)
        self.assertTrue(any("no authority citation" in b for b in r.blocking))

    def test_protected_change_without_proposal_and_lock_fails(self):
        self.fx.write("GOVERNANCE.md", "# Governance\n\nRewritten by an agent.\n")
        head = self.commit_all("Rewrite governance (EWP-0003)", author="Codex Agent <codex@example.test>")
        r = gate.run_gate(self.fx.cfg(), self.base, head)
        self.assertFalse(r.passed)
        self.assertEqual(len(r.blocking), 2)
        self.assertIn("Codex Agent (commit author)", r.agents)
        self.assertNotIn("@", md := r.to_markdown())
        self.assertTrue(any("every commit in this range is attributed to an agent" in w for w in r.warnings))
        self.assertIn("IWOS gate report: FAIL", md)
        self.assertIn("GOVERNANCE.md", md)

    def test_protected_change_with_proposal_and_lock_passes(self):
        self.fx.write("GOVERNANCE.md", "# Governance\n\nAmended under AIP-0007.\n")
        self.fx.run_cli("lock")
        head = self.commit_all("Amend governance\n\nAuthorised by AIP-0007.")
        r = gate.run_gate(self.fx.cfg(), self.base, head, body="Implements AIP-0007 as accepted.")
        self.assertTrue(r.passed, r.blocking)
        self.assertEqual(r.proposal_citations, ["AIP-0007"])
        self.assertTrue(r.lock_changed)

    def test_architecture_change_requires_decision_record(self):
        self.fx.write("src/core/engine.py", "print('rewired')\n")
        head = self.commit_all("Rewire core (EWP-0005)")
        r = gate.run_gate(self.fx.cfg(), self.base, head)
        self.assertFalse(r.passed)
        self.assertTrue(any("decision-record citation" in b for b in r.blocking))
        r2 = gate.run_gate(self.fx.cfg(), self.base, head, body="Per ADR-0012.")
        self.assertTrue(r2.passed, r2.blocking)

    def test_agent_trailers_are_detected(self):
        self.fx.write("README.md", "# Example\n\nAgent edit.\n")
        head = self.commit_all("Edit README (EWP-0002)\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>\nClaude-Session: https://example.test/session")
        r = gate.run_gate(self.fx.cfg(), self.base, head)
        self.assertIn("Claude Fable 5.1 (Co-Authored-By trailer)", r.agents)
        self.assertEqual(r.humans, ["Human Maintainer"])
        self.assertIn("Claude-Session", r.commits[0].trailers)
        self.assertNotIn("noreply@", r.to_markdown())
        self.assertNotIn("maintainer@example.test", gate.dumps(r))

    def test_agent_committing_as_a_human_is_caught_only_by_disclosure(self):
        """The shape of the real pull request 1: human commit identity, agent named only in the description and label."""
        self.fx.write("GOVERNANCE.md", "# Governance\n\nReplaced.\n")
        head = self.commit_all("Add governance onboarding")
        silent = gate.run_gate(self.fx.cfg(), self.base, head)
        self.assertEqual(silent.agents, [])
        self.assertTrue(any("no agent disclosed" in w for w in silent.warnings))
        disclosed = gate.run_gate(self.fx.cfg(), self.base, head, body="Done.\n\n[Codex Task](https://chatgpt.com/codex/cloud/tasks/task_x)", labels=["codex"])
        self.assertIn("OpenAI Codex (pull request description)", disclosed.agents)
        self.assertIn("codex (pull request label)", disclosed.agents)
        self.assertTrue(any("rests on disclosure alone" in w for w in disclosed.warnings))
        self.assertFalse(disclosed.passed)

    def test_report_shows_resolved_revisions(self):
        self.fx.write("README.md", "# Example\n\nMore.\n")
        self.commit_all("Expand README (EWP-0002)")
        r = gate.run_gate(self.fx.cfg(), self.base, "HEAD")
        self.assertEqual(len(r.head_sha), 12)
        self.assertIn(r.head_sha, r.to_markdown())
        self.assertNotIn("..HEAD", r.to_markdown())

    def test_cli_gate_writes_both_formats(self):
        self.fx.write("README.md", "# Example\n\nMore.\n")
        head = self.commit_all("Expand README (EWP-0002)")
        out = self.fx.root / "report.md"
        code, printed = self.fx.run_cli("gate", "--base", self.base, "--head", head, "--format", "both", "--output", str(out), "--label", "codex")
        self.assertEqual(code, 0, printed)
        self.assertTrue(out.exists() and out.with_suffix(".json").exists())
        report = json.loads(out.with_suffix(".json").read_text())
        self.assertEqual(report["result"], "pass")
        self.assertIn("codex (pull request label)", report["agents"])

    def test_unknown_ref_is_exit_two(self):
        code, _ = self.fx.run_cli("gate", "--base", "no-such-ref")
        self.assertEqual(code, 2)


class Mcp(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)

    def roundtrip(self, *messages: dict) -> list[dict]:
        stdin = io.StringIO("\n".join(json.dumps(m) for m in messages) + "\n")
        stdout = io.StringIO()
        mcp_server.serve(self.fx.cfg(), stdin=stdin, stdout=stdout)
        return [json.loads(l) for l in stdout.getvalue().splitlines() if l.strip()]

    def test_initialize_list_and_check_authority(self):
        out = self.roundtrip(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "check_authority", "arguments": {"path": "docs/architecture/baseline.md"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "check_authority", "arguments": {"path": "src/core/engine.py"}}},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "check_authority", "arguments": {"path": "README.md"}}},
        )
        self.assertEqual(out[0]["result"]["protocolVersion"], "2025-06-18")
        self.assertEqual(out[0]["result"]["serverInfo"]["name"], "iwos")
        names = [t["name"] for t in out[1]["result"]["tools"]]
        self.assertEqual(names, ["check_authority", "list_protected", "read_state", "record_decision", "validate"])
        a = json.loads(out[2]["result"]["content"][0]["text"])
        self.assertTrue(a["protected"] and a["lock_matches"])
        b = json.loads(out[3]["result"]["content"][0]["text"])
        self.assertTrue(b["architecture"] and not b["protected"])
        c = json.loads(out[4]["result"]["content"][0]["text"])
        self.assertFalse(c["protected"] or c["architecture"])

    def test_record_decision_appends_and_never_rewrites(self):
        args = {"title": "Use SQLite for the cache", "context": "A cache is needed and must be embedded.", "decision": "Use SQLite.",
                "consequences": ["No server to run."], "authority": "docs/architecture/baseline.md", "related_files": ["README.md"]}
        out = self.roundtrip({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "record_decision", "arguments": args}},
                             {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "record_decision", "arguments": {**args, "title": "Second"}}},
                             {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "read_state"}})
        first = json.loads(out[0]["result"]["content"][0]["text"])["recorded"]
        self.assertEqual(first["id"], "DEC-0001")
        ledger = yaml.safe_load((self.fx.root / ".iwos/decisions.yaml").read_text())
        self.assertEqual([d["id"] for d in ledger["decisions"]], ["DEC-0001", "DEC-0002"])
        self.assertEqual(ledger["decisions"][0]["title"], "Use SQLite for the cache")
        state = json.loads(out[2]["result"]["content"][0]["text"])
        self.assertEqual(state["decisions"], 2)
        findings, _ = checks.validate(self.fx.cfg())
        self.assertEqual([str(f) for f in findings], [])

    def test_errors_are_tool_errors_not_crashes(self):
        out = self.roundtrip({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "nope"}},
                             {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "check_authority", "arguments": {}}},
                             {"jsonrpc": "2.0", "id": 3, "method": "unknown/method"},
                             {"jsonrpc": "2.0", "id": 4, "method": "ping"})
        self.assertEqual(out[0]["error"]["code"], -32602)
        self.assertTrue(out[1]["result"]["isError"])
        self.assertEqual(out[2]["error"]["code"], -32601)
        self.assertEqual(out[3]["result"], {})

    def test_server_runs_as_subprocess(self):
        proc = subprocess.run([sys.executable, "-m", "iwos.cli", "--root", str(self.fx.root), "mcp"],
                              input=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}) + "\n",
                              capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(SRC)}, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("check_authority", proc.stdout)


class SpecProfile(unittest.TestCase):
    """The repository that defines the toolchain must pass its own constitution."""

    def test_iwos_spec_profile_loads_and_protects_the_charter(self):
        cfg = load_config(REPO_ROOT)
        self.assertEqual(cfg.profile, "iwos-spec")
        self.assertIn("engineering-charter/*", cfg.protected)
        self.assertEqual(cfg.lock_file, ".ai/CONSTITUTION_LOCK.yaml")
        self.assertTrue(lock.matches_protected(cfg, "engineering-charter/00_FOUNDING_CHARTER.md"))
        self.assertTrue(lock.matches_protected(cfg, "governance/decision-process.md"))
        self.assertFalse(lock.matches_protected(cfg, "governance/rfc/README.md"))
        self.assertFalse(lock.matches_protected(cfg, "standards/README.md"))
        self.assertTrue(lock.matches_protected(cfg, "standards/naming-standard.md"))
        self.assertTrue(lock.matches_architecture(cfg, "architecture/engineering-governance/SPEC-ENGGOV-001.md"))
        self.assertEqual(lock.glob_to_regex("docs/**").match("docs/a/b.md") is not None, True)
        self.assertIsNone(lock.glob_to_regex("docs/*.md").match("docs/a/b.md"))
        self.assertEqual(lock.check_lock(cfg), [])

    def test_bundled_schema_matches_repository_schema(self):
        bundled = json.loads((SRC / "iwos" / "iwos_config.schema.json").read_text())
        canonical = json.loads((REPO_ROOT / "schemas" / "iwos-config.schema.json").read_text())
        self.assertEqual(bundled, canonical)

    def test_repository_validates_under_iwos(self):
        findings, summary = checks.validate(load_config(REPO_ROOT))
        self.assertEqual([str(f) for f in findings], [], summary)


if __name__ == "__main__":
    unittest.main()
