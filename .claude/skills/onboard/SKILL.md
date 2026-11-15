---
name: onboard
description: Start a learner's record and place them on the ladder from evidence. Use for 'onboard me', or when there is no learner/ folder.
---

# Onboard a new learner

A record starts empty, and levels start at L0 because there is no evidence yet. Onboarding collects the first evidence. The record's files are described in `docs/learner-record.md`.

## Steps

1. **Start the record,** if `learner/` does not exist. Ask for a handle (not a name), then run `python3 scripts/learner.py init <handle>`.
2. **Fill the profile.** In one message, ask: which courses in `curricula/courses.json` they are taking now, have done, or take next; any exams and their dates; and a few lines about what they are studying, what they work with, and what they want from an explanation. Write the answers into `learner/profile.md`: the JSON block and "About me". Run `python3 scripts/learner.py check`.
3. **Placement.** For each course marked `now`, run `python3 scripts/learner.py next --course "<course>" -n 10`. This returns the ten heaviest topics.
4. **Ask one `predict` question on each of those topics, pitched at L3,** whatever kind the list says. A prediction places a learner best: an answer showing L3 puts the topic at L2 at once and starts L3, and an answer showing L2 counts toward L2. Follow the loop in `docs/quiz-protocol.md`: a confidence first, no hints, grade by the anchors.
5. **Record each answer** with `python3 scripts/learner.py add --kind predict --aim 3 ...`.
6. **Show the result:** `python3 scripts/learner.py report`. Explain in two lines that no topic can pass L2 on the first day, because L3 needs correct predictions on two different days.
7. **Say what comes next:** tomorrow, `quiz me <course>`.

## Checks

- `python3 scripts/learner.py check` passes.
- `learner/profile.md` has a handle and no name or email address.

## Done means

- The record exists and is valid.
- Every `now` course has first evidence on its heaviest topics.
- No level came from a self-rating.
