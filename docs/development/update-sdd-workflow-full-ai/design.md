# System Design: SDD Workflow Architecture (P0-P7 Level 1 AI, P8-P9 Level 2 Human)

## 1. Phase Architecture

```
LEVEL 1 (AI: P0 - P7)
P0 setup   Receipt → /kanche:git-branch-create
P1 specs   /kanche:design-grill → loop ≤3x (/kanche:design-specs → /kanche:design-specs-review)
P2 design  loop ≤3x (/kanche:design-init → /kanche:design-review)
P3 tasks   loop ≤3x (/kanche:planner-tasks → /kanche:planner-review) → Docs Commit
P4 build   loop ≤3x (/kanche:dev-implement → /kanche:qa-review) → Implementation Commit
P5 valid.  /kanche:qa-validate & fix (≤3x loop)
P6 deploy  /kanche:git-push → /kanche:gh-cli-pr-create → loop ≤3x (/kanche:gh-cli-pr-review → /kanche:gh-cli-pr-respond → /kanche:git-commit → /kanche:git-push)
P7 align   /kanche:sdd-sync (Promote dev docs → product docs, commit & push)

LEVEL 2 (Human: P8 - P9)
P8 human review  gated human-review /kanche:qa-validate (show verification checklist)
P9 PR merge      /kanche:gh-cli-pr-merge (user merges PR)
```

## 2. Structural Component Mapping

### 2.1 `sdd-run` & `sdd-continue` Skills
- Level 1 AI automates P0 through P7 straight through in auto mode.
- P6 deploys, creates PR, and loops up to 3x reviewing, fixing, committing, and pushing PR updates.
- P7 runs `/kanche:sdd-sync` to consolidate dev docs into permanent domain directories under `docs/product/plugins/kanche/{domain}/`.
- Level 2 Human gates execution at P8 (gated human review checklist) and P9 (`gh-cli-pr-merge`).

### 2.2 `index.html` Pipeline Visualization
- Pipeline map updated to render 10 distinct phases (P0-P9) grouped into LEVEL 1 AI (P0-P7) and LEVEL 2 Human (P8-P9).
