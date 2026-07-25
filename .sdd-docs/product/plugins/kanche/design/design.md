---
feature: design
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# Design & Specs Plugin — Architectural Design

## Overview
Modular plugin providing requirements and architectural design workflows (`plugins/design`).

## Structure
- `plugin.json`: Defines metadata, output-language rules, skills directory, and agents (`analyst`, `architect`).
- `agents/`:
  - `analyst/agent.json`
  - `architect/agent.json`
- `skills/`:
  - `grill/SKILL.md`
  - `specs/SKILL.md`
  - `specs-review/SKILL.md`
  - `init/SKILL.md`
  - `review/SKILL.md`
