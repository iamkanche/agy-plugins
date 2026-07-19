---
feature: sdd
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
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

## Specialized SDD Subagents
To minimize parent token bloat and establish safety boundaries, the SDD plugin exposes 5 specialized subagents:
- `sdd-analyst`: Handles feature interrogation, specs drafting, and specs review (`grill`, `specs`, `specs-review`). Read-only tools.
- `sdd-architect`: Handles architecture design and design review (`design`, `design-review`). Read-only tools.
- `sdd-planner`: Handles guideline bootstrap, repository updates, tasks drafting, and tasks review (`init`, `init-update`, `steering`, `tasks`, `tasks-review`). Write tools enabled.
- `sdd-coder`: Handles code implementation and implementation code review (`build`, `build-review`). Write tools enabled.
- `sdd-validator`: Handles validation, deployment/alignment actions, and overall workflow run control (`validate`, `sync`, `continue`, `run`). Read-only tools.

## Interactive Skill Connections Map
Introduces a graphical connection map to the sdd plugin dashboard showing relations and execution flow between sdd, git, and gh-cli commands, with real-time path tracing and details panel integration.

## Acceptance criteria (as-built)
1. Workflow orchestrators (`run` and `continue`) use updated correct namespaces (`/git:branch-create`, `/gh-cli:pr-create`, `/gh-cli:pr-respond`).
2. Level 2 (P7→P9) execution is automated in `auto` mode to perform validation checks, PR checks, sync, and folder cleanup without prompting.
3. Commits are consolidated into a docs commit after P3 and implementation commit after P4.
4. Feature folders and branches are named directly using feature slugs without numeric prefix.
5. `/sdd:sync` copies docs to `.sdd-docs/product/features/{slug}/`, cleans up development folders, and commits/pushes the changes.
6. Manual phase transitions and validation checkpoints use the interactive `default_api:ask_question` tool for confirmations.
7. Presents a structured verification receipt (branch, base, target, title, slug) for user approval in P0 before checkout.
8. Spawns specialized, token-optimized subagents (Analyst, Architect, Planner, Coder, Validator) to execute phase-specific tasks and reviews to conserve parent tokens.
9. Automates 3x retry and response/fix loops for specs/design/tasks/build reviews, validation failures, and PR comments polling/fixing.
10. Automatically merges PR on approval, syncs feature documentation post-merge, and preserves settings/memory.
11. Declarative subagent configuration files (`agent.json`) are structured under the `plugins/sdd/agents/{agent-name}/` directories, register via `plugins/sdd/plugin.json`, and trace dynamically in the registry dashboard in `index.html`.
12. Dashboard renders an Interactive Skill Connections Map containing all 35 sdd, git, and gh-cli commands linked via Cubic/Quadratic Bezier path arrows.
13. Hovering over a command highlights its direct incoming/outgoing paths, displays details in the sidebar, and dims unrelated nodes/edges to 0.15/0.05 opacity.
14. Highlighted connection paths animate dashed strokes in the direction of flow.
15. Clicking a command locks the path highlights and details panel, synchronizing with the sidebar selection.
16. Supports tab cycling and spatial Euclidean keyboard navigation for Arrow keys alongside Enter/Space actions.
17. Sidebar items group command buttons dynamically by plugin with distinct headers.
