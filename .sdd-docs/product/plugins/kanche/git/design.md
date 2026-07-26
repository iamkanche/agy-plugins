---
feature: git
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
---

# Git Plugin — Consolidated Technical Design

<!-- schema: design | written by /kanche:sdd-sync (dev-only sections stripped) -->

## Approach
Extend `git` plugin by writing namespaced skill files under its `skills/` directory, registering new commands in `plugin.json`, and updating the inspection web dashboard. Mandate `default_api:ask_question` tool for all human gates.

## Components
- `skills/tag-delete/SKILL.md` (New): Implements local and remote tag deletion.
- `skills/tag-push/SKILL.md` (New): Implements pushing local tags to remote.
- `rules/git-hard-rules.md` (Modified): Mandate interactive `default_api:ask_question` tool for all human gates.
- `skills/` (Modified): Updated commit, push, branch-delete, tag-create, tag-delete, tag-push, rebase skills to use `default_api:ask_question` tool.
- `plugin.json` (Modified): Registered `/kanche:git-tag-delete` and `/kanche:git-tag-push`.
- `index.html` (Modified): Registered new commands and options.
