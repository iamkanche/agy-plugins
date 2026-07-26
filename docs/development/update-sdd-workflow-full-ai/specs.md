# Specification: Full AI SDD Workflow & Level 2 Human Merge Reorganization

## 1. Executive Summary
This specification updates the SDD workflow (`/kanche:sdd-run` and `/kanche:sdd-continue`) to operate as a Full AI workflow where Level 1 and Level 2 AI automation execute end-to-end, moving Phase P7 (Human Review & PR Merge) to the last phase of Level 2 and handing over PR merging to the user instead of automated merge in Phase P9.

## 2. Requirements & Changes

### 2.1 Level 2 Phase Sequence
Reorganize Level 2 phases in `sdd-run` and `sdd-continue`:
- **P8 (PR Modifications & Polling)**: AI automatically polls PR reviews/comments (up to 3x loop) and executes `/kanche:gh-cli-pr-respond` to fix issues, re-verify, commit, and push updates.
- **P9 (Product Alignment & Sync)**: AI automatically runs `/kanche:sdd-sync` on the feature branch to promote feature documentation (`docs/development/{slug}/*`) to domain-level product directories (`docs/product/plugins/kanche/{domain}/`), remove the temporary dev folder, and commit/push updates to the remote feature branch.
- **P7 (Human Review & PR Merge)**: Positioned as the final phase in Level 2. The human user reviews the finalized PR diff, verified tests, and synced product docs, then performs/triggers the PR merge (instead of P9 auto-merging).

### 2.2 Skill & Documentation Updates
1. `plugins/kanche/skills/sdd-run/SKILL.md`:
   - Update Phase Model diagram and step explanations.
   - Update P8, P9, and P7 descriptions to reflect Full AI execution leading up to human PR merge at P7.
2. `plugins/kanche/skills/sdd-continue/SKILL.md`:
   - Update phase detection logic and phase walk order for Level 2 (P8 -> P9 -> P7).
3. Domain Documentation (`docs/product/plugins/kanche/sdd/`):
   - Update `specs.md`, `design.md`, `decisions.md`, `changelog.md` to record ADR and workflow updates.
4. UI Dashboard (`index.html`):
   - Update P7-P9 visualization step descriptions and labels if applicable.

## 3. Acceptance Criteria
1. `/kanche:sdd-run` Phase Model displays Level 2 as P8 -> P9 -> P7 (Human Review & PR Merge).
2. P9 performs documentation sync (`/kanche:sdd-sync`) autonomously before P7.
3. P7 explicitly delegates PR merging to the user instead of automated P9 execution.
4. All existing safety rules and plugin conventions are maintained.
