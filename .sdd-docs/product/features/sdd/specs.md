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

## P9 Alignment Sequence Optimization
Reorders Level 2 P9 to execute `/sdd:sync` on the feature branch before PR merge, consolidating all changes into a single PR.

### Acceptance Criteria
18. After PR approval in P9 auto mode, `/sdd:run` executes `/sdd:sync` locally on the feature branch, commits and pushes the sync changes to the remote feature branch.
19. After sync is pushed, `/sdd:run` polls CI/status checks using `pr_polling` settings from `.sdd-docs/settings.json` (default: 30s interval, 3 max attempts) before merging.
20. Once status checks pass, `/sdd:run` invokes `/gh-cli:pr-merge` (no `--keep-branch`) to merge the PR and delete both local and remote branches.
21. In manual mode, P9 presents two separate confirmation gates: (1) sync gate, (2) merge gate.
22. The connections map in `index.html` routes: `/gh-cli:pr-approve` → `/sdd:sync` (1080,540) → `/gh-cli:pr-merge` (1080,640).
23. The `/sdd:run` command details panel lists P7 (Human Review), P8 (PR Feedback & Approval), and P9 (Sync & Merge) steps.

## Fully AI-Automated Workflow
Removes interactive `default_api:ask_question` confirmation gates when running in auto mode, while keeping manual mode gates and safety invariants.

### Acceptance Criteria
24. In auto mode, the `default_api:ask_question` gate is bypassed for all side effects (git commit, git push, git branch-delete, gh pr-create, gh pr-merge, and gh pr-respond); instead, actions are logged and executed automatically.
25. In manual mode, all existing interactive gating behavior is preserved exactly.
26. All safety invariants (protected-branch refusal, force-push ban, pre-commit bypass hooks ban, secrets checks, self-approval ban, etc.) remain unconditionally active in all execution modes.
27. Gated operations must still be done using formal plugin slash command workflows rather than raw commands.
28. guidelines/product.md has L23 out-of-scope entry removed; auto-mode SDD added to In-Scope.
29. guidelines/rules.md L4 and L14 updated to define gates as mode-conditional.
30. guidelines/tech.md L28-29 updated to reflect mode-conditional gating.
31. plugins/sdd/rules/workflow-gating.md L7 Side Effect Confirmation updated to mode-conditional.
32. plugins/git/rules/git-hard-rules.md L14 rewritten to be mode-conditional.
33. plugins/gh-cli/rules/gh-hard-rules.md L9 rewritten to be mode-conditional.
34. plugins/sdd/skills/run/SKILL.md updated to display the feature receipt as a log in auto mode (no prompt), and references to confirmation prompts are removed from P3/P4 commits, P6 push/PR-create.
35. plugins/git/skills/commit/SKILL.md Gate step 7 conditionalized with standard clause, Done-when updated.
36. plugins/git/skills/push/SKILL.md Gate step 5 conditionalized with standard clause, Done-when updated.
37. plugins/git/skills/branch-delete/SKILL.md Gate step 5 conditionalized with standard clause, Done-when and narrative updated.
38. plugins/gh-cli/skills/pr-create/SKILL.md Gate step 6 conditionalized with standard clause, Done-when updated.
39. plugins/gh-cli/skills/pr-merge/SKILL.md Gate step 4 conditionalized with standard clause, Done-when updated.
40. plugins/gh-cli/skills/pr-respond/SKILL.md Gate steps 5 and 8 conditionalized with standard clause, Done-when updated.
41. No document contains a rule that contradicts any other document on the subject of gating.

## Command Arguments & Usage Samples in Dashboard
Adds examples of CLI command syntax and arguments to the interactive skills connection dashboard.

### Acceptance Criteria
42. A labeled "Arguments / Usage Sample" section is rendered in the details sidebar header section when a command that defines a `usage` property is selected.
43. The usage example text is displayed inside a code snippet box matching `.code-snippet` styling.
44. If a command does not define a `usage` property, no usage section or label is displayed.
45. `/sdd:run` specifies: `/sdd:run <slug> [--mode=auto|manual] [--from=<phase>] [--until=<phase>]`
46. `/sdd:continue` specifies: `/sdd:continue [--mode=auto|manual] [--from=<phase>] [--until=<phase>] [<slug>]`
47. `/git:branch-create` specifies: `/git:branch-create <branch-name>`
48. `/git:branch-delete` specifies: `/git:branch-delete <branch-name> [--remote]`
49. `/git:commit` specifies: `/git:commit`
50. `/git:push` specifies: `/git:push [--set-upstream]`
51. `/git:pull` specifies: `/git:pull`
52. `/git:rebase` specifies: `/git:rebase <target-branch>`
53. `/git:stash` specifies: `/git:stash [push|pop|list|clear]`
54. `/git:switch` specifies: `/git:switch <branch-name>`
55. `/gh-cli:pr-create` specifies: `/gh-cli:pr-create [--title=<title>] [--body=<body>] [--draft] [--base=<branch>]`
56. `/gh-cli:pr-merge` specifies: `/gh-cli:pr-merge [<pr-number>] [--squash|--rebase|--merge] [--keep-branch]`
57. `/gh-cli:pr-respond` specifies: `/gh-cli:pr-respond [<pr-number>]`
58. `/gh-cli:pr-approve` specifies: `/gh-cli:pr-approve [<pr-number>]`
59. All other commands in the dashboard registry carry descriptive usage example strings where applicable.

## Fix Grid Column Blowouts & Card Text Clipping
Resolves layout container viewport overflow and command card bottom clipping.

### Acceptance Criteria
60. Given a desktop or laptop viewport, when the root `index.html` or `plugins/sdd/index.html` is loaded, the page grid template layout columns stay confined to the viewport width without causing horizontal scrollbars on the document body.
61. Flex and grid item content areas (`.content-area` and `.details-area`) use `min-width: 0` and `minmax(0, 1fr)` to enable layout column shrinking.
62. The Interactive Skill Connections Map SVG element and pipeline steps container scroll locally inside scrollable containers instead of expanding grid track width.
63. The command card height is responsive using `min-height: 180px` in root `index.html`, allowing the cards to expand vertically for long text descriptions and ensuring no bottom buttons are clipped.
