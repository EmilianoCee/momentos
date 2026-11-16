# 0012. Course ids are the names in everyday use, checked against the catalog in a registry

Status: accepted, 2026-11-15.

## Context

Berkeley renumbers courses. In the 2026-27 catalog, EECS 16A is EL ENG 66, EECS 16B is EL ENG 64, and Math 1B is Math 52. Learners still call them by the old names, and the local materials are filed under them.

## Options

- **Use catalog numbers everywhere.** Correct today, unfamiliar to the people using the repo, and wrong again after the next renumbering.
- **Use everyday names with no check.** Familiar, but a stale number would be cited as fact.
- **Everyday names as ids, with a registry that records the catalog entry and the date it was read.** Familiar and verifiable.

## Decision

`curricula/courses.json` lists every course id used anywhere in the repo, with its current catalog number, exact title, catalog URL and the date the catalog was read. Every course named in a curriculum, a plan, a topic's `later` note or a learner profile must be in the registry.

## Consequences

- When the catalog changes, one file changes.
- The readable curricula show both the everyday name and the catalog entry.
