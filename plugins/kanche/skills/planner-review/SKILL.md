---
name: planner-review
description: Review task manifests and planning breakdown layout.
---

# /kanche:planner-review

**Mission.** Critically review `tasks.md` for coverage, dependency ordering, sizing, and verifiability, returning a GO/NO-GO verdict with findings for closed-loop iteration with `/kanche:planner-tasks`.

## Loop Engineering Protocol (Reviewer Role — P3 Tasks Loop)

In the Loop Engineering Framework, `/kanche:planner-review` acts as the **Reviewer Skill** paired with `/kanche:planner-tasks`:
- Audits `tasks.md` for complete design coverage, valid dependency order, concrete file targeting, and verification setup.
- Emits structured `sdd-review` block consumed by `/kanche:planner-tasks` during retry loops (up to 3x).

## Read

- `docs/development/{NNN}_{slug}/tasks.md` — the list under review.
- `docs/development/{NNN}_{slug}/{design,specs,api-diff,db-diff}.md` — to confirm tasks cover whole design.
- `docs/guidelines/{tech,structure,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — build/test/lint commands and loop rules.
- The codebase to confirm file paths are plausible.

## Produce

Judge against these criteria and record every issue as a finding:

- **Coverage** — every design component, endpoint, schema change, and criterion has an implementing task and verification check.
- **Ordering** — tasks are in dependency-correct order.
- **Sizing & clarity** — single-outcome tasks naming concrete target files.
- **Verification section** — present with real commands and criterion mapping.

Return exactly one fenced `sdd-review` block plus a short prose rationale beneath it:

```sdd-review
verdict: GO            # or NO-GO
loop_iteration: 1/3    # current iteration / max_loops
findings:
  - severity: blocker  # blocker | major | nit
    msg: "Description of issue"
    file: "docs/development/{slug}/tasks.md"
    line: 18
    fix_suggestion: "Concrete guidance to fix task breakdown"
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`; `nit`-only ⇒ `GO`. Each `msg` is specific and fixable. If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/kanche:planner-review`); does NOT edit tasks, commit, push, or orchestrate. Read-only — no writes/edits.
- Review only; propose fixes as findings, do not apply them.
- Follow `docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.

