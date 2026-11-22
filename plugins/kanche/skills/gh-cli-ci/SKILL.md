---
name: gh-cli-ci
description: Inspect GitHub Actions PR checks and failed workflow logs via gh CLI for P5/P6 self-healing remediation. Read-only.
---

# /kanche:gh-cli-ci

**Summary.** Inspect GitHub Actions workflow runs and PR check statuses (`@devops` / `@gh-operator`), extracting failing job logs for `/kanche:debug-rca` and `/kanche:code-implement`. Read-only.

## Inputs

- `<pr-or-run-id>` (optional) — PR number, run ID, or current branch PR if omitted.
- `--watch` — stream active check status until completion (`gh pr checks --watch`).

## Steps

1. **Verify Auth & Repo:** Run `gh auth status` and resolve `-R <owner>/<repo>`.
2. **Inspect Checks & Recent Runs:**
   ```bash
   gh pr checks [<pr>] -R "$OWNER_REPO"
   gh run list -R "$OWNER_REPO" --branch "$(git rev-parse --abbrev-ref HEAD)" --limit 5
   ```
3. **Extract Failed Logs (when any check fails):**
   ```bash
   gh run view <run-id> -R "$OWNER_REPO" --log-failed
   ```
4. **Report Compact Diagnosis:** Output check table (Check | Status | Duration | URL), failing step excerpt, and hand off to `/kanche:debug-rca` or `/kanche:code-implement` if repairs are needed.

## Rules

- Strictly read-only (`gh run list/view`, `gh pr checks`). Never trigger or re-run workflows without explicit request.
- Follow `rules/token-optimization.md`.
