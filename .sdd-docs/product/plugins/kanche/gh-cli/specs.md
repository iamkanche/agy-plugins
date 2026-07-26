---
feature: gh-cli
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
---

# GitHub CLI Plugin — Consolidated Specification

<!-- schema: specs | written by /kanche:sdd-sync (dev-only sections stripped) -->

## Context
Google Antigravity utilizes the `gh-cli` plugin to manage the lifecycle of pull requests, audit modifications, and post reviews.

## Capabilities
- `/kanche:pr-create` - Push branch and open a pull request, with auto-assignee support.
- `/kanche:pr-list` - Lists repository PRs and identifies current branch connection.
- `/kanche:pr-review` - Audits a PR and submits inline suggestion comments.
- `/kanche:pr-approve` - Submits approval reviews (refusing self-approvals).
- `/kanche:pr-respond` - Coordinates thread replies and local fixes commits.
- `/kanche:pr-merge` - Merge a PR, with deleting the branch enabled by default.

## Acceptance criteria (as-built)
1. `/kanche:pr-create` automatically appends `--assignee "@me"` by default to auto-assign the creator.
2. `/kanche:pr-merge` successfully merges the PR and deletes local and remote feature branches unless `--keep-branch` is requested.
3. Gated GitHub commands (pr-create, pr-list, pr-approve, pr-merge, pr-respond, pr-review) use the interactive `default_api:ask_question` tool for confirmations.
