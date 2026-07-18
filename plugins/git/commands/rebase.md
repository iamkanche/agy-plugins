# /git:rebase

**Summary.** Rebase the current branch onto a target branch, gated by confirmation; handles conflicts without force-resolving. The workflow delegates all local fetch, review, and rebase operations to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<base-branch>` (positional, required) — the branch/commit to rebase onto (e.g. `main` or `origin/main`).

If the target branch is missing, ask the user (do not guess).

## Steps

1. **Confirm this is a git repo.** If `git status` errors, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Check the working tree is clean.** If there are uncommitted changes, STOP and tell the user to commit or stash first (`/git:stash`).

   ```bash
   git status --short
   ```

3. **Fetch remote data.** Fetch latest changes from the remote to ensure local tracking of remote targets is up to date.

   ```bash
   git fetch origin
   ```

4. **Verify the target branch exists.**

   ```bash
   TARGET="<base-branch>"
   git rev-parse --verify --quiet "$TARGET" || git rev-parse --verify --quiet "origin/$TARGET"
   ```

   If the target branch cannot be resolved, STOP and tell the user.

5. **Refuse protected branches.** Refuse to rebase if the current branch is a protected branch (`main`/`master`/`develop`).

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   case "$BRANCH" in
     main|master|develop) echo "PROTECTED: $BRANCH — rebasing protected branches is not allowed here"; exit 1 ;;
   esac
   ```

6. **Gate — STOP.** Ask the user to confirm rebasing `<branch>` onto `<target>` (this rewrites local history). Show the target and the commits that will be replayed (`git log --oneline <target>..HEAD`). Proceed only on an explicit yes; on no, STOP.

   ```bash
   git rebase "$TARGET"
   ```

7. **Handle conflicts explicitly.** If the rebase reports conflicts, STOP and report the conflicting files. Do not force-resolve, do not `reset --hard`, do not `push --force`. Tell the user to resolve then `git rebase --continue` or `git rebase --abort`.

8. **Report** the resulting state.

   ```bash
   git status --short --branch
   ```

## git hard rules

Never force-push · never `--no-verify` · never amend a pushed commit · never `reset --hard` · never force-resolve conflicts.

## Done when

- The current branch is rebased onto `<base-branch>`, confirmed via the rebase gate.
- Any conflicts are reported clearly and left for the user to resolve (no force-resolve, no hard reset).
- No history was rewritten without explicit confirmation.
