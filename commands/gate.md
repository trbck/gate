---
description: "Project quality gates & portfolio: /gate init|status|audit|review|session [project]"
---

Load and follow the `gate` skill (SKILL.md in the gate skill directory).
Argument: `$ARGUMENTS` — `<subcommand> [project-dir]`; default project = cwd.

- **init** — bootstrap `.gate/` for the project: read its docs/history, run the
  charter interview (≤10 questions), draft the ladder, verify the true current
  level with real evidence, seed todos, add the CLAUDE.md snippet, log, audit.
  Then AUTOMATICALLY: set `status: active`, run `scripts/gate-portfolio.py
  --check`, resolve any WIP breach by parking the displaced project (stub
  charter if needed), and show the fresh portfolio table. Init isn't done
  until the check passes or violations are explicitly acknowledged.
- **status** — read `.gate/` + last log entries; report level, score, open
  criteria of the current gate, NOW list, and the single next action. Read-only.
- **audit** — full audit per SKILL.md: re-verify auto evidence, drift check vs
  git log, staleness, todo rules; regenerate `scorecard.md`; run
  `scripts/gate-portfolio.py`.
- **review** — weekly portfolio review: run gate-portfolio.py, then for each
  active project apply the moved/recommit/park/kill decision protocol; append
  the verdicts to PORTFOLIO.md review notes. Surface kill-by breaches bluntly.
- **session** — start the session protocol (read state, bind work to a NOW
  item) and remind yourself to write the log entry at the end.

No subcommand → `status`.
