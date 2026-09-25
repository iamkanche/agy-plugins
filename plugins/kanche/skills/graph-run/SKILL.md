---
name: graph-run
description: Drive a feature work item through the 10-phase Graph Engineering Workflow (P0 to P9) orchestrating all 16 specialized agents and knowledge graph capabilities.
model: flash
---

# /kanche:graph-run

**Summary.** Drive a work item through the complete Graph Engineering Workflow (P0→P9), orchestrating the full 16-agent autonomous software engineering team and native graph engineering skills across the software development lifecycle: native AST & module graph discovery, backlog PBI registration, impact subgraph specs drafting, system architecture topology & StitchMCP UI designs, topological DAG task manifests, QA test plans, specialized frontend/backend implementation in dependency order, deep code reviews, automated graph health diagnostics, Playwright MCP browser validations, security vulnerability scanning, GitHub PR review-respond loops with graph blast-radius analysis and JSON inline comments, persistent dependency graph memory promotion, gated human verification, and PR merge with release tagging. All destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) strictly require human confirmation. Supports `/goal` persistent execution mode.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description (e.g. `auth-oauth2` or `graph-pipeline`). If absent, prompt the user for it to construct the folder path `.docs/development/{slug}/`.
- **`--mode=auto|manual`** — default **auto**. Also accept a bare `auto`/`manual` positional.
  - **auto:** run the entire workflow (P0→P9) straight through, automatically performing non-destructive steps (knowledge graph extraction, specs, design, DAG tasks, code generation, lint, tests, PR comment analysis). Whenever reaching a destructive command (`git push`, `git commit`, `rm -rf`, `gh pr merge`), STOP and prompt the human for confirmation per `plugins/kanche/rules/destructive-safety.md`.
  - **manual:** before advancing to each next phase, ask "Proceed to `<next phase>`? [Yes|No]". "No" stops the walk cleanly (state where it stopped).
- **`--goal` / `/goal`** — enable goal-driven persistent execution mode for long-running or overnight tasks. The workflow continuously self-audits, automatically retries failed steps up to policy limits (3x), and appends `<!-- GOAL_COMPLETE -->` upon full completion.
- **`--from=<phase>`** — start the walk at this phase instead of P0 (`P0`..`P9`, or a name like `design`/`build`). Phases before it are assumed already done; do not re-run them.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 AI-validation, P6 deploy, and Level 2 entirely. Bound both ends: never run outside `[from, until]`.

If `--from`/`--until` are inconsistent (from > until), stop and report.

## Phase Model (Graph-Native Team Orchestration)

```text
LEVEL 1 (AI: P0 - P7)
P0 Graph Discovery      @researcher (/kanche:graph-steering) → @scrum-master (/kanche:scrum-pbi-create) → @git-operator (Receipt → /kanche:git-branch-create)
P1 Impact Subgraphs     @analyst & @scrum-master (/kanche:design-grill → loop ≤3x [/kanche:design-specs → /kanche:design-specs-review])
P2 Architecture & UI    @architect & @designer (loop ≤3x [/kanche:design-init & /kanche:ui-design-stitch → /kanche:design-review])
P3 Topological DAG      @planner & @tester (loop ≤3x [/kanche:planner-tasks & /kanche:qa-test-plan → /kanche:planner-review]) → Docs Commit (Gated /kanche:git-commit)
P4 Graph-Guided Build   @coder, @frontend-expert, @backend-expert (loop ≤3x [/kanche:code-implement → @reviewer /kanche:code-review & /kanche:qa-review]) → Implementation Commit (Gated /kanche:git-commit)
P5 Graph Health & QA    @validator, @tester, @security-engineer (/kanche:security-scan → /kanche:qa-validate & 3x self-healing fix loop)
P6 PR Blast Radius Loop @devops & @gh-operator (Gated /kanche:git-push → Gated /kanche:gh-cli-pr-create → loop ≤3x [/kanche:gh-cli-pr-review → /kanche:gh-cli-pr-respond → Gated /kanche:git-commit → Gated /kanche:git-push])
P7 Knowledge Graph Sync @gh-operator & @git-operator (/kanche:graph-sync → Gated dev folder cleanup → Gated /kanche:git-commit → Gated /kanche:git-push)

LEVEL 2 (Human: P8 - P9)
P8 Human Graph Review   @validator & @tester (gated interactive verification checklist via /kanche:qa-validate)
P9 PR Merge & Release   @devops & @gh-operator (Gated /kanche:gh-cli-pr-merge → optional release tag /kanche:git-tag-create / /kanche:git-tag-push)
```

## Goal Mode Protocol (`/goal`)

When `--goal` or `/goal` is passed:
1. **Persistent Execution:** Do not abort on transient errors; attempt up to 3 automatic remediation loops for failed validations or code reviews.
2. **Self-Auditing:** Audit all output files (`.docs/development/{slug}/*`, implementation diffs, test logs, graph health reports) before moving across phase boundaries.
3. **Safety Invariants:** All destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) remain strictly gated by human confirmation.
4. **Completion Marker:** Upon successfully completing the workflow, append `<!-- GOAL_COMPLETE -->` to the final summary output.

---

## Detailed Phase Execution

### P0 — Knowledge Graph Discovery, Alignment & Setup

1. **Verify Git Repo.**
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "NOT_A_GIT_REPO"
   ```
2. **Native Graph Survey & Steering Guidelines.** Delegate to `@researcher` to run `/kanche:graph-steering` if `.docs/guidelines/` does not exist or requires refresh. Surveys AST dependencies, entry points, and module boundaries.
3. **Check/Register Product Backlog Item.** Delegate to `@scrum-master` to verify or create the corresponding PBI under `.docs/backlog/{domain}/{PBI_ID}.md` using `/kanche:scrum-pbi-create`.
4. **Load Settings & Memory.** Check if `.docs/settings.json` and `.docs/product/memory.md` exist to load project conventions and architectural constraints.
5. **Present Feature Receipt.** Generate a structured receipt for the user:
   - Feature Slug: `{slug}`
   - Feature Title: derived from backlog PBI or description
   - Base Branch: default remote branch (e.g. `main`)
   - Target PR Branch: default remote branch (e.g. `main`)
   - Branch Name: `feat/{slug}`
   - Execution Mode: `auto` or `manual`
6. **Checkout Feature Branch.** Delegate to `@git-operator` to run `/kanche:git-branch-create` as `feat/{slug}`.

---

### P1 — Requirements & Impact Subgraph Specs Loop (≤3x Loop)

1. **Adversarial Probing.** Delegate to `@analyst` to probe feature ambiguities and cross-community boundaries via `/kanche:design-grill`.
2. **Draft Functional Specifications.** Delegate to `@analyst` (assisted by `@scrum-master`) to write `.docs/development/{slug}/specs.md` via `/kanche:design-specs`. Explicitly document affected graph nodes, upstream callers, and downstream dependents.
3. **Forced Specs Review.** Delegate to `@analyst` to audit specs against guidelines via `/kanche:design-specs-review`, emitting `review-verdict` verdict.
   - On `NO-GO`, apply targeted delta fixes and re-evaluate (up to 3x).

---

### P2 — Graph Architecture Topology & UI/UX Design Loop (≤3x Loop)

1. **Architecture & Schema Design.** Delegate to `@architect` to draft `.docs/development/{slug}/design.md`, `api-diff.md`, and `db-diff.md` via `/kanche:design-init`, defining added/modified graph entities, contracts, and dependency boundaries.
2. **Visual UI Screens & Design Tokens.** Delegate to `@designer` to generate screen wireframes, UI themes, and design tokens using StitchMCP via `/kanche:ui-design-stitch`.
3. **Forced Design Review.** Delegate to `@architect` to audit architecture, contracts, and visual specs via `/kanche:design-review`, emitting `review-verdict` verdict.
   - On `NO-GO`, apply targeted delta fixes and re-evaluate (up to 3x).

---

### P3 — Topological Task DAG & QA Test Plan Matrix

1. **Topological Task DAG Decomposition.** Delegate to `@planner` to decompose approved designs into ordered dependency tiers (Tier 0: Models/Contracts → Tier 1: Services → Tier 2: UI/Endpoints → Tier 3: Tests/Docs) in `.docs/development/{slug}/tasks.md` via `/kanche:planner-tasks`.
2. **Test Plan Specifications.** Delegate to `@tester` to formulate the test strategy, unit/integration stubs, and Playwright E2E visual matrices in `.docs/development/{slug}/test-plan.md` via `/kanche:qa-test-plan`.
3. **Forced Task Review.** Delegate to `@planner` to audit task order and criteria coverage via `/kanche:planner-review`.
4. **P3 Docs Commit Checkpoint (Human-Gated).** Delegate to `@git-operator` to run `/kanche:git-commit` with message `docs({slug}): add specs, design, test plan, and tasks`. Must prompt human for approval before committing.

---

### P4 — Graph-Guided Implementation & Review Loop (≤3x Loop)

1. **Specialized Implementation Dispatch in DAG Order:**
   - **Frontend Tasks (`.ts`, `.tsx`, `.jsx`, `.vue`, CSS, UI components)**: Dispatched to `@frontend-expert`.
   - **Backend Tasks (`.php`, `.go`, `.py`, controllers, APIs, DB migrations)**: Dispatched to `@backend-expert`.
   - **General Tasks & Integration Logic**: Dispatched to `@coder`.
   All code changes are applied incrementally via `/kanche:code-implement` strictly adhering to `tasks.md` DAG tier ordering with minimal diffs.
2. **Forced Code & QA Review:**
   - Delegate to `@reviewer` to run deep code review and security checks via `/kanche:code-review`.
   - Delegate to `@validator` to audit visual and functional conformance via `/kanche:qa-review`.
   - On `NO-GO`, subagents perform targeted delta fixes and re-audit (up to 3x).
3. **P4 Implementation Commit Checkpoint (Human-Gated).** Delegate to `@git-operator` to run `/kanche:git-commit` with message `feat({slug}): implement feature logic and unit tests`. Must prompt human for approval before committing.

---

### P5 — Graph Health Integrity Gate & AI Validation Loop (≤3x Loop)

1. **Security Vulnerability Scan.** Delegate to `@security-engineer` to execute `/kanche:security-scan` (secrets scanning, dependency audit, OWASP patterns). Any critical blocker forces remediation.
2. **Graph Health Diagnostic Gate & Comprehensive Validation.** Delegate to `@validator` and `@tester` to run `/kanche:qa-validate`:
   - Non-destructive AST and Graph Health Diagnostics (verifying 0 dangling endpoint edges, 0 missing endpoints, and 0 circular dependencies).
   - Unit & integration test runners.
   - MCP Playwright interactive browser checks & visual screenshot comparisons.
   - Chrome DevTools MCP accessibility (`a11y-debugging`) and performance (`debug-optimize-lcp`) audits.
3. **Self-Healing Repair Loop:** If validations or graph diagnostics fail, stack traces and error logs are automatically passed to `@coder` / `@frontend-expert` / `@backend-expert` via `/kanche:code-implement` for up to 3 repair iterations before human escalation.

---

### P6 — Deploy & PR Blast Radius Loop (≤3x Loop)

1. **Push Feature Branch (Human-Gated).** Run `/kanche:git-push` via `@git-operator` (prompts human confirmation).
2. **Open Pull Request (Human-Gated).** Run `/kanche:gh-cli-pr-create` via `@gh-operator` with auto-assignee `@me` and Graph Blast Radius Summary (prompts human confirmation).
3. **AI PR Review & JSON Comment Submission.** Run `/kanche:gh-cli-pr-review` via `@gh-operator` & `@reviewer`:
   - Generates `review.json` payload.
   - Submits top-level review body (`#  Summary`, `## Review Summary`, `---`) and line-level inline comments in a single request via `gh api`.
4. **Automated PR Feedback Response Loop:** If review comments exist, execute `/kanche:gh-cli-pr-respond` → targeted code fixes → Gated `/kanche:git-commit` (`fix({slug}): address PR review feedback`) → Gated `/kanche:git-push` up to 3 times to resolve threads and push updates.

---

### P7 — Knowledge Graph Memory Promotion & Cache Sync (LEVEL 1 Final Step)

1. **Promote Documentation & Sync Knowledge Graph.** Run `/kanche:graph-sync` via `@gh-operator`:
   - Synchronizes codebase module dependencies and architectural entities.
   - Consolidates dev docs into permanent domain directories (`.docs/product/{domain}/`).
   - Prompts human confirmation via `default_api:ask_question` before deleting ephemeral dev folder `.docs/development/{slug}/` via `rm -rf`.
   - Commits changes via Gated `/kanche:git-commit` (`docs({domain}): promote feature docs and sync knowledge graph`).
   - Pushes updates via Gated `/kanche:git-push`.

---

### P8–P9 — Level 2 (Human Review & PR Merge)

1. **P8 Gated Human Review.** Delegate to `@validator` and `@tester` to present the interactive verification checklist, visual graph evidence, and test logs via `/kanche:qa-validate`.
2. **P9 PR Merge & Release Tagging (Human-Gated):**
   - Execute PR merge via `/kanche:gh-cli-pr-merge` upon human confirmation.
   - Optionally delegate to `@devops` to create and push annotated release tags via `/kanche:git-tag-create` and `/kanche:git-tag-push` upon human confirmation.

---

### 10. Notify User (P10)

Brief the user with a summary:
- Final status (Ready for Human Review & PR Merge, or Completed)
- Summary of documentation, topological implementation tiers, and test suites executed
- Direct link to the open PR and feature logs
- Present P8 verification checklist and prompt for P9 PR merge
- Include `<!-- GOAL_COMPLETE -->` if `/goal` was active.

## Done when

- All in-bounds phases ran in order orchestrating the corresponding specialized subagents.
- All 16 agents participated across their respective phases with graph-native awareness.
- Zero autonomous destructive commands were executed — all commits, pushes, merges, and folder deletions were explicitly confirmed by the human.
- Codebase Knowledge Graph and product docs were promoted to domain directories in P7 (`.docs/product/{domain}/`).
- If `/goal` mode was requested, `<!-- GOAL_COMPLETE -->` tag is appended upon completion.
