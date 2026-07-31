---
name: qa-validate
description: Verify task checklist and run validations using CLI test runners and MCP Playwright / Chrome DevTools browser automation with self-healing repair loops.
---

# /kanche:qa-validate

**Mission.** Run the project's automated checks — build, unit tests, integration tests, linting, interactive browser/E2E checks via MCP Playwright, and accessibility/performance checks via Chrome DevTools MCP — for the current feature and return a per-suite pass/fail report with evidence, driving the closed-loop self-healing validation & fix cycle with `/kanche:code-implement`.

## Loop Engineering Protocol (Evaluator Role — P5 Validation & Self-Healing Loop)

In the Loop Engineering Framework, `/kanche:qa-validate` acts as the **Validation Evaluator Skill** paired with `/kanche:code-implement` (Fixer):
- Executes all CLI test runners, Playwright E2E visual checks, and Chrome DevTools MCP audits.
- Returns a structured validation report detailing passed/failed suites.
- **Self-Healing Loop (<=3x Iterations)**: When validation fails, automatically feeds failing log excerpts, stack traces, and test signatures into `/kanche:code-implement` in Phase P4 to apply targeted fixes and re-trigger validation for up to 3 repair cycles before human escalation.

## Read

- `docs/guidelines/tech.md` and `plugins/kanche/rules/loop-engineering.md` — source of truth for build/test/lint commands, loop rules, and model tiering.
- `docs/development/{slug}/{tasks,specs}.md` — the tasks' Verification section and acceptance criteria.

## Produce

Run each discovered check via CLI bash or MCP browser automation tools:

1. **CLI Test Runners.** Execute build, unit, integration, and lint commands using `bash`, capturing exit status and output.
2. **MCP Playwright / Browser E2E Automation.** When E2E/UI checks exist:
   - Ensure target application or local dev server is running.
   - Use Playwright MCP tools (`browser_navigate`, `browser_screenshot`, `browser_click`, `browser_type`, `browser_console`) to execute visual workflow checks, capture screenshot evidence, and verify console errors.
   - Run `npx playwright test` or project-specific E2E commands if pre-configured.
3. **Chrome DevTools MCP Auditing.**
   - Accessibility Audits: Execute `a11y-debugging` guidelines for ARIA labels, focus states, tap targets, and color contrast.
   - Core Web Vitals: Execute `debug-optimize-lcp` to check LCP rendering and page load speed.

Return a **validation report** (chat data, not a file):

- **Summary line** — overall PASS/FAIL and counts (e.g. `5 suites: 4 pass, 1 fail`).
- **Per-suite table/rows** — suite name · tool/command run · PASS/FAIL/SKIPPED/NOT-RUN · key metrics.
- **Failures & Self-Healing Fix Hints** — for each failing suite, the failing test/rule names, browser console errors, relevant log excerpts, and actionable fix hints for `/kanche:code-implement`.
- **Coverage vs. acceptance criteria** — which criteria are exercised by passing checks and which require human manual review.
- **Environment notes** — missing dependencies, server URLs, or skipped suites.

## Rules

- Returns DATA to the calling workflow (`/kanche:qa-validate`); does NOT directly commit, push, or alter git branches.
- Report results faithfully: never mark something PASS you did not actually run and observe pass.
- In case of failures, automatically trigger the 3-cycle self-healing repair loop with `/kanche:code-implement`.
- Follow `docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.
