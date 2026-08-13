---
name: planner-tasks
description: Generate implementation checklist task manifest.
model: pro
---

# /kanche:planner-tasks

**Mission.** Decompose approved `design.md` (and deltas) into an ordered, checkable `tasks.md` body for `.docs/development/{NNN}_{slug}/tasks.md`, incorporating closed-loop feedback from `/kanche:planner-review`.

## Loop Engineering Protocol (Generator Role — P3 Tasks Loop)

In the Loop Engineering Framework, `/kanche:planner-tasks` acts as the **Generator Skill** paired with `/kanche:planner-review`:
- **Iteration 1**: Generates initial task breakdown in `tasks.md`.
- **Iteration 2..N (≤3x Loop)**: Receives `sdd-review` findings (`verdict: NO-GO`, `findings: [{severity, msg, fix_suggestion}]`). Applies targeted task list adjustments resolving ordering, sizing, or coverage findings while preserving already completed `[x]` items.

## Read

- `.docs/development/{NNN}_{slug}/design.md`, `api-diff.md`, `db-diff.md` — what to build.
- `.docs/development/{NNN}_{slug}/specs.md` — so every acceptance criterion has a task and verification check.
- `.docs/guidelines/{tech,structure,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — build/test/lint commands and loop rules.
- `sdd-review` findings from prior review iterations (when running in iteration 2..N).
- Existing `tasks.md` (preserve already-checked `[x]` items when refining).
- The codebase (glob/grep/read) to confirm file locations.

## Produce

Return the `tasks.md` body only, grouped into phases that run in dependency order (Schema/migrations → Backend → API → Frontend → Tests → Docs).

- Every task is a Markdown checkbox `- [ ]` — actionable, single-outcome, and small enough to verify.
- Order strictly by dependency.
- Mark tasks safe to do in parallel with `[P]`.
- Name target file path(s) and trace to acceptance criterion or design component.
- Include verification section sourced from `guidelines/tech.md`.

## Rules

- Returns DATA to the calling workflow (`/kanche:planner-tasks`); does NOT write files, commit, push, or orchestrate. Read-only — no writes/edits.
- Cover the whole design and every acceptance criterion.
- Keep tasks minimal-diff oriented.
- Follow `.docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.

