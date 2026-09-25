# PBI-20260925-convert-sdd-to-graph-engineering: Convert SDD Workflow to Graph Engineering Workflow

- **ID:** PBI-20260925-convert-sdd-to-graph-engineering
- **Domain:** graph
- **Priority:** P1
- **Story Points:** 8
- **Status:** In Progress

## Summary
Transform the Spec-Driven Development (SDD) workflow family in agy-plugins into a modern, graph-native Graph Engineering Workflow (GEW / Graph-Driven Development). Grounds every lifecycle phase in codebase knowledge graphs, AST dependency structures, topological DAG task planning, and graph integrity verification.

## User Story
**As an** autonomous software engineering agent or developer using Google Antigravity  
**I want to** execute a graph-native software development workflow (`/kanche:graph-run`) that leverages knowledge graphs, topological task DAGs, and AST diagnostics  
**So that** complex multi-file features are architected, implemented, and validated with precise dependency order and zero broken cross-boundary contracts, while retaining backward compatibility with `/kanche:sdd-*`.

## Acceptance Criteria
- [ ] **Given** a target codebase, **When** `/kanche:graph-steering` or `/kanche:graph-init` executes, **Then** it surveys the repo using knowledge graph extraction (`graphify` / AST structures) and outputs grounded guidelines.
- [ ] **Given** a feature work item, **When** `/kanche:graph-run` or `/kanche:sdd-run` is invoked, **Then** it orchestrates the 10-phase graph engineering model (P0-P9) with topological DAG planning in P3 and graph integrity gates in P5.
- [ ] **Given** legacy SDD commands (`/kanche:sdd-run`, `/kanche:sdd-continue`, `/kanche:sdd-steering`, `/kanche:sdd-sync`, `/kanche:sdd-init`, `/kanche:sdd-init-update`), **When** invoked, **Then** they cleanly forward to the corresponding `/kanche:graph-*` skills with backward-compatible deprecation notices.
- [ ] **Given** any destructive operations (`git commit`, `git push`, `rm -rf`, `gh pr merge`), **When** reached, **Then** they halt and prompt for explicit human confirmation per `destructive-safety.md`.
- [ ] **Given** the documentation showcase (`index.html`) and manifest (`plugin.json`), **When** rendered, **Then** they display the Graph Engineering Workflow phases, subagents, and updated command catalogs.

## Technical Notes & Dependencies
- Core skills: `graph-run`, `graph-continue`, `graph-steering`, `graph-sync`, `graph-init`, `graph-init-update`.
- Enhanced skills: `planner-tasks` (Topological DAGs), `qa-validate` (Graph Health Check gate).
- Subagents: `@researcher`, `@architect`, `@planner`, `@validator`.
- Compatibility: `sdd-run`, `sdd-continue`, `sdd-steering`, `sdd-sync`, `sdd-init`, `sdd-init-update`.

## Linked Specs & Design
- Specs: `.docs/product/graph/specs.md`
- Design: `.docs/product/graph/design.md`
