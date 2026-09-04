---
name: gh-cli-pr-review
description: Review a pull request diff against AGENTS.md rules and post structured inline suggestion comments to GitHub with .json format support.
model: flash
---

# /kanche:gh-cli-pr-review

**Summary.** Review a pull request and post structured findings to GitHub, functioning as the **PR Auditor / Reviewer Skill** in Phase P6 of the Loop Engineering Framework. The workflow delegates to the specialized `@gh-operator` subagent to perform all GitHub CLI and API remote interactions, auditing touched files against `AGENTS.md` and repository guidelines. Supports `--json` format to generate a standardized `review.json` payload for one-shot review and inline comment submission.

## Loop Engineering Protocol (Reviewer Role — P6 PR Review Loop)

In the Loop Engineering Framework, `/kanche:gh-cli-pr-review` acts as the **PR Auditor Skill** paired with `/kanche:gh-cli-pr-respond`:
- Inspects PR diffs, CI checks, and repo rules.
- Emits structured review summary and inline GitHub code suggestions (`HIGH` / `MEDIUM` / `LOW`).
- Supports `.json` payload generation conforming to the GitHub PR review schema.
- Drives the ≤3x closed-loop cycle: `/kanche:gh-cli-pr-review` → `/kanche:gh-cli-pr-respond` → `/kanche:git-commit` → `/kanche:git-push`.

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to review. If omitted, `gh` resolves the PR for the current branch.
- `--json` / `--format=json` (flag, optional) — export and save the review payload in standardized JSON format (`review.json`) and output machine-readable JSON.

## Steps

1. **Invoke gh-operator for authentication check.** Verify `gh` is authenticated (`gh auth status`).
2. **Fetch PR metadata, diff, and checks.** Retrieve target branch metadata, diff contents, and head SHA (`headRefOid`).
   ```bash
   PR="<pr-number or current>"
   HEAD_OID=$(gh pr view $PR --json headRefOid -q .headRefOid)
   gh pr diff $PR
   ```
3. **Assess diff size.** Target ~400–500 substantive lines; note size in Summary if larger.
4. **Audit touched files against repository rules.** Audit changes specifically against guidelines in `AGENTS.md`, `plugins/kanche/rules/destructive-safety.md`, and `plugins/kanche/rules/loop-engineering.md`.
5. **Classify each finding** as **HIGH** (Critical Bugs / Security / Breaking), **MEDIUM** (Correctness Risk / Test Coverage), or **LOW** (Documentation / Style Nit). Format inline comments pointing directly to file and lines of code:

   ````markdown
   [<SEVERITY>] <Short description>
   Issue: <what is wrong with the code>
   Suggestion:
   ```suggestion
   <suggested code replacement>
   ```
   Why: <explanation>
   ````

6. **Build the review body and JSON payload:**
   - **Review Comment Body Structure**:
     Must strictly follow the `#  Summary` layout:
     - `#  Summary`: short summary sentence, severity score (e.g. `Severity: eg: 6/10`), total files reviewed, total lines of code reviewed.
     - `## Review Summary`: GitHub Markdown table (`|---|`) detailing `Severity`, `Count`, and `Category` with `🔴 HIGH`, `🟡 MEDIUM`, `🟢 LOW`.
     - `---` divider.
     - `Inline comment directly to the files and lines of codes` anchor line.
   - **JSON Format Structure (`review.json`)**:
     Format according to the GitHub REST API Pull Request Review schema:
     ```json
     {
       "commit_id": "<HEAD_OID>",
       "body": "#  Summary\n- <short summary>\n- Severity: eg: 6/10\n- Total files: <x> files\n- Total lines: <x> lines of codes\n\n## Review Summary\n\n| Severity | Count | Category |\n|---|---|---|\n| 🔴 HIGH | 0 | Critical Bugs / Security / Breaking |\n| 🟡 MEDIUM | 0 | Correctness Risk / Test Coverage |\n| 🟢 LOW | 1 | Documentation / Style Nit |\n\n---\nInline comment directly to the files and lines of codes",
       "event": "COMMENT",
       "comments": [
         {
           "path": "<file_path>",
           "line": <line_number>,
           "side": "RIGHT",
           "body": "[<SEVERITY>] <description>\nIssue: <details>\nSuggestion:\n```suggestion\n<replacement>\n```\nWhy: <rationale>"
         }
       ]
     }
     ```

7. **Save JSON Format when requested.** If `--json` is passed, write the payload to `review.json` and output the JSON to chat.
8. **Gate — STOP.** Ask user to confirm posting review to GitHub using `default_api:ask_question`. Show review summary counts and number of inline comments.
9. **Post review and inline comments in one single request** via `gh api`:

   ```bash
   gh api --method POST "repos/{owner}/{repo}/pulls/$PR/reviews" --input review.json
   ```

10. **Report** posted review URL, counts, and status.

## Target Output Format

All generated PR review comment bodies posted on GitHub must strictly adhere to the following verbatim structure:

`````markdown
#  Summary
- Short PR review summary
- Severity: eg: 6/10
- Total files: x files
- Total lines: x lines of codes

## Review Summary

| Severity | Count | Category |
|---|---|---|
| 🔴 HIGH | 0 | Critical Bugs / Security / Breaking |
| 🟡 MEDIUM | 0 | Correctness Risk / Test Coverage |
| 🟢 LOW | 1 | Documentation / Style Nit |

---
Inline comment directly to the files and lines of codes
`````

*Inline comments are posted directly to the files and line numbers on GitHub via the `comments` array in the review JSON payload.*

## Rules

- Read-only to working tree and git history — posts PR review via `gh`.
- Follow `plugins/kanche/rules/destructive-safety.md` and `plugins/kanche/rules/loop-engineering.md` for PR review-respond loop governance.
- Never approve PRs automatically; default event is always `COMMENT`.
