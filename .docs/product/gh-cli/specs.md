# GitHub CLI Workflows Specification

## 1. Overview
Automates GitHub Pull Request lifecycle operations using the GitHub CLI (`gh`), delegating operations to the specialized `@gh-operator` subagent with safety gating.

## 2. Included Skills & Commands
- `/kanche:gh-cli-pr-create`: Opens a pull request on GitHub built from branch commits and diff, gated by mandatory human confirmation.
- `/kanche:gh-cli-pr-review`: Reviews pull request diff against rules, supports `--json` / `--format=json` export to `review.json`, and posts reviews with `#  Summary`, `## Review Summary`, standard Markdown severity tables (`|---|`), and inline line comments via atomic single-request `gh api` submission.
- `/kanche:gh-cli-pr-approve`: Approves the current branch's PR on GitHub (strictly prohibits self-approval).
- `/kanche:gh-cli-pr-merge`: Merges a pull request on GitHub, gated by mandatory human confirmation.
- `/kanche:gh-cli-pr-respond`: Triages review comments, applies targeted fixes via `/kanche:code-implement`, commits via `/kanche:git-commit`, pushes via `/kanche:git-push`, resolves threads via GraphQL, and replies.
- `/kanche:gh-cli-pr-list`: Lists open pull requests and shows current branch PR context (read-only).

## 3. Product Invariants
- Prohibition against self-approval.
- Zero autonomous destructive actions: PR merges (`gh pr merge`) and PR creation pushes (`git push`) strictly require interactive human approval via `default_api:ask_question`.
- Single-request atomic PR review submissions via `gh api --method POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews --input review.json`.
- Comment event by default on reviews (`COMMENT`) unless explicitly requested otherwise.
- Skills stand alone with zero caller execution mode dependencies.
