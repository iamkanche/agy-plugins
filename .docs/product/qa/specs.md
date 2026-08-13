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
- `/kanche:qa-validate` - Run static analysis checks, linters, compilers, and test suites.
- `/kanche:qa-test-plan` - Generate comprehensive test plan matrices, edge-case scenarios, and test case specs.
- `/kanche:qa-review` - Perform review on implementation code modifications diff before staging.

## Specialized Subagent
- `validator`: Handles validation execution, linter runs, test plan verification, and build code reviews.

## Acceptance Criteria (as-built)
1. Exposes `/kanche:qa-validate`, `/kanche:qa-test-plan`, and `/kanche:qa-review` slash commands.
2. Registers subagent `validator` in `plugins/qa/plugin.json`.
3. Integrates with `/kanche:sdd-run` orchestrator for P4 (Build Review) and P5 (Validation) phases.
