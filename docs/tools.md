# Tools

A tool makes one idea visible. The default is a single self-contained `.html` file. The three existing tools are
the quality bar: `maths/linear-algebra/vector-products.html`, `signals/complex-periodicity.html` and
`circuits/kcl-kvl-resistors.html`.

## The rules

- **One file.** No dependencies, no `fetch`, no ES modules, no script or stylesheet loaded from elsewhere. It has
  to work opened from disk, and in a preview that shows one file as a snapshot with no address. There, relative
  links cannot be followed and storage can throw, so every use of `localStorage` sits inside try/catch.
- **Start from `templates/tool-template.html`.** Keep its house-style block, between the two marker comments,
  exactly as it is. A tool's own CSS goes after the end marker.
- **Colour is for quantities:** `--c1` to `--c4`, one colour per quantity, the same in the figure, the numbers and
  the prose. Controls stay neutral.
- **Every tool has:** a `← map` link to its topic (`index.html#topic-id`, with the right number of `../`), a
  light/dark button with `id="theme"`, a "What should click" section, a "Predict, then try" section with at least
  three prompts whose answers are folded away in `<details>`, and a "Where this shows up" section whose links go
  back to map topics.
- **Keyboard works wherever the pointer does.** A draggable handle is focusable and moves with the arrow keys.
- **Respect `prefers-reduced-motion`,** and do not redraw when nothing is moving.
- **Writing:** plain, short sentences. The picture first, then the formula. Units on every number. `j` for the
  imaginary unit. No hype.

## Where a tool lives, and its name

In the folder of its topic on the map (see [map.md](map.md)), with a lowercase kebab-case name that starts with
the concept: `rc-step-response.html`. A tool with several files gets its own subfolder and a short `README.md`.
Other formats are allowed where a browser is the wrong instrument: `.py` (NumPy, Matplotlib), `.ipynb`, `.m`
(MATLAB or Octave) and `.asc` (LTspice). They carry the same header fields as comments, and they go on the map
the same way.

## The header

Every tool starts with this comment block.

```html
<!--
  Concept:      One sentence: the idea this tool makes visible
  Course:       Where it shows up
  Play with:    What to drag or change
  Should click: The thing you should be able to picture afterwards
  Plan:         plans/the-plan-id.md
  Checked:      What was compared with what, with the numbers
-->
```

Leave `Plan:` out if the tool was not built from a plan. Leave `Checked:` out until something has been checked,
and never write it for something that was not. "Should click" is copied into the README's tool index.

## The maths block and its check cases

The maths lives apart from the drawing, in its own script block that defines one global, `MATHS`:

```html
<script id="maths">
var MATHS = (function () {
  "use strict";
  // time constant of an RC circuit, in seconds, from ohms and farads
  function tau(R, C) { return R * C; }
  return { tau: tau };
})();
</script>
<script type="application/json" id="check-cases">
[
  { "fn": "tau", "args": [1000, 1e-6], "expect": 0.001, "tol": 1e-12, "units": "s", "note": "1 kΩ and 1 µF give 1 ms" }
]
</script>
```

The functions are pure: no DOM, no page state, no storage. The main script reads what the learner has set and
calls `MATHS`; it holds no formulas of its own. `node scripts/test-tools.js` runs each maths block in an empty
context, so a function that touches the page fails there.

A check case has:

| Field | What it is |
|---|---|
| `fn` | the name of a function on `MATHS` |
| `args` | its arguments, in order |
| `expect` | a number, string, boolean, null, list or object. In an object, only the keys named are compared. |
| `tol` | how far a number may be off, absolutely or relative to its size. Default 1e-9. |
| `pick` | optional: a dotted path into the result to compare, such as `V.A` |
| `units` | the units of the expected value (`""` for a pure number) |
| `note` | what is being checked, in words, with the inputs and their units |
| `tag` | in a plan: `typical`, `limit-zero`, `limit-infinity`, `breaks`, `sign` or `other` |

`"Infinity"`, `"-Infinity"` and `"NaN"` stand for those numbers. A tool built from a plan carries every check
case of its plan, unchanged.

## Putting it on the map

Add the tool's path to the `tools` list of each topic it teaches, in `map/<folder>.json`. Then:

```bash
python3 scripts/build.py
```

```bash
python3 scripts/check.py
```

The build regenerates the map data and the README's tool index. The check fails if a tool file is not on the map,
if a rule above is broken, if the house style has drifted, or if a check case fails.

## Changing the look

Edit the block in `templates/tool-template.html`, then run `python3 scripts/sync-house-style.py`. If a tool needs
a different layout, override the rule after the end marker. An override of something the house block changes
inside a media query must sit inside the opposite media query.

## Checking a tool by eye

Open it in a browser, in light and dark. From the command line, headless Chrome takes a screenshot of a
`file://` URL. Each tool exposes `window.TOOL` for reading and setting its state from the console.

## An evidence block (optional)

A tool that marks numeric answers itself may offer the learner a block to paste into their record, in the format
of [learner-record.md](learner-record.md): one line per answered problem, with `kind` `compute`, `aim` 2, `shows` 2
for a right answer with no hint, and `by` set to `tool:` followed by the tool's path. A tool never writes files.
