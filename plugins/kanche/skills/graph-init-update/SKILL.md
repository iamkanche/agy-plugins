---
name: graph-init-update
description: Re-analyze this repository using Knowledge Graph extraction and refresh guidelines merging new findings.
model: flash
---

# /kanche:graph-init-update

**Summary.** Re-analyze this repository using Knowledge Graph extraction and refresh the four steering docs under `.docs/guidelines/`, **merging** new graph findings into the existing docs rather than overwriting them. Applies the **graph-steering** skill for graph-grounded analysis and merge drafting.

This workflow runs in the main conversation context. The graph-steering skill only returns document data; this workflow owns all writes to disk.

## Inputs

This workflow takes no arguments. It operates on the current repository.

## Steps

1. **Preconditions.** Confirm we are in a git repo and detect the default branch:
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "NOT_A_GIT_REPO"; exit 1; }
   DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
   DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
   DEFAULT=${DEFAULT:-main}
   ```
   If not a git repo, STOP.

2. **Require existing guidelines.** If `.docs/guidelines/` does not exist (or has none of the four docs), STOP and tell the user to run `/kanche:graph-init` first. Read existing `product.md`, `tech.md`, `structure.md`, `rules.md` to pass as the base to merge into.

3. **Survey the repo structure**:
   ```bash
   git ls-files | head -400
   git ls-files | sed -n 's@.*\.@@p' | sort | uniq -c | sort -rn | head -30
   ```
   Read top-level `README*`, manifests, and directory layout.

4. **Apply the graph-steering skill** (`skills/graph-steering/SKILL.md`) in **merge mode**: give it both existing docs and the fresh graph survey. Ask it to update the steering guidelines, preserving hand-tuned rules (`rules.md`), adding newly identified entities or community clusters, and correcting drifted commands.

5. **Persist (merge).** Write each returned doc back to `.docs/guidelines/{product,tech,structure,rules}.md`. Never discard hand-tuned sections.

6. **Report.** Print changed paths and a per-doc changelog.
