---
feature: dev
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# Development Plugin — Consolidated Specification

## Context
The `dev` plugin packages incremental code implementation, refactoring, and code generation workflows for Google Antigravity agents.

## Capabilities
- `/kanche:dev-implement` - Incrementally apply codebase modifications according to task checklist.

## Specialized Subagent
- `coder`: Handles target codebase modifications incrementally, following specifications and task manifests.

## Acceptance Criteria (as-built)
1. Exposes `/kanche:dev-implement` slash command.
2. Registers subagent `coder` in `plugins/dev/plugin.json`.
3. Integrates with `/kanche:sdd-run` orchestrator for P4 (Build / Implementation) phase.
