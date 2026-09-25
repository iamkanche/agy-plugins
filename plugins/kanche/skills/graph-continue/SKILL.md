---
name: graph-continue
description: Resume the Graph Engineering Workflow at the phase inferred from on-disk graph state orchestrating the full 16-agent team.
model: flash
---

# /kanche:graph-continue

**Summary.** Resume the Graph Engineering Workflow at the phase inferred from on-disk graph state and development artifacts instead of starting fresh, orchestrating the full 16-agent team forward following the exact same loop rules and destructive safety gates as `/kanche:graph-run`. State every workflow you run before executing it.

## Inputs

Parse the arguments:

- **`--mode=auto|manual`** — default **auto**. Auto executes non-destructive steps and stops for human confirmation on all destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) per `plugins/kanche/rules/destructive-safety.md`. Manual prompts before advancing between phases.
- **`--from=<phase>`** — override detection and force the resume point (`P0`..`P9`).
- **`--until=<phase>`** — stop after this phase (inclusive).
- **slug** (optional, positional) — disambiguates when several dev folders exist.

## Steps

### 1. Detect current phase

Gather on-disk, graph, and repo signals:

```bash
# Guidelines & Knowledge Graph check
ls .docs/guidelines 2>/dev/null
[ -f "graphify-out/graph.json" ] && echo "GRAPH_EXISTS"

# Backlog PBIs check
ls .docs/backlog/*/*.md 2>/dev/null

# Feature folder + docs
FEAT=$(ls -dt .docs/development/*/ 2>/dev/null | head -1)
echo "feature_dir=$FEAT"
[ -n "$FEAT" ] && ls "$FEAT"                        # specs.md? design.md? tasks.md? test-plan.md?
[ -f "$FEAT/tasks.md" ] && grep -c -- '- \[ \]' "$FEAT/tasks.md"   # unchecked count
[ -f "$FEAT/tasks.md" ] && grep -c -- '- \[x\]' "$FEAT/tasks.md"   # checked count

# Branch / push / PR state
DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
DEFAULT=${DEFAULT:-main}
CURRENT=$(git rev-parse --abbrev-ref HEAD)
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "NO_UPSTREAM"
gh pr view --json state,number,mergedAt 2>/dev/null || echo "NO_PR"
ls .docs/product/ 2>/dev/null
```

Apply detection rules **in order**:

1. **No `.docs/guidelines/`** → steering missing. Delegate to `@researcher` to run `/kanche:graph-steering` and `/kanche:graph-init`.
2. **No feature folder** → resume at **P0/P1** (check backlog PBI with `@scrum-master`, ensure branch with `@git-operator`, then specs with `@analyst`).
3. **`specs.md` absent** → **P1** (`@analyst` `/kanche:design-specs`).
4. **`specs.md` present, `design.md` absent** → **P2** (`@architect` `/kanche:design-init` & `@designer` `/kanche:ui-design-stitch`).
5. **`design.md` present, `tasks.md` or `test-plan.md` absent** → **P3** (`@planner` `/kanche:planner-tasks` & `@tester` `/kanche:qa-test-plan`).
6. **`tasks.md` present with unchecked `- [ ]` items** → **P4 Build** (dispatch to `@frontend-expert`, `@backend-expert`, or `@coder` via `/kanche:code-implement` strictly along topological DAG tiers).
7. **All `tasks.md` items checked, unvalidated** → **P5 Validation** (`@security-engineer` `/kanche:security-scan` & `@validator` / `@tester` `/kanche:qa-validate` with Graph Health check).
8. **Validation complete, PR not open** → **P6 Deploy** (`@devops` Gated `/kanche:git-push`, `@gh-operator` Gated `/kanche:gh-cli-pr-create` with Graph Blast Radius Summary, and AI review-respond loop).
9. **P6 deploy complete, dev folder present** → **P7 Knowledge Graph Sync** (`@gh-operator` `/kanche:graph-sync` with gated dev folder cleanup).
10. **P7 complete and PR open** → **P8** (`@validator` verification checklist), then **P9** (`@devops` Gated `/kanche:gh-cli-pr-merge`).

### 2. Resume the walk

Execute remaining phases delegating to the specialized subagents of the 16-agent team:

- **P1 Specs & Impact Subgraphs**: `@analyst` & `@scrum-master` (`/kanche:design-grill` → loop ≤3x [`/kanche:design-specs` ↔ `/kanche:design-specs-review`]).
- **P2 Architecture & Visuals**: `@architect` & `@designer` (loop ≤3x [`/kanche:design-init` & `/kanche:ui-design-stitch` ↔ `/kanche:design-review`]).
- **P3 Topological DAG Tasks & Test Plan**: `@planner` & `@tester` (loop ≤3x [`/kanche:planner-tasks` & `/kanche:qa-test-plan` ↔ `/kanche:planner-review`]) → Gated Docs Commit (`/kanche:git-commit`).
- **P4 Graph-Guided Build & Review**: Routing to `@frontend-expert` (TS/React/CSS), `@backend-expert` (Laravel/APIs/DB), or `@coder` (loop ≤3x [`/kanche:code-implement` in DAG order ↔ `@reviewer` `/kanche:code-review` & `/kanche:qa-review`]) → Gated Implementation Commit (`/kanche:git-commit`).
- **P5 Graph Health & Validation**: `@security-engineer` (`/kanche:security-scan`) & `@validator`/`@tester` (`/kanche:qa-validate` with Graph Health check, Playwright MCP / Chrome DevTools MCP and 3x self-healing fix loop).
- **P6 Deploy & PR Blast Radius Loop**: `@devops` & `@gh-operator` (Gated `/kanche:git-push` → Gated `/kanche:gh-cli-pr-create` → loop ≤3x [`/kanche:gh-cli-pr-review` ↔ `/kanche:gh-cli-pr-respond` → Gated `/kanche:git-commit` → Gated `/kanche:git-push`]).
- **P7 Knowledge Graph Sync & Alignment**: `@gh-operator` (`/kanche:graph-sync` with gated folder deletion → Gated `/kanche:git-commit` → Gated `/kanche:git-push`).
- **P8 Human Review**: `@validator` & `@tester` (interactive verification matrix & graph inspection).
- **P9 PR Merge & Release**: `@devops` & `@gh-operator` (Gated `/kanche:gh-cli-pr-merge` → optional release tagging via `/kanche:git-tag-create` / `/kanche:git-tag-push`).

## Rules

- Destructive operations (`git push`, `git commit`, `rm -rf`, `gh pr merge`) always pause and prompt the human for explicit confirmation.
- Subagent delegation and graph grounding are maintained across all resumed phases.
