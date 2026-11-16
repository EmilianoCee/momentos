---
name: where-am-i
description: Report the learner's progress in each course against its mastery target. Use for 'where am I' or 'progress report'.
---

# Where am I

The report is computed. Your job is to print it and say what it means in three lines.

## Steps

1. **Is there a record?** If `learner/profile.md` does not exist, say so, offer the `onboard` skill, and stop.
2. **Run** `python3 scripts/learner.py report`, or with `--course "<course>"` for one course. Print what it prints.
3. **Add at most three lines of your own:** the single heaviest gap; what is due for review today; and what the calibration table says (confidence ahead of results, behind them, or matched).
4. **Offer the next step:** `review` if anything is due, otherwise `quiz me <the course with the largest gap>`.

## Checks

- Every number you state is in the report.

## Done means

- The learner has seen the report.
- Nothing was said about a level that the report does not say.
