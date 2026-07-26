# Product Memory

<!-- durable cross-feature memory; written by /kanche:sdd-sync -->

- In **manual mode**, side-effect operations (git commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges) MUST gate on the interactive `default_api:ask_question` tool before proceeding.
- In **auto mode** (SDD `mode=auto`), the `default_api:ask_question` gate is suppressed for side-effect operations; the action is logged and executed immediately without a prompt, EXCEPT for PR merging when `auto_merge: false` (in `docs/settings.json`), which requires explicit human confirmation via `default_api:ask_question`.
- **Human-Gated Merges (`auto_merge: false`)**: Merging pull requests to the target branch (`main`) via `/kanche:gh-cli-pr-merge` or Phase P9 MUST ALWAYS gate on explicit human approval via the interactive `default_api:ask_question` tool before executing the merge.
- Safety invariants (no force-push, no `--no-verify`, protected-branch refusal, secrets detection, self-approval prohibition) are enforced unconditionally in both modes.
- Gated operations and commits MUST still be done using the formal slash command workflows from the `kanche` plugin (e.g. `/kanche:git-commit`, `/kanche:git-push`, `/kanche:gh-cli-pr-create`, `/kanche:gh-cli-pr-merge`, `/kanche:sdd-run`) instead of raw shell commands.
- **Flattened Plugin Skill Structure**: All 36 skills in the `kanche` plugin use single-level flattened subdirectories under `plugins/kanche/skills/<skill-name>/SKILL.md` (e.g. `sdd-init`, `git-commit`, `gh-cli-pr-create`) to ensure full compatibility with the `agy plugin install` CLI engine and AGY slash command discovery.
