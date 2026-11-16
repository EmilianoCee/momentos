# momentos

The rules for this repo are in `AGENTS.md`, which is imported here so that they live in one place.

@AGENTS.md

## Claude Code only

- The skills in `.claude/skills/` can be called by name: `/quiz EE 120`, `/exam-prep EE 105 FINAL`, `/where-am-i`,
  `/onboard`, `/add-topic`, `/write-plan`, `/build-tool`, `/record-evidence`, `/add-course`.
- To check a page, run headless Chrome on its `file://` URL and read the screenshot. The desktop preview shows one
  file as a snapshot: it cannot follow links, read `#hash` anchors or load `learner/levels.js`.
- Use cheaper models for reading and extraction, and at most three subagents at a time.

## How to teach

@prompts/learning-preprompt.md
