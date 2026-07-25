# Antigravity Git Plugin

A namespaced plugin bundle for Google Antigravity that packages robust, secure git workflow commands and strict repository rules.

This plugin ensures all agent-driven Git modifications conform to professional repository practices and safety standards.

## Security Rules (rules/git-hard-rules.md)

The following hard rules are active across all git operations:

1. **No Force-Pushes**: Actions will never execute `git push --force` or `--force-with-lease`.
2. **No Verification Bypass**: Commands will never use `--no-verify` (pre-commit hooks must run).
3. **No Rewriting Shared History**: Changing history on pushed commits or protected branches is strictly prohibited.
4. **No Secrets in Repo**: File additions are scanned for keys, credentials, or `.env` files.
5. **No Deletion of Protected Branches**: Cannot delete `main`, `master`, or `develop` branches.
6. **Explicit Human Gates**: All side effects (commits, pushes, tags) require explicit human confirmation.

## Available Slash Commands

Skills are located in [skills/](skills/) and map to the following commands:

- `/git:commit` - Safe staging and conventional commit creation.
- `/git:branch-create` - Creates a new branch branched off the latest `origin/<default>`.
- `/git:branch-delete` - Deletes a local and/or remote branch securely.
- `/git:tag-create` - Creates and pushes annotated tags.
- `/git:fetch` - Fetches from remote origins.
- `/git:pull` - Fast-forward pulls or rebases local branch.
- `/git:push` - Pushes current branch (sets upstream on first push).
- `/git:stash` - Safe stash operations (push, pop, list, drop).
- `/git:status` - Displays working-tree status and recent commits.
- `/git:rebase` - Interactive-style rebase onto target branches.
- `/git:switch` - Switches branch checkout after fetching remote updates.
