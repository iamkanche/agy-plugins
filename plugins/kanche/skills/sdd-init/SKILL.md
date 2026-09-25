---
name: sdd-init
description: Bootstrap the steering guidelines for this repository — seamlessly forwards to /kanche:graph-init.
model: flash
---

# /kanche:sdd-init (Compatibility Forwarder)

> 💡 **Notice**: SDD bootstrapping has been upgraded to the Knowledge Graph-grounded **`/kanche:graph-init`**. Invoking `/kanche:sdd-init` automatically executes `/kanche:graph-init`.

**Summary.** Analyze this repository using Knowledge Graph extraction and write the four steering docs under `.docs/guidelines/`.

## Execution

Execute the Graph Engineering bootstrap workflow:
```
/kanche:graph-init
```
Refer to `plugins/kanche/skills/graph-init/SKILL.md` for full instructions.
