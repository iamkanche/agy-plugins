---
name: graph-sync
description: Sync development documents to domain-level product directories and update the repository Knowledge Graph.
model: flash
---

# /kanche:graph-sync

**Summary.** Promote final feature documentation from the temporary development folder `.docs/development/{slug}/` into the permanent domain-level product directories (`.docs/product/{domain}/`), trigger incremental Knowledge Graph update (`graphify --update` when available), and prompt for cleanup of ephemeral dev folders. State every action before executing it.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description under `.docs/development/` (e.g. `auth-oauth2`). If omitted, pick the feature folder under `.docs/development/`.
- **domain** (optional, flag `--domain=<domain>`) — explicitly specify the target domain group folder (`graph`, `design`, `git`, `gh-cli`, `dev`, `planner`, `qa`, `scrum`). If omitted, infer from the modified skills or files.

## Steps

### 1. Collect Documents & Graph State

Locate the target development folder:
- Source path: `.docs/development/{slug}/`
- Confirm it exists and contains documentation (`specs.md`, `design.md`, `tasks.md`). If not, STOP and report.

### 2. Identify Target Domain Group(s)

Identify the domain group directory under `.docs/product/`:
- Map modified skills or code paths to their domain group (`graph`, `design`, `git`, `gh-cli`, `dev`, `planner`, `qa`, `scrum`).
- Target directory path: `.docs/product/{domain}/`. Do NOT create ephemeral feature slug folders (such as `.docs/product/{slug}/`).

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

### 4. Incremental Knowledge Graph Synchronization

If `graphify-out/` or `graphify` is installed, update the codebase knowledge graph incrementally to reflect newly added or modified entities:
```bash
if [ -d "graphify-out" ] && command -v graphify >/dev/null 2>&1; then
    graphify --update
    echo "Knowledge graph updated."
fi
```

### 5. Cleanup Development Folder (Human-Gated)

Deleting the development feature directory is a destructive action (`rm -rf`). In accordance with `plugins/kanche/rules/destructive-safety.md`, you MUST STOP and prompt the human for explicit confirmation before deleting:
- Prompt via `default_api:ask_question` asking: "Approve deleting ephemeral development directory `.docs/development/{slug}/` after syncing into `.docs/product/{domain}/`?" with options `(Recommended) Yes, delete development folder` and `No, keep development folder`.
- Only upon selecting Yes, execute the cleanup:
  ```bash
  rm -rf ".docs/development/${slug}/"
  ```
- If the user selects No, keep the folder and proceed to commit product domain updates.

### 6. Commit and Push (Human-Gated)

Create a conventional commit detailing the domain sync using **/kanche:git-commit**:
- Stage updated domain product files, graph artifacts, and deleted development directory if approved.
- Run **/kanche:git-commit** (which prompts human for confirmation):

```bash
git commit -F - <<'EOF'
docs({domain}): promote feature docs and sync knowledge graph

## Overview
Promote development documentation from .docs/development/{slug}/ into permanent domain product directory .docs/product/{domain}/ and update repository knowledge graph.

## Changes
- Consolidated specs and design documents into .docs/product/{domain}/.
- Synchronized codebase knowledge graph entities.
- Cleaned up ephemeral dev folder.

## Impact
Preserves long-term project memory and maintains accurate graph topology.
EOF
```

- Run **/kanche:git-push** to update remote (prompts human for confirmation). Never push autonomously.
