---
name: add-topic
description: Add a topic or a link to the knowledge map. Use when a new idea, a new tool or a course concept has to appear on the map.
---

# Add a topic to the map

The map's source is `map/<folder>.json`. The block inside `index.html` is generated from it. The format and the rule for choosing a folder are in `docs/map.md`. Read that first.

## Steps

1. **Look before you add.** Search the map for the idea: `grep -ril "<a word of the idea>" map/`. One idea is one topic across all courses. If it exists, reuse its id: add a link, or add it to a curriculum, and stop here.
2. **Choose the folder** with the table in `docs/map.md`: file the topic under what the idea is about, never under the course that teaches it. The file is `map/<folder>.json`. For a new folder, create the file with `{"topics": [], "links": []}`.
3. **Write the topic:** `id` (lowercase words joined by hyphens, unique, never an id listed in `map/renames.json`), `title` (the words on the map: three or four at most), `essence` (one or two sentences giving the picture that should stay in the learner's head, not a definition), `check` (one question that asks for a prediction or a reason, not a formula).
4. **Link it.** Add at least one link, and usually two to four: what it builds on, and what it makes possible. A link points from the foundation to what it makes possible, and is stored in the file of the topic it leads to. Its `why` is one sentence saying exactly what carries over.
5. **Courses.** Never write `courses` on a topic. If the topic belongs to a course, add a concept for it in `curricula/<course>.json` (see `docs/curricula.md`).
6. **Later courses.** If the idea comes back in a later course, add `later`: the course id (it must be in `curricula/courses.json`) and one line on how it comes back.
7. **Build and check:** `python3 scripts/build.py`, then `python3 scripts/check.py`.
8. **Look at it.** Open `index.html#<the id>` in a browser, or take a screenshot with headless Chrome, and see that the topic sits readably in its circle.

## Checks

- `python3 scripts/check.py map generated curricula` passes.
- The writing follows the house style: plain, short sentences, the picture first, units on every number, `j` for the imaginary unit.

## Done means

- The topic is on the map with an essence, a check question and at least one link with a why.
- Nothing was edited inside `index.html` by hand.
- No existing topic says the same thing.
