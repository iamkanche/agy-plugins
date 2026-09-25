---
name: sdd-steering
description: Analyze the repository and return steering guideline bodies — seamlessly forwards to /kanche:graph-steering.
model: flash
---

# /kanche:sdd-steering (Compatibility Forwarder)

> 💡 **Notice**: Spec-Driven Development (SDD) steering has been upgraded to the Knowledge Graph-grounded **`/kanche:graph-steering`**. Invoking `/kanche:sdd-steering` automatically executes `/kanche:graph-steering`.

**Mission.** Analyze the repository using Knowledge Graph extraction and return the four steering guideline bodies (`product.md`, `tech.md`, `structure.md`, `rules.md`).

## Execution

Execute the Graph Engineering steering analyzer:
```
/kanche:graph-steering
```
Refer to `plugins/kanche/skills/graph-steering/SKILL.md` for analysis guidelines and output schema.
