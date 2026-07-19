# Specifications - SDD Full Automation Development

## Context
Antigravity SDD workflow relies on a systematic phase-gate model (P0 to P9). In order to achieve fully autonomous software engineering, the workflow must be capable of executing all phases with zero human interaction when run in auto mode, using safe defaults and automatic command/edit execution, while preserving product memories and settings.
To optimize token consumption during long-running automated development, the workflow must delegate each phase's tasks to dedicated token-optimized specialized subagents. Additionally, at the start of the workflow (P0), the agent must generate a confirmation receipt detailing branch information and feature metadata for user approval.

## Scope
### In Scope
- Automatic/unattended execution of `/sdd:run` in `auto` mode.
- Integration of `.sdd-docs/settings.json` to configure the automation settings (e.g. loops, polling time, custom commands).
- **Confirmation Receipt (P0)**: Presentation of a structured receipt containing branch name, based branch, target PR branch, title, and short description/slug for user approval before modifying files.
- **Token-Optimized Subagents Delegation**: Delegation of phase-specific work to specialized subagents (`sdd-analyst`, `sdd-architect`, `sdd-planner`, `sdd-coder`, `sdd-validator`) using the system's subagent execution framework to conserve parent agent tokens.
- Full loop automation:
  - Phase P1-P4: Specs, Design, Tasks, Build (up to 3x loops of generate -> review delegated to subagents).
  - Phase P5: Validate & Fix loop (up to 3x loops if validation fails, delegated to subagent).
  - Phase P6-P8: Deploy, PR creation, and PR review comments polling (up to 3x loops of polling for comments, responding/fixing, and pushing).
- Safe automatic execution of Git operations (`git commit`, `git push`, `gh pr create`, `gh pr merge`, etc.) when `auto_approve_commands` is true or when in `auto` mode.
- Post-merge synchronization of feature documents to product guidelines.
- Preservation of `.sdd-docs/product/memory.md` and `.sdd-docs/settings.json` during branch cleanup/merging.
- Summary notification to the user upon completion, including requests for optional feedback/deployment preferences.

### Out of Scope / Non-goals
- Full bypass of system-level permissions (e.g. bypassing the user prompt for BypassSandbox: true if the system itself enforces it, but the workflow should automatically select the bypass parameter or request the command cleanly).
- Automated git pushing to protected branches.

## User Stories
- **As an autonomous developer agent**, I want to execute the complete SDD phase loop (P0 to P9) without blocking on human approvals, so that I can implement features end-to-end completely unattended.
- **As a repository owner**, I want to define automation rules in `settings.json` (such as loop counts and safe command permissions), so that I can control the agent's autonomy.
- **As a developer**, I want to see and approve a feature checkout receipt at the start of the run, so that I have visibility and control over what branch is created and where it is targeted.
- **As a project coordinator**, I want the workflow to delegate phase-specific execution to specialized subagents, so that I save tokens and keep the main context window optimized.
- **As a product manager**, I want the agent to automatically monitor PR feedback, address PR comments, and merge when approved, so that features are shipped without manual intervention.
- **As a product memory manager**, I want the agent to preserve important memories and settings across feature cycles, so that past learnings are not lost.

## Acceptance Criteria
1. **Given** the workflow starts (P0), **When** a new feature branch is about to be checked out, **Then** it must present a structured receipt containing branch name, based branch, target PR branch, title, and short description, and request user confirmation.
2. **Given** the workflow is executing P1 to P5, **When** executing each phase, **Then** it must delegate the tasks to the corresponding specialized subagent (`sdd-analyst`, `sdd-architect`, `sdd-planner`, `sdd-coder`, or `sdd-validator`) with a specialized, minimized context.
3. **Given** the workflow is executed in `auto` mode, **When** any inner phase (Specs, Design, Tasks, Build) returns a `NO-GO` verdict, **Then** it must automatically re-run the generate-and-review loop up to 3 times, passing the findings as context.
4. **Given** the workflow is in `auto` mode, **When** validation (P5) fails, **Then** it must automatically fix the codebase in a validation-fix loop up to 3 times.
5. **Given** the PR is successfully created (P6), **When** in `auto` mode, **Then** the workflow must poll the PR status and comments via GitHub CLI up to 3 times, automatically invoking the PR response/fix flow if new feedback or comments are found.
6. **Given** the PR is approved and checks pass, **When** in `auto` mode, **Then** the workflow must automatically merge the PR.
7. **Given** the workflow is finished, **When** product sync runs, **Then** it must sync feature docs, clean up the development branch/folder, and preserve `memory.md` and `settings.json`.
8. **Given** execution is complete, **When** the agent notifies the user, **Then** it must present a summary of changes, and ask for optional feedback.

## Data Model
### Settings Structure (`.sdd-docs/settings.json`)
- `mode`: String (`"auto"` or `"manual"`)
- `max_loops`: Integer (default: `3`)
- `pr_polling`:
  - `interval_seconds`: Integer (default: `60`)
  - `max_attempts`: Integer (default: `3`)
- `auto_merge`: Boolean (default: `true`)
- `preserve_files`: Array of Strings (default: `["memory.md", "settings.json"]`)

### Product Memory (`.sdd-docs/product/memory.md`)
- Durable memory entries stored as markdown list items.

## NFR (Non-functional Requirements)
- **Token Efficiency**: Subagent context size must not exceed the required workspace context for their respective phases.
- **Security**: The workflow must only execute safe commands automatically. Any command modifying outside the workspace must still require system permission.
- **Resilience**: Network failures during PR polling must not crash the workflow; it should retry or fail gracefully.

## Open Questions
- **How to implement polling delay?**
  - *Assumption*: We will use the `schedule` tool or short wait cycles. Since we are inside the agent execution, we can use `schedule` to wake up or run a series of poll checks.
