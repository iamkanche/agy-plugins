---
name: gh-cli-pr-respond
description: Triage PR review comments, apply code fixes locally, commit via /kanche:git-commit, push, resolve threads via GraphQL, and reply to reviewers in-thread.
---

# /kanche:gh-cli-pr-respond

**Summary.** Fetch a PR's review comments and threads, triage each one, apply actionable code fixes locally, commit via `/kanche:git-commit`, push via `/kanche:git-push`, resolve threads via GraphQL API, and reply to reviewers in-thread. The workflow delegates GitHub operations to `@gh-operator` and git actions to `@git-operator`.

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to respond to. If omitted, `gh` resolves the PR for the current branch.

## Steps

1. **Verify gh auth.**

   ```bash
   gh auth status
   ```

2. **Fetch all PR review comments and threads.**

   ```bash
   PR="<pr-number or empty for current branch>"
   gh pr view $PR --json number,title,comments,reviews
   gh api "repos/{owner}/{repo}/pulls/${PR}/comments"
   ```

3. **Filter and group comments.** Group by file/thread, filtering out resolved threads.

4. **Triage and plan responses.** Draft code fixes and response text.

5. **Gate (Triage Review) — mode-conditional.** Log in auto mode, or ask via `default_api:ask_question` in manual mode.

6. **Apply code fixes locally.** Modify files and run local verification tests.

7. **Stage, commit, and push.** Execute commits exclusively via `/kanche:git-commit` with conventional commit message (`fix({slug}): address PR review feedback`) and push via `/kanche:git-push`.

8. **Gate (Reply Confirmation) — mode-conditional.**

9. **Submit replies and resolve threads.** Post replies to threads and execute GraphQL thread resolution:

   ```bash
   gh api --method POST "repos/{owner}/{repo}/pulls/comments/<comment_id>/replies" -f body="<reply text>"

   gh api graphql -f query='
     mutation {
       resolveReviewThread(input: { threadId: "<thread_id>" }) {
         thread { isResolved }
       }
     }
   '
   ```

10. **Report** status, updated files, and resolved threads.

## Done when

- Feedback triaged, fixes applied and verified.
- Commits formatted via `/kanche:git-commit` and pushed to origin.
- Replies posted and review threads resolved via GitHub API.
