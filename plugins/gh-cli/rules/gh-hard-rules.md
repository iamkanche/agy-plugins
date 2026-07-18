# GitHub CLI Hard Rules

Always in effect for every `gh-cli` workflow:

- **Never approve your own PR.** Detect the PR author's login; if it matches the current user's login, block the approval command.
- **Never force-merge or bypass status checks.** All merge reviews and approvals must be submitted normally. Bypassing branch protections is strictly prohibited.
- **Use COMMENT event by default.** When submitting pull request reviews, always use `event=COMMENT` (never `APPROVE` or `REQUEST_CHANGES` unless explicitly instructed by the user).
- **Never expose secrets.** If API keys, credentials, private keys, or tokens are found in code diffs, redact them in the public review suggestions or notify the user privately.
- **Every side effect is human-gated.** Before creating a pull request, submitting review comments, approving a pull request, or replying to review threads: STOP and ask the user to confirm using the interactive `default_api:ask_question` tool, showing exactly what metadata/content will be posted to GitHub. Proceed only on an explicit yes (e.g. choosing the Proceed option in the question modal).
