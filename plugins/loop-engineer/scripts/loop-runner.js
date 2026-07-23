/**
 * Loop Runner Controller
 * Path: plugins/loop-engineer/scripts/loop-runner.js
 *
 * State machine execution controller managing up to 3 iterative cycles
 * between loop-engineer-agent and loop-qa-agent.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const MAX_LOOPS = 3;
const SUBAGENT_TIMEOUT_MS = 600000; // 600 seconds

const Status = {
  IN_PROGRESS: 'IN_PROGRESS',
  APPROVED: 'APPROVED',
  MAX_LOOPS_EXCEEDED: 'MAX_LOOPS_EXCEEDED',
  QA_PROTOCOL_ERROR: 'QA_PROTOCOL_ERROR',
  FATAL_ERROR: 'FATAL_ERROR'
};

const Verdict = {
  GO: 'GO',
  NO_GO: 'NO-GO'
};

const Severity = {
  BLOCKER: 'blocker',
  MAJOR: 'major',
  NIT: 'nit'
};

/**
 * Validates structured QA feedback payload against schema requirements.
 * @param {object} payload
 * @returns {{ valid: boolean, error?: string }}
 */
function validateQAFeedback(payload) {
  if (!payload || typeof payload !== 'object') {
    return { valid: false, error: 'QA feedback payload must be a non-null object.' };
  }

  if (payload.verdict !== Verdict.GO && payload.verdict !== Verdict.NO_GO) {
    return { valid: false, error: `Invalid verdict "${payload.verdict}". Must be "GO" or "NO-GO".` };
  }

  if (!payload.test_results || typeof payload.test_results !== 'object') {
    return { valid: false, error: 'QA feedback must include a test_results object.' };
  }

  const { total, passed, failed } = payload.test_results;
  if (typeof total !== 'number' || typeof passed !== 'number' || typeof failed !== 'number') {
    return { valid: false, error: 'test_results must contain numeric total, passed, and failed counts.' };
  }

  if (!Array.isArray(payload.findings)) {
    return { valid: false, error: 'QA feedback must include a findings array.' };
  }

  if (payload.verdict === Verdict.NO_GO) {
    if (payload.findings.length === 0) {
      return { valid: false, error: 'QA NO-GO verdict must contain at least one structured finding.' };
    }

    for (let i = 0; i < payload.findings.length; i++) {
      const item = payload.findings[i];
      if (!item || typeof item !== 'object') {
        return { valid: false, error: `Finding at index ${i} is not an object.` };
      }

      if (![Severity.BLOCKER, Severity.MAJOR, Severity.NIT].includes(item.severity)) {
        return { valid: false, error: `Finding at index ${i} has invalid severity "${item.severity}".` };
      }

      if (typeof item.file !== 'string' || !item.file) {
        return { valid: false, error: `Finding at index ${i} is missing a valid file path.` };
      }

      if (typeof item.line_range !== 'string') {
        return { valid: false, error: `Finding at index ${i} is missing a valid line_range string.` };
      }

      if (typeof item.message !== 'string' || !item.message) {
        return { valid: false, error: `Finding at index ${i} is missing a valid message string.` };
      }

      if (typeof item.test_context !== 'string') {
        return { valid: false, error: `Finding at index ${i} is missing a valid test_context string.` };
      }
    }
  }

  return { valid: true };
}

/**
 * Validates persistent loop log structure.
 * @param {object} logData
 * @returns {{ valid: boolean, error?: string }}
 */
function validateLoopLog(logData) {
  if (!logData || typeof logData !== 'object') {
    return { valid: false, error: 'Loop log must be a non-null object.' };
  }

  if (!logData.id || typeof logData.id !== 'string') {
    return { valid: false, error: 'Loop log missing valid id string.' };
  }

  if (!logData.feature_slug || typeof logData.feature_slug !== 'string') {
    return { valid: false, error: 'Loop log missing valid feature_slug string.' };
  }

  if (!Object.values(Status).includes(logData.status)) {
    return { valid: false, error: `Invalid status "${logData.status}" in loop log.` };
  }

  if (logData.max_loops !== MAX_LOOPS) {
    return { valid: false, error: `max_loops must equal ${MAX_LOOPS}.` };
  }

  if (!Array.isArray(logData.iterations) || logData.iterations.length > MAX_LOOPS) {
    return { valid: false, error: `iterations must be an array with max ${MAX_LOOPS} items.` };
  }

  return { valid: true };
}

/**
 * Helper to wrap subagent calls with a 600-second timeout.
 * @param {Function} subagentFn
 * @param {object} args
 * @param {number} timeoutMs
 */
async function invokeSubagentWithTimeout(subagentFn, args, timeoutMs = SUBAGENT_TIMEOUT_MS) {
  return new Promise((resolve, reject) => {
    let timer = setTimeout(() => {
      timer = null;
      reject(new Error(`Subagent invocation timed out after ${timeoutMs / 1000}s.`));
    }, timeoutMs);

    subagentFn(args)
      .then((result) => {
        if (timer) {
          clearTimeout(timer);
          resolve(result);
        }
      })
      .catch((err) => {
        if (timer) {
          clearTimeout(timer);
          reject(err);
        }
      });
  });
}

/**
 * Default mock / fallback Engineer runner for standalone CLI or testing.
 */
async function defaultEngineerRunner(input) {
  return {
    status: 'DONE',
    engineer_summary: `Implemented changes for iteration ${input.iteration}.`,
    changed_files: ['plugins/loop-engineer/scripts/loop-runner.js']
  };
}

/**
 * Default mock / fallback QA runner for standalone CLI or testing.
 */
async function defaultQARunner(input) {
  return {
    verdict: Verdict.GO,
    test_results: {
      total: 10,
      passed: 10,
      failed: 0,
      execution_time_ms: 1500
    },
    findings: []
  };
}

/**
 * Main Loop Execution Function
 * @param {object} options
 * @returns {Promise<{ status: string, log: object, error?: string }>}
 */
async function runLoop(options = {}) {
  const {
    featureSlug = 'loop-engineer',
    taskDescription = 'Execute build task',
    testCommand = 'npm run test:e2e',
    maxLoops = MAX_LOOPS,
    baseDir = process.cwd(),
    timeoutMs = SUBAGENT_TIMEOUT_MS,
    engineerRunner = defaultEngineerRunner,
    qaRunner = defaultQARunner
  } = options;

  const docDir = path.join(baseDir, '.sdd-docs', 'development', featureSlug);
  if (!fs.existsSync(docDir)) {
    fs.mkdirSync(docDir, { recursive: true });
  }

  const logFilePath = path.join(docDir, 'loop-log.json');
  let state;

  if (fs.existsSync(logFilePath)) {
    try {
      const raw = fs.readFileSync(logFilePath, 'utf8');
      state = JSON.parse(raw);
    } catch (e) {
      state = null;
    }
  }

  if (!state || typeof state !== 'object' || !state.id) {
    state = {
      id: crypto.randomUUID ? crypto.randomUUID() : `loop-${Date.now()}`,
      feature_slug: featureSlug,
      status: Status.IN_PROGRESS,
      max_loops: maxLoops,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      iterations: []
    };
  } else {
    // If state exists and was in a terminal state, return existing state
    if ([Status.APPROVED, Status.MAX_LOOPS_EXCEEDED, Status.QA_PROTOCOL_ERROR, Status.FATAL_ERROR].includes(state.status)) {
      return { status: state.status, log: state };
    }
    state.status = Status.IN_PROGRESS;
  }

  const saveState = () => {
    state.updated_at = new Date().toISOString();
    fs.writeFileSync(logFilePath, JSON.stringify(state, null, 2), 'utf8');
  };

  saveState();

  let startIteration = state.iterations.length + 1;
  let previousQAFindings = [];

  if (state.iterations.length > 0) {
    const lastIter = state.iterations[state.iterations.length - 1];
    previousQAFindings = lastIter.qa_findings || [];
  }

  for (let iter = startIteration; iter <= maxLoops; iter++) {
    let engOutput;
    try {
      engOutput = await invokeSubagentWithTimeout(
        engineerRunner,
        {
          feature_slug: featureSlug,
          iteration: iter,
          task_description: taskDescription,
          qa_findings_from_previous_loop: previousQAFindings
        },
        timeoutMs
      );
    } catch (err) {
      state.status = Status.FATAL_ERROR;
      saveState();
      return { status: Status.FATAL_ERROR, log: state, error: `Engineer Agent error: ${err.message}` };
    }

    let qaOutput;
    try {
      qaOutput = await invokeSubagentWithTimeout(
        qaRunner,
        {
          feature_slug: featureSlug,
          iteration: iter,
          task_description: taskDescription,
          engineer_summary: engOutput ? engOutput.engineer_summary : '',
          changed_files: engOutput ? engOutput.changed_files : [],
          test_command: testCommand
        },
        timeoutMs
      );
    } catch (err) {
      state.status = Status.FATAL_ERROR;
      saveState();
      return { status: Status.FATAL_ERROR, log: state, error: `QA Agent error: ${err.message}` };
    }

    const validation = validateQAFeedback(qaOutput);
    if (!validation.valid) {
      state.status = Status.QA_PROTOCOL_ERROR;
      saveState();
      return { status: Status.QA_PROTOCOL_ERROR, log: state, error: validation.error };
    }

    const iterationRecord = {
      iteration: iter,
      timestamp: new Date().toISOString(),
      engineer_summary: engOutput ? engOutput.engineer_summary : '',
      changed_files: engOutput ? engOutput.changed_files || [] : [],
      qa_verdict: qaOutput.verdict,
      qa_findings: qaOutput.findings || [],
      test_results: qaOutput.test_results
    };

    state.iterations.push(iterationRecord);

    if (qaOutput.verdict === Verdict.GO) {
      state.status = Status.APPROVED;
      saveState();
      return { status: Status.APPROVED, log: state };
    }

    if (qaOutput.verdict === Verdict.NO_GO) {
      previousQAFindings = qaOutput.findings;
      if (iter >= maxLoops) {
        state.status = Status.MAX_LOOPS_EXCEEDED;
        saveState();
        return { status: Status.MAX_LOOPS_EXCEEDED, log: state };
      }
      saveState();
    }
  }

  state.status = Status.MAX_LOOPS_EXCEEDED;
  saveState();
  return { status: Status.MAX_LOOPS_EXCEEDED, log: state };
}

// Support CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  let featureSlug = 'loop-engineer';
  for (const arg of args) {
    if (arg.startsWith('--feature=')) {
      featureSlug = arg.split('=')[1];
    }
  }

  runLoop({ featureSlug })
    .then((res) => {
      console.log(`Loop Runner completed with status: ${res.status}`);
      process.exit(res.status === Status.APPROVED ? 0 : 1);
    })
    .catch((err) => {
      console.error('Fatal error in Loop Runner:', err);
      process.exit(1);
    });
}

module.exports = {
  runLoop,
  validateQAFeedback,
  validateLoopLog,
  Status,
  Verdict,
  Severity,
  MAX_LOOPS,
  SUBAGENT_TIMEOUT_MS
};
