# GitHub CLI Plugin — Changelog

<!-- schema: changelog | written by /kanche:sdd-sync -->

## 2026-07-18 — 001_update_plugins
- Implemented `/kanche:pr-merge` with auto branch deletion default.
- Updated `/kanche:pr-create` to auto-assign PRs to creator.
- Updated the plugin inspector dashboard index file.

## 2026-07-19 — improvements_of_plugins
- Migrated all gh-cli side-effect gating (pr-create, pr-approve, pr-merge, pr-respond, pr-review) to use the interactive `default_api:ask_question` tool.
