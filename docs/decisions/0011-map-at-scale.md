# 0011. How the map stays readable with hundreds of topics

Status: accepted, 2026-11-15.

## Context

The map grows from 21 topics to about 450. At that size, fitting the whole map on screen makes every label a few pixels tall, hundreds of hairlines become a haze, and working out the arrangement takes time.

## Options

- **Show less: one area at a time.** Readable, but it hides the connections between areas, which are the point of the map.
- **Keep drawing everything at every zoom.** Unreadable when zoomed out.
- **Change what is drawn with the zoom, and add filters.** The overview shows the shape; the detail appears as you go in.

## Decision

Below half scale a topic is drawn as a dot and the folder names carry the map; the topic in focus and its neighbours keep readable labels. Links are fainter the more of them there are, and full strength only for the focused topic. A subfolder's name sits on the bottom of its circle so it never lands on its parent's. Filters dim what does not match: by course, by what exists (a tool, a plan, nothing), and by the learner's level. When `learner/levels.js` can be loaded, each topic carries a mark in one hue that deepens with the level. The arrangement is worked out once per data and window shape and kept in local storage.

## Consequences

- Measured in headless Chrome with 522 topics and 749 links: 0.9 s for the first arrangement, 0 ms afterwards.
- A preview that cannot load `learner/levels.js` draws the map without levels and shows no error.
- `window.MOMENTOS.show(folder)` jumps to a folder with no animation, for checking with screenshots.
