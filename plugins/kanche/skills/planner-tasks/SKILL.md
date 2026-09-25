---
name: planner-tasks
description: Generate implementation checklist task manifest organized by Topological Dependency Tiers.
model: flash
---

# /kanche:planner-tasks

**Mission.** Decompose approved `design.md` (and deltas) into an ordered, checkable `tasks.md` body for `.docs/development/{NNN}_{slug}/tasks.md`, organized strictly by **Topological Dependency Tiers**, incorporating closed-loop feedback from `/kanche:planner-review`.

## Loop Engineering Protocol (Generator Role — Task Planning Loop)

In the Loop Engineering Framework, `/kanche:planner-tasks` acts as the **Generator Skill** paired with `/kanche:planner-review`:
- **Iteration 1**: Generates initial task breakdown in `tasks.md` ordered by Topological Dependency Tiers.
- **Iteration 2..N (≤3x Loop)**: Receives `review-verdict` findings (`verdict: NO-GO`, `findings: [{severity, msg, fix_suggestion}]`). Applies targeted task list adjustments resolving ordering, sizing, or coverage findings while preserving already completed `[x]` items.

## Read

- `.docs/development/{NNN}_{slug}/design.md`, `api-diff.md`, `db-diff.md` — what to build and architectural entity relationships.
- `.docs/development/{NNN}_{slug}/specs.md` — so every acceptance criterion has a task and verification check.
- `.docs/guidelines/{tech,structure,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — build/test/lint commands, loop rules, and topological DAG protocol.
- `review-verdict` findings from prior review iterations (when running in iteration 2..N).
- Existing `tasks.md` (preserve already-checked `[x]` items when refining).
- The codebase (glob/grep/read) to confirm file locations.

## Produce: Topological Dependency Tiers

Return the `tasks.md` body only, grouped into strict **Topological Dependency Tiers**:
- **Tier 0: Models, Contracts & Core Schemas** — foundational types, database migrations, base configurations, and interface contracts.
- **Tier 1: Core Services & Repositories** — business logic, domain services, and data access layers.
- **Tier 2: Presentation & Controllers** — HTTP/API controllers, CLI endpoints, UI components, and client-side integrations.
- **Tier 3: E2E Tests & Documentation** — integration tests, Playwright MCP E2E tests, user documentation, and showcase views.

Task Formatting Rules:
- Every task is a Markdown checkbox `- [ ]` — actionable, single-outcome, and minimal-diff oriented.
- Mark tasks safe to execute concurrently within the same tier with `[P]`.
- Name target file path(s) and trace to acceptance criteria or design components.
- Include a Verification Checkpoint section with automated commands sourced from `guidelines/tech.md`.

## Rules

- Returns DATA to the calling workflow (`/kanche:planner-tasks`); does NOT write files, commit, push, or orchestrate. Read-only.
- Cover the entire design and every acceptance criterion.
- Follow `.docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.
