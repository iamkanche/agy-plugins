# Loop Engineer Plugin (`plugins/loop-engineer`)

The **Loop Engineer System** automates iterative software development and verification in Google Antigravity (AGY). It establishes a closed-loop feedback mechanism between an **Engineer Agent** (`loop-engineer-agent`) and a **QA Agent** (`loop-qa-agent`), coordinated by the deterministic **Loop Runner Controller** (`scripts/loop-runner.js`).

---

## Key Features

1. **Inner Feedback Loop**: Automates code implementation, testing, code review, and targeted fix iterations.
2. **Hard Loop Bound (Max 3 Loops)**: Guarantees execution safety by capping iterations at a maximum of 3 cycles before escalation.
3. **Structured QA Protocol**: Requires precise JSON findings (`severity`, `file`, `line_range`, `message`, `test_context`) on `NO-GO` verdicts.
4. **Execution Safety & Timeout Enforcement**: Enforces a 600-second execution timeout per subagent dispatch to prevent hangs or deadlocks.
5. **Persistent State Log**: Saves complete session telemetry to `.sdd-docs/development/{feature_slug}/loop-log.json`, enabling idempotent state recovery.

---

## Plugin Architecture

```
plugins/loop-engineer/
├── plugin.json                 # Plugin manifest registering subagents & skills
├── README.md                   # Comprehensive plugin documentation
├── agents/
│   ├── engineer/
│   │   └── agent.json          # Engineer subagent definition (implementation & fix application)
│   └── qa/
│       └── agent.json          # QA subagent definition (test execution & code review)
├── skills/
│   └── loop/
│       └── SKILL.md            # Slash command /loop-engineer:run definition
└── scripts/
    └── loop-runner.js          # Controller managing state machine, timeouts, and JSON logging
```

---

## Subagent Contracts

### 1. Loop Engineer Agent (`loop-engineer-agent`)
- **Role**: Analyzes task requirements and QA findings from iteration $N-1$; performs code modifications in the workspace; returns execution summary and changed files.
- **Input Payload**:
  ```json
  {
    "feature_slug": "loop-engineer",
    "iteration": 2,
    "task_description": "Implement feature component",
    "qa_findings_from_previous_loop": [...]
  }
  ```
- **Output Payload**:
  ```json
  {
    "status": "DONE",
    "engineer_summary": "Applied targeted fix for line-item finding in loop-runner.js",
    "changed_files": ["plugins/loop-engineer/scripts/loop-runner.js"]
  }
  ```

### 2. Loop QA Agent (`loop-qa-agent`)
- **Role**: Executes verification tests (`npm run test:e2e`), conducts code reviews against project guidelines, and returns structured `GO` or `NO-GO` verdicts.
- **Input Payload**:
  ```json
  {
    "feature_slug": "loop-engineer",
    "iteration": 1,
    "engineer_summary": "Initial code implementation",
    "changed_files": ["..."],
    "test_command": "npm run test:e2e"
  }
  ```
- **Output Payload**:
  ```json
  {
    "verdict": "NO-GO",
    "test_results": { "total": 5, "passed": 4, "failed": 1, "execution_time_ms": 1200 },
    "findings": [
      {
        "severity": "major",
        "file": "plugins/loop-engineer/scripts/loop-runner.js",
        "line_range": "L45-L60",
        "message": "Missing timeout handling.",
        "test_context": "tests/loop-engineer.spec.js"
      }
    ]
  }
  ```

---

## Usage

### Slash Command

Launch or resume the inner feedback loop via slash command:

```bash
/loop-engineer:run --feature=<feature_slug> [--tasks=<task_ids>] [--max-loops=3]
```

### Direct CLI Execution

Run the controller script using Node.js:

```bash
node plugins/loop-engineer/scripts/loop-runner.js --feature=loop-engineer
```

### Programmatic API

```javascript
const { runLoop } = require('./plugins/loop-engineer/scripts/loop-runner.js');

const result = await runLoop({
  featureSlug: 'my-feature',
  taskDescription: 'Build UI components',
  maxLoops: 3
});

console.log('Result status:', result.status);
```

---

## State Machine & Status Codes

| Status | Description |
| :--- | :--- |
| `IN_PROGRESS` | Inner loop actively running cycles. |
| `APPROVED` | QA Agent issued `verdict: GO` within 3 loops. |
| `MAX_LOOPS_EXCEEDED` | Capped at 3 iterations without QA approval; escalated. |
| `QA_PROTOCOL_ERROR` | QA returned invalid schema or empty findings on `NO-GO`. |
| `FATAL_ERROR` | Subagent timeout (>600s) or unrecoverable system exception. |

---

## Telemetry & Logging

State is saved to `.sdd-docs/development/{feature_slug}/loop-log.json`:

```json
{
  "id": "c1f7a29e-4b71-482a-9e12-321456789abc",
  "feature_slug": "loop-engineer",
  "status": "APPROVED",
  "max_loops": 3,
  "created_at": "2026-07-23T22:50:00.000Z",
  "updated_at": "2026-07-23T22:52:00.000Z",
  "iterations": [...]
}
```
