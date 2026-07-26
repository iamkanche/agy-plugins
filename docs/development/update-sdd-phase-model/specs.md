# Functional Specification: Update SDD Phase Model Layout, Forced Auto-Reviews & AI PR Review

## 1. Goal & Context
The `/kanche:sdd-run` master orchestrator workflow was presenting LEVEL 1 and LEVEL 2 phases side-by-side in a multi-column ASCII block, and per-phase reviews were not strictly enforced. To ensure maximum code quality and adherence to repository guidelines, each phase review must be forced and run up to 3x in a retry loop until a GO verdict is achieved, and an automated AI PR review (`/kanche:gh-cli-pr-review`) must execute immediately after PR creation at P6 deploy.

## 2. Scope & Requirements
- **Phase Model Layout**: Reformat the Phase Model diagram in `sdd-run` so LEVEL 2 appears directly below LEVEL 1 in a single vertical progression.
- **Forced Phase Review Loops**: Explicitly mandate in the SDD phase model and workflow instructions that every phase (P1 through P4) must automatically invoke its corresponding review skill immediately after generation (`/kanche:design-specs-review`, `/kanche:design-review`, `/kanche:planner-review`, `/kanche:qa-review`), running a retry loop up to 3x (`≤3x`) on NO-GO verdicts.
- **P6 AI PR Review**: Add `/kanche:gh-cli-pr-review` to P6 deploy step immediately after PR creation (`/kanche:pr-create`) to audit the PR diff against project rules and post inline suggestions.
- **Syncing Runtime Configuration**: Maintain 100% parity between source plugin files under `plugins/kanche/skills/` and active runtime installed plugins under `~/.gemini/config/plugins/kanche/skills/`.

## 3. Review Verdict & Criteria
- Verdict: GO
- Findings: None
