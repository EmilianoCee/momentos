# Plan: <the tool's title>

<!-- Copy this file to plans/<id>.md. Replace everything in angle brackets. Delete these comments.
     The format is explained in docs/plans.md. A plan leaves no choice open: write exactly what, never "or similar". -->

```json plan
{
  "id": "<kebab-case-id, the same as the file name>",
  "title": "<the tool's title>",
  "status": "planned",
  "kind": "tool",
  "courses": ["<course id>"],
  "topics": ["<map topic id>"],
  "prerequisites": ["<map topic id>"],
  "size": "M",
  "tool": "<folder>/<id>.html",
  "checks": "plans/checks/<id>.py"
}
```

## Concept

<The idea in one sentence, in plain words.>

## Picture

<Everything on the screen. For each figure: its id, its viewBox (for example 640 by 400), the axes with their
quantities, units and ranges, and each thing drawn in it. Then the readouts beside the figure.>

Colours, the same in the figure, the numbers and the prose:

| Quantity | Symbol | Colour |
|---|---|---|
| <quantity> | <symbol> | `--c1` |

## Interaction

| Control | Kind | Quantity | Range | Step | Start | Keys |
|---|---|---|---|---|---|---|
| <name> | <draggable handle, slider, buttons or checkbox> | <symbol and unit> | <from, to> | <step> | <value> | <which keys move it, and by how much> |

- What moves when each control changes: <one line per control>.
- Reset: <what the reset button restores>.
- Motion: <what animates, and what is shown instead under prefers-reduced-motion>.
- The one thing that should click: <one sentence>.

## Maths

Every function below goes on `MATHS`, with exactly this name and these arguments.

### `<name>(<arg>, <arg>)`

- Arguments: <each argument, its meaning and its unit>.
- Returns: <the value and its unit>.
- Formula: <the formula in plain text>.
- Sign convention: <which direction is positive>.
- Valid for: <the range of each argument>.
- Approximation: <its name, and the condition it needs. Write "none" if exact.>

## Check cases

Computed by `<plans/checks/id.py>`. Copy this block into the tool unchanged.

```json check-cases
[
  { "fn": "<name>", "args": [], "expect": 0, "tol": 1e-9, "units": "<unit>", "tag": "typical", "note": "<the inputs with units, in words, and what the result means>" }
]
```

There is at least one case tagged `limit-zero`, one tagged `limit-infinity`, and one tagged `breaks`.

## Predict, then try

These go on the page word for word. The answer is folded away under "why".

1. <A prediction to make before touching anything.>
   Why: <the answer, in one or two sentences>.
2. <...>
   Why: <...>
3. <...>
   Why: <...>

## Misconceptions

- <A wrong idea, as a learner would say it.> What the tool shows instead: <what they see that contradicts it>.

## Quiz hooks

- L2 looks like: <what a learner who can only compute says or does on this concept>.
- L3 looks like: <what a learner who has the picture says>.
- L4 looks like: <what a learner who can use it and knows where it breaks says>.
- Missteps: <the usual first wrong steps, one per line>.
- Seeds, to be varied and never asked word for word:
  - predict: <a "what changes if" set-up>
  - explain: <a "why" to explain>
  - limit: <a parameter to push, and what fails first>
  - transfer: <the outline of an unfamiliar problem that needs this idea>

## Where this shows up

- `<map topic id>`: <one sentence on what carries over, as it will appear on the page>.
- Later: <course id>: <one line on how the idea comes back>.

## Page text

- Header `Concept:` <one sentence>
- Header `Course:` <where it shows up>
- Header `Play with:` <what to drag or change>
- Header `Should click:` <what the learner should be able to picture afterwards>
- Title: <the page's h1>
- Lede: <two or three plain sentences: the picture, not the formula>
- Caption of <figure id>: <what can be dragged, and which keys do the same>
- What should click: <the paragraphs of that section, each starting with a bold name for the idea>

## Acceptance checklist

- [ ] One `.html` file at the plan's `tool` path, started from `templates/tool-template.html`, with no dependencies, no `fetch` and no modules.
- [ ] The house-style block is unchanged, and the tool's own CSS comes after its end marker.
- [ ] The header comment has `Concept`, `Course`, `Play with`, `Should click` and `Plan`. `Checked` is written last, and only for what was checked.
- [ ] `MATHS` has every function in the Maths section, with those names and arguments, and nothing in the maths block touches the page.
- [ ] The check-cases block is the plan's, unchanged, and `node scripts/test-tools.js` passes for this tool.
- [ ] Every control in the Interaction table exists, with its range, step and start value, and works from the keyboard.
- [ ] Each quantity has its colour from the table, the same in the figure, the numbers and the prose. Controls are neutral.
- [ ] Every number on the page has its unit. `j` is the imaginary unit.
- [ ] The page has a `← map` link to its topic, a light/dark button, "What should click", "Predict, then try" with the prompts above, and "Where this shows up" with links to the map.
- [ ] It respects `prefers-reduced-motion` and does not redraw when nothing is moving.
- [ ] The tool's path is in the `tools` of each of the plan's topics in `map/`, and the plan's status is `built`.
- [ ] `python3 scripts/build.py` and `python3 scripts/check.py` pass, and the page was looked at in a browser in light and dark.
