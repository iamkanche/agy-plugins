---
name: pr-review
description: Review a pull request diff against AGENTS.md rules and post structured inline suggestion comments to GitHub.
---

# /kanche:pr-review

**Summary.** Review a pull request and post the result to GitHub. The workflow delegates to the specialized `@gh-operator` subagent (defined in `agents/gh-operator/agent.json`) to perform all GitHub CLI and API remote interactions, while ensuring the code audit checks adherence to all repository rules, guidelines, and styles defined in `AGENTS.md` (located locally in `.agents/AGENTS.md` or globally in `~/.gemini/config/AGENTS.md`). All actions are gated behind human confirmation.

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to review. If omitted, `gh` resolves the PR for the current branch.

## Steps

1. **Invoke gh-operator for authentication check.** Verify `gh` is authenticated.

   ```bash
   gh auth status
   ```

2. **Fetch PR metadata, diff, and checks.** The `@gh-operator` subagent retrieves the target branch metadata and diff contents. Capture the head commit SHA (`headRefOid`) — inline comments must anchor to it.

   ```bash
   PR="<pr-number or empty for current branch>"
   gh pr view $PR --json number,title,author,baseRefName,headRefName,headRefOid,additions,deletions,files
   gh pr diff $PR
   gh pr checks $PR
   ```

3. **Assess diff size.** Target ~400–500 substantive lines; if larger, note it in the Summary and recommend splitting (exclude generated/mock files and large mechanical renames from the count). Informational — continue the full review regardless.

4. **Audit touched files against repository rules.** Read touched files for context and check call sites, related tests, and patterns. **Audit the changes specifically against repository rules, guidelines, styles, and conventions defined in AGENTS.md** (located locally in `.agents/AGENTS.md` or globally in `~/.gemini/config/AGENTS.md`). Assess correctness, error handling, security (no secrets, no injection), test coverage, and repo-convention adherence.

5. **Classify each finding** as **HIGH** (bug/security/breaking), **MEDIUM** (correctness risk, missing test, notable smell), or **LOW** (style/nit/optional).

   For each finding, record: `file`, `line` (a line in the diff), `severity`, and **format the comment body exactly as follows**:

   ```
   [<SEVERITY>] <Short description>
   Issue: <what is wrong with the code>
   Suggestion:
   ```suggestion
   <suggested code replacement>
   ```
   Why: <explanation of why this suggestion is recommended>
   ```

   Note:
   - `<SEVERITY>` must be HIGH, MEDIUM, or LOW in uppercase.
   - The code block inside ```suggestion must be a valid dropped-in replacement for the code on target `line`.

6. **Build the review body** in this exact shape:

   ```markdown
   ## Summary

   <2–4 sentence prose summary: what the PR does, overall quality, and any diff-size flag.>

   | Severity | Count |
   |----------|-------|
   | HIGH     | <n>   |
   | MEDIUM   | <n>   |
   | LOW      | <n>   |

   CI: <passing / failing — brief>
   ```

7. **Gate — STOP.** Show the full review body **and** the list of inline comments (each as `file:line — severity — comment`), then ask the user to confirm posting this review to PR #<n> (summary + <k> inline comments) using the interactive `default_api:ask_question` tool with options `(Recommended) Yes, post review` and `No, abort`. Proceed only on selecting Yes; on No, print everything and STOP without posting.

8. **Post the review with inline comments in one request.** The `@gh-operator` subagent posts the review with comments anchored to the target file lines. Use the reviews API with the head SHA from step 2:

   ```bash
   gh api --method POST "repos/{owner}/{repo}/pulls/${PR}/reviews" \
     -f commit_id="<headRefOid>" \
     -f event="COMMENT" \
     -f body="<the Summary body from step 6>" \
     -F 'comments[][path]=<file>'  -F 'comments[][line]=<line>' -F 'comments[][side]=RIGHT' -F 'comments[][body]=<comment>' \
     # repeat the four comments[][*] fields per inline comment
   ```

   Notes: `line` must be a line present in the diff on the given `side` (`RIGHT` = the new version); for a deleted line use `side=LEFT`. If a comment's line can't be anchored in the diff, fold it into the summary body instead of dropping it. Use `event=COMMENT` (never `APPROVE`/`REQUEST_CHANGES` — approval is the human's call). Post secrets to no one.

9. **Report** the posted review URL, the counts, and any comments that were folded into the summary because their line wasn't in the diff.

## git hard rules

Read-only to the working tree and to git history — this command only posts a PR **review** via `gh`, never commits, pushes, approves, or requests changes. Posting happens only after the gate.

## Done when

- A Summary (prose + HIGH/MEDIUM/LOW count table + CI line) and per-line inline comments were prepared.
- Inline comments conform to the `[<SEVERITY>] Short description\nIssue:\nSuggestion:\n\`\`\`suggestion\n...\n\`\`\`\nWhy:` format.
- The user confirmed via the gate; the review + inline comments were posted to the PR in one request (or the user chose not to post and everything was shown instead).
- The `@gh-operator` subagent was used to execute remote repository interactions.
- Touch files are audited against all active repository guidelines in `AGENTS.md`.
