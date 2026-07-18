---
feature: sdd
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-18
---

# SDD Plugin — Consolidated Specification

<!-- schema: specs | written by /sdd:sync-product (dev-only sections stripped) -->

## Context
Google Antigravity utilizes the `sdd` plugin to drive feature implementation through the Software Development Document (SDD) model: specifications, design, tasks, build, validation, deploy, and product alignment.

## Capabilities
- `/sdd:run` - Drive a feature work item through the full SDD phase model (P0 to P9).
- `/sdd:continue` - Resume the SDD workflow at the phase inferred from on-disk state.
- `/sdd:sync` - Promote feature documentation to product directory and clean up dev folders.
- `/sdd:init` - Scan the repository and bootstrap initial guidelines documents.
- `/sdd:init-update` - Re-analyze repository and refresh guidelines.
- Other worker skills (`/sdd:steering`, `/sdd:grill`, `/sdd:specs`, `/sdd:design`, `/sdd:tasks`, `/sdd:build`, `/sdd:specs-review`, `/sdd:design-review`, `/sdd:tasks-review`, `/sdd:build-review`, `/sdd:validate`).

## Acceptance criteria (as-built)
1. Workflow orchestrators (`run` and `continue`) use updated correct namespaces (`/git:branch-create`, `/gh-cli:pr-create`, `/gh-cli:pr-respond`).
2. Level 2 (P7→P9) execution is automated in `auto` mode to perform validation checks, PR checks, sync, and folder cleanup without prompting.
3. Commits are consolidated into a docs commit after P3 and implementation commit after P4.
4. Feature folders and branches are named directly using feature slugs without numeric prefix.
5. `/sdd:sync` copies docs to `.sdd-docs/product/features/{slug}/`, cleans up development folders, and commits/pushes the changes.
