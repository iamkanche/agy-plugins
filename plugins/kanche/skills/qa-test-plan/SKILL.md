---
name: qa-test-plan
description: Generate comprehensive test plans, unit/integration test specifications, Playwright E2E visual matrices, and test stubs.
---

# /kanche:qa-test-plan

**Summary.** Generate comprehensive test plans, unit/integration test specifications, edge-case test matrices, Playwright E2E visual verification scenarios, and test file stubs for a feature, laying the test suite groundwork for closed-loop validation in Phase P5.

## Loop Engineering Protocol (Test Setup Role — P5 Validation Loop)

In the Loop Engineering Framework, `/kanche:qa-test-plan` defines the multi-tiered testing matrix that `/kanche:qa-validate` evaluates and `/kanche:code-implement` repairs during closed-loop validation:
- Establishes concrete test cases, visual matrices, and executable stubs.
- Provides test assertions that drive automated pass/fail evaluation in the P5 validation loop.

## Inputs
- Feature specs (`specs.md`) and design docs (`design.md`) in `docs/development/{slug}/`.
- Project test suite setup (PHPUnit, Playwright, Jest, PyTest, etc.) and `plugins/kanche/rules/loop-engineering.md`.

## Steps
1. **Analyze Requirements & Contracts.** Map out acceptance criteria and public interface contracts.
2. **Inspect Existing Test Patterns.** Scan project test directories to align naming conventions and directory structures (`tests/`, `__tests__/`, `e2e/`).
3. **Define Multi-Tiered Test Strategy.**
   - **Unit Test Scenarios**: Domain logic, boundary conditions, edge cases (Given/When/Then).
   - **Integration Test Scenarios**: API endpoints, DB operations, external services.
   - **Playwright E2E & Visual Scenarios**: Browser interaction flows, UI element assertions, console error checks, visual screenshot comparisons.
   - **Risk & Test Data Seeding**: Data fixtures, mocks, and risk mitigation matrix.
4. **Draft Test Plan & Generate Test Stubs.**
   - Create `docs/development/{slug}/test-plan.md` outlining the test matrix and assertion checklists.
   - Generate stub test files matching project framework patterns.
5. **Report.** Output test plan summary and generated stub list.

## Done when
- `docs/development/{slug}/test-plan.md` is generated with full multi-tiered coverage details.
- Runnable test stubs/skeletons are generated for the project's test framework.

