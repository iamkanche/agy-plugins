---
name: git-switch
description: Switch the working tree to a different branch, fetching first to resolve remote tracking branches.
---

# /kanche:git-switch

**Summary.** Switch the current working tree to a different branch, fetching first to resolve remote branches and tracking. Lightweight checkouts run directly or via `@git-operator` (`agents/git-operator.md`).

## Inputs

Parse the invocation arguments:

- `<branch-name>` (positional, required) — the branch to switch to.
- `-c` / `--create` — create and switch to a new branch (delegates to `/kanche:git-branch-create`).

If `<branch-name>` is missing, ask the user (do not guess).

## Steps

1. **Confirm this is a git repo.** If `git status` errors, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Handle create flag.** If `-c` or `--create` is passed, stop and delegate directly to `/kanche:git-branch-create <branch-name>`.

3. **Fetch remote data.** Fetch latest remote branches before switching so that remote branches can be tracked correctly.

   ```bash
   git fetch origin
   ```

4. **Verify branch existence locally and remotely.**

   ```bash
   TARGET="<branch-name>"
   git rev-parse --verify --quiet "refs/heads/$TARGET" && echo "local exists" || echo "no local"
   git rev-parse --verify --quiet "refs/remotes/origin/$TARGET" && echo "remote exists" || echo "no remote"
   ```

5. **Switch branch.**
   - If the branch exists locally:
     ```bash
     git switch "$TARGET"
     ```
   - If the branch exists only remotely (remote exists, local does not): Switch and track remote branch:
     ```bash
     git switch --track "origin/$TARGET"
     ```
   - If the branch does not exist anywhere: STOP and suggest creating it via `/kanche:git-branch-create "$TARGET"`.

6. **Report** the resulting checked-out branch and status.

   ```bash
   git branch -vv
   ```

## git hard rules

Never `reset --hard` when switching branches. Always fetch first to check for remote branches.

## Done when

- The working tree is switched to `<branch-name>`.
- Remote tracking was configured if the branch existed only on origin.
- The new branch state is reported to the user.
