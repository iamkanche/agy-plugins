---
name: git-fetch
description: Fetch branches and tags from origin, updating remote-tracking branches. Read-only to working-tree.
---

# /git:fetch

**Summary.** Fetch branches and tags from one or more other repositories, updating remote-tracking branches. Read-only to working-tree and local history. The workflow delegates all remote fetch operations to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `--all` — fetch from all remotes.
- `--prune` — before fetching, remove any remote-tracking references that no longer exist on the remote.

No positional argument is required.

## Steps

1. **Confirm this is a git repo.** If `git rev-parse --is-inside-work-tree` fails, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Fetch.** Run the fetch command with parsed options.
   - If `--all` was passed, add `--all` flag.
   - If `--prune` was passed (or default to true), add `--prune` flag.

   ```bash
   # Default:
   git fetch --prune

   # With --all:
   git fetch --all --prune
   ```

3. **Report** the fetched changes, tags, and branches.

   ```bash
   git status --short --branch
   ```

## git hard rules

Read-only to the working tree and local branch history. Never force-push · never use `--no-verify`.

## Done when

- References have been fetched from the remote(s) with options applied correctly.
- The outcome (updated branches, new tags, etc.) is reported back to the user.
