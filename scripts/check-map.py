#!/usr/bin/env python3
"""Check that the knowledge map in index.html matches what is actually in the repo.

    python3 scripts/check-map.py

It reads the JSON block at the top of index.html and reports:

  errors    a tool path that does not exist, a link to a topic that is not there, a repeated id,
            a tool file in a topic folder that no topic mentions, a tool missing from the README
  warnings  a topic with no links, a folder that is on the map but not on disk,
            an essence that has grown into a paragraph

Exit code 0 means there are no errors. Only the standard library is used.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_FILE = ROOT / "index.html"
README = ROOT / "README.md"

# Files with these endings, inside a topic folder, count as tools and must be on the map.
TOOL_SUFFIXES = {".html", ".py", ".ipynb", ".m", ".asc"}
# Top-level folders that do not hold topics.
NOT_TOPICS = {"course-materials", "templates", "scripts", "prompts", "node_modules"}

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BLOCK = re.compile(r'<script type="application/json" id="map-data">(.*?)</script>', re.S)


def load_map():
    """Return the map data, or exit with a message that says where the JSON is broken."""
    if not MAP_FILE.exists():
        sys.exit("index.html is missing, so there is no map to check.")
    text = MAP_FILE.read_text(encoding="utf-8")
    found = BLOCK.search(text)
    if not found:
        sys.exit('index.html has no <script type="application/json" id="map-data"> block.')
    try:
        return json.loads(found.group(1))
    except json.JSONDecodeError as err:
        line = text[: found.start(1)].count("\n") + err.lineno
        sys.exit(f"The map data is not valid JSON: {err.msg} at index.html line {line}.\n"
                 "It must be strict JSON: double quotes, no trailing commas, no comments.")


def tool_files():
    """Every tool-like file that sits inside a topic folder, as a repo-relative path."""
    found = set()
    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir() or folder.name.startswith(".") or folder.name in NOT_TOPICS:
            continue
        for path in folder.rglob("*"):
            if path.is_file() and path.suffix.lower() in TOOL_SUFFIXES and not any(p.startswith(".") for p in path.parts):
                found.add(path.relative_to(ROOT).as_posix())
    return found


def main():
    data = load_map()
    topics = data.get("topics", [])
    links = data.get("links", [])
    errors, warnings = [], []

    # ---- topics
    ids, registered = set(), set()
    for n, topic in enumerate(topics, 1):
        name = topic.get("id") or f"topic number {n}"
        for field in ("id", "title", "folder", "essence"):
            if not str(topic.get(field, "")).strip():
                errors.append(f"{name}: has no {field}.")
        tid = topic.get("id", "")
        if tid:
            if not KEBAB.match(tid):
                errors.append(f"{tid}: the id should be lowercase words joined by hyphens.")
            if tid in ids:
                errors.append(f"{tid}: this id is used more than once.")
            ids.add(tid)
        folder = str(topic.get("folder", ""))
        if folder.startswith("/") or folder.endswith("/") or "\\" in folder:
            errors.append(f"{name}: write the folder like maths/linear-algebra, with no slash at either end.")
        tools = topic.get("tools", [])
        if not isinstance(tools, list):
            errors.append(f"{name}: tools must be a list of paths.")
            tools = []
        for tool in tools:
            registered.add(tool)
            if not (ROOT / tool).is_file():
                errors.append(f"{name}: the tool {tool} does not exist.")
        if folder and not (ROOT / folder).is_dir():
            warnings.append(f"{name}: the folder {folder}/ is on the map but not on disk. Create it when the first file arrives.")
        if len(str(topic.get("essence", ""))) > 260:
            warnings.append(f"{name}: the essence is {len(topic['essence'])} characters. One or two sentences reads better on the map.")

    # ---- links
    seen, linked = set(), set()
    for link in links:
        a, b = link.get("from"), link.get("to")
        label = f"link {a} -> {b}"
        if a not in ids:
            errors.append(f"{label}: there is no topic called {a}.")
        if b not in ids:
            errors.append(f"{label}: there is no topic called {b}.")
        if a == b:
            errors.append(f"{label}: a topic cannot link to itself.")
        if (a, b) in seen:
            errors.append(f"{label}: this link appears twice.")
        if (b, a) in seen:
            warnings.append(f"{label}: the opposite link exists too. Links point from the foundation to what it makes possible, so one of them is probably enough.")
        seen.add((a, b))
        linked.update((a, b))
        if not str(link.get("why", "")).strip():
            errors.append(f"{label}: has no why. The sentence that says what carries over is the point of the link.")
    for tid in sorted(ids - linked):
        warnings.append(f"{tid}: is not linked to anything.")

    # ---- the repo against the map, and the map against the README
    for path in sorted(tool_files() - registered):
        errors.append(f"{path}: is in the repo but no topic on the map lists it. Add it to a topic's tools in index.html.")
    readme = README.read_text(encoding="utf-8") if README.exists() else ""
    for tool in sorted(registered):
        if (ROOT / tool).is_file() and tool not in readme:
            errors.append(f"{tool}: is on the map but not in the tool index in README.md.")

    # ---- report
    built = sum(1 for t in topics if t.get("tools"))
    print(f"{len(topics)} topics ({built} with a tool, {len(topics) - built} planned), {len(registered)} tools, {len(links)} links")
    for message in warnings:
        print("  warning  " + message)
    for message in errors:
        print("  ERROR    " + message)
    if errors:
        print(f"\n{len(errors)} error(s). The map and the repo disagree.")
        return 1
    print("The map and the repo agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
