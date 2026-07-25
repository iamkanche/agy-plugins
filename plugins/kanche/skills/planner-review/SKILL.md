---
name: review
description: Review task manifests and planning breakdown layout.
---

# /planner:review

**Mission.** Critically review `tasks.md` for coverage, dependency ordering, sizing, and
verifiability against the design and specs, and return a GO/NO-GO verdict with findings.

## Read

- `.sdd-docs/development/{NNN}_{slug}/tasks.md` — the list under review.
- `.sdd-docs/development/{NNN}_{slug}/{design,specs,api-diff,db-diff}.md` — to confirm the tasks
  cover the whole design and every acceptance criterion.
- `.sdd-docs/guidelines/{tech,structure,rules}.md` — for correct build/test/lint commands,
  code/test locations, and mandatory rules the tasks must reflect.
- The codebase only to confirm that file paths named by tasks are plausible.

## Produce

Judge against these criteria and record every issue as a finding:

- **Coverage** — every design component, `api-diff` endpoint, and `db-diff` change has a task;
  every acceptance criterion has an implementing task and a verifying (test) task; a lint/format
  task exists.
- **Ordering** — tasks are in dependency-correct order; nothing precedes what it needs;
  `[P]` parallel flags are safe.
- **Sizing & clarity** — each task is single-outcome, concrete, names its target file(s), and is
  small enough to verify; no vague catch-alls.
- **Traceability** — each task references the criterion/component it serves.
- **Verification section** — present, uses real commands from `guidelines/tech.md`, and maps
  each acceptance criterion to a check; no criterion left uncovered.
- **Scope** — no speculative/gold-plating tasks beyond the design.

Return exactly one fenced `sdd-review` block plus a short prose rationale beneath it:

```sdd-review
verdict: GO            # or NO-GO
findings:
  - {severity: blocker|major|nit, msg: "..."}
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`; `nit`-only ⇒ `GO`. Each `msg` is specific and
fixable. If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/sdd:tasks-review`); does NOT edit tasks, commit, push,
  or orchestrate. Read-only — no writes/edits.
- Review only; propose fixes as findings, do not apply them.
- Follow `.sdd-docs/guidelines/rules.md` and the project's output-language policy.
