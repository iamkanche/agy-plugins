---
feature: sdd
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-18
---

# SDD Plugin — Consolidated Technical Design

<!-- schema: design | written by /sdd:sync-product (dev-only sections stripped) -->

## Approach
Improve the workflows in the `sdd` plugin by editing orchestration logic in namespaced skill files under its `skills/` directory, adding frontmatter, and updating the inspection web dashboard.

## Components
- `skills/run/SKILL.md` (Modified): Logic updated to correct command namespaces, consolidate docs/code commits, automate Level 2, and use slug directories.
- `skills/continue/SKILL.md` (Modified): State restoration rules updated to align with automated Level 2 execution and slug paths.
- `skills/sync/SKILL.md` (Modified): Converted from drift detector worker to `/sdd:sync` orchestrator. Adds support for copying to `/features/{slug}/`, cleanup of development directory, and auto-committing.
- Worker skills (Modified): Added frontmatter blocks to all worker skills so they trigger as standard commands.
