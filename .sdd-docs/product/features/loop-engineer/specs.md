# Loop Engineer System — Specification

<!-- schema: specs | written by /sdd:specs -->

## Context
In autonomous software development workflows, feature implementations often require iterative cycles of development, testing, and feedback. Without a structured inner feedback loop, minor test failures or code quality regressions require human intervention or lead to incomplete tasks. 

The **Loop Engineer System** automates this iterative process by establishing a closed-loop collaboration between an **Engineer Agent** (implementation) and a **QA Agent** (verification & review). The Engineer implements code changes and submits them to QA; QA verifies the implementation against tests and rules; if issues are found, QA returns structured actionable feedback to the Engineer, who applies targeted fixes. This cycle repeats for up to a maximum of 3 iterations until QA issues a `GO` verdict or escalates.

## Scope

### In-Scope
- **Iterative Loop Engine**: Execution controller managing up to 3 iterative cycles between Engineer and QA subagents.
- **Engineer Agent Role**: Implementation of code, application of fixes based on QA feedback, and updating task completion state.
- **QA Agent Role**: Verification of code changes via test execution (e.g. unit/E2E test suites), code review against project guidelines/rules, and structured verdict generation (`GO` or `NO-GO` with line-item findings).
- **Feedback Protocol**: Standardized data schema for QA feedback passed to the Engineer on subsequent loops ($N+1$).
- **Termination & Escalation Handlers**: Clean termination on QA `GO`, escalation report generation on max iterations reached (3 loops), and early exit on fatal unrecoverable errors.
- **Loop State Logging**: Persistent JSON log tracking iteration counts, diff summaries, QA findings, test execution results, and final status.

### Out of Scope / Non-Goals
- Unlimited or infinite iteration loops (hard-capped at 3 iterations).
- Direct remote git pushing or PR merging within the inner loop (handled by outer SDD deployment/git plugins).
- Supporting non-Antigravity agent frameworks.

## User Stories

1. **Autonomous Feature Implementation**:
   - *As a* Lead Developer / SDD Orchestrator,
   - *I want* the system to automatically run an Engineer-QA feedback loop when executing build tasks,
   - *So that* minor bugs, lint errors, and test failures are automatically fixed without manual developer intervention.

2. **Structured QA Feedback**:
   - *As an* Engineer Agent,
   - *I want* to receive precise, structured QA feedback (failed test output, specific file locations, error tracebacks),
   - *So that* I can apply targeted fixes on subsequent iterations rather than repeating blind edits.

3. **Loop Bound & Safety Escalation**:
   - *As a* Project Stakeholder,
   - *I want* the loop execution to be capped at 3 iterations and escalate if unresolved,
   - *So that* agents do not waste resources or loop indefinitely on complex or unresolvable failures.

## Acceptance Criteria

### Happy Path
1. **First-Pass Approval**:
   - **Given** a feature task request,
   - **When** the Engineer Agent implements the code and passes verification on the first attempt,
   - **Then** the QA Agent issues a `verdict: GO` on loop 1, the loop terminates immediately with status `APPROVED`, and progress is logged.

2. **Iterative Remediation (Feedback & Fix)**:
   - **Given** an implementation that fails QA verification on loop 1 with specific test failures or review findings,
   - **When** QA returns `verdict: NO-GO` with structured findings,
   - **Then** the Loop Engineer system invokes the Engineer Agent for loop 2 with QA findings, the Engineer applies fixes, QA re-reviews, and if verified clean, QA issues `verdict: GO` on loop 2.

### Boundary & Edge Cases
3. **Maximum Iterations Capping (3 Loops)**:
   - **Given** an implementation that continues to fail QA review after 3 full iterations (loop 1, loop 2, loop 3),
   - **When** QA issues `verdict: NO-GO` on iteration 3,
   - **Then** the Loop Engineer system halts further iterations, marks status as `MAX_LOOPS_EXCEEDED`, logs an Escalation Summary detailing all 3 attempts, and escalates to human operator.

4. **Empty or Missing QA Findings**:
   - **Given** QA issues a `NO-GO` verdict without providing any actionable findings or error logs,
   - **When** the loop state is evaluated,
   - **Then** the system flags a QA schema error, logs the invalid response, and halts loop execution with status `QA_PROTOCOL_ERROR`.

5. **Fatal Environment / Build Failure**:
   - **Given** an unrecoverable failure during QA execution (e.g., missing dependencies, broken node runtime, environment error),
   - **When** detected by the QA runner,
   - **Then** the loop terminates immediately without consuming remaining loop attempts, setting status to `FATAL_ERROR`.

6. **Idempotent State Recovery**:
   - **Given** a loop execution interrupted mid-cycle (e.g., process termination),
   - **When** re-invoked with `/sdd:continue` or loop resume command,
   - **Then** the system reads the persistent `loop-log.json` state and resumes execution at the exact iteration and agent role recorded.

## Data Model

### Domain Entities

```
+-------------------+        1:N        +-------------------+
|  LoopExecution    |-------------------|   LoopIteration   |
+-------------------+                   +-------------------+
| id: string        |                   | iteration: int (1..3)
| feature_slug: str |                   | timestamp: string |
| status: Enum      |                   | engineer_summary: str
| max_loops: int(3) |                   | qa_verdict: Enum  |
| created_at: str   |                   | qa_findings: Array|
| updated_at: str   |                   | test_results: Obj |
+-------------------+                   +-------------------+
```

#### LoopExecution State Enum
- `IN_PROGRESS`: Loop execution active.
- `APPROVED`: QA returned `verdict: GO` within 3 loops.
- `MAX_LOOPS_EXCEEDED`: 3 loops completed without QA approval.
- `QA_PROTOCOL_ERROR`: QA response missing required structured findings.
- `FATAL_ERROR`: Unrecoverable environment or system failure.

#### QA Verdict Enum
- `GO`: Implementation meets all acceptance criteria and quality checks.
- `NO-GO`: Implementation has failing tests, regressions, or rule violations.

#### QA Finding Item Schema
- `severity`: `blocker` | `major` | `nit`
- `file`: string (absolute or relative file path)
- `line_range`: string (e.g., `L10-L25`)
- `message`: string (description of issue and expected fix)
- `test_context`: string (failing test name or log line)

## Non-Functional Requirements (NFR)

1. **Loop Limit Invariant**: The system MUST NEVER exceed 3 iterations under any circumstance. Capping logic is enforced at the controller level before subagent dispatch.
2. **Observability & Logging**: Every iteration MUST log structured JSON telemetry to `.sdd-docs/development/{feature_slug}/loop-log.json`, recording timestamps, changed files, QA verdicts, and iteration counts.
3. **Execution Timeout**: Each subagent invocation (Engineer or QA) MUST time out after 600 seconds to prevent deadlocks or hanging loops.
4. **Safety & Policy Invariants**: All code modifications applied during loops MUST adhere strictly to project rules (no secret additions, no force-push, standard gating rules).

## Open Questions

- *Q1: Should loop logs be cleaned up after sync?*
  - **Resolution**: No, `loop-log.json` is preserved in the development feature folder as an audit trail for quality assurance and model evaluation.

---

## Specs Review Verdict

```sdd-review
verdict: GO
findings: []
```

### Review Rationale
- **Structure**: All required SDD sections (Context, Scope, User stories, Acceptance criteria, Data model, NFR, Open questions) are completely defined.
- **Testability**: All 6 acceptance criteria use concrete Given/When/Then syntax and cover happy path, maximum iteration capping (3 loops), missing findings edge cases, fatal errors, and state recovery.
- **Coverage**: Maps directly to all user stories and enforces the feature goal (Engineer-QA inner loop capped at 3 iterations).
- **NFR**: Specific, measurable constraints on max loop count, execution timeouts (600s), logging format, and safety invariants.
- **Consistency**: Fully aligned with project rules in `.sdd-docs/guidelines/` and SDD gating conventions.
