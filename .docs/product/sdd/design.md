# SDD Workflows Design (Migrated to Graph Engineering)

> 💡 **Migration Notice**: The Spec-Driven Development (SDD) architecture has been upgraded to the **Graph Engineering Workflow (GEW)**. Please see `.docs/product/graph/design.md` for current system architecture, phase models, and topological DAG protocols.

## System Architecture
The SDD workflow family continues to support legacy invocations via compatibility forwarding wrappers:
- `sdd-run` delegates to `graph-run`
- `sdd-continue` delegates to `graph-continue`
- `sdd-steering` delegates to `graph-steering`
- `sdd-sync` delegates to `graph-sync`
- `sdd-init` delegates to `graph-init`
- `sdd-init-update` delegates to `graph-init-update`

All execution benefits from knowledge graph grounding, topological task DAGs, and graph integrity health checks while retaining complete backward compatibility.
