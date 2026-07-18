# /gh-cli:pr-respond

**Summary.** Fetch a PR's review comments and threads, triage each one, apply the actionable code fixes locally, then commit, push, and reply to the reviewers — each side effect behind its own explicit confirmation. The workflow delegates GitHub PR view, comment queries, and replies to the specialized `@gh-operator` subagent (defined in `agents/gh-operator/agent.json`), and local workspace modifications, commits, and pushes to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to respond to. If omitted, `gh` resolves the PR for the current branch.

No options are required.

## Steps

1. **Verify gh auth.** Check auth status before making requests.

   ```bash
   gh auth status
   ```

2. **Fetch all PR review comments and threads.**

   ```bash
   PR="<pr-number or empty for current branch>"
   gh pr view $PR --json number,title,comments,reviews
   gh api "repos/{owner}/{repo}/pulls/${PR}/comments"
   ```

3. **Filter and group comments.** Group comments by file and thread. Filter out resolved/outdated threads. Identify open feedback, especially those containing explicit requests or suggestions.

4. **Triage and plan responses.** For each active thread:
   - Identify if it requires a code change or a text reply.
   - For code changes, draft the exact local changes needed.
   - For text replies, draft the explanation.

5. **Gate (Triage Review) — STOP.** Show the user the list of active comments, your proposed code changes, and your drafted text replies. Proceed only on an explicit yes; if the user wants revisions, update and re-ask.

6. **Apply code fixes locally.** Modify the target files in the workspace. Verify compilation, build, and tests locally.

7. **Stage, commit, and push.** Stage the changes, commit using conventional commit patterns, and push. **This step delegates local operations to the `@git-operator` subagent.**

   ```bash
   git add <modified-files>
   git commit -m "fix(pr): address review feedback on <topic>"
   git push origin <branch>
   ```

8. **Gate (Reply Confirmation) — STOP.** Verify the code is pushed successfully, and present the final text replies you will post to GitHub. Ask for user confirmation.

9. **Submit replies to threads.** For each comment thread, post the reply and optionally resolve it. **This step delegates GitHub API updates to the `@gh-operator` subagent.**

   ```bash
   gh api --method POST "repos/{owner}/{repo}/pulls/comments/<comment_id>/replies" \
     -f body="<reply text>"
   ```

10. **Report** all threads replied to, files updated, and the push status.

## git hard rules

Never force-push · never commit directly without testing · never reply without confirming the local code changes are pushed successfully.

## Done when

- All active feedback comments and threads were fetched and triaged.
- Proposed code changes and replies were reviewed and approved by the user.
- Local code changes were made, verified, committed, and pushed to origin.
- Text replies were posted back to the respective comment threads on GitHub.
