# momentos: rules for every agent

momentos is a shared store of intuition for maths, physics, signals, systems and circuits, and a system for
reaching mastery of them with evidence. The content (map, tools, plans, curricula, rubrics) is shared. Each
learner's levels and history are their own and are never in the shared repo.

If you have read nothing else, read [docs/charter.md](docs/charter.md) (one page). This file is the single source
of the rules. `CLAUDE.md` only imports it.

## If you are asked to do X, read Y

| You are asked to | Read first | Then follow the skill |
|---|---|---|
| teach or explain a topic | `prompts/learning-preprompt.md`, `learner/profile.md` | `record-evidence` when the session ends |
| quiz: "quiz me EE 120", "quiz me convolution", "review" | `docs/quiz-protocol.md` | `quiz` |
| prepare for an exam: "exam prep EE 105 FINAL" | `docs/quiz-protocol.md` | `exam-prep` |
| report progress: "where am I" | `docs/levels.md` | `where-am-i` |
| start a record for a new learner, or place them | `docs/learner-record.md` | `onboard` |
| record an evidence block pasted from a chat or a tool | `docs/learner-record.md` | `record-evidence` |
| add a topic or a link to the map | `docs/map.md` | `add-topic` |
| write a plan: "write the next plan" | `docs/plans.md`, `plans/BACKLOG.md` | `write-plan` |
| build a tool: "build the next tool" | `docs/tools.md`, the plan itself | `build-tool` |
| add a course, or extend a curriculum | `docs/curricula.md` | `add-course` |
| continue building the repo: "what's next", "carry on" | `docs/roadmap.md` | the skill the task names |
| add a learner's own courses | `prompts/add-my-courses.md` | `add-course` |
| change how the repo itself works | `docs/decisions/` | none: write a new decision record |

Skills are plain markdown in `.claude/skills/<name>/SKILL.md`. Each gives its steps, its checks and what done
looks like. An agent that cannot load skills reads the file and follows it.

## Hard rules

1. **A tool is one file.** No dependencies, no `fetch`, no ES modules, nothing loaded from another file. It must
   work opened from disk and in a preview that shows a single file. Wrap storage in try/catch.
2. **The house style is not edited in a tool.** Change it in `templates/tool-template.html`, then run
   `python3 scripts/sync-house-style.py`.
3. **Colour is for quantities.** One colour per quantity (`--c1` to `--c4`), the same in the figure, the numbers
   and the prose. Controls stay neutral.
4. **`j` is the imaginary unit, everywhere,** including content for courses that write `i`.
5. **Units on every number.** Define each symbol once.
6. **Keyboard works wherever the pointer does. Respect `prefers-reduced-motion`.** Do not redraw when nothing moves.
7. **Maths lives in the tool's `maths` block,** as plain functions with no DOM, tested by its check cases.
8. **Never claim a check that was not made.** No `Checked:` line, and no check case in a plan, for something that
   was not computed by a script you ran.
9. **Nothing is copied from `course-materials/` or `course-survey/` into a tracked file.** No problem text, no
   figures, no solutions, no reader prose. Concept names, chapter titles and question identifiers are fine.
   Questions are always written fresh.
10. **No personal details in tracked files.** A learner is a handle. Everything about one learner lives in `learner/`.
11. **Never set a level by hand.** Grade one answer against the anchors and record it with
    `python3 scripts/learner.py add`. The script works out the level.
12. **Never edit a generated file:** the `map-data` block of `index.html`, the tool index in `README.md`,
    `curricula/*.md`, `plans/BACKLOG.md`, and `state.json`, `levels.js`, `progress.md` in `learner/`.
    Edit the source and run `python3 scripts/build.py`.
13. **Before you finish any change:** `python3 scripts/build.py`, then `python3 scripts/check.py`. It must pass.
14. **Write plainly.** Short sentences. The picture first, then the formula. No hype, and nothing that only
    sounds like an explanation.

## Where things are

| Path | What it holds |
|---|---|
| `index.html` | the knowledge map. Its data block is generated. |
| `map/<folder>.json` | the map's source: topics, and the links that lead to them. Format: `docs/map.md` |
| `maths/`, `physics/`, `signals/`, `systems/`, `circuits/`, `devices/` | the tools, one folder per area of the map |
| `curricula/` | one JSON file per course, a generated readable view, and the course registry |
| `rubrics/<folder>.json` | per-topic level descriptors and question seeds for quizzes |
| `plans/` | one plan per tool, a reference script per plan in `plans/checks/`, and the generated backlog |
| `prompts/` | the learning pre-prompt, and the quiz protocol for a chat with no repo access |
| `templates/` | the starting point for a tool, and for a learner's record |
| `scripts/` | `build.py`, `check.py`, `learner.py`, `assessed.py`, `sync-house-style.py`, `test-tools.js` |
| `docs/` | the charter, the conventions, the decision records, and the roadmap of work left |
| `learner/` | **not in the shared repo.** This checkout's learner record. |
| `course-materials/`, `course-survey/` | **not in the shared repo.** Local course files and notes about them. |

## The learner's record

`learner/` is ignored by git, so search tools that respect `.gitignore` will not find it. Read it by path:
`learner/profile.md` for who the learner is, and `python3 scripts/learner.py report` or `show <topic>` for where
they stand. If `learner/` does not exist, say so and offer the `onboard` skill. Never copy anything from it into a
tracked file.
