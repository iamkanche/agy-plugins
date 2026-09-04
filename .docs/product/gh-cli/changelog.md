# GitHub CLI Plugin — Changelog

<!-- schema: changelog | written by /kanche:sdd-sync -->

## 2026-07-18 — 001_update_plugins
- Implemented `/kanche:pr-merge` with auto branch deletion default.
- Updated `/kanche:pr-create` to auto-assign PRs to creator.
- Updated the plugin inspector dashboard index file.

## 2026-07-19 — improvements_of_plugins
- Migrated all gh-cli side-effect gating (pr-create, pr-approve, pr-merge, pr-respond, pr-review) to use the interactive `default_api:ask_question` tool.

## 2026-09-04 — json-format-and-destructive-safety
- Added `--json` format export and atomic `gh api` review comment submission to `/kanche:gh-cli-pr-review`.
- Standardized review summary structure to `#  Summary` with `## Review Summary` and file/line inline comments.
- Enforced strict human confirmation via `ask_question` for `/kanche:gh-cli-pr-merge` and `/kanche:gh-cli-pr-create`.
- Unified subagent `@gh-operator` on `model: flash`.

