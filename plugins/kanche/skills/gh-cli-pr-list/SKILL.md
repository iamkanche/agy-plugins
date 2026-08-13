---
name: gh-cli-pr-list
description: List the repository's open pull requests and show the current branch's PR context. Read-only.
model: flash
---

# /kanche:gh-cli-pr-list

**Summary.** List the repository's pull requests and show the current branch's PR context. Read-only. The workflow delegates all GitHub query and listing operations to the specialized `@gh-operator` subagent (defined in `agents/gh-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `--state=<all|open|closed|merged>` — PR state filter. Defaults to `open`.
- `--limit=<number>` — maximum count to return. Defaults to `10`.

No positional argument is required.

## Steps

1. **Verify gh auth.** Check auth status before making requests.

   ```bash
   gh auth status
   ```

2. **Retrieve PR list.** Run `pr list` with parsed filters.

   ```bash
   gh pr list --state "<state>" --limit "<limit>"
   ```

3. **Check current branch PR context.** Check if a PR already exists for the checked out branch.

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   gh pr view "$BRANCH" --json number,title,state,url,mergeable 2>/dev/null
   ```

4. **Format and output results.** Present the list of pull requests, and highlight the current branch's PR context (PR number, status, mergeable state) if found.

## git hard rules

Read-only to workspace and history. No modifications are made.

## Done when

- The repository's open/selected PR list was formatted and output.
- The current branch's PR connection and details were checked and reported.
