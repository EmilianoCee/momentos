# The learner's record

Each learner keeps their own record in `learner/`, at the root of their checkout. The shared repo ignores that
folder, so a fork never carries anyone's levels, and pulling updates never touches it. It is its own git
repository, which is where its history is kept. Why it works this way is in
[decisions/0001](decisions/0001-learner-record-in-a-gitignored-folder.md) and
[0002](decisions/0002-evidence-log-and-computed-levels.md).

## Start one

```bash
python3 scripts/learner.py init your-handle
```

A handle is lowercase letters, digits and hyphens. No names, no emails. Then fill in `learner/profile.md`.

## The files

| File | Written by | What it is |
|---|---|---|
| `profile.md` | the learner | a small JSON block, then free prose about how they learn |
| `evidence.jsonl` | `scripts/learner.py` | one graded answer per line, oldest first, append only. The record of truth. |
| `state.json` | generated | every topic's level, next review and what is missing for the next level |
| `levels.js` | generated | the same, for the map to colour topics by level |
| `progress.md` | generated | the "where am I" report |
| `notes/` | the learner | anything else. Nothing reads it. |

Never edit a generated file, and never edit `evidence.jsonl` by hand except to append a pasted block.

## profile.md

```json
{
  "schema": 1,
  "handle": "your-handle",
  "started": "2026-11-15",
  "courses": { "EE 120": "now", "Math 53": "done" },
  "exams": [{ "course": "EE 120", "name": "FINAL", "date": "2026-12-17" }],
  "session_size": 8
}
```

- `courses`: ids from `curricula/courses.json`, each `now`, `done` or `next`. Reports cover these, `now` first.
- `exams`: what is being prepared for. `name` is `FINAL`, `MT1`, `MT2` or `MT3`.
- `session_size`: how many questions a quiz session asks.

The prose under the block ("About me") is read by every teaching session: what the learner is studying, what they
have done, what they work with, and what they want from an explanation.

## One line of evidence

```json
{"date": "2026-11-16", "topic": "convolution", "kind": "predict", "aim": 3, "shows": 3, "help": "none", "confidence": 70, "asked": "The input pulse is made twice as wide. What happens to the width and the peak of the output?", "note": "Got the width by sliding one pulse across the other; said the peak doubles, then corrected it.", "misstep": null, "by": "claude-code"}
```

| Field | Values | Meaning |
|---|---|---|
| `date` | `YYYY-MM-DD` | the day the answer was given |
| `topic` | a topic id on the map | one event is about one topic |
| `kind` | `self`, `recall`, `compute`, `predict`, `explain`, `sketch`, `limit`, `connect`, `transfer`, `derive` | the kind of question ([quiz-protocol.md](quiz-protocol.md)) |
| `aim` | 1 to 5 | the level the question was pitched at. Fixed by the kind: recall 1, compute 2, predict 3, explain 3, sketch 3, limit 3 or 4, connect 3 or 5, transfer 4, derive 5. |
| `shows` | 0 to 5 | the level the answer showed, by the anchors. For `self`, the level claimed. |
| `help` | `none`, `hint`, `worked` | what help came before the answer. Only `none` can raise a level. |
| `confidence` | 0 to 100, or null | how sure the learner said they were, before answering |
| `asked` | one line | what was asked, in the session's own words |
| `note` | one line | the reasoning, not just right or wrong |
| `misstep` | one line, or null | the first step where the reasoning went wrong |
| `by` | text | who graded: `claude-code`, `chat`, `tool:<path>` |
| `session` | text, optional | groups the answers of one sitting |

A self-rating is `{"date": ..., "topic": ..., "kind": "self", "shows": 3}`. It never counts for more than L1.

## Adding evidence

From a session that can run commands, one call per answer:

```bash
python3 scripts/learner.py add --topic convolution --kind predict --aim 3 --shows 3 --confidence 70 --asked "..." --note "..."
```

Add `--misstep "..."` when the reasoning went wrong, `--help-given hint` when a hint came first, and `--by` to
say who graded. The script refuses anything malformed, appends the line, rebuilds the generated files, commits
inside `learner/`, and prints the topic's level and what it needs next.

From a chat or a tool, the evidence arrives as a block:

```
momentos-evidence v1
{"date": "2026-11-16", "topic": "convolution", "kind": "predict", "aim": 3, "shows": 3, "confidence": 70, "asked": "...", "note": "..."}
{"date": "2026-11-16", "topic": "kcl", "kind": "compute", "aim": 2, "shows": 2, "asked": "...", "note": "..."}
end
```

```bash
python3 scripts/learner.py paste < block.txt
```

Every line is checked before any is recorded.

## Reading it back

| Command | Prints |
|---|---|
| `python3 scripts/learner.py report` | progress in each course against its target, calibration, open missteps. Add `--course "EE 120"` for one. |
| `python3 scripts/learner.py show convolution` | one topic: its level, what it needs next, and every answer so far |
| `python3 scripts/learner.py next --course "EE 120"` | the questions a quiz should ask next, as JSON. Also `--topic`, `--due`, `--exam "EE 105 FINAL"`, and `-n`. |
| `python3 scripts/learner.py export --course "EE 120"` | everything a chat with no repo access needs, in one block |
| `python3 scripts/learner.py check` | whether the record is valid |

## Backing it up

`learner/` is a git repository with no remote. Give it a private one:

```bash
git -C learner remote add origin <the address of a private repository>
```

Never add `learner/` to the shared repo.
