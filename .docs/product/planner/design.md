---
feature: planner
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# Task Planner Plugin — Architectural Design

## Overview
Modular planning and task manifest generation workflows providing checkable implementation matrices.

## Structure
- `plugin.json`: Defines metadata and registers `@planner` agent and skills.
- `agents/planner/agent.json`: Specialized task planning subagent (`model: flash`).
- `skills/planner-tasks/SKILL.md`: Checklist generator.
- `skills/planner-review/SKILL.md`: Planning auditor emitting `review-verdict` blocks.
