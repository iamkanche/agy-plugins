# Git Plugin — Changelog

<!-- schema: changelog | written by /kanche:sdd-sync -->

## 2026-07-18 — 001_update_plugins
- Implemented `/kanche:git-tag-delete` and `/kanche:git-tag-push` skills.
- Updated the plugin inspector dashboard index file.

## 2026-07-19 — improvements_of_plugins
- Migrated all git side-effect gating (commit, push, branch-delete, tag-create, tag-delete, tag-push, rebase) to use the interactive `default_api:ask_question` tool.

## 2026-09-04 — destructive-safety-and-decoupling
- Enforced strict human confirmation for all destructive Git operations (`git commit`, `git push`, branch deletion, tag deletion, rebase) per `rules/destructive-safety.md`.
- Removed auto-mode bypass branches from Git skills, ensuring skills stand alone safely.
- Unified subagent `@git-operator` on `model: flash`.

