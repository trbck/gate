# gate — quality gates, todo discipline & portfolio management for LLM-assisted projects

**The problem:** after months of vibe coding, every project is 80% done and 0%
productive. Not because the code is bad — because (a) "done" was never defined
observably at the *project* level, (b) LLMs make adding features cheaper than
finishing, so scope grows sideways, (c) attention is split across 20+ projects
with no forcing function to ship, charge, or kill anything.

**The fix:** gate is a pure-markdown, LLM-executable governance layer:

| Mechanism | File | Kills which failure |
|---|---|---|
| Maturity ladder L0–L5, evidence-gated checkboxes | `.gate/ladder.md` | "done" undefined; progress theater |
| Charter with north star, kill criteria, non-goals | `.gate/charter.md` | scope creep; zombie projects |
| Todo rules (NOW ≤5, every item → gate criterion) | `.gate/todo.md` | working on whatever is fun |
| Session protocol + append-only log with *gate delta* | `.gate/log.md` | sessions that feel productive but move nothing |
| Audit → scorecard (drift, stale evidence, stuck) | `.gate/scorecard.md` | invisible quality debt |
| Portfolio: WIP limit 3, weekly recommit/park/kill | `PORTFOLIO.md` | 25 half-projects instead of 1 shipped one |

Full logic: [SKILL.md](SKILL.md). Ladder levels in one line each:
**L0** worth pursuing → **L1** core loop works once → **L2** I use it → **L3**
survives a stranger → **L4** others use it / 30-day habit → **L5** revenue /
load-bearing in my life.

The load-bearing idea: **L4/L5 criteria are deliberately non-code** (post the
Reddit thread, email 5 users, turn on Stripe live mode). The ladder keeps
shoving those in front of you as `[human-action]` items instead of letting the
LLM do another refactor.

## Relationship to boil

boil = inner loop ("build this feature until verified").
gate = outer loop ("is the project converging, and should I even work on it?").
Each open ladder criterion is a ready-made boil goal:
`boil "<criterion>" till "<its evidence command> is green"`, and a green boil
run yields a paste-ready EVIDENCE line. boil stories are the preferred
auto-evidence for L2/L3 criteria. boil's human-action tickets mirror into
`.gate/todo.md`.

## Install

```bash
# as a Claude Code skill (recommended)
git clone git@github.com:trbck/gate.git ~/.claude/skills/gate
# slash command
mkdir -p ~/.claude/commands && cp ~/.claude/skills/gate/commands/gate.md ~/.claude/commands/gate.md
```

Update an existing install: `git -C ~/.claude/skills/gate pull`.

Or vendor it into boil: copy `SKILL.md` → `boil/references/gate-spec.md`,
`commands/gate.md` → `boil/commands/`, `scripts/gate-portfolio.py` →
`boil/scripts/`, and add a "gate integration" paragraph to boil's SKILL.md.

## Usage

```
/gate init          # in a project: interview → charter, ladder, verified level, todos
/gate status        # where am I, what's the one next action (read-only)
/gate session       # start the session protocol (any coding session)
/gate audit         # re-verify evidence, drift check, regenerate scorecard
/gate review        # weekly portfolio review: moved / recommit / park / kill
python3 scripts/gate-portfolio.py            # regenerate workspace PORTFOLIO.md
python3 scripts/gate-portfolio.py --check    # exit 1 on rule violations (cron/CI)
```

Automate the weekly review: `/schedule` a cloud agent (or `/loop`) that runs
`/gate review` every Monday and pushes the violations via Pushover/susi.

## Rollout for an existing 20-project workspace (do this once)

1. **Pick 3.** Choose the 3 projects you'd bet on this quarter.
2. `/gate init` the 3 active projects (~20 min each). Expect the honest answer
   to be L1–L2 with holes. That's the point — now the holes are a checklist.
   Init handles the portfolio automatically: it sets the project active, parks
   the projects it displaces (stub charters with a re-entry condition), runs
   `gate-portfolio.py --check`, and shows you the fresh — uncomfortable —
   `PORTFOLIO.md`.
3. From then on: every session starts with `/gate session`, every Monday
   `/gate review`. The system does the rest by construction.

## Layout

```
gate/
├── SKILL.md                     # the full spec — loaded when the skill triggers
├── commands/gate.md             # /gate init|status|session|audit|review
├── templates/                   # charter, ladder, todo, log, scorecard, CLAUDE.md snippet
├── examples/                    # fully filled charter + ladder showing evidence discipline
└── scripts/gate-portfolio.py    # PORTFOLIO.md generator + rule checker (stdlib only)
```

## Anti-gaming clause

The system only works if evidence is real. An LLM (or you at 1am) ticking a box
without running the command is the same lie as before, in nicer clothes. Hence:
audits *re-run* auto evidence, human evidence has an expiry, and the weekly
review asks only one question — did the score move — which cannot be vibed.

## License

[MIT](LICENSE) — © 2026 trbck
