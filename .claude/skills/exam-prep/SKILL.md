---
name: exam-prep
description: Prepare the learner for a named exam, with questions weighted by what past exams asked. Use for 'exam prep <course> <exam>'.
---

# Exam preparation

The same loop as a quiz, with the topics chosen by exam weight. The protocol is `docs/quiz-protocol.md`.

## Steps

1. **Read the exam** from what the learner said, for example "EE 105 FINAL". Look in `learner/profile.md` for its date and say how many days are left.
2. **Get the questions:** `python3 scripts/learner.py next --exam "EE 105 FINAL" -n 10`. The script weights each topic by how often exams of that kind examined it, and by how far the learner is below target.
3. **Run the quiz loop** exactly as in the `quiz` skill: fresh questions, a confidence first, no hints, grade by the anchors, record each answer with `python3 scripts/learner.py add`.
4. **Write `transfer` questions in the style of an exam:** several steps, real values, a time limit that you state, and no method named. Never reuse a real exam question.
5. **After the last question,** run `python3 scripts/learner.py report --course "<course>"` and name the three heaviest gaps.
6. **Point to past papers by identifier only.** The generated `curricula/<course>.md` lists where each concept was examined (such as `FA24 MT1 Q3`). Suggest working those, closed-book and timed, on the learner's own copy.

## Checks

- `python3 scripts/learner.py check` passes.

## Done means

- Every answered question is recorded.
- The learner has the three heaviest gaps and the identifiers of past items to practise on.
