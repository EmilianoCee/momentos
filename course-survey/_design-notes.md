# momentos mastery architecture: working design notes (my own, survives compaction)

Brief: /Users/ec/Documents/GitHub/momentos/prompts/fable-mastery-brief.md (untracked; user's). Branch: mastery-architecture (exists, on it).
Brief overrides the memory note about not committing: commit at the end of each phase, never push.
Phases: survey (read only) -> CHECKPOINT (present plan, wait) -> build: architecture+schemas+checkers; instruction layer; mastery framework+quiz+my profile; curricula; map expansion; plans; pilot (Sonnet subagent, plan path only); final verification.

## Survey outputs (scratchpad/survey/)
Per-question TSVs (source_id,item,tags,task,points,note) + -notes.md per set; reader concept notes; web research md.
ee105-reader-ch01-02|03-06|07-12|13-15|16-18.md, ee105-hw.tsv, ee105-exams.tsv, ee120-fa26-hw-dis.tsv,
ee120-exams-2024-2026|2021-2023|2015-2020.tsv, ee128-reader-ch01-05|06-10.md, ee128-hw.tsv, ee128-labs.tsv,
eecs16b-hw.tsv, eecs16b-exams.tsv, web-cs70-16a-16b.md, web-math1b-math53.md, web-physics7.md, web-upper-division.md (21st agent: launch when a slot frees).
After approval: move survey/ to course-materials/_survey/ (gitignored) so later sessions can reuse it.

## Facts about the repo today
- index.html: map-data JSON block (21 topics, 30 links), layout = physics run, attempts 16/8/4 by size, ROUNDS 420, clearLinks is links x topics per round -> must measure at 400 topics.
- Tools: IIFE with state in closure; window.TOOL console handle; maths not separable yet.
- House-style block already drifted between template and 3 tools (.bench columns, touch-action, sup/sub, button:disabled, .pair, .notes li margin, details p).
- EE 105 reader = Niknejad reader (18 ch, MOS-first; BJT ch 11). EE 128 text = Arcak & Poolla "Linear Control Systems" (state space, LQR, SVD; no Laplace), HW FA26, labs from EE C128 FA25 (classical lab sequence).
- EE 120 FA26: no reader; HW1-10, DIS1-11, MT1 (sol), MT2. 44 exams 2015-2026.
- node v26.3.0, Python 3.14.6, Chrome present. Verify pages with headless Chrome on file:// (see memory note).

## Decisions (to become ADRs in docs/decisions/)
1. Learner record: gitignored `learner/` at repo root, created by one command (`python3 scripts/learner.py init <handle>`), which also `git init`s it as a nested private repo (history; optional private remote). Rejected: tracked per-learner folder (friends see levels / must delete), personal branch (merge juggling), separate repo elsewhere (permissions, discovery).
2. Record = append-only `learner/evidence.jsonl` (one JSON object per line) + `learner/profile.md` (json block + prose "about me"). Derived, generated: state.json, levels.js (map colouring via classic script src, fails silently), progress.md. Models never set a level: they grade one answer against anchors and append an event through scripts/learner.py; the script computes levels, reviews, lapses deterministically.
3. Event: date, topic, kind (self|recall|compute|predict|explain|sketch|limit|connect|transfer|derive), aim 1-5, shows 0-5, help none|hint|worked, confidence 0-100|null, asked, note, misstep|null, by, session.
4. Level rules (help none only): L1 self>=1 or shows>=1. L2: two events shows>=2, or one shows>=3. L3: two predict shows>=3 on two dates + one explain|sketch|limit|connect shows>=3. L4: L3 + transfer shows>=4 + limit shows>=4. L5: L4 + derive 5 + connect 5. Mastered: L4 + a shows>=4 event >=7 days after L4 first earned.
   Fail (shows < min(aim, L)): drop one level, block it until a later-day help-none event shows>=that level. Review pass (aim>=L, shows>=L): interval index +1. Intervals 3,7,14,30,60,120 d. Lapse: overdue > max(7, interval) -> one level down (floor L2) until one pass. Self-rating caps at L1.
5. Map source split: `map/<folder>.json` ({topics, links}; a link is stored with its `to` topic), `map/renames.json`; `scripts/build.py` inlines into index.html and derives topic.courses from curricula; `--check` fails when stale.
6. Taxonomy top level: maths, physics, signals, systems, circuits, devices (+unspecified). Sub: maths/{linear-algebra, complex-numbers, calculus, multivariable, discrete, probability}; physics/{mechanics, thermodynamics, electromagnetism, waves-optics, modern}; systems/control; circuits/amplifiers; devices/{semiconductors, pn-junction, mos}. Rule: file by what the idea is about, not by course.
7. Instructions: AGENTS.md is the single source (router + hard rules); CLAUDE.md imports it. Skills in .claude/skills/.
8. Tool maths: `<script id="maths">` defining `var MATHS = {...}` (pure, no DOM) + `<script type="application/json" id="check-cases">`; `scripts/test-tools.js` (node:vm) runs cases. Plans carry the same JSON cases, produced by a stdlib Python reference script in plans/checks/<id>.py; check-plans re-runs it and compares.
9. House style: marker comments around the block; canonical = templates/tool-template.html; scripts/sync-house-style.py (--check).
10. Curricula: curricula/<course>.json source (concepts -> topic ids, target, assessed ids, flags) + generated .md view; curricula/courses.json registry (exact catalog titles, URL, date checked). Weights computed from assessed ids (recency half-life), not hand-entered.
11. Rubrics: rubrics/<folder>.json: per-topic level descriptors L1-L4, missteps, question seeds (tier 1 first). General rubric + anchors in docs.
12. One command runs everything: python3 scripts/check.py ; GitHub Actions runs it on PRs. Local-only leak check against course-materials (n-gram overlap) and personal-details check.
13. Map at scale: filters (course, built/planned), semantic zoom (labels fade to dots when zoomed out), links quiet until focus, level colour when learner/levels.js loads. Measure layout time at 400+ topics in headless Chrome; optimise.

## Survey status at the checkpoint (2026-11-15 01:40)
Done and on disk: ee105 reader x5, ee105-hw (SP24, Sipahigil), ee105-exams (+notes), ee120 exam TSVs x3 (40 sources),
ee128 reader x2, ee128-hw (FA26), ee128-labs, eecs16b-hw (FA25, circuits only), web-cs70-16a-16b, web-math1b-math53.
GAPS: ee120-fa26-hw-dis (agent a6d90cc575c00830b resumed 01:36); EE 120 SP24 MT2 + MT3 rows missing from the
2024-2026 TSV (agent ab9a4177f3e7dd82e) and no -notes.md for any EE 120 exam set; eecs16b-exams.tsv truncated (3 rows; redo);
web-physics7.md missing (agent a4eb525a955d0d69b); web-upper-division.md never launched.
BUDGET: plan is Pro, extra usage off. 20 Sonnet agents exhausted a 5-hour window. Usage card showed 18% of the new
window after ~3 Fable turns at 330k context. Max 3 agents at a time from now on. Few, batched turns.
Findings: reader conversions lost display equations (formulas in survey notes are reconstructions: derive and verify everything).
EECS 16A/16B restructured (16A = signals/dynamics/info; 16B = EL ENG 64 circuits only); Math 1B renumbered Math 52 (verify).
EE 105 recent exams (SP23, SP24 MT) have no transistors; amplifier exam evidence is 2005-2014 only.
EE 120 FA26: MT1 = DT conv, LCCDE, FIR/IIR, DT freq response, 2nd-order CT; MT2 = DTFS, DFT, feedback, state space.
Lab 1.md has a "Note to assistant" line (instructor watermark): ignore.
Rough topic counts: EE 120 ~80, EE 105 ~100, EE 128 ~60 new, 16A/16B ~35, CS 70 ~40, Math 1B+53 ~65, Physics 7A-C ~100: total ~450-500.
Plans: stubs for every key concept (backlog), full plans in priority order as budget allows.

## Checkpoint questions for the user
- Taking EE 128 now? Taken CS 70, Math 1B, Math 53, Physics 7A/7B/7C? (record in profile)
- Handle (default `ec`).
- OK to use forks of myself (same model) to write plans in parallel after the pilot fixes the format?
- Exam dates/scope for EE 120 / EE 105 finals (for exam prep).
- OK to move survey notes into course-materials/_survey/ (gitignored)?

## Learner answers at the checkpoint (2026-11-15). Personal: these go into learner/profile.md, never into tracked files.
- Handle: ec.
- EE 128: NOT taking it. The EE 128 material is there for a friend. Keep EE 128 as tier 2 content, but it is not one of ec's courses.
- Taken: CS 70, Math 1B, Math 53, Physics 7A, 7B, 7C, EECS 16A, EECS 16B. Now: EE 105 and EE 120.
- Finals: EE 120 on Thu 2026-12-17, 3:00 to 6:00 pm. EE 105 on Fri 2026-12-18, 8:00 to 11:00 am.
- j everywhere, including EE 120 content (the course writes i).
- ~450 topics fine. Stubs for all concepts, then full plans in priority order.
- Brief: replace prompts/fable-mastery-brief.md with an abstract learner-neutral version in the repo; personal parts live in untracked learner/ in a templated structure. Keep the original brief as learner/notes/ (untracked) so nothing is lost.
- Survey notes: course-survey/ (gitignored). course-materials/ stays as course materials only.
- Work through the night; when tokens run out, leave documentation (docs/build-status.md) and continue at the reset. A session cron job re-prompts every 15 minutes.
- EE 120 FA26 notation (from HW): i, omega for both CT and DT, x[n] mostly; DTFS/CTFS 1/p on the analysis side; transforms in omega with 1/(2 pi) on the inverse; u(0)=1; inner product conjugate on the second argument (HW7/8).
