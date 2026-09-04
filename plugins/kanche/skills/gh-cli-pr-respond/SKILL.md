---
name: gh-cli-pr-respond
description: Triage PR review comments, apply code fixes locally, commit via /kanche:git-commit, push, resolve threads via GraphQL, and reply to reviewers in-thread.
model: flash
---

# /kanche:gh-cli-pr-respond

**Summary.** Fetch PR review comments and threads, triage feedback, execute targeted code fixes locally (via `/kanche:code-implement`), commit via `/kanche:git-commit`, push via `/kanche:git-push`, resolve threads via GraphQL API, and reply in-thread, functioning as the **PR Responder / Generator Skill** in the Loop Engineering Framework.

## Loop Engineering Protocol (Generator / Responder Role — PR Review Loop)

In the Loop Engineering Framework, `/kanche:gh-cli-pr-respond` acts as the **PR Fixer & Responder Skill** paired with `/kanche:gh-cli-pr-review`:
- Parses inline review comments and findings posted by `/kanche:gh-cli-pr-review` or human reviewers.
- Delegates local code modifications to `/kanche:code-implement` to perform targeted delta fixes.
- Re-runs local verification checks to ensure zero regressions before committing and pushing.
- Posts thread replies and marks resolved threads via GitHub API.

## Inputs

Parse the invocation arguments:

- `<pr-number>` (positional, optional) — the PR to respond to. If omitted, `gh` resolves the PR for the current branch.

## Steps

1. **Verify gh auth.** (`gh auth status`)
2. **Fetch all PR review comments and threads.** Retrieve unresolved comments and thread IDs.
3. **Filter and group comments.** Group by file/thread, filtering out already resolved threads.
4. **Triage and plan responses.** Draft targeted code fixes and response text.
5. **Triage and Review Plan.** Inspect unresolved comments and draft targeted code fix plans against repository standards.
6. **Apply code fixes locally.** Invoke `/kanche:code-implement` with review findings to apply targeted fixes and run tests.
7. **Stage, commit, and push.** Execute commits strictly via `/kanche:git-commit` (`fix({slug}): address PR review feedback`) and push via `/kanche:git-push`.
8. **Prepare thread replies & resolutions.** Verify reply messages and target thread IDs before posting.
9. **Submit replies and resolve threads.** Post replies to threads and execute GraphQL thread resolution:

   ```bash
   gh api --method POST "repos/{owner}/{repo}/pulls/comments/<comment_id>/replies" -f body="<reply text>"
   gh api graphql -f query='mutation { resolveReviewThread(input: { threadId: "<thread_id>" }) { thread { isResolved } } }'
   ```

10. **Report** status, updated files, resolved threads, and loop iteration state.

## Rules

- Follow `plugins/kanche/rules/loop-engineering.md` for closed-loop iteration governance (≤3x loop).
- Code fixes must be committed exclusively via `/kanche:git-commit` and pushed via `/kanche:git-push`.

