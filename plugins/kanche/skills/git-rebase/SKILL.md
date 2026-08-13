---
name: git-rebase
description: Rebase the current branch onto a target branch, gated by confirmation (auto-mode compatible). Handles conflicts without force-resolving.
model: flash
---

# /kanche:git-rebase

**Summary.** Rebase the current branch onto a target branch, supporting both interactive manual mode and automated SDD mode; handles conflicts without force-resolving. The workflow delegates all local fetch, review, and rebase operations to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<base-branch>` (positional, required) — the branch/commit to rebase onto (e.g. `main` or `origin/main`).

If the target branch is missing, ask the user (do not guess).

## Steps

1. **Confirm this is a git repo.**

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Check the working tree is clean.** If there are uncommitted changes, STOP and tell the user to commit or stash first (`/kanche:git-stash`).

   ```bash
   git status --short
   ```

3. **Fetch remote data.**

   ```bash
   git fetch origin
   ```

4. **Verify the target branch exists.**

   ```bash
   TARGET="<base-branch>"
   git rev-parse --verify --quiet "$TARGET" || git rev-parse --verify --quiet "origin/$TARGET"
   ```

5. **Refuse protected branches.** Refuse to rebase if the current branch is a protected branch (`main`/`master`/`develop`).

6. **Gate — mode-conditional.** If invoked from SDD auto mode, log the action (target branch and commit replay list `git log --oneline <target>..HEAD`) and proceed automatically. If invoked standalone or from SDD manual mode, ask user confirmation via `default_api:ask_question`.

   ```bash
   git rebase "$TARGET"
   ```

7. **Handle conflicts explicitly.** If the rebase reports conflicts, STOP and report conflicting files. Do not force-resolve, do not `reset --hard`. Tell the user to resolve then `git rebase --continue` or `git rebase --abort`.

8. **Report** the resulting state.

## git hard rules

Never force-push · never `--no-verify` · never amend a pushed commit · never `reset --hard` · never force-resolve conflicts.

## Done when

- The current branch is rebased onto `<base-branch>`.
- Mode-conditional gating executed appropriately (logged in auto mode, confirmed in manual mode).
- Conflicts are reported clearly without force-resolving.
