# Workflow Gating (SDD)

Antigravity has no per-command tool permissions; gating is enforced by prose + your autonomy level.

- **AI-Driven Decisions**: The AI can autonomously decide which is the best approach, design pattern, or answer for a given task. There is no need to pause for human approval on choices or approaches.
- **Document Decisions**: The AI must explicitly list all decisions, choices, and architectural approaches it makes during the workflow (e.g., in a development notes file or within the generated document's context section).
- **Side Effect Confirmation**: Before any repository-modifying side effect — committing code, pushing branches, creating PRs, or publishing tags — **STOP and ask the user to confirm using the interactive `default_api:ask_question` tool**, showing exactly what changes will be written. Never commit or push on assumed consent.
- **Phase Execution**: Inner-loop phases (specs, design, tasks, build) run generate → review cycles up to 3× until the review returns GO, then commit via the `git` plugin's `commit` workflow under the git commit gate.

