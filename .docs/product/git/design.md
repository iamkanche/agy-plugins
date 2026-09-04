---
feature: git
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
---

# Git Plugin — Consolidated Technical Design

<!-- schema: design | written by /kanche:sdd-sync (dev-only sections stripped) -->

## Approach
Provide robust Git lifecycle management via flattened skill directories under `plugins/kanche/skills/git-*`, registering commands in `plugin.json`, and updating the inspection web dashboard. Mandate `default_api:ask_question` tool for all human gates per `plugins/kanche/rules/destructive-safety.md`.

## Components
- `skills/git-commit/SKILL.md`: Safe staging and conventional commit creation gated behind interactive human confirmation.
- `skills/git-push/SKILL.md`: Remote branch push with upstream tracking, gated behind interactive human confirmation.
- `skills/git-branch-create/SKILL.md` & `skills/git-branch-delete/SKILL.md`: Branch lifecycle management with confirmation for deletion.
- `skills/git-tag-create/SKILL.md`, `skills/git-tag-delete/SKILL.md`, `skills/git-tag-push/SKILL.md`: Annotated tag lifecycle with confirmation gates.
- `skills/git-rebase/SKILL.md`: Branch rebase gated behind interactive human confirmation.
- `rules/destructive-safety.md` & `rules/git-hard-rules.md`: Strict human-in-the-loop policies preventing autonomous execution of destructive actions.
- `plugin.json`: Registered all 13 git commands.
- `index.html`: Registered commands and options in web dashboard.
