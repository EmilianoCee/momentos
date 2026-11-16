# Learner profile

This file is yours. Every teaching and quiz session reads it first, and the shared repo never tracks it.
The block below is checked by `python3 scripts/learner.py check`. The prose under it is free.

```json
{
  "schema": 1,
  "handle": "",
  "started": "",
  "courses": {},
  "exams": [],
  "session_size": 8
}
```

- `courses`: each course id from `curricula/courses.json` that matters to you, set to `now`, `done` or `next`.
  For example `{"EE 120": "now", "Math 53": "done"}`.
- `exams`: the exams you are preparing for, for example `{"course": "EE 120", "name": "FINAL", "date": "2026-12-17"}`.
- `session_size`: how many questions a quiz session asks.

## About me

Write a few lines here in place of this paragraph. A session uses them to choose examples and to pitch its
explanations. Use a handle, never a name or an email address.

- What I am studying, and where I am heading.
- What I have already done, and what I am taking now.
- What I work with (languages, simulators, tools).
- What I want from an explanation (for example: the picture before the formula).
