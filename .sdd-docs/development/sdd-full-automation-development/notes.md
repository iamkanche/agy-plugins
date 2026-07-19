# Notes - SDD Full Automation Development

## Clarifying Questions and Assumptions

### 1. Mode of Execution & Human Interaction
- **Question**: Under `--mode=auto`, how should we handle tools that usually require human confirmation (e.g., `git:commit`, `git:push`, `gh-cli:pr-create`)?
- **Why it matters**: The user specifies "no human interaction - auto mode(accept edits, commands(safe commands), etc)".
- **Category**: Scope boundary / Workflow gating.
- **Assumption if unanswered**: In `--mode=auto`, standard prompt questions are bypassed or auto-approved. Safe commands are executed automatically. If a tool blocks, we rely on the caller's auto-approve behavior if configured, or automatically proceed with standard execution flags.

### 2. Settings JSON Configuration
- **Question**: What settings can be configured in `.sdd-docs/settings.json`?
- **Why it matters**: We need a standard schema/properties that the workflow can read.
- **Category**: Data & state.
- **Assumption if unanswered**: `.sdd-docs/settings.json` can specify:
  - `mode`: "auto" or "manual"
  - `max_loops`: 3 (default for inner loops)
  - `auto_approve_commands`: boolean
  - `pr_polling_interval_seconds`: integer (for PR comment check)
  - `pr_polling_max_attempts`: integer (default 3)

### 3. PR Feedback Polling
- **Question**: How do we check PR status/comments without webhooks?
- **Why it matters**: We need to poll GitHub to see if there is new review feedback on the created PR.
- **Category**: Integration/dependency.
- **Assumption if unanswered**: We will poll the GitHub CLI command:
  ```bash
  gh pr view --json reviews,comments,status
  ```
  We will do this up to `pr_polling_max_attempts` times, waiting between checks (using the `schedule` or a sleep/polling helper) to inspect reviews and comments. If comments are found, we'll invoke `/gh-cli:pr-respond` (or equivalent parsing logic) to resolve them.

### 4. Merging and Product Sync
- **Question**: When/how should the PR be merged?
- **Why it matters**: The workflow should automatically merge the PR once it passes review.
- **Category**: Acceptance/definition-of-done.
- **Assumption if unanswered**: Once the PR review returns green (approved) and validation passes, we will execute `/gh-cli:pr-merge` (or `gh pr merge --auto --merge`) to merge the branch into the default branch.

### 5. Memory Preservation
- **Question**: What files should be preserved across runs?
- **Why it matters**: The user requested to preserve `memory.md` and `settings.json`.
- **Category**: Data & state.
- **Assumption if unanswered**: `.sdd-docs/product/memory.md` and `.sdd-docs/settings.json` must be copied to a safe local temporary path or left untouched during cleanup of the feature branch, and synced/preserved back to the product/ root directory after merge.

## Readiness
The feature request is specs-ready. We proceed to writing `specs.md`.
