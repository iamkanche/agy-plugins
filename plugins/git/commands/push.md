# /git:push

**Summary.** Push the current feature branch to `origin`, gated behind explicit confirmation; sets upstream on first push. The workflow delegates remote push executions and tracking configuration to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `--set-upstream` — force `git push -u origin <branch>` even if an upstream already exists. If omitted, `-u` is added automatically when the branch has no upstream.

No positional argument is required.

## Steps

1. **Confirm this is a git repo.** If `git rev-parse --is-inside-work-tree` fails, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Resolve the current branch and refuse protected branches.**

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   case "$BRANCH" in
     main|master|develop) echo "PROTECTED: $BRANCH — pushing protected branches is not allowed here"; exit 1 ;;
   esac
   echo "$BRANCH"
   ```

   If protected, STOP.

3. **Check state.** Show what will be pushed and whether an upstream exists.

   ```bash
   git status --short --branch
   ```

   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "NO_UPSTREAM"
   ```

4. **Decide the push command.** If `--set-upstream` was passed OR the branch reported `NO_UPSTREAM`, use `git push -u origin "$BRANCH"`. Otherwise use `git push`.

5. **Gate — STOP.** Ask the user to confirm pushing `<branch>` to origin. Show the exact command (with or without `-u`) and the ahead/behind summary from step 3. Proceed only on an explicit yes; on no, STOP without pushing.

6. **Push.** Never `--force`, never `--force-with-lease`, never `--no-verify`.

   ```bash
   git push -u origin "$BRANCH"   # or: git push
   ```

7. **Report** the result to the user (branch, remote, upstream set y/n).

## git hard rules

Never force-push · never `--no-verify` · never amend a pushed commit · never `reset --hard` · never push a protected branch.

## Done when

- The current feature branch is pushed to `origin`, with upstream tracking configured on first push.
- The user explicitly confirmed the push via the gate.
- No force flag or `--no-verify` was used, and no protected branch was pushed.
