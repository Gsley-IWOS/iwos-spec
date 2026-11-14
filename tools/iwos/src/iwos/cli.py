"""Command-line interface: iwos init | validate | lock | gate | agents | events | lessons | stats | incident | mcp."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import __version__, agents_block, checks, events, gate as gate_mod, incidents, lock as lock_mod, mcp_server, sarif
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
    print("Next: commit these files, add `uses: Gsley-IWOS/iwos-spec@<commit>` to a pull-request workflow, and point agents at `iwos mcp`.")
    return 0


def cmd_validate(args) -> int:
    cfg = load_config(_root(args))
    findings, summary = checks.validate(cfg)
    for f in findings:
        print(str(f))
    print(summary)
    if args.sarif:
        Path(args.sarif).write_text(json.dumps(sarif.from_validation(findings, cfg.lock_file), indent=2), encoding="utf-8")
    if any(f.category == "integrity" or "credential pattern" in f.message for f in findings):
        print("A finding above is a security incident. Record it with `iwos incident open` and follow `iwos incident playbook <class>`.")
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
    cfg, adoption = gate_mod.constitution_for(_root(args), args.base)
    labels = list(args.label or [])
    if args.labels_env:
        labels += [l.strip() for l in os.environ.get(args.labels_env, "").split(",") if l.strip()]
    result = gate_mod.run_gate(cfg, args.base, args.head, _read_body(args), labels, adoption=adoption)
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
    event = result.to_event(__version__)
    if args.event_out:
        Path(args.event_out).write_text(json.dumps(event, sort_keys=True) + "\n", encoding="utf-8")
    if args.record:
        events.append_event(load_config(_root(args)), event)
    if args.sarif:
        Path(args.sarif).write_text(json.dumps(sarif.from_gate(result), indent=2), encoding="utf-8")
    return 0 if result.passed else 1


def cmd_events(args) -> int:
    cfg = load_config(_root(args))
    added = 0
    for name in args.files:
        for line in Path(name).read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append_event(cfg, json.loads(line))
                added += 1
    print(f"appended {added} event(s) to {cfg.events_file}")
    return 0


def cmd_lessons(args) -> int:
    cfg = load_config(_root(args))
    data = events.lessons(cfg, args.limit)
    if args.format == "json":
        print(json.dumps(data, indent=2))
        return 0
    print(f"{data['gate_runs']} gate run(s) recorded, {data['failed_runs']} failed.")
    for item in data["lessons"]:
        where = f" Most affected: {', '.join(item['most_affected_paths'])}." if item["most_affected_paths"] else ""
        print(f"- {item['rule']} x{item['occurrences']}: {item['title']}. {item['advice']}{where}")
    if not data["lessons"]:
        print("No blocking finding recorded yet.")
    return 0


def cmd_stats(args) -> int:
    print(json.dumps(events.stats(load_config(_root(args))), indent=2))
    return 0


def cmd_incident(args) -> int:
    cfg = load_config(_root(args))
    if args.action == "open":
        entry = incidents.open_incident(cfg, args.incident_class, args.severity, args.summary, args.path or [], args.detected_by)
        print(f"opened {entry['id']} ({entry['class']}, {entry['severity']}) in {cfg.incident_ledger}")
        for i, step in enumerate(incidents.PLAYBOOKS[entry["class"]], 1):
            print(f"  {i}. {step}")
    elif args.action == "update":
        entry = incidents.update_incident(cfg, args.id, args.status, args.note, args.decision or "")
        print(f"{entry['id']} is now {entry['status']}")
    elif args.action == "playbook":
        if args.incident_class not in incidents.PLAYBOOKS:
            raise incidents.IncidentError(f"unknown class '{args.incident_class}'; one of {', '.join(incidents.CLASSES)}")
        for i, step in enumerate(incidents.PLAYBOOKS[args.incident_class], 1):
            print(f"{i}. {step}")
    else:
        entries = incidents.load(cfg)["incidents"]
        for e in entries:
            print(f"{e.get('id')}  {e.get('status'):<9}  {e.get('severity'):<8}  {e.get('class')}  {e.get('summary')}")
        if not entries:
            print("No incident recorded.")
    return 0


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

    s = sub.add_parser("validate", help="check integrity, ledgers, content and agent files")
    s.add_argument("--sarif", help="also write the findings as SARIF 2.1.0 to this file"); s.set_defaults(func=cmd_validate)
    s = sub.add_parser("lock", help="regenerate the integrity lock (constitutional changes only)"); s.set_defaults(func=cmd_lock)
    s = sub.add_parser("agents", help="regenerate the generated block in agent files"); s.add_argument("--check", action="store_true"); s.set_defaults(func=cmd_agents)

    s = sub.add_parser("gate", help="evaluate a revision range against the constitution")
    s.add_argument("--base", required=True); s.add_argument("--head", default="HEAD")
    s.add_argument("--body", help="file holding the pull request description"); s.add_argument("--body-env", help="environment variable holding the pull request description")
    s.add_argument("--label", action="append", help="pull request label (repeatable); labels matching an agent marker count as disclosure")
    s.add_argument("--labels-env", help="environment variable holding comma-separated pull request labels")
    s.add_argument("--format", choices=["markdown", "json", "both"], default="markdown"); s.add_argument("--output", help="write the report here (.md or .json)")
    s.add_argument("--summary", action="store_true", help="append the Markdown report to $GITHUB_STEP_SUMMARY when set")
    s.add_argument("--event-out", help="write the structured event record of this run to this file")
    s.add_argument("--record", action="store_true", help="append the event record to the local event log")
    s.add_argument("--sarif", help="also write the findings as SARIF 2.1.0 to this file")
    s.set_defaults(func=cmd_gate)

    s = sub.add_parser("events", help="append event records produced by `iwos gate --event-out` to the event log")
    s.add_argument("action", choices=["append"]); s.add_argument("files", nargs="+"); s.set_defaults(func=cmd_events)
    s = sub.add_parser("lessons", help="what the event log says agents get wrong here, as structured fields")
    s.add_argument("--limit", type=int, default=5); s.add_argument("--format", choices=["text", "json"], default="text"); s.set_defaults(func=cmd_lessons)
    s = sub.add_parser("stats", help="print an anonymous summary of the event log (rule identifiers and counts only)"); s.set_defaults(func=cmd_stats)

    s = sub.add_parser("incident", help="record and track security incidents in the incident ledger")
    isub = s.add_subparsers(dest="action", required=True)
    o = isub.add_parser("open"); o.add_argument("--class", dest="incident_class", required=True, choices=sorted(incidents.CLASSES))
    o.add_argument("--severity", required=True, choices=incidents.SEVERITIES); o.add_argument("--summary", required=True)
    o.add_argument("--path", action="append"); o.add_argument("--detected-by", default="maintainer")
    u = isub.add_parser("update"); u.add_argument("id"); u.add_argument("--status", required=True, choices=incidents.STATUSES)
    u.add_argument("--note", required=True); u.add_argument("--decision", help="decision record that closes the loop")
    isub.add_parser("list")
    b = isub.add_parser("playbook"); b.add_argument("incident_class")
    s.set_defaults(func=cmd_incident)

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
    except (incidents.IncidentError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
