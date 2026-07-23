---
name: loop
description: Launch or resume the Loop Engineer automated inner feedback loop between Engineer and QA subagents (capped at 3 loops).
---

# /loop-engineer:run

**Summary.** Execute or resume the Loop Engineer automated inner feedback loop. The Loop Runner controller (`plugins/loop-engineer/scripts/loop-runner.js`) orchestrates up to 3 iterative cycles between `loop-engineer-agent` (code implementation & fix application) and `loop-qa-agent` (verification & code review), persisting state to `.sdd-docs/development/{feature_slug}/loop-log.json`.

## Inputs

Parse invocation arguments:

- `--feature=<feature_slug>` (required) — Feature slug identifier (e.g. `loop-engineer`).
- `--tasks=<task_ids>` (optional) — Specific task IDs or descriptions to target.
- `--max-loops=<n>` (optional, default: `3`) — Maximum iteration bound (hard capped at 3).
- `--resume` (optional) — Explicit flag to resume execution from existing `loop-log.json` checkpoint.

## Steps

1. **Verify workspace & feature directory.**
   Ensure `.sdd-docs/development/{feature_slug}/` exists. If missing, STOP and prompt the user to initialize feature docs first via `/sdd:init` or `/sdd:specs`.

2. **Invoke Loop Runner Controller.**
   Execute the Loop Runner controller script using Node.js:

   ```bash
   node plugins/loop-engineer/scripts/loop-runner.js --feature=<feature_slug> [--tasks=<task_ids>]
   ```

3. **Loop Execution Flow (up to 3 iterations):**
   - **Iteration Initialization**: Read or initialize `.sdd-docs/development/{feature_slug}/loop-log.json` with status `IN_PROGRESS`.
   - **Engineer Dispatch**: Invoke `loop-engineer-agent` with task specification and previous QA findings (if iteration > 1).
   - **QA Dispatch**: Invoke `loop-qa-agent` with implementation diff and test suite execution requirements (`npm run test:e2e`).
   - **Verdict & Schema Evaluation**:
     - `verdict: GO` $\rightarrow$ Set status `APPROVED`, log success, and terminate.
     - `verdict: NO-GO` and $N < 3$ $\rightarrow$ Extract structured findings and initiate iteration $N+1$.
     - `verdict: NO-GO` and $N = 3$ $\rightarrow$ Set status `MAX_LOOPS_EXCEEDED`, generate Escalation Report, and halt.
     - Invalid QA Schema / Empty Findings on `NO-GO` $\rightarrow$ Set status `QA_PROTOCOL_ERROR` and halt.
     - Timeout (>600s) or Unrecoverable Error $\rightarrow$ Set status `FATAL_ERROR` and halt.

4. **Report Outcome.**
   Present loop execution summary, including total iterations completed, final status, and path to `loop-log.json`.

## Data Models & Schema Rules

- State log location: `.sdd-docs/development/{feature_slug}/loop-log.json`.
- Max iteration limit: Strictly capped at 3 loops.
- QA Findings payload on `NO-GO` MUST include: `severity`, `file`, `line_range`, `message`, and `test_context`.

## Done when

- The loop execution reaches a terminal status (`APPROVED`, `MAX_LOOPS_EXCEEDED`, `QA_PROTOCOL_ERROR`, or `FATAL_ERROR`).
- Full execution telemetry is persisted to `.sdd-docs/development/{feature_slug}/loop-log.json`.
- A final summary report is returned to the outer caller.
