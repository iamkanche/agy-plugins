---
name: sdd-sync
description: Sync development logs and documents to domain-level product directories, merging changes into domain docs instead of creating ephemeral slug folders.
model: flash
---

# /kanche:sdd-sync

**Summary.** Promote the final feature documentation from the temporary development folder `.docs/development/{slug}/` into the permanent domain-level product directories (`.docs/product/{domain}/` e.g. `design/`, `git/`, `gh-cli/`, `sdd/`, `dev/`, `planner/`, `qa/`, `scrum/`), merging changes into existing domain docs rather than creating ephemeral feature slug folders. State every action before executing it.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description under `.docs/development/` (e.g. `improve-sdd-plugins` or `login`). If omitted, pick the feature folder under `.docs/development/`. If ambiguous or empty, ask the user.
- **domain** (optional, flag `--domain=<domain>`) — explicitly specify the target domain group folder (`design`, `git`, `gh-cli`, `sdd`, `dev`, `planner`, `qa`, `scrum`). If omitted, infer from the modified skills or files.

## Steps

### 1. Collect Documents

Locate the target development folder:
- Source path: `.docs/development/{slug}/` (e.g. `.docs/development/improve-sdd-plugins/`).
- Confirm it exists and contains documentation (`specs.md`, `design.md`, `tasks.md`). If not, STOP and report.

### 2. Identify Target Domain Group(s)

Identify the domain group directory under `.docs/product/`:
- Map modified skills or code paths to their domain group (`design`, `git`, `gh-cli`, `sdd`, `dev`, `planner`, `qa`, `scrum`).
- Target directory path: `.docs/product/{domain}/` (e.g., `.docs/product/design/` or `.docs/product/sdd/`). Do NOT create ephemeral feature slug folders (such as `.docs/product/{slug}/`).

### 3. Promote & Merge to Product Domain Docs

Sync and merge final documentation into the permanent domain directory:
- Destination path: `.docs/product/{domain}/`
- Create the domain directory if it does not exist:
  ```bash
  mkdir -p .docs/product/{domain}
  ```
- **Merge Content into Domain Docs:**
  - Merge requirements and capabilities from `.docs/development/{slug}/specs.md` into `.docs/product/{domain}/specs.md`.
  - Merge design choices and architecture from `.docs/development/{slug}/design.md` into `.docs/product/{domain}/design.md`.
  - If additional domain groups were impacted, update each corresponding `.docs/product/{domain}/` documentation set accordingly.

### 4. Cleanup Development Folder

Delete the development feature directory to prevent drift and keep the workspace clean:
- Command:
  ```bash
  rm -rf .docs/development/{slug}/
  ```

### 5. Commit and Push

Create a conventional commit detailing the domain sync and cleanup using **/kanche:git-commit**:
- Stage the updated domain product files and the deleted development directory.
- Run **/kanche:git-commit** using multi-line HEREDOC format:

```bash
git commit -F - <<'EOF'
docs(sync): merge {slug} into {domain} domain docs and cleanup dev folder

## Overview
Promote development documentation from .docs/development/{slug}/ into permanent domain product directory .docs/product/{domain}/ and clean up ephemeral dev folder.

## Changes
- Consolidated specs and design documents into .docs/product/{domain}/.
- Cleaned up development folder .docs/development/{slug}/.

## Impact
Maintains long-term project memory integrity without ephemeral feature slug accumulation.
EOF
```

- Run **/kanche:git-push** to update remote (as an isolated subsequent step).

---

# doc-synchronizer (drift detection)

This skill also provides guidelines for detecting drift between docs and code during PR reviews or development checkpoints.

## Drift Detection Mission

Detect drift — between the feature docs and each other, and between the docs and the as-built code — and return a drift report plus concrete proposed edits.

### Read

- Feature docs: `.docs/development/{slug}/{specs,design,tasks,api-diff,db-diff}.md`.
- Consolidated domain docs: `.docs/product/{domain}/*`.
- Guidelines: `.docs/guidelines/{tech,structure,rules}.md`.
- As-built code: use read-only git to check actual endpoints, schema, and behavior against what the docs claim.

### Produce Drift Report

Return a **drift report** (chat data) with:
1. **Drift findings** — discrepancy entries detailing what the doc says vs. what is true in code/docs.
2. **Proposed edits** — precise, ready-to-apply changes to fix the drift (prefer editing docs to match code unless the code is wrong).
