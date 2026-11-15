# 0005. Topics are filed by what the idea is about, not by course

Status: accepted, 2026-11-15.

## Context

The map grows from three areas to cover discrete maths, calculus, mechanics, electromagnetism, devices and control. Folders are drawn as circles, so the folder tree is the shape of the map. An idea such as convolution belongs to several courses but must be one topic.

## Options

- **One folder per course.** Easy to file, but the same idea would appear once per course, and the map would show the timetable, not the subject.
- **A flat list with tags.** No filing decisions, but nothing to draw as circles and nothing to zoom into.
- **A small set of subject folders, with courses as a property of each topic.** One topic per idea. Courses become a filter.

## Decision

Top-level folders: `maths`, `physics`, `signals`, `systems`, `circuits`, `devices`, and `unspecified` as a parking lot. Subfolders: `maths/{linear-algebra, complex-numbers, calculus, multivariable, discrete, probability}`, `physics/{mechanics, thermodynamics, electromagnetism, waves-optics, modern}`, `signals/{fourier, sampling}`, `systems/control`, `circuits/amplifiers`, `devices/{semiconductors, pn-junction, mos}`. The rule: file a topic under the kind of thing it is a statement about. Maths needs no physical quantity. Physics is a law of nature. Devices is what happens inside a component. Circuits is what connected components do. Signals are functions of time and their representations. Systems turn signals into signals.

## Consequences

- A new top-level folder needs a change to `TOP_FOLDERS` in `scripts/momentos.py` and to `docs/map.md`. That friction is intended.
- A folder that passes about 45 topics should be split into subfolders.
- The three existing tools stay where they are.
