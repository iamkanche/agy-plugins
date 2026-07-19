# Steering Rules

- **Feature Branching**: All modifications must be committed on feature branches checked out from the default branch.
- **Explicit Human Gates**: Gated confirmations are required for all repository-modifying actions (commits, pushes, pull request creations, and posting API reviews).
- **Autonomy & Decisions**: The AI is empowered to decide the best approaches for implementation, design, and specifications autonomously, but must explicitly list all key design decisions in the respective documentation files.
- **No Force-Pushes**: Force-pushing (`--force`, `--force-with-lease`) is strictly prohibited.
- **No Verification Bypass**: Bypassing pre-commit hooks (`--no-verify`) is strictly prohibited.
- **Never amend a pushed commit** (grounded in `plugins/git/rules/git-hard-rules.md`).
- **Never `git reset --hard` on shared work** (grounded in `plugins/git/rules/git-hard-rules.md`).
- **Never commit secrets** (such as `.env`, credentials, private keys, or tokens) (grounded in `plugins/git/rules/git-hard-rules.md` and `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Never approve your own PR** (grounded in `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Never force-merge or bypass status checks** (grounded in `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Use COMMENT event by default** when reviewing a PR unless explicitly instructed (grounded in `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Interactive Question Gating**: Every side effect (commits, pushes, PR creation/approval/merge, tag creation/deletion) must use the interactive `default_api:ask_question` tool (grounded in `.sdd-docs/product/memory.md` and hard rules).
