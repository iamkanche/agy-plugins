# GitHub CLI Plugin — Decisions (ADR log)

<!-- schema: decisions | written by /sdd:sync-product -->

## ADR-001: Branch Deletion by Default on PR Merge
- **Context:** Leftover branch names pollute local and remote repositories after pull request completion.
- **Decision:** Enable `--delete-branch` flag as the default behavior for `/gh-cli:pr-merge` command execution, providing `--keep-branch` to override it.
- **Consequences:** Cleaner branch listing locally and remotely without manual intervention.

## ADR-002: Auto-Assignee by Default
- **Context:** PRs are typically assigned to the creator of the PR upon initialization.
- **Decision:** Automatically include the `--assignee "@me"` flag during `/gh-cli:pr-create` execution by default.
- **Consequences:** Simplifies flow for contributors, ensuring proper assignee mapping immediately.

## ADR-003: Interactive Gating via AskQuestion
- **Context:** Command confirmations via text prompt (yes/no) interrupt execution flow and require manual typing in the terminal.
- **Decision:** Mandate using the `default_api:ask_question` tool for all human gates across all gh-cli side-effect commands.
- **Consequences:** Modal-driven, structured confirmations that prevent CLI disruption and reduce keystroke errors.
