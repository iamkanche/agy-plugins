---
name: qa-review
description: Audit code quality, implementation diffs, and test coverage.
---

# /kanche:qa-review

**Mission.** Review the implementation produced by `build` for correctness, spec/design
conformance, and code quality — using read-only checks and, where useful, a browser — and return
a GO/NO-GO verdict with findings.

## Read

- The change under review: `git diff` / `git status` against the feature branch's base (use
  read-only git commands only) plus the changed source files.
- `docs/development/{NNN}_{slug}/{tasks,design,specs,api-diff,db-diff}.md` — to verify the
  code matches what was specified/designed and that every checked task is actually done.
- `docs/guidelines/{tech,structure,rules}.md` — for conventions, mandatory rules, and the
  build/test/lint commands.

## Produce

Assess and record every issue as a finding:

- **Correctness** — the code does what the acceptance criteria require; edge/error cases handled;
  no obvious bugs, race conditions, or resource leaks.
- **Conformance** — matches the design's interfaces and the `api-diff`/`db-diff`; checked-off
  tasks are genuinely complete.
- **Quality & rules** — follows `guidelines/rules.md` and repo conventions; minimal diff, no
  gold-plating; no secrets committed; adequate tests for the new behavior.
- **Verification evidence** — run read-only build/test/lint commands from `guidelines/tech.md`;
  report their outcome. For UI changes, drive the running app in a browser only if a dev server
  is already available, and describe what you observed. If a browser check is required but not
  runnable here, record it as a finding for the workflow/human to run — do not claim to have run it.

Return exactly one fenced `sdd-review` block plus a short prose rationale (and any command
output that supports it) beneath:

```sdd-review
verdict: GO            # or NO-GO
findings:
  - {severity: blocker|major|nit, msg: "..."}
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`; `nit`-only ⇒ `GO`. Each `msg` is specific and
fixable (file:line where possible). If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/kanche:qa-review`); does NOT edit code, commit, push,
  or orchestrate. Use bash for read-only inspection/tests only — never git write/commit/push.
- Review only; propose fixes as findings, do not apply them.
- Do not overstate verification: report exactly which checks you actually ran and their results.
- Follow `docs/guidelines/rules.md` and the project's output-language policy.
