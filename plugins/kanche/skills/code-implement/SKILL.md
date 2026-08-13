---
name: code-implement
description: Implement target code changes incrementally, execute closed-loop fixes from reviews, and run tests.
model: flash
---

# /kanche:code-implement

**Mission.** Implement the feature exactly as laid out in `tasks.md`, writing real code with a
minimal diff, execute closed-loop fixes when handling review findings from `/kanche:code-review` or `/kanche:qa-review`, then return a change summary and task completion status. This is the primary skill that edits source files — it still does **not** commit, push, or orchestrate.

## Loop Engineering Protocol (Generator Role — P4 Build Loop)

In the Loop Engineering Framework, `/kanche:code-implement` acts as the **Generator & Fixer Skill** paired with Evaluator skills (`/kanche:code-review` / `/kanche:qa-review`):
- **Iteration 1**: Implements initial code and tests from `tasks.md`.
- **Iteration 2..N (≤3x Loop)**: Receives `sdd-review` findings (`verdict: NO-GO`, `findings: [{severity, msg, file, line, fix_suggestion}]`) or test failure reports from previous review/validation runs.
- **Targeted Delta Fixes**: Applies minimal, focused changes strictly resolving reported `blocker` and `major` findings without introducing unrequested refactors or regressions to passing tests.

## Read

- `.docs/development/{NNN}_{slug}/tasks.md` — the ordered work list; this is your plan of record.
- `.docs/development/{NNN}_{slug}/{design,specs,api-diff,db-diff}.md` — for the interfaces, contracts, and acceptance criteria each task must satisfy.
- `.docs/guidelines/{tech,structure,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — stack conventions, loop rules, where code/tests live, mandatory rules, and build/test/lint commands.
- `sdd-review` findings or test execution logs from prior loop iterations (when running in iteration 2..N).
- The actual source files each task names, plus their existing patterns and neighbors, before changing them.

## Produce

Work through `tasks.md` in order, respecting dependencies; do `[P]` tasks in any order. For each task (or loop feedback item): make the smallest change that satisfies it, following existing patterns and guidelines. Add/adjust tests as tasks specify. Check off completed items by editing `tasks.md` (`- [ ]` → `- [x]`). Run the build/lint/test commands from `guidelines/tech.md` to confirm changes compile and pass locally.

Then return (as chat data, not a file) a **change summary**:

- **Loop Iteration & Status** — current iteration number (e.g. Iteration N/3) and whether this run was initial implementation or review finding remediation.
- **Tasks completed** — the checked task ids, and any left unchecked with the reason (blocked, needs decision, out of scope).
- **Files changed & delta fixes** — path + one-line what-and-why per file (created/modified/deleted), referencing specific `sdd-review` findings resolved.
- **Commands run & results** — build/test/lint invocations and their pass/fail outcome.
- **Deviations & follow-ups** — anywhere the implementation departed from the design/tasks and why, plus anything discovered that belongs in a later task or a doc-sync.

## Rules

- Returns DATA (the change summary) to the calling workflow (`/kanche:code-implement`). It DOES write code files and may update `tasks.md` checkboxes, but does NOT commit, push, or orchestrate — the workflow owns git side effects.
- Minimal diff: implement only what the tasks or review findings require. No speculative refactors, renames, or scope beyond `tasks.md` or review findings.
- Zero-regression rule: when fixing review findings in loop iterations 2..N, verify that previously passing tests and criteria remain green.
- Never commit secrets (`.env`, credentials, keys). Never run git write/commit/push commands.
- If a task is ambiguous or conflicts with the design, stop and report it rather than guessing.
- Follow `.docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.

