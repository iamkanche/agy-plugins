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

