---
name: git-branch-delete
description: Delete a git branch locally and/or on origin remote, refusing protected branches, gated by explicit confirmation.
model: flash
---

# /kanche:git-branch-delete

**Summary.** Delete a git branch locally and/or on the remote (`origin`), refusing to delete protected branches, gated by explicit confirmation. The workflow delegates local and remote branch deletions to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<branch-name>` (positional, required) — the name of the branch to delete.
- `--remote` — also delete the branch on the remote (`origin`).
- `--force` — force-delete local branch (`git branch -D`) even if it has unmerged changes.

If `<branch-name>` is missing, ask the user (do not invent one).

## Steps

1. **Confirm this is a git repo.** If `git status` errors, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Refuse protected branches.** Never delete protected branches (`main`/`master`/`develop`), locally or remotely.

   ```bash
   TARGET="<branch-name>"
   case "$TARGET" in
     main|master|develop) echo "PROTECTED: $TARGET — deletion of protected branches is not allowed"; exit 1 ;;
   esac
   ```

3. **Check current branch.** You cannot delete the branch you are currently on.

   ```bash
   CURRENT=$(git rev-parse --abbrev-ref HEAD)
   if [ "$CURRENT" = "$TARGET" ]; then
     echo "REJECTED: Cannot delete current branch '$CURRENT'. Switch to another branch first (/kanche:git-switch)."
     exit 1
   fi
   ```

4. **Verify branch existence.** Verify that the branch exists locally and/or remotely before deleting.

   ```bash
   git rev-parse --verify --quiet "refs/heads/$TARGET" && echo "local exists" || echo "no local"
   git rev-parse --verify --quiet "refs/remotes/origin/$TARGET" && echo "remote exists" || echo "no remote"
   ```

5. **Gate — Mandatory Human Confirmation.** Never delete branches autonomously. STOP and ask the user to confirm deleting branch `<target>` locally (and if `--remote` is passed, on origin remote). Warn them if it is unmerged and `--force` is required. Use the interactive `default_api:ask_question` tool with options `(Recommended) Yes, proceed with deletion` and `No, abort`. Proceed only on selecting Yes; on No, STOP without deleting.

6. **Delete locally.** 
   - By default, use safe deletion:
     ```bash
     git branch -d "$TARGET"
     ```
   - If `--force` was passed, or safe delete fails and the user authorizes force-deletion, use:
     ```bash
     git branch -D "$TARGET"
     ```

7. **Delete remotely** (only if `--remote` was requested and confirmed). Never delete a protected branch.

   ```bash
   git push origin --delete "$TARGET"
   ```

8. **Report** deletion status (local deleted y/n, remote deleted y/n).

## git hard rules

Never delete remote protected branches. All branch deletions must be explicitly confirmed by the human prior to execution. Follow `plugins/kanche/rules/destructive-safety.md`.

## Done when

- The specified branch is deleted locally.
- If `--remote` was passed, the branch is deleted on origin.
- The action was explicitly confirmed by the human before deletion ran.

