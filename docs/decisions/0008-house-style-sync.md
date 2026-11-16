# 0008. The house style is copied from the template by a script

Status: accepted, 2026-11-15.

## Context

Every tool carries the same block of CSS. It had already drifted in all three tools.

## Options

- **A shared stylesheet.** Impossible: a tool is one file.
- **Trust people to copy it.** It drifted within three tools.
- **Markers round the block, a sync script, and a check.** The template is the one place to change the look.

## Decision

The block sits between `/* ---- momentos house style: begin` and `/* ---- momentos house style: end ---- */` in the first `<style>` of the template and of every tool. `python3 scripts/sync-house-style.py` copies the template's block into each tool. `scripts/check.py style` fails when a tool differs.

## Consequences

- A tool that needs a different layout overrides a rule after the end marker, inside its own section.
- An override of a rule that the house block changes in a media query must be wrapped in the opposite media query.
