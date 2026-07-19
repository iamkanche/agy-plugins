# Product Memory

<!-- durable cross-feature memory; written by /sdd:preserve (NOT by sync-product) -->

- Human gating side-effect operations MUST use the interactive `default_api:ask_question` tool instead of raw text prompts.
- Gated operations include git commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges.
- Manual phase transitions, validation failures, and LEVEL 2 checkpoints in SDD workflow execution also use `default_api:ask_question`.
- Gated operations and commits MUST be done using the formal slash command workflows from the `git` and `gh-cli` plugins (e.g. `/git:commit`, `/git:push`, `/gh-cli:pr-create`, `/gh-cli:pr-merge`) instead of raw shell commands to enforce structured commit message sections (Overview/Changes/Impact) and gating validations.
