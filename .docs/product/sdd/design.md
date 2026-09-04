# SDD Workflows Design

## 1. System Architecture & Phase Progression (P0–P9)
The SDD workflow family orchestrates the full 16-agent autonomous software engineering team and 40 standalone skills:

### LEVEL 1: Autonomous AI Lifecycle (P0–P7)
- **P0 Discovery, Alignment & Setup**:
  - Codebase research & steering analysis via `@researcher` (`/kanche:sdd-steering`)
  - Backlog PBI verification/creation via `@scrum-master` (`/kanche:scrum-pbi-create`)
  - Structured receipt & feature branch creation via `@git-operator` (`/kanche:git-branch-create`)
- **P1 Functional Specifications (≤3x Loop)**:
  - Adversarial probing via `@analyst` (`/kanche:design-grill`)
  - Specs authoring via `@analyst` & `@scrum-master` (`/kanche:design-specs`)
  - Formal spec review via `@analyst` (`/kanche:design-specs-review` emitting `review-verdict`)
- **P2 Technical Architecture & UI Design (≤3x Loop)**:
  - Architecture, schema, and contracts via `@architect` (`/kanche:design-init`)
  - Visual wireframes, screens, and tokens via `@designer` (`/kanche:ui-design-stitch`)
  - System design review via `@architect` (`/kanche:design-review` emitting `review-verdict`)
- **P3 Task Manifest & QA Test Plan Matrix**:
  - Checkable task manifest via `@planner` (`/kanche:planner-tasks`)
  - E2E/visual test plan & stubs via `@tester` (`/kanche:qa-test-plan`)
  - Planning review via `@planner` (`/kanche:planner-review`)
  - Docs commit checkpoint via `@git-operator` (Human-Gated `/kanche:git-commit`)
- **P4 Build & Code Review Loop (≤3x Loop)**:
  - Incremental implementation via `@coder`, `@frontend-expert`, `@backend-expert` (`/kanche:code-implement`)
  - Static audit & quality review via `@reviewer` (`/kanche:code-review` & `/kanche:qa-review` emitting `review-verdict`)
  - Implementation commit checkpoint via `@git-operator` (Human-Gated `/kanche:git-commit`)
- **P5 Automated Validation & Security Audit**:
  - Security scanning via `@security-engineer` (`/kanche:security-scan`)
  - Automated test runs & Playwright MCP browser validation via `@validator` & `@tester` (`/kanche:qa-validate` with 3x repair loop)
- **P6 Deployment & GitHub PR Review Loop**:
  - Push branch via `@devops` (Human-Gated `/kanche:git-push`)
  - Open pull request via `@gh-operator` (Human-Gated `/kanche:gh-cli-pr-create`)
  - Autonomous review loop (≤3x): `@gh-operator` (`/kanche:gh-cli-pr-review` with `--json` format → `/kanche:gh-cli-pr-respond` → Gated `/kanche:git-commit` → Gated `/kanche:git-push`)
- **P7 Memory Promotion & Documentation Sync**:
  - Domain document synchronization via `@gh-operator` & `@git-operator` (`/kanche:sdd-sync`)
  - Active development folder cleanup (Human-Gated)
  - Documentation commit & push checkpoints (Human-Gated `/kanche:git-commit` & `/kanche:git-push`)

### LEVEL 2: Human-in-the-Loop Governance (P8–P9)
- **P8 Gated Human Verification**: Interactive verification checklist execution via `@validator` & `@tester` (`/kanche:qa-validate`).
- **P9 PR Merge & Release Tagging**: Gated pull request merge via `@devops` & `@gh-operator` (`/kanche:gh-cli-pr-merge`) with branch deletion and optional annotated tag creation (`/kanche:git-tag-create` / `/kanche:git-tag-push`).

## 2. File Organization
- Steering Guidelines: `.docs/guidelines/{product,tech,structure,rules}.md`
- Active Development: `.docs/development/{slug}/` (transient during feature build)
- Consolidated Product Memory: `.docs/product/{domain}/{specs,design}.md`
- Product Backlog: `.docs/backlog/{domain}/{PBI_ID}.md`

## 3. Communication & Decoupling Protocol
- All skills are isolated standalone capabilities that do not rely on orchestrator internals or auto-mode gate bypasses.
- Inter-skill review loops communicate through the universal `review-verdict` protocol block (`verdict: GO` | `NO-GO`).
- All 16 agents and 40 skills are configured with `model: flash` (Gemini Flash High).
