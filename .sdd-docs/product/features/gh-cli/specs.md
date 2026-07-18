---
feature: gh-cli
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-18
---

# GitHub CLI Plugin — Consolidated Specification

<!-- schema: specs | written by /sdd:sync-product (dev-only sections stripped) -->

## Context
Google Antigravity utilizes the `gh-cli` plugin to manage the lifecycle of pull requests, audit modifications, and post reviews.

## Capabilities
- `/gh-cli:pr-create` - Push branch and open a pull request, with auto-assignee support.
- `/gh-cli:pr-list` - Lists repository PRs and identifies current branch connection.
- `/gh-cli:pr-review` - Audits a PR and submits inline suggestion comments.
- `/gh-cli:pr-approve` - Submits approval reviews (refusing self-approvals).
- `/gh-cli:pr-respond` - Coordinates thread replies and local fixes commits.
- `/gh-cli:pr-merge` - Merge a PR, with deleting the branch enabled by default.

## Acceptance criteria (as-built)
1. `/gh-cli:pr-create` automatically appends `--assignee "@me"` by default to auto-assign the creator.
2. `/gh-cli:pr-merge` successfully merges the PR and deletes local and remote feature branches unless `--keep-branch` is requested.
