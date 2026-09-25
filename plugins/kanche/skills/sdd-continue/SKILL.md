---
name: sdd-continue
description: Resume the SDD workflow at the phase inferred from on-disk state — seamlessly forwards to /kanche:graph-continue.
model: flash
---

# /kanche:sdd-continue (Compatibility Forwarder)

> 💡 **Notice**: SDD workflows have upgraded to **Graph Engineering Workflow (GEW)**. `/kanche:sdd-continue` forwards directly to `/kanche:graph-continue`.

**Summary.** Resume workflow at phase inferred from on-disk state, orchestrating the 17-agent team. Destructive operations strictly require human confirmation per `rules/destructive-safety.md`. Enforces `rules/token-optimization.md`.

## Inputs

Forwards directly to `/kanche:graph-continue`:
- **`--mode=auto|manual`** — default **auto**.
- **`--from=<phase>`** — force resume phase (`P0`..`P9`).
- **`--until=<phase>`** — stop phase (inclusive).
- **slug** (optional, positional) — target dev folder.

## Execution

```
/kanche:graph-continue [--mode=auto|manual] [--from=<phase>] [--until=<phase>] [slug]
```
See `plugins/kanche/skills/graph-continue/SKILL.md` for phase details.
