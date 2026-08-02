# GitHub CLI Workflows Specification

## 1. Overview
Automates GitHub Pull Request lifecycle operations using the GitHub CLI (`gh`), delegating operations to the specialized `@gh-operator` subagent with safety gating.

## 2. Included Skills & Commands
- `/kanche:gh-cli-pr-create`: Opens a pull request on GitHub built from branch commits and diff.
- `/kanche:gh-cli-pr-review`: Reviews pull request diff against rules and posts inline suggestions using a standardized `# Summary`, ASCII severity table (`🔴 HIGH`, `🟡 MEDIUM`, `🟢 LOW`), and structured `suggestion` inline comments format.
- `/kanche:gh-cli-pr-approve`: Approves the current branch's PR on GitHub (prevents self-approval).
- `/kanche:gh-cli-pr-merge`: Merges a pull request on GitHub.
- `/kanche:gh-cli-pr-respond`: Triages review comments, applies fixes, commits, pushes, and replies.
- `/kanche:gh-cli-pr-list`: Lists open pull requests and shows current branch PR context.

## 3. Product Invariants
- Prohibition against self-approval.
- Human confirmation required for merges (`auto_merge: false`).
- Comment event by default on reviews unless explicitly requested otherwise.
