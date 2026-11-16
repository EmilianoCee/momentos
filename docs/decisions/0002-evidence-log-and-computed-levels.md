# 0002. Evidence is an append-only log, and levels are computed from it

Status: accepted, 2026-11-15.

## Context

Sessions with different models will grade answers and record progress. If each model decided a level by its own judgement, two models would disagree and the record would drift. The record must also be plain text, clean in a diff, and safe for a small model to write.

## Options

- **One file per topic, edited by the session.** Readable, but every edit is a chance to break the format or to set a level by feel.
- **A single state file with a level per topic.** Compact, but it throws away the evidence, so a level cannot be checked or recomputed when the rules change.
- **An append-only event log, with levels derived by a script.** Each graded answer is one line. The level is whatever the fixed rules say the lines support.

## Decision

`learner/evidence.jsonl` holds one JSON object per graded answer and is only ever appended to, through `scripts/learner.py add` or `paste`. A session grades a single answer against written anchors and records what the answer showed. `scripts/learner.py` computes the level, the next review and any fall-back. `state.json`, `levels.js` and `progress.md` are generated and never edited.

## Consequences

- Every model applies the rules the same way, because no model applies them: the script does.
- If the rules change, every level is recomputed from the same evidence.
- The only judgement left to a model is grading one answer, which the anchors in `docs/quiz-protocol.md` pin down.
- A chat with no repo access returns the same lines as an evidence block, which the learner pastes in.
- When a topic is renamed or merged, `map/renames.json` carries the old id to the new one, so old evidence still counts.
