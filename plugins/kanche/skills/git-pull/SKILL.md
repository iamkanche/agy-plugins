---
name: git-pull
description: Integrate changes from the remote branch into the current branch, supporting fast-forward or gated rebase.
model: flash
---

# /kanche:git-pull

**Summary.** Integrate changes from the remote branch into the current branch (supporting merge or gated rebase), reporting conflicts without force-resolving. The workflow delegates all local merges, fetches, and rebasing tasks to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `--rebase` — rebase the current branch onto its upstream instead of a merge pull. History-rewriting → requires a gate.
- `--onto=<branch>` — rebase target branch (implies `--rebase`); e.g. `--onto=develop`. If omitted with `--rebase`, rebase onto the branch's upstream.

No positional argument is required.

## Steps

1. **Confirm this is a git repo.** If `git status` errors, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Check the working tree is clean.** If there are uncommitted changes, STOP and tell the user to commit or stash first (`/kanche:git-stash`) — do not pull/rebase over a dirty tree.

   ```bash
   git status --short
   ```

3. **Fetch remote data.** Fetch changes from the remote to ensure local tracking branches are up to date.

   ```bash
   git fetch origin
   ```

4. **Merge path (default, no `--rebase`).** Fast-forward / merge pull from upstream. If the branch has no upstream, report that and STOP.

   ```bash
   git pull --ff-only 2>/dev/null || git pull
   ```

5. **Rebase path (`--rebase` / `--onto`).** This rewrites history → **Gate — STOP.** Ask the user to confirm rebasing `<branch>` onto `<upstream or --onto target>` (this rewrites local history). Show the target and the commits that will be replayed (`git log --oneline <target>..HEAD`). Proceed only on an explicit yes; on no, STOP.

   ```bash
   git rebase "<--onto target, or upstream>"
   ```

6. **Handle conflicts explicitly.** If the pull/rebase reports conflicts, STOP and report the conflicting files. Do not force-resolve, do not `reset --hard`, do not `push --force`. Tell the user to resolve then `git rebase --continue` / commit the merge, or `git rebase --abort`.

7. **Report** the resulting state (ahead/behind, whether rebased or merged).

   ```bash
   git status --short --branch
   ```

## git hard rules

Never force-push · never `--no-verify` · never amend a pushed commit · never `reset --hard` · never force-resolve conflicts.

## Done when

- The branch is updated from upstream (merged, or rebased after the rebase gate).
- Any conflicts are reported clearly and left for the user to resolve (no force-resolve, no hard reset).
- No history was rewritten without explicit confirmation, and nothing was force-pushed.
