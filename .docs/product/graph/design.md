# Graph Engineering Workflows Design

## 1. System Architecture & Phase Progression (P0–P9)
The Graph Engineering Workflow orchestrates the full 16-agent autonomous software engineering team and knowledge-graph-native skills:

### LEVEL 1: Autonomous AI Lifecycle (P0–P7)
- **P0 Graph Discovery & Ingestion**:
  - Codebase research & Knowledge Graph survey via `@researcher` (`/kanche:graph-steering`)
  - Backlog PBI verification/creation via `@scrum-master` (`/kanche:scrum-pbi-create`)
  - Structured receipt & feature branch creation via `@git-operator` (`/kanche:git-branch-create`)
- **P1 Impact Subgraph Specs (≤3x Loop)**:
  - Adversarial probing via `@analyst` (`/kanche:design-grill`)
  - Specs authoring via `@analyst` & `@scrum-master` (`/kanche:design-specs`) mapping affected graph nodes and contracts
  - Formal spec review via `@analyst` (`/kanche:design-specs-review` emitting `review-verdict`)
- **P2 Graph Architecture & UI Design (≤3x Loop)**:
  - Graph entity topology, contracts, and schema via `@architect` (`/kanche:design-init`)
  - Visual wireframes, screens, and tokens via `@designer` (`/kanche:ui-design-stitch`)
  - System design review via `@architect` (`/kanche:design-review` emitting `review-verdict`)
- **P3 Topological Task DAG & QA Test Plan Matrix**:
  - Checkable task manifest in Topological Dependency Tiers via `@planner` (`/kanche:planner-tasks`)
  - E2E/visual test plan & stubs via `@tester` (`/kanche:qa-test-plan`)
  - Planning review via `@planner` (`/kanche:planner-review`)
  - Docs commit checkpoint via `@git-operator` (Human-Gated `/kanche:git-commit`)
- **P4 Graph-Guided Build & Code Review Loop (≤3x Loop)**:
  - Implementation in DAG dependency order via `@coder`, `@frontend-expert`, `@backend-expert` (`/kanche:code-implement`)
  - Quality review via `@reviewer` (`/kanche:code-review` & `/kanche:qa-review` emitting `review-verdict`)
  - Implementation commit checkpoint via `@git-operator` (Human-Gated `/kanche:git-commit`)
- **P5 Graph Health Diagnostics & Automated Validation**:
  - Graph integrity diagnostics (0 dangling edges, 0 circular dependencies) via `@validator` (`/kanche:qa-validate`)
  - Security scanning via `@security-engineer` (`/kanche:security-scan`)
  - Automated test runs & Playwright MCP browser validation with 3x self-healing repair loop
- **P6 Deployment & GitHub PR Review Loop**:
  - Push branch via `@devops` (Human-Gated `/kanche:git-push`)
  - Open pull request with Graph Blast Radius summary via `@gh-operator` (Human-Gated `/kanche:gh-cli-pr-create`)
  - Autonomous review loop (≤3x): `@gh-operator` (`/kanche:gh-cli-pr-review` with `--json` format → `/kanche:gh-cli-pr-respond` → Gated `/kanche:git-commit` → Gated `/kanche:git-push`)
- **P7 Knowledge Graph Sync & Memory Promotion**:
  - Incremental Knowledge Graph update (`graphify --update`) and domain doc sync via `@gh-operator` & `@git-operator` (`/kanche:graph-sync`)
  - Active development folder cleanup (Human-Gated)
  - Documentation commit & push checkpoints (Human-Gated `/kanche:git-commit` & `/kanche:git-push`)

### LEVEL 2: Human-in-the-Loop Governance (P8–P9)
- **P8 Gated Human Verification**: Interactive verification checklist execution & graph inspection via `@validator` & `@tester` (`/kanche:qa-validate`).
- **P9 PR Merge & Release Tagging**: Gated pull request merge via `@devops` & `@gh-operator` (`/kanche:gh-cli-pr-merge`) with branch deletion and optional annotated tag creation (`/kanche:git-tag-create` / `/kanche:git-tag-push`).

## 2. File Organization
- Steering Guidelines: `.docs/guidelines/{product,tech,structure,rules}.md`
- Active Development: `.docs/development/{slug}/` (transient during feature build)
- Consolidated Product Memory: `.docs/product/{domain}/{specs,design}.md`
- Product Backlog: `.docs/backlog/{domain}/{PBI_ID}.md`
- Knowledge Graph Artifacts: `graphify-out/{graph.json,graph.html,GRAPH_REPORT.md}`

## 3. Communication & Decoupling Protocol
- All skills are isolated standalone capabilities that do not rely on orchestrator internals or auto-mode gate bypasses.
- Inter-skill review loops communicate through the universal `review-verdict` protocol block (`verdict: GO` | `NO-GO`).
- All 16 agents and skills are configured with `model: flash` (Gemini Flash High).
