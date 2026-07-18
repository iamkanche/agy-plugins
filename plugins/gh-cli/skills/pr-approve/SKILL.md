---
name: gh-cli-pr-approve
description: Approve the current branch's PR on GitHub using gh CLI, refusing self-approval and gated by confirmation.
---

# /gh-cli:pr-approve

**Summary.** Approve the current branch's PR (or a specified PR) on GitHub using the `gh` CLI, refusing self-approval and gated by confirmation. The workflow delegates all GitHub authentication, PR metadata checks, and review submissions to the specialized `@gh-operator` subagent (defined in `agents/gh-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to approve. If omitted, `gh` resolves the PR for the current branch.

## Steps

1. **Verify gh auth.** Check auth status before making requests.

   ```bash
   gh auth status
   ```

2. **Check current user coordinates.** Identify who is running the command.

   ```bash
   gh api user -q .login
   ```

3. **Fetch PR details and author.**

   ```bash
   PR="<pr-number or empty for current branch>"
   gh pr view $PR --json number,title,author
   ```

4. **Verify self-approval restriction.** If the current user's login matches the PR author's login, STOP and refuse approval.

5. **Gate — STOP.** Present the PR title, author, and number, then ask the user to confirm submitting approval. Proceed only on an explicit yes; on no, STOP without approving.

6. **Submit approval review.**

   ```bash
   gh pr review $PR --approve
   ```

7. **Report** approval status and review URL.

## git hard rules

Read-only to workspace and local git history. The workflow only posts reviews via `gh`. Self-approvals are strictly blocked.

## Done when

- The PR author was checked and self-approval checks passed.
- The user confirmed approval via the gate.
- The PR was approved using the `gh pr review --approve` command.
