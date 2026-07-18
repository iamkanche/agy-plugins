---
feature: git
module: plugins
integrated_at: 2026-07-18
updated_at: 2026-07-18
---

# Git Plugin — Consolidated Specification

<!-- schema: specs | written by /sdd:sync-product (dev-only sections stripped) -->

## Context
Google Antigravity utilizes the `git` plugin to manage local repository branch lifecycles, stash operations, committing, and tagging.

## Capabilities
- `/git:commit` - Safe staging and conventional commit creation.
- `/git:branch-create` - Creates a new branch branched off the latest remote default branch.
- `/git:branch-delete` - Deletes a local and/or remote branch securely.
- `/git:tag-create` - Creates and pushes annotated tags.
- `/git:tag-delete` - Delete local and/or remote tag.
- `/git:tag-push` - Push local tags to remote origin.
- `/git:fetch` - Fetches from remote origins.
- `/git:pull` - Fast-forward pulls or rebases local branch.
- `/git:push` - Pushes current branch.
- `/git:stash` - Safe stash operations (push, pop, list, drop).
- `/git:status` - Displays working-tree status.
- `/git:rebase` - Interactive-style rebase onto target branches.
- `/git:switch` - Switches branch checkout.

## Acceptance criteria (as-built)
1. `/git:tag-delete` deletes the specified tag locally, and on remote origin if `--remote` is passed.
2. `/git:tag-push` pushes local tags to origin remote.
