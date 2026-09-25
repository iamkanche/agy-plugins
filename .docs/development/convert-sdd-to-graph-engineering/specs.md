# Functional Specifications: Convert SDD to Graph Engineering Workflow

## Context
Spec-Driven Development (SDD) in `agy-plugins` has successfully established a 16-agent autonomous engineering lifecycle across phases P0–P9. However, the current lifecycle operates predominantly on static Markdown documents (`specs.md`, `design.md`, `tasks.md`, `test-plan.md`) without structural awareness of the target repository's code graph. This introduces limitations:
- Surveys in P0 rely on file listing and regex checks rather than code AST/semantic relationships.
- Task planning in P3 generates linear checklists rather than dependency-ordered Directed Acyclic Graphs (DAGs).
- Validations in P5 run tests but cannot verify graph integrity (dangling endpoint references, missing imports, circular dependencies).
- Knowledge captured during feature implementation does not update the repository's permanent Knowledge Graph.

Converting SDD to a **Graph Engineering Workflow (GEW)** equips agents with structural graph reasoning across all lifecycle phases, grounded in AST/semantic knowledge graphs (`graphify`), topological DAG task execution, and graph integrity validation, while preserving full backward compatibility for `/kanche:sdd-*` commands.

## Scope
### In-Scope
1. **Graph Engineering Skill Family**: Create master orchestrator `/kanche:graph-run`, resume engine `/kanche:graph-continue`, repository survey `/kanche:graph-steering`, knowledge sync `/kanche:graph-sync`, and bootstrap/update skills `/kanche:graph-init` & `/kanche:graph-init-update`.
2. **Backward Compatibility**: Transform existing `/kanche:sdd-*` skills (`sdd-run`, `sdd-continue`, `sdd-steering`, `sdd-sync`, `sdd-init`, `sdd-init-update`) into transparent compatibility wrappers that forward directly to `/kanche:graph-*` with actionable migration notices.
3. **Topological Task Manifests**: Enhance `/kanche:planner-tasks` to generate ordered dependency DAGs with explicit execution tiers.
4. **Graph Health Integrity Gate**: Enhance `/kanche:qa-validate` to include AST/graph diagnostic audits (detecting dangling edges, missing endpoints, circular dependencies).
5. **Agent Capabilities**: Update subagent definitions (`@researcher`, `@architect`, `@planner`, `@validator`) with graph-aware system prompts and responsibilities.
6. **Documentation & Showcase**: Update `plugin.json` (bump to v0.4.0), `README.md`, `index.html` (interactive Graph Engineering pipeline), and establish `.docs/product/graph/`.

### Out-of-Scope / Non-Goals
- Modifying underlying standalone Git or GitHub CLI tools (`git-*`, `gh-cli-pr-*`).
- Altering the strict human-in-the-loop safety gating policy for destructive operations (`destructive-safety.md`).

## User Stories
1. **As an Antigravity AI Agent**, I want to execute `/kanche:graph-run` so that I can drive complex engineering tasks through a graph-grounded lifecycle with topological DAG task execution and graph health gates.
2. **As an Engineer with existing scripts or habits using `/kanche:sdd-run`**, I want legacy SDD commands to continue working seamlessly without syntax errors while informing me of the new Graph Engineering Workflow syntax.
3. **As a Software Architect**, I want `/kanche:graph-steering` to extract codebase entities and community hubs into structured guidelines so that implementation is grounded in the actual dependency graph.
4. **As a Quality Assurance Engineer**, I want `/kanche:qa-validate` to verify graph health alongside automated test suites to catch structural circular dependencies or dangling imports before deployment.

## Acceptance Criteria
1. **AC-1 (Skill Availability & Manifest)**: `plugins/kanche/skills/` contains `graph-run`, `graph-continue`, `graph-steering`, `graph-sync`, `graph-init`, and `graph-init-update` with valid YAML frontmatter and `model: flash`.
2. **AC-2 (Backward Compatibility)**: Existing SDD skills (`sdd-run`, `sdd-continue`, `sdd-steering`, `sdd-sync`, `sdd-init`, `sdd-init-update`) accept identical inputs/flags and seamlessly forward execution to their corresponding `graph-*` skills.
3. **AC-3 (Topological Task Planning)**: `/kanche:planner-tasks` produces task manifests partitioned into dependency tiers (Tier 0 to Tier N) based on component DAG order.
4. **AC-4 (Graph Integrity Diagnostics)**: `/kanche:qa-validate` includes an AST/graph diagnostic check for dangling endpoints, missing dependencies, and circular references.
5. **AC-5 (Safety Gating Preserved)**: All destructive commands (`git push`, `git commit`, `rm -rf`, `gh pr merge`) remain strictly gated behind interactive human confirmation via `default_api:ask_question`.
6. **AC-6 (Showcase & Documentation)**: `index.html` displays the Graph Engineering Workflow tab with interactive visual pipeline, and `README.md` documents all new and aliased commands.

## Data Model & Entity Specifications
- **Graph Node**: Represents an architectural entity (File, Class, Function, Interface, Component, Domain).
  - Attributes: `id`, `label`, `file_path`, `community_id`, `type`, `tier`.
- **Graph Edge**: Represents a structural or semantic relationship.
  - Attributes: `source`, `target`, `relation` (imports, calls, implements, defines, depends_on), `confidence` (EXTRACTED, INFERRED).
- **Task DAG Entity**:
  - Attributes: `task_id`, `tier` (0..N), `dependencies` (array of `task_id`), `action`, `file`, `status` (pending, done).

## Non-Functional Requirements (NFR)
- **Zero Regression**: All existing 40 skills and workflows must continue to execute without breaking changes.
- **Fast Execution**: All skills and subagents maintain `model: flash` (Gemini Flash High) for rapid execution.
- **Zero Autonomous Destructive Operations**: Strict compliance with `destructive-safety.md`.
- **Valid JSON & Markdown**: All JSON files (`plugin.json`, `agent.json`) and YAML frontmatters must pass strict parsing.

## Open Questions
- None; the design strategy of first-class `/kanche:graph-*` skills with transparent `/kanche:sdd-*` compatibility wrappers directly fulfills all backward compatibility and modern graph engineering requirements.
