# 0003. What evidence each level needs, and when a level falls back

Status: accepted, 2026-11-15.

## Context

The ladder runs from L0 (unseen) to L5 (teach). Mastery means L4 with evidence, still holding at a spaced review. A self-rating says little, a single good day says little more, and understanding fades when it is not used.

## Options

- **Any correct answer at a level earns the level.** Fast, but one lucky answer or one good session passes for understanding.
- **A points score per topic.** Smooth, but a number hides what was shown, and it lets many easy answers stand in for one hard one.
- **Named requirements per level, spread over days, with a fall-back on a failed or missed review.** Slower to earn, but each level means a specific thing was seen.

## Decision

Only unaided answers count. L1: a self-rating, or any graded answer. L2: two answers showing L2, or one showing L3. L3: correct predictions on new what-changes-if prompts on two different days, plus one explain, sketch, limit or connection answer. L4: L3, plus an unfamiliar exam-style problem solved, plus naming where the model breaks. L5: L4, plus a derivation and a connection to another field. Mastered: L4, and an L4 answer at least 7 days after L4 was earned. A failed review drops one level until one clean answer on a later day. Reviews come 3, 7, 14, 30, 60 and 120 days apart. A review overdue by more than its own interval, and by at least 7 days, costs one level, never below L2.

## Consequences

- A self-rating never raises a level past L1.
- L3 cannot be earned in one sitting, which builds spacing into the definition.
- One slip costs one level and one clean answer wins it back, so the record tracks the truth without punishing noise.
- The rules are code: `scripts/learner.py selftest` runs 19 scenarios, and `scripts/check.py` runs the self-test.
