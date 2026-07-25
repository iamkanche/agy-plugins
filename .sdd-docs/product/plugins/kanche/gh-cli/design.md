---
feature: gh-cli
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
---

# GitHub CLI Plugin — Consolidated Technical Design

<!-- schema: design | written by /sdd:sync-product (dev-only sections stripped) -->

## Approach
Extend `gh-cli` plugin by writing namespaced skill files under its `skills/` directory, registering new commands in `plugin.json`, and updating the inspection web dashboard. Mandate `default_api:ask_question` tool for all human gates.

## Components
- `skills/pr-merge/SKILL.md` (New): Implements merging and branch cleanup.
- `skills/pr-create/SKILL.md` (Modified): Added `--assignee` parameter.
- `rules/gh-hard-rules.md` (Modified): Mandate interactive `default_api:ask_question` tool for all human gates.
- `skills/` (Modified): Updated pr-approve, pr-create, pr-merge, pr-respond, pr-review skills to use `default_api:ask_question` tool.
- `plugin.json` (Modified): Registered `/gh-cli:pr-merge`.
- `index.html` (Modified): Registered new commands and options.
