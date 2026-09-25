---
name: sdd-init-update
description: Re-analyze this repository and refresh guidelines — seamlessly forwards to /kanche:graph-init-update.
model: flash
---

# /kanche:sdd-init-update (Compatibility Forwarder)

> 💡 **Notice**: SDD guidelines refresh has been upgraded to the Knowledge Graph-grounded **`/kanche:graph-init-update`**. Invoking `/kanche:sdd-init-update` automatically executes `/kanche:graph-init-update`.

**Summary.** Re-analyze this repository using Knowledge Graph extraction and refresh the four steering docs under `.docs/guidelines/`, merging new graph findings into existing docs.

## Execution

Execute the Graph Engineering guidelines refresh workflow:
```
/kanche:graph-init-update
```
Refer to `plugins/kanche/skills/graph-init-update/SKILL.md` for full instructions.
