# 0006. AGENTS.md is the single source of rules for every model

Status: accepted, 2026-11-15.

## Context

Smaller models will do most of the future work in short sessions, and some of them will not be Claude. Rules written in two places drift apart.

## Options

- **Keep everything in CLAUDE.md.** Only Claude Code reads it.
- **Maintain CLAUDE.md and AGENTS.md side by side.** Two copies of every rule.
- **Put the rules in AGENTS.md and have CLAUDE.md import it.** One copy. Claude Code follows the import; other agents read AGENTS.md directly.

## Decision

`AGENTS.md` holds a short router (if you are doing X, read Y) and the hard rules. `CLAUDE.md` is one import line plus what only Claude Code needs. Each recurring procedure is a skill under `.claude/skills/`, written for a model that has read nothing else, with its steps, its checks and what done looks like. Detailed conventions live in `docs/`.

## Consequences

- `scripts/check.py skills` fails if `CLAUDE.md` stops importing `AGENTS.md`, if a skill lacks its sections, or if an instruction file names a path that does not exist.
- An agent that does not load skills can still follow them: they are plain markdown files.
