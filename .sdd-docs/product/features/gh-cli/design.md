---
feature: gh-cli
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-18
---

# GitHub CLI Plugin — Consolidated Technical Design

<!-- schema: design | written by /sdd:sync-product (dev-only sections stripped) -->

## Approach
Extend `gh-cli` plugin by writing namespaced skill files under its `skills/` directory, registering new commands in `plugin.json`, and updating the inspection web dashboard.

## Components
- `skills/pr-merge/SKILL.md` (New): Implements merging and branch cleanup.
- `skills/pr-create/SKILL.md` (Modified): Added `--assignee` parameter.
- `plugin.json` (Modified): Registered `/gh-cli:pr-merge`.
- `index.html` (Modified): Registered new commands and options.
