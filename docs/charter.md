# Charter

One page. Every model and every fork starts here.

## The goal

To understand every key topic in a set of courses to mastery, and to be able to show it with evidence, not with a
feeling. The tools and the map are stepping stones to that. The repo is shared: the content is common to every
fork, and each learner builds their own record in their own checkout.

## The ladder

A level belongs to one topic for one learner.

| Level | What the learner can do |
|---|---|
| L0 unseen | nothing, or only recognise the name |
| L1 recognise | state the definition or the formula with notes open |
| L2 compute | solve the standard problems by following the procedure |
| L3 picture | explain why it works, sketch it, and predict what changes when a parameter moves |
| L4 use | reach for it on an unfamiliar problem, and know where it breaks |
| L5 teach | derive it from first principles and connect it to other fields |

**Mastery** is L4 with evidence, still holding at a spaced review. The target for a course is L4 on every topic
that carries exam weight and L3 on the rest. L5 is optional.

## What counts as evidence

- Evidence is a graded answer to a question written fresh for the session. It records the date, the kind of
  question, what was asked, what level the answer showed, the confidence stated beforehand, and one line on the
  reasoning. If the reasoning went wrong, it records the first step where it did.
- Only unaided answers raise a level. A self-rating never raises a level past L1.
- L3 needs correct predictions on two different days. L4 needs an unfamiliar exam-style problem solved, and the
  learner naming where the model breaks.
- A level falls back when a review is failed or missed, and comes back with one clean answer.
- A level is never typed in. It is computed from the evidence by `scripts/learner.py`, by rules that are written
  down in [levels.md](levels.md) and tested.

## The rules

1. **Honest records.** The record is the learner's own, and gaming it only fools the learner. A session grades
   what was shown, says so plainly, and never rounds up.
2. **Fresh questions.** Nothing is copied from course materials: not into questions, and not into any tracked file.
3. **Shared content, private records.** No tracked file holds anything about one learner. A learner is a handle.
4. **The picture first.** An explanation that leaves the picture missing has not done its job, however correct.
5. **Nothing unchecked is called checked.** A number marked verified was computed by a script that was run.
6. **Small models can follow it.** Every recurring task has written steps, a checker, and a definition of done.
   When a judgement call comes up twice, it is made once and written down.
7. **One command says whether the repo is sound:** `python3 scripts/check.py`.

The working rules for an agent are in [`AGENTS.md`](../AGENTS.md). The reasons behind the design are in
[decisions/](decisions/), and the learning research behind the method is in [mastery.md](mastery.md).
