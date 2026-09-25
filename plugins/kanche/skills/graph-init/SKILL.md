---
name: graph-init
description: Bootstrap the graph-grounded steering guidelines (product.md, tech.md, structure.md, rules.md) for this repository.
model: flash
---

# /kanche:graph-init

**Summary.** Analyze this repository using Knowledge Graph extraction and write the four steering docs under `.docs/guidelines/`, applying the **graph-steering** skill for graph-grounded analysis and drafting.

This workflow runs in the main conversation context. The graph-steering skill returns document data; this workflow owns all writes to disk.

## Inputs

This workflow takes no arguments. It operates on the current repository.

## Steps

1. **Preconditions.** Confirm we are in a git repo and detect the default branch:
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "NOT_A_GIT_REPO"; exit 1; }
   DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
   DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
   DEFAULT=${DEFAULT:-main}
   echo "default_branch=$DEFAULT"
   ```
   If not a git repo, STOP and report.

2. **Idempotency check.** If `.docs/guidelines/` already exists with any of `product.md`, `tech.md`, `structure.md`, `rules.md`, STOP and tell the user to run `/kanche:graph-init-update` instead.

3. **Survey the repo structure**:
   ```bash
   git ls-files | head -400
   git ls-files | sed -n 's@.*\.@@p' | sort | uniq -c | sort -rn | head -30
   ```
   Read top-level `README*`, manifests (`package.json`, `go.mod`, `pyproject.toml`, etc.), and directory layout.

4. **Apply the graph-steering skill** (`skills/graph-steering/SKILL.md`): give it the survey as context. Ask it to return the full content of all four docs — `product.md`, `tech.md`, `structure.md`, `rules.md` — grounded in files and graph entities.

5. **Persist.** Create directory and write each returned document:
   ```bash
   mkdir -p .docs/guidelines
   ```
   Write `.docs/guidelines/{product,tech,structure,rules}.md`.

6. **Report.** Print the four written paths and summary of captured product, tech stack, and graph structure boundaries.
