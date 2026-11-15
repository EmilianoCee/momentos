# Build status: the mastery architecture

This file is temporary. It exists so that a session that runs out of tokens can be picked up again.
When the build is finished it is replaced by the final report and deleted.

## How to resume

1. Read this file. Then read `course-survey/_design-notes.md` (local, untracked): it holds the design
   decisions in full and the learner's answers from the checkpoint.
2. Run `git log --oneline -15` and `git status` to see what is committed and what is in flight.
3. Check the usage limits before starting subagents. Run at most three at a time.
4. Carry on from "Next action" below. Tick items as they finish. Commit at the end of each phase. Never push.
5. Keep turns few and batched: write several files per turn, verify with scripts, do not re-read files.

## What was approved (2026-11-15)

- The learner's record lives in a gitignored `learner/` folder, created by `python3 scripts/learner.py init <handle>`,
  which is also its own private git repository. Evidence is an append-only `learner/evidence.jsonl`. A script
  computes levels, reviews and fall-backs. Models only grade one answer against written anchors.
- Level rules: L1 self-rating or any answer; L2 two answers showing L2 or one showing L3; L3 correct predictions
  on two days plus one explain, sketch, limit or connection answer; L4 adds an unfamiliar exam-style problem and
  naming where the model breaks; L5 adds a derivation and a connection to another field. Mastered is L4 held at a
  review at least 7 days later. A failed review drops one level. Intervals 3, 7, 14, 30, 60, 120 days. A review
  overdue by more than its interval (at least 7 days) costs one level, never below L2.
- Map source is split into `map/<folder>.json`; `scripts/build.py` inlines it into `index.html`.
- Top-level topic folders: maths, physics, signals, systems, circuits, devices (plus unspecified).
- `AGENTS.md` is the single source of rules; `CLAUDE.md` imports it. Skills live in `.claude/skills/`.
- Each tool keeps its maths in `<script id="maths">` with `<script type="application/json" id="check-cases">`.
  `scripts/test-tools.js` runs them with Node built-ins. A plan's check cases must equal the output of its Python
  reference script in `plans/checks/`.
- Curricula are `curricula/<course>.json` with a generated readable view and a verified course registry.
- `j` is the imaginary unit everywhere, including EE 120 content (the course itself writes `i`).
- About 450 map topics is accepted. Plans: a stub for every key concept first, then full plans in priority order.
- The original brief is replaced by an abstract, learner-neutral version in the repo. Anything that describes one
  learner lives in the untracked `learner/` folder, in a structure the template gives every learner.
- Survey notes live in `course-survey/` (gitignored). `course-materials/` holds only course materials.
- Course ids keep the names in use (`EECS 16A`, `EECS 16B`, `Math 1B`); the registry records the current catalog
  number and title for each.

## Phases

- [x] Survey and checkpoint
- [ ] 0. Close the survey gaps
  - [ ] Physics 7A, 7B, 7C research -> `course-survey/web-physics7.md`
  - [ ] Upper-division course numbers checked against the catalog -> `course-survey/web-upper-division.md`
  - [ ] EE 120 SP24 MT2 and MT3 rows, and notes for the 2024 to 2026 exams
  - [ ] EECS 16B exam table (the saved file has 3 of 26 rows)
  - [ ] Citations for the learning research checked
- [ ] 1. Architecture, schemas, checkers
  - [ ] `map/` source files, `scripts/build.py`, `index.html` reads the generated block
  - [ ] `scripts/learner.py`, `templates/learner/`
  - [ ] `scripts/check.py` (map, tools, house style, plans, curricula, skills, learner template), `scripts/test-tools.js`
  - [ ] `scripts/sync-house-style.py`; the three tools moved to the maths block and the synced style
  - [ ] Map page: filters, labels to dots when zoomed out, quiet links, level colour; timed at 450 topics
  - [ ] GitHub Actions workflow
  - [ ] Decision records in `docs/decisions/`
- [ ] 2. Instruction layer: `AGENTS.md`, `CLAUDE.md`, skills, `README.md`, `docs/`
- [ ] 3. Mastery framework: charter, levels, quiz protocol, pre-prompt, chat protocol, my profile in `learner/`
- [ ] 4. Curricula: EE 120, EE 105, EE 128, EECS 16B, then outlines for the tier 4 courses
- [ ] 5. Map expansion, with notes for later courses; screenshots checked
- [ ] 6. Plans: template, stubs and backlog, full plans in priority order
- [ ] 7. Pilot: a Sonnet subagent builds one tool from its plan alone
- [ ] 8. Final verification and report; abstract brief; delete this file

## Next action

Phase 0 is running (three agents). Start phase 1 with `map/` and `scripts/build.py`.

## Log

- 2026-11-15 01:50. Plan approved. Survey notes copied to `course-survey/`. `.gitignore` updated.
