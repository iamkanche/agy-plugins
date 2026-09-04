---
name: git-rebase
description: Rebase the current branch onto a target branch, gated by explicit human confirmation. Handles conflicts without force-resolving.
model: flash
---

# /kanche:git-rebase

**Summary.** Rebase the current branch onto a target branch, gated by explicit human confirmation; handles conflicts without force-resolving. The workflow delegates all local fetch, review, and rebase operations to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

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

6. **Gate — Mandatory Human Confirmation.** Never rebase without explicit confirmation. STOP and ask the user to confirm: present the target branch and commit replay list (`git log --oneline <target>..HEAD`) using the interactive `default_api:ask_question` tool with options `(Recommended) Yes, proceed with rebase` and `No, abort`. Proceed only on selecting Yes; on No, STOP.

   ```bash
   git rebase "$TARGET"
   ```

7. **Handle conflicts explicitly.** If the rebase reports conflicts, STOP and report conflicting files. Do not force-resolve, do not `reset --hard`. Tell the user to resolve then `git rebase --continue` or `git rebase --abort`.

8. **Report** the resulting state.

## git hard rules

Never force-push · never `--no-verify` · never amend a pushed commit · never `reset --hard` · never force-resolve conflicts.

## Done when

- The current branch is rebased onto `<base-branch>`.
- The user explicitly confirmed the rebase operation via the gate.
- Conflicts are reported clearly without force-resolving.
