#!/usr/bin/env python3
"""Find where a concept is assessed, from the local survey tables, for a curriculum's `assessed` list.

    python3 scripts/assessed.py "EE 105" --list-tags
    python3 scripts/assessed.py "EE 105" common-source,source-degeneration

The survey tables are course-survey/*.tsv: one row per homework, exam or lab item, with the concept tags a
reader gave it (columns: source_id, item, tags, task, points, note). They are local only and never tracked,
because they were made from course materials. This script prints identifiers only, such as "SP24 MT Q2", which
are safe to put in a tracked curriculum.

For a list of tags it prints, as JSON: the identifiers of every item carrying any of the tags (newest first), the
weight and exam weight they give, and the target and flags that docs/curricula.md says follow from them. The
scope term and tier are read from curricula/<course>.json when it exists; pass --scope and --tier otherwise.
--old-before YEAR marks a concept "old-exams-only" when every exam item is older than YEAR and nothing else
assesses it. Standard library only.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import momentos as m  # noqa: E402

SURVEY = m.ROOT / "course-survey"
KIND = {"FINAL": 0, "MT3": 1, "MT2": 2, "MT1": 3, "MT": 3, "MTP": 4}


def rows_for(course):
    """[(identifier, set of tags)] for every survey row of the course."""
    out = []
    for path in sorted(SURVEY.glob("*.tsv")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            p = line.split("\t")
            if i == 0 or len(p) < 3 or not p[0].startswith(course + " "):
                continue
            source = p[0][len(course) + 1:].strip()
            ident = (source + " " + p[1]).strip()
            if m.parse_assessed(ident) is None:
                ident = source
                if m.parse_assessed(ident) is None:
                    continue
            out.append((ident, {t.strip().lstrip("+") for t in p[2].split(";") if t.strip()}))
    return out


def order(ident):
    a = m.parse_assessed(ident)
    k = a["kind"]
    rank = KIND.get(k, 5 if k.startswith(("HW", "PSET", "DIS")) else 6)
    return (-a["year"], 0 if a["term"].startswith("FA") else 1, rank, k, a["item"])


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("course")
    p.add_argument("tags", nargs="?", default="")
    p.add_argument("--list-tags", action="store_true", help="print every tag the survey uses for this course, with counts")
    p.add_argument("--scope", help="the scope term, such as SP24, if the course has no curriculum file yet")
    p.add_argument("--tier", type=int, help="the course's tier, if it has no curriculum file yet")
    p.add_argument("--old-before", type=int, help="a year: exam items before it count as old")
    args = p.parse_args()

    if not SURVEY.is_dir():
        sys.exit("There is no course-survey/ folder in this checkout. It is local only: see docs/curricula.md.")
    rows = rows_for(args.course)
    if not rows:
        sys.exit(f"No survey rows for {args.course!r}. Source ids in the tables start with the course id, such as 'EE 105 SP24 HW3'.")

    if args.list_tags:
        counts = {}
        for _, tags in rows:
            for t in tags:
                counts[t] = counts.get(t, 0) + 1
        for t, n in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            print(f"{n:4d}  {t}")
        return 0

    wanted = {t.strip() for t in args.tags.split(",") if t.strip()}
    if not wanted:
        sys.exit("Give the survey tags, comma separated, or --list-tags to see them.")
    cur_path = m.CURRICULA_DIR / (m.course_slug(args.course) + ".json")
    cur = json.loads(cur_path.read_text(encoding="utf-8")) if cur_path.exists() else {}
    cur.setdefault("scope_term", args.scope)
    tier = args.tier or cur.get("tier", 9)
    scope = cur.get("scope_term")

    assessed = sorted({ident for ident, tags in rows if tags & wanted}, key=order)
    concept = {"assessed": assessed}
    weight, exam_weight = m.concept_weight(concept, cur)
    parsed = [m.parse_assessed(a) for a in assessed]
    in_scope = sum(1 for a in parsed if a["term"] == scope)
    target = 4 if (exam_weight > 0 or in_scope >= 2) else 3
    flags = []
    if tier <= 3:
        exams = [a for a in parsed if a["exam"]]
        if not assessed:
            flags.append("reader-only")
        elif args.old_before and exams and all(a["year"] < args.old_before for a in exams) \
                and all(a["exam"] for a in parsed):
            flags.append("old-exams-only")
        elif scope and in_scope == 0:
            flags.append("not-yet-assessed")
        elif all(a["kind"].startswith("LAB") for a in parsed):
            flags.append("lab-only")
    unknown = sorted(wanted - {t for _, tags in rows for t in tags})
    out = {"assessed": assessed, "weight": weight, "exam_weight": exam_weight, "target": target, "flags": flags}
    if unknown:
        out["unknown_tags"] = unknown
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
