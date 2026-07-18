---
feature: git
module: plugins
pbi: [001_update_plugins]
integrated_at: 2026-07-18
updated_at: 2026-07-18
---

# Git Plugin — Consolidated Technical Design

<!-- schema: design | written by /sdd:sync-product (dev-only sections stripped) -->

## Approach
Extend `git` plugin by writing namespaced skill files under its `skills/` directory, registering new commands in `plugin.json`, and updating the inspection web dashboard.

## Components
- `skills/tag-delete/SKILL.md` (New): Implements local and remote tag deletion.
- `skills/tag-push/SKILL.md` (New): Implements pushing local tags to remote.
- `plugin.json` (Modified): Registered `/git:tag-delete` and `/git:tag-push`.
- `index.html` (Modified): Registered new commands and options.
