# SDD Plugin — Changelog

<!-- schema: changelog | written by /kanche:sdd-sync -->

## 2026-07-18 — improve-sdd-plugins
- Corrected incorrect git/gh-cli command namespaces in workflows.
- Automated Level 2 phases (P7-P9) in auto mode.
- Aggregated commits into docs-related and implementation-related checkpoints.
- Removed numeric prefix requirements, adopting clean feature slugs.
- Registered all worker skills as top-class Antigravity commands with frontmatter.

## 2026-07-19 — improvements_of_plugins
- Migrated manual phase transitions, validation failures, and LEVEL 2 checkpoints in SDD workflow execution to use the interactive `default_api:ask_question` tool.

## 2026-07-19 — add-sdd-agents
- Defined 5 specialized subagents (`sdd-analyst`, `sdd-architect`, `sdd-planner`, `sdd-coder`, `sdd-validator`) to handle specific phases of the SDD feature lifecycle.
- Configured security-oriented write-permission boundaries (only coder and planner subagents have write privileges).
- Updated the registry dashboard in `index.html` to trace command delegation to the subagents.

## 2026-07-19 — sdd-full-automation-development
- Added verification receipt generation and confirmation gate in Phase P0.
- Implemented phase delegation to specialized, token-optimized subagents (Analyst, Architect, Planner, Coder, Validator) to conserve parent context and tokens.
- Automated 3x retry and response/fix loops for specs/design/tasks/build reviews, validation failures, and PR feedback.
- Configured automatic PR merge on approval and synchronization of feature documentation post-merge.
- Supported settings customization via `docs/settings.json`.

## 2026-07-21 — fix-sdd-ui-containers
- Changed grid template columns layout in root `index.html` and `plugins/sdd/index.html` from fixed fraction boundaries to responsive `minmax(0, 1fr)` tracks to prevent layout blowout under narrow viewports or wide children.
- Added `min-width: 0` to main content and details container elements (`.content-area`, `.details-area`) to allow proper browser shrinking.
- Fixed command card height clipping bug by replacing hardcoded `height: 180px` style with `min-height: 180px` in root dashboard, ensuring no action buttons are cut off.

## 2026-07-25 — human-gated-merge
- Added `auto_merge` setting handling in `docs/settings.json` and workflow skills (`/kanche:sdd-run`, `/kanche:pr-merge`).
- Enforced human confirmation via `default_api:ask_question` for PR merging when `auto_merge: false`.
- Updated durable memory in `docs/product/memory.md` to mandate human-gated PR merging.

## 2026-07-26 — update-sdd-phase-model
- Updated Phase Model diagram layout in sdd-run to position Level 2 below Level 1 in a single vertical progression.
- Mandated forced automatic phase review execution across P1-P4 (`design-specs-review`, `design-review`, `planner-review`, `qa-review`) with retry loops up to 3x (`≤3x`).
- Integrated `/kanche:gh-cli-pr-review` at P6 deploy step to perform automated AI code review against project guidelines immediately after PR creation.

