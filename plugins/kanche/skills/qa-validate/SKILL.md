---
name: qa-validate
description: Verify task checklist and run validations using CLI test runners and MCP Playwright / Chrome DevTools browser automation.
---

# /kanche:qa-validate

**Mission.** Run the project's automated checks — build, unit tests, integration tests, linting, and interactive browser/E2E checks via MCP Playwright — for the current feature and return a per-suite pass/fail report with evidence.

## Read

- `docs/guidelines/tech.md` — the source of truth for the exact build/test/lint/run commands. Discover the commands from here first; fall back to project manifests (`Makefile`, `package.json` scripts, `go.mod`, CI configs) only if `tech.md` is silent.
- `docs/development/{slug}/{tasks,specs}.md` — the tasks' Verification section and the acceptance criteria, so you run the checks that actually cover this feature and know what "pass" means.

## Produce

Run each discovered check via CLI bash or MCP browser automation tools:

1. **CLI Test Runners.** Execute build, unit, integration, and lint commands using `bash`, capturing exit status and output.
2. **MCP Playwright / Browser E2E Automation.** When E2E/UI checks or Playwright configs (`playwright.config.*`, `cypress.config.*`, `e2e/`) exist:
   - Ensure target application or local dev server is running.
   - Use Playwright MCP tools (`browser_navigate`, `browser_screenshot`, `browser_click`, `browser_type`, `browser_console`) to execute visual workflow checks, capture screenshot evidence, and verify console errors.
   - Run `npx playwright test` or project-specific E2E commands if pre-configured.

Return a **validation report** (chat data, not a file):

- **Summary line** — overall PASS/FAIL and counts (e.g. `5 suites: 4 pass, 1 fail`).
- **Per-suite table/rows** — suite name · tool/command run · PASS/FAIL/SKIPPED/NOT-RUN · key metrics (tests run/failed, lint errors, browser visual status).
- **Failures** — for each failing suite, the failing test/rule names, browser console errors, and relevant log excerpts.
- **Coverage vs. acceptance criteria** — which criteria are exercised by passing checks and which require human manual review.
- **Environment notes** — missing dependencies, server URLs, or skipped suites.

## Rules

- Returns DATA to the calling workflow (`/kanche:qa-validate`); does NOT edit code, fix failures, commit, push, or orchestrate.
- Report results faithfully: never mark something PASS you did not actually run and observe pass.
- Do not attempt to repair a failing suite; report it for the build/loop to address.
- Follow `docs/guidelines/rules.md` and the project's output-language policy.
