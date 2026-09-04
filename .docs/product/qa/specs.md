---
feature: qa
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# QA & Validation Plugin — Consolidated Specification

## Context
The `qa` plugin packages automated testing, test plan creation, build code reviews, and quality validation workflows for Google Antigravity agents.

## Capabilities
- `/kanche:qa-validate`: Run static analysis checks, linters, compilers, CLI test suites, and Playwright MCP browser automation.
- `/kanche:qa-test-plan`: Generate comprehensive test plan matrices, edge-case scenarios, test case specs, and Playwright E2E visual matrices.
- `/kanche:qa-review`: Perform review on implementation code modifications diff before staging, emitting `review-verdict`.
- `/kanche:code-review`: Perform deep static code reviews with auto-fix recommendations, emitting `review-verdict`.
- `/kanche:security-scan`: Scan codebase for hardcoded secrets, dependency vulnerabilities, and anti-patterns.

## Specialized Subagents
- `@validator`: Handles validation execution, linter runs, test suite verification, and human verification checklists.
- `@tester`: Formulates test strategies, unit/integration stubs, and browser test automation.
- `@reviewer`: Performs rigorous code review and quality audits.
- `@security-engineer`: Performs secret detection and vulnerability scanning.
All subagents configured with `model: flash`.

## Acceptance Criteria (as-built)
1. Exposes `/kanche:qa-validate`, `/kanche:qa-test-plan`, `/kanche:qa-review`, `/kanche:code-review`, and `/kanche:security-scan` commands.
2. Emits and consumes universal `review-verdict` protocol blocks (`verdict: GO` | `NO-GO`).
3. Registers subagents `@validator`, `@tester`, `@reviewer`, and `@security-engineer` in `plugins/kanche/plugin.json`.
4. Integrates with `/kanche:sdd-run` orchestrator for P3 (Test Plan), P4 (Review), and P5 (Validation) phases.

