# SDD Workflows Specification (Migrated to Graph Engineering)

> 💡 **Migration Notice**: The Spec-Driven Development (SDD) workflow has been upgraded to the **Graph Engineering Workflow (GEW)**. All SDD commands now forward directly to their graph-native counterparts in `.docs/product/graph/specs.md`.

## 1. Overview
Automates the Spec-Driven Development (SDD) lifecycle for autonomous Google Antigravity agents across phases P0 to P9, upgraded to graph-native execution.

## 2. Forwarded Skills & Commands
- `/kanche:sdd-init` → forwards to `/kanche:graph-init`
- `/kanche:sdd-init-update` → forwards to `/kanche:graph-init-update`
- `/kanche:sdd-run` → forwards to `/kanche:graph-run`
- `/kanche:sdd-continue` → forwards to `/kanche:graph-continue`
- `/kanche:sdd-steering` → forwards to `/kanche:graph-steering`
- `/kanche:sdd-sync` → forwards to `/kanche:graph-sync`

## 3. Product Invariants
- 100% backward compatibility maintained for all existing workflows.
- Strictly adheres to `plugins/kanche/rules/destructive-safety.md` with mandatory interactive human confirmation.
- Primary documentation and architecture are maintained under `.docs/product/graph/`.
