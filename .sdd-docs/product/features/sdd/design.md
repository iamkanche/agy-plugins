---
feature: sdd
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
---

# SDD Plugin — Consolidated Technical Design

<!-- schema: design | written by /sdd:sync-product (dev-only sections stripped) -->

## Approach
Improve the workflows in the `sdd` plugin by editing orchestration logic in namespaced skill files under its `skills/` directory, adding frontmatter, and updating the inspection web dashboard. Mandate `default_api:ask_question` tool for all human gates. Add support for token-optimized specialized subagents and full workflow automation loops.

## Components
- `skills/run/SKILL.md` (Modified): Logic updated to correct command namespaces, consolidate docs/code commits, automate Level 2, use slug directories, use `default_api:ask_question` tool for all manual gates, generate verification receipts in P0, delegate tasks to specialized subagents, parse settings from `settings.json`, and run 3x loops for review retry, validation fix, and PR polling.
- `skills/continue/SKILL.md` (Modified): State restoration rules updated to align with automated Level 2 execution and slug paths.
- `skills/sync/SKILL.md` (Modified): Converted from drift detector worker to `/sdd:sync` orchestrator. Adds support for copying to `/features/{slug}/`, cleanup of development directory, and auto-committing.
- `rules/workflow-gating.md` (Modified): Mandate interactive `default_api:ask_question` tool for all side-effect confirmations.
- Worker skills (Modified): Added frontmatter blocks to all worker skills so they trigger as standard commands.
- `settings.json` (New): Configuration schema at `.sdd-docs/settings.json` to control automation loops and polling.
- **Subagent Definitions** (New): Configuration files under `plugins/sdd/agents/{agent-name}/agent.json` that register with the SDK CLI to define focused execution contexts.
  - `sdd-analyst`: Handles specs analysis & reviews. Write tools: `false`.
  - `sdd-architect`: Handles architecture design & reviews. Write tools: `false`.
  - `sdd-planner`: Handles planning, task list drafting & reviews. Write tools: `true`.
  - `sdd-coder`: Handles code build modifications & reviews. Write tools: `true`.
  - `sdd-validator`: Handles validation, synchronization, and run controllers. Write tools: `false`.
- **Registry Dashboard View**: `index.html` (Modified) to render command descriptions referencing the delegated subagents to improve visual clarity of the agentic workflow.

## Interfaces
- **Subagent Manifest Interface**: Each subagent's `agent.json` conforms to:
  ```json
  {
    "name": "string",
    "description": "string",
    "system_prompt": "string",
    "enable_write_tools": boolean,
    "enable_mcp_tools": boolean,
    "enable_subagent_tools": boolean
  }
  ```
- **Settings Manifest Interface**: Configuration options parsed from `.sdd-docs/settings.json`:
  ```json
  {
    "mode": "auto" | "manual",
    "max_loops": integer,
    "pr_polling": {
      "interval_seconds": integer,
      "max_attempts": integer
    },
    "auto_merge": boolean,
    "preserve_files": ["string"]
  }
  ```
