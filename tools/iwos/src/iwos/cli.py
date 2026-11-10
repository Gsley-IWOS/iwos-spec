"""Command-line interface: iwos init | validate | lock | gate | agents | mcp."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import __version__, agents_block, checks, gate as gate_mod, lock as lock_mod, mcp_server
from .config import CONFIG_NAME, ConfigError, default_config_text, load_config


def _root(args) -> Path:
    return Path(args.root).resolve()


def cmd_init(args) -> int:
    root = _root(args)
    path = root / CONFIG_NAME
    if path.exists() and not args.force:
        print(f"{CONFIG_NAME} already exists; use --force to overwrite", file=sys.stderr)
        return 1
    protected = args.protected or ["docs/architecture/**", "GOVERNANCE.md"]
    path.write_text(default_config_text(args.name or root.name, protected, args.architecture or []), encoding="utf-8")
    cfg = load_config(root)
    lock_path = lock_mod.write_lock(cfg)
    for f in cfg.agent_files:
        agents_block.apply(cfg, root / f)
    print(f"wrote {CONFIG_NAME}, {lock_path.relative_to(root)} and {', '.join(cfg.agent_files)}")
    print("Next: commit these files, add `uses: Gsley-IWOS/iwos-spec@main` to a pull-request workflow, and point agents at `iwos mcp`.")
    return 0


def cmd_validate(args) -> int:
    cfg = load_config(_root(args))
    findings, summary = checks.validate(cfg)
    for f in findings:
        print(str(f))
    print(summary)
    return 0 if not findings else 1


def cmd_lock(args) -> int:
    cfg = load_config(_root(args))
    path = lock_mod.write_lock(cfg)
    print(f"wrote {path.relative_to(cfg.root)} covering {len(lock_mod.protected_files(cfg))} protected artefact(s)")
    return 0


def cmd_agents(args) -> int:
    cfg = load_config(_root(args))
    if args.check:
        stale = agents_block.stale_files(cfg)
        for f in stale:
            print(f"[agents] {f}: generated block is missing or stale")
        print("PASS: agent files are current" if not stale else f"FAIL: {len(stale)} stale agent file(s)")
        return 0 if not stale else 1
    changed = [f for f in cfg.agent_files if agents_block.apply(cfg, cfg.root / f)]
    print(f"updated {', '.join(changed)}" if changed else "agent files already current")
    return 0


def _read_body(args) -> str:
    if args.body:
        return Path(args.body).read_text(encoding="utf-8")
    if args.body_env:
        return os.environ.get(args.body_env, "")
    return ""


def cmd_gate(args) -> int:
    cfg = load_config(_root(args))
    result = gate_mod.run_gate(cfg, args.base, args.head, _read_body(args))
    md, js = result.to_markdown(), gate_mod.dumps(result)
    if args.format in ("markdown", "both"):
        print(md)
    if args.format == "json":
        print(js)
    if args.output:
        out = Path(args.output)
        out.write_text(md if out.suffix == ".md" else js, encoding="utf-8")
        if args.format == "both":
            out.with_suffix(".json").write_text(js, encoding="utf-8")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if args.summary and summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(md)
    return 0 if result.passed else 1


def cmd_mcp(args) -> int:
    cfg = load_config(_root(args))
    mcp_server.serve(cfg)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="iwos", description="IWOS Guard: constitution-as-code for repositories changed by AI agents.")
    p.add_argument("--root", default=".", help="repository root (default: current directory)")
    p.add_argument("--version", action="version", version=f"iwos {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("init", help="write a constitution file, the first lock and the agent block")
    s.add_argument("--name"); s.add_argument("--protected", action="append", help="protected glob (repeatable)")
    s.add_argument("--architecture", action="append", help="architecture glob (repeatable)"); s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("validate", help="check integrity, ledger, content and agent files"); s.set_defaults(func=cmd_validate)
    s = sub.add_parser("lock", help="regenerate the integrity lock (constitutional changes only)"); s.set_defaults(func=cmd_lock)
    s = sub.add_parser("agents", help="regenerate the generated block in agent files"); s.add_argument("--check", action="store_true"); s.set_defaults(func=cmd_agents)

    s = sub.add_parser("gate", help="evaluate a revision range against the constitution")
    s.add_argument("--base", required=True); s.add_argument("--head", default="HEAD")
    s.add_argument("--body", help="file holding the pull request description"); s.add_argument("--body-env", help="environment variable holding the pull request description")
    s.add_argument("--format", choices=["markdown", "json", "both"], default="markdown"); s.add_argument("--output", help="write the report here (.md or .json)")
    s.add_argument("--summary", action="store_true", help="append the Markdown report to $GITHUB_STEP_SUMMARY when set")
    s.set_defaults(func=cmd_gate)

    s = sub.add_parser("mcp", help="serve the authority interface over standard input and output"); s.set_defaults(func=cmd_mcp)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ConfigError as exc:
        print(f"constitution error: {exc}", file=sys.stderr)
        return 2
    except gate_mod.GateError as exc:
        print(f"gate error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
