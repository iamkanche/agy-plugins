---
name: git-tag-push
description: Push local tags to the remote origin, gated behind explicit confirmation.
model: flash
---

# /kanche:git-tag-push

**Summary.** Push a specific local tag or all local tags to the remote origin, gated behind explicit confirmation. The workflow delegates pushing tags to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<tag-name>` (positional, optional) — the specific local tag to push. If omitted, all local tags are pushed (`--all`).
- `--all` — push all local tags (equivalent to `git push origin --tags`).

## Steps

1. **Confirm this is a git repo.** If `git status` errors, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Verify tag(s) exist.**
   - If `<tag-name>` is specified, verify it exists locally.
     ```bash
     TAG="<tag-name>"
     git rev-parse --verify --quiet "refs/tags/$TAG" && echo "exists" || echo "missing"
     ```
     If the specific tag is missing locally, STOP.
   - If pushing all, check if there are any local tags.
     ```bash
     git tag | grep -q . && echo "has tags" || echo "no tags"
     ```

3. **Gate — STOP.** Ask the user to confirm pushing the tag(s). Show the tag name(s) and destination using the interactive `default_api:ask_question` tool with options `(Recommended) Yes, proceed with push` and `No, abort`. Proceed only on selecting Yes; on No, STOP.

4. **Push tag(s).**
   - If specific `<tag-name>`:
     ```bash
     git push origin "$TAG"
     ```
   - If pushing all:
     ```bash
     git push origin --tags
     ```

5. **Report** push status.

## git hard rules

Never force-push tags · never overwrite or move remote tags.

## Done when

- The specified tag or all local tags are successfully pushed to origin.
- The action was explicitly confirmed via the gate.
