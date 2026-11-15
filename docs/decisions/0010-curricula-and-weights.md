# 0010. Curricula are data, and exam weight is computed from where a concept is assessed

Status: accepted, 2026-11-15.

## Context

For each course the repo needs the concepts in scope, where each is assessed, a priority order and a mastery target. Quizzes and exam preparation need those as numbers. The course materials themselves cannot be shared.

## Options

- **Prose outlines.** Readable, but a script cannot order a quiz from prose.
- **Hand-entered weights.** Usable, but arbitrary, and stale after every new exam.
- **Concepts with the identifiers of the items that assess them, and a fixed formula.** Reproducible, and the identifiers mean something to anyone who has the materials.

## Decision

`curricula/<course>.json` lists units and concepts. A concept names its map topic, its target level and the items that assess it, written like `FA24 MT1 Q3`. Weight: an exam item counts 1, halved for every 4 years of age; a homework, discussion, lab or practice item counts 0.5 in the scope term and 0.25, aged the same way, before it. The target is L4 where a concept carries exam weight or is assessed twice in the current term, and L3 otherwise. A readable view, `curricula/<course>.md`, is generated.

## Consequences

- No problem text is stored, only identifiers.
- A topic's list of courses on the map is derived from the curricula.
- Exam preparation re-weights by the kind of exam being prepared for.
