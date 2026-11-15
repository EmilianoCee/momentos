# 0001. The learner's record lives in a gitignored folder

Status: accepted, 2026-11-15.

## Context

The repo is shared and forked. The content is common, but each learner's levels and history are their own. A friend who forks must start clean in one step, must never see another learner's levels, and must be able to pull content updates without a conflict. Browser tools cannot write files, so the record is written by a script or by an LLM session.

## Options

- **A tracked folder per learner.** Simple, and history comes free. But a fork carries the owner's levels, a new learner has to delete files to start, and every pull can touch files a learner edits.
- **A personal branch.** Keeps one repository. But the record and the content then live on different branches, so every session needs a merge before it can see both.
- **A separate repository somewhere else.** Private and clean. But a session working in this repo has to find it and be allowed to write outside the working folder.
- **A gitignored folder inside the repo, which is its own git repository.** A fork never contains it, git never touches it on a pull, and the nested repository keeps the history.

## Decision

The record lives in `learner/` at the repo root. The shared `.gitignore` ignores it. `python3 scripts/learner.py init <handle>` creates it from `templates/learner/` and runs `git init` inside it. A learner is known only by a handle.

## Consequences

- A fork starts with no record and nothing to delete. One command starts one.
- History is in a second repository: `git -C learner log`. It is not backed up until the learner adds a private remote.
- A cloud session that clones the repo has no `learner/` folder. It uses the paste block from `scripts/learner.py export` instead.
- Search tools that respect `.gitignore` do not find the record. `AGENTS.md` tells every session where it is.
- One checkout holds one learner.
