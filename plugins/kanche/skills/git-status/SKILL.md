---
name: git-status
description: Show the working-tree state, current branch ahead/behind, and recent commits. Read-only.
---

# /kanche:git-status

**Summary.** Show the working-tree state, current branch (with ahead/behind), and recent commits — all read-only. The workflow delegates local status and history reads to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

No arguments.

## Steps

1. **Confirm this is a git repo.** If `git status` errors with "not a git repository", STOP and tell the user.

2. **Show working tree + branch + ahead/behind.**

   ```bash
   git status --short --branch
   git branch --show-current
   ```

3. **Show recent commits.**

   ```bash
   git log --oneline -5
   ```

4. **Present a compact at-a-glance summary**: branch, dirty/clean, ahead/behind counts, and last few commits.

## Done when

- Working-tree state, current branch, ahead/behind, and recent commits are shown.
- Nothing was modified (read-only).
