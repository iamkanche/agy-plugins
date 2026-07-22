---
name: validate
description: Verify task checklist and run validations.
---

# validator (skill)

**Mission.** Run the project's automated checks — build, tests, lint, and any browser/e2e
checks — for the current feature and return a per-suite pass/fail report with evidence.

## Read

- `.sdd-docs/guidelines/tech.md` — the source of truth for the exact build/test/lint/run
  commands. Discover the commands from here first; fall back to project manifests
  (`Makefile`, `package.json` scripts, `go.mod`, CI configs) only if `tech.md` is silent.
- `.sdd-docs/development/{NNN}_{slug}/{tasks,specs}.md` — the tasks' Verification section and the
  acceptance criteria, so you run the checks that actually cover this feature and know what
  "pass" means.

## Produce

Run each discovered check with bash, capturing exit status and the salient output. Group into
suites (build, unit, integration, lint/format, e2e/browser). For e2e/browser validation:
- First, check if Node.js, npm, and Playwright (`@playwright/test`) are available in the workspace.
- If dependencies or browser binaries are missing, skip the suite and mark it **SKIPPED (missing dependencies)** or **SKIPPED (missing browsers)** with details in the environment notes, rather than claiming a failure.
- If present, run the e2e validation suite (e.g., `npm run test:e2e`). Do not save or write screenshots; verify in-memory/run-time and report test outcomes or page console errors.

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

- Returns DATA to the calling workflow (`/sdd:ai-validation`); does NOT edit code, fix failures,
  commit, push, or orchestrate. Use bash to run checks only — never git write/commit/push,
  never modify source.
- Report results faithfully: never mark something PASS you did not actually run and observe pass.
- Do not attempt to repair a failing suite; report it for the build/loop to address.
- Follow `.sdd-docs/guidelines/rules.md` and the project's output-language policy.
