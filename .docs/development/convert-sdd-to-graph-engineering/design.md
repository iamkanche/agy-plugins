# Technical Design: Convert SDD to Graph Engineering Workflow

## Approach
We implement the Graph Engineering Workflow as the foundational architecture for the `kanche` plugin bundle in `agy-plugins`. Rather than breaking backward compatibility, we adopt a **Dual-Surface Compatibility Architecture**:
1. **Primary Graph Surface (`/kanche:graph-*`)**: Native implementations of `graph-run`, `graph-continue`, `graph-steering`, `graph-sync`, `graph-init`, and `graph-init-update`.
2. **Compatibility Wrapper Surface (`/kanche:sdd-*`)**: Thin forwarding wrappers that accept legacy arguments/flags, emit a deprecation guidance banner, and invoke the graph engineering pipeline.
3. **Graph Diagnostics & Topological Planning**: `/kanche:planner-tasks` generates Topological Dependency Tiers, and `/kanche:qa-validate` incorporates an automated AST & Graph Health Check.

## Architecture Context

```mermaid
flowchart TD
    User([User / Autonomous Agent]) --> InputChoice{Command Invocation}
    InputChoice -->|/kanche:graph-run| GraphEngine[Graph Engineering Workflow Orchestrator]
    InputChoice -->|/kanche:sdd-run (Legacy)| SDDWrapper[Backward-Compatible SDD Wrapper]
    SDDWrapper -->|Forward with Notice| GraphEngine

    subgraph "Graph Engineering Lifecycle (P0 - P9)"
        GraphEngine --> P0[P0: Graph Discovery & Ingestion<br/>AST & Module Knowledge Graph]
        P0 --> P1[P1: Impact Subgraph Specs<br/>design-grill & design-specs]
        P1 --> P2[P2: Graph Architecture & Stitch UI<br/>design-init & ui-design-stitch]
        P2 --> P3[P3: Topological Task DAG<br/>planner-tasks & qa-test-plan]
        P3 --> P4[P4: Graph-Guided Implementation<br/>code-implement & code-review]
        P4 --> P5[P5: Graph Integrity Gate<br/>Graph Health & qa-validate]
        P5 --> P6[P6: Graph Blast Radius PR<br/>gh-cli-pr-review & PR loop]
        P6 --> P7[P7: Knowledge Graph Memory Sync<br/>graph-sync & domain consolidation]
        P7 --> P8[P8: Graph Verification Checklist]
        P8 --> P9[P9: Gated PR Merge & Release Tag]
    end
```

## Components

### 1. Master Graph Orchestrator (`plugins/kanche/skills/graph-run/SKILL.md`)
- Coordinates the 10 phases P0–P9.
- Manages persistent `/goal` execution, loop-state tracking, and automatic 3x retry loops.
- Enforces strict human-confirmation safety gating for destructive actions.

### 2. Graph State Resume Engine (`plugins/kanche/skills/graph-continue/SKILL.md`)
- Evaluates on-disk state (`.docs/guidelines/`, `.docs/development/{slug}/`, `tasks.md` DAG tier progress, git branch state).
- Resumes execution at the precise phase without losing previous progress.

### 3. Graph Steering & Repository Survey (`plugins/kanche/skills/graph-steering/SKILL.md`)
- Surveys repository using Knowledge Graph AST and semantic extractions.
- Identifies community hubs, god nodes, and module boundaries.
- Emits the four steering docs (`product.md`, `tech.md`, `structure.md`, `rules.md`).

### 4. Graph Knowledge Sync (`plugins/kanche/skills/graph-sync/SKILL.md`)
- Synchronizes feature documentation into permanent domain product memory (`.docs/product/{domain}/`).
- Verifies module and dependency boundaries, syncing product memory and requesting confirmation to clean up the ephemeral development directory.

### 5. Graph Init & Update Skills (`graph-init` & `graph-init-update`)
- Bootstraps or refreshes repository steering guidelines with knowledge graph context.

### 6. Backward Compatibility Wrappers (`sdd-run`, `sdd-continue`, `sdd-steering`, `sdd-sync`, `sdd-init`, `sdd-init-update`)
- Transparently wrap around the `graph-*` skills.
- Parse identical CLI parameters (`--mode`, `--from`, `--until`, `/goal`) and emit:
  `[NOTICE] /kanche:sdd-* is deprecated and forwarded to /kanche:graph-*. Please use /kanche:graph-* in future workflows.`

### 7. Enhanced Planning & Validation Skills
- `planner-tasks/SKILL.md`: Decomposes tasks into **Topological Tiers** (Tier 0: Models/Contracts, Tier 1: Core Services, Tier 2: Controllers/UI, Tier 3: E2E/Tests) to enforce proper implementation order.
- `qa-validate/SKILL.md`: Introduces **Graph Health Diagnostics Gate** before running test suites, checking for missing endpoint edges, dangling imports, and circular dependencies.

### 8. Subagent Profiles Enhancement (`plugins/kanche/agents/`)
- `@researcher`: Knowledge Graph traversal and survey.
- `@architect`: Interface topology and boundary mapping.
- `@planner`: Topological DAG decomposition.
- `@validator`: Graph integrity diagnostics and health checking.

## Interfaces & CLI Specifications
All skills maintain standard Antigravity YAML frontmatter and unified model routing:
```yaml
---
name: graph-run
description: Drive a feature work item through the 10-phase Graph Engineering Workflow (P0 to P9).
model: flash
---
```

## Alternatives Considered
- **Direct Hard Replacement (Removing `sdd-*` immediately)**: Rejected. Would break existing developer habits, scripts, and documentation referencing `sdd-run`. Dual-surface compatibility provides a smooth, zero-disruption upgrade path.

## Risks & Mitigations
- **Risk**: User confusion regarding `sdd-*` vs `graph-*`.
  - **Mitigation**: Clear notice messages emitted when `sdd-*` is invoked, and comprehensive documentation in `README.md` and `index.html`.
- **Risk**: Missing external graph dependencies on user machine.
  - **Mitigation**: 100% native zero-dependency implementation using standard library AST parsing, manifest inspection, and topological task DAGs.
