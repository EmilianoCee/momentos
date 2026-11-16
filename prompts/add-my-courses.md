# Add your own courses

Paste this into Claude Code (or any agent that reads `AGENTS.md`) at the root of your fork, after you have started
your record with `python3 scripts/learner.py init <handle>`. Replace the list at the end with your courses.

---

Read `AGENTS.md`, `docs/charter.md`, `docs/curricula.md` and `docs/map.md` first. Then add the courses listed below
to this repo so that I can be quizzed on them toward mastery. Take the time it needs: depth, not speed.

1. **Survey, without changing anything.** For each course: open its official catalog entry and its course
   website, and read whatever course materials I have put in `course-materials/<course>/` (that folder is
   ignored by git). If a file is large, read its outline first and only the parts you need. Write what you find,
   in your own words, to `course-survey/` (also ignored by git): the concepts in scope, and where each is
   assessed, one row per item, as `course-survey/<course>-<what>.tsv` with the columns
   `source_id, item, tags, task, points, note`. A `source_id` looks like `EE 120 FA24 MT1`.
2. **Stop and show me** the course outlines, a rough count of new topics, and any question you need answered.
   Wait for my answer.
3. **Build**, one course at a time, with the `add-course` and `add-topic` skills: the registry entry, the map
   topics (one idea is one topic across all courses, so reuse what exists), and `curricula/<course>.json`, with
   each concept's `assessed` list filled by `python3 scripts/assessed.py`.
4. **Check** with `python3 scripts/build.py` and `python3 scripts/check.py`, and look at the map in a browser.
5. **Tell me** what you added, and add the courses to `learner/profile.md`.

Rules that matter most: nothing from my course materials goes into a tracked file, only concept names and
identifiers such as `FA24 MT1 Q3`; course numbers come from the catalog, never from memory; `j` is the imaginary
unit.

My courses: <for example: "EE 140, which I am taking now; materials in course-materials/ee_140/">
