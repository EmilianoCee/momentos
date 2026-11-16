---
name: build-tool
description: Build one tool from its plan. Use for 'build the next tool' or 'build <plan id>'.
---

# Build a tool from a plan

The plan is the specification. Build exactly what it says: no extra controls, no missing ones. The rules for every tool are in `docs/tools.md`.

## Steps

1. **Pick the plan.** The one the user named. Otherwise the first row of `plans/BACKLOG.md` whose status is `planned`. Read the whole plan before writing anything.
2. **Read** `docs/tools.md` and `templates/tool-template.html`. For how a finished tool is put together, read `signals/complex-periodicity.html`.
3. **Copy the template** to the plan's `tool` path. Leave the house-style block untouched. Fix the `← map` link: one `../` per folder of depth, and the id of the plan's first topic.
4. **Header.** Fill `Concept`, `Course`, `Play with` and `Should click` from the plan's "Page text". Add `Plan:` with the plan's path. Do not write `Checked:` yet.
5. **Maths first.** Write the `maths` block exactly as the plan's Maths section says: the same names, arguments, units and sign conventions. Copy the plan's check cases into the `check-cases` block unchanged.
6. **Make the cases pass:** `node scripts/test-tools.js <tool path>`. When a case fails, the tool is wrong, not the case. Never change an expected value. If you are sure the plan is wrong, stop and report it.
7. **Draw it.** Build the figures and controls from "Picture" and "Interaction": every control with its range, step and start value, pointer and keyboard both, each quantity in its colour, numbers with units. The main script holds no formulas: it calls `MATHS`.
8. **Words.** Add the title, the lede, the captions, "What should click", "Predict, then try" with each answer in `<details>`, and "Where this shows up" with links to `index.html#<topic id>`, all from the plan.
9. **Register it.** Add the tool's path to `tools` for each of the plan's topics in `map/<folder>.json`. Set the plan's `status` to `built`.
10. **Check:** `python3 scripts/build.py`, then `python3 scripts/check.py`.
11. **Look at it.** Take a headless Chrome screenshot of the `file://` URL in light and in dark, read both, and confirm that the console has no errors. Move each control through `window.TOOL` or by hand.
12. **Write `Checked:`** in the header: the number of check cases that pass, and what you confirmed by eye. Nothing you did not check.
13. **Tick the plan's acceptance checklist,** item by item. Fix what does not hold.

## Checks

- `node scripts/test-tools.js <tool path>` passes.
- `python3 scripts/check.py` passes with no errors.
- The screenshots were looked at, in light and dark.

## Done means

- Every item of the plan's acceptance checklist holds.
- The tool does everything in the plan and nothing that is not in it.
- The plan's status is `built` and the tool is on the map.
