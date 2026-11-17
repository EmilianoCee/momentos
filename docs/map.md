# The map

`index.html` draws the map. Its data is generated from the files in `map/`. Edit those, never the block inside
`index.html`, then run `python3 scripts/build.py`.

## One file per folder

`map/maths/linear-algebra.json` holds the topics of the folder `maths/linear-algebra`, which is drawn as a circle
inside the circle of `maths`. A file has two lists:

```json
{
  "topics": [
    {
      "id": "rc-step-response",
      "title": "RC step response",
      "essence": "A capacitor charges toward the source voltage, covering 63% of what is left every RC seconds.",
      "check": "You double R. What happens to the final voltage, and to how long it takes to get there?",
      "tools": ["circuits/rc-step-response.html"],
      "later": [{ "course": "EE 140", "how": "Every amplifier node settles like this, with its own R and C." }]
    }
  ],
  "links": [
    { "from": "kvl", "to": "rc-step-response", "why": "KVL round the loop is what turns into the differential equation." }
  ]
}
```

| Field | Required | What it is |
|---|---|---|
| `id` | yes | unique across the whole map, lowercase words joined by hyphens. It never changes (see Renames). |
| `title` | yes | the words drawn on the map. Short: three words is plenty. |
| `essence` | yes | one or two sentences: the picture that should stay in the learner's head. Not a definition. |
| `check` | yes | one question that tests whether the learner can picture it. It asks for a prediction or a reason, not a formula. |
| `tools` | no | repo paths of the tools that teach it. A topic with none is drawn in italics, as planned. |
| `later` | no | where the idea comes back in a later course: `course` (an id in `curricula/courses.json`) and `how` (one line). |

A topic's folder is its file's place, so there is no `folder` field. Its courses come from `curricula/`, so there
is no `courses` field either. Write `e^(jθ)` to get a superscript. Write the thermal voltage as kT/q: `V_T` is the
MOS threshold voltage.

A link points from a foundation to what it makes possible. It is stored in the file of the topic it leads **to**.
Its `why` is one sentence saying what exactly carries over. Every topic needs at least one link.

## What is one topic

One topic is one idea that can be pictured and tested with one question. It is not a chapter, and it is not a
formula. "Convolution" is a topic. "Signals and systems" is a folder. "The convolution integral's limits" is part
of a topic.

One idea gets one topic across all courses. Convolution is taught in three courses and is still one topic, listed
in three curricula.

## Which folder

File a topic under the kind of thing it is a statement about, never under the course that teaches it.

| Folder | A topic belongs here when it is about | Subfolders |
|---|---|---|
| `maths` | something that needs no physical quantity to state | `linear-algebra`, `complex-numbers`, `calculus`, `multivariable`, `discrete`, `probability` |
| `physics` | a law of nature | `mechanics`, `thermodynamics`, `electromagnetism`, `waves-optics`, `modern` |
| `signals` | functions of time or of an index, and ways to represent them | `fourier`, `sampling` |
| `systems` | things that turn signals into signals | `control` |
| `circuits` | what connected components do, given how each behaves at its terminals | `amplifiers` |
| `devices` | what happens inside a component to give it that behaviour | `semiconductors`, `pn-junction`, `mos`, `bjt` |
| `unspecified` | nothing yet: a parking lot | |

When two folders fit, choose the one where the idea is first needed. A folder that passes about 45 topics is split
into subfolders. A new top-level folder needs a decision record and a change to `TOP_FOLDERS` in
`scripts/momentos.py`.

## Renames

Learners' records refer to topics by id, so an id is never reused and never silently changed. To rename or merge a
topic, change it in its map file and add `"old-id": "new-id"` to `map/renames.json`. Records follow the rename.

## The page

Scroll to zoom, drag to pan, `/` to search, click a folder's name to zoom to it. Zoomed out, topics are drawn as
dots. The three menus dim what does not match: one course; what exists for a topic (a tool, a plan ready to
build, nothing yet); and, when this checkout has a learner record, the learner's level. The level marks come from
`learner/levels.js`, which `scripts/learner.py` writes.
