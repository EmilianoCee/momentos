"""Shared helpers for the momentos scripts. Standard library only.

Everything that reads the repo's source files lives here, so that build.py, check.py and learner.py
agree on what a topic, a curriculum and a plan are. The formats are documented in docs/.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_DIR = ROOT / "map"
CURRICULA_DIR = ROOT / "curricula"
PLANS_DIR = ROOT / "plans"
RUBRICS_DIR = ROOT / "rubrics"
INDEX = ROOT / "index.html"
README = ROOT / "README.md"
TEMPLATE = ROOT / "templates" / "tool-template.html"

# The top-level folders a topic may live in. The rule for choosing one is in docs/map.md.
TOP_FOLDERS = ("maths", "physics", "signals", "systems", "circuits", "devices", "unspecified")
# Files with these endings, inside a topic folder, count as tools and must be on the map.
TOOL_SUFFIXES = {".html", ".py", ".ipynb", ".m", ".asc"}

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAP_BLOCK = re.compile(r'(<script type="application/json" id="map-data">)(.*?)(</script>)', re.S)

TOPIC_KEYS = ("id", "title", "essence", "check", "tools", "later")
LINK_KEYS = ("from", "to", "why")


def read_json(path, problems):
    """Parse a JSON file. On failure, add a readable message to problems and return None."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        problems.append(f"{rel(path)}: not valid JSON ({err.msg} at line {err.lineno}). "
                        "It must be strict JSON: double quotes, no trailing commas, no comments.")
    except OSError as err:
        problems.append(f"{rel(path)}: cannot be read ({err}).")
    return None


def rel(path):
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


# ----------------------------------------------------------------------------------------- the map

def map_files():
    """Every map source file, in the fixed order the build uses."""
    if not MAP_DIR.is_dir():
        return []
    return sorted(p for p in MAP_DIR.rglob("*.json") if p.name != "renames.json")


def folder_of(path):
    """map/maths/linear-algebra.json -> maths/linear-algebra"""
    return path.relative_to(MAP_DIR).with_suffix("").as_posix()


def load_map(problems=None):
    """Read every map source file.

    Returns {"topics": [...], "links": [...]}. Each topic gains "folder" (from its file's path) and
    "_file". Each link gains "_file". Order: files by path, then the order inside each file.
    """
    problems = problems if problems is not None else []
    topics, links = [], []
    for path in map_files():
        data = read_json(path, problems)
        if not isinstance(data, dict):
            continue
        folder = folder_of(path)
        for topic in data.get("topics", []):
            if not isinstance(topic, dict):
                problems.append(f"{rel(path)}: a topic is not an object.")
                continue
            if "folder" in topic and topic["folder"] != folder:
                problems.append(f"{rel(path)}: {topic.get('id')}: folder says {topic['folder']} "
                                f"but the file's place says {folder}. Leave folder out.")
            entry = dict(topic)
            entry["folder"] = folder
            entry["_file"] = rel(path)
            topics.append(entry)
        for link in data.get("links", []):
            if not isinstance(link, dict):
                problems.append(f"{rel(path)}: a link is not an object.")
                continue
            entry = dict(link)
            entry["_file"] = rel(path)
            links.append(entry)
    return {"topics": topics, "links": links}


def load_renames(problems=None):
    """map/renames.json: {"old-id": "new-id"}. Learner records follow these."""
    path = MAP_DIR / "renames.json"
    if not path.exists():
        return {}
    data = read_json(path, problems if problems is not None else [])
    return data if isinstance(data, dict) else {}


def resolve_id(topic_id, renames):
    """Follow renames to the id a topic has today."""
    seen = set()
    while topic_id in renames and topic_id not in seen:
        seen.add(topic_id)
        topic_id = renames[topic_id]
    return topic_id


def dump_map_file(topics, links):
    """The text of one map source file: topics spread out, links one per line."""
    out = ["{", '  "topics": [']
    blocks = []
    for topic in topics:
        ordered = {k: topic[k] for k in TOPIC_KEYS if k in topic}
        for k in topic:
            if k not in ordered and not k.startswith("_") and k != "folder":
                ordered[k] = topic[k]
        text = json.dumps(ordered, indent=2, ensure_ascii=False)
        # short lists read better on one line
        text = re.sub(r"\[\n\s+((?:\"[^\"\n]*\"(?:,\n\s+)?)+)\n\s+\]",
                      lambda m: "[" + re.sub(r",\n\s+", ", ", m.group(1)) + "]", text)
        blocks.append("\n".join("    " + line for line in text.splitlines()))
    out.append(",\n".join(blocks))
    out.append("  ],")
    out.append('  "links": [')
    rows = []
    for link in links:
        ordered = {k: link[k] for k in LINK_KEYS if k in link}
        rows.append("    { " + ", ".join(f"{json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}"
                                        for k, v in ordered.items()) + " }")
    out.append(",\n".join(rows))
    out.append("  ]")
    out.append("}")
    return "\n".join(out) + "\n"


def tool_files():
    """Every tool-like file inside a topic folder, as a repo-relative path."""
    found = set()
    for top in TOP_FOLDERS:
        folder = ROOT / top
        if not folder.is_dir():
            continue
        for path in folder.rglob("*"):
            if path.is_file() and path.suffix.lower() in TOOL_SUFFIXES \
                    and not any(part.startswith(".") for part in path.relative_to(ROOT).parts):
                found.add(path.relative_to(ROOT).as_posix())
    return found


# --------------------------------------------------------------------------------------- the tools

HEADER_FIELDS = ("Concept", "Course", "Play with", "Should click", "Checked", "Plan")


def tool_header(text):
    """The fields of the comment block at the top of a tool, as {field: text}."""
    found = re.search(r"<!--(.*?)-->", text, re.S)
    if not found:
        return {}
    fields, current = {}, None
    for line in found.group(1).splitlines():
        hit = re.match(r"\s*(" + "|".join(HEADER_FIELDS) + r"):\s*(.*)$", line)
        if hit:
            current = hit.group(1)
            fields[current] = hit.group(2).strip()
        elif current and line.strip() and re.match(r"\s{8,}\S", line):
            fields[current] += " " + line.strip()
        elif not line.strip():
            current = None
        else:
            current = None
    return fields


def script_block(text, block_id):
    """The contents of <script ... id="block_id">, or None."""
    found = re.search(r'<script\b[^>]*\bid="' + re.escape(block_id) + r'"[^>]*>(.*?)</script>', text, re.S)
    return found.group(1) if found else None


STYLE_BEGIN = "/* ---- momentos house style: begin"
STYLE_END = "/* ---- momentos house style: end ---- */"


def house_style(text):
    """The house-style block of a tool or of the template, markers included. None if it has none."""
    a = text.find(STYLE_BEGIN)
    b = text.find(STYLE_END)
    if a < 0 or b < 0 or b < a:
        return None
    return text[a:b + len(STYLE_END)]


# ------------------------------------------------------------------------------------- the courses

def load_courses(problems=None):
    """curricula/courses.json: the registry of course ids, checked against the catalog."""
    path = CURRICULA_DIR / "courses.json"
    if not path.exists():
        return []
    data = read_json(path, problems if problems is not None else [])
    return data.get("courses", []) if isinstance(data, dict) else []


def load_curricula(problems=None):
    """Every curricula/<slug>.json except the registry, as a list of dicts with "_file"."""
    out = []
    if not CURRICULA_DIR.is_dir():
        return out
    for path in sorted(CURRICULA_DIR.glob("*.json")):
        if path.name == "courses.json":
            continue
        data = read_json(path, problems if problems is not None else [])
        if isinstance(data, dict):
            data["_file"] = rel(path)
            out.append(data)
    return out


ASSESSED = re.compile(r"^(FA|SP|SU)(\d\d) (MT\d?|FINAL|HW\d+|DIS\d+|PSET\d+|LAB[0-9a-z]+(?:-PRE)?|MTP)(?: (.+))?$")
EXAM_KINDS = ("MT", "FINAL")


def parse_assessed(text):
    """'FA24 MT1 Q3' -> {"term": "FA24", "year": 2024, "kind": "MT1", "exam": True, "item": "Q3"} or None."""
    hit = ASSESSED.match(text.strip())
    if not hit:
        return None
    kind = hit.group(3)
    return {"term": hit.group(1) + hit.group(2), "year": 2000 + int(hit.group(2)), "kind": kind,
            "exam": kind.startswith(EXAM_KINDS), "item": hit.group(4) or ""}


def scope_year(curriculum):
    hit = re.match(r"^(FA|SP|SU)(\d\d)$", str(curriculum.get("scope_term", "")))
    return 2000 + int(hit.group(2)) if hit else None


def concept_weight(concept, curriculum, exam_kind=None):
    """How much a concept is assessed. The formula is fixed here and explained in docs/curricula.md.

    An exam item counts 1, halved for every 4 years of age. A homework, discussion, lab or practice
    item counts 0.5 in the scope term and 0.25 (aged the same way) in any other term.
    Returns (weight, exam_weight). With exam_kind ("MT1", "FINAL", ...), only matching exam items count:
    a FINAL counts every exam, "MT" counts every midterm.
    """
    now = scope_year(curriculum)
    scope = curriculum.get("scope_term")
    total = exams = 0.0
    for text in concept.get("assessed", []):
        item = parse_assessed(text)
        if not item:
            continue
        age = max(0, (now - item["year"])) if now else 0
        recency = 0.5 ** (age / 4.0)
        if item["exam"]:
            if exam_kind and exam_kind != "FINAL":
                if exam_kind == "MT" and not item["kind"].startswith("MT"):
                    continue
                if exam_kind != "MT" and item["kind"] not in (exam_kind, "MT"):
                    continue
            total += recency
            exams += recency
        elif not exam_kind:
            total += 0.5 if item["term"] == scope else 0.25 * recency
    return round(total, 3), round(exams, 3)


def course_slug(course_id):
    return re.sub(r"[^a-z0-9]+", "-", course_id.lower()).strip("-")


# --------------------------------------------------------------------------------------- the plans

PLAN_META = re.compile(r"```json plan\n(.*?)\n```", re.S)
PLAN_CASES = re.compile(r"```json check-cases\n(.*?)\n```", re.S)
PLAN_STATUSES = ("stub", "planned", "built")
PLAN_KINDS = ("tool", "quiz-only")


def load_plans(problems=None):
    """Every plans/*.md that carries a plan block. Returns dicts: the block's fields plus _file, _text."""
    problems = problems if problems is not None else []
    out = []
    if not PLANS_DIR.is_dir():
        return out
    for path in sorted(PLANS_DIR.glob("*.md")):
        if path.name in ("README.md", "BACKLOG.md", "TEMPLATE.md"):
            continue
        text = path.read_text(encoding="utf-8")
        hit = PLAN_META.search(text)
        if not hit:
            problems.append(f"{rel(path)}: has no ```json plan block.")
            continue
        try:
            meta = json.loads(hit.group(1))
        except json.JSONDecodeError as err:
            problems.append(f"{rel(path)}: the plan block is not valid JSON ({err.msg}).")
            continue
        if not isinstance(meta, dict):
            problems.append(f"{rel(path)}: the plan block must be a JSON object.")
            continue
        meta["_file"] = rel(path)
        meta["_text"] = text
        out.append(meta)
    return out


def plan_sections(text):
    """The '## ' headings of a plan, in order."""
    return [m.group(1).strip() for m in re.finditer(r"^## (.+)$", text, re.M)]


def plan_cases(text, problems=None, where=""):
    """The check cases of a plan (a list), or None if the block is missing or broken."""
    hit = PLAN_CASES.search(text)
    if not hit:
        return None
    try:
        cases = json.loads(hit.group(1))
    except json.JSONDecodeError as err:
        if problems is not None:
            problems.append(f"{where}: the check-cases block is not valid JSON ({err.msg}).")
        return None
    return cases if isinstance(cases, list) else None


def plans_by_topic(plans):
    """topic id -> the plan that serves it (a built plan wins over a planned one, then a stub)."""
    rank = {"built": 0, "planned": 1, "stub": 2}
    best = {}
    for plan in plans:
        for topic in plan.get("topics", []):
            if topic not in best or rank.get(plan.get("status"), 9) < rank.get(best[topic].get("status"), 9):
                best[topic] = plan
    return best
