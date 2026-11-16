---
name: record-evidence
description: Record what the learner showed: the closing answer of a teaching session, or an evidence block pasted from a chat or a tool.
---

# Record evidence

Evidence is the learner's own answers, one line each, added through `scripts/learner.py`. The fields are in `docs/learner-record.md` and the grading anchors are in `docs/quiz-protocol.md`.

## Steps

1. **After a teaching session:** take the learner's answer to the closing question. Decide what kind of question it was and the level it showed, by the anchors. Record it: `python3 scripts/learner.py add --topic <id> --kind <kind> --aim <n> --shows <n> --asked "..." --note "..." --by <your model name>`, with `--misstep "..."` if the reasoning went wrong and `--help-given hint` if you had hinted.
2. **For a pasted evidence block:** save the block, from the line `momentos-evidence v1` to the line `end`, to a temporary file outside the repo, and run `python3 scripts/learner.py paste < <that file>`.
3. **If a line is refused,** show the learner the reason the script gave and ask what was meant. Do not rewrite a line by guessing.
4. **Repeat what the script printed:** each topic's level, its next review, and what it needs next.

## Checks

- `python3 scripts/learner.py check` passes.

## Done means

- Only answers the learner gave, or lines in the pasted block, were recorded.
- `learner/evidence.jsonl` was not edited by hand.
- No level was stated that the script did not print.
