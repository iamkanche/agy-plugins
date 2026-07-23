# API Diff — Loop Engineer System

<!-- schema: api-diff | written by /sdd:design -->

## Changes Overview

No external HTTP / OpenAPI REST endpoints added, modified, or removed.

## Subagent / CLI Interface Deltas

### 1. Slash Command Endpoint
- **Command**: `/loop-engineer:run`
- **Arguments**:
  - `--feature=<slug>` (Required: Feature slug, e.g., `loop-engineer`)
  - `--tasks=<task_ids>` (Optional: Specific task filter)
  - `--max-loops=3` (Optional: Overriding loop cap up to max 3)

### 2. Internal Subagent Interfaces

#### Engineer Subagent Contract (`loop-engineer-agent`)
- **Input**: `{ feature_slug, iteration, task_description, qa_findings_from_previous_loop }`
- **Output**: `{ status: "DONE" | "FAILED", engineer_summary: string, changed_files: string[] }`

#### QA Subagent Contract (`loop-qa-agent`)
- **Input**: `{ feature_slug, iteration, task_description, engineer_summary, changed_files, test_command }`
- **Output**: `{ verdict: "GO" | "NO-GO", test_results: { total, passed, failed, execution_time_ms }, findings: [ { severity, file, line_range, message, test_context } ] }`
