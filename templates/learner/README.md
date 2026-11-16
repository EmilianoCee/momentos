# Your record

This folder is your own record of mastery. The shared repo ignores it, so a fork never carries anyone's levels,
and pulling updates can never conflict with it. It is its own git repository, so your history is kept.

| File | What it is |
|---|---|
| `profile.md` | Who you are: your handle, your courses, your exams, and a few lines about how you learn. |
| `evidence.jsonl` | One graded answer per line. Append only. This is the record of truth. |
| `state.json`, `levels.js`, `progress.md` | Rebuilt from the two files above by `scripts/learner.py`. Never edit them. |

Nothing here sets a level by hand. A level is what the evidence supports, by the rules in `docs/levels.md`.

To back the record up, give it a private remote of its own:

```bash
git -C learner remote add origin <the address of a private repository>
```

```bash
git -C learner push -u origin HEAD
```

Never add this folder to the shared repo.
