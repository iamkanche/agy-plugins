---
name: sdd-continue
description: Resume the SDD workflow at the phase inferred from on-disk state — seamlessly forwards to /kanche:graph-continue.
model: flash
---

# /kanche:sdd-continue (Compatibility Forwarder)

> 💡 **Notice**: Spec-Driven Development (SDD) workflows have been upgraded to the **Graph Engineering Workflow (GEW)**. Invoking `/kanche:sdd-continue` automatically executes `/kanche:graph-continue` with complete backward compatibility. We recommend updating your commands and scripts to `/kanche:graph-continue`.

**Summary.** Resume the engineering workflow at the phase inferred from on-disk graph and development state, orchestrating the full 16-agent team. All destructive operations strictly require human confirmation.

## Inputs

Accepts all legacy SDD inputs and forwards them directly to `/kanche:graph-continue`:

- **`--mode=auto|manual`** — default **auto**.
- **`--from=<phase>`** — override detection and force resume point (`P0`..`P9`).
- **`--until=<phase>`** — stop after this phase (inclusive).
- **slug** (optional, positional) — disambiguates dev folder.

## Execution

Execute the Graph Engineering resume engine:
```
/kanche:graph-continue [--mode=auto|manual] [--from=<phase>] [--until=<phase>] [slug]
```
Refer to `plugins/kanche/skills/graph-continue/SKILL.md` for detection rules and execution details.
