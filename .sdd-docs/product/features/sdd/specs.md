# Specs: Improve SDD Plugins

## Context
This feature improves the Software Development Document (SDD) plugins under `plugins/sdd` to automate Level 2 execution, support double-commit checkpoint policy, enforce conventional branch naming, correct git/github CLI command names, completely remove numerical item IDs in favor of feature slugs, and clean up feature directories upon syncing.

## Scope
- Update `run/SKILL.md` and `continue/SKILL.md` to:
  - Fix git/gh-cli command names.
  - Implement double-commit checkpoints (docs commit after P3, implementation commit after P4).
  - Implement automated Level 2 (P7→P9) execution in `auto` mode.
  - Completely remove item_id and use feature slug directly for directories and branch naming.
- Update `sync/SKILL.md` to:
  - Register as top-level skill command with YAML frontmatter.
  - Sync docs per feature (directly under `product/{slug}/`).
  - Delete temporary development folders post-sync.
  - Commit/push changes.
- Add frontmatter to all other worker skills.

## User stories
- As an Antigravity developer, I want all SDD workflows to use correct Git and GitHub CLI command names so that workflows do not fail.
- As a developer, I want Level 2 phases (human checks, PR checks, and sync) to be automated in auto mode to reduce manual steps.
- As a developer, I want to commit all documentation files together, and all implementation files together, rather than committing at every phase.
- As a developer, I want to use feature slugs directly instead of tracking incremental numeric item IDs.

## Acceptance criteria
1. No workflows refer to deprecated commands like `/git:create-branch`, `/git:create-pr`, or `/git:respond-pr`.
2. Running `/sdd:run` in `auto` mode automatically triggers `/sdd:sync` at the end and deletes the `development/{slug}/` folder.
3. Only two commits are created during the `run` pipeline: one for docs at the end of P3, and one for code changes at the end of P4.
4. Feature directories are structured as `.sdd-docs/development/{slug}/` with no numeric prefix.
5. All worker skills in `plugins/sdd/skills/` have YAML frontmatter blocks.
