---
feature: sdd
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
---

# SDD Plugin — Consolidated Technical Design

<!-- schema: design | written by /sdd:sync-product (dev-only sections stripped) -->

## Approach
Improve the workflows in the `sdd` plugin by editing orchestration logic in namespaced skill files under its `skills/` directory, adding frontmatter, and updating the inspection web dashboard. Mandate `default_api:ask_question` tool for all human gates.

## Components
- `skills/run/SKILL.md` (Modified): Logic updated to correct command namespaces, consolidate docs/code commits, automate Level 2, use slug directories, and use `default_api:ask_question` tool for all manual gates.
- `skills/continue/SKILL.md` (Modified): State restoration rules updated to align with automated Level 2 execution and slug paths.
- `skills/sync/SKILL.md` (Modified): Converted from drift detector worker to `/sdd:sync` orchestrator. Adds support for copying to `/features/{slug}/`, cleanup of development directory, and auto-committing.
- `rules/workflow-gating.md` (Modified): Mandate interactive `default_api:ask_question` tool for all side-effect confirmations.
- Worker skills (Modified): Added frontmatter blocks to all worker skills so they trigger as standard commands.
