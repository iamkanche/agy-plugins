# Loop Engineering Protocol & Guidelines

## 1. Concept Definition
**Loop Engineering** is the systematic design pattern of paired, closed-loop execution cycles between a **Generator Skill** (producing artifacts/code) and a **Reviewer Skill** (evaluating quality/conformance). The loop executes iteratively until convergence (`verdict: GO`) or hitting the maximum iteration bound (`max_loops = 3`).

## 2. Skill Pairing Matrix
| SDD Phase | Initial / Generator Skill | Follow-up / Reviewer Skill | Target Artifact / Objective |
|---|---|---|---|
| P1 Specs | `/kanche:design-specs` (Gen) | `/kanche:design-specs-review` (Rev) | `specs.md` |
| P2 Design | `/kanche:design-init` & `/kanche:ui-design-stitch` (Gen) | `/kanche:design-review` (Rev) | `design.md`, `api-diff.md`, `db-diff.md` |
| P3 Tasks | `/kanche:planner-tasks` (Gen) | `/kanche:planner-review` (Rev) | `tasks.md` |
| P4 Build | `/kanche:code-implement` (Gen) | `/kanche:code-review` / `/kanche:qa-review` (Rev) | Source code & unit tests |
| P5 Validation | `/kanche:qa-validate` (Eval + Playwright/Chrome DevTools MCP) | `/kanche:code-implement` (Self-Healing Fixer) | Test suite pass state |
| P6 PR Review | `/kanche:gh-cli-pr-review` (Auditor) | `/kanche:gh-cli-pr-respond` (Fixer/Responder) | PR audit comments & automated code fix response |

## 3. Review Output Interface (`sdd-review` Block)
All reviewer skills MUST output a structured `sdd-review` fenced code block formatted as:

```sdd-review
verdict: GO | NO-GO
loop_iteration: <current_iteration>/<max_loops>
findings:
  - severity: blocker | major | nit
    msg: "<Clear, fixable description of the issue>"
    file: "<file_path>"
    line: <line_number>
    fix_suggestion: "<Actionable guidance for the generator>"
```

## 4. Closed-Loop Iteration & State Tracking (`loop-state.json`)
1. **Initial Run (Iteration 1)**: Generator produces the initial artifact or code. Paired reviewer evaluates and returns `sdd-review`.
2. **State Persistence**: The workflow updates `docs/development/{slug}/loop-state.json` recording phase iteration count and verdict status.
3. **Feedback Loop (Iterations 2..N, N <= max_loops)**:
   - If verdict is `NO-GO`, the Generator receives the previous `sdd-review` findings.
   - The Generator performs **Targeted Delta Fixes** — resolving reported `blocker` and `major` findings without altering unrelated code or introducing regressions.
   - Re-evaluate: Reviewer re-audits the updated artifact and diff.
4. **Termination & Convergence**:
   - **`GO` Verdict**: Achieved when `findings` contain 0 `blocker` and 0 `major` issues. Minor `nit` findings do not block `GO`.
   - **Max Loops Reached (3x)**: If iteration count reaches `max_loops` and verdict remains `NO-GO`, the loop terminates with an escalation report summarizing remaining blockers.
5. **Self-Healing P5 Validation Loop**: If P5 validation fails, the stack trace/error logs are automatically passed to `/kanche:code-implement` in P4 for up to 3 repair cycles before escalating.

## 5. Model Tiering Guidelines
- **High-Reasoning Tasks (`Model: pro`)**: Subagents performing investigación, architecture (`@architect`, `@analyst`), code reviews (`@reviewer`), and QA audits (`@quality_assurance`).
- **Fast Execution Tasks (`Model: flash`)**: Subagents performing code edits (`@coder`), task planning (`@planner`), and Git/GitHub operators (`@git-operator`, `@gh-operator`).
