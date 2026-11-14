# Handoff: where the first build session stopped

The session ran out of usage partway through. This file is everything needed to pick it up.
Delete it once the list under "Not done" is empty.

## Done and checked in a browser

| File | State |
|---|---|
| `index.html` | The knowledge map. One self-contained file. Checked in light and dark, wide and narrow: layout, selecting a topic, the detail panel, search, zoom, folder zoom. |
| `maths/linear-algebra/vector-products.html` | Finished. Numbers checked by hand (see the `Checked:` line in its header). |
| `signals/complex-periodicity.html` | Works, and its maths is checked (periods, aliasing, the one-radian case). A few cosmetic items are left, listed below. |

Nothing has been committed.

## Not done

1. **`circuits/kcl-kvl-resistors.html` does not exist yet.** The map already lists it as the tool for
   Ohm's law, KCL, KVL, dividers and nodal analysis, so those five "open the tool" links are dead until it is built.
   Plan: resistor-only practice problems with a check button and stepwise hints, plus an explore mode with sliders.
   A small modified-nodal-analysis solver (resistors, voltage sources, current sources; units V, kΩ, mA) drives
   everything. Circuits: one loop with 2 or 3 resistors (KVL), one node pair with 2 or 3 resistors (KCL),
   a T network, and a two-source circuit. Show current as dots moving along the wires at a rate proportional
   to the current, a KCL "in equals out" bar for a node, and a KVL "height around the loop" chart.
2. **`prompts/learning-preprompt.md`** (the LLM pre-prompt). Plan: a learner profile (third-year UC Berkeley EECS,
   EE side, heading to analog), then a per-topic level ladder asked before any new concept
   (L0 unseen, L1 recognise, L2 compute, L3 picture, L4 use, L5 teach), and the level picks the mode:
   L0–L1 pedagogy (the LLM leads, worked examples), L2–L3 andragogy (problem first, hints before answers),
   L4–L5 heutagogy (the learner leads, the LLM challenges). Then a fixed shape for explanations
   (essence, picture, formalism, worked numbers with units, limits, connections, one check question)
   and a "map it" command that outputs a topic entry in the map's JSON format.
3. **`scripts/check-map.py`**: read the JSON block in `index.html` and fail if a tool path does not exist,
   a link names an unknown topic, an id repeats, or a tool file in the repo is not registered in the map.
4. **`templates/tool-template.html`**: the shared house-style block (the first `<style>` section in either
   finished tool) plus an empty stage, so new tools start consistent.
5. **`CLAUDE.md`**: the rule "every new topic or tool gets a map entry and a README row, then run the checker",
   the house style, and an import of the pre-prompt.
6. **`README.md`** still describes the repo before this session: update the folder tree, fill in the tool index,
   add a section on the map and on the pre-prompt. Add one-line stubs to `systems/` and `unspecified/`
   so git keeps those folders.
7. **Cosmetic items in `signals/complex-periodicity.html`**: the figure has spare space at the bottom
   (viewBox height 420, about 376 is enough), the "−1" label sits close to the left edge, it redraws every frame
   even when paused, and the one-radian walk should speed up after about 40 steps.

## Decisions already made (keep these)

- **The map is one file with its data inside.** The data is the JSON block near the top of `index.html`
  (`<script type="application/json" id="map-data">`). Add a topic by adding an object to `topics` and
  at least one entry to `links`. Folders become circles from each topic's `folder` path.
- **Everything is a single self-contained HTML file**: no fetch, no modules, no external files.
  The Claude desktop app's preview pane only renders self-contained files, and it cannot follow links
  between pages. To click from the map into a tool, open `index.html` in a normal browser.
- **House style**: paper and ink colours through `light-dark()`, a serif for prose and topic names,
  monospace for numbers and labels, colour kept for quantities (blue, orange, teal, purple). Every page has a
  light/dark button.

## Things I assumed that you should check

- I read "each topic title is encapsulated in a circle representing the folder it lies in" as: one circle per
  folder, with the topic names inside it.
- Nine topics on the map are **planned** (italic, no tool): determinant, linear systems, eigenvectors,
  Fourier series, frequency response, phasors & impedance, AC power, work, magnetic force. I added them
  because they are the bridges between the three tools. Delete any you do not want.
- The course tags on topics (EECS 16A, 16B, EE 120, Physics 7A/7B, Math 53) are my best guess, not checked
  against a syllabus.

## To continue

Open this repo in Claude Code and say: "Read HANDOFF.md and finish the Not done list, starting with the circuits tool."
