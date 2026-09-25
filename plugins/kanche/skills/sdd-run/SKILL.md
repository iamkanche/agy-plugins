---
name: sdd-run
description: Drive a feature work item through the full SDD phase model (P0 to P9) — seamlessly forwards to /kanche:graph-run for Graph Engineering.
model: flash
---

# /kanche:sdd-run (Compatibility Forwarder)

> 💡 **Notice**: SDD workflows have upgraded to **Graph Engineering Workflow (GEW)**. `/kanche:sdd-run` forwards directly to `/kanche:graph-run`.

**Summary.** Drive a work item through the Graph Engineering Lifecycle (P0→P9), orchestrating the full 17-agent team. Destructive operations strictly require human confirmation per `rules/destructive-safety.md`. Enforces `rules/token-optimization.md`.

## Inputs

Forwards directly to `/kanche:graph-run`:
- **slug** (optional, positional) — feature slug.
- **`--mode=auto|manual`** — default **auto**.
- **`--goal` / `/goal`** — persistent execution mode.
- **`--from=<phase>`** — start phase (`P0`..`P9`).
- **`--until=<phase>`** — stop phase (inclusive).

## Execution

```
/kanche:graph-run [slug] [--mode=auto|manual] [--goal] [--from=<phase>] [--until=<phase>]
```
See `plugins/kanche/skills/graph-run/SKILL.md` for phase details.
