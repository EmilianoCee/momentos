# Build status: the mastery architecture

This file is temporary. It exists so that a session that runs out of tokens, or whose context is compacted or
cleared, can pick the build up again from files alone. When the build is finished it is replaced by the final
report and deleted. The brief for the whole job is `prompts/fable-mastery-brief.md` (untracked; see phase 8).

## How to resume

1. Read this file. Then read `course-survey/_design-notes.md` (local, untracked): the learner's answers from the
   checkpoint are at the end of it. Read `docs/decisions/` for why things are the way they are.
2. Run `git log --oneline -8` and `git status`, then `python3 scripts/check.py` to see what passes.
3. Check the usage limits before anything expensive. Run at most three subagents at a time.
4. Carry on from "Next action". Tick items as they finish. Commit at the end of each phase. Never push.
5. Keep turns few and batched: write several files per turn, verify with scripts, do not re-read files.
   A turn that starts with a cold cache and a large context is very expensive, so keep the context small.

## What exists (committed)

- `map/<folder>.json` (source), `map/renames.json`, `scripts/build.py` (inlines the map into `index.html`,
  generates the README tool index, `curricula/*.md` and `plans/BACKLOG.md`), `scripts/momentos.py` (shared helpers,
  the weight formula, plan and curriculum loaders).
- `scripts/check.py`: sections generated, map, tools, style, tests, plans, curricula, rubrics, skills, docs,
  learner, personal, leaks. Read its top docstring and its constants (`FULL_SECTIONS`, `STUB_SECTIONS`, `VAGUE`,
  `CASE_TAGS`, `FLAGS`): they are the schemas.
- `scripts/learner.py` (init, add, paste, next, report, show, export, check, selftest) and `templates/learner/`.
- `scripts/test-tools.js`, `scripts/sync-house-style.py`, `.github/workflows/check.yml`.
- The three tools and the template follow the new conventions (maths block, check cases, synced house style).
- `index.html` handles hundreds of topics (dots when far, filters, level marks, kept arrangement).
- `docs/decisions/0001` to `0012`.

Known failing check right now: `skills` (instruction files name paths that phases 2 to 4 create), and it also
scans the untracked brief in `prompts/`. Both clear as the phases below land.

## Phases

- [x] Survey and checkpoint (approved 2026-11-15)
- [x] 0. Survey gaps. Done: Physics 7 (`course-survey/web-physics7.md`), course numbers
      (`course-survey/web-upper-division.md`), EE 120 homework and discussions. Left as they are: the EECS 16B exam
      table has 3 of 26 rows (the per-exam topics are in `course-survey/eecs16b-exams-notes.md`, which is enough);
      the complete EE 120 2024 to 2026 exam table (269 rows) and its notes are in the session scratchpad, not in
      `course-survey/` (an agent's write was blocked; the copy there has 207 rows and lacks SP24 MT2 and MT3).
- [x] 1. Architecture, schemas, checkers
- [ ] 2. Instruction layer
- [ ] 3. Mastery framework, quiz protocol, pre-prompt, the owner's record in `learner/`
- [ ] 4. Curricula
- [ ] 5. Map expansion
- [ ] 6. Plans: template, stubs, backlog, full plans in priority order
- [ ] 7. Pilot
- [ ] 8. Final verification and report

## Next action

Phase 2, then 3. Write these files, in this order, several per turn.

### Phase 2 files

- `AGENTS.md`: the single source. A router table ("if you are doing X, read Y, then use skill Z") and the hard
  rules: one file per tool with no dependencies, no `fetch`, no modules; the house style; colour only for
  quantities; `j` for the imaginary unit everywhere; units on every number; `prefers-reduced-motion`; keyboard
  wherever the pointer works; nothing copied from `course-materials/` or `course-survey/` into a tracked file; no
  personal details in tracked files; never write `Checked:` or a verified check case for something not checked;
  never edit a generated file; never set a level by hand; run `python3 scripts/build.py` then
  `python3 scripts/check.py` before a commit. Also: where the learner's record is, and that search tools skip it.
- `CLAUDE.md`: `@AGENTS.md`, `@prompts/learning-preprompt.md`, and two or three Claude-only lines.
- `README.md`: the front door for a friend. What this is; start your own record (one command); get quizzed; add a
  tool; how the repo is laid out; accuracy. Keep the tool-index markers. Move detailed conventions to `docs/`.
- `docs/charter.md` (one page: the shared goal, the ladder, what counts as evidence, the rules),
  `docs/map.md` (topic and link fields, the folder rule from decision 0005, granularity: one topic is one idea that
  can be pictured and tested with one question; `later` notes; renames),
  `docs/tools.md` (everything the old README said about tools, plus the maths block, check-case format from the
  header of `scripts/test-tools.js`, the header fields, the house-style sync, the optional evidence block),
  `docs/learner-record.md` (the files, the event fields and allowed aims per kind from `scripts/learner.py`, the
  evidence block format: JSON lines between `momentos-evidence v1` and `end`), `docs/levels.md` (the ladder and the
  rules exactly as `scripts/learner.py` implements them, with the self-test scenarios as examples),
  `docs/plans.md` and `plans/TEMPLATE.md` (see phase 6), `docs/curricula.md` (see phase 4).
- Skills in `.claude/skills/<name>/SKILL.md`, each with front matter (`name`, `description`) and the sections
  `## Steps`, `## Checks`, `## Done means`, written for a model that has read nothing else: `add-topic`,
  `write-plan`, `build-tool`, `quiz` (covers `quiz me <course>`, `quiz me <topic>`, `review`), `exam-prep`,
  `where-am-i`, `onboard`, `record-evidence`, `add-course`.

### Phase 3 files

- `docs/quiz-protocol.md`: the entry points and the `scripts/learner.py next` call behind each; the session loop
  (one question at a time; ask for a confidence from 0 to 100 before the answer; no hints until an answer, and a
  hint is recorded as `help: hint`; grade against the anchors; say the first wrong step; record with
  `scripts/learner.py add`); questions are always written fresh, with new numbers and units, never from course
  materials. The question kinds and what each asks: recall (L1), compute (L2), predict (L3), explain (L3),
  sketch in words (L3), limit (L3 inside the model, L4 where it breaks), connect (L3 for a map link, L5 for another
  field), transfer (L4), derive (L5). For each kind, anchors for what an L2, an L3 and an L4 answer looks like,
  concrete enough that two models grade alike. The general shape: L2 is right by formula with no mechanism; L3
  gives the mechanism in terms of the picture and gets the direction and rough size right; L4 also says, unasked or
  when asked, which assumption the answer rests on and what happens when it fails. An arithmetic slip with the
  right structure keeps the level; a right answer for a wrong reason does not earn it.
- `docs/mastery.md`: the loop (find the level, build the picture, practise, retrieve, space it out, transfer) and
  where the map, tools, quizzes and past exams sit in it, each choice grounded in research with sources. Have one
  subagent verify every citation (authors, year, title, venue) before it is written down. Candidates: Roediger and
  Karpicke 2006 (testing effect); Karpicke and Blunt 2011; Cepeda et al. 2006 and 2008 (spacing); Rohrer and Taylor
  2007 and Rohrer, Dedrick and Stershic 2015 (interleaving); Kalyuga, Ayres, Chandler and Sweller 2003 (expertise
  reversal); Dunlosky and Rawson 2012 (overconfidence); Rawson and Dunlosky 2011 (successive relearning); Dunlosky
  et al. 2013 (review of techniques); Crouch, Fagen, Callan and Mazur 2004 (predicting before a demonstration); Chi
  et al. 1989 (self-explanation); Barnett and Ceci 2002 (transfer); Bjork and Bjork 2011 (desirable difficulties).
- `prompts/learning-preprompt.md`: remove "Who I am" (it moves to `learner/profile.md`); step 1 reads the record
  and skips the level questions when there is evidence; a stated level sets the teaching mode for the session but
  never changes the record; after a session, the closing question is graded and recorded. Keep the ladder, the
  three modes and the shortcuts. `prompts/quiz-in-chat.md`: the protocol condensed for a chat with no repo, ending
  with the evidence block the model must return.
- The owner's record: `python3 scripts/learner.py init ec`, then fill `learner/profile.md` from the answers in
  `course-survey/_design-notes.md` and the old "Who I am" block. Move `prompts/fable-mastery-brief.md` to
  `learner/notes/` (untracked) once the abstract version exists (phase 8).

### Phase 4: curricula

`curricula/courses.json` first: every course id with its catalog entry from `course-survey/web-upper-division.md`
(ids keep everyday names: `EE 105`, `EE 120`, `EE 128`, `EECS 16A`, `EECS 16B`, `CS 70`, `Math 1B`, `Math 53`,
`Physics 7A`, `Physics 7B`, `Physics 7C`, plus the later courses used in `later` notes). Then one
`curricula/<slug>.json` per course (schema: `check_curricula` in `scripts/check.py`; view: `curriculum_view` in
`scripts/build.py`). Build the `assessed` lists from the tables in `course-survey/*.tsv` with a script that maps
survey tags to topic ids; identifiers drop the course prefix (`FA24 MT1 Q3`). Tiers: EE 120 and EE 105 are 1,
EE 128 is 2, EECS 16B is 3, the rest are 4. Targets: L4 where a concept has exam weight or two current-term
items, else L3. Flags: `old-exams-only` (EE 105 amplifiers: only 2005 to 2014 exams), `reader-only`,
`not-yet-assessed`, `lab-only`. Facts from the survey: EE 105 homework is SP24; its recent exams (SP23, SP24
midterms) have no transistors. EE 120 FA26 covers DT systems, state space, DTFS, DFT, CTFS, DTFT, CTFT and
modulation so far; sampling, Laplace and z are in scope by past exams. EE 128 FA26 uses the Arcak and Poolla text
(state feedback `u = Lx + v` in the book, `u = -Kx` in homework) plus classical design and labs. The EECS 16B
materials are FA25, circuits only. Every curriculum file must make sense without `course-materials/`.

### Phase 5: map expansion (about 450 topics)

Add topics to `map/<folder>.json` using the folders of decision 0005. Each new topic: `id`, `title`, `essence`,
`check`, and at least one link with a `why`, in the house style (plain, short, picture first, units, `j`). One idea
is one topic across all courses. Add `later` notes (course and one line on how the idea comes back) using only
course ids in the registry. Remove hand-written `courses` from the map files once the curricula list them. Then
`python3 scripts/build.py`, `python3 scripts/check.py`, and screenshots in headless Chrome of the whole map and of
zoomed areas (`window.MOMENTOS.show("folder/path")` jumps without animation).

### Phase 6: plans

`docs/plans.md` and `plans/TEMPLATE.md` define the format the checker enforces: a `json plan` block (id, title,
status stub|planned|built, kind tool|quiz-only, courses, topics, prerequisites, size S|M|L, tool path, checks path)
and the sections in `FULL_SECTIONS`. A tool plan's `json check-cases` block must equal the output of
`plans/checks/<id>.py` (standard library, prints one JSON list); cases carry `fn`, `args`, `expect`, `tol`,
`units`, `note` and a `tag`, with at least one each of `limit-zero`, `limit-infinity` and `breaks`. "Page text" is
the exact words on the page (title, lede, captions, what should click, predict prompts with answers, where this
shows up). Write a stub for every key concept of tiers 1 and 2 and the EECS 16B concepts the upper courses lean on
(the picture, what is dragged, the misconception), then full plans in backlog order. Derive every formula and
compute every number independently: the course readers lost their equations in conversion.

### Phase 7: pilot

Pick one high-priority full plan. Start a Sonnet subagent with only the repo path and the plan's path. Watch where
it struggles, fix the plan format, the template and the `build-tool` skill, and keep the tool only if every check
and every check case passes. Record what changed and why.

### Phase 8: finish

Run every check and test. Screenshot the map. Read five plans at random as a small model would. Write an abstract,
learner-neutral version of the brief (how to run this kind of pass for one's own courses) into the repo, move the
original brief to `learner/notes/`, delete this file, and write the final report the brief asks for.

## Log

- 2026-11-15 01:50. Plan approved. Survey notes in `course-survey/`.
- 2026-11-15 02:10. Phase 1 done in two commits. The usage window ran out.
- 2026-11-15 06:35. Resumed. Status rewritten so the build can continue from files alone.
