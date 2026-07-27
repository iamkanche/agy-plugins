---
name: gh-cli-pr-review
description: Review a pull request diff against AGENTS.md rules and post structured inline suggestion comments to GitHub.
---

# /kanche:gh-cli-pr-review

**Summary.** Review a pull request and post structured findings to GitHub, functioning as the **PR Auditor / Reviewer Skill** in Phase P6 of the Loop Engineering Framework. The workflow delegates to the specialized `@gh-operator` subagent to perform all GitHub CLI and API remote interactions, auditing touched files against `AGENTS.md` and repository guidelines.

## Loop Engineering Protocol (Reviewer Role — P6 PR Review Loop)

In the Loop Engineering Framework, `/kanche:gh-cli-pr-review` acts as the **PR Auditor Skill** paired with `/kanche:gh-cli-pr-respond`:
- Inspects PR diffs, CI checks, and repo rules.
- Emits structured review summary and inline GitHub code suggestions (`HIGH` / `MEDIUM` / `LOW`).
- Drives the ≤3x closed-loop cycle: `/kanche:gh-cli-pr-review` → `/kanche:gh-cli-pr-respond` → `/kanche:git-commit` → `/kanche:git-push`.

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to review. If omitted, `gh` resolves the PR for the current branch.

## Steps

1. **Invoke gh-operator for authentication check.** Verify `gh` is authenticated (`gh auth status`).
2. **Fetch PR metadata, diff, and checks.** Retrieve target branch metadata, diff contents, and head SHA (`headRefOid`).
3. **Assess diff size.** Target ~400–500 substantive lines; note size in Summary if larger.
4. **Audit touched files against repository rules.** Audit changes specifically against guidelines in `AGENTS.md` and `plugins/kanche/rules/loop-engineering.md`.
5. **Classify each finding** as **HIGH** (bug/security/breaking), **MEDIUM** (correctness risk, missing test), or **LOW** (style/nit/optional). Format inline comments:

   ```
   [<SEVERITY>] <Short description>
   Issue: <what is wrong with the code>
   Suggestion:
   ```suggestion
   <suggested code replacement>
   ```
   Why: <explanation>
   ```

6. **Build the review body** (Summary + severity count table + CI line).
7. **Gate — STOP.** Ask user to confirm posting review to GitHub (or auto-confirm in automated SDD runs).
8. **Post the review with inline comments in one request** via `@gh-operator`.
9. **Report** posted review URL, counts, and status.

## Rules

- Read-only to working tree and git history — posts PR review via `gh`.
- Follow `plugins/kanche/rules/loop-engineering.md` for PR review-respond loop governance.

