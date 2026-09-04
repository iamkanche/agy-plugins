---
name: git-stash
description: Save, restore, list, or discard uncommitted changes with git stash. Shows working-tree state before and after.
model: flash
---

# /kanche:git-stash

**Summary.** Save, restore, list, or discard uncommitted changes with `git stash`, showing the working-tree state before and after so the user sees what moved. The workflow delegates all local stash actions (push, pop, list, drop) to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- Subcommand (positional, optional): `push` (default), `pop`, `list`, `drop`.
- `--message=<msg>` — label for `push` (`git stash push -m <msg>`).

If no subcommand is given, default to `push`.

## Steps

1. **Confirm this is a git repo.** If `git status` errors, STOP.

2. **Show state before.**

   ```bash
   git status --short
   git stash list
   ```

3. **Dispatch the subcommand:**

   - **`push` (default)** — stash current changes. If the working tree is clean, report "nothing to stash" and stop.

     ```bash
     git stash push -m "<msg>"   # -m omitted if no --message
     ```

   - **`pop`** — restore (and remove) the most recent stash. If it conflicts on apply, STOP and report the conflicting files; do not force-resolve. Do not `drop` on conflict.

     ```bash
     git stash pop
     ```

   - **`list`** — enumerate stashes and stop (read-only).

     ```bash
     git stash list
     ```

   - **`drop`** — discard a stash. This is destructive and irreversible. You MUST STOP and ask the human for explicit confirmation before running drop:
     - Show the specific stash reference (e.g. `stash@{0}`) and the stash message.
     - Prompt the user using `default_api:ask_question` with options `(Recommended) Yes, drop stash` and `No, keep stash`.
     - Only on selecting Yes, run:
       ```bash
       git stash drop "stash@{<n>}"
       ```
     - Never run `git stash clear`.

4. **Show state after** so the user sees what moved.

   ```bash
   git status --short
   git stash list
   ```

## git hard rules

Never drop a stash autonomously without explicit human confirmation · never `reset --hard` · never `git stash clear` (bulk-discard) · never force-resolve `pop` conflicts · never drop more than the user named. Follow `plugins/kanche/rules/destructive-safety.md`.

## Done when

- The requested stash operation ran (or a clean "nothing to stash" was reported).
- Working-tree and stash-list state are shown before and after.
- `pop` conflicts, if any, are reported and left for the user (no force-resolve, stash kept).
