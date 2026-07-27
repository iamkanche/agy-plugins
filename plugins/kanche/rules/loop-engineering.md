# Loop Engineering Protocol & Guidelines

## 1. Concept Definition
**Loop Engineering** is the systematic design pattern of paired, closed-loop execution cycles between a **Generator Skill** (producing artifacts/code) and a **Reviewer Skill** (evaluating quality/conformance). The loop executes iteratively until convergence (`verdict: GO`) or hitting the maximum iteration bound (`max_loops = 3`).

## 2. Skill Pairing Matrix
| SDD Phase | Initial / Reviewer Skill | Follow-up / Generator Skill | Target Artifact / Objective |
|---|---|---|---|
| P1 Specs | `/kanche:design-specs` (Gen) | `/kanche:design-specs-review` (Rev) | `specs.md` |
| P2 Design | `/kanche:design-init` (Gen) | `/kanche:design-review` (Rev) | `design.md`, `api-diff.md`, `db-diff.md` |
| P3 Tasks | `/kanche:planner-tasks` (Gen) | `/kanche:planner-review` (Rev) | `tasks.md` |
| P4 Build | `/kanche:code-implement` (Gen) | `/kanche:code-review` / `/kanche:qa-review` (Rev) | Source code & unit tests |
| P5 Validation | `/kanche:qa-validate` (Eval) | `/kanche:code-implement` (Fixer) | Test suite pass state |
| P6 PR Review | `/kanche:gh-cli-pr-review` (Step 1 Auditor) | `/kanche:gh-cli-pr-respond` (Step 2 Fixer/Responder) | PR audit comments & automated code fix response |


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

## 4. Closed-Loop Iteration Rules
1. **Initial Run (Iteration 1)**: Generator produces the initial artifact or code. Paired reviewer evaluates and returns `sdd-review`.
2. **Feedback Loop (Iterations 2..N, N <= max_loops)**:
   - If verdict is `NO-GO`, the Generator receives the previous `sdd-review` findings.
   - The Generator performs **Targeted Delta Fixes** — resolving reported `blocker` and `major` findings without altering unrelated code or introducing regressions.
   - Re-evaluate: Reviewer re-audits the updated artifact and diff.
3. **Termination & Convergence**:
   - **`GO` Verdict**: Achieved when `findings` contain 0 `blocker` and 0 `major` issues. Minor `nit` findings do not block `GO`.
   - **Max Loops Reached (3x)**: If iteration count reaches `max_loops` and verdict remains `NO-GO`, the loop terminates with an escalation report summarizing remaining blockers.
4. **Auto-Apply Policy**: When `--auto-apply` is specified, minor `nit` severity findings are auto-fixed by the reviewer or generator without triggering additional iteration loops.
