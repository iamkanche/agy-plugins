# Specification: Full AI SDD Workflow & Level 2 Reorganization (P9 -> P7 -> P8)

## 1. Executive Summary
This specification updates the SDD workflow (`/kanche:sdd-run` and `/kanche:sdd-continue`) to operate as a Full AI workflow where Level 1 and Level 2 AI automation execute end-to-end. Phase P6 is updated to include an automated 3x PR review/respond loop, and Level 2 is reorganized as P9 (Alignment/Sync) -> P7 (Human Review) -> P8 (User PR Merge).

## 2. Requirements & Changes

### 2.1 Phase P6 (Deploy & PR Review/Respond Loop)
- **/kanche:git-push** -> **/kanche:gh-cli-pr-create** -> **loop ≤3x (/kanche:gh-cli-pr-review -> /kanche:gh-cli-pr-respond)**.
- AI pushes the feature branch, opens the PR, runs automated AI PR review, and automatically responds/fixes any flagged review feedback in a loop up to 3 times.

### 2.2 Level 2 Phase Sequence (P9 -> P7 -> P8)
Reorganize Level 2 phases in `sdd-run` and `sdd-continue`:
- **P9 (Product Alignment & Sync)**: AI automatically runs `/kanche:sdd-sync` on the feature branch to promote feature documentation (`docs/development/{slug}/*`) to domain-level product directories (`docs/product/plugins/kanche/{domain}/`), remove the temporary dev folder, and commit/push updates to the remote feature branch.
- **P7 (Human Review)**: Human review & verification checklist (`/kanche:qa-validate`). The user reviews the finalized code diff, verified test suite, and promoted product docs.
- **P8 (User PR Merge)**: The user merges the PR (or executes `/kanche:gh-cli-pr-merge`).

### 2.3 Skill & Documentation Updates
1. `plugins/kanche/skills/sdd-run/SKILL.md`:
   - Update Phase Model diagram and step explanations (P6 loop and P9 -> P7 -> P8 Level 2).
2. `plugins/kanche/skills/sdd-continue/SKILL.md`:
   - Update phase detection logic and phase walk order for Level 2 (P9 -> P7 -> P8).
3. Domain Documentation (`docs/product/plugins/kanche/sdd/`):
   - Update `specs.md`, `design.md`, `decisions.md` (ADR-007), and `changelog.md`.
4. UI Dashboard (`index.html`):
   - Update P6 and P9/P7/P8 visualization step descriptions and labels.

## 3. Acceptance Criteria
1. `/kanche:sdd-run` Phase Model displays Level 1 P6 with 3x review-respond loop, and Level 2 as P9 -> P7 -> P8.
2. P9 performs documentation sync (`/kanche:sdd-sync`) autonomously on the feature branch before P7.
3. P7 provides human review & checklist validation, and P8 hands over PR merging to the user.
4. All existing safety rules and plugin conventions are maintained.
