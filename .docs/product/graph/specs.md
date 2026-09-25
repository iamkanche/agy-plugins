# Graph Engineering Workflows Specification

## 1. Overview
Automates the **Graph Engineering Workflow (GEW / Graph-Driven Development)** lifecycle for autonomous Google Antigravity agents across phases P0 to P9, grounding all architecture, planning, implementation, and verification steps in the repository's Knowledge Graph (AST entities, community hubs, and topological DAGs).

## 2. Included Skills & Commands
- `/kanche:graph-run`: Master 10-phase Graph Engineering Workflow orchestrator (P0 to P9) with persistent `/goal` support.
- `/kanche:graph-continue`: Resumes Graph Engineering Workflow from on-disk graph and task state.
- `/kanche:graph-steering`: Analyzes repository using Knowledge Graph extraction and returns steering guideline bodies.
- `/kanche:graph-sync`: Promotes feature documentation to domain-level product directories (`.docs/product/{domain}/`), verifies module dependency integrity, and cleans up dev folders.
- `/kanche:graph-init`: Bootstraps graph-grounded steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/kanche:graph-init-update`: Re-analyzes repo and merges updates into steering guidelines with knowledge graph context.

## 3. Backward Compatibility
- Legacy SDD commands (`/kanche:sdd-run`, `/kanche:sdd-continue`, `/kanche:sdd-steering`, `/kanche:sdd-sync`, `/kanche:sdd-init`, `/kanche:sdd-init-update`) are preserved as seamless forwarding wrappers that execute the corresponding `graph-*` skills.

## 4. Product Invariants
- **Knowledge Graph Grounding**: Architectural analysis, impact mapping, and guidelines survey are grounded in AST and semantic knowledge graphs.
- **Topological DAG Planning**: In P3, `/kanche:planner-tasks` decomposes tasks into strict dependency tiers (Tier 0 to Tier 3), preventing orphan references and circular coupling.
- **Graph Health Diagnostics Gate**: In P5, `/kanche:qa-validate` audits AST structures to ensure 0 dangling endpoint edges, 0 missing endpoints, and 0 circular dependencies before running functional tests.
- **Zero Autonomous Destructive Execution**: All destructive commands (`git push`, `git commit`, `rm -rf`, `gh pr merge`, branch/tag deletes) unconditionally require interactive human confirmation via `default_api:ask_question`.
- **Unified Model Routing**: All 16 subagents and skills are standardized on `model: flash` (Gemini Flash High).
