---
name: implement
description: Implement target code changes incrementally and run tests.
---

# /dev:implement

**Mission.** Implement the feature exactly as laid out in `tasks.md`, writing real code with a
minimal diff, then return a change summary and which tasks are now complete. This is the one
skill that edits source files — it still does **not** commit, push, or orchestrate.

## Read

- `.sdd-docs/development/{NNN}_{slug}/tasks.md` — the ordered work list; this is your plan of
  record.
- `.sdd-docs/development/{NNN}_{slug}/{design,specs,api-diff,db-diff}.md` — for the interfaces,
  contracts, and acceptance criteria each task must satisfy.
- `.sdd-docs/guidelines/{tech,structure,rules}.md` — stack, conventions, where code/tests live,
  mandatory rules, and the build/test/lint commands.
- The actual source files each task names, plus their existing patterns and neighbors, before
  changing them.

## Produce

Work through `tasks.md` in order, respecting dependencies; do `[P]` tasks in any order. For each
task: make the smallest change that satisfies it, following existing patterns and the
guidelines. Add/adjust tests as the tasks specify. Check off completed items by editing
`tasks.md` (`- [ ]` → `- [x]`). Run the build/lint/test commands from `guidelines/tech.md` to
confirm your changes compile and pass locally.

Then return (as chat data, not a file) a **change summary**:

- **Tasks completed** — the checked task ids, and any left unchecked with the reason (blocked,
  needs decision, out of scope).
- **Files changed** — path + one-line what-and-why per file (created/modified/deleted).
- **Commands run & results** — build/test/lint invocations and their pass/fail outcome.
- **Deviations & follow-ups** — anywhere the implementation departed from the design/tasks and
  why, plus anything discovered that belongs in a later task or a doc-sync.

## Rules

- Returns DATA (the change summary) to the calling workflow (`/sdd:build`). It DOES write code
  files and may update `tasks.md` checkboxes, but does NOT commit, push, or orchestrate — the
  workflow owns git side effects.
- Minimal diff: implement only what the tasks require. No speculative refactors, renames, or
  scope beyond `tasks.md`; surface such ideas as follow-ups.
- Never commit secrets (`.env`, credentials, keys). Never run git write/commit/push commands.
- If a task is ambiguous or conflicts with the design, stop and report it rather than guessing.
- Follow `.sdd-docs/guidelines/rules.md` and the project's output-language policy.
