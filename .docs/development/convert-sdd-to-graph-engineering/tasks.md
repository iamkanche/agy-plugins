# Task Manifest: Convert SDD to Graph Engineering Workflow

## Topological Dependency Tiers

### Tier 0: Foundation, Manifest & Loop Protocol
- [x] Task 0.1: Update `plugins/kanche/plugin.json` to bump version to `0.4.0`, add graph engineering description, tools, and keywords (`graph-engineering`, `knowledge-graph`, `dag`, `ast`).
- [x] Task 0.2: Update `plugins/kanche/rules/loop-engineering.md` to define the 10-phase Graph Engineering lifecycle, topological DAG task protocol, and graph health integrity gate.
- [x] Task 0.3: Update agent manifests in `plugins/kanche/agents/`:
  - `researcher/agent.json`: Add knowledge graph survey & traversal responsibilities.
  - `architect/agent.json`: Add interface topology and graph contract mapping responsibilities.
  - `planner/agent.json`: Add topological DAG task decomposition responsibilities.
  - `validator/agent.json`: Add graph integrity and AST diagnostic audit responsibilities.

### Tier 1: Core Graph Engineering Skills
- [x] Task 1.1: Create `plugins/kanche/skills/graph-run/SKILL.md` (Master orchestrator for P0–P9 with `/goal` and loop support).
- [x] Task 1.2: Create `plugins/kanche/skills/graph-continue/SKILL.md` (Resume Graph Engineering Workflow from on-disk graph state).
- [x] Task 1.3: Create `plugins/kanche/skills/graph-steering/SKILL.md` (Knowledge Graph repository survey & steering guideline extraction).
- [x] Task 1.4: Create `plugins/kanche/skills/graph-sync/SKILL.md` (Domain documentation sync and knowledge graph cache update).
- [x] Task 1.5: Create `plugins/kanche/skills/graph-init/SKILL.md` (Bootstrap graph steering docs and knowledge graph).
- [x] Task 1.6: Create `plugins/kanche/skills/graph-init-update/SKILL.md` (Refresh steering guidelines with updated knowledge graph).

### Tier 2: Enhanced Skills & Compatibility Wrappers
- [x] Task 2.1: Enhance `plugins/kanche/skills/planner-tasks/SKILL.md` to formally support Topological Dependency Tiers.
- [x] Task 2.2: Enhance `plugins/kanche/skills/qa-validate/SKILL.md` to incorporate the Graph Health Integrity Gate.
- [x] Task 2.3: Convert legacy SDD skills into backward-compatible forwarding wrappers:
  - `plugins/kanche/skills/sdd-run/SKILL.md` -> wraps `graph-run`
  - `plugins/kanche/skills/sdd-continue/SKILL.md` -> wraps `graph-continue`
  - `plugins/kanche/skills/sdd-steering/SKILL.md` -> wraps `graph-steering`
  - `plugins/kanche/skills/sdd-sync/SKILL.md` -> wraps `graph-sync`
  - `plugins/kanche/skills/sdd-init/SKILL.md` -> wraps `graph-init`
  - `plugins/kanche/skills/sdd-init-update/SKILL.md` -> wraps `graph-init-update`

### Tier 3: Showcase UI & Permanent Product Memory
- [x] Task 3.1: Create permanent domain product memory in `.docs/product/graph/specs.md` and `.docs/product/graph/design.md`.
- [x] Task 3.2: Update `.docs/product/sdd/specs.md` and `.docs/product/sdd/design.md` noting migration to Graph Engineering Workflow.
- [x] Task 3.3: Update `index.html` showcase dashboard to feature the Graph Engineering Workflow tab, updated visual pipeline, and command catalog.
- [x] Task 3.4: Update `README.md` with complete documentation for the Graph Engineering Workflow and command reference.

### Verification Checkpoints
- [x] Verify all JSON manifests parse cleanly with zero syntax errors.
- [x] Verify all YAML frontmatters across all `SKILL.md` files match standard schema.
- [x] Verify `index.html` renders valid HTML and loads all commands.
