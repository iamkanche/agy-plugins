---
name: git-commit
description: Commit staged work with a Conventional Commits message gated behind explicit confirmation. Use when ready to record changes.
---

# /kanche:git-commit

**Summary.** Commit staged work with a Conventional Commits message whose body has Overview / Changes / Impact sections, gated behind explicit confirmation. The workflow delegates all local Git operations (staging, scanning, committing) to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `--all` — stage every tracked modification (`git add -A`) before committing, instead of committing only what is already staged.
- `--scope=<scope>` — force the Conventional Commits scope. If absent, infer the scope from the touched paths (top-level module/dir); if it cannot be inferred confidently, omit the scope.

No positional argument is required. Never invent a scope — omit it rather than guess.

## Steps

1. **Confirm this is a git repo.** If `git rev-parse --is-inside-work-tree` fails, STOP and tell the user this is not a git repository.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Refuse protected branches.** Detect the current branch; never commit on `main`/`master`/`develop`.

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   case "$BRANCH" in
     main|master|develop) echo "PROTECTED: $BRANCH — create a feature branch first (/kanche:git-branch-create)"; exit 1 ;;
   esac
   ```

   If protected, STOP and point the user to `/kanche:git-branch-create`.

3. **Inspect the change set.** Understand what is staged vs unstaged before composing anything.

   ```bash
   git status --short
   git diff --staged
   git diff        # unstaged, for context
   ```

4. **Stage.** With `--all`, stage all tracked modifications; otherwise commit only what is already staged. Never stage secrets.

   ```bash
   # only when --all was passed:
   git add -A
   ```

   Before staging or committing, scan the paths and diff for secrets (`.env`, `credentials`, `*.pem`, `*.key`, `id_rsa`, tokens). If any appear, STOP and ask the user to remove them from the change set — do not commit them.

5. **Verify something is staged.** If `git diff --staged --quiet` reports no staged changes, STOP: there is nothing to commit (tell the user to stage files or pass `--all`).

   ```bash
   git diff --staged --quiet && echo "NOTHING STAGED" || echo "staged changes present"
   ```

6. **Compose the message** (technical identifiers stay verbatim), following the structure in "Commit message structure" below. Subject line `<type>(<scope>): <subject>` ≤ 50 chars; wrap body prose at 72 cols.

7. **Gate — mode-conditional.** If invoked from SDD auto mode, log the action (staged changes, commit message, and target branch) and proceed automatically. If invoked standalone or from SDD manual mode, STOP and ask the user to confirm committing the staged changes with this message. Present the complete message and the target branch using the interactive `default_api:ask_question` tool with options `(Recommended) Yes, commit these changes` and `No, abort commit`. Proceed only on selecting Yes; on No, STOP without committing.

8. **Commit via HEREDOC** so the multi-line body and footer are preserved verbatim. Do not use `--no-verify`.

   ```bash
   git commit -F - <<'EOF'
   <type>(<scope>): <subject>

   ## Overview
   <summary>

   ## Changes
   - <change 1>
   - <change 2>

   ## Impact
   <impact>

   <footer>
   EOF
   ```

9. **Report** the resulting commit.

   ```bash
   git log -1 --oneline
   ```

## Commit message structure

```
<type>(<scope>): <descriptive subject ≤50 chars>

## Overview
<Review-ready summary of what/why; wrap at 72 cols>

## Changes
- <concrete change 1>
- <concrete change 2>

## Impact
<why it was needed and the effect; wrap at 72 cols>

<footer — e.g. Closes #123>
```

Types: feat · fix · docs · style · refactor · perf · test · build · ci · chore · revert.

## git hard rules

Never force-push · never `--no-verify` · never amend a pushed commit · never `reset --hard` · never commit secrets · never commit on `main`/`master`/`develop`.

## Done when

- The staged change set is committed with a Conventional Commits message carrying Overview / Changes / Impact sections.
- The action was confirmed (manual mode) or logged (auto mode) before the commit ran.
- No secrets were committed, and the commit was made on a feature branch (not a protected branch).
- The new commit hash/subject is reported back to the user.
