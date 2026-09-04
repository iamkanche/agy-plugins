# Loop Engineering Protocol & Guidelines

## 1. Concept Definition
**Loop Engineering** is the systematic design pattern of paired, closed-loop execution cycles between a **Generator Skill** (producing artifacts/code) and a **Reviewer Skill** (evaluating quality/conformance). The loop executes iteratively until convergence (`verdict: GO`) or hitting the maximum iteration bound (`max_loops = 3`).

## 2. Skill Pairing Matrix
| Engineering Phase | Specialized Agents | Generator / Primary Skill | Reviewer / Evaluator Skill | Target Artifact / Objective |
|---|---|---|---|---|
| **Discovery** | `@researcher`, `@scrum-master` | `/kanche:sdd-steering` & `/kanche:scrum-pbi-create` | Steering audit / Backlog verification | `.docs/guidelines/*`, `.docs/backlog/*` |
| **Specs** | `@analyst`, `@scrum-master` | `/kanche:design-specs` (Gen) | `/kanche:design-specs-review` (Rev) | `specs.md` |
| **Design** | `@architect`, `@designer` | `/kanche:design-init` & `/kanche:ui-design-stitch` (Gen) | `/kanche:design-review` (Rev) | `design.md`, `api-diff.md`, Stitch UI |
| **Tasks** | `@planner`, `@tester` | `/kanche:planner-tasks` & `/kanche:qa-test-plan` (Gen) | `/kanche:planner-review` (Rev) | `tasks.md`, `test-plan.md` |
| **Build** | `@coder`, `@frontend-expert`, `@backend-expert` | `/kanche:code-implement` (Gen) | `@reviewer` `/kanche:code-review` & `/kanche:qa-review` | Source code & unit tests |
| **Validation** | `@validator`, `@tester`, `@security-engineer` | `/kanche:qa-validate` & `/kanche:security-scan` | `/kanche:code-implement` (Self-Healing Fixer) | Green test suites & zero security flaws |
| **PR Review** | `@devops`, `@gh-operator`, `@reviewer` | `/kanche:gh-cli-pr-review` (Auditor) | `/kanche:gh-cli-pr-respond` (Fixer/Responder) | PR audit comments & automated fixes |
| **Alignment** | `@gh-operator`, `@git-operator` | `/kanche:sdd-sync` (Promoter) | Memory & doc-drift auditor | `.docs/product/{domain}/*` |


## 3. Review Output Interface (`review-verdict` Block)
All reviewer skills MUST output a structured `review-verdict` fenced code block formatted as:

```review-verdict
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
1. **Initial Run (Iteration 1)**: Generator produces the initial artifact or code. Paired reviewer evaluates and returns `review-verdict`.
2. **State Persistence**: The workflow updates `.docs/development/{slug}/loop-state.json` recording phase iteration count and verdict status.
3. **Feedback Loop (Iterations 2..N, N <= max_loops)**:
   - If verdict is `NO-GO`, the Generator receives the previous `review-verdict` findings.
   - The Generator performs **Targeted Delta Fixes** — resolving reported `blocker` and `major` findings without altering unrelated code or introducing regressions.
   - Re-evaluate: Reviewer re-audits the updated artifact and diff.
4. **Termination & Convergence**:
   - **`GO` Verdict**: Achieved when `findings` contain 0 `blocker` and 0 `major` issues. Minor `nit` findings do not block `GO`.
   - **Max Loops Reached (3x)**: If iteration count reaches `max_loops` and verdict remains `NO-GO`, the loop terminates with an escalation report summarizing remaining blockers.
5. **Self-Healing P5 Validation Loop**: If P5 validation fails, the stack trace/error logs are automatically passed to `/kanche:code-implement` in P4 for up to 3 repair cycles before escalating.

## 5. Subagent Model Tiering (Gemini Flash High)

The subagent engineering team runs unified on the latest **Gemini Flash (High)** model tier (`model: flash`), providing lightning-fast inference, low latency, and high-quality reasoning across all 16 roles:
- **Research & Architecture**: `@researcher`, `@analyst`, `@architect`, `@designer`
- **Implementation Specialists**: `@coder`, `@frontend-expert`, `@backend-expert`
- **Quality & Security**: `@reviewer`, `@validator`, `@tester`, `@security-engineer`
- **Agile & Platform Operations**: `@scrum-master`, `@planner`, `@devops`, `@git-operator`, `@gh-operator`

> 🛑 **Safety Boundary**: Regardless of agent model tier or automated loops, all destructive and remote-mutating commands (`git push`, `git commit`, `rm`, branch deletion, tag deletion, stash drop, PR merge) MUST halt and prompt the human for explicit confirmation per `plugins/kanche/rules/destructive-safety.md`.


