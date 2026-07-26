# Specs: Enforce HEREDOC Commit Formatting in SDD Orchestrator & Sync Workflows

## Context
During feature automation runs, inline single-line `git commit -m` commands were occasionally executed during P7 doc-sync steps, bypassing the mandatory Conventional Commits HEREDOC structure (`## Overview`, `## Changes`, `## Impact`) defined in `/kanche:git-commit`. To prevent context drift and ensure strict adherence across all orchestrations, the SDD workflow specifications (`sdd-run`, `sdd-continue`, and `sdd-sync`) must explicitly embed the HEREDOC format requirements and prohibit single-line commit shortcuts.

## Scope
- **In-Scope:**
  - Update `plugins/kanche/skills/sdd-sync/SKILL.md` step 5 to display the exact `/kanche:git-commit` HEREDOC template syntax.
  - Update `plugins/kanche/skills/sdd-run/SKILL.md` Section 3 (Commit Checkpoint Policy) to explicitly prohibit inline single-line `git commit -m` commands and mandate HEREDOC execution.
  - Update `plugins/kanche/skills/sdd-continue/SKILL.md` to reinforce the HEREDOC commit policy.
- **Out of Scope:**
  - Modifying git CLI binary execution behavior.

## User Stories
- **As a Developer/Lead**, I want all commits across SDD workflows to carry structured `## Overview`, `## Changes`, and `## Impact` sections, so that git history remains clean and standardized.

## Acceptance Criteria
1. `sdd-sync/SKILL.md` specifies the exact `git commit -F - <<'EOF'` HEREDOC structure in Step 5.
2. `sdd-run/SKILL.md` explicitly prohibits single-line `git commit -m` shortcuts.
3. `sdd-continue/SKILL.md` aligns with `sdd-run/SKILL.md` commit checkpoint policy.

## NFR
- Maintainability: 100% compliance with Conventional Commits HEREDOC standard.
