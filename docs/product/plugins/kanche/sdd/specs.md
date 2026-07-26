# SDD Workflows Specification

## 1. Overview
Automates the Spec-Driven Development (SDD) lifecycle for autonomous Google Antigravity agents across phases P0 to P9.

## 2. Included Skills & Commands
- `/kanche:sdd-init`: Bootstraps steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/kanche:sdd-init-update`: Re-analyzes repo and merges updates into steering guidelines.
- `/kanche:sdd-run`: Drives feature work items through the full SDD phase model (P0 to P9).
- `/kanche:sdd-continue`: Resumes SDD workflow from on-disk state.
- `/kanche:sdd-steering`: Analyzes repository and returns steering guideline bodies.
- `/kanche:sdd-sync`: Promotes feature documentation to product directory and cleans up dev folders.

## 3. Product Invariants
- Preserves human-tuned guidelines and safety rules during updates.
- Enforces gated confirmation for PR merges when `auto_merge: false`.
