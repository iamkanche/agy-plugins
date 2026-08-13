# Workflow Gating Rules

- **Manual Mode**: Every side-effect operation (git commit, git push, PR creation, PR merge, tag creation) MUST prompt the human for confirmation via interactive `default_api:ask_question`.
- **Auto Mode (`mode=auto`)**: Side-effect operations are executed automatically and logged, EXCEPT PR merging when `auto_merge: false` in `.docs/settings.json`, which still requires explicit confirmation.
- **Safety Invariants**: Safety rules (no force push, no secrets, no protected branch edits, no self approval) apply unconditionally in both manual and auto modes.
