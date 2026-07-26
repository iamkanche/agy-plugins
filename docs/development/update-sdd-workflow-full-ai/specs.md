# Specification: SDD Workflow Architecture (P0-P7 Level 1 AI, P8-P9 Level 2 Human)

## 1. Executive Summary
This specification defines the 10-phase SDD workflow (`/kanche:sdd-run` and `/kanche:sdd-continue`) partitioned cleanly into LEVEL 1 AI Automation (P0-P7) and LEVEL 2 Human Review & Deployment (P8-P9).

## 2. Phase Workflow Definitions

### 2.1 LEVEL 1 AI Automation (P0 – P7)
- **P0 Setup**: Feature receipt generation & branch checkout (`/kanche:git-branch-create`).
- **P1 Specs**: `/kanche:design-grill` → loop ≤3x (`/kanche:design-specs` → `/kanche:design-specs-review`).
- **P2 Design**: loop ≤3x (`/kanche:design-init` → `/kanche:design-review`).
- **P3 Tasks**: loop ≤3x (`/kanche:planner-tasks` → `/kanche:planner-review`) → Docs Commit (`/kanche:git-commit`).
- **P4 Build**: loop ≤3x (`/kanche:dev-implement` → `/kanche:qa-review`) → Implementation Commit (`/kanche:git-commit`).
- **P5 Validation**: `/kanche:qa-validate` & fix (≤3x loop).
- **P6 Deploy & PR Review/Respond**: `/kanche:git-push` → `/kanche:gh-cli-pr-create` → loop ≤3x (`/kanche:gh-cli-pr-review` → `/kanche:gh-cli-pr-respond` → `/kanche:git-commit` → `/kanche:git-push`).
- **P7 Product Alignment**: `/kanche:sdd-sync` (Promote feature dev docs → domain product directories, remove dev folder, commit & push to origin feature branch).

### 2.2 LEVEL 2 Human Review & Deployment (P8 – P9)
- **P8 Gated Human Review**: Interactive review checklist (`/kanche:qa-validate`) presented to the user displaying test outcomes, lint validations, and checklist verification.
- **P9 PR Merge**: PR merge execution (`/kanche:gh-cli-pr-merge`) upon human confirmation.

## 3. Acceptance Criteria
1. LEVEL 1 AI executes P0 through P7 autonomously straight through.
2. P6 executes a 3x PR review-respond loop that commits and pushes fixes.
3. P7 executes `/kanche:sdd-sync` to promote product docs and clean up dev folders before Level 2.
4. LEVEL 2 begins at P8 with interactive human review checklist, followed by P9 PR merge.
