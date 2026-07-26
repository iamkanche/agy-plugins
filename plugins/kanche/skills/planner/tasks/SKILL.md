---
name: planner-tasks
description: Generate implementation checklist task manifest.
---

# /kanche:planner-tasks

**Mission.** Decompose the approved `design.md` (and its deltas) into an ordered, dependency-
correct, checkable `tasks.md` body for `.sdd-docs/development/{NNN}_{slug}/tasks.md` that
`build` can execute top-to-bottom.

## Read

- `.sdd-docs/development/{NNN}_{slug}/design.md`, `api-diff.md`, `db-diff.md` — what to build.
- `.sdd-docs/development/{NNN}_{slug}/specs.md` — so every acceptance criterion has a task that
  makes it true and a task that verifies it.
- `.sdd-docs/guidelines/{tech,structure,rules}.md` — build/test/lint commands, where code and
  tests live, mandatory rules.
- Existing `tasks.md` (preserve already-checked `[x]` items when refining).
- The codebase (glob/grep/read) only to confirm file locations the tasks will name.

## Produce

Return the `tasks.md` body only, grouped into **phases** that run in dependency order (e.g.
Schema/migrations → Backend → API → Frontend → Tests → Docs — adapt to the actual design). Rules
for the list:

- Every task is a Markdown checkbox `- [ ]` — actionable, single-outcome, and small enough to
  verify. Number phases; keep tasks concrete ("Add `X` to `path/to/file`").
- Order strictly by dependency; a task never precedes something it needs.
- Mark tasks safe to do in parallel with `[P]`.
- Name the target file path(s) for each task where known, and the acceptance criterion or
  design component it implements (traceability).
- Include a task for each schema change (from `db-diff.md`) and each endpoint (from
  `api-diff.md`), plus tasks for tests covering the acceptance criteria and a lint/format task.

End with a **Verification** section: the exact commands to prove the feature is done — build,
unit/integration tests, lint, and any manual/browser checks — sourced from `guidelines/tech.md`.
Map each acceptance criterion to the check that covers it, and call out any criterion not yet
covered.

## Rules

- Returns DATA to the calling workflow (`/kanche:planner-tasks`); does NOT write files, commit, push, or
  orchestrate. Read-only — no writes/edits.
- Cover the whole design and every acceptance criterion; flag any gap instead of quietly
  dropping it. Do not invent work beyond the design.
- Keep tasks minimal-diff oriented — no speculative refactors or gold-plating.
- Follow `.sdd-docs/guidelines/rules.md` and the project's output-language policy.
