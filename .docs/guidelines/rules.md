# Steering Rules

- **Feature Branching**: All modifications must be committed on feature branches checked out from the default branch.
- **Explicit Human Gates**: Gated human confirmations via the interactive `default_api:ask_question` tool are unconditionally required for all destructive and remote-mutating actions (commits, pushes, pull request merges, branch/tag deletions, and directory deletions). Skills stand alone and never bypass these gates.
- **Autonomy & Decisions**: The AI is empowered to decide the best approaches for implementation, design, and specifications autonomously, but must explicitly list all key design decisions in the respective documentation files.
- **No Force-Pushes**: Force-pushing (`--force`, `--force-with-lease`) is strictly prohibited.
- **No Verification Bypass**: Bypassing pre-commit hooks (`--no-verify`) is strictly prohibited.
- **Never amend a pushed commit** (grounded in `plugins/kanche/rules/git-hard-rules.md`).
- **Never `git reset --hard` on shared work** (grounded in `plugins/kanche/rules/git-hard-rules.md`).
- **Never commit secrets** (such as `.env`, credentials, private keys, or tokens) (grounded in `plugins/kanche/rules/git-hard-rules.md` and `plugins/kanche/rules/gh-hard-rules.md`).
- **Never approve your own PR** (grounded in `plugins/kanche/rules/gh-hard-rules.md`).
- **Never force-merge or bypass status checks** (grounded in `plugins/kanche/rules/gh-hard-rules.md`).
- **Use COMMENT event by default** when reviewing a PR unless explicitly instructed (grounded in `plugins/kanche/rules/gh-hard-rules.md`).
- **Interactive Question Gating**: Every side effect (commits, pushes, PR creation/approval/merge, tag creation/deletion, directory removal) must use the interactive `default_api:ask_question` tool. Autonomous execution of destructive commands without explicit human approval is strictly prohibited across all modes. (Grounded in `plugins/kanche/rules/destructive-safety.md` and `.docs/product/memory.md`.)
- **Plugin Gating Enforcement**: Always use the formal slash command workflows from the `kanche` plugin (e.g. `/kanche:git-commit`, `/kanche:git-push`, `/kanche:gh-cli-pr-create`, `/kanche:gh-cli-pr-merge`, `/kanche:sdd-run`) instead of raw shell commands for repository-modifying actions. This ensures that Conventional Commit message structures (Overview/Changes/Impact) and all safety gating questions are consistently applied.
