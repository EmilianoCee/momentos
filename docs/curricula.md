# Curricula

A curriculum says, for one course: which concepts are in scope, where each is assessed, in what order they
matter, and the mastery target for each. Quizzes, exam preparation and the backlog of tools are all ordered from
it. The source is `curricula/<course>.json`. `python3 scripts/build.py` generates the readable
`curricula/<course>.md` beside it. Never edit the generated file.

A curriculum must make sense to someone who has none of the course's materials. It stores identifiers such as
`FA24 MT1 Q3`, never the text of a question.

## The course registry

`curricula/courses.json` lists every course id used anywhere in the repo.

```json
{ "id": "EE 120", "catalog": "EL ENG 120", "title": "Signals and Systems",
  "url": "https://undergraduate.catalog.berkeley.edu/courses/1062941", "checked": "2026-11-15" }
```

`id` is the name in everyday use. `catalog` and `title` are the current catalog entry, `url` is where it was
read, and `checked` is the date. Course numbers change, so an id is only added after its catalog entry has been
opened. A course mentioned only in a topic's `later` note still needs an entry here.

## A curriculum file

`curricula/ee-120.json`: the file name is the id in lowercase with hyphens.

```json
{
  "course": "EE 120",
  "tier": 1,
  "scope_term": "FA26",
  "built_from": ["Homework 1 to 10 and discussions 1 to 11 of Fall 2026", "40 past exams, 2015 to 2026"],
  "notes": ["The course writes i for the imaginary unit. This repo writes j."],
  "sources": [{ "title": "Catalog entry", "url": "https://...", "accessed": "2026-11-15" }],
  "outline": ["Weeks 1 to 2: complex numbers and exponentials"],
  "units": [{ "id": "u1", "title": "Complex exponentials and periodicity" }],
  "concepts": [
    { "topic": "periodicity", "unit": "u1", "target": 4,
      "assessed": ["FA26 HW3 Q1", "FA24 MT1 Q2", "SP19 MT1 Q4"], "flags": [] }
  ]
}
```

| Field | Meaning |
|---|---|
| `tier` | 1: full curriculum, coverage and a plan for every key concept. 2: the same, after tier 1. 3: curriculum and map topics, plans only where higher tiers lean on them. 4: map topics and a researched outline, no plans. |
| `scope_term` | the term whose materials define what is in scope, such as `FA26` |
| `built_from` | what the curriculum was built from, in words |
| `notes` | anything a reader must know: notation that differs, a course that changed |
| `sources` | for researched outlines: title, URL and the date it was read |
| `outline` | optional: the course in teaching order, a line per week or unit |
| `units` | the course's parts, in order, each with an `id` and a `title` |
| `concepts` | one entry per concept (below) |

A concept:

| Field | Meaning |
|---|---|
| `topic` | the id of its topic on the map. One concept is one topic. |
| `unit` | the unit it belongs to |
| `target` | the level to reach: 4 or 3 (5 only by choice) |
| `assessed` | where it is assessed: term, assessment, item. `FA24 MT1 Q3`, `FA26 HW4 Q2`, `FA26 DIS3 Q1`, `FA25 LAB4a 3.1`, `FA26 MTP A3`, or just `FA25 FINAL` when the item is not known. |
| `flags` | `old-exams-only` (examined only before the course's present form), `reader-only` (in the text, never assessed), `not-yet-assessed` (in scope, no item yet this term), `lab-only` |

## Weight

How heavily a concept is assessed is computed, not entered (`concept_weight` in `scripts/momentos.py`):

- an exam item counts 1, halved for every 4 years between it and the scope term;
- a homework, discussion, lab or practice item counts 0.5 in the scope term, and 0.25, aged the same way, in any
  other term.

The generated view shows each concept's weight and its exam-only weight, and lists the concepts heaviest first.
For exam preparation the weight is recomputed from the exams of the kind being prepared for: a final counts every
exam, a midterm counts midterms of that number.

## Target

Set `target` to 4 when the concept has any exam weight, or at least two items in the scope term. Set it to 3
otherwise. A concept flagged `old-exams-only` keeps 4 when the course's text treats it as core, and drops to 3
when it has left the course.

## Scope

The scope term's own materials decide what is in scope. Older exams show the style of question and add weight.
A concept that appears only in old exams, or only in the text, is kept and flagged, so that the gap is visible.

## Adding or extending a course

Follow the `add-course` skill. In short: open the catalog entry and add the course to the registry; list the
units; for each concept, find or add its map topic (one idea is one topic across all courses); record where it is
assessed (`python3 scripts/assessed.py` reads the local survey tables in `course-survey/` and prints the identifiers, the weight, the target and the flags); set the target; run `python3 scripts/build.py` and `python3 scripts/check.py`. To add courses to your own fork, paste `prompts/add-my-courses.md` into an agent. For a course with no
local materials, build the outline from the official course site and the catalog, and cite them in `sources`.
