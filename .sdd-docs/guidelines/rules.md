# Steering Rules

- **Feature Branching**: All modifications must be committed on feature branches checked out from the default branch.
- **Explicit Human Gates**: In manual mode, gated confirmations are required for all repository-modifying actions (commits, pushes, pull request creations, and posting API reviews). In SDD auto mode, these gates are suppressed and actions proceed automatically; safety invariants remain unconditional in both modes.
- **Autonomy & Decisions**: The AI is empowered to decide the best approaches for implementation, design, and specifications autonomously, but must explicitly list all key design decisions in the respective documentation files.
- **No Force-Pushes**: Force-pushing (`--force`, `--force-with-lease`) is strictly prohibited.
- **No Verification Bypass**: Bypassing pre-commit hooks (`--no-verify`) is strictly prohibited.
- **Never amend a pushed commit** (grounded in `plugins/git/rules/git-hard-rules.md`).
- **Never `git reset --hard` on shared work** (grounded in `plugins/git/rules/git-hard-rules.md`).
- **Never commit secrets** (such as `.env`, credentials, private keys, or tokens) (grounded in `plugins/git/rules/git-hard-rules.md` and `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Never approve your own PR** (grounded in `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Never force-merge or bypass status checks** (grounded in `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Use COMMENT event by default** when reviewing a PR unless explicitly instructed (grounded in `plugins/gh-cli/rules/gh-hard-rules.md`).
- **Interactive Question Gating**: In manual mode (or standalone skill invocation), every side effect (commits, pushes, PR creation/approval/merge, tag creation/deletion) must use the interactive `default_api:ask_question` tool. In SDD auto mode, the gate is suppressed and replaced by a logged action record. (Grounded in `.sdd-docs/product/memory.md` and hard rules.)
- **Plugin Gating Enforcement**: Always use the formal slash command workflows from the `git` and `gh-cli` plugins (e.g. `/git:commit`, `/git:push`, `/gh-cli:pr-create`, `/gh-cli:pr-merge`) instead of raw shell commands for repository-modifying actions. This ensures that Conventional Commit message structures (Overview/Changes/Impact) and all safety gating questions are consistently applied.
