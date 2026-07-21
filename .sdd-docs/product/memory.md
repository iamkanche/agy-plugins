# Product Memory

<!-- durable cross-feature memory; written by /sdd:preserve (NOT by sync-product) -->

- In **manual mode**, side-effect operations (git commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges) MUST gate on the interactive `default_api:ask_question` tool before proceeding.
- In **auto mode** (SDD `mode=auto`), the `default_api:ask_question` gate is suppressed for side-effect operations; the action is logged and executed immediately without a prompt.
- Safety invariants (no force-push, no `--no-verify`, protected-branch refusal, secrets detection, self-approval prohibition) are enforced unconditionally in both modes.
- Gated operations and commits MUST still be done using the formal slash command workflows from the `git` and `gh-cli` plugins (e.g. `/git:commit`, `/git:push`, `/gh-cli:pr-create`, `/gh-cli:pr-merge`) instead of raw shell commands.
