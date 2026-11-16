#!/usr/bin/env python3
"""Copy the house-style block of templates/tool-template.html into every tool.

    python3 scripts/sync-house-style.py           rewrite the block in each tool that differs
    python3 scripts/sync-house-style.py --check   change nothing; exit 1 if a tool differs

The block is everything between the two marker comments in the first <style> of a tool:

    /* ---- momentos house style: begin ...
    /* ---- momentos house style: end ---- */

Change the look in the template only, then run this. A tool's own rules go after the end marker.
Standard library only.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import momentos as m  # noqa: E402


def main():
    check = "--check" in sys.argv[1:]
    canonical = m.house_style(m.TEMPLATE.read_text(encoding="utf-8"))
    if canonical is None:
        sys.exit("templates/tool-template.html has no house-style markers.")
    changed = missing = 0
    for tool in sorted(m.tool_files()):
        if not tool.endswith(".html"):
            continue
        path = m.ROOT / tool
        text = path.read_text(encoding="utf-8")
        block = m.house_style(text)
        if block is None:
            print(f"  ERROR    {tool}: has no house-style markers. Copy the first <style> block of the template by hand.")
            missing += 1
        elif block != canonical:
            changed += 1
            if check:
                print(f"  ERROR    {tool}: its house-style block differs from the template's.")
            else:
                path.write_text(text.replace(block, canonical, 1), encoding="utf-8")
                print(f"  synced   {tool}")
    if check and (changed or missing):
        return 1
    if not changed and not missing:
        print("Every tool carries the template's house style.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
