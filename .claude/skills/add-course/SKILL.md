---
name: add-course
description: Add a course to the repo, or extend the curriculum of one that is there. Use when a learner wants their own course covered.
---

# Add or extend a course

A curriculum is data: `curricula/<course>.json`. Its format, the weight formula and the rule for targets are in `docs/curricula.md`. Read that first.

## Steps

1. **Register the course.** Open its entry in the official catalog. Add it to `curricula/courses.json`: `id` (the everyday name), `catalog`, `title` (exact), `url`, `checked` (today). Never add a course from memory.
2. **Find the scope.** With local materials: take the outline from the text's chapters or from the current term's homework, then from the exams. With none: use the official course site and the catalog, and cite them under `sources`.
3. **Create `curricula/<slug>.json`** (the id in lowercase with hyphens): `course`, `tier`, `scope_term`, `built_from`, `notes`, `units`.
4. **List the concepts.** For each one, find its topic on the map, or add it with the `add-topic` skill. One idea is one topic across all courses. Give each concept its `topic`, `unit`, `target` and `assessed`.
5. **Record where it is assessed** as identifiers only, such as `FA24 MT1 Q3`. Never the text of a question. If this checkout has `course-survey/`, run `python3 scripts/assessed.py "<course>" --list-tags` once, then `python3 scripts/assessed.py "<course>" <tags>` for each concept, and copy its `assessed`, `target` and `flags`.
6. **Set targets and flags** by the rules in `docs/curricula.md`: 4 where there is exam weight or two current-term items, 3 otherwise; flag `old-exams-only`, `reader-only`, `not-yet-assessed`, `lab-only`.
7. **Build and check:** `python3 scripts/build.py`, then `python3 scripts/check.py`. Read the generated `curricula/<slug>.md`: it must make sense to someone with none of the course's materials.

## Checks

- `python3 scripts/check.py curricula map generated` passes.
- No sentence from any course material is in a tracked file.

## Done means

- The course is in the registry with a catalog URL and the date it was read.
- Every concept points at a topic on the map.
- The generated view reads well on its own.
