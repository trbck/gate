#!/usr/bin/env python3
"""Regenerate PORTFOLIO.md from every <project>/.gate/ in the workspace.

Reads simple `key: value` frontmatter from charter.md and scorecard.md
(no external deps). Enforces reporting of the hard rules: active-count vs
WIP limit, ZOMBIE detection, kill_by breaches.

Usage:
    python3 gate-portfolio.py [--root /home/trbck/workspace] [--wip 3]
                              [--out PORTFOLIO.md] [--check]

--check exits 1 if any hard rule is violated (usable in CI / cron / hooks).
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

SKIP_PREFIXES = ("_", ".")


def parse_frontmatter(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            out[key.strip()] = val.split("#", 1)[0].strip().strip('"')
    return out


def days_since(datestr: str, today: dt.date) -> int | None:
    try:
        return (today - dt.date.fromisoformat(datestr)).days
    except (ValueError, TypeError):
        return None


def collect(root: Path, today: dt.date) -> list[dict]:
    rows = []
    for project_dir in sorted(root.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith(SKIP_PREFIXES):
            continue
        gate = project_dir / ".gate"
        if not gate.is_dir():
            continue
        charter = parse_frontmatter(gate / "charter.md")
        score = parse_frontmatter(gate / "scorecard.md")
        last_delta = score.get("last_gate_delta", "")
        row = {
            "project": charter.get("project", project_dir.name),
            "type": charter.get("type", "?"),
            "status": charter.get("status", "?"),
            "stage": score.get("stage", charter.get("stage", "?")),
            "score": score.get("score", "?"),
            "health": score.get("health", "no-audit"),
            "north_star": charter.get("north_star", "?"),
            "current": charter.get("north_star_current", "?"),
            "kill_by": charter.get("kill_by", "?"),
            "delta_days": days_since(last_delta, today),
            "audit_days": days_since(score.get("audited", ""), today),
        }
        d = row["delta_days"]
        if row["status"] == "active" and (d is None or d > 30):
            row["health"] = "ZOMBIE"
        kb = days_since(row["kill_by"], today)
        row["kill_breached"] = kb is not None and kb >= 0 and row["status"] in ("active", "parked")
        rows.append(row)
    return rows


def render(rows: list[dict], wip: int, today: dt.date) -> tuple[str, list[str]]:
    violations: list[str] = []
    active = [r for r in rows if r["status"] == "active"]
    if len(active) > wip:
        violations.append(
            f"WIP limit breached: {len(active)} active projects (max {wip}): "
            + ", ".join(r["project"] for r in active)
        )
    for r in rows:
        if r["health"] == "ZOMBIE":
            violations.append(f"ZOMBIE: {r['project']} is active with no gate delta in >30d (or never audited)")
        if r["kill_breached"]:
            violations.append(f"KILL-BY reached: {r['project']} ({r['kill_by']}) — decide: recommit / park / kill")

    order = {"active": 0, "candidate": 1, "parked": 2, "killed": 3, "?": 4}
    rows = sorted(rows, key=lambda r: (order.get(r["status"], 4), str(r["project"])))

    lines = [
        "# PORTFOLIO",
        "",
        f"Generated {today.isoformat()} by gate-portfolio.py — do not hand-edit the table.",
        f"WIP limit: {wip} active. Weekly review notes go below the table.",
        "",
        "| Project | Type | Status | Stage | Score | Health | North star | Now | Kill by | Δ days |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        delta = "—" if r["delta_days"] is None else str(r["delta_days"])
        lines.append(
            f"| {r['project']} | {r['type']} | {r['status']} | {r['stage']} | {r['score']} "
            f"| {r['health']} | {r['north_star']} | {r['current']} | {r['kill_by']} | {delta} |"
        )
    lines.append("")
    if violations:
        lines.append("## ⚠️ Rule violations")
        lines.extend(f"- {v}" for v in violations)
        lines.append("")
    lines.append("## Weekly review notes")
    lines.append("<!-- appended by `gate review`: date, per-active-project verdict (moved / recommit / park / kill) -->")
    lines.append("")
    return "\n".join(lines), violations


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/trbck/workspace")
    ap.add_argument("--wip", type=int, default=3)
    ap.add_argument("--out", default=None, help="default: <root>/PORTFOLIO.md")
    ap.add_argument("--check", action="store_true", help="exit 1 on rule violations")
    args = ap.parse_args()

    root = Path(args.root).expanduser()
    today = dt.date.today()
    rows = collect(root, today)
    if not rows:
        print(f"No <project>/.gate/ directories found under {root}", file=sys.stderr)
        return 2

    content, violations = render(rows, args.wip, today)
    out = Path(args.out) if args.out else root / "PORTFOLIO.md"
    # preserve previously appended review notes
    if out.is_file():
        old = out.read_text(encoding="utf-8", errors="replace")
        marker = "## Weekly review notes"
        if marker in old:
            notes = old.split(marker, 1)[1]
            content = content.split(marker, 1)[0] + marker + notes
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out} ({len(rows)} projects, {len(violations)} violations)")
    for v in violations:
        print(f"  ⚠️  {v}")
    return 1 if (args.check and violations) else 0


if __name__ == "__main__":
    raise SystemExit(main())
