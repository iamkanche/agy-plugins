# System Design: Enforce HEREDOC Commit Formatting in SDD Orchestrator & Sync Workflows

## Approach
Update SDD orchestrator skill definitions (`sdd-run`, `sdd-continue`, and `sdd-sync`) to explicitly define and enforce the HEREDOC Conventional Commit template syntax, while adding strict negative constraints prohibiting single-line inline commit shortcuts.

## Affected Components
1. `plugins/kanche/skills/sdd-sync/SKILL.md`:
   - Replace generic commit prose in Step 5 with the full HEREDOC template structure (`## Overview`, `## Changes`, `## Impact`).
2. `plugins/kanche/skills/sdd-run/SKILL.md`:
   - Update Section 3 (Commit Checkpoint Policy) to mandate `/kanche:git-commit` HEREDOC formatting and explicitly forbid single-line `git commit -m` commands.
3. `plugins/kanche/skills/sdd-continue/SKILL.md`:
   - Align commit rules with `sdd-run/SKILL.md`.

## Detailed Template Specification
```bash
git commit -F - <<'EOF'
<type>(<scope>): <subject>

## Overview
<summary>

## Changes
- <change 1>
- <change 2>

## Impact
<impact>
EOF
```
