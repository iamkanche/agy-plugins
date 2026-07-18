---
name: tag-create
description: Create an annotated tag at HEAD and push it to origin remote, gated behind explicit confirmation.
---

# /git:tag-create

**Summary.** Create an annotated tag at HEAD and push it to origin, gated behind explicit confirmation. The workflow delegates local Git tag creations and pushes to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<tag>` (positional, required) — the tag name (e.g. `v1.4.0`). If missing, ask the user (do not invent one).
- `--message=<msg>` — annotation message. If omitted, ask the user for one (annotated tags require a message).

## Steps

1. **Confirm this is a git repo.** If `git rev-parse --is-inside-work-tree` fails, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Verify the target commit** and that the tag does not already exist.

   ```bash
   TAG="<tag>"
   git rev-parse HEAD
   git rev-parse -q --verify "refs/tags/$TAG" && echo "TAG EXISTS" || echo "free"
   ```

   If the tag already exists, STOP (never overwrite/move an existing tag here).

3. **Gate — STOP.** Ask the user to confirm creating and pushing annotated tag `<tag>` at `<HEAD short sha / subject>`. Show the tag name, the target commit, and the message. Proceed only on an explicit yes; on no, STOP.

4. **Create the annotated tag and push it.** Never force, never overwrite.

   ```bash
   git tag -a "$TAG" -m "<message>"
   git push origin "$TAG"
   ```

5. **Report** the pushed tag.

## git hard rules

Never force-push · never overwrite or move an existing tag · never `--no-verify` · never `reset --hard`.

## Done when

- An annotated tag `<tag>` exists at HEAD and is pushed to origin, confirmed via the tag gate.
- No existing tag was overwritten and no force flag was used.
