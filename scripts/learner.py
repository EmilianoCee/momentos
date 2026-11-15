#!/usr/bin/env python3
"""The learner's record: start it, add evidence to it, and read levels and reviews back out of it.

    python3 scripts/learner.py init <handle>            start a record in learner/ (one time)
    python3 scripts/learner.py next --course "EE 120"   what to quiz next, as JSON  (also --topic, --due, --exam)
    python3 scripts/learner.py add --topic kcl --kind predict --aim 3 --shows 3 --confidence 70 \\
            --asked "..." --note "..."                  record one graded answer
    python3 scripts/learner.py paste < block.txt        record an evidence block from a chat or a tool
    python3 scripts/learner.py report                   where am I: progress per course, written to learner/progress.md
    python3 scripts/learner.py show <topic>             one topic: level, what is missing, every answer so far
    python3 scripts/learner.py export --course "EE 120" everything a chat with no repo access needs, as one block
    python3 scripts/learner.py check                    validate the record
    python3 scripts/learner.py selftest                 run the built-in scenarios for the level rules

The record is plain text in learner/, which the shared repo ignores:

    profile.md       who the learner is: a small JSON block, then free prose
    evidence.jsonl   one graded answer per line, append only. This is the record of truth.
    state.json, levels.js, progress.md   generated from the two files above. Never edit them.

A model never sets a level. It grades one answer against the anchors in docs/quiz-protocol.md and adds the
event here. The rules below turn the events into levels, reviews and fall-backs, the same way every time.
They are documented in docs/levels.md. Standard library only.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import momentos as m  # noqa: E402

ROOT = m.ROOT
TEMPLATE = ROOT / "templates" / "learner"
GENERATED = ("state.json", "levels.js", "progress.md")

KINDS = ("self", "recall", "compute", "predict", "explain", "sketch", "limit", "connect", "transfer", "derive")
# The level a question of each kind is pitched at. docs/quiz-protocol.md says what each kind asks for.
AIMS = {"recall": (1,), "compute": (2,), "predict": (3,), "explain": (3,), "sketch": (3,),
        "limit": (3, 4), "connect": (3, 5), "transfer": (4,), "derive": (5,)}
HELP = ("none", "hint", "worked")
INTERVALS = (3, 7, 14, 30, 60, 120)      # days until the next review, after each review passed in a row
GRACE_MIN = 7                             # a review is "missed" once it is overdue by max(this, its interval)
MASTERY_GAP = 7                           # days L4 must have been held before a review confirms mastery
HANDLE = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")
STATUSES = ("now", "done", "next")
BLOCK_START, BLOCK_END = "momentos-evidence v1", "end"


def day(text):
    return datetime.date.fromisoformat(text)


def add_days(text, n):
    return (day(text) + datetime.timedelta(days=n)).isoformat()


def is_date(text):
    try:
        day(str(text))
        return True
    except ValueError:
        return False


# ----------------------------------------------------------------------------------- reading files

def read_profile(folder, problems):
    path = folder / "profile.md"
    if not path.is_file():
        problems.append("profile.md is missing.")
        return {}, ""
    text = path.read_text(encoding="utf-8")
    hit = re.search(r"```json\n(.*?)\n```", text, re.S)
    if not hit:
        problems.append("profile.md has no ```json block.")
        return {}, text
    try:
        data = json.loads(hit.group(1))
    except json.JSONDecodeError as err:
        problems.append(f"profile.md: the JSON block is not valid ({err.msg} at line {err.lineno} of the block).")
        return {}, text
    about = text[hit.end():].strip()
    return (data if isinstance(data, dict) else {}), about


def read_events(folder, problems):
    path = folder / "evidence.jsonl"
    events = []
    if not path.is_file():
        return events
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as err:
            problems.append(f"evidence.jsonl line {n}: not valid JSON ({err.msg}).")
            continue
        if not isinstance(event, dict):
            problems.append(f"evidence.jsonl line {n}: must be a JSON object.")
            continue
        event["_line"] = n
        events.append(event)
    return events


def event_problems(event, ids, renames):
    """What is wrong with one event, as a list of sentences. Empty means it is valid."""
    out = []
    if not is_date(event.get("date", "")):
        out.append("date must be YYYY-MM-DD")
    topic = event.get("topic")
    if not isinstance(topic, str) or not topic:
        out.append("topic is missing")
    elif m.resolve_id(topic, renames) not in ids:
        out.append(f"topic {topic!r} is not on the map")
    kind = event.get("kind")
    if kind not in KINDS:
        out.append(f"kind must be one of {', '.join(KINDS)}")
        return out
    shows = event.get("shows")
    if not isinstance(shows, int) or isinstance(shows, bool) or not 0 <= shows <= 5:
        out.append("shows must be a whole number from 0 to 5")
    if kind == "self":
        return out
    aim = event.get("aim")
    if aim not in AIMS[kind]:
        out.append(f"aim for a {kind} question must be {' or '.join(str(a) for a in AIMS[kind])}")
    if event.get("help", "none") not in HELP:
        out.append(f"help must be one of {', '.join(HELP)}")
    conf = event.get("confidence")
    if conf is not None and (isinstance(conf, bool) or not isinstance(conf, (int, float)) or not 0 <= conf <= 100):
        out.append("confidence must be a number from 0 to 100, or null")
    for field in ("asked", "note"):
        value = event.get(field)
        if not isinstance(value, str) or not value.strip():
            out.append(f"{field} is missing: one line, in your own words")
        elif len(value) > 400 or "\n" in value:
            out.append(f"{field} must be one line of at most 400 characters")
    if event.get("misstep") is not None and (not isinstance(event["misstep"], str) or not event["misstep"].strip()):
        out.append("misstep must be one line of text, or null")
    return out


def check_record(folder, template=False):
    """Validate a learner folder. Returns a list of problems (empty when it is valid)."""
    problems = []
    folder = Path(folder)
    profile, about = read_profile(folder, problems)
    if profile:
        if profile.get("schema") != 1:
            problems.append("profile.md: schema must be 1.")
        handle = profile.get("handle", "")
        if template:
            if handle != "":
                problems.append("profile.md: the template's handle must be empty.")
        elif not isinstance(handle, str) or not HANDLE.match(handle):
            problems.append("profile.md: handle must be lowercase letters, digits and hyphens (at most 32).")
        if not template and not is_date(profile.get("started", "")):
            problems.append("profile.md: started must be a date, YYYY-MM-DD.")
        known = {c.get("id") for c in m.load_courses([])}
        courses = profile.get("courses", {})
        if not isinstance(courses, dict):
            problems.append("profile.md: courses must be an object, course id to now, done or next.")
            courses = {}
        for course, status in courses.items():
            if known and course not in known:
                problems.append(f"profile.md: {course} is not a course id in curricula/courses.json.")
            if status not in STATUSES:
                problems.append(f"profile.md: {course} must be one of {', '.join(STATUSES)}.")
        for exam in profile.get("exams", []) or []:
            if not isinstance(exam, dict) or not exam.get("course") or not exam.get("name") or not is_date(exam.get("date", "")):
                problems.append("profile.md: each exam needs a course, a name (FINAL, MT1, ...) and a date.")
        size = profile.get("session_size", 8)
        if not isinstance(size, int) or not 1 <= size <= 30:
            problems.append("profile.md: session_size must be a whole number from 1 to 30.")
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}", json.dumps(profile) + about):
            problems.append("profile.md: contains an email address. A learner is known only by a handle.")
    ids = {t.get("id") for t in m.load_map([])["topics"]}
    renames = m.load_renames([])
    last = ""
    for event in read_events(folder, problems):
        for text in event_problems(event, ids, renames):
            problems.append(f"evidence.jsonl line {event['_line']}: {text}.")
        if is_date(event.get("date", "")):
            if event["date"] < last:
                problems.append(f"evidence.jsonl line {event['_line']}: is dated before the line above it. "
                                "The file is append only, oldest first.")
            last = max(last, event["date"])
    return problems


# --------------------------------------------------------------------------------- the level rules

def supported(seen, blocked, self_claim):
    """The highest level the evidence supports, and which levels' requirements are met.

    seen: graded events so far, oldest first. blocked: {level: date} for levels lost at a failed or missed
    review; a blocked level counts again once an unaided answer at that level is dated after the block.
    """
    unaided = [e for e in seen if e.get("help", "none") == "none"]

    def free(level):
        since = blocked.get(level)
        return since is None or any(e["shows"] >= level and e["date"] > since for e in unaided)

    n2 = sum(1 for e in unaided if e["shows"] >= 2)
    n3 = sum(1 for e in unaided if e["shows"] >= 3)
    days = {e["date"] for e in unaided if e["kind"] == "predict" and e["shows"] >= 3}
    other = any(e["kind"] in ("explain", "sketch", "limit", "connect") and e["shows"] >= 3 for e in unaided)
    met = {
        1: self_claim >= 1 or any(e["shows"] >= 1 for e in seen),
        2: n2 >= 2 or n3 >= 1,
        3: len(days) >= 2 and other,
        4: any(e["kind"] == "transfer" and e["shows"] >= 4 for e in unaided)
           and any(e["kind"] == "limit" and e["shows"] >= 4 for e in unaided),
        5: any(e["kind"] == "derive" and e["shows"] >= 5 for e in unaided)
           and any(e["kind"] == "connect" and e["shows"] >= 5 for e in unaided),
    }
    level = 0
    for step in (1, 2, 3, 4, 5):
        if not (met[step] and free(step)):
            break
        level = step
    progress = {"answers_at_l2": n2, "predict_days": len(days), "other_l3": other,
                "transfer": any(e["kind"] == "transfer" and e["shows"] >= 4 for e in unaided),
                "limit_l4": any(e["kind"] == "limit" and e["shows"] >= 4 for e in unaided),
                "derive": any(e["kind"] == "derive" and e["shows"] >= 5 for e in unaided),
                "connect_l5": any(e["kind"] == "connect" and e["shows"] >= 5 for e in unaided)}
    regain = level + 1 if level < 5 and met.get(level + 1) and not free(level + 1) else None
    return level, progress, regain


def topic_state(events, today):
    """Replay one topic's events, oldest first, and return where the topic stands on `today`."""
    s = {"level": 0, "earned": 0, "k": 0, "interval": None, "next_review": None, "lapsed": False,
         "mastered": False, "misstep": None, "last": None, "answers": 0}
    blocked, seen, self_claim, since4 = {}, [], 0, None

    def lapse(on):
        # A review overdue by more than its own interval (at least a week) costs one level, never below L2.
        if s["lapsed"] or s["level"] < 3 or not s["next_review"]:
            return
        limit = add_days(s["next_review"], max(GRACE_MIN, s["interval"] or 0))
        if on > limit:
            for level in range(s["level"], 6):
                blocked[level] = limit
            s["level"] = supported(seen, blocked, self_claim)[0]
            s.update(lapsed=True, k=0, interval=INTERVALS[0], next_review=limit)

    for e in events:
        lapse(e["date"])
        s["last"] = e["date"]
        if e["kind"] == "self":
            self_claim = max(self_claim, e["shows"])
            s["level"] = max(s["level"], supported(seen, blocked, self_claim)[0])
            s["earned"] = max(s["earned"], s["level"])
            continue
        s["answers"] += 1
        held = s["level"]
        seen.append(e)
        unaided = e.get("help", "none") == "none"
        failed = held >= 2 and e["shows"] < min(e["aim"], held)
        if failed:
            for level in range(held, 6):
                blocked[level] = e["date"]
        level = supported(seen, blocked, self_claim)[0]
        if failed:
            s.update(k=0, interval=1, next_review=add_days(e["date"], 1), lapsed=False)
        elif level >= 2 and level > held:
            s.update(k=0, interval=INTERVALS[0], next_review=add_days(e["date"], INTERVALS[0]), lapsed=False)
        elif level >= 2 and unaided and e["aim"] >= held and e["shows"] >= held:
            k = min(s["k"] + 1, len(INTERVALS) - 1)
            s.update(k=k, interval=INTERVALS[k], next_review=add_days(e["date"], INTERVALS[k]), lapsed=False)
        elif level >= 2 and s["next_review"] is None:
            s.update(interval=INTERVALS[0], next_review=add_days(e["date"], INTERVALS[0]))
        if level < 2:
            s.update(next_review=None, interval=None)
        if level >= 4 and held < 4:
            since4 = e["date"]
        elif level < 4:
            since4 = None
        s["level"] = level
        s["earned"] = max(s["earned"], level)
        if e.get("misstep"):
            s["misstep"] = {"date": e["date"], "text": e["misstep"], "aim": e["aim"]}
        elif s["misstep"] and unaided and e["shows"] >= e["aim"] >= s["misstep"]["aim"]:
            s["misstep"] = None
    lapse(today)
    level, progress, regain = supported(seen, blocked, self_claim)
    s["level"] = level
    s["progress"], s["regain"] = progress, regain
    if since4 and level >= 4:
        s["mastered"] = any(e.get("help", "none") == "none" and e["shows"] >= 4
                            and e["date"] >= add_days(since4, MASTERY_GAP) for e in seen)
    s["due"] = bool(level >= 2 and s["next_review"] and s["next_review"] <= today)
    return s


def next_step(state):
    """The question that would move this topic on: (aim, kind, why)."""
    level, p = state["level"], state["progress"]
    if state["regain"]:
        lost = state["regain"]
        kind = {2: "compute", 3: "predict", 4: "transfer", 5: "derive"}[lost]
        return lost, kind, f"L{lost} was lost at a review: one clean answer on a later day wins it back"
    if level <= 1:
        return 2, "compute", f"L2 needs two answers showing L2 (has {p['answers_at_l2']}), or one showing L3"
    if level == 2:
        if p["predict_days"] < 2:
            return 3, "predict", f"L3 needs correct predictions on two different days (has {p['predict_days']})"
        return 3, "explain", "L3 needs one explain, sketch, limit or connection answer"
    if level == 3:
        if not p["transfer"]:
            return 4, "transfer", "L4 needs an unfamiliar exam-style problem solved without help"
        return 4, "limit", "L4 needs naming where the model breaks"
    if level == 4:
        if not p["derive"]:
            return 5, "derive", "L5 needs a derivation from first principles"
        return 5, "connect", "L5 needs a connection to another field"
    return 5, "connect", "holding L5"


def review_step(state):
    level = state["level"]
    turn = state["answers"] % 2
    kind = {2: ("compute", "compute"), 3: ("predict", "explain"), 4: ("transfer", "limit"), 5: ("derive", "connect")}[level][turn]
    aim = level if level in AIMS[kind] else AIMS[kind][0]
    return aim, kind, f"review of L{level}, due {state['next_review']}"


# ------------------------------------------------------------------------------------- the record

class Record:
    def __init__(self, folder, today):
        self.folder = Path(folder)
        self.today = today
        self.problems = []
        self.profile, self.about = read_profile(self.folder, self.problems)
        self.renames = m.load_renames([])
        data = m.load_map([])
        self.topics = {t.get("id"): t for t in data["topics"]}
        self.events = read_events(self.folder, self.problems)
        by_topic = {}
        for event in self.events:
            if event_problems(event, set(self.topics), self.renames):
                continue
            by_topic.setdefault(m.resolve_id(event["topic"], self.renames), []).append(event)
        self.by_topic = by_topic
        self.states = {tid: topic_state(evs, today) for tid, evs in by_topic.items()}
        self.curricula = {c.get("course"): c for c in m.load_curricula([])}
        self._rubrics = {}

    def state(self, tid):
        return self.states.get(tid) or topic_state([], self.today)

    def concepts(self, course):
        """[(topic id, target, weight, exam weight)] for a course, with renames followed."""
        cur = self.curricula.get(course)
        out = []
        for concept in (cur or {}).get("concepts", []):
            tid = m.resolve_id(concept.get("topic", ""), self.renames)
            if tid in self.topics:
                w, ew = m.concept_weight(concept, cur)
                out.append((tid, concept.get("target", 3), w, ew))
        return out

    def rubric(self, tid):
        folder = self.topics[tid]["folder"]
        if folder not in self._rubrics:
            path = m.RUBRICS_DIR / (folder + ".json")
            self._rubrics[folder] = m.read_json(path, []) if path.is_file() else {}
        return (self._rubrics[folder] or {}).get(tid)

    def item(self, tid, mode, target=None, weight=None, step=None):
        st, topic = self.state(tid), self.topics[tid]
        aim, kind, why = step or (review_step(st) if mode == "review" else next_step(st))
        out = {"topic": tid, "title": topic.get("title"), "folder": topic["folder"], "mode": mode,
               "level": st["level"], "aim": aim, "kind": kind, "why": why,
               "essence": topic.get("essence"), "check": topic.get("check")}
        if target is not None:
            out["target"] = target
        if weight is not None:
            out["weight"] = weight
        if st["misstep"]:
            out["open_misstep"] = st["misstep"]["text"]
        rubric = self.rubric(tid)
        if rubric:
            out["rubric"] = rubric
        if topic.get("tools"):
            out["tools"] = topic["tools"]
        return out


def interleave(items):
    """Reorder so that neighbours come from different folders where that is possible."""
    out, rest = [], list(items)
    while rest:
        pick = next((i for i, it in enumerate(rest) if not out or it["folder"] != out[-1]["folder"]), 0)
        out.append(rest.pop(pick))
    return out


def queue_course(rec, course, n, exam_kind=None):
    if course not in rec.curricula:
        sys.exit(f"There is no curriculum for {course!r}. Courses with one: {', '.join(sorted(rec.curricula)) or 'none yet'}.")
    cur = rec.curricula[course]
    reviews, grows = [], []
    for concept in cur.get("concepts", []):
        tid = m.resolve_id(concept.get("topic", ""), rec.renames)
        if tid not in rec.topics:
            continue
        target = concept.get("target", 3)
        w, ew = m.concept_weight(concept, cur)
        if exam_kind:
            xw = m.concept_weight(concept, cur, exam_kind)[1]
            w = xw + 0.25 * w
        st = rec.state(tid)
        if st["due"] or st["regain"]:
            over = (day(rec.today) - day(st["next_review"])).days if st["next_review"] else 0
            reviews.append((over / max(1, st["interval"] or 1) + 0.01 * w, tid, target, w))
        elif st["level"] < target and (st["last"] != rec.today or exam_kind):
            grows.append((w * (target - st["level"]) * (0.5 if st["last"] == rec.today else 1), tid, target, w))
    reviews.sort(key=lambda x: (-x[0], x[1]))
    grows.sort(key=lambda x: (-x[0], x[1]))
    take = reviews[:max((n + 1) // 2, n - len(grows))]
    items = [rec.item(tid, "regain" if rec.state(tid)["regain"] and not rec.state(tid)["due"] else "review", t, w,
                      None if rec.state(tid)["due"] and not rec.state(tid)["regain"] else next_step(rec.state(tid)))
             for _, tid, t, w in take]
    items += [rec.item(tid, "grow", t, w) for _, tid, t, w in grows[:n - len(items)]]
    return interleave(items)


def queue_topic(rec, tid, n):
    tid = m.resolve_id(tid, rec.renames)
    if tid not in rec.topics:
        sys.exit(f"{tid!r} is not a topic on the map.")
    st = rec.state(tid)
    items = []
    if st["level"] >= 2:
        items.append(rec.item(tid, "review"))
    first = next_step(st)
    ladder = {0: [(2, "compute")] * 2, 1: [(2, "compute")] * 2, 2: [(3, "predict"), (3, "explain"), (3, "sketch")],
              3: [(4, "transfer"), (4, "limit")], 4: [(5, "derive"), (5, "connect")], 5: [(5, "connect")]}
    steps = [first] + [(a, k, first[2]) for a, k in ladder[st["level"]] if (a, k) != first[:2]]
    for step in steps:
        items.append(rec.item(tid, "regain" if st["regain"] else "grow", step=step))
    return items[:n]


def queue_due(rec, n):
    due = []
    for tid, st in rec.states.items():
        if st["due"] or st["regain"]:
            over = (day(rec.today) - day(st["next_review"])).days if st["next_review"] else 0
            due.append((over / max(1, st["interval"] or 1), tid))
    due.sort(key=lambda x: (-x[0], x[1]))
    return interleave([rec.item(tid, "review" if rec.state(tid)["due"] and not rec.state(tid)["regain"] else "regain",
                                step=None if rec.state(tid)["due"] and not rec.state(tid)["regain"] else next_step(rec.state(tid)))
                       for _, tid in due[:n]])


# ---------------------------------------------------------------------------------------- reports

def calibration(events):
    """Confidence against outcome. A pass counts 1, one level short counts 0.5, anything less 0."""
    rows = []
    for e in events:
        if e.get("kind") == "self" or e.get("confidence") is None or "aim" not in e:
            continue
        outcome = 1.0 if e["shows"] >= e["aim"] else 0.5 if e["shows"] == e["aim"] - 1 else 0.0
        rows.append((float(e["confidence"]), outcome))
    bands = []
    for lo, hi in ((0, 49), (50, 69), (70, 89), (90, 100)):
        mine = [(c, o) for c, o in rows if lo <= c <= hi]
        if mine:
            bands.append({"band": f"{lo} to {hi}", "answers": len(mine),
                          "confidence": round(sum(c for c, _ in mine) / len(mine)),
                          "right": round(100 * sum(o for _, o in mine) / len(mine))})
    brier = round(sum((c / 100 - o) ** 2 for c, o in rows) / len(rows), 3) if rows else None
    return {"answers": len(rows), "brier": brier, "bands": bands}


def course_summary(rec, course):
    concepts = rec.concepts(course)
    counts = [0] * 6
    at_target = mastered = due = lapsed = 0
    gaps = []
    for tid, target, w, _ in concepts:
        st = rec.state(tid)
        counts[st["level"]] += 1
        at_target += st["level"] >= target
        mastered += st["mastered"]
        due += st["due"]
        lapsed += st["lapsed"]
        if st["level"] < target:
            gaps.append((-(w * (target - st["level"])), rec.topics[tid].get("title"), st["level"], target, w))
    gaps.sort()
    return {"course": course, "concepts": len(concepts), "l4_targets": sum(1 for c in concepts if c[1] >= 4),
            "counts": counts, "at_target": at_target, "mastered": mastered, "due": due, "lapsed": lapsed,
            "gaps": [{"title": g[1], "level": g[2], "target": g[3], "weight": g[4]} for g in gaps[:8]]}


def report_text(rec, only=None):
    profile = rec.profile
    order = {"now": 0, "next": 1, "done": 2}
    courses = [only] if only else sorted(profile.get("courses", {}), key=lambda c: (order.get(profile["courses"][c], 3), c))
    out = [f"# Where {profile.get('handle', 'the learner')} stands", "",
           f"Generated on {rec.today} by `python3 scripts/learner.py report`. Do not edit: it is rebuilt from evidence.jsonl.", ""]
    exams = {(e.get("course"), e.get("name")): e.get("date") for e in profile.get("exams", []) or []}
    for course in courses:
        status = profile.get("courses", {}).get(course, "")
        out.append(f"## {course}" + (f" ({status})" if status else ""))
        out.append("")
        if course not in rec.curricula:
            out += ["No curriculum for this course yet, so there is no target to measure against.", ""]
            continue
        s = course_summary(rec, course)
        for (c, name), date in sorted(exams.items(), key=lambda x: x[1]):
            if c == course and date >= rec.today:
                out.append(f"{name} on {date}: {(day(date) - day(rec.today)).days} days away.")
        pct = round(100 * s["at_target"] / s["concepts"]) if s["concepts"] else 0
        out += [f"Target: L4 on {s['l4_targets']} concepts and L3 on {s['concepts'] - s['l4_targets']}. "
                f"At target: {s['at_target']} of {s['concepts']} ({pct}%). Mastered: {s['mastered']}. "
                f"Due for review: {s['due']}. Lapsed: {s['lapsed']}.", "",
                "| Level | L0 | L1 | L2 | L3 | L4 | L5 |", "|---|---|---|---|---|---|---|",
                "| Concepts | " + " | ".join(str(n) for n in s["counts"]) + " |", ""]
        if s["gaps"]:
            out += ["Heaviest gaps first:", ""]
            out += [f"- {g['title']}: L{g['level']}, target L{g['target']}, weight {g['weight']:g}" for g in s["gaps"]]
            out.append("")
    cal = calibration(rec.events)
    out += ["## Calibration", ""]
    if cal["answers"] < 5:
        out += [f"{cal['answers']} answers with a stated confidence so far. The table appears after five.", ""]
    else:
        out += ["Confidence is what you said before answering. Right is how the answers in that band came out. "
                "They should match.", "", "| Confidence | Answers | Mean confidence | Right |", "|---|---|---|---|"]
        out += [f"| {b['band']} | {b['answers']} | {b['confidence']}% | {b['right']}% |" for b in cal["bands"]]
        out += ["", f"Brier score: {cal['brier']} (0 is perfect, 0.25 is what guessing 50% every time gives).", ""]
    open_missteps = [(st["misstep"]["date"], rec.topics[tid].get("title"), st["misstep"]["text"])
                     for tid, st in rec.states.items() if st["misstep"]]
    if open_missteps:
        out += ["## Open missteps", "", "The first step where the reasoning went wrong, not yet answered right since.", ""]
        out += [f"- {title} ({date}): {text}" for date, title, text in sorted(open_missteps, reverse=True)]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def write_generated(rec):
    """Rebuild state.json, levels.js and progress.md from the record."""
    targets = {}
    for course, status in rec.profile.get("courses", {}).items():
        if status in ("now", "next"):
            for tid, target, _, _ in rec.concepts(course):
                targets[tid] = max(targets.get(tid, 0), target)
    topics = {}
    for tid, st in sorted(rec.states.items()):
        topics[tid] = {k: st[k] for k in ("level", "earned", "next_review", "interval", "due", "lapsed",
                                          "mastered", "regain", "last", "answers", "progress")}
        if st["misstep"]:
            topics[tid]["misstep"] = st["misstep"]["text"]
    state = {"generated": rec.today, "handle": rec.profile.get("handle"), "topics": topics}
    (rec.folder / "state.json").write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    levels = {tid: {"level": st["level"], "due": st["due"], "mastered": st["mastered"]} for tid, st in sorted(rec.states.items())}
    for tid, target in targets.items():
        levels.setdefault(tid, {"level": 0, "due": False, "mastered": False})["target"] = target
    js = ("// Generated by scripts/learner.py. The map (index.html) reads this to colour topics by level.\n"
          "window.MOMENTOS_LEARNER = " + json.dumps({"handle": rec.profile.get("handle"), "generated": rec.today,
                                                    "levels": levels}, ensure_ascii=False, sort_keys=True) + ";\n")
    (rec.folder / "levels.js").write_text(js, encoding="utf-8")
    (rec.folder / "progress.md").write_text(report_text(rec), encoding="utf-8")


def commit(folder, message):
    if not (folder / ".git").exists() or not shutil.which("git"):
        return
    subprocess.run(["git", "-C", str(folder), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(folder), "commit", "-q", "-m", message], capture_output=True)


# --------------------------------------------------------------------------------------- commands

def need_record(folder):
    if not (folder / "profile.md").is_file():
        sys.exit(f"There is no learner record at {m.rel(folder)}/. Start one with: python3 scripts/learner.py init <handle>")


def cmd_init(args, folder):
    if folder.exists() and any(folder.iterdir()):
        sys.exit(f"{m.rel(folder)}/ already holds a record. Nothing was changed.")
    if not HANDLE.match(args.handle):
        sys.exit("A handle is lowercase letters, digits and hyphens, at most 32 characters. No names, no emails.")
    folder.mkdir(parents=True, exist_ok=True)
    for src in sorted(TEMPLATE.iterdir()):
        name = ".gitignore" if src.name == "dot-gitignore" else src.name
        text = src.read_text(encoding="utf-8")
        if src.name == "profile.md":
            text = text.replace('"handle": ""', f'"handle": "{args.handle}"').replace('"started": ""', f'"started": "{args.today}"')
        (folder / name).write_text(text, encoding="utf-8")
    (folder / "evidence.jsonl").write_text("", encoding="utf-8")
    if shutil.which("git"):
        subprocess.run(["git", "init", "-q", str(folder)], capture_output=True)
        subprocess.run(["git", "-C", str(folder), "config", "user.name", args.handle], capture_output=True)
        subprocess.run(["git", "-C", str(folder), "config", "user.email", f"{args.handle}@momentos.invalid"], capture_output=True)
        commit(folder, "start the record")
    print(f"Started a record for {args.handle} in {m.rel(folder)}/. It is ignored by the shared repo and is its own git repository.")
    print("Next: fill in learner/profile.md (your courses), then ask for the onboarding quiz.")


def append_events(folder, events, today):
    ids = {t.get("id") for t in m.load_map([])["topics"]}
    renames = m.load_renames([])
    existing = read_events(folder, [])
    last = max([e.get("date", "") for e in existing if is_date(e.get("date", ""))] or [""])
    bad = []
    for n, event in enumerate(events, 1):
        event.setdefault("help", "none")
        event.setdefault("confidence", None)
        event.setdefault("misstep", None)
        for text in event_problems(event, ids, renames):
            bad.append(f"event {n}: {text}")
        if is_date(event.get("date", "")) and event["date"] > today:
            bad.append(f"event {n}: is dated in the future")
        if is_date(event.get("date", "")) and event["date"] < last:
            bad.append(f"event {n}: is dated {event['date']}, before the newest event already recorded ({last})")
    if bad:
        sys.exit("Nothing was recorded:\n  " + "\n  ".join(bad))
    order = ("date", "topic", "kind", "aim", "shows", "help", "confidence", "asked", "note", "misstep", "by", "session")
    with open(folder / "evidence.jsonl", "a", encoding="utf-8") as f:
        for event in events:
            clean = {k: event[k] for k in order if k in event}
            clean["topic"] = m.resolve_id(clean["topic"], renames)
            f.write(json.dumps(clean, ensure_ascii=False) + "\n")


def after_write(folder, today, touched, message):
    rec = Record(folder, today)
    write_generated(rec)
    commit(folder, message)
    for tid in touched:
        st = rec.state(tid)
        aim, kind, why = next_step(st)
        review = f", next review {st['next_review']}" if st["next_review"] else ""
        print(f"{tid}: L{st['level']}{' (mastered)' if st['mastered'] else ''}{review}. Next: a {kind} question at L{aim}. {why}.")


def cmd_add(args, folder):
    need_record(folder)
    event = {"date": args.date or args.today, "topic": args.topic, "kind": args.kind, "shows": args.shows}
    if args.kind != "self":
        event.update(aim=args.aim, help=args.help_given, confidence=args.confidence, asked=args.asked, note=args.note,
                     misstep=args.misstep)
    event["by"] = args.by
    if args.session:
        event["session"] = args.session
    append_events(folder, [event], args.today)
    after_write(folder, args.today, [m.resolve_id(args.topic, m.load_renames([]))], f"evidence: {args.topic} ({args.kind})")


def cmd_paste(args, folder):
    need_record(folder)
    lines = sys.stdin.read().splitlines()
    if any(line.strip() == BLOCK_START for line in lines):
        start = next(i for i, line in enumerate(lines) if line.strip() == BLOCK_START)
        lines = lines[start + 1:]
    events = []
    for line in lines:
        text = line.strip().strip("`")
        if text == BLOCK_END:
            break
        if not text:
            continue
        try:
            event = json.loads(text)
        except json.JSONDecodeError:
            sys.exit(f"Nothing was recorded: this line is not JSON:\n  {line}")
        event.setdefault("by", "chat")
        events.append(event)
    if not events:
        sys.exit("Nothing was recorded: no events found. A block is JSON lines between 'momentos-evidence v1' and 'end'.")
    append_events(folder, events, args.today)
    touched = sorted({m.resolve_id(e["topic"], m.load_renames([])) for e in events})
    after_write(folder, args.today, touched, f"evidence: {len(events)} answers pasted")


def cmd_next(args, folder):
    need_record(folder)
    rec = Record(folder, args.today)
    n = args.n or rec.profile.get("session_size", 8)
    if args.topic:
        items = queue_topic(rec, args.topic, n)
    elif args.exam:
        parts = args.exam.rsplit(" ", 1)
        if len(parts) != 2:
            sys.exit('Write the exam as course then name, for example --exam "EE 105 FINAL".')
        items = queue_course(rec, parts[0], n, parts[1].upper())
    elif args.course:
        items = queue_course(rec, args.course, n)
    else:
        items = queue_due(rec, n)
    print(json.dumps({"today": args.today, "handle": rec.profile.get("handle"), "questions": items}, indent=1, ensure_ascii=False))


def cmd_report(args, folder):
    need_record(folder)
    rec = Record(folder, args.today)
    write_generated(rec)
    print(report_text(rec, args.course), end="")


def cmd_show(args, folder):
    need_record(folder)
    rec = Record(folder, args.today)
    tid = m.resolve_id(args.topic, rec.renames)
    if tid not in rec.topics:
        sys.exit(f"{args.topic!r} is not a topic on the map.")
    st = rec.state(tid)
    aim, kind, why = next_step(st)
    print(f"{rec.topics[tid].get('title')} ({tid}): L{st['level']}, highest earned L{st['earned']}"
          + (", mastered" if st["mastered"] else "") + (", lapsed" if st["lapsed"] else ""))
    if st["next_review"]:
        print(f"Next review: {st['next_review']}" + (" (due)" if st["due"] else ""))
    print(f"Next step: a {kind} question at L{aim}. {why}.")
    if st["misstep"]:
        print(f"Open misstep ({st['misstep']['date']}): {st['misstep']['text']}")
    for e in rec.by_topic.get(tid, []):
        if e["kind"] == "self":
            print(f"  {e['date']}  self-rating L{e['shows']}")
        else:
            conf = "" if e.get("confidence") is None else f", confidence {e['confidence']:g}"
            print(f"  {e['date']}  {e['kind']} at L{e['aim']}, showed L{e['shows']}, help {e.get('help', 'none')}{conf}: {e['asked']}")
            print(f"              {e['note']}")


def cmd_export(args, folder):
    need_record(folder)
    rec = Record(folder, args.today)
    n = args.n or rec.profile.get("session_size", 8)
    items = queue_topic(rec, args.topic, n) if args.topic else queue_course(rec, args.course, n) if args.course else queue_due(rec, n)
    protocol = ROOT / "prompts" / "quiz-in-chat.md"
    print(protocol.read_text(encoding="utf-8").rstrip() if protocol.is_file() else "(prompts/quiz-in-chat.md is missing)")
    print("\n---\n\n## The learner\n")
    print(f"Handle: {rec.profile.get('handle')}. Today is {args.today}.\n")
    print(rec.about or "(no profile prose)")
    print("\n## The questions to ask, in this order\n")
    print("```json")
    print(json.dumps(items, indent=1, ensure_ascii=False))
    print("```")


def cmd_check(args, folder):
    need_record(folder)
    problems = check_record(folder)
    for text in problems:
        print("  ERROR    " + text)
    print("The record is valid." if not problems else f"{len(problems)} problem(s).")
    return 1 if problems else 0


def cmd_selftest(args, folder):
    def ev(date, kind, aim, shows, help_="none"):
        return {"date": date, "topic": "t", "kind": kind, "aim": aim, "shows": shows, "help": help_}

    def level(events, today):
        return topic_state(events, today)["level"]

    l3 = [ev("2026-01-01", "predict", 3, 3), ev("2026-01-02", "predict", 3, 3), ev("2026-01-02", "explain", 3, 3)]
    l4 = l3 + [ev("2026-01-03", "transfer", 4, 4), ev("2026-01-03", "limit", 4, 4)]
    cases = [
        ("a self-rating alone stops at L1", level([{"date": "2026-01-01", "topic": "t", "kind": "self", "shows": 4}], "2026-01-01"), 1),
        ("one answer showing L2 is not yet L2", level([ev("2026-01-01", "compute", 2, 2)], "2026-01-01"), 1),
        ("two answers showing L2 make L2", level([ev("2026-01-01", "compute", 2, 2)] * 2, "2026-01-01"), 2),
        ("one answer showing L3 makes L2", level([ev("2026-01-01", "predict", 3, 3)], "2026-01-01"), 2),
        ("two predictions on one day are not L3", level([ev("2026-01-01", "predict", 3, 3)] * 2 + [ev("2026-01-01", "explain", 3, 3)], "2026-01-01"), 2),
        ("predictions on two days plus an explanation make L3", level(l3, "2026-01-02"), 3),
        ("a hinted answer does not count", level(l3[:2] + [ev("2026-01-02", "explain", 3, 3, "hint")], "2026-01-02"), 2),
        ("a transfer problem and a limit answer make L4", level(l4, "2026-01-03"), 4),
        ("L4 is not mastered on the day", topic_state(l4, "2026-01-03")["mastered"], False),
        ("L4 held at a review a week later is mastered", topic_state(l4 + [ev("2026-01-10", "transfer", 4, 4)], "2026-01-10")["mastered"], True),
        ("a failed review drops one level", level(l4 + [ev("2026-01-06", "transfer", 4, 2)], "2026-01-06"), 3),
        ("a clean answer on a later day wins it back", level(l4 + [ev("2026-01-06", "transfer", 4, 2), ev("2026-01-07", "transfer", 4, 4)], "2026-01-07"), 4),
        ("a clean answer the same day does not", level(l4 + [ev("2026-01-06", "transfer", 4, 2), ev("2026-01-06", "transfer", 4, 4)], "2026-01-06"), 3),
        ("the first review is 3 days out", topic_state(l3, "2026-01-02")["next_review"], "2026-01-05"),
        ("a passed review moves to 7 days", topic_state(l3 + [ev("2026-01-05", "predict", 3, 3)], "2026-01-05")["next_review"], "2026-01-12"),
        ("a review overdue by a week is only due", level(l3, "2026-01-12"), 3),
        ("a review overdue by more than a week costs a level", level(l3, "2026-01-13"), 2),
        ("a lapse never goes below L2", level(l3, "2027-01-01"), 2),
        ("one clean answer after a lapse restores the level", level(l3 + [ev("2026-03-01", "predict", 3, 3)], "2026-03-01"), 3),
    ]
    failed = [f"{name}: got {got!r}, expected {want!r}" for name, got, want in cases if got != want]
    for line in failed:
        print("  FAIL  " + line)
    print(f"{len(cases) - len(failed)} of {len(cases)} level-rule scenarios pass.")
    return 1 if failed else 0


def main():
    p = argparse.ArgumentParser(description="The learner's record. See docs/learner-record.md.")
    p.add_argument("--dir", help="the record's folder (default: learner/, or $MOMENTOS_LEARNER)")
    p.add_argument("--today", help="pretend today is this date, YYYY-MM-DD (for testing)")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("init"); s.add_argument("handle")
    s = sub.add_parser("add")
    s.add_argument("--topic", required=True); s.add_argument("--kind", required=True, choices=KINDS)
    s.add_argument("--aim", type=int); s.add_argument("--shows", type=int, required=True)
    s.add_argument("--help-given", default="none", choices=HELP); s.add_argument("--confidence", type=float)
    s.add_argument("--asked"); s.add_argument("--note"); s.add_argument("--misstep")
    s.add_argument("--by", default="unknown"); s.add_argument("--date"); s.add_argument("--session")
    sub.add_parser("paste")
    for name in ("next", "export"):
        s = sub.add_parser(name)
        s.add_argument("--course"); s.add_argument("--topic"); s.add_argument("-n", type=int)
        if name == "next":
            s.add_argument("--due", action="store_true"); s.add_argument("--exam")
    s = sub.add_parser("report"); s.add_argument("--course")
    s = sub.add_parser("show"); s.add_argument("topic")
    sub.add_parser("check"); sub.add_parser("selftest")
    args = p.parse_args()
    args.today = args.today or datetime.date.today().isoformat()
    if not is_date(args.today):
        sys.exit("--today must be YYYY-MM-DD.")
    folder = Path(args.dir or os.environ.get("MOMENTOS_LEARNER") or ROOT / "learner")
    commands = {"init": cmd_init, "add": cmd_add, "paste": cmd_paste, "next": cmd_next, "report": cmd_report,
                "show": cmd_show, "export": cmd_export, "check": cmd_check, "selftest": cmd_selftest}
    return commands[args.command](args, folder) or 0


if __name__ == "__main__":
    sys.exit(main())
