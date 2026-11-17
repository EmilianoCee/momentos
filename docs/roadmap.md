# Roadmap: the work that is left

The architecture is finished: map, build, checks, learner record, quizzes, skills, docs and decision records all
exist and pass `python3 scripts/check.py`. What is left is content. Each task below is sized for one session of
Opus 5.5 or Sonnet 5.5, names the skill to follow, and says what done means. Take the first unticked task unless
the user names another. Tick it in the same change that finishes it.

Every task ends with `python3 scripts/build.py`, then `python3 scripts/check.py`, which must pass. Commit on a
branch, never on `main`, and never push unless the user asks.

## How to read a task

- **Model:** the cheapest model that does it well. Opus for design and writing that a smaller model will build
  on (topics, curricula, plans). Sonnet for building from a complete specification (tools, rubric entries from a
  plan) and for extraction in subagents. At most three subagents at a time.
- **Local inputs:** `course-survey/` and `course-materials/` exist only in the owner's checkout. A task that needs
  them says so. Nothing from either folder is copied into a tracked file: identifiers and concept names only.
- **Formulas:** the course readers lost their display equations in conversion, so every formula in
  `course-survey/` is a reconstruction. Derive each formula yourself and check it against a limit before it goes
  into a plan or a check case.

## Now: the user can start

The owner's record exists and EE 120 is fully mapped. The user can run `onboard me` (the `onboard` skill), then
`quiz me EE 120` daily. Finals: EE 120 on 2026-12-17 and EE 105 on 2026-12-18 (the dates are also in
`learner/profile.md`). Tasks 1 to 3 serve those finals first.

## Tier 1: EE 120 and EE 105

- [x] **1. EE 105 topics and curriculum.** Model: Opus. Skills: `add-topic`, `add-course`. Local inputs: yes.
  - Read `course-survey/ee105-reader-ch*.md` (concept notes per chapter, with the tags used below),
    `course-survey/ee105-hw-notes.md` and `course-survey/ee105-exams-notes.md`.
  - Add about 90 topics in `devices/semiconductors`, `devices/pn-junction`, `devices/mos` and
    `circuits/amplifiers`, and reuse what exists (`transfer-function`, `poles-and-zeros`, `phasors-impedance`,
    `feedback`, `frequency-response`, `first-order-system`, `kcl`, `nodal-analysis`). A Bode plot topic is
    missing from the map: add `bode-plot` in `systems` and use it for both EE 120 and EE 105.
  - Units follow the reader's chapters: LTI and AC circuits; semiconductors and drift and diffusion; IC resistors
    and capacitors; pn junctions in equilibrium and with current; the MOS capacitor; MOSFET physics; small-signal
    models; the bipolar transistor; single-stage amplifiers; current mirrors and biasing; amplifier frequency
    response; multistage amplifiers; differential pairs; op-amps and feedback; non-ideal op-amps.
  - Fill each concept's `assessed` with `python3 scripts/assessed.py "EE 105" <tags> --scope SP24 --tier 1 --old-before 2020`
    (`--list-tags` shows the tags). Copy `target` and `flags` from its output.
  - In `notes`, say: the latest local homework is Spring 2024; the two recent midterms (SP23, SP24) have no
    transistor questions, so amplifier concepts carry only 2005 to 2014 exam weight and are flagged
    `old-exams-only`; they stay at target 4 because the course text treats them as core. EE 105 symbols: `V_T` is
    the MOS threshold and kT/q is the thermal voltage; "saturation" means opposite things for MOS and BJT;
    PMOS is written with source-high quantities (`V_SG`, `V_SD`, `|V_T|`).
  - Done: the file curricula/ee-105.json exists, every concept points at a map topic, `python3 scripts/learner.py report`
    shows an EE 105 section, and the map reads well in a headless Chrome screenshot of `devices`.
  - Done 2026-11-16. 108 concepts in 16 units (89 at target 4, 19 at 3); 94 new topics, 14 reused. Read these
    before extending it:
    - The concept-to-tag map lives in the local helper `course-survey/build-ee105-curriculum.py` (untracked, like
      the survey). It writes curricula/ee-105.json from the survey tables with the same target and flag rules as
      `assessed.py`, and lets a concept narrow its tagged rows by a regex on the survey's note column
      (`depletion-width`, `triode-region`, `minority-carrier-diffusion`, `early-effect`,
      `diode-connected-transistor`) or list items by hand (`rhp-zero`). Edit the map there and re-run it rather
      than editing the JSON by hand. `--report` prints weights and any unused tag.
    - One topic per idea across MOS and BJT: `common-source` also covers common emitter, `common-gate` common
      base, `source-follower` the emitter follower, `source-degeneration` emitter degeneration. Their survey tags
      are merged.
    - The thermal voltage is written kT/q on the map, never V_T, which is the MOS threshold (see `docs/map.md`).
    - New folders: `devices/bjt` (added to the table in `docs/map.md`), `systems/control` (loop gain, the
      gain-bandwidth trade, phase margin; EE 128 will add to it), `physics/thermodynamics`
      (`boltzmann-factor`), `physics/electromagnetism` (`gauss-law`, `poisson-equation`).
    - Twelve concepts are `reader-only` (no survey item): they are the connecting ideas (`boltzmann-factor`,
      `incremental-capacitance`, `potential-vs-doping`, `phase-margin`, ...). Keep them at target 3.

- [ ] **2. Rubrics for the 30 heaviest EE 120 and EE 105 topics.** Model: Opus writes five as models; Sonnet
  subagents write the rest from them. Skill: none (format in `docs/quiz-protocol.md`, "The topic's rubric").
  - One entry per topic in `rubrics/<folder>.json`: `L1` to `L4` (what an answer at that level says, on this
    topic, concretely), `missteps` (the usual first wrong steps), `seeds` (one per kind: `predict`, `explain`,
    `limit`, `transfer`; set-ups to vary, never exam text).
  - Take the order from `plans/BACKLOG.md`, "Concepts with no plan yet".
  - Done: `python3 scripts/check.py rubrics` names fewer than 150 tier 1 topics without descriptors (179 before).

- [ ] **3. Plan stubs for every tier 1 concept.** Model: Opus. Skill: `write-plan` (stubs only: steps 1 to 4).
  - A stub is `plans/<id>.md` with the `json plan` block (`status` `stub`, no `checks`) and four short sections:
    Concept, Picture, Interaction, Misconception (quiz-only: Concept, Why no tool, Misconception). See
    `docs/plans.md`.
  - Group closely linked concepts into one tool (for example `ft-time-shift`, `ft-frequency-shift` and
    `ft-duality` into one Fourier-properties tool). Expect about 60 tools and 25 quiz-only plans for the two courses.
  - Done: "Concepts with no plan yet" in `plans/BACKLOG.md` lists no EE 120 or EE 105 concept.
  - Suggested EE 105 groups (one tool each): junction electrostatics (`depletion-region`, `depletion-width`,
    `built-in-potential`, `poisson-equation`, `pn-reverse-bias`, `depletion-capacitance`); diode currents
    (`pn-forward-bias`, `minority-carrier-diffusion`, `diode-iv`, `diode-small-signal`); carriers and transport
    (`doping`, `mass-action-law`, `drift-current`, `diffusion-current`, `resistivity`); the MOS capacitor
    (`accumulation-depletion-inversion`, `flatband-voltage`, `threshold-voltage`, `mos-cv-curve`); MOSFET I–V
    (`mosfet-regions`, `triode-region`, `pinch-off`, `square-law`, `channel-length-modulation`, `pmos`);
    single-stage amplifiers (`common-source`, `common-gate`, `source-follower`, `source-degeneration`,
    `resistance-looking-in`); mirrors (`current-mirror`, `cascode-mirror`, `output-swing`); the differential pair
    (`differential-pair`, `common-and-differential-mode`, `half-circuit`, `cmrr`); op-amp feedback (`loop-gain`,
    `gain-bandwidth-product`, `phase-margin`, `op-amp-model`); and `bode-plot`, shared with EE 120. Likely
    quiz-only: `planar-process`, `ac-power`, `electrons-and-holes`, `energy-bands`, `offset-voltage`,
    `op-amp-bias-current`, `amplifier-noise`.
  - Started 2026-11-16: ten stubs for the circuits side (RC and RL, amplifiers, op-amps) are in `plans/`:
    `thevenin-norton`, `rc-rl-step-response`, `bode-plot`, `small-signal-analysis`, `common-source`,
    `resistance-looking-in`, `amplifier-two-port`, `current-mirror`, `ideal-op-amp`, `loop-gain`. They are stubs
    only: no reference scripts, no numbers. Still without a stub on that side: the Miller effect and amplifier
    frequency response (`miller-effect`, `amplifier-frequency-response`, `open-circuit-time-constants`,
    `dominant-pole`), the differential pair (`differential-pair`, `common-and-differential-mode`, `half-circuit`,
    `cmrr`), and everything on the devices side, starting with junction electrostatics (a stub was not written:
    the owner moved to circuits first).
  - Tool folders: a tool goes in the folder of its first topic on the map. So the RC and RL tool is under
    `systems/` (its topics are `first-order-system` and `step-response`), and the amplifier tools are under
    `circuits/amplifiers/`.

- [ ] **4. Full plans, in backlog order.** Model: Opus, one or two plans per session. Skill: `write-plan`.
  - Expand the first `stub` row of `plans/BACKLOG.md`. The reference script in `plans/checks/` comes first, and
    the plan's check cases are its output, pasted unchanged.
  - Done per plan: status `planned`, and `python3 scripts/check.py plans` passes.
  - Started 2026-11-17: `bode-plot`, `ideal-op-amp` and `rc-rl-step-response` are full plans with reference
    scripts, and their topics have rubric entries. Next: `small-signal-analysis`.

- [ ] **5. The pilot.** Model: Opus runs it, a Sonnet subagent builds. Skill: `build-tool`.
  - Once one full plan exists, start a Sonnet subagent with only: "Work in the repo at <path>. Follow
    `.claude/skills/build-tool/SKILL.md` to build the tool specified by `plans/<id>.md`." Nothing else from the
    conversation.
  - Watch where it struggles. Fix `plans/TEMPLATE.md`, `docs/plans.md` and the `build-tool` skill to match.
    Keep the tool only if every check and every check case passes and it looks right in light and dark.
  - Done: a new decision record, docs/decisions/0013-pilot.md, records what the subagent got wrong, what was changed, and why.

- [ ] **6. Build tools, in backlog order.** Model: Sonnet, one tool per session. Skill: `build-tool`.
  - Done per tool: the plan's acceptance checklist holds and the plan's status is `built`.
  - Started 2026-11-17: the three plans above were built in the same session that wrote them (by the plan's
    author, not a fresh builder), so they do not count as the pilot of task 5. Each plan was edited where the
    build showed a layout that did not work (figure placement, label positions), and the plan now says what was
    built.

## Tier 2: EE 128

- [ ] **7. EE 128 topics and curriculum.** Model: Opus. Skills: `add-topic`, `add-course`. Local inputs: yes.
  - The materials are a friend's Fall 2026 offering: `course-survey/ee128-reader-ch01-05.md` and
    `ee128-reader-ch06-10.md` (Arcak and Poolla, *Linear Control Systems*), `ee128-hw-notes.md`,
    `ee128-labs-notes.md`. The catalog now calls the course EECS C128, "Invitation to Intelligent Control"; the
    registry already says so.
  - About 60 new topics, mostly in `systems/control` and `maths/linear-algebra`; reuse `state-space-model`,
    `state-modes`, `internal-stability`, `eigenvectors`.
  - In `notes`: the book writes state feedback as u = Lx + v (closed loop A + BL); the homework writes u = −Kx.
  - `assessed` from `python3 scripts/assessed.py "EE 128" <tags> --tier 2`, scope `FA26`.
  - Done: the file curricula/ee-128.json exists and passes. Then tasks 2 to 4 apply to it, after tier 1.

## Tier 3: EECS 16B

- [ ] **8. EECS 16B curriculum.** Model: Opus. Local inputs: yes (`course-survey/eecs16b-hw-notes.md`,
  `eecs16b-exams-notes.md`; the exam table has only 3 rows, so use the notes).
  - The local materials are the Fall 2025 offering, which is circuits only (the catalog now calls it EL ENG 64).
    Most topics exist or belong in `circuits`: capacitor and inductor laws, RC and RL transients, RLC, phasors,
    op-amps, Thevenin and Norton.
  - Plans only for the concepts EE 105, EE 120 and EE 128 lean on most: transients, phasors and impedance,
    op-amp basics, Bode plots.

## Tier 4: the rest of the map

- [ ] **9. Map topics and outlines for CS 70, EECS 16A, Math 1B, Math 53, Physics 7A, 7B and 7C.** Model: Opus,
  one or two courses per session. Skills: `add-topic`, `add-course`.
  - Inputs, already researched with sources: `course-survey/web-cs70-16a-16b.md`, `web-math1b-math53.md`,
    `web-physics7.md` (local), each with 30 to 50 topic candidates. Without them, research the official course
    site and the catalog again.
  - `curricula/<course>.json` with `tier` 4, `sources` (URL and access date), `outline`, units, and concepts
    with empty `assessed`. No plans.
  - Expect about 250 topics in all. Folders: `maths/discrete`, `maths/probability`, `maths/calculus`,
    `maths/multivariable`, `physics/mechanics`, `physics/thermodynamics`, `physics/electromagnetism`,
    `physics/waves-optics`, `physics/modern`.
  - Done per course: it passes, and the map still reads well (screenshots of the whole map and of the new folder).

- [ ] **10. Notes for later courses.** Model: Sonnet. After task 9.
  - Add `later` to every topic that comes back in an upper-division course, using only ids in
    `curricula/courses.json` (EE 113 to EE 192, EECS 126, 127, 149, 151, C106A, CS 170, 189, EE 221A, 240A).
    One line each on how it comes back.

## Finishing

- [ ] **11. Final verification.** Model: Opus.
  - Every check passes. Screenshots of the whole map and of three zoomed folders, in light and dark.
  - Read five plans picked at random as a builder with nothing else, and fix what is unclear.
  - Write the final report: what exists, numbers per course, what is left.

## Done

- 2026-11-15: architecture, schemas and checkers; the instruction layer and nine skills; the mastery framework,
  quiz protocol and pre-prompts; the course registry (35 courses, checked against the 2026-27 catalog); the
  EE 120 curriculum and its 82 concepts on the map; the owner's record.
- 2026-11-16: the EE 105 curriculum (108 concepts) and 94 new map topics; `bode-plot` added to EE 120. Fixed a
  map bug: the filters overwrote each topic's list of outgoing links, so clicking a topic or opening
  `index.html#<id>` threw an error.
- 2026-11-17: the first three EE 105 and EE 120 tools, from full plans: `systems/bode-plot.html`,
  `circuits/amplifiers/ideal-op-amp.html`, `systems/rc-rl-step-response.html`, with 65 check cases between them
  and rubric entries for their seven topics.
