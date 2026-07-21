# Product Memory

<!-- durable cross-feature memory; written by /sdd:preserve (NOT by sync-product) -->

- In **manual mode**, side-effect operations (git commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges) MUST gate on the interactive `default_api:ask_question` tool before proceeding.
- In **auto mode** (SDD `mode=auto`), the `default_api:ask_question` gate is suppressed for side-effect operations; the action is logged and executed immediately without a prompt.
- Safety invariants (no force-push, no `--no-verify`, protected-branch refusal, secrets detection, self-approval prohibition) are enforced unconditionally in both modes.
- Gated operations and commits MUST still be done using the formal slash command workflows from the `git` and `gh-cli` plugins (e.g. `/git:commit`, `/git:push`, `/gh-cli:pr-create`, `/gh-cli:pr-merge`) instead of raw shell commands.
- When `/sdd:run` or `/sdd:continue` is executed, the agent MUST strictly follow the defined SDD workflow phases and delegate phase execution and reviews to the designated specialized subagents (`sdd-analyst`, `sdd-architect`, `sdd-planner`, `sdd-coder`, `sdd-validator`) using the `invoke_subagent` tool, rather than running modifications directly in the parent context.
- Pull request merges executed via `/gh-cli:pr-merge` MUST default to the `--merge` (merge commit) method, adhering to the plugin specifications, unless a different merge method is explicitly specified by the user.
