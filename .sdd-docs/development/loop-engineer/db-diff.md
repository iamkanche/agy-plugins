# Database Diff — Loop Engineer System

<!-- schema: db-diff | written by /sdd:design -->

## Schema Changes Overview

No SQL database schema modifications or migrations required.

## Persistent File State Deltas

The Loop Engineer System persists execution state in file-based JSON log storage:

- **Path**: `.sdd-docs/development/{feature_slug}/loop-log.json`
- **Format**: JSON matching `LoopExecutionLog` schema
- **State Entities**:
  - `LoopExecution`: Session header (`id`, `feature_slug`, `status`, `max_loops: 3`, `created_at`, `updated_at`)
  - `LoopIteration`: Iteration record (up to 3 items) containing `iteration`, `timestamp`, `engineer_summary`, `changed_files`, `qa_verdict`, `qa_findings`, `test_results`.
