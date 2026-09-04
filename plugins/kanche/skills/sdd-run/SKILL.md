---
name: sdd-run
description: Drive a feature work item through the full SDD phase model (P0 to P9) orchestrating all 16 specialized agents and 40 skills.
model: flash
---

# /kanche:sdd-run

**Summary.** Drive a work item through the complete SDD phase model (P0→P9), orchestrating the full 16-agent autonomous software engineering team and 40 skills across the software development lifecycle: codebase research, backlog PBI registration, specs drafting, system architecture & StitchMCP UI designs, task manifests, QA test plans, specialized frontend/backend implementation, deep code reviews, automated validations & Playwright MCP browser checks, security vulnerability scanning, GitHub PR review-respond loops with JSON inline comments, product memory promotion, gated human verification, and PR merge with release tagging. All destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) strictly require human confirmation. Supports `/goal` persistent execution mode.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description (e.g. `improve-sdd-plugins` or `auth-oauth2`). If absent, prompt the user for it to construct the folder path `.docs/development/{slug}/`.
- **`--mode=auto|manual`** — default **auto**. Also accept a bare `auto`/`manual` positional.
  - **auto:** run the entire workflow (P0→P9) straight through, automatically performing non-destructive steps (research, specs, design, tasks, code generation, lint, tests, PR comment analysis). Whenever reaching a destructive command (`git push`, `git commit`, `rm -rf`, `gh pr merge`), STOP and prompt the human for confirmation per `plugins/kanche/rules/destructive-safety.md`.
  - **manual:** before advancing to each next phase, ask "Proceed to `<next phase>`? [Yes|No]". "No" stops the walk cleanly (state where it stopped).
- **`--goal` / `/goal`** — enable goal-driven persistent execution mode for long-running or overnight tasks. The workflow continuously self-audits, automatically retries failed steps up to policy limits, and appends `<!-- GOAL_COMPLETE -->` upon full completion.
- **`--from=<phase>`** — start the walk at this phase instead of P0 (`P0`..`P9`, or a name like `design`/`build`). Phases before it are assumed already done; do not re-run them.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 AI-validation, P6 deploy, and Level 2 entirely. Bound both ends: never run outside `[from, until]`.

If `--from`/`--until` are inconsistent (from > until), stop and report.

## Phase Model (Full Team & 40 Skills Orchestration)

```text
LEVEL 1 (AI: P0 - P7)
P0 setup & research     @researcher (/kanche:sdd-steering) → @scrum-master (/kanche:scrum-pbi-create) → @git-operator (Receipt → /kanche:git-branch-create)
P1 specs                @analyst & @scrum-master (/kanche:design-grill → loop ≤3x [/kanche:design-specs → /kanche:design-specs-review])
P2 design & visuals     @architect & @designer (loop ≤3x [/kanche:design-init & /kanche:ui-design-stitch → /kanche:design-review])
P3 tasks & test plan    @planner & @tester (loop ≤3x [/kanche:planner-tasks & /kanche:qa-test-plan → /kanche:planner-review]) → Docs Commit (Gated /kanche:git-commit)
P4 build & review       @coder, @frontend-expert, @backend-expert (loop ≤3x [/kanche:code-implement → @reviewer /kanche:code-review & /kanche:qa-review]) → Implementation Commit (Gated /kanche:git-commit)
P5 validation & sec.    @validator, @tester, @security-engineer (/kanche:security-scan → /kanche:qa-validate & 3x self-healing fix loop)
P6 deploy & PR loop     @devops & @gh-operator (Gated /kanche:git-push → Gated /kanche:gh-cli-pr-create → loop ≤3x [/kanche:gh-cli-pr-review → /kanche:gh-cli-pr-respond → Gated /kanche:git-commit → Gated /kanche:git-push])
P7 align & sync         @gh-operator & @git-operator (/kanche:sdd-sync → Gated dev folder cleanup → Gated /kanche:git-commit → Gated /kanche:git-push)

LEVEL 2 (Human: P8 - P9)
P8 human review         @validator & @tester (gated interactive verification checklist via /kanche:qa-validate)
P9 PR merge & release   @devops & @gh-operator (Gated /kanche:gh-cli-pr-merge → optional release tag /kanche:git-tag-create / /kanche:git-tag-push)
```

## Goal Mode Protocol (`/goal`)

When `--goal` or `/goal` is passed:
1. **Persistent Execution:** Do not abort on transient errors; attempt up to 3 automatic remediation loops for failed validations or code reviews.
2. **Self-Auditing:** Audit all output files (`.docs/development/{slug}/*`, implementation diffs, test logs) before moving across phase boundaries.
3. **Safety Invariants:** All destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) remain strictly gated by human confirmation.
4. **Completion Marker:** Upon successfully completing the workflow, append `<!-- GOAL_COMPLETE -->` to the final summary output.

---

## Detailed Phase Execution

### P0 — Preconditions, Discovery & Setup

1. **Verify Git Repo.**
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "NOT_A_GIT_REPO"
   ```
2. **Survey Codebase & Steering Guidelines.** Delegate to `@researcher` to run `/kanche:sdd-steering` if `.docs/guidelines/` does not exist or requires refresh.
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

### P1 — Requirements & Specs Loop (≤3x Loop)

1. **Adversarial Probing.** Delegate to `@analyst` to probe feature ambiguities via `/kanche:design-grill`.
2. **Draft Functional Specifications.** Delegate to `@analyst` (assisted by `@scrum-master`) to write `.docs/development/{slug}/specs.md` via `/kanche:design-specs`.
3. **Forced Specs Review.** Delegate to `@analyst` to audit specs against guidelines via `/kanche:design-specs-review`, emitting `review-verdict` verdict.
   - On `NO-GO`, apply targeted delta fixes and re-evaluate (up to 3x).

---

### P2 — System Architecture & UI/UX Design Loop (≤3x Loop)

1. **Architecture & Schema Design.** Delegate to `@architect` to draft `.docs/development/{slug}/design.md`, `api-diff.md`, and `db-diff.md` via `/kanche:design-init`.
2. **Visual UI Screens & Design Tokens.** Delegate to `@designer` to generate screen wireframes, UI themes, and design tokens using StitchMCP via `/kanche:ui-design-stitch`.
3. **Forced Design Review.** Delegate to `@architect` to audit architecture, contracts, and visual specs via `/kanche:design-review`, emitting `review-verdict` verdict.
   - On `NO-GO`, apply targeted delta fixes and re-evaluate (up to 3x).

---

### P3 — Task Manifest & QA Test Plan Matrix

1. **Task Manifest Breakdown.** Delegate to `@planner` to decompose approved designs into ordered, checkable items in `.docs/development/{slug}/tasks.md` via `/kanche:planner-tasks`.
2. **Test Plan Specifications.** Delegate to `@tester` to formulate the test strategy, unit/integration stubs, and Playwright E2E visual matrices in `.docs/development/{slug}/test-plan.md` via `/kanche:qa-test-plan`.
3. **Forced Task Review.** Delegate to `@planner` to audit task order and criteria coverage via `/kanche:planner-review`.
4. **P3 Docs Commit Checkpoint (Human-Gated).** Delegate to `@git-operator` to run `/kanche:git-commit` with message `docs({slug}): add specs, design, test plan, and tasks`. Must prompt human for approval before committing.

---

### P4 — Implementation & Review Loop (≤3x Loop)

1. **Specialized Implementation Dispatch:**
   - **Frontend Tasks (`.ts`, `.tsx`, `.jsx`, `.vue`, CSS, UI components)**: Dispatched to `@frontend-expert`.
   - **Backend Tasks (`.php`, `.go`, `.py`, controllers, APIs, DB migrations)**: Dispatched to `@backend-expert`.
   - **General Tasks & Integration Logic**: Dispatched to `@coder`.
   All code changes are applied incrementally via `/kanche:code-implement` strictly adhering to `tasks.md` with minimal diffs.
2. **Forced Code & QA Review:**
   - Delegate to `@reviewer` to run deep code review and security checks via `/kanche:code-review`.
   - Delegate to `@validator` to audit visual and functional conformance via `/kanche:qa-review`.
   - On `NO-GO`, subagents perform targeted delta fixes and re-audit (up to 3x).
3. **P4 Implementation Commit Checkpoint (Human-Gated).** Delegate to `@git-operator` to run `/kanche:git-commit` with message `feat({slug}): implement feature logic and unit tests`. Must prompt human for approval before committing.

---

### P5 — AI Validation, Security Audit & Self-Healing Loop (≤3x Loop)

1. **Security Vulnerability Scan.** Delegate to `@security-engineer` to execute `/kanche:security-scan` (secrets scanning, dependency audit, OWASP patterns). Any critical blocker forces remediation.
2. **Comprehensive Validation Suite.** Delegate to `@validator` and `@tester` to run `/kanche:qa-validate`:
   - Unit & integration test runners.
   - MCP Playwright interactive browser checks & visual screenshot comparisons.
   - Chrome DevTools MCP accessibility (`a11y-debugging`) and performance (`debug-optimize-lcp`) audits.
3. **Self-Healing Repair Loop:** If validations fail, stack traces and error logs are automatically passed to `@coder` / `@frontend-expert` / `@backend-expert` via `/kanche:code-implement` for up to 3 repair iterations before human escalation.

---

### P6 — Deploy & AI PR Review-Respond Loop (≤3x Loop)

1. **Push Feature Branch (Human-Gated).** Run `/kanche:git-push` via `@git-operator` (prompts human confirmation).
2. **Open Pull Request (Human-Gated).** Run `/kanche:gh-cli-pr-create` via `@gh-operator` with auto-assignee `@me` (prompts human confirmation).
3. **AI PR Review & JSON Comment Submission.** Run `/kanche:gh-cli-pr-review` via `@gh-operator` & `@reviewer`:
   - Generates `review.json` payload.
   - Submits top-level review body (`#  Summary`, `## Review Summary`, `---`) and line-level inline comments in a single request via `gh api`.
4. **Automated PR Feedback Response Loop:** If review comments exist, execute `/kanche:gh-cli-pr-respond` → targeted code fixes → Gated `/kanche:git-commit` (`fix({slug}): address PR review feedback`) → Gated `/kanche:git-push` up to 3 times to resolve threads and push updates.

---

### P7 — Product Alignment & Doc Promotion (LEVEL 1 Final Step)

1. **Promote Documentation.** Run `/kanche:sdd-sync` via `@gh-operator`:
   - Consolidates dev docs into permanent domain directories (`.docs/product/{domain}/`).
   - Prompts human confirmation via `default_api:ask_question` before deleting ephemeral dev folder `.docs/development/{slug}/` via `rm -rf`.
   - Commits changes via Gated `/kanche:git-commit` (`docs({domain}): promote feature docs and sync product knowledge`).
   - Pushes updates via Gated `/kanche:git-push`.

---

### P8–P9 — Level 2 (Human Review & PR Merge)

1. **P8 Gated Human Review.** Delegate to `@validator` and `@tester` to present the interactive verification checklist and test evidence via `/kanche:qa-validate`.
2. **P9 PR Merge & Release Tagging (Human-Gated):**
   - Execute PR merge via `/kanche:gh-cli-pr-merge` upon human confirmation.
   - Optionally delegate to `@devops` to create and push annotated release tags via `/kanche:git-tag-create` and `/kanche:git-tag-push` upon human confirmation.

---

### 10. Notify User (P10)

Brief the user with a summary:
- Final status (Ready for Human Review & PR Merge, or Completed)
- Summary of documentation, implementation, and test suites executed
- Direct link to the open PR and feature logs
- Present P8 verification checklist and prompt for P9 PR merge
- Include `<!-- GOAL_COMPLETE -->` if `/goal` was active.

## Done when

- All in-bounds phases ran in order orchestrating the corresponding specialized subagents.
- All 16 agents and 40 skills participated across their respective phases.
- Zero autonomous destructive commands were executed — all commits, pushes, merges, and folder deletions were explicitly confirmed by the human.
- Product docs were promoted to domain directories in P7 (`.docs/product/{domain}/`).
- If `/goal` mode was requested, `<!-- GOAL_COMPLETE -->` tag is appended upon completion.
