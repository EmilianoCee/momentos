# 0009. A plan's check cases are produced by a reference script

Status: accepted, 2026-11-15.

## Context

A plan must let a smaller model build a tool without opening the course materials and without asking a question. Its numbers must be right. A number typed from mental arithmetic is the likeliest thing in a plan to be wrong, and the course readers lost most of their equations in conversion, so no formula can be taken from them on trust.

## Options

- **Numbers written into the plan by hand.** Unverifiable.
- **Cases in a separate data file.** Verifiable, but the plan is no longer self-contained.
- **Cases inside the plan, with a script that must reproduce them.** Self-contained and checked.

## Decision

Each tool plan has a `json check-cases` block and a standard-library Python script in `plans/checks/` that prints the same cases. `scripts/check.py plans` runs the script and fails if any value differs. Cases are tagged, and a plan must include a limit to zero, a limit to infinity and a case where the approximation breaks. The built tool copies the cases, so the JavaScript is tested against numbers that came from an independent implementation.

## Consequences

- Writing a plan means writing a small reference implementation first.
- A plan starts as a stub that fixes the design (the picture, what is dragged, the misconception) and is expanded in place.
- Words that leave a choice open are rejected by the checker.
