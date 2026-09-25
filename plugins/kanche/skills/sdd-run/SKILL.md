---
name: sdd-run
description: Drive a feature work item through the full SDD phase model (P0 to P9) — seamlessly forwards to /kanche:graph-run for Graph Engineering.
model: flash
---

# /kanche:sdd-run (Compatibility Forwarder)

> 💡 **Notice**: Spec-Driven Development (SDD) workflows have been upgraded to the **Graph Engineering Workflow (GEW)**. Invoking `/kanche:sdd-run` automatically executes `/kanche:graph-run` with complete backward compatibility. We recommend updating your commands and scripts to `/kanche:graph-run`.

**Summary.** Drive a work item through the complete Graph Engineering Lifecycle (P0→P9), orchestrating the full 16-agent team and knowledge graph skills. All destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) strictly require human confirmation. Supports `/goal` persistent execution mode.

## Inputs

Accepts all legacy SDD inputs and forwards them directly to `/kanche:graph-run`:

- **slug** (optional, positional) — feature slug (e.g. `auth-oauth2`).
- **`--mode=auto|manual`** — default **auto**.
- **`--goal` / `/goal`** — enable goal-driven persistent execution mode.
- **`--from=<phase>`** — start the walk at this phase (`P0`..`P9`).
- **`--until=<phase>`** — stop after this phase (inclusive).

## Execution

Execute the master Graph Engineering orchestrator:
```
/kanche:graph-run [slug] [--mode=auto|manual] [--goal] [--from=<phase>] [--until=<phase>]
```
Refer to `plugins/kanche/skills/graph-run/SKILL.md` for full phase details and execution rules.
