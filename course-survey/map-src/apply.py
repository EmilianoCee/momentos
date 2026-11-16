#!/usr/bin/env python3
"""Turn the compact topic lists in this folder (*.txt) into map/<folder>.json and curricula/<course>.json.

Line types (fields separated by " | "):
  F folder/path                      the folder for the T and M lines that follow
  T id | title | essence | check     a topic (new, or replacing the text of an existing one)
  M id                               move an existing topic into the current folder, text unchanged
  L from > to | why                  a link
  N id | course | how                a note on where the idea comes back later
  U course | unit-id | title         a unit of a course
  C course | unit-id | topic | survey tags, comma separated [| target]
The survey tags pick the assessment items (course-survey/*.tsv) that count for the concept.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import momentos as m
SRC = Path(__file__).parent
SURVEY = ROOT / "course-survey"
SCRATCH = Path("/private/tmp/claude-501/-Users-ec--claude-spares-spare-0sWyHV/bff8eedd-1319-40c5-97fb-0a573f7a7cf6/scratchpad/survey")
from meta import COURSES

def rows_for(course):
    out = []
    for name in COURSES[course].get("tsv", []):
        path = SCRATCH / name if (name == "ee120-exams-2024-2026.tsv" and (SCRATCH / name).exists()) else SURVEY / name
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            p = line.split("\t")
            if i == 0 or len(p) < 3 or not p[0].startswith(course + " "):
                continue
            ident = (p[0][len(course) + 1:] + " " + p[1]).strip()
            if m.parse_assessed(ident) is None:
                ident = p[0][len(course) + 1:].strip()
                if m.parse_assessed(ident) is None:
                    continue
            out.append((ident, {t.strip().lstrip("+") for t in p[2].split(";") if t.strip()}))
    return out

KIND = {"FINAL": 0, "MT3": 1, "MT2": 2, "MT1": 3, "MT": 3, "MTP": 4}
def order(ident):
    a = m.parse_assessed(ident)
    return (-a["year"], 0 if a["term"].startswith("FA") else 1, KIND.get(a["kind"], 5 if a["kind"].startswith("HW") or a["kind"].startswith("PSET") else 6), a["kind"], a["item"])

topics, links, notes, units, concepts = {}, {}, {}, {}, {}
old = m.load_map([])
for t in old["topics"]:
    e = {k: v for k, v in t.items() if not k.startswith("_") and k != "courses"}
    topics[t["id"]] = e
for l in old["links"]:
    links[(l["from"], l["to"])] = l["why"]
folder = None
for path in sorted(SRC.glob("*.txt")):
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        kind, rest = line[0], line[2:]
        f = [x.strip() for x in rest.split(" | ")]
        try:
            if kind == "F":
                folder = f[0]
            elif kind == "T":
                tid, title, essence, check = f
                e = topics.get(tid, {})
                e.update(id=tid, title=title, essence=essence, check=check, folder=folder)
                topics[tid] = e
            elif kind == "M":
                topics[f[0]]["folder"] = folder
            elif kind == "L":
                a, b = [x.strip() for x in f[0].split(" > ")]
                links[(a, b)] = f[1]
            elif kind == "N":
                notes.setdefault(f[0], []).append({"course": f[1], "how": f[2]})
            elif kind == "U":
                units.setdefault(f[0], []).append({"id": f[1], "title": f[2]})
            elif kind == "C":
                concepts.setdefault(f[0], []).append((f[1], f[2], [x.strip() for x in f[3].split(",") if x.strip()] if len(f) > 3 else [], int(f[4]) if len(f) > 4 else None))
            else:
                raise ValueError("unknown line type")
        except Exception as err:
            sys.exit(f"{path.name} line {n}: {err}: {raw}")
for tid, items in notes.items():
    if tid not in topics:
        sys.exit(f"note for unknown topic {tid}")
    topics[tid]["later"] = items
bad = [f"{a} > {b}" for (a, b) in links if a not in topics or b not in topics]
if bad:
    sys.exit("links to unknown topics: " + ", ".join(bad))

by_folder = {}
for t in topics.values():
    by_folder.setdefault(t["folder"], {"topics": [], "links": []})["topics"].append(t)
for (a, b), why in links.items():
    by_folder[topics[b]["folder"]]["links"].append({"from": a, "to": b, "why": why})
for p in m.map_files():
    p.unlink()
for fo, d in by_folder.items():
    p = m.MAP_DIR / (fo + ".json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(m.dump_map_file(d["topics"], d["links"]), encoding="utf-8")

for course, items in concepts.items():
    meta = COURSES[course]
    rows = rows_for(course)
    cur = {"course": course, "tier": meta["tier"]}
    for k in ("scope_term", "built_from", "notes", "sources", "outline"):
        if meta.get(k):
            cur[k] = meta[k]
    cur["units"] = units.get(course, [])
    scope = meta.get("scope_term")
    out, seen = [], set()
    for unit, tid, tags, target in items:
        if tid not in topics:
            sys.exit(f"{course}: concept {tid} is not a topic")
        if tid in seen:
            sys.exit(f"{course}: concept {tid} listed twice")
        seen.add(tid)
        assessed = sorted({ident for ident, rt in rows if rt & set(tags)}, key=order)
        c = {"topic": tid, "unit": unit, "target": 3, "assessed": assessed}
        w, ew = m.concept_weight(c, cur)
        parsed = [m.parse_assessed(a) for a in assessed]
        in_scope = sum(1 for a in parsed if a["term"] == scope)
        c["target"] = target or (4 if (ew > 0 or in_scope >= 2) else 3)
        flags = []
        if meta["tier"] <= 3:
            exams = [a for a in parsed if a["exam"]]
            if not assessed:
                flags.append("reader-only")
            elif meta.get("old_before") and exams and all(a["year"] < meta["old_before"] for a in exams) and not any(not a["exam"] for a in parsed):
                flags.append("old-exams-only")
            elif scope and meta.get("flag_not_yet") and in_scope == 0:
                flags.append("not-yet-assessed")
            elif all(a["kind"].startswith("LAB") for a in parsed):
                flags.append("lab-only")
        if flags:
            c["flags"] = flags
        out.append(c)
    head = json.dumps({k: v for k, v in cur.items()}, indent=2, ensure_ascii=False)[:-2]
    text = head + ',\n  "concepts": [\n' + ",\n".join("    " + json.dumps(c, ensure_ascii=False) for c in out) + "\n  ]\n}\n"
    (m.CURRICULA_DIR / (m.course_slug(course) + ".json")).write_text(text, encoding="utf-8")
    print(f"{course}: {len(out)} concepts, {sum(1 for c in out if c['target'] >= 4)} at L4, {sum(1 for c in out if not c['assessed'])} with no items")
print(len(topics), "topics,", len(links), "links,", len(by_folder), "folders")
