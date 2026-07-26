---
feature: planner
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# Task Planner Plugin — Consolidated Specification

## Context
The `planner` plugin packages task decomposition, checklist manifests, and implementation planning workflows for Google Antigravity agents.

## Capabilities
- `/kanche:planner-tasks` - Formulate task checklist lists representing discrete files to edit and test plan commands.
- `/kanche:planner-review` - Perform review on tasks checklist layout, returning a GO/NO-GO verdict with findings.

## Specialized Subagent
- `planner`: Handles task manifest creation, task decomposition, and tasks review.

## Acceptance Criteria (as-built)
1. Exposes `/kanche:planner-tasks` and `/kanche:planner-review` slash commands.
2. Registers subagent `planner` in `plugins/planner/plugin.json`.
3. Integrates with `/kanche:sdd-run` orchestrator for P3 (Tasks) phase.
