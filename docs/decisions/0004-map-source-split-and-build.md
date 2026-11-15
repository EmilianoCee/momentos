# 0004. The map's data is split into source files and built into index.html

Status: accepted, 2026-11-15.

## Context

The map's data was one JSON block inside `index.html`. With hundreds of topics that block is hard to edit, conflicts in merges, and costs a model a lot to read. But `index.html` must still open from disk, and as a single file in a preview that cannot load anything else.

## Options

- **Keep one block and edit it in place.** Nothing to build, but every change touches one large file.
- **Load the data at run time from separate files.** Impossible: no `fetch` from `file://`, and the preview shows one file.
- **Source files per folder, inlined by a build script.** Small files to edit, one file to open, and a check that fails when the inlined copy is stale.

## Decision

`map/<folder>.json` is the source: one file per folder on the map, holding that folder's topics and the links that lead to them. `python3 scripts/build.py` writes the combined data into the `map-data` block of `index.html`, one topic per line. `python3 scripts/build.py --check` fails when the block is out of date. A topic's `folder` is its file's path, and its `courses` come from `curricula/`.

## Consequences

- Adding a topic means editing one small file and running the build.
- Two people adding topics to different folders do not conflict.
- The generated block must never be edited by hand. The check catches it when it is.
- The same build step generates the README tool index, the readable curricula and the backlog.
