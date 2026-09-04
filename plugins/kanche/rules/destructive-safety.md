# Destructive Action Safety Rules

## 1. Zero Autonomous Destructive Execution Policy

**NEVER execute destructive or remote-modifying commands autonomously.**

Under no circumstances may an agent or automated workflow (`mode=auto` or `/goal`) execute destructive commands without prior, explicit human confirmation via the interactive `default_api:ask_question` tool.

The following operations are classified as **Destructive or Remote-Mutating** and are strictly gated behind human confirmation:

| Category | Operations / Commands | Required Human Confirmation Gate |
|---|---|---|
| **Remote Git Mutations** | `git push`, `git push --tags`, `git push origin --delete` | Always prompt user showing branch/tag name and target remote. |
| **History Mutations** | `git commit`, `git merge`, `git rebase` | Always prompt user showing commit message, target branch, and staged files diff. |
| **Deletions & Drops** | `rm`, `rm -rf`, `git rm`, `git branch -d/-D`, `git tag -d`, `git stash drop` | Always prompt user showing exact path or reference to be deleted and data loss consequences. |
| **Pull Request Merges** | `gh pr merge` (all merge methods: `--merge`, `--squash`, `--rebase`) | Always prompt user showing PR number, title, target base, and branch deletion flag. |
| **Database & Environment Resets** | `migrate:fresh`, `migrate:reset`, dropping tables or databases, container purges | Always prompt user with high-visibility warning of irreversible data loss. |

---

## 2. Universal Confirmation Standard

Before executing any command listed above, the executing agent or skill MUST:
1. **STOP execution**.
2. **Display Context**: State precisely what command is about to run, target targets/branches/paths, and what changes or deletions will occur.
3. **Prompt the Human**: Invoke `default_api:ask_question` with explicit options:
   - `(Recommended) Yes, proceed with <action>`
   - `No, abort <action>`
4. **Enforce Decision**:
   - On selecting **Yes**: Proceed with the single confirmed command.
   - On selecting **No**: Immediately abort the action, leave working tree and remote untouched, and report the cancellation.

---

## 3. Skills Stand Alone Principle

- **Skills Are Decoupled and Isolated**: Individual skills do NOT contain internal "auto mode" bypass branches, caller-mode checks, or mode-conditional skips.
- Every skill stands completely on its own:
  - Destructive skills (`git-push`, `git-commit`, `git-branch-delete`, `git-stash`, `gh-cli-pr-merge`, `sdd-sync`) unconditionally present interactive confirmation gates via `default_api:ask_question`.
  - Non-destructive skills (`code-implement`, `qa-validate`, `design-specs`, `planner-tasks`) perform their focused domain tasks.
- **Orchestration Boundary**: High-level orchestrators (`/kanche:sdd-run`, `/kanche:sdd-continue`) coordinate skills in sequence, but skills never depend on the orchestrator's mode to govern their internal safety gates. Every skill is 100% safe and complete when invoked standalone.
