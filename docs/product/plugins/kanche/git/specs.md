---
feature: git
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-19
---

# Git Plugin — Consolidated Specification

<!-- schema: specs | written by /kanche:sdd-sync (dev-only sections stripped) -->

## Context
Google Antigravity utilizes the `git` plugin to manage local repository branch lifecycles, stash operations, committing, and tagging.

## Capabilities
- `/kanche:git-commit` - Safe staging and conventional commit creation.
- `/kanche:git-branch-create` - Creates a new branch branched off the latest remote default branch.
- `/kanche:git-branch-delete` - Deletes a local and/or remote branch securely.
- `/kanche:git-tag-create` - Creates and pushes annotated tags.
- `/kanche:git-tag-delete` - Delete local and/or remote tag.
- `/kanche:git-tag-push` - Push local tags to remote origin.
- `/kanche:git-fetch` - Fetches from remote origins.
- `/kanche:git-pull` - Fast-forward pulls or rebases local branch.
- `/kanche:git-push` - Pushes current branch.
- `/kanche:git-stash` - Safe stash operations (push, pop, list, drop).
- `/kanche:git-status` - Displays working-tree status.
- `/kanche:git-rebase` - Interactive-style rebase onto target branches.
- `/kanche:git-switch` - Switches branch checkout.

## Acceptance criteria (as-built)
1. `/kanche:git-tag-delete` deletes the specified tag locally, and on remote origin if `--remote` is passed.
2. `/kanche:git-tag-push` pushes local tags to origin remote.
3. Gated Git commands (commit, push, branch-create, branch-delete, tag-create, tag-delete, tag-push, fetch, pull, stash, status, rebase, switch) use the interactive `default_api:ask_question` tool for confirmations.
