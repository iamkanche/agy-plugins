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
