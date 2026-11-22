---
name: team-swarm
description: Orchestrate parallel kanche specialists across DAG tiers or workstreams using Antigravity native swarm or run_workflow.
---

# /kanche:team-swarm

**Summary.** Scale Graph Engineering execution across non-overlapping files/modules using Antigravity 2.0's native **`swarm`** (interactive parallel collaborators on a shared board) or **`run_workflow`** (deterministic Python DAG fan-out & `<=3x` loops).

## When to Use Which

- **Use `run_workflow` (Python DAG):** Deterministic Tier 0 → Tier 3 execution, `[P]` task fan-out, and `<=3x` Generator ↔ Reviewer `review-verdict` loops with structured JSON schemas.
- **Use native `swarm`:** Large multi-area features needing live cross-worker coordination (`#frontend`, `#backend`, `#qa` channels) and dedicated verifiers (1 verifier per 2–3 authors).

## Execution Protocol

### Option A — Native Swarm
1. Partition work so **no two authors touch the same file**.
2. Set title via `swarm{action:"title", title:"<slug>"}`.
3. Add domain authors with `workspace:"share"` (isolated working copy) and explicit file ownership + `[done]` post instructions (`@frontend-expert`, `@backend-expert`, `@data-architect`, `@coder`).
4. Add verifiers (`@reviewer`, `@tester`, `@validator`) with default `workspace:"inherit"` to inspect diffs, run `scripts/graph_health.py` / tests, and post findings to authors by `@name`.
5. Merge/land each `share` workspace back cleanly before `kill`ing workers.

### Option B — Dynamic Python `run_workflow`
1. Write a Python script using `phase()`, `parallel()`, `pipeline()`, and `agent(..., workspace="share", model="flash")` to run `[P]` tasks concurrently per DAG tier, followed by `reviewer` verdict checks.
2. Execute via `run_workflow` tool.

## Rules

- **Main-Session Gates:** Neither swarm workers nor `run_workflow` scripts may bypass `rules/destructive-safety.md`. All commits, pushes, merges, and `rm -rf` remain in the main conversation via `default_api:ask_question`.
- Follow `rules/token-optimization.md` and `rules/loop-engineering.md`.
