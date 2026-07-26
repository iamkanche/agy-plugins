# System Design: Full AI SDD Workflow & Level 2 Reorganization

## 1. Phase Architecture

```
LEVEL 1 (Full AI + Subagents)
P0 setup   Receipt → /kanche:git-branch-create
P1 specs   /kanche:design-grill → /kanche:design-specs → FORCED /kanche:design-specs-review (Analyst, ≤3x loop)
P2 design  /kanche:design-init → FORCED /kanche:design-review (Architect, ≤3x loop)
P3 tasks   /kanche:planner-tasks → FORCED /kanche:planner-review → Docs Commit (Planner, ≤3x loop)
P4 build   /kanche:dev-implement → FORCED /kanche:qa-review → Code Commit (Coder, ≤3x loop)
P5 valid.  /kanche:qa-validate & fix (Validator, ≤3x loop)
P6 deploy  /kanche:git-push → /kanche:pr-create → FORCED /kanche:gh-cli-pr-review (AI PR Review)

LEVEL 2 (Full AI Automation + Human Merge)
P8 PR mods       /kanche:pr-respond & poll (≤3x loop)
P9 alignment     /kanche:sdd-sync (Promote dev docs → product docs & push feature branch)
P7 human review  Human Review & Manual PR Merge
```

## 2. Structural Component Changes

### 2.1 `sdd-run` Skill
- Phase model updated to show Level 2 as P8 -> P9 -> P7.
- P8 handles PR comments triaging and auto-fixes.
- P9 runs `/kanche:sdd-sync` to promote documentation to `docs/product/plugins/kanche/{domain}/` and remove `docs/development/{slug}/`, committing and pushing to the feature branch.
- P7 asks the user to review and merge the pull request.

### 2.2 `sdd-continue` Skill
- Update detection logic:
  - If PR is open and review comments exist -> P8.
  - If PR is open, no unresolved comments, but dev folder exists -> P9 (`sdd-sync`).
  - If `sdd-sync` completed and PR is ready -> P7 (Human Review & Merge).

### 2.3 `index.html` & `docs/product/plugins/kanche/sdd/*`
- Update UI cards and sdd domain docs to reflect P8 (PR Mods), P9 (Doc Sync), P7 (Human Review & Merge).
