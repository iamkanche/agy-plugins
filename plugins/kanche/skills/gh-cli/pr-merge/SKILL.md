---
name: gh-cli-pr-merge
description: Merge a pull request on GitHub, with deleting the branch enabled by default, gated by confirmation.
---

# /kanche:gh-cli-pr-merge

**Summary.** Merge the current branch's PR (or a specified PR) on GitHub, deleting the remote and local branch by default unless `--keep-branch` is requested. The workflow delegates all GitHub authentication, PR metadata checks, and merge executions to the specialized `@gh-operator` subagent (defined in `agents/gh-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to merge. If omitted, `gh` resolves the PR for the current branch.
- `--squash` — use the squash merge method.
- `--rebase` — use the rebase merge method.
- `--merge` — use the merge commit method (default).
- `--keep-branch` — do not delete the local and remote branch after the merge.

## Steps

1. **Verify gh auth.** Check auth status before making requests.

   ```bash
   gh auth status
   ```

2. **Retrieve PR details.** Resolve the target PR and its associated branch coordinates.

   ```bash
   PR="<pr-number or empty for current branch>"
   gh pr view $PR --json number,title,headRefName,baseRefName,mergeable
   ```

3. **Check checked-out status.** Determine if the PR's head branch matches the current checked-out branch.

   ```bash
   CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
   HEAD_BRANCH="<headRefName returned by gh>"
   BASE_BRANCH="<baseRefName returned by gh>"
   ```

4. **Gate — mode-conditional.** If this skill is invoked from SDD auto mode (`mode=auto` in `settings.json`) AND `auto_merge` is `true` in `settings.json`, log the action (PR title, number, base branch, merge method, and branch-deletion flag) and proceed automatically without prompting. If `auto_merge` is `false` (or unset), or if invoked standalone/from SDD manual mode, STOP and ask the user to confirm: present the PR title, number, base branch, merge method, and whether branch deletion is enabled using the interactive `default_api:ask_question` tool with options `(Recommended) Yes, merge PR` and `No, abort`. Proceed only on selecting Yes; on No, STOP without merging.

5. **Execute merge.** Run the merge command.

   ```bash
   METHOD="--merge" # or --squash or --rebase
   DELETE_FLAG="--delete-branch"
   if [ "<--keep-branch passed>" = "true" ]; then
     DELETE_FLAG=""
   fi
   gh pr merge $PR $METHOD $DELETE_FLAG
   ```

6. **Post-merge branch cleanup (local).** If the branch was merged and `--keep-branch` was NOT specified, and the merged branch was the current branch:
   - Switch to the base branch.
   - Delete the local merged branch.

   ```bash
   if [ "$CURRENT_BRANCH" = "$HEAD_BRANCH" ] && [ -z "$DELETE_FLAG" ]; then
     git checkout "$BASE_BRANCH"
     git branch -d "$HEAD_BRANCH"
   fi
   ```

7. **Report** merge success.

## git hard rules

Never bypass branch protections · never force-merge without confirmation.

## Done when

- The pull request was merged successfully using the requested method.
- The local and remote feature branches were deleted (unless `--keep-branch` was specified).
- The action was confirmed (manual mode) or logged (auto mode) before the merge ran.
