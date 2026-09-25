---
name: sdd-sync
description: Sync development logs and documents to domain-level product directories — seamlessly forwards to /kanche:graph-sync.
model: flash
---

# /kanche:sdd-sync (Compatibility Forwarder)

> 💡 **Notice**: SDD synchronization has been upgraded to the Knowledge Graph-native **`/kanche:graph-sync`**, which synchronizes product documents and validates codebase module dependencies. Invoking `/kanche:sdd-sync` automatically executes `/kanche:graph-sync`.

**Summary.** Promote development documentation from `.docs/development/{slug}/` into permanent domain product directories (`.docs/product/{domain}/`) and sync the repository Knowledge Graph. Cleanup of ephemeral dev folders is strictly human-gated.

## Inputs

Accepts all legacy SDD inputs and forwards them directly to `/kanche:graph-sync`:
- **slug** (optional, positional) — the feature slug.
- **`--domain=<domain>`** (optional, flag) — the target product domain.

## Execution

Execute the Graph Engineering sync skill:
```
/kanche:graph-sync [slug] [--domain=<domain>]
```
Refer to `plugins/kanche/skills/graph-sync/SKILL.md` for promotion protocol and gated cleanup instructions.
