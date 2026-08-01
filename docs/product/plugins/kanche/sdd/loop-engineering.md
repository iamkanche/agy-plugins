# Loop Engineering Architecture Specification

## 1. Executive Overview
**Loop Engineering** is the foundational agentic design pattern of paired, closed-loop execution cycles between a **Generator Skill** (producing code or specifications) and an **Evaluator/Reviewer Skill** (auditing quality, testability, and rule adherence).

## 2. Core Architectural Pillars

### A. Closed-Loop Reciprocal Skill Pairs
Every generative workflow is explicitly bound to a complementary evaluator workflow:

```
+---------------------+       Generates Artifact       +------------------------+
|   Generator Skill   | -----------------------------> |     Reviewer Skill     |
| (e.g. code-implement|                                |  (e.g. code-review /   |
|   design-specs,     | <----------------------------- |      qa-review)        |
|   planner-tasks,    |   Structured sdd-review block  +------------------------+
|  ui-design-stitch)  |    (verdict, findings, line)
+---------------------+
```

### B. Standardized Machine-Readable Review Interface (`sdd-review`)
All reviewer skills produce a standardized `sdd-review` block:

```sdd-review
verdict: GO | NO-GO
loop_iteration: N / max_loops
findings:
  - severity: blocker | major | nit
    msg: "Clear description of failure or issue"
    file: "path/to/file"
    line: 123
    fix_suggestion: "Concrete repair recommendation"
```

### C. State Tracking & Delta Fixes (`loop-state.json`)
State per phase is tracked in `docs/development/{slug}/loop-state.json`. When iterating on `NO-GO` verdicts:
1. Generator reads the `findings` list.
2. Applies targeted delta modifications resolving reported `blocker` and `major` items.
3. Re-runs local verification commands to guarantee zero regressions against existing passing tests.

### D. Loop Governance, Self-Healing & Model Tiering
- **Maximum Loop Limit**: 3 iterations per phase.
- **Self-Healing P5 Validation**: Failing tests in P5 automatically feed stack traces back into P4 implementation for up to 3 repair cycles.
- **StitchMCP UI Design (P2)**: Autonomous UI design, design system generation, and screen variants via StitchMCP.
- **Playwright & Chrome DevTools MCP (P5)**: Live E2E browser automation and accessibility auditing (`a11y-debugging`).
- **Model Tiering**: `pro` for high-reasoning subagents (`@analyst`, `@architect`, `@validator`), `flash` for fast execution (`@coder`, `@planner`, `@git-operator`, `@gh-operator`).

## 3. Skill Pairing & Sequence Reference Matrix

| Phase | Step 1 (Primary Action) | Step 2 (Paired Feedback Action) | Target Artifact / Objective |
|---|---|---|---|
| P1 Specs | `/kanche:design-specs` (Generator) | `/kanche:design-specs-review` (Reviewer) | `specs.md` |
| P2 Design | `/kanche:design-init` & `/kanche:ui-design-stitch` (Generator) | `/kanche:design-review` (Reviewer) | `design.md`, `api-diff.md`, `db-diff.md` |
| P3 Tasks | `/kanche:planner-tasks` (Generator) | `/kanche:planner-review` (Reviewer) | `tasks.md` |
| P4 Build | `/kanche:code-implement` (Generator) | `/kanche:code-review` / `/kanche:qa-review` (Reviewer) | Source code & unit tests |
| P5 Validation | `/kanche:qa-validate` (Evaluator + Playwright/Chrome DevTools MCP) | `/kanche:code-implement` (Self-Healing Fixer) | Passing test suite |
| P6 PR Review | `/kanche:gh-cli-pr-review` (Step 1 Reviewer) | `/kanche:gh-cli-pr-respond` (Step 2 Fixer & Responder) | PR review audit & automated fix response loop |
