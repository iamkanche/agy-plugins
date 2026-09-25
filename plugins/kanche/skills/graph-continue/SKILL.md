---
name: graph-continue
description: Resume the Graph Engineering Workflow at the phase inferred from on-disk graph state orchestrating the full 17-agent team.
model: flash
---

# /kanche:graph-continue

**Summary.** Resume the Graph Engineering Workflow at the phase inferred from on-disk state, orchestrating the 17-agent team forward under `rules/destructive-safety.md`.

## Inputs

- **`--mode=auto|manual`** — default **auto**. Auto executes non-destructive steps and stops for confirmation before destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`).
- **`--from=<phase>`** — override detection and force resume phase (`P0`..`P9`).
- **`--until=<phase>`** — stop after phase (inclusive).
- **slug** (optional, positional) — target dev folder.

## Steps

### 1. Detect Current Phase

Evaluate signals in order:
1. **No `.docs/guidelines/`** → **P0** (delegate to `@researcher` for `/kanche:graph-steering`).
2. **No feature folder** → **P0/P1** (check backlog PBI via `@scrum-master`, branch via `@git-operator`, specs via `@analyst`).
3. **`specs.md` absent** → **P1** (`@analyst` `/kanche:design-specs`).
4. **`specs.md` present, `design.md` absent** → **P2** (`@architect` `/kanche:design-init` & `@designer` `/kanche:ui-design-stitch`).
5. **`design.md` present, `tasks.md` or `test-plan.md` absent** → **P3** (`@planner` `/kanche:planner-tasks` & `@tester` `/kanche:qa-test-plan`).
6. **`tasks.md` present with unchecked `- [ ]` items** → **P4 Build** (dispatch to `@frontend-expert`, `@backend-expert`, `@token-optimizer`, or `@coder` via `/kanche:code-implement`).
7. **All `tasks.md` items checked, unvalidated** → **P5 Validation** (`@security-engineer` `/kanche:security-scan` & `@validator` / `@tester` `/kanche:qa-validate`).
8. **Validation complete, PR not open** → **P6 Deploy** (`@devops` Gated `/kanche:git-push`, `@gh-operator` Gated `/kanche:gh-cli-pr-create`, and AI review-respond loop).
9. **P6 deploy complete, dev folder present** → **P7 Graph Sync** (`@gh-operator` `/kanche:graph-sync` with gated dev folder cleanup).
10. **P7 complete and PR open** → **P8** (`@validator` checklist), then **P9** (`@devops` Gated `/kanche:gh-cli-pr-merge`).

### 2. Resume Workflow

Resume remaining phases delegating to the 17-agent team:
- **P1 Specs**: `@analyst` & `@scrum-master` (`/kanche:design-grill` → loop ≤3x [`/kanche:design-specs` ↔ `/kanche:design-specs-review`]).
- **P2 Architecture**: `@architect` & `@designer` (loop ≤3x [`/kanche:design-init` & `/kanche:ui-design-stitch` ↔ `/kanche:design-review`]).
- **P3 Task DAG & Test Plan**: `@planner` & `@tester` (loop ≤3x [`/kanche:planner-tasks` & `/kanche:qa-test-plan` ↔ `/kanche:planner-review`]) → Gated Docs Commit (`/kanche:git-commit`).
- **P4 Graph Build**: Routing to `@frontend-expert` (TS/React), `@backend-expert` (Laravel/APIs), `@token-optimizer` (prompts/context), or `@coder` (loop ≤3x [`/kanche:code-implement` in DAG order ↔ `@reviewer` `/kanche:code-review` & `/kanche:qa-review`]) → Gated Commit (`/kanche:git-commit`).
- **P5 Graph Health & Validation**: `@security-engineer` (`/kanche:security-scan`) & `@validator`/`@tester` (`/kanche:qa-validate` with Playwright MCP / DevTools MCP and 3x self-healing).
- **P6 Deploy & PR Loop**: `@devops` & `@gh-operator` (Gated push → Gated PR create → loop ≤3x [PR review ↔ PR respond → Gated commit → Gated push]).
- **P7 Graph Sync**: `@gh-operator` (`/kanche:graph-sync` with gated folder deletion → Gated commit → Gated push).
- **P8 Human Review**: `@validator` & `@tester` (interactive verification matrix).
- **P9 PR Merge & Release**: `@devops` & `@gh-operator` (Gated `/kanche:gh-cli-pr-merge` → optional release tagging via `/kanche:git-tag-*`).

## Rules

- Destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) always pause for explicit human confirmation.
- Subagent delegation and graph grounding are maintained across all resumed phases.
