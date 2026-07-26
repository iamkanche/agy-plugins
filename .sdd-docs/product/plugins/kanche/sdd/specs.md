---
feature: sdd
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-25
---

# SDD Master Orchestrator Plugin — Consolidated Specification

## Context
Google Antigravity utilizes the `sdd` plugin as a master workflow orchestrator to drive feature implementation through the Software Development Document (SDD) phase model: specifications, design, tasks, build, validation, deploy, and product alignment.

The `sdd` plugin orchestrates domain-specific capabilities provided by dedicated companion plugins:
- **`design`**: Requirements grilling (`/kanche:design-grill`), specs (`/kanche:design-specs`), and system design (`/kanche:design-init`).
- **`planner`**: Task breakdown (`/kanche:planner-tasks`).
- **`dev`**: Code implementation (`/kanche:dev-implement`).
- **`qa`**: Test planning (`/kanche:qa-test-plan`), build reviews (`/kanche:qa-review`), and validation (`/kanche:qa-validate`).
- **`git`**: Branch management, commits, and pushes.
- **`gh-cli`**: Pull request creation, review responses, and automated merging.

## Capabilities
- `/kanche:sdd-run` - Drive a feature work item through the full SDD phase model (P0 to P9) delegating to domain plugins.
- `/kanche:sdd-continue` - Resume the SDD workflow at the phase inferred from on-disk state.
- `/kanche:sdd-sync` - Promote feature documentation to product directory and clean up dev folders.
- `/kanche:sdd-steering` - Analyze repo structure and return steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/kanche:sdd-init` - Bootstrap steering guidelines for the repository.
- `/kanche:sdd-init-update` - Re-analyze repository and refresh guidelines.

## Acceptance Criteria (as-built)
1. Workflow orchestrators (`run` and `continue`) delegate to domain plugin slash commands (`/kanche:design-specs`, `/kanche:design-init`, `/kanche:planner-tasks`, `/kanche:dev-implement`, `/kanche:qa-validate`).
2. Level 2 (P7→P9) execution is automated in `auto` mode to perform validation checks, PR checks, sync, and folder cleanup without prompting.
3. Commits are consolidated into a docs commit after P3 and implementation commit after P4.
4. `/kanche:sdd-sync` copies docs to `.sdd-docs/product/features/{slug}/`, cleans up development folders, and commits/pushes changes.
