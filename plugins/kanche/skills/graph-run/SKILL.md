---
name: graph-run
description: Drive a feature work item through the 10-phase Graph Engineering Workflow (P0 to P9) orchestrating all 17 specialized agents and knowledge graph capabilities.
model: flash
---

# /kanche:graph-run

**Summary.** Drive a work item through the complete Graph Engineering Workflow (P0→P9), orchestrating the full 17-agent autonomous software engineering team: native AST discovery, backlog registration, impact subgraph specs, architecture topology, UI wireframes, topological task DAGs, QA test plans, specialized implementation, deep reviews, graph health checks, browser validations, security scans, token optimization, and PR lifecycle management. All destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) strictly require human confirmation per `rules/destructive-safety.md`. Supports `/goal` persistent execution mode.

## Inputs

- **slug** (optional, positional) — feature slug (e.g. `auth-oauth2`). If absent, prompt user for folder path `.docs/development/{slug}/`.
- **`--mode=auto|manual`** — default **auto**.
  - **auto:** run workflow (P0→P9), automatically executing non-destructive steps. Halt for confirmation before destructive commands (`git push`, `git commit`, `rm -rf`, `gh pr merge`).
  - **manual:** prompt "Proceed to `<next phase>`? [Yes|No]" before each phase.
- **`--goal` / `/goal`** — persistent execution mode. Automatically retries failed steps up to 3x, self-audits outputs, and appends `<!-- GOAL_COMPLETE -->` on full completion.
- **`--from=<phase>`** — start phase (`P0`..`P9`). Earlier phases assumed done.
- **`--until=<phase>`** — stop phase (inclusive). If `--until` < `build` (P4), skip P5-P9.

## Phase Model (Graph-Native Team Orchestration)

```text
LEVEL 1 (AI: P0 - P7)
P0 Graph Discovery      @researcher (/kanche:graph-steering) → @scrum-master (/kanche:scrum-pbi-create) → @git-operator (Receipt → /kanche:git-branch-create)
P1 Impact Subgraphs     @analyst & @scrum-master (/kanche:design-grill → loop ≤3x [/kanche:design-specs → /kanche:design-specs-review])
P2 Architecture & UI    @architect & @designer (loop ≤3x [/kanche:design-init & /kanche:ui-design-stitch → /kanche:design-review])
P3 Topological DAG      @planner & @tester (loop ≤3x [/kanche:planner-tasks & /kanche:qa-test-plan → /kanche:planner-review]) → Docs Commit (Gated /kanche:git-commit)
P4 Graph-Guided Build   @coder, @frontend-expert, @backend-expert, @token-optimizer (loop ≤3x [/kanche:code-implement → @reviewer /kanche:code-review & /kanche:qa-review]) → Implementation Commit (Gated /kanche:git-commit)
P5 Graph Health & QA    @validator, @tester, @security-engineer (/kanche:security-scan → /kanche:qa-validate & 3x self-healing fix loop)
P6 PR Blast Radius Loop @devops & @gh-operator (Gated /kanche:git-push → Gated /kanche:gh-cli-pr-create → loop ≤3x [/kanche:gh-cli-pr-review → /kanche:gh-cli-pr-respond → Gated /kanche:git-commit → Gated /kanche:git-push])
P7 Knowledge Graph Sync @gh-operator & @git-operator (/kanche:graph-sync → Gated dev folder cleanup → Gated /kanche:git-commit → Gated /kanche:git-push)

LEVEL 2 (Human: P8 - P9)
P8 Human Graph Review   @validator & @tester (gated interactive verification checklist via /kanche:qa-validate)
P9 PR Merge & Release   @devops & @gh-operator (Gated /kanche:gh-cli-pr-merge → optional release tag /kanche:git-tag-create / /kanche:git-tag-push)
```

## Goal Mode Protocol (`/goal`)

1. **Persistent Execution:** Do not abort on transient errors; run up to 3 automatic remediation loops for failed validations or reviews.
2. **Self-Auditing:** Audit all output files (`.docs/development/{slug}/*`, diffs, test logs, graph health reports) across phase boundaries.
3. **Safety Invariants:** All destructive operations remain strictly gated by human confirmation via `default_api:ask_question`.
4. **Completion Marker:** Append `<!-- GOAL_COMPLETE -->` to final summary on full completion.

---

## Detailed Phase Execution

### P0 — Knowledge Graph Discovery, Alignment & Setup
1. **Verify Git Repo:** Run `git rev-parse --is-inside-work-tree`.
2. **Steering Guidelines:** Delegate to `@researcher` to run `/kanche:graph-steering` if `.docs/guidelines/` is missing or stale.
3. **Product Backlog Item:** Delegate to `@scrum-master` to verify or create PBI under `.docs/backlog/{domain}/{PBI_ID}.md` via `/kanche:scrum-pbi-create`.
4. **Load Settings & Memory:** Read `.docs/settings.json` and `.docs/product/memory.md`.
5. **Feature Receipt:** Output Feature Slug, Title, Base Branch, Target Branch, Branch Name, and Mode.
6. **Checkout Branch:** Delegate to `@git-operator` to run `/kanche:git-branch-create` as `feat/{slug}`.

### P1 — Requirements & Impact Subgraph Specs Loop (≤3x Loop)
1. **Adversarial Probing:** Delegate to `@analyst` to probe ambiguities via `/kanche:design-grill`.
2. **Functional Specifications:** Delegate to `@analyst` & `@scrum-master` to write `.docs/development/{slug}/specs.md` via `/kanche:design-specs`.
3. **Specs Review:** Delegate to `@analyst` to audit specs via `/kanche:design-specs-review`, emitting `review-verdict`. On `NO-GO`, apply delta fixes (≤3x).

### P2 — Graph Architecture Topology & UI/UX Design Loop (≤3x Loop)
1. **Architecture Design:** Delegate to `@architect` to draft `.docs/development/{slug}/design.md`, `api-diff.md`, and `db-diff.md` via `/kanche:design-init`.
2. **UI Screens & Design Tokens:** Delegate to `@designer` to generate wireframes and tokens via `/kanche:ui-design-stitch`.
3. **Design Review:** Delegate to `@architect` to audit architecture via `/kanche:design-review`, emitting `review-verdict`. On `NO-GO`, refine (≤3x).

### P3 — Topological Task DAG & QA Test Plan Matrix
1. **Topological Task DAG:** Delegate to `@planner` to decompose design into ordered dependency tiers in `.docs/development/{slug}/tasks.md` via `/kanche:planner-tasks`.
2. **Test Plan Specifications:** Delegate to `@tester` to formulate test matrix in `.docs/development/{slug}/test-plan.md` via `/kanche:qa-test-plan`.
3. **Task Review:** Delegate to `@planner` to audit task order and criteria via `/kanche:planner-review`.
4. **Docs Commit Checkpoint (Human-Gated):** Delegate to `@git-operator` to run `/kanche:git-commit` (`docs({slug}): add specs, design, test plan, and tasks`). Must prompt human before committing.

### P4 — Graph-Guided Implementation & Review Loop (≤3x Loop)
1. **Specialized Implementation Dispatch:**
   - Frontend (`.ts`, `.tsx`, `.jsx`, `.vue`, CSS): Dispatched to `@frontend-expert`.
   - Backend (`.php`, `.go`, `.py`, APIs, migrations): Dispatched to `@backend-expert`.
   - Token & Prompt Distillation: Dispatched to `@token-optimizer` via `/kanche:token-optimize`.
   - General Tasks & Integration: Dispatched to `@coder`.
   Apply changes incrementally via `/kanche:code-implement` strictly adhering to `tasks.md` DAG tier ordering.
2. **Code & QA Review:**
   - Delegate to `@reviewer` for deep review and security checks via `/kanche:code-review`.
   - Delegate to `@validator` for conformance via `/kanche:qa-review`.
   - On `NO-GO`, perform targeted fixes and re-audit (≤3x).
3. **Implementation Commit Checkpoint (Human-Gated):** Delegate to `@git-operator` to run `/kanche:git-commit` (`feat({slug}): implement feature logic and unit tests`). Must prompt human before committing.

### P5 — Graph Health Integrity Gate & AI Validation Loop (≤3x Loop)
1. **Security Vulnerability Scan:** Delegate to `@security-engineer` to execute `/kanche:security-scan`.
2. **Graph Health Gate & Comprehensive Validation:** Delegate to `@validator` and `@tester` to run `/kanche:qa-validate` (AST diagnostics, test runners, Playwright browser checks, a11y & LCP audits).
3. **Self-Healing Loop:** If validations fail, pass stack traces to `@coder` / `@frontend-expert` / `@backend-expert` via `/kanche:code-implement` for up to 3 repair iterations.

### P6 — Deploy & PR Blast Radius Loop (≤3x Loop)
1. **Push Feature Branch (Human-Gated):** Run `/kanche:git-push` via `@git-operator` (prompts human).
2. **Open Pull Request (Human-Gated):** Run `/kanche:gh-cli-pr-create` via `@gh-operator` (prompts human).
3. **AI PR Review:** Run `/kanche:gh-cli-pr-review` via `@gh-operator` & `@reviewer` (submits inline comments and top-level summary via `gh api`).
4. **PR Feedback Response Loop:** If review comments exist, run `/kanche:gh-cli-pr-respond` → targeted fixes → Gated commit → Gated push (≤3x).

### P7 — Knowledge Graph Memory Promotion & Cache Sync (LEVEL 1 Final Step)
1. **Promote Docs & Sync Graph:** Run `/kanche:graph-sync` via `@gh-operator`.
2. **Dev Folder Cleanup (Human-Gated):** Prompt human confirmation via `default_api:ask_question` before deleting `.docs/development/{slug}/` via `rm -rf`.
3. **Docs Promotion Commit (Human-Gated):** Gated `/kanche:git-commit` (`docs({domain}): promote feature docs and sync knowledge graph`).
4. **Push Updates (Human-Gated):** Gated `/kanche:git-push`.

### P8–P9 — Level 2 (Human Review & PR Merge)
1. **P8 Gated Human Review:** Delegate to `@validator` and `@tester` to present interactive verification checklist and test logs via `/kanche:qa-validate`.
2. **P9 PR Merge & Release Tagging (Human-Gated):**
   - Execute PR merge via `/kanche:gh-cli-pr-merge` upon human confirmation.
   - Optionally delegate to `@devops` for release tags via `/kanche:git-tag-create` and `/kanche:git-tag-push` upon confirmation.

### 10. Notify User (P10)
Brief user with final status, links, and append `<!-- GOAL_COMPLETE -->` if `/goal` was active.

## Done when

- All in-bounds phases ran in order orchestrating corresponding specialized subagents.
- All 17 agents participated across their respective phases with graph-native awareness.
- Zero autonomous destructive commands were executed — all commits, pushes, merges, and folder deletions explicitly confirmed by human.
- Codebase Knowledge Graph and product docs promoted to domain directories in P7 (`.docs/product/{domain}/`).
- If `/goal` mode was requested, `<!-- GOAL_COMPLETE -->` tag is appended upon completion.
