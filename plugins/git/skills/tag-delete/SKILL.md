---
name: tag-delete
description: Delete a local and/or remote tag securely, gated by explicit confirmation.
---

# /git:tag-delete

**Summary.** Delete a git tag locally and/or on origin remote, gated by explicit confirmation. The workflow delegates local and remote tag deletions to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<tag-name>` (positional, required) — the name of the tag to delete.
- `--remote` — also delete the tag on origin remote.

If `<tag-name>` is missing, ask the user (do not invent one).

## Steps

1. **Confirm this is a git repo.** If `git status` errors, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Verify tag existence.** Check if the tag exists locally and/or remotely before deleting.

   ```bash
   TAG="<tag-name>"
   git rev-parse --verify --quiet "refs/tags/$TAG" && echo "local exists" || echo "no local"
   git ls-remote --tags origin "refs/tags/$TAG" | grep -q "$TAG" && echo "remote exists" || echo "no remote"
   ```

3. **Gate — STOP.** Ask the user to confirm deleting tag `<tag>` locally (and if `--remote` is passed, on origin). Proceed only on an explicit yes; on no, STOP.

4. **Delete locally.** Run the deletion command.

   ```bash
   git tag -d "$TAG"
   ```

5. **Delete remotely** (only if `--remote` was requested and confirmed).

   ```bash
   git push origin --delete "$TAG"
   ```

6. **Report** deletion status.

## git hard rules

All deletions must be explicitly confirmed by the user. Never use `--force` or modify tags without authorization.

## Done when

- The specified tag is deleted locally.
- If `--remote` was passed, the tag is deleted on origin.
- The action was explicitly confirmed via the gate.
