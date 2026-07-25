---
name: test-plan
description: Generate comprehensive test plans, unit/integration test specifications, and acceptance test cases.
---

# /qa:test-plan

**Summary.** Generate comprehensive test plans, unit/integration test specifications, edge-case test matrices, and automated test suite guidelines for a feature.

## Inputs
- Feature specs (`specs.md`) and design docs (`design.md`) in `.sdd-docs/development/{slug}/`.
- Project test suite setup (e.g., PHPUnit, Playwright, Jest, PyTest).

## Steps
1. **Analyze Requirements & Contracts.** Read feature specs and design specifications to map out acceptance criteria and public interface contracts.
2. **Define Test Strategy.**
   - Unit Test Scenarios (isolated domain logic, edge cases, boundaries).
   - Integration Test Scenarios (API endpoints, database operations, external integrations).
   - End-to-End / Visual Verification Scenarios (UI workflows, user interactions).
3. **Draft Test Plan.** Create `.sdd-docs/development/{slug}/test-plan.md` outlining the test matrix, preconditions, test data requirements, and assertion checklists.
4. **Report.** Output the test plan summary with total test coverage goals.

## Done when
- `.sdd-docs/development/{slug}/test-plan.md` is generated with clear test scenarios and acceptance criteria verification.
