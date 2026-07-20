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
- **Registry Dashboard View**: `index.html` (Modified) to replace the static pipeline tables with an interactive SVG connections map canvas (`#connection-map-svg`, `viewBox="0 0 1300 700"`). It dynamically plots node positions for all 35 commands and hooks path connectors to node boundaries utilizing boundary offset calculations. Tracks state via `MapState` controller (`selectedNodeId`, `hoveredNodeId`). Connects click locks to sidebar active loaders and wires Arrow key Euclidean distance spatial focus navigation. Appends static configurations database (`gitAndGhCliData`) for non-sdd commands.

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

## P9 Alignment Sequence Optimization
Reorders the SDD Level 2 P9 step to run `/sdd:sync` on the feature branch before `/gh-cli:pr-merge`.

- **`plugins/sdd/skills/run/SKILL.md` (Modified)**: Phase model diagram updated: `P9 alignment /sdd:sync → /gh-cli:pr-merge & preserve`. P9 auto mode now runs `/sdd:sync` locally (promoting dev docs, committing and pushing to feature branch), polls CI via `pr_polling` settings, then invokes `/gh-cli:pr-merge`. P9 manual mode gated with two separate `default_api:ask_question` prompts.
- **`plugins/sdd/index.html` (Modified)**: Node coordinates swapped: `/sdd:sync` → `(1080, 540, P9 Sync)`, `/gh-cli:pr-merge` → `(1080, 640, P9 Merge)`. Edges updated: removed `pr-approve→pr-merge`, `pr-merge→sync`, `sync→branch-delete`; added `pr-approve→sync`, `sync→pr-merge`. `/sdd:run` commandData steps extended with P7/P8/P9 entries.

## Fully AI-Automated Workflow
Removes interactive `default_api:ask_question` confirmation gates when running in auto mode.

- **Mode-Conditional Gate Pattern**: Replaced the target unconditional `default_api:ask_question` calls in skill files with a standard clause that checks if the skill is invoked from SDD auto mode. If yes, it logs the action details and continues automatically. Otherwise, it presents the user prompt.
- **Skills Updated**: commit, push, branch-delete, pr-create, pr-merge, and pr-respond skills have their main Gate steps conditionalized and Done-when blocks updated.
- **Rules & Memory Updated**: memory.md, rules.md, tech.md, and plugin rules (workflow-gating.md, git-hard-rules.md, gh-hard-rules.md) updated to replace unconditional ask_question references with mode-conditional versions.
- **Safety Invariants**: Enforced unconditionally in all modes.

## Command Arguments & Usage Samples in Dashboard
Adds examples of CLI command syntax and arguments to the interactive skills connection dashboard.

- **UI Rendering Update**: Modified `loadCommandDetails(cmdName)` to check if `data.usage` exists and dynamically inject a labeled `.code-snippet` HTML block containing the usage example directly in the details panel header.
- **Registry Update**: Populated the `usage` string property for all 35 commands in `commandData` and `gitAndGhCliData` objects within `plugins/sdd/index.html`.
