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
- `/kanche:planner-tasks`: Formulate checkable task manifests representing discrete files to edit and test plan commands.
- `/kanche:planner-review`: Perform review on tasks checklist layout, returning a structured `review-verdict` (`GO` | `NO-GO`) block with actionable findings.

## Specialized Subagent
- `@planner`: Handles task manifest creation, task decomposition, and tasks review. Configured with `model: flash`.

## Acceptance Criteria (as-built)
1. Exposes `/kanche:planner-tasks` and `/kanche:planner-review` slash commands.
2. Registers subagent `@planner` in `plugins/kanche/plugin.json`.
3. Emits and consumes universal `review-verdict` protocol block.
4. Integrates with `/kanche:sdd-run` orchestrator for P3 (Tasks) phase.
