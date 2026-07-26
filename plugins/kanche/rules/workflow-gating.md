# Workflow Gating (SDD)

Antigravity has no per-command tool permissions; gating is enforced by prose + your autonomy level.

- **AI-Driven Decisions**: The AI can autonomously decide which is the best approach, design pattern, or answer for a given task. There is no need to pause for human approval on choices or approaches.
- **Document Decisions**: The AI must explicitly list all decisions, choices, and architectural approaches it makes during the workflow (e.g., in a development notes file or within the generated document's context section).
- **Side Effect Confirmation**: Before any repository-modifying side effect — committing code, pushing branches, creating PRs, or publishing tags — apply the mode-conditional gate: in **manual mode** (or standalone invocation), STOP and ask the user to confirm using the interactive `default_api:ask_question` tool, showing exactly what changes will be written; in **auto mode**, log the action (what will be written, the exact command, and the target branch) and proceed immediately (except for PR merging when `auto_merge: false` in `.sdd-docs/settings.json`, which must always gate on explicit human confirmation). Never commit or push on assumed consent in manual mode.
- **Phase Execution**: Inner-loop phases (specs, design, tasks, build) run generate → review cycles up to 3× until the review returns GO, then commit via the `git` plugin's `commit` workflow under the git commit gate.
- **Plugin Enforcement**: Never run raw Git or GitHub CLI commands directly on the command line shell for repository-modifying operations (such as commits, pushes, tag creations, or pull request creations/merges). Always invoke the corresponding slash command workflows from the `git` and `gh-cli` plugins (e.g., `/git:commit`, `/git:push`, `/gh-cli:pr-create`, `/gh-cli:pr-merge`) to perform these operations, ensuring that Conventional Commit templates (Overview/Changes/Impact) and gating structures are strictly applied at all times.

