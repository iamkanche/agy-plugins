---
name: gh-cli-issue
description: Sync local Scrum PBIs (.docs/backlog/{domain}/PBI-*.md) with GitHub Issues using gh CLI, gated on mutations.
---

# /kanche:gh-cli-issue

**Summary.** Create, list, view, or close GitHub Issues (`@gh-operator` & `@scrum-master`) and link `.docs/backlog/{domain}/PBI-*.md` items to PRs (`Closes #<issue>`). Keep interactive `default_api:ask_question` confirmation gates in the main conversation.

## Inputs

- Subcommand: `list` (read-only), `view <num>` (read-only), `create <pbi-path-or-title>`, `close <num>`.
- `-R <owner>/<repo>` (inferred from `git remote get-url origin` if omitted, matching `permissioned-github`).

## Steps

1. **Verify Auth & Repo:** Run `gh auth status` and resolve `OWNER_REPO`.
2. **Read-Only Subcommands (`list`, `view`):**
   ```bash
   gh issue list -R "$OWNER_REPO" --state open --limit 20
   gh issue view <num> -R "$OWNER_REPO"
   ```
3. **Create / Sync from PBI (`create`):**
   - Read target `.docs/backlog/{domain}/PBI-*.md`; compose concise issue title + User Story & Acceptance Criteria body.
   - **Gate — STOP:** Prompt user via `default_api:ask_question` displaying title, labels, and repo before running `gh issue create`.
   - Execute `gh issue create -R "$OWNER_REPO" --title "<title>" --body "<body>"` and record the issue URL/number back in the PBI file (`- **GitHub Issue:** #<num>`).
4. **Close Issue (`close`):**
   - **Gate — STOP:** Prompt user via `default_api:ask_question` before running `gh issue close <num> -R "$OWNER_REPO"`.

## Rules

- Never create, edit, or close GitHub issues without human confirmation.
- Never include secrets or local absolute machine paths in issue bodies.
- Follow `rules/gh-hard-rules.md` and `rules/token-optimization.md`.
