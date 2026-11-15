#!/usr/bin/env python3
"""Run every check in the repo. This is the one command to run before a commit.

    python3 scripts/check.py              every section
    python3 scripts/check.py map tools    only the sections named

Sections:

  generated  the generated files match their sources (scripts/build.py --check)
  map        map/<folder>.json: topics, links, renames, and the tool files on disk
  tools      every tool follows the rules in docs/tools.md
  style      every tool carries the house-style block of templates/tool-template.html
  tests      every tool's maths passes its check cases (node scripts/test-tools.js)
  plans      plans/*.md: fields, sections, vague words, check cases against their reference script
  curricula  curricula/*.json and the course registry
  rubrics    rubrics/<folder>.json
  skills     .claude/skills/*/SKILL.md, and the paths that instruction files point at
  docs       links between markdown files resolve
  learner    templates/learner/, and learner/ if this checkout has one
  personal   no email address or git user name in a tracked file
  leaks      no long run of words from course-materials/ in a tracked file (only where that folder exists)

Exit code 0 means no errors. Warnings do not fail. Standard library only.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import momentos as m  # noqa: E402
import build  # noqa: E402

ROOT = m.ROOT
TOPIC_FIELDS = {"id", "title", "essence", "check", "tools", "later", "courses", "folder", "_file"}
QUESTION_KINDS = ("recall", "compute", "predict", "explain", "sketch", "limit", "connect", "transfer", "derive")
FLAGS = {"old-exams-only", "reader-only", "not-yet-assessed", "lab-only"}
CASE_TAGS = {"typical", "limit-zero", "limit-infinity", "breaks", "sign", "other"}
STUB_SECTIONS = {"tool": ["Concept", "Picture", "Interaction", "Misconception"],
                 "quiz-only": ["Concept", "Why no tool", "Misconception"]}
FULL_SECTIONS = {"tool": ["Concept", "Picture", "Interaction", "Maths", "Check cases", "Predict, then try",
                          "Misconceptions", "Quiz hooks", "Where this shows up", "Page text", "Acceptance checklist"],
                 "quiz-only": ["Concept", "Why no tool", "Misconceptions", "Quiz hooks", "Where this shows up"]}
VAGUE = re.compile(r"\b(etc\b\.?|and so on|maybe|perhaps|as appropriate|as needed|if desired|if you like|or similar|"
                   r"something like|TBD|to be decided|optionally|should probably)", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
EMAIL_OK = {"noreply@anthropic.com"}
TEXT_SUFFIXES = {".md", ".html", ".json", ".py", ".js", ".yml", ".yaml", ".txt", ".css", ""}


class Report:
    def __init__(self):
        self.errors, self.warnings, self.notes = [], [], []

    def error(self, text):
        self.errors.append(text)

    def warn(self, text):
        self.warnings.append(text)

    def note(self, text):
        self.notes.append(text)


def topic_ids():
    return {t.get("id") for t in m.load_map([])["topics"]}


# --------------------------------------------------------------------------------------- generated

def check_generated(r):
    problems = []
    outputs = build.build_all(problems)
    for message in problems:
        r.error(message)
    for name in build.stale(outputs):
        r.error(f"{name} is out of date. Run: python3 scripts/build.py")
    r.note(f"{len(outputs)} generated files")


# --------------------------------------------------------------------------------------------- map

def check_map(r):
    problems = []
    data = m.load_map(problems)
    renames = m.load_renames(problems)
    for message in problems:
        r.error(message)
    topics, links = data["topics"], data["links"]
    courses = {c.get("id") for c in m.load_courses([])}
    with_curriculum = {c.get("course") for c in m.load_curricula([])}
    ids, registered, file_of = set(), set(), {}
    for n, topic in enumerate(topics, 1):
        name = topic.get("id") or f"topic number {n} in {topic['_file']}"
        for field in ("id", "title", "essence", "check"):
            if not str(topic.get(field, "")).strip():
                r.error(f"{name}: has no {field}.")
        for key in topic:
            if key not in TOPIC_FIELDS:
                r.error(f"{name}: unknown field {key}. The fields are listed in docs/map.md.")
        tid = topic.get("id", "")
        if tid:
            if not m.KEBAB.match(tid):
                r.error(f"{tid}: the id should be lowercase words joined by hyphens.")
            if tid in ids:
                r.error(f"{tid}: this id is used more than once.")
            ids.add(tid)
            file_of[tid] = topic["_file"]
        if topic["folder"].split("/")[0] not in m.TOP_FOLDERS:
            r.error(f"{name}: {topic['folder']} is not under one of {', '.join(m.TOP_FOLDERS)}. See docs/map.md.")
        tools = topic.get("tools", [])
        if not isinstance(tools, list):
            r.error(f"{name}: tools must be a list of paths.")
            tools = []
        for tool in tools:
            registered.add(tool)
            if not (ROOT / tool).is_file():
                r.error(f"{name}: the tool {tool} does not exist.")
        for course in topic.get("courses", []):
            if course in with_curriculum:
                r.error(f"{name}: lists {course} by hand. Courses come from curricula/: add the topic to "
                        f"curricula/{m.course_slug(course)}.json and remove it here.")
        later = topic.get("later", [])
        if not isinstance(later, list):
            r.error(f"{name}: later must be a list of {{course, how}}.")
            later = []
        for item in later:
            if not isinstance(item, dict) or not str(item.get("course", "")).strip() or not str(item.get("how", "")).strip():
                r.error(f"{name}: each entry in later needs a course and a how.")
            elif courses and item["course"] not in courses:
                r.error(f"{name}: later names {item['course']}, which is not in curricula/courses.json.")
        if len(str(topic.get("essence", ""))) > 260:
            r.warn(f"{name}: the essence is {len(topic['essence'])} characters. One or two sentences reads better.")
        if len(str(topic.get("title", ""))) > 44:
            r.warn(f"{name}: the title is long for a label on the map.")

    seen, linked = set(), set()
    for link in links:
        a, b = link.get("from"), link.get("to")
        label = f"link {a} -> {b}"
        if a not in ids:
            r.error(f"{label}: there is no topic called {a}.")
        if b not in ids:
            r.error(f"{label}: there is no topic called {b}.")
        if a == b:
            r.error(f"{label}: a topic cannot link to itself.")
        if (a, b) in seen:
            r.error(f"{label}: this link appears twice.")
        if (b, a) in seen:
            r.warn(f"{label}: the opposite link exists too. One of them is probably enough.")
        seen.add((a, b))
        linked.update((a, b))
        if not str(link.get("why", "")).strip():
            r.error(f"{label}: has no why. The sentence that says what carries over is the point of the link.")
        if b in file_of and link["_file"] != file_of[b]:
            r.error(f"{label}: is stored in {link['_file']} but belongs in {file_of[b]}, the file of the topic it leads to.")
    for tid in sorted(ids - linked):
        r.error(f"{tid}: is not linked to anything. Every topic needs at least one link with a why.")

    for old, new in renames.items():
        if old in ids:
            r.error(f"map/renames.json: {old} is renamed but is still a topic id.")
        if m.resolve_id(old, renames) not in ids:
            r.error(f"map/renames.json: {old} -> {new} does not end at a topic on the map.")

    for path in sorted(m.tool_files() - registered):
        r.error(f"{path}: is in the repo but no topic lists it. Add it to a topic's tools in map/.")
    built = sum(1 for t in topics if t.get("tools"))
    r.note(f"{len(topics)} topics ({built} with a tool), {len(registered)} tools, {len(links)} links, "
           f"{len(m.map_files())} map files")


# ------------------------------------------------------------------------------------------- tools

def registered_tools():
    tools = set()
    for topic in m.load_map([])["topics"]:
        tools.update(t for t in topic.get("tools", []) if isinstance(t, str))
    return sorted(tools)


def check_tools(r):
    ids = topic_ids()
    tools = [t for t in registered_tools() if t.endswith(".html") and (ROOT / t).is_file()]
    for tool in tools:
        text = (ROOT / tool).read_text(encoding="utf-8")
        depth = tool.count("/")

        header = m.tool_header(text)
        for field in ("Concept", "Course", "Play with", "Should click"):
            if not header.get(field):
                r.error(f"{tool}: the comment header has no {field}: line.")
        if "Checked" in header and not header["Checked"]:
            r.error(f"{tool}: the Checked: line is empty. Leave the line out until something has been checked.")
        if header.get("Plan") and not (ROOT / header["Plan"]).is_file():
            r.error(f"{tool}: the header names the plan {header['Plan']}, which does not exist.")

        hrefs = re.findall(r'href="((?:\.\./)*)index\.html#([^"]*)"', text)
        if not re.search(r'href="(?:\.\./)*index\.html#[^"]*"[^>]*>\s*←\s*map\s*<', text):
            r.error(f"{tool}: has no '← map' link to index.html#topic-id.")
        for ups, tid in hrefs:
            if ups.count("../") != depth:
                r.error(f"{tool}: a link to the map uses '{ups}index.html' but the file is {depth} folder(s) deep.")
            if tid not in ids:
                r.error(f"{tool}: links to index.html#{tid}, which is not a topic on the map.")

        if 'id="theme"' not in text:
            r.error(f"{tool}: has no light/dark button (id=\"theme\").")
        for heading in ("What should click", "Predict, then try", "Where this shows up"):
            if not re.search(r"<h2[^>]*>\s*" + re.escape(heading) + r"\s*</h2>", text):
                r.error(f"{tool}: has no '{heading}' section.")
        if len(re.findall(r"<details\b", text)) < 2:
            r.warn(f"{tool}: fewer than two folded answers. A tool needs a few 'Predict, then try' prompts.")

        for pattern, what in ((r"\bfetch\s*\(", "fetch()"), (r'type="module"', "an ES module"),
                              (r"^\s*import\s[^;]*from\s", "an import statement"),
                              (r"<script[^>]+\bsrc=", "a script loaded from another file"),
                              (r'<link[^>]+rel="stylesheet"', "a stylesheet loaded from another file"),
                              (r"@import\b", "a CSS @import"), (r'<(?:img|iframe)[^>]+src="https?:', "a remote image or frame")):
            if re.search(pattern, text, re.M):
                r.error(f"{tool}: uses {what}. A tool is one file with no dependencies.")
        for hit in re.finditer(r"localStorage", text):
            if "try" not in text[max(0, hit.start() - 300):hit.start()]:
                line = text.count("\n", 0, hit.start()) + 1
                r.error(f"{tool}: line {line} uses localStorage outside try/catch. Storage can throw in a preview.")
        if "requestAnimationFrame" in text and "prefers-reduced-motion" not in text:
            r.error(f"{tool}: animates but never asks for prefers-reduced-motion.")
        if "pointerdown" in text and "keydown" not in text:
            r.error(f"{tool}: handles the pointer but not the keyboard.")

        maths = m.script_block(text, "maths")
        if maths is None:
            r.error(f"{tool}: has no <script id=\"maths\"> block. The maths lives there, apart from the drawing.")
        else:
            if not re.search(r"\bvar\s+MATHS\s*=", maths):
                r.error(f"{tool}: the maths block must define `var MATHS = ...`.")
            for word in ("document", "window", "localStorage", "querySelector"):
                if re.search(r"\b" + word + r"\b", maths):
                    r.error(f"{tool}: the maths block mentions {word}. It must not touch the page.")
        cases_text = m.script_block(text, "check-cases")
        if cases_text is None:
            r.error(f"{tool}: has no <script type=\"application/json\" id=\"check-cases\"> block.")
        else:
            try:
                cases = json.loads(cases_text)
            except json.JSONDecodeError as err:
                r.error(f"{tool}: the check cases are not valid JSON ({err.msg}).")
                cases = None
            if cases is not None:
                check_cases_shape(r, tool, cases, need_tags=False)
    r.note(f"{len(tools)} tools")


def check_cases_shape(r, where, cases, need_tags):
    if not isinstance(cases, list) or not cases:
        r.error(f"{where}: the check cases must be a list with at least one case.")
        return
    for n, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            r.error(f"{where}: check case {n} is not an object.")
            continue
        if not isinstance(case.get("fn"), str) or not isinstance(case.get("args"), list) or "expect" not in case:
            r.error(f"{where}: check case {n} needs fn (a name), args (a list) and expect.")
        if not str(case.get("note", "")).strip():
            r.error(f"{where}: check case {n} has no note saying, with units, what is being checked.")
        if "tag" in case and case["tag"] not in CASE_TAGS:
            r.error(f"{where}: check case {n} has the tag {case['tag']}. Use one of {', '.join(sorted(CASE_TAGS))}.")
        if need_tags and "units" not in case:
            r.error(f"{where}: check case {n} has no units (use \"\" for a pure number).")
    if need_tags:
        tags = {c.get("tag") for c in cases if isinstance(c, dict)}
        for tag in ("limit-zero", "limit-infinity", "breaks"):
            if tag not in tags:
                r.error(f"{where}: no check case is tagged {tag}. A plan needs both limits and one case where "
                        "the approximation fails.")


# ------------------------------------------------------------------------------------------- style

def check_style(r):
    if not m.TEMPLATE.exists():
        r.error("templates/tool-template.html is missing.")
        return
    canonical = m.house_style(m.TEMPLATE.read_text(encoding="utf-8"))
    if canonical is None:
        r.error("templates/tool-template.html has no house-style markers.")
        return
    for tool in registered_tools():
        path = ROOT / tool
        if not tool.endswith(".html") or not path.is_file():
            continue
        block = m.house_style(path.read_text(encoding="utf-8"))
        if block is None:
            r.error(f"{tool}: has no house-style markers. Copy the first <style> block of the template.")
        elif block != canonical:
            r.error(f"{tool}: its house-style block differs from the template's. Run: python3 scripts/sync-house-style.py")


# ------------------------------------------------------------------------------------------- tests

def check_tests(r):
    node = shutil.which("node")
    if not node:
        r.warn("node is not installed, so the tools' maths was not tested.")
        return
    done = subprocess.run([node, str(ROOT / "scripts" / "test-tools.js")], capture_output=True, text=True)
    lines = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
    if done.returncode != 0:
        for line in lines[-25:]:
            r.error("test-tools: " + line.strip())
    elif lines:
        r.note(lines[-1].strip())


# ------------------------------------------------------------------------------------------- plans

def close(a, b, tol):
    """Are two JSON values equal, with numbers allowed to differ by tol (absolute, or relative to size)?"""
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k], tol) for k in a)
    return a == b


def strip_fences(text):
    return re.sub(r"```.*?```", lambda hit: "\n" * hit.group(0).count("\n"), text, flags=re.S)


def check_plans(r):
    problems = []
    plans = m.load_plans(problems)
    for message in problems:
        r.error(message)
    ids = topic_ids()
    courses = {c.get("id") for c in m.load_courses([])}
    tools_of = {}
    for topic in m.load_map([])["topics"]:
        tools_of[topic.get("id")] = topic.get("tools", [])
    seen = set()
    for plan in plans:
        where, text = plan["_file"], plan["_text"]
        pid = plan.get("id", "")
        if pid != Path(where).stem:
            r.error(f"{where}: the id {pid!r} must match the file name.")
        if pid in seen:
            r.error(f"{where}: the id {pid} is used twice.")
        seen.add(pid)
        status, kind = plan.get("status"), plan.get("kind")
        if status not in m.PLAN_STATUSES:
            r.error(f"{where}: status must be one of {', '.join(m.PLAN_STATUSES)}.")
            continue
        if kind not in m.PLAN_KINDS:
            r.error(f"{where}: kind must be one of {', '.join(m.PLAN_KINDS)}.")
            continue
        if not str(plan.get("title", "")).strip():
            r.error(f"{where}: has no title.")
        if not plan.get("topics") or not isinstance(plan.get("topics"), list):
            r.error(f"{where}: topics must list at least one map topic id.")
        for field in ("topics", "prerequisites"):
            for tid in plan.get(field, []) or []:
                if tid not in ids:
                    r.error(f"{where}: {field} names {tid}, which is not a topic on the map.")
        for course in plan.get("courses", []) or []:
            if courses and course not in courses:
                r.error(f"{where}: {course} is not in curricula/courses.json.")
        if not plan.get("courses"):
            r.error(f"{where}: courses must list at least one course.")
        tool = plan.get("tool")
        if kind == "tool":
            if plan.get("size") not in ("S", "M", "L"):
                r.error(f"{where}: size must be S, M or L.")
            if not isinstance(tool, str) or not tool.endswith(".html") or tool.split("/")[0] not in m.TOP_FOLDERS:
                r.error(f"{where}: tool must be the path of the .html file to build, inside a topic folder.")
                tool = None
            elif status == "built":
                if not (ROOT / tool).is_file():
                    r.error(f"{where}: status is built but {tool} does not exist.")
                elif not any(tool in tools_of.get(t, []) for t in plan.get("topics", [])):
                    r.error(f"{where}: {tool} is built but none of the plan's topics lists it in map/.")
            elif (ROOT / tool).is_file():
                r.warn(f"{where}: {tool} exists. Set the plan's status to built.")

        want = (STUB_SECTIONS if status == "stub" else FULL_SECTIONS)[kind]
        have = m.plan_sections(text)
        for name in want:
            if name not in have:
                r.error(f"{where}: has no '## {name}' section.")
        if status == "stub":
            continue

        for n, line in enumerate(strip_fences(text).splitlines(), 1):
            hit = VAGUE.search(line)
            if hit:
                r.error(f"{where}: line {n} says '{hit.group(0)}'. A plan leaves no choice open: say exactly what.")
        if kind != "tool":
            continue

        problems = []
        cases = m.plan_cases(text, problems, where)
        for message in problems:
            r.error(message)
        if cases is None:
            r.error(f"{where}: has no ```json check-cases block.")
            continue
        check_cases_shape(r, where, cases, need_tags=True)
        script = plan.get("checks")
        if not isinstance(script, str) or not (ROOT / script).is_file():
            r.error(f"{where}: checks must be the path of the reference script that computes the check cases.")
            continue
        done = subprocess.run([sys.executable, str(ROOT / script)], capture_output=True, text=True)
        if done.returncode != 0:
            r.error(f"{where}: {script} failed: {done.stderr.strip().splitlines()[-1] if done.stderr.strip() else 'no output'}")
            continue
        try:
            computed = json.loads(done.stdout)
        except json.JSONDecodeError:
            r.error(f"{where}: {script} must print the check cases as one JSON list and nothing else.")
            continue
        if len(computed) != len(cases):
            r.error(f"{where}: the plan has {len(cases)} check cases but {script} prints {len(computed)}.")
            continue
        for n, (mine, theirs) in enumerate(zip(cases, computed), 1):
            if mine.get("fn") != theirs.get("fn") or mine.get("args") != theirs.get("args"):
                r.error(f"{where}: check case {n} does not match {script} (fn or args differ).")
            elif not close(mine.get("expect"), theirs.get("expect"), mine.get("tol", 1e-9)):
                r.error(f"{where}: check case {n} expects {mine.get('expect')} but {script} computes {theirs.get('expect')}.")
        if status == "built" and tool and (ROOT / tool).is_file():
            block = m.script_block((ROOT / tool).read_text(encoding="utf-8"), "check-cases")
            try:
                in_tool = json.loads(block) if block else []
            except json.JSONDecodeError:
                in_tool = []
            keys = {json.dumps([c.get("fn"), c.get("args")]): c for c in in_tool if isinstance(c, dict)}
            for n, case in enumerate(cases, 1):
                twin = keys.get(json.dumps([case.get("fn"), case.get("args")]))
                if twin is None:
                    r.error(f"{where}: check case {n} is missing from {tool}. A tool carries every case of its plan.")
                elif not close(twin.get("expect"), case.get("expect"), case.get("tol", 1e-9)):
                    r.error(f"{where}: check case {n} has a different expected value in {tool}.")
    r.note(f"{len(plans)} plans ({sum(1 for p in plans if p.get('status') == 'stub')} stubs, "
           f"{sum(1 for p in plans if p.get('status') == 'planned')} planned, "
           f"{sum(1 for p in plans if p.get('status') == 'built')} built)")


# --------------------------------------------------------------------------------------- curricula

def check_curricula(r):
    problems = []
    courses = m.load_courses(problems)
    curricula = m.load_curricula(problems)
    renames = m.load_renames([])
    for message in problems:
        r.error(message)
    ids = topic_ids()
    known = set()
    for course in courses:
        cid = course.get("id", "")
        if not cid:
            r.error("curricula/courses.json: a course has no id.")
            continue
        if cid in known:
            r.error(f"curricula/courses.json: {cid} is listed twice.")
        known.add(cid)
        for field in ("catalog", "title", "checked"):
            if not str(course.get(field, "")).strip():
                r.error(f"curricula/courses.json: {cid} has no {field}.")
        if not str(course.get("url", "")).startswith("http"):
            r.error(f"curricula/courses.json: {cid} needs the url of its catalog entry.")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(course.get("checked", ""))):
            r.error(f"curricula/courses.json: {cid}: checked must be the date the catalog was read, as YYYY-MM-DD.")
    concepts_total = 0
    for cur in curricula:
        where = cur["_file"]
        cid = cur.get("course", "")
        if cid not in known:
            r.error(f"{where}: the course {cid!r} is not in curricula/courses.json.")
        if Path(where).name != m.course_slug(cid) + ".json":
            r.error(f"{where}: the file for {cid} must be called {m.course_slug(cid)}.json.")
        tier = cur.get("tier")
        if tier not in (1, 2, 3, 4):
            r.error(f"{where}: tier must be 1, 2, 3 or 4.")
        if cur.get("scope_term") and m.scope_year(cur) is None:
            r.error(f"{where}: scope_term must look like FA26 or SP24.")
        units = [u.get("id") for u in cur.get("units", [])]
        if len(units) != len(set(units)):
            r.error(f"{where}: two units share an id.")
        for source in cur.get("sources", []):
            if not str(source.get("title", "")).strip():
                r.error(f"{where}: a source has no title.")
            if source.get("url") and (not str(source["url"]).startswith("http") or not source.get("accessed")):
                r.error(f"{where}: the source {source.get('title')} needs an http url and an accessed date.")
        seen = set()
        for concept in cur.get("concepts", []):
            tid = concept.get("topic", "")
            concepts_total += 1
            if tid not in ids:
                new = m.resolve_id(tid, renames)
                r.error(f"{where}: {tid} is not a topic on the map" + (f" (it was renamed to {new})." if new != tid else "."))
            if tid in seen:
                r.error(f"{where}: {tid} is listed twice.")
            seen.add(tid)
            if concept.get("unit") not in units:
                r.error(f"{where}: {tid} names the unit {concept.get('unit')!r}, which is not in units.")
            if concept.get("target") not in (3, 4, 5):
                r.error(f"{where}: {tid}: target must be 3, 4 or 5.")
            for text in concept.get("assessed", []):
                if m.parse_assessed(text) is None:
                    r.error(f"{where}: {tid}: cannot read the identifier {text!r}. Write it like 'FA24 MT1 Q3'.")
            for flag in concept.get("flags", []):
                if flag not in FLAGS:
                    r.error(f"{where}: {tid}: unknown flag {flag}. Use one of {', '.join(sorted(FLAGS))}.")
    r.note(f"{len(courses)} courses in the registry, {len(curricula)} curricula, {concepts_total} concepts")


# ----------------------------------------------------------------------------------------- rubrics

def check_rubrics(r):
    data = m.load_map([])
    folder_of = {t.get("id"): t["folder"] for t in data["topics"]}
    have = set()
    if m.RUBRICS_DIR.is_dir():
        for path in sorted(m.RUBRICS_DIR.rglob("*.json")):
            problems = []
            entries = m.read_json(path, problems)
            for message in problems:
                r.error(message)
            if not isinstance(entries, dict):
                continue
            folder = path.relative_to(m.RUBRICS_DIR).with_suffix("").as_posix()
            for tid, entry in entries.items():
                where = f"{m.rel(path)}: {tid}"
                if tid not in folder_of:
                    r.error(f"{where}: is not a topic on the map.")
                    continue
                if folder_of[tid] != folder:
                    r.error(f"{where}: belongs in rubrics/{folder_of[tid]}.json, next to its map file.")
                have.add(tid)
                for level in ("L1", "L2", "L3", "L4"):
                    if not isinstance(entry, dict) or not str(entry.get(level, "")).strip():
                        r.error(f"{where}: has no {level} descriptor.")
                if not isinstance(entry, dict):
                    continue
                if not isinstance(entry.get("missteps", []), list):
                    r.error(f"{where}: missteps must be a list.")
                for kind in entry.get("seeds", {}) or {}:
                    if kind not in QUESTION_KINDS:
                        r.error(f"{where}: seeds has the kind {kind}. Use one of {', '.join(QUESTION_KINDS)}.")
    need = set()
    for cur in m.load_curricula([]):
        if cur.get("tier") == 1:
            need.update(c.get("topic") for c in cur.get("concepts", []))
    missing = sorted(need - have)
    if missing:
        r.warn(f"{len(missing)} tier 1 topics have no level descriptors in rubrics/ yet "
               f"(first few: {', '.join(missing[:5])}).")
    r.note(f"{len(have)} topics with level descriptors")


# ------------------------------------------------------------------------- skills and instructions

PATH_IN_TICKS = re.compile(r"`((?:scripts|docs|map|plans|curricula|rubrics|templates|prompts|\.claude|\.github)/[^`\s]*)`")


def instruction_files():
    files = [ROOT / name for name in ("README.md", "AGENTS.md", "CLAUDE.md")]
    for folder in ("docs", "prompts", "plans", "curricula", "templates", ".claude", ".github"):
        if (ROOT / folder).is_dir():
            files += sorted((ROOT / folder).rglob("*.md"))
    return [f for f in files if f.is_file()]


def check_skills(r):
    skills = ROOT / ".claude" / "skills"
    count = 0
    if skills.is_dir():
        for folder in sorted(p for p in skills.iterdir() if p.is_dir()):
            path = folder / "SKILL.md"
            if not path.is_file():
                r.error(f"{m.rel(folder)}: has no SKILL.md.")
                continue
            count += 1
            text = path.read_text(encoding="utf-8")
            front = re.match(r"---\n(.*?)\n---\n", text, re.S)
            if not front:
                r.error(f"{m.rel(path)}: must start with a front-matter block giving name and description.")
                continue
            name = re.search(r"^name:\s*(.+)$", front.group(1), re.M)
            desc = re.search(r"^description:\s*(.+)$", front.group(1), re.M)
            if not name or name.group(1).strip() != folder.name:
                r.error(f"{m.rel(path)}: name must be {folder.name}.")
            if not desc or len(desc.group(1).strip()) < 30:
                r.error(f"{m.rel(path)}: the description must say when to use the skill.")
            for heading in ("## Steps", "## Checks", "## Done means"):
                if heading not in text:
                    r.error(f"{m.rel(path)}: has no '{heading}' section.")
    for name in ("AGENTS.md", "CLAUDE.md"):
        if not (ROOT / name).is_file():
            r.error(f"{name} is missing.")
    claude = ROOT / "CLAUDE.md"
    if claude.is_file() and "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
        r.error("CLAUDE.md must import AGENTS.md (a line with @AGENTS.md), so the rules live in one place.")
    for path in instruction_files():
        for hit in PATH_IN_TICKS.finditer(path.read_text(encoding="utf-8")):
            target = hit.group(1).rstrip(".,:;)")
            if any(ch in target for ch in "<>*{}$") or target.endswith("/..."):
                continue
            if not (ROOT / target).exists():
                r.error(f"{m.rel(path)}: mentions `{target}`, which does not exist.")
    r.note(f"{count} skills")


def check_docs(r):
    link = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    count = 0
    for path in instruction_files():
        text = strip_fences(path.read_text(encoding="utf-8"))
        for hit in link.finditer(text):
            target = hit.group(1)
            if re.match(r"^(https?:|mailto:|#)", target) or target.startswith("<"):
                continue
            count += 1
            file_part = target.split("#")[0]
            if file_part and not (path.parent / file_part).exists():
                r.error(f"{m.rel(path)}: links to {target}, which does not exist.")
    r.note(f"{count} links between files")


# ----------------------------------------------------------------------------------------- learner

def check_learner(r):
    try:
        import learner
    except ImportError:
        r.error("scripts/learner.py is missing.")
        return
    done = subprocess.run([sys.executable, str(ROOT / "scripts" / "learner.py"), "selftest"], capture_output=True, text=True)
    if done.returncode != 0:
        for line in done.stdout.splitlines():
            r.error("learner.py selftest: " + line.strip())
    else:
        r.note(done.stdout.strip().splitlines()[-1])
    template = ROOT / "templates" / "learner"
    if not template.is_dir():
        r.error("templates/learner/ is missing: it is what a new learner's record is copied from.")
    else:
        for message in learner.check_record(template, template=True):
            r.error("templates/learner: " + message)
    mine = ROOT / "learner"
    if mine.is_dir():
        problems = learner.check_record(mine, template=False)
        for message in problems:
            r.error("learner: " + message)
        r.note("this checkout has a learner record" + ("" if problems else ", and it is valid"))
    else:
        r.note("no learner record in this checkout (start one with: python3 scripts/learner.py init <handle>)")


# ---------------------------------------------------------------------------- personal and leaks

def tracked_files():
    try:
        done = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return None
    if done.returncode != 0:
        return None
    return [ROOT / line for line in done.stdout.splitlines() if line.strip()]


def git_config(key):
    try:
        done = subprocess.run(["git", "config", key], cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return ""
    return done.stdout.strip() if done.returncode == 0 else ""


def text_of(path):
    if path.suffix.lower() not in TEXT_SUFFIXES or not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def check_personal(r):
    files = tracked_files()
    if files is None:
        r.warn("git is not available here, so tracked files were not scanned for personal details.")
        return
    name, email = git_config("user.name"), git_config("user.email")
    for path in files:
        text = text_of(path)
        if text is None:
            continue
        for hit in sorted(set(EMAIL.findall(text)) - EMAIL_OK):
            if hit.lower() == email.lower() or not hit.lower().endswith((".png", ".svg")):
                r.error(f"{m.rel(path)}: contains an email address. Tracked files carry no personal details.")
                break
        if len(name) >= 6 and name.lower() in text.lower():
            r.error(f"{m.rel(path)}: contains the git user's name. Tracked files carry no personal details.")


def words_of(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def check_leaks(r, run=12):
    materials = ROOT / "course-materials"
    if not materials.is_dir():
        r.note("no course-materials/ here, so nothing to compare against")
        return
    files = tracked_files()
    if files is None:
        r.warn("git is not available here, so tracked files were not compared with course-materials/.")
        return
    seen = set()
    for path in materials.rglob("*.md"):
        try:
            words = words_of(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
        for i in range(len(words) - run + 1):
            seen.add(hash(tuple(words[i:i + run])))
    hits = 0
    for path in files:
        text = text_of(path)
        if text is None:
            continue
        words = words_of(text)
        for i in range(len(words) - run + 1):
            if hash(tuple(words[i:i + run])) in seen:
                r.error(f"{m.rel(path)}: shares a run of {run} words with course-materials/: "
                        f"\"{' '.join(words[i:i + run])}\". Nothing is copied from the course materials.")
                hits += 1
                break
    r.note(f"compared {len(files)} tracked files with course-materials/ ({hits} overlaps)")


# ------------------------------------------------------------------------------------------ run it

SECTIONS = [("generated", check_generated), ("map", check_map), ("tools", check_tools), ("style", check_style),
            ("tests", check_tests), ("plans", check_plans), ("curricula", check_curricula), ("rubrics", check_rubrics),
            ("skills", check_skills), ("docs", check_docs), ("learner", check_learner), ("personal", check_personal),
            ("leaks", check_leaks)]


def main():
    wanted = [a for a in sys.argv[1:] if not a.startswith("-")]
    unknown = [a for a in wanted if a not in dict(SECTIONS)]
    if unknown:
        sys.exit(f"Unknown section: {', '.join(unknown)}. Sections: {', '.join(name for name, _ in SECTIONS)}.")
    errors = warnings = 0
    for name, fn in SECTIONS:
        if wanted and name not in wanted:
            continue
        r = Report()
        fn(r)
        status = "FAIL" if r.errors else "ok"
        print(f"{name:<10} {status:<5} {'; '.join(r.notes)}")
        for message in r.warnings:
            print("  warning  " + message)
        for message in r.errors:
            print("  ERROR    " + message)
        errors += len(r.errors)
        warnings += len(r.warnings)
    print()
    if errors:
        print(f"{errors} error(s), {warnings} warning(s). Fix the errors before committing.")
        return 1
    print(f"All checks pass ({warnings} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
