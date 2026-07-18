# Antigravity GitHub CLI Plugin

A namespaced plugin bundle for Google Antigravity that packages robust integrations with GitHub using the `gh` CLI and REST API.

This plugin enables agents to manage the pull request lifecycle, audit code modifications against repository guidelines, submit reviews and approvals, and triage review threads safely.

## Available Slash Commands

Workflows are located in [.agent/workflows/](file:///.agent/workflows/) and map to the following commands:

- `/gh-cli:pr-create` - Safe branch push and pull request creation.
- `/gh-cli:pr-list` - Lists repository PRs and identifies current branch connection.
- `/gh-cli:pr-review` - Audits a PR against `AGENTS.md` rules and submits formatted inline suggestion comments.
- `/gh-cli:pr-approve` - Submits approval reviews (refusing self-approvals).
- `/gh-cli:pr-respond` - Coordinates comments/threads triaging, local fixes verification, commits, pushes, and thread replies.
