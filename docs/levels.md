# Levels and evidence

A level belongs to one topic for one learner. It is never typed in: `scripts/learner.py` computes it from
`learner/evidence.jsonl`, by the rules on this page. `python3 scripts/learner.py selftest` runs these rules
against nineteen scenarios, so the page and the code cannot drift apart unnoticed.

## The ladder

| Level | What the learner can do |
|---|---|
| L0 unseen | nothing, or only recognise the name |
| L1 recognise | state the definition or the formula with notes open |
| L2 compute | solve the standard problems by following the procedure |
| L3 picture | explain why it works, sketch it, and predict what changes when a parameter moves |
| L4 use | reach for it on an unfamiliar problem, and know where it breaks |
| L5 teach | derive it from first principles and connect it to other fields |

## What each level needs

Only unaided answers count: an answer given after a hint is recorded, but it cannot raise a level. "Showing L3"
means the answer was graded as L3 by the anchors in [quiz-protocol.md](quiz-protocol.md).

| To hold | The record must contain |
|---|---|
| L1 | a self-rating of L1 or more, or any graded answer showing L1 or more |
| L2 | two answers showing L2 or more, or one answer showing L3 or more |
| L3 | L2, plus `predict` answers showing L3 on two different days, plus one `explain`, `sketch`, `limit` or `connect` answer showing L3 |
| L4 | L3, plus one `transfer` answer showing L4, plus one `limit` answer showing L4 (naming where the model breaks) |
| L5 | L4, plus one `derive` answer showing L5, plus one `connect` answer showing L5 |

Three consequences are intended. A self-rating alone stops at L1. L3 cannot be earned in one sitting. And no
number of easy answers adds up to a hard one: each level names the kind of answer it needs.

**Mastered** means L4 is held and an unaided answer showing L4 is dated at least 7 days after L4 was earned.
The target for a course is L4 on the concepts its curriculum marks 4, and L3 on the rest.

## Reviews

From L2 up, a topic has a next review date.

- Earning a new level sets the next review 3 days out.
- A review is passed by an unaided answer, to a question pitched at the held level or above, that shows the held
  level or more. Each pass in a row moves the next review further out: 3, 7, 14, 30, 60, then 120 days.
- A topic is **due** when its review date has arrived.

## Falling back

- **A failed review.** Holding level L, an answer that shows less than the question asked for, and less than L,
  drops the topic one level. The next review is the following day.
- **A missed review.** A review overdue by more than its own interval, and by at least 7 days, drops the topic
  one level. This never takes a topic below L2, and it happens once: the topic then waits, due, at the lower level.
- **Winning it back.** One unaided answer showing the lost level, on a later day, restores it. The evidence that
  earned the level the first time still counts; the clean answer shows it is still true.

## What a quiz asks next

`python3 scripts/learner.py next` chooses the question that would move each topic on:

| Where the topic stands | Next question |
|---|---|
| a level was lost | the kind that wins it back: compute for L2, predict for L3, transfer for L4, derive for L5 |
| L0 or L1 | `compute` at L2 |
| L2 | `predict` at L3 until two days have one, then `explain` (or `sketch`) |
| L3 | `transfer` at L4, then `limit` at L4 |
| L4 | `derive`, then `connect` at L5 |
| due for review | a question at the held level, alternating kinds |

For a course, due reviews come first (most overdue first, relative to their interval), then the topics furthest
below target, heaviest first by the curriculum's weights. Neighbouring questions are drawn from different folders
where possible, so practice is mixed. A topic already answered today is not asked again for growth.

## Calibration

Before each answer the learner states a confidence from 0 to 100. The report compares, in four bands, the mean
confidence with how the answers came out (a pass counts 1, an answer one level short counts 0.5, anything less
counts 0), and gives a Brier score: 0 is perfect, and 0.25 is what saying 50 every time would score. Confidence
that runs ahead of results is the signal to slow down and retrieve more before moving on.

## Missteps

When an answer goes wrong, the session records the first step where the reasoning did. The topic's latest
misstep stays open until an unaided answer passes a question at that level or above. A quiz on the topic probes
an open misstep first.
