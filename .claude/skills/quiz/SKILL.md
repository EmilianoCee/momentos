---
name: quiz
description: Quiz the learner and record the evidence. Use for 'quiz me <course>', 'quiz me <topic>' and 'review'.
---

# Run a quiz

You ask, the learner answers, you grade against written anchors, and a script records it and works out the level. You never decide a level. The protocol is `docs/quiz-protocol.md`: read all of it before the first question.

## Steps

1. **Is there a record?** If `learner/profile.md` does not exist, say so, offer the `onboard` skill, and stop.
2. **Get the questions.** A course: `python3 scripts/learner.py next --course "EE 120"`. A topic: `python3 scripts/learner.py next --topic <id>`. "Review": `python3 scripts/learner.py next --due`. If the list is empty, say that nothing is due, and offer a course or a topic.
3. **Ask them in the order given,** one at a time. Each item gives the topic, the `kind` of question and the level it is pitched at. Do not reorder, skip or re-pitch.
4. **Write each question fresh:** new numbers with units, a set-up the learner has not seen, never from course materials, never the topic's `check` word for word. If the item has `open_misstep`, write the question so that the same wrong step gives a wrong answer.
5. **Ask for a confidence from 0 to 100 with the question.** Then wait. No hint before an answer.
6. **Grade** against the anchors in `docs/quiz-protocol.md` and the item's `rubric`, if it has one. Between two levels, record the lower.
7. **Say three things, briefly:** the level the answer showed and why; the first step where the reasoning went wrong, if it did; the picture that makes the right answer obvious.
8. **Record it before the next question:** `python3 scripts/learner.py add --topic <id> --kind <kind> --aim <n> --shows <n> --confidence <n> --asked "..." --note "..." --by <your model name>`. Add `--misstep "..."` when the reasoning went wrong, and `--help-given hint` when a hint came first.
9. **At the end,** repeat what the script printed for each topic (its level and next review). For a course, run `python3 scripts/learner.py report --course "<course>"` and give the three lines that matter.

## Checks

- `python3 scripts/learner.py check` passes.
- Every answered question has exactly one line of evidence.

## Done means

- No level was stated that the script did not print.
- No question came from course materials.
- The learner knows what is due next, and when.
