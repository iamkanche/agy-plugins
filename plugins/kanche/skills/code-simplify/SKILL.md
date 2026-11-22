---
name: code-simplify
description: Audit modified code for DRY, YAGNI, dead code, and complexity reductions, optionally applying safe simplifications.
---

# /kanche:code-simplify

**Mission.** Identify and eliminate code duplication, dead paths, deep nesting, and premature abstractions on touched files (`@reviewer` / `@coder`), keeping behavior 100% intact.

## Inputs

- `<target-path>` (optional) — files/directories to simplify. Defaults to `git diff --name-only` / `git diff --staged --name-only`.
- `--auto-apply` — apply safe, behavior-preserving simplifications and re-run project tests. Defaults to read-only diff suggestions.

## Steps

1. **Scope Diff.** Inspect modified/staged files (`git diff`) and surrounding helpers.
2. **Detect Simplification Opportunities:**
   - Duplicate logic extractable into a shared helper.
   - Deep nesting replaceable by early returns.
   - Unused imports, dead variables, or speculative abstractions (YAGNI).
   - Over-specialized `if/elif` chains replaceable by a lookup table/mapping.
3. **Apply or Report:**
   - **Default (Read-Only):** Output compact `file:line` findings and minimal replacement snippets.
   - **`--auto-apply`:** Edit files with minimal diffs, then run the project's lint/test commands from `.docs/guidelines/tech.md` to confirm zero regressions.

## Rules

- Never alter public API contracts, test assertions, or existing comments unrelated to the change.
- Never run `git commit` or `git push`.
- Follow `rules/token-optimization.md` and `rules/destructive-safety.md`.
