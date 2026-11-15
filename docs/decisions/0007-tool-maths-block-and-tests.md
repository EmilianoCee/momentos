# 0007. Each tool keeps its maths in a block that Node can test

Status: accepted, 2026-11-15.

## Context

The rule was that a tool's maths lives in plain functions with no DOM, so it can be tested with Node. In practice the functions sat inside a closure with the drawing code, and there was no harness.

## Options

- **A separate .js file per tool.** Easy to test, but a tool must be one file with no script loaded from elsewhere.
- **Marker comments inside the main script.** One file, but the functions still close over page state.
- **A dedicated script block, run on its own by the harness.** One file, and a function that touches the page fails the test.

## Decision

A tool has `<script id="maths">` defining `var MATHS = {...}` with pure functions, and `<script type="application/json" id="check-cases">` listing cases as function, arguments and expected value with a note that carries the units. `node scripts/test-tools.js` runs each maths block in an empty context and compares. Node built-ins only.

## Consequences

- The three existing tools were moved to this shape, and their header `Checked:` numbers became 26 check cases.
- A tool built from a plan must carry every check case of its plan.
- The main script reads the page state and calls `MATHS`; it holds no formulas of its own.
