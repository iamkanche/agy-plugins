# QA Test Plan: Token Optimizer Agents & Global Token Optimization

- **Feature:** Token Optimizer Agents & Global Token Optimization
- **Slug:** `token-optimizer`
- **PBI:** `PBI-20260926-token-optimizer`
- **Domain:** `optimizer`

## Multi-Tiered Test Strategy

### 1. Structural & Syntax Validation (Tier 0 & Tier 1)
- **JSON Linting:** Verify all 17 `agent.json` files and `plugin.json` parse with zero syntax errors via `jq`.
- **Tool Permissions:** Ensure `@token-optimizer` has `enable_write_tools: false` and read-only tools `["read_file", "view_file", "grep_search", "list_dir"]`.
- **YAML Frontmatter Integrity:** Verify each `SKILL.md` retains valid `name`, `description`, and `model` frontmatter fields.

### 2. Safety Invariant & Contract Regression Tests (Tier 2)
- **Destructive Safety Verification:** Verify that destructive safety references (`destructive-safety.md`, `ask_question`) remain present in all mutating skills (`git-push`, `git-commit`, `gh-cli-pr-merge`, `git-branch-delete`, `git-tag-*`, `graph-sync`, `graph-run`).
- **Review Verdict Interface:** Verify that review skills (`code-review`, `qa-review`, `design-review`, `design-specs-review`, `planner-review`) retain the exact `review-verdict` fenced block schema.
- **Workflow Phase Integrity:** Verify `graph-run` and `graph-continue` maintain all 10 phases (P0 to P9) without broken steps.

### 3. Token Efficiency & Metrics Benchmark (Tier 3)
- **Character / Token Reduction Benchmark:** Compare total size of `plugins/kanche/skills/` and `plugins/kanche/agents/` before and after optimization.
- **Target:** ≥ 15% reduction in overall instruction token count while retaining 100% semantic coverage.

### 4. UI & Showcase Visual Assertions
- Verify `index.html` loads cleanly, has no broken tags, and displays:
  - 17 Agents in header badge and team grid.
  - `@token-optimizer` agent card with teal/cyan styling.
  - `/kanche:token-optimize` skill badge.
