# SDD Plugin — Changelog

<!-- schema: changelog | written by /sdd:sync-product -->

## 2026-07-18 — improve-sdd-plugins
- Corrected incorrect git/gh-cli command namespaces in workflows.
- Automated Level 2 phases (P7-P9) in auto mode.
- Aggregated commits into docs-related and implementation-related checkpoints.
- Removed numeric prefix requirements, adopting clean feature slugs.
- Registered all worker skills as top-class Antigravity commands with frontmatter.

## 2026-07-19 — improvements_of_plugins
- Migrated manual phase transitions, validation failures, and LEVEL 2 checkpoints in SDD workflow execution to use the interactive `default_api:ask_question` tool.

## 2026-07-19 — add-sdd-agents
- Defined 5 specialized subagents (`sdd-analyst`, `sdd-architect`, `sdd-planner`, `sdd-coder`, `sdd-validator`) to handle specific phases of the SDD feature lifecycle.
- Configured security-oriented write-permission boundaries (only coder and planner subagents have write privileges).
- Updated the registry dashboard in `index.html` to trace command delegation to the subagents.

## 2026-07-19 — sdd-full-automation-development
- Added verification receipt generation and confirmation gate in Phase P0.
- Implemented phase delegation to specialized, token-optimized subagents (Analyst, Architect, Planner, Coder, Validator) to conserve parent context and tokens.
- Automated 3x retry and response/fix loops for specs/design/tasks/build reviews, validation failures, and PR feedback.
- Configured automatic PR merge on approval and synchronization of feature documentation post-merge.
- Supported settings customization via `.sdd-docs/settings.json`.
