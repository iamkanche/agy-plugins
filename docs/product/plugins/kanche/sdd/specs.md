# SDD Workflows Specification

## 1. Overview
Automates the Spec-Driven Development (SDD) lifecycle for autonomous Google Antigravity agents across phases P0 to P9.

## 2. Included Skills & Commands
- `/kanche:sdd-init`: Bootstraps steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/kanche:sdd-init-update`: Re-analyzes repo and merges updates into steering guidelines.
- `/kanche:sdd-run`: Drives feature work items through the full SDD phase model (P0 to P9).
- `/kanche:sdd-continue`: Resumes SDD workflow from on-disk state.
- `/kanche:sdd-steering`: Analyzes repository and returns steering guideline bodies.
- `/kanche:sdd-sync`: Promotes feature documentation to domain-level product directories (`docs/product/plugins/kanche/{domain}/`) and cleans up dev folders.

## 3. Domain-Based Document Routing
- `/kanche:sdd-sync` maps modified skills and code paths to one of the 7 core domain groups (`sdd`, `git`, `gh-cli`, `design`, `dev`, `planner`, `qa`).
- Document specifications and design decisions are merged into permanent `docs/product/plugins/kanche/{domain}/specs.md` and `design.md` files rather than creating transient feature slug subfolders.

## 4. Product Invariants
- Preserves human-tuned guidelines and safety rules during updates.
- Executes Level 1 and Level 2 as Full AI automation, running PR modifications (P8) and document sync (P9) before handing over final review and PR merge to the user at P7.
- Eliminates ephemeral feature slug subfolders in product documentation.
