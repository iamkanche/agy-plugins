# SDD Workflows Design

## 1. System Architecture
The SDD workflow family provides structured phase progression (P0-P9):
- P0: Feature Initiation & Steering Alignment
- P1: Functional Specification (`specs.md`)
- P2: Technical Design & Architecture (`design.md`)
- P3: Task Breakdown & Manifest (`tasks.md`)
- P4: Implementation & Verification (`code-implement`)
- P5: AI Validation (`qa-validate` & fix loop)
- P6: Deploy & AI PR Review/Respond Loop (`git-push` → `gh-cli-pr-create` → ≤3x loop `gh-cli-pr-review` → `gh-cli-pr-respond` → `git-commit` → `git-push`)
- P7: Documentation Promotion & Sync (`sdd-sync`)
- P8: Gated Human Review Checklist (`qa-validate`)
- P9: PR Merge (`gh-cli-pr-merge`)

## 2. File Organization
- Steering Guidelines: `.docs/guidelines/{product,tech,structure,rules}.md`
- Active Development: `.docs/development/{slug}/`
- Consolidated Product Knowledge: `.docs/product/{group}/`
