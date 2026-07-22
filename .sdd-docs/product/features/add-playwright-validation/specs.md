# Specs: Playwright Browser Validation for SDD

## Context
Google Antigravity utilizes the `sdd` plugin to drive feature implementation through the Software Development Document (SDD) model: specifications, design, tasks, build, validation, deploy, and product alignment. The central dashboard (`index.html`) serves as the central visual interface to preview plugins, rules, and commands. Introducing automated browser validation (via Playwright or Chrome DevTools MCP) ensures the UI renders correctly and handles user actions as expected during the P5 validation phase, preventing broken visual layouts, clipping, or console errors from being committed.

**Driving Item ID**: `feat/playwright-validation`

## Scope
### In-Scope
- Updating the `/sdd:validate` skill definition and execution to include a browser-based validation suite.
- Creating a basic Node.js dependency configuration (`package.json`) at the root repository to manage Playwright.
- Adding a Playwright test script/suite to run functional browser checks against the root dashboard (`index.html`).
- Configuring a local static file server that runs dynamically to serve the repository files for the browser tests.
- Capturing page console errors, layout overflow/clipping warnings, and connection map element renders.
- Updating the `sdd-validator` agent configuration (`agent.json`) if needed to support MCP tools or Node.js execution.
- Standardizing the output report from Playwright so that any failures are readable by the `sdd-coder` to allow auto-fixing.

### Out of Scope / Non-goals
- Visual regression testing / pixel-by-pixel image comparisons (visual diffs).
- Saving browser screenshots to disk or as persistent artifacts (the verification happens in-memory/run-time).
- Testing external integrations (outside the local registry dashboard).
- Adding browser validations to plugins other than `sdd` (e.g., `git` and `gh-cli` plugins do not have dashboards requiring browser validation).

## User stories
- **As a** developer running the SDD workflow,
  **I want** the validate skill to automatically spin up a browser and check the registry dashboard's layout and functionality,
  **so that** I don't merge broken UI changes or visual clipping issues.
- **As a** parent agent running `/sdd:run` in auto mode,
  **I want** any Playwright browser validation failures to be formatted clearly in the validation report,
  **so that** I can pass the logs back to `sdd-coder` to automatically fix the implementation.

## Acceptance criteria
1. **Given** a workspace with dashboard files (`index.html`), **When** `/sdd:validate` is invoked, **Then** a browser validation suite is run as part of the validation checklist.
2. **Given** the browser validation suite is executed, **When** it starts, **Then** it spins up a temporary HTTP server on a local free port, serves the workspace root, and shuts down the server upon completion.
3. **Given** the browser validation runner, **When** it navigates to the dashboard, **Then** it asserts that:
   - The page status is 200.
   - There are no JavaScript uncaught exceptions or console errors thrown during load or execution.
   - The Interactive Skill Connections Map SVG element contains a valid SVG node hierarchy with at least 15 commands rendered.
   - Selecting a command card successfully highlights the card and displays corresponding details in the sidebar panel.
4. **Given** a layout change that causes visual clipping or container blowout, **When** the browser validation suite runs, **Then** it detects the clipping (by comparing element bounding boxes against viewport bounds or checking overflow properties) and fails the test.
5. **Given** the browser validation runs, **When** it completes, **Then** the validation report contains a dedicated `browser/e2e` suite row with the count of tests run, passed, and failed.
6. **Given** a browser validation failure, **When** it is reported, **Then** the report includes the specific test failure messages and console logs, and does NOT write or save screenshot files to the disk.
7. **Given** the SDD run is in `auto` mode and browser validation fails, **When** the workflow enters the fix loop, **Then** the failure details are fed to `sdd-coder` to modify files (e.g., HTML/CSS) and re-verify, up to 3 times.
8. **Given** the local execution environment lacks Node.js, Playwright, or browser binaries, **When** `/sdd:validate` runs, **Then** it marks the browser validation suite as `SKIPPED (missing dependencies)` with environment notes, and does not fail the entire validation phase.

## Data model
- **Changed configuration schema**:
  - `.sdd-docs/settings.json`: Added `validation` block specifying browser testing config:
    ```json
    {
      "validation": {
        "browser": {
          "enabled": true,
          "port": "auto",
          "framework": "playwright"
        }
      }
    }
    ```
- **New workspace files**:
  - `package.json`: defines `@playwright/test` and script to run validation.
  - `playwright.config.js`: defines browser config, timeout, base URL, and reporter.
  - `tests/dashboard.spec.js`: Playwright test file containing assertions.

## NFR (non-functional requirements)
- **Performance**: The browser validation suite must complete execution within 30 seconds under normal resource constraints.
- **Portability**: Playwright tests must be compatible with headless execution in containerized/headless environments (e.g., CI runners or local dev boxes).
- **Observability**: Playwright output must write to standard output to be captured by the `sdd-validator` and passed in context.

## Open questions
1. **Should we use Chrome DevTools MCP tools or Playwright CLI?**
   - *Assumption*: We will implement Playwright CLI (`npx playwright test`) as the default since it fits the standard automated test-suite pattern (non-interactive, headless, multi-browser), but document how to configure and use Chrome DevTools MCP tools if the environment does not allow Node.js.
2. **Do we need to test across multiple browsers (Chromium, Firefox, WebKit)?**
   - *Assumption*: We will test Chromium by default to save execution time and memory in resource-constrained agent environments, with options to enable other browsers via `playwright.config.js`.
