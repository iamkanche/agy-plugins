# Functional Specification: Domain-Based SDD Sync & Documentation Consolidation

## 1. Overview
Refactor `/kanche:sdd-sync` to map documentation promotion directly into permanent domain group directories (`docs/product/plugins/kanche/{domain}/` e.g., `design/`, `git/`, `gh-cli/`, `sdd/`, `dev/`, `planner/`, `qa/`), preventing creation of transient feature slug directories.

## 2. User Stories
- **As a** developer or AI pair programmer,
- **I want** product documentation to be updated cleanly under fixed domain folders (`docs/product/plugins/kanche/sdd/`),
- **So that** specifications and design docs remain structured by system domain without folder sprawl.

## 3. Acceptance Criteria
1. `/kanche:sdd-sync` routes feature documentation to matching `docs/product/plugins/kanche/{domain}/` directories.
2. Temporary development folder `docs/development/{slug}/` is cleaned up after synchronization.
3. Steering guidelines (`docs/guidelines/`) and durable memory (`docs/product/memory.md`) remain aligned.
