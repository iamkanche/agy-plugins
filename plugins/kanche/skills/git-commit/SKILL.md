---
name: git-commit
description: Commit staged work with a Conventional Commits message gated behind explicit confirmation. Use when ready to record changes.
model: flash
---

# /kanche:git-commit

**Summary.** Commit staged work with a Conventional Commits message (Overview / Changes / Impact) gated behind explicit confirmation. Delegated to `@git-operator` per `rules/destructive-safety.md` and `rules/token-optimization.md`.

## Inputs

- `--all` — stage all tracked modifications (`git add -A`) before committing.
- `--scope=<scope>` — Conventional Commits scope (inferred if omitted).

## Steps

1. **Verify Git Repo:** Run `git rev-parse --is-inside-work-tree`. If not inside repo, stop.
2. **Refuse Protected Branches:** Fail if branch is `main`, `master`, or `develop`. Require a feature branch (`/kanche:git-branch-create`).
3. **Inspect Diff & Secrets:** Run `git status --short` and `git diff --staged`. Check for secrets (`.env`, credentials, private keys). Stop if secrets found.
4. **Stage Changes:** If `--all`, run `git add -A`. Verify staged diff exists via `git diff --staged --quiet`.
5. **Compose Commit Message:**
   - Subject: `<type>(<scope>): <subject ≤50 chars>`
   - Body sections: `## Overview`, `## Changes`, `## Impact`, optional `<footer>`.
6. **Mandatory Confirmation Gate:**
   - Stop and prompt user via `default_api:ask_question`:
     - Options: `(Recommended) Yes, commit these changes`, `No, abort commit`.
     - Present branch, commit message, and staged file list.
     - Stop if user does not confirm.
7. **Commit via HEREDOC:** Run `git commit -F - <<'EOF' ... EOF` (never use `--no-verify`).
8. **Report Commit:** Output `git log -1 --oneline`.

## Commit Message Format

```
<type>(<scope>): <subject ≤50 chars>

## Overview
<Review summary; wrapped at 72 cols>

## Changes
- <change 1>
- <change 2>

## Impact
<effect of change; wrapped at 72 cols>

<footer>
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

## Rules

- Enforce `rules/destructive-safety.md`, `rules/git-hard-rules.md`, and `rules/token-optimization.md`.
- Never commit autonomously without interactive confirmation.
- Never commit secrets or commit on protected branches.

## Done when

- Staged changes committed on feature branch with confirmed Conventional Commits message.
- Human confirmation received before commit execution.
- Resulting commit hash reported.
