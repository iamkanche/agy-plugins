---
name: pr-create
description: Open a pull request for the current branch on GitHub, building title and body from commits and diff, gated by confirmation.
---

# /gh-cli:pr-create

**Summary.** Open a pull request for the current branch against the default (or given) base, building title + body from the branch's commits and diff, gated behind explicit confirmation. The workflow delegates all GitHub PR creation and interactions to the specialized `@gh-operator` subagent (defined in `agents/gh-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `--draft` — create the PR as a draft (`gh pr create --draft`).
- `--base=<branch>` — target base branch. If omitted, `gh` uses the repository default base.
- `--assignee=<user>` — assign the PR to a user. Defaults to `@me` (auto-assigns the PR creator).

No positional argument is required.

## Steps

1. **Require gh and auth.** If `gh` is not authenticated, STOP and tell the user to run `gh auth login` (do not attempt to authenticate for them).

   ```bash
   gh auth status
   ```

2. **Resolve the branch and refuse protected branches.** A PR must originate from a feature branch.

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   case "$BRANCH" in
     main|master|develop) echo "PROTECTED: $BRANCH — create a feature branch first"; exit 1 ;;
   esac
   ```

   (Uses `git rev-parse`; if that helper is unavailable, read the branch from `git branch`.) If protected, STOP.

3. **Ensure the branch is pushed.** If it has no upstream, push it with `-u` first (never `--force`, never `--no-verify`).

   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || git push -u origin "$BRANCH"
   ```

4. **Gather material for the PR.** Determine the merge base against the target base and summarize the commits + diff.

   ```bash
   BASE="<--base value, or the repo default>"
   git log --oneline "origin/$BASE..HEAD"
   git diff --stat "origin/$BASE...HEAD"
   ```

5. **Compose the PR title + body** (technical identifiers verbatim). Title = concise summary; body = what/why, key changes, and any testing notes.

6. **Gate — STOP.** Ask the user to confirm opening this pull request. Show the title, the full body, the base branch, and whether it is a draft using the interactive `default_api:ask_question` tool with options `(Recommended) Yes, create PR` and `No, abort`. Proceed only on selecting Yes; on No, STOP without creating the PR.

7. **Create the PR.** Pass the title and body; add `--draft` and `--base` as parsed. Include `--assignee` (defaults to `@me` if not specified).

   ```bash
   gh pr create --title "<title>" --body "<body>" --assignee "<user>" [--draft] [--base "<branch>"]
   ```

8. **Report** the PR URL returned by `gh`.

## git hard rules

Never force-push · never `--no-verify` · never amend a pushed commit · never `reset --hard` · never open a PR from a protected branch.

## Done when

- A pull request is open for the current feature branch against the intended base.
- The branch was pushed to origin beforehand (with upstream tracking).
- The user explicitly confirmed the title + body via the gate before creation.
- The PR URL is reported back to the user.
