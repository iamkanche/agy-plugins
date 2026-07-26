# Architecture & Technical Design: SDD Phase Model Update

## 1. Component Boundaries & Layout Specification
- **Level 1 (AI + Subagents)**: Covers setup (P0), specs (P1), design (P2), tasks (P3), build (P4), validation (P5), and deploy & AI PR review (P6).
- **Level 2 (AI + Human, auto/gated)**: Covers human review/checklist (P7), PR modifications & polling (P8), and product alignment/merge (P9).
- Placement: Level 2 is placed vertically underneath Level 1.

## 2. Review Integration Architecture
- P1 Specs: `/kanche:design-grill` (cycle 1) → `/kanche:design-specs` → FORCED `/kanche:design-specs-review` (≤3x loop)
- P2 Design: `/kanche:design-init` → FORCED `/kanche:design-review` (≤3x loop)
- P3 Tasks: `/kanche:planner-tasks` → FORCED `/kanche:planner-review` (≤3x loop)
- P4 Build: `/kanche:dev-implement` → FORCED `/kanche:qa-review` (≤3x loop)
- P5 Validation: `/kanche:qa-validate` & fix (≤3x loop)
- P6 Deploy & AI PR Review: `/kanche:git-push` → `/kanche:pr-create` → FORCED `/kanche:gh-cli-pr-review` (AI PR Review)

## 3. Review Verdict & Criteria
- Verdict: GO
- Findings: None
