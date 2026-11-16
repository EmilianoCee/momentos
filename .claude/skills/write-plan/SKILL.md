---
name: write-plan
description: Write the full plan for one tool, or expand a stub into one. Use for 'write the next plan' or 'write a plan for <concept>'.
---

# Write a plan

A plan lets a smaller model build a tool in one session with no other source. The format is in `docs/plans.md` and the skeleton is `plans/TEMPLATE.md`. Read both before you start.

## Steps

1. **Pick the plan.** The one the user named. Otherwise the first row of `plans/BACKLOG.md` whose status is `stub`. Otherwise the first concept under "Concepts with no plan yet".
2. **Read:** `docs/plans.md`, `plans/TEMPLATE.md`, `docs/tools.md`, the topics' entries in `map/`, and one plan in `plans/` whose status is `planned` or `built`, as a model of the level of detail.
3. **Tool or quiz-only?** A picture does not help when the idea is a definition, a classification or a proof technique. Then write a quiz-only plan and say why in "Why no tool".
4. **Fix the design:** what is on the screen, what is dragged, the one thing that should click, and the misconceptions it is aimed at. If this checkout has `course-survey/`, use it for scope, notation and typical values only. Copy nothing from it.
5. **Write the reference script first:** `plans/checks/<id>.py`, standard library only. Implement each function of the tool independently. Derive every formula yourself and test it against a limit you can reason out. Print the check cases as one JSON list: typical cases, a `limit-zero`, a `limit-infinity`, a `breaks` case where the tool's approximation is visibly wrong, and a `sign` case where a sign convention matters. Run it.
6. **Write the plan** from the template, every section. Paste the script's output into the `json check-cases` block unchanged. Write the page's words in full in "Page text" and "Predict, then try".
7. **Rubric.** Put the plan's quiz hooks into `rubrics/<folder>.json` for each topic: `L1` to `L4`, `missteps`, `seeds`.
8. **Set `status` to `planned`.** Then `python3 scripts/build.py` and `python3 scripts/check.py`.
9. **Read it as the builder.** Go through the plan once as someone who has only the plan and the template. Wherever you would have to choose or guess, rewrite the sentence so that there is nothing to choose.

## Checks

- `python3 scripts/check.py plans rubrics generated` passes.
- The reference script reproduces every check case.
- No sentence in the plan leaves a choice open.

## Done means

- The plan is listed as `planned` in `plans/BACKLOG.md`.
- A builder needs nothing but the plan, the template and `docs/tools.md`.
- The topics' rubric entries exist.
