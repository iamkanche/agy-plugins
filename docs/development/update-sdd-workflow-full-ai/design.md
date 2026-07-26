# System Design: Full AI SDD Workflow & Level 2 Reorganization (P9 -> P7 -> P8)

## 1. Phase Architecture

```
LEVEL 1 (Full AI + Subagents)
P0 setup   Receipt → /kanche:git-branch-create
P1 specs   /kanche:design-grill → /kanche:design-specs → FORCED /kanche:design-specs-review (Analyst, ≤3x loop)
P2 design  /kanche:design-init → FORCED /kanche:design-review (Architect, ≤3x loop)
P3 tasks   /kanche:planner-tasks → FORCED /kanche:planner-review → Docs Commit (Planner, ≤3x loop)
P4 build   /kanche:dev-implement → FORCED /kanche:qa-review → Code Commit (Coder, ≤3x loop)
P5 valid.  /kanche:qa-validate & fix (Validator, ≤3x loop)
P6 deploy  /kanche:git-push → /kanche:gh-cli-pr-create → loop ≤3x (/kanche:gh-cli-pr-review → /kanche:gh-cli-pr-respond)

LEVEL 2 (Full AI Automation + Human Merge)
P9 alignment     /kanche:sdd-sync (Promote dev docs → product docs & push feature branch)
P7 human review  /kanche:qa-validate (Human review & verification checklist)
P8 PR merge      User merges the PR (or /kanche:gh-cli-pr-merge by user)
```

## 2. Structural Component Changes

### 2.1 `sdd-run` Skill
- Update Phase Model to show Level 1 P6 with 3x review-respond loop.
- Level 2 updated to P9 -> P7 -> P8:
  - P9 runs `/kanche:sdd-sync` to promote documentation to `docs/product/plugins/kanche/{domain}/` and remove `docs/development/{slug}/`, committing and pushing to the feature branch.
  - P7 runs human review and verification checklist (`/kanche:qa-validate`).
  - P8 hands over PR merge to the user.

### 2.2 `sdd-continue` Skill
- Update detection logic:
  - If PR is open and dev folder exists -> P9 (`sdd-sync`).
  - If `sdd-sync` completed and PR is ready -> P7 (Human review & checklist).
  - If human review passed -> P8 (User PR merge).

### 2.3 `index.html` & `docs/product/plugins/kanche/sdd/*`
- Update UI cards and sdd domain docs to reflect P6 (Deploy & PR Review/Respond Loop), P9 (Doc Sync), P7 (Human Review), and P8 (User PR Merge).
