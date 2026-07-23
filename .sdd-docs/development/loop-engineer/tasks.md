# Loop Engineer System — Tasks Checklist

<!-- schema: tasks | written by /sdd:tasks -->

## Phase 1: Plugin Manifest & Directory Structure

- [ ] **Phase 1.1: Create Plugin Manifest**
  - Path: `plugins/loop-engineer/plugin.json`
  - Implement plugin manifest registering `loop-engineer` metadata (version `0.1.0`), description, subagents (`agents/engineer/agent.json`, `agents/qa/agent.json`), and skills directory (`skills`).
  - *Traceability*: Design Component 1 (`plugins/loop-engineer/plugin.json`)

- [ ] **Phase 1.2: Register Plugin in Marketplace Registry** [P]
  - Path: `.agents/plugins/marketplace.json`
  - Add `loop-engineer` entry mapping plugin name to its directory source for local plugin discovery and registration.
  - *Traceability*: Design Component 1, Guidelines (`tech.md`)

---

## Phase 2: Subagent Definitions & Prompts

- [ ] **Phase 2.1: Define Loop Engineer Subagent** [P]
  - Path: `plugins/loop-engineer/agents/engineer/agent.json`
  - Implement configuration for `loop-engineer-agent` with system prompt for code implementation, applying targeted QA fixes, enabling write tools, and returning structured JSON `EngineerOutput`.
  - *Traceability*: AC 1, AC 2, Design Component 4, Design Section 4

- [ ] **Phase 2.2: Define Loop QA Subagent** [P]
  - Path: `plugins/loop-engineer/agents/qa/agent.json`
  - Implement configuration for `loop-qa-agent` with system prompt for verifying implementations via test suites (`npm run test:e2e`), code review, enabling write/MCP tools, and returning structured JSON `QAOutput` (`GO`/`NO-GO` verdict + line-item findings).
  - *Traceability*: AC 1, AC 2, AC 4, Design Component 5, Design Section 5

---

## Phase 3: Loop Command Skill

- [ ] **Phase 3.1: Create Loop Command Skill Specification**
  - Path: `plugins/loop-engineer/skills/loop/SKILL.md`
  - Define slash command `/loop-engineer:run` with parameters (`--feature=<slug>`, `--tasks=<task_ids>`, `--max-loops=3`) to initiate or resume the inner feedback loop.
  - *Traceability*: Design Component 2 (`plugins/loop-engineer/skills/loop/SKILL.md`)

---

## Phase 4: Loop Runner Controller Script

- [ ] **Phase 4.1: Implement State Machine & Log Persistence**
  - Path: `plugins/loop-engineer/scripts/loop-runner.js`
  - Build `LoopExecution` state manager that reads/writes persistent state to `.sdd-docs/development/{feature_slug}/loop-log.json`, creating iteration records and maintaining status (`IN_PROGRESS`, `APPROVED`, `MAX_LOOPS_EXCEEDED`, `QA_PROTOCOL_ERROR`, `FATAL_ERROR`).
  - *Traceability*: AC 6, NFR 2, Design Component 3

- [ ] **Phase 4.2: Implement Schema Validation Module**
  - Path: `plugins/loop-engineer/scripts/loop-runner.js`
  - Add JSON Schema validation logic for QA feedback payload and persistent logs; trap empty findings or missing fields on `NO-GO` verdict and set status to `QA_PROTOCOL_ERROR`.
  - *Traceability*: AC 4, Design Component 3, Design Section 6

- [ ] **Phase 4.3: Implement Subagent Invocation & Timeout Wrapper**
  - Path: `plugins/loop-engineer/scripts/loop-runner.js`
  - Implement async process dispatch wrapper for subagents (`loop-engineer-agent` and `loop-qa-agent`) with 600s execution timeout enforcement and fatal error handlers (`FATAL_ERROR`).
  - *Traceability*: AC 5, NFR 3, Design Component 3

- [ ] **Phase 4.4: Implement Inner Feedback Loop Controller**
  - Path: `plugins/loop-engineer/scripts/loop-runner.js`
  - Implement execution loop capped at 3 iterations: invoke Engineer (passing QA findings from loop $N-1$), invoke QA, evaluate verdict (`GO` -> exit `APPROVED`, `NO-GO` at $N=3$ -> exit `MAX_LOOPS_EXCEEDED`).
  - *Traceability*: AC 1, AC 2, AC 3, NFR 1, Design Component 3

---

## Phase 5: Integration & Unit Tests

- [ ] **Phase 5.1: Create Test Harness & Unit Tests**
  - Path: `tests/loop-engineer.spec.js`
  - Create test suite covering:
    1. First-Pass Approval (`GO` on Loop 1 -> `APPROVED`)
    2. Iterative Remediation (`NO-GO` on Loop 1, fix applied, `GO` on Loop 2 -> `APPROVED`)
    3. Maximum Iterations Capping (`NO-GO` on Loops 1..3 -> `MAX_LOOPS_EXCEEDED`)
    4. QA Protocol Error Handling (empty findings on `NO-GO` -> `QA_PROTOCOL_ERROR`)
    5. Fatal Environment Failure / Timeout handling (>600s -> `FATAL_ERROR`)
    6. Idempotent State Recovery (resume from `loop-log.json` checkpoint)
  - *Traceability*: AC 1, AC 2, AC 3, AC 4, AC 5, AC 6, Design Section 7

---

## Phase 6: Documentation & README

- [ ] **Phase 6.1: Write Plugin Documentation** [P]
  - Path: `plugins/loop-engineer/README.md`
  - Create comprehensive README covering Loop Engineer System architecture, subagent contracts, slash command usage `/loop-engineer:run`, state persistence format, and troubleshooting guidelines.
  - *Traceability*: Design Components 1-5

---

## Verification

### Verification Commands
```bash
# Run unit and integration tests for loop-runner controller
node tests/loop-engineer.spec.js

# Run Playwright / E2E verification suite across plugins
npm run test:e2e
```

### Acceptance Criteria Coverage Matrix

| Acceptance Criterion | Description | Test Check / Verification Task | Status |
| :--- | :--- | :--- | :--- |
| **AC 1** | First-Pass Approval (`GO` on Loop 1 -> `APPROVED`) | `tests/loop-engineer.spec.js` - Case 1 | Covered |
| **AC 2** | Iterative Remediation (`NO-GO` -> fix -> `GO` on Loop 2) | `tests/loop-engineer.spec.js` - Case 2 | Covered |
| **AC 3** | Max Iterations Cap (3 Loops Exceeded -> `MAX_LOOPS_EXCEEDED`) | `tests/loop-engineer.spec.js` - Case 3 | Covered |
| **AC 4** | Empty QA Findings / Schema Error (`QA_PROTOCOL_ERROR`) | `tests/loop-engineer.spec.js` - Case 4 | Covered |
| **AC 5** | Fatal Environment Failure / Timeout 600s (`FATAL_ERROR`) | `tests/loop-engineer.spec.js` - Case 5 | Covered |
| **AC 6** | Idempotent State Recovery from `loop-log.json` | `tests/loop-engineer.spec.js` - Case 6 | Covered |

---

## Tasks Review Verdict

```sdd-review
verdict: GO
findings: []
```

### Review Rationale
- **Coverage**: Every component in `design.md` and every acceptance criterion (AC 1 to AC 6) from `specs.md` has dedicated implementation and test verification tasks.
- **Ordering**: Logical, incremental order from plugin structure -> subagents -> skill -> controller logic -> unit/integration tests -> documentation.
- **Sizing & Clarity**: Each task is single-outcome, concrete, explicitly names target file path(s), and references traceability to specs/design.
- **Traceability**: All tasks map to specific acceptance criteria, NFRs, or design components.
- **Verification Section**: Includes exact test execution commands and full AC coverage mapping table.
