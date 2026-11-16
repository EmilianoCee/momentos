# Plans

A plan is the full specification of one tool, written so that a smaller model can build the tool in one session
without opening any course materials and without asking a question. A plan leaves no choice open. Words such as
"etc.", "maybe" or "as appropriate" are defects, and `python3 scripts/check.py plans` rejects them.

A tool may cover a few closely linked concepts. A concept that a picture would not help gets a quiz-only plan
that says why.

## Files

| File | What it is |
|---|---|
| `plans/<id>.md` | one plan. The id is the file name. |
| `plans/checks/<id>.py` | the plan's reference script: it computes the check cases |
| `plans/TEMPLATE.md` | the skeleton to copy |
| `plans/BACKLOG.md` | generated: every plan in priority order, then the concepts that have no plan yet |

"Build the next tool" means the first row of the backlog whose status is `planned`. "Write the next plan" means
the first row whose status is `stub`, or, when there are no stubs, the first concept with no plan.

## The plan block

Every plan starts with a title line and this block:

````
```json plan
{
  "id": "rc-step-response",
  "title": "RC step response",
  "status": "planned",
  "kind": "tool",
  "courses": ["EECS 16B", "EE 105"],
  "topics": ["rc-step-response", "time-constant"],
  "prerequisites": ["kvl", "capacitor-iv"],
  "size": "M",
  "tool": "circuits/rc-step-response.html",
  "checks": "plans/checks/rc-step-response.py"
}
```
````

| Field | Meaning |
|---|---|
| `status` | `stub` (the design is fixed, the detail is not written), `planned` (complete, ready to build), `built` (the tool exists and passes) |
| `kind` | `tool`, or `quiz-only` for a concept with no tool |
| `courses` | course ids from `curricula/courses.json` |
| `topics` | the map topics the tool teaches. The backlog's order comes from their weight in the curricula. |
| `prerequisites` | map topics the learner should already hold at L2 |
| `size` | `S` up to 450 lines of HTML, `M` up to 800, `L` up to 1200 |
| `tool` | the path of the file to build (not for quiz-only) |
| `checks` | the path of the reference script (not for quiz-only, not needed in a stub) |

## Sections

A **stub** has four short sections: `Concept`, `Picture`, `Interaction`, `Misconception`. They fix the design: the
idea in a sentence, what is on the screen, what is dragged and what should click, and the one wrong idea the tool
is aimed at. A quiz-only stub has `Concept`, `Why no tool`, `Misconception`.

A **full tool plan** has these sections, in this order.

1. **Concept.** The idea in one sentence.
2. **Picture.** Everything on the screen: each figure with its `viewBox`, its axes with units and ranges, what is
   drawn in it, and which colour variable (`--c1` to `--c4`) each quantity takes, everywhere it appears.
3. **Interaction.** A table of controls: what kind (a draggable handle, a slider, buttons, a checkbox), the
   quantity and its symbol, the range, the step, the starting value, and the keys that move it. Then what moves
   when each changes, what the reset does, what happens under `prefers-reduced-motion`, and the one thing that
   should click.
4. **Maths.** Every function on `MATHS`: its name and arguments with units, what it returns with units, the
   formula, the sign convention, the range it is valid in, and every approximation with the condition it needs.
5. **Check cases.** A `json check-cases` block, and one line naming the reference script. See below.
6. **Predict, then try.** At least three prompts, each with its answer, word for word as they go on the page.
7. **Misconceptions.** The wrong ideas the tool targets, each with what the learner sees that contradicts it.
8. **Quiz hooks.** For this concept: what an L2, an L3 and an L4 answer looks like, known missteps, and seeds for
   `predict`, `explain`, `limit` and `transfer` questions. The same content goes into `rubrics/<folder>.json`.
9. **Where this shows up.** The map topics to link to, each with its one sentence, and the later courses where
   the idea returns.
10. **Page text.** The exact words: the header comment's `Concept`, `Course`, `Play with` and `Should click`
    lines, the page title, the lede, each figure's caption, and the "What should click" paragraphs.
11. **Acceptance checklist.** The list at the end of `plans/TEMPLATE.md`, unchanged.

A **full quiz-only plan** has `Concept`, `Why no tool`, `Misconceptions`, `Quiz hooks`, `Where this shows up`.

## Check cases and the reference script

The numbers in a plan are never typed from mental arithmetic. Write `plans/checks/<id>.py` first: a
standard-library Python script that implements the maths independently and prints the check cases as one JSON
list. Paste its output into the plan's block. The checker runs the script and fails if any value differs.

```json
{ "fn": "vStep", "args": [1000, 1e-6, 5, 0.001], "expect": 3.160602794142788, "tol": 1e-9, "units": "V",
  "tag": "typical", "note": "R = 1 kΩ, C = 1 µF, a 5 V step, after 1 ms (one time constant): 63.2% of 5 V" }
```

Each case has `fn`, `args`, `expect`, `tol`, `units`, `tag` and `note` (the fields are described in
[tools.md](tools.md)). The note states the inputs with their units in words. A plan must have at least one case
tagged `limit-zero`, one tagged `limit-infinity`, and one tagged `breaks`, which shows a value where the
approximation the tool relies on is visibly wrong, so that the tool can say so. The built tool carries every case.

Derive every formula yourself and check it against a limit. Course notes are for scope and notation, not for
formulas: do not copy an equation into a plan on trust.

## Writing and building

The `write-plan` skill turns a stub or a concept into a full plan. The `build-tool` skill turns a full plan into a
tool. After either: `python3 scripts/build.py`, then `python3 scripts/check.py`.
