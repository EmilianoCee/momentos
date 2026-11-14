# momentos

A personal store of intuition for maths, signals, systems and circuits: small interactive tools, and a
knowledge map (`index.html`) that shows how the topics connect. `README.md` has the full conventions.
This file is the short version for working in the repo.

## When a topic or a tool is added

Do all of these in the same change. The map is only useful if it is never behind the repo.

1. Put the tool in its topic folder. The default is one self-contained `.html` file with a lowercase
   kebab-case name, starting with the comment header (Concept, Course, Play with, Should click, Checked).
2. Add it to the map: the JSON block at the top of `index.html` (`id="map-data"`). Add the topic, or add
   the path to an existing topic's `tools`, and add at least one link with a `why`. A new folder needs
   nothing else, because the circles are drawn from the `folder` paths.
3. Add a row to the tool index in `README.md`.
4. Run `python3 scripts/check-map.py`. It must pass.
5. Check the tool against a hand calculation and write what was checked in the header's `Checked:` line.
   Never write a `Checked:` line for something that was not actually checked.

A topic can go on the map before anything teaches it. Leave out `tools` and it is drawn in italics as planned.

## How tools are built

- Start from `templates/tool-template.html`. Its first `<style>` block is the house style: copy it unchanged.
- One file, no dependencies, no `fetch`, no ES modules. It has to work opened from disk, and in the Claude
  desktop preview, which shows a file as a snapshot with no address. There, relative links cannot be followed
  and storage can throw, so wrap `localStorage` in try/catch.
- Colour is for quantities (`--c1` to `--c4`), one colour per quantity, the same in the figure, the numbers
  and the prose. Controls stay neutral.
- Every tool has: a `← map` link to its topic (`index.html#topic-id`), a light/dark button, a
  "What should click" section, a few "Predict, then try" prompts with the answer folded away, and
  "Where this shows up" links back to map topics.
- Keep the maths in plain functions with no DOM in them, so it can be tested with Node before it is drawn.
- Respect `prefers-reduced-motion`, and do not redraw when nothing is moving.
- Keyboard works wherever the pointer does.

## Writing, in tools and on the map

Plain, short sentences. The picture first, then the formula. Units on every number. `j` for the imaginary
unit. No hype, and nothing that only sounds like an explanation.

## Not tracked

`course-materials/` is local only (lecture notes, problem sets). Read it to check a tool against the course,
but never copy from it into tracked files.

## How to teach me

@prompts/learning-preprompt.md
