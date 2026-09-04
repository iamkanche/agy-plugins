# Workflow Gating Rules

- **Destructive Operations Policy**: Every destructive or remote-modifying operation (`git push`, `git commit`, `rm`, `rm -rf`, branch/tag deletions, `git stash drop`, and `gh pr merge`) MUST prompt the human for confirmation via interactive `default_api:ask_question` unconditionally.
- **Skills Stand Alone**: Individual skills do not embed auto-mode bypass logic, caller-mode checks, or mode-conditional skips. Every skill is self-contained, modular, and independently safe.
- **Manual Mode (`mode=manual`)**: Orchestrators prompt the human before advancing between phases.
- **Auto Mode (`mode=auto`)**: Orchestrators run non-destructive phases continuously. Destructive operations in skills unconditionally halt for human confirmation.
- **Safety Invariants**: Safety rules (no force push, no secrets, no protected branch edits, no self approval, no autonomous destructive commands) apply unconditionally across all skills, agents, and workflows.

