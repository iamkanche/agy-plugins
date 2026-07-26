# SDD Workflows Design

## 1. System Architecture
The SDD workflow family provides structured phase progression (P0-P9):
- P0: Feature Initiation & Steering Alignment
- P1: Functional Specification (`specs.md`)
- P2: Technical Design & Architecture (`design.md`)
- P3: Task Breakdown & Manifest (`tasks.md`)
- P4: Implementation & Verification (`dev-implement`)
- P5-P6: AI Validation & Deployment (`qa-validate`, `git-push`, `pr-create`, `gh-cli-pr-review`)
- P8: PR Modifications & Polling (`pr-respond`)
- P9: Documentation Promotion (`sdd-sync`)
- P7: Human Review & Manual PR Merge

## 2. File Organization
- Steering Guidelines: `docs/guidelines/{product,tech,structure,rules}.md`
- Active Development: `docs/development/{slug}/`
- Consolidated Product Knowledge: `docs/product/plugins/kanche/{group}/`
