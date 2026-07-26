# GitHub CLI Workflows Design

## 1. Subagent Delegation
GitHub actions delegate execution to `@gh-operator` (`plugins/kanche/agents/gh-operator/agent.json`), ensuring:
- Safe GitHub CLI execution via `gh pr create`, `gh pr review`, `gh pr merge`.
- Structural Conventional Commit title/body parsing.

## 2. Interactive Gating
In manual mode, operations ask confirmation via `default_api:ask_question`. In SDD auto mode, PR creation/reviews proceed with auto-logging, while PR merges remain human-gated when `auto_merge: false`.
