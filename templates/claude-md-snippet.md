# Paste into the project's CLAUDE.md / AGENTS.md

```markdown
## Project governance (gate)

This project is governed by `.gate/` (spec: ~/.claude/skills/gate/SKILL.md).

- BEFORE any work: read `.gate/charter.md`, `.gate/ladder.md`, `.gate/todo.md`
  and the last 3 entries of `.gate/log.md`. State the current level and which
  NOW item this session targets.
- Work that serves no open criterion of the current level: stop and ask —
  icebox it or amend the ladder (explicit user confirmation required).
- Charter non-goals are a fence. Do not build past it.
- Ladder checkboxes only flip with fresh EVIDENCE lines (run the command,
  paste the result, date it). Auto-evidence expires after 14 days.
- AFTER work, append to `.gate/log.md`: did / gate delta / todo delta / next.
  A session without a log entry did not happen.
- If `.gate/charter.md` says `status: parked` or `killed`: say so and stop.
```
