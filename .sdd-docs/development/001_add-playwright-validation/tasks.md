# Tasks: Playwright Browser Validation for SDD

## Phase 1: Infrastructure and Config Setup
- [ ] Create `package.json` at root to define `@playwright/test` devDependency and register `test:e2e` script. Traces: Component 1, AC 1. [P]
- [ ] Create `playwright.config.js` at root. Set test folder to `tests/`, timeout to 30s, workers to 1, reporter to `list`, and use headless Chromium. Traces: Component 2, AC 1. [P]
- [ ] Modify `.sdd-docs/settings.json` to add the `validation.browser` settings object (`enabled: true`, `port: "auto"`, `framework: "playwright"`). Traces: Component 4, Data model. [P]

## Phase 2: Skill and Tech Guidelines Updates
- [ ] Modify `.sdd-docs/guidelines/tech.md` to add `npm run test:e2e` under test commands section. Traces: Component 5, AC 1, AC 5.
- [ ] Modify `plugins/sdd/skills/validate/SKILL.md` to instruct the validator to check for Node/Playwright dependencies and handle skipped states, outputting a `SKIPPED (missing dependencies)` state. Traces: Component 6, AC 8.

## Phase 3: E2E Test Suite Development
- [ ] Create `tests/dashboard.spec.js` and implement the inline HTTP static server setup in `beforeAll` and cleanup in `afterAll` listening on dynamic port `0`. Traces: Component 3, AC 2.
- [ ] Add test case to `tests/dashboard.spec.js` for loading `/index.html`, asserting 200 HTTP status, no console errors, and presence of 3 active plugin buttons. Traces: Component 3, AC 3.1, AC 3.2.
- [ ] Add test case to `tests/dashboard.spec.js` for loading `/plugins/sdd/index.html`, asserting 200 HTTP status, no console errors, checking that `#connection-map-svg` exists with >= 15 command nodes, clicking `[data-node-id="/sdd:run"]` node, and verifying `#details-header-section .details-title` contains `/sdd:run`. Traces: Component 3, AC 3.1, AC 3.2, AC 3.3, AC 3.4.
- [ ] Add test case to `tests/dashboard.spec.js` to assert document `scrollWidth <= clientWidth` to detect layout clipping or container blowout. Traces: Component 3, AC 4.
- [ ] Ensure `tests/dashboard.spec.js` asserts no screenshot files are saved/written. Traces: Component 3, AC 6.

## Phase 4: Run Verification & Linting
- [ ] Run `npm install` to fetch Playwright dependencies. Traces: AC 1.
- [ ] Run `npm run test:e2e` to verify all tests pass locally. Traces: AC 5, AC 6.
- [ ] Perform a code quality check and format validation on new JS files (`playwright.config.js`, `tests/dashboard.spec.js`). Traces: Lint task.
- [ ] Dry-run check the validate skill `/sdd:validate` (or mock missing deps) to verify that if Playwright is missing, validation skips gracefully with `SKIPPED (missing dependencies)`. Traces: AC 8.

## Verification
The following verification commands and checks will be used to prove the implementation is complete:

1. **E2E Test Execution**:
   ```bash
   npm run test:e2e
   ```
   - Covers **AC 2** (server lifecycle on dynamic port), **AC 3** (loading, console errors, SVG node check, click interaction), and **AC 4** (layout clipping check).
2. **Validation Skill Execution**:
   - Run the validation runner:
     ```bash
     # Sourced from validate skill / tech.md
     /sdd:validate
     ```
   - Verify that the report contains the `browser/e2e` row and marks the results correctly (**AC 1**, **AC 5**).
3. **Graceful Skipped State Check**:
   - Temporarily uninstall Playwright/move node_modules and run `/sdd:validate`.
   - Verify the suite reports `SKIPPED (missing dependencies)` instead of failing (**AC 8**).
4. **Failure Logging & No Screenshots**:
   - Induce a deliberate test assertion failure (e.g. modify detail header assertion).
   - Run `npm run test:e2e` and verify failure log output shows the detail.
   - Verify that no screenshots are generated/written to the disk (**AC 6**).
