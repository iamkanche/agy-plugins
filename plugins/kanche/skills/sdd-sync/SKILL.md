---
name: sdd-sync
description: Sync development logs and documents to the repository-wide product directory, cleaning up feature files.
---

# /kanche:sdd-sync

**Summary.** Promote the final feature documentation from the temporary development folder `docs/development/{slug}/` to the permanent product directory `docs/product/plugins/kanche/{slug}/`, then delete the development folder. State every action before executing it.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description (e.g. `improve-sdd-plugins` or `login`). If omitted, pick the feature folder under `docs/development/`. If ambiguous or empty, ask the user.

## Steps

### 1. Collect Documents

Locate the target development folder:
- Source path: `docs/development/{slug}/` (e.g. `docs/development/improve-sdd-plugins/`).
- Confirm it exists and contains documentation (`specs.md`, `design.md`, `tasks.md`). If not, STOP and report.

### 2. Promote to Product

Sync the final files to the permanent product feature directory:
- Destination path: `docs/product/plugins/kanche/{slug}/` (e.g. `docs/product/plugins/kanche/improve-sdd-plugins/`).
- Create the destination directory if it does not exist:
  ```bash
  mkdir -p docs/product/plugins/kanche/{slug}
  ```
- Copy the final documentation files:
  - `docs/development/{slug}/specs.md` -> `docs/product/plugins/kanche/{slug}/specs.md`
  - `docs/development/{slug}/design.md` -> `docs/product/plugins/kanche/{slug}/design.md`
  - `docs/development/{slug}/notes.md` -> `docs/product/plugins/kanche/{slug}/notes.md` (if present)
- Keep other relevant files if appropriate (e.g. openapi or database diffs), merging or copying them into `docs/product/plugins/kanche/{slug}/` or repository-wide product directories.

### 3. Cleanup Development Folder

Delete the development feature directory to prevent drift and keep the workspace clean:
- Command:
  ```bash
  rm -rf docs/development/{slug}/
  ```

### 4. Commit and Push

Create a conventional commit detailing the synchronization and cleanup:
- Stage the new/updated product files and the deleted development directory.
- Run **/kanche:git-commit** with a conventional message (e.g., `docs: sync {slug} to product and clean up dev folder`).
- Run **/kanche:git-push** to update remote.

---

# doc-synchronizer (drift detection)

This skill also provides guidelines for detecting drift between docs and code during PR reviews or development checkpoints.

## Drift Detection Mission

Detect drift — between the feature docs and each other, and between the docs and the as-built code — and return a drift report plus concrete proposed edits.

### Read

- Feature docs: `docs/development/{slug}/{specs,design,tasks,api-diff,db-diff}.md`.
- Consolidated docs: `docs/product/plugins/kanche/{slug}/*`.
- Guidelines: `docs/guidelines/{tech,structure,rules}.md`.
- As-built code: use read-only git to check actual endpoints, schema, and behavior against what the docs claim.

### Produce Drift Report

Return a **drift report** (chat data) with:
1. **Drift findings** — discrepancy entries detailing what the doc says vs. what is true in code/docs.
2. **Proposed edits** — precise, ready-to-apply changes to fix the drift (prefer editing docs to match code unless the code is wrong).
