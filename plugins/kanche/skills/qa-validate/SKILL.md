---
name: qa-validate
description: Verify task checklist and run validations.
---

# /kanche:qa-validate

**Mission.** Run the project's automated checks — build, tests, lint, and any browser/e2e
checks — for the current feature and return a per-suite pass/fail report with evidence.

## Read

- `docs/guidelines/tech.md` — the source of truth for the exact build/test/lint/run
  commands. Discover the commands from here first; fall back to project manifests
  (`Makefile`, `package.json` scripts, `go.mod`, CI configs) only if `tech.md` is silent.
- `docs/development/{NNN}_{slug}/{tasks,specs}.md` — the tasks' Verification section and the
  acceptance criteria, so you run the checks that actually cover this feature and know what
  "pass" means.

## Produce

Run each discovered check with bash, capturing exit status and the salient output. Group into
suites (build, unit, integration, lint/format, e2e/browser). For browser/e2e: run only if the
project defines such checks and a runtime is available; if an interactive browser check is
required but not runnable here, mark it **not run (needs browser)** rather than claiming a result.

Return a **validation report** (chat data, not a file):

- **Summary line** — overall PASS/FAIL and counts (e.g. `4 suites: 3 pass, 1 fail`).
- **Per-suite table/rows** — suite name · command run · PASS/FAIL/SKIPPED/NOT-RUN · key numbers
  (tests run/failed, lint errors).
- **Failures** — for each failing suite, the failing test/rule names and the relevant log
  excerpt (trimmed), enough to locate the cause.
- **Coverage vs. acceptance criteria** — which criteria are exercised by a passing check and
  which are not covered by any automated check (so the human knows what still needs manual
  validation).
- **Environment notes** — anything that affected the run (missing deps, skipped suites and why).

## Rules

- Returns DATA to the calling workflow (`/kanche:qa-validate`); does NOT edit code, fix failures,
  commit, push, or orchestrate. Use bash to run checks only — never git write/commit/push,
  never modify source.
- Report results faithfully: never mark something PASS you did not actually run and observe pass.
- Do not attempt to repair a failing suite; report it for the build/loop to address.
- Follow `docs/guidelines/rules.md` and the project's output-language policy.
