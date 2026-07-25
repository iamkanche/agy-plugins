---
feature: planner
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# Task Planner Plugin — Architectural Design

## Overview
Modular plugin providing task manifest and planning workflows (`plugins/planner`).

## Structure
- `plugin.json`: Defines metadata, output-language rules, skills directory, and agent (`planner`).
- `agents/`:
  - `planner/agent.json`
- `skills/`:
  - `tasks/SKILL.md`
  - `review/SKILL.md`
