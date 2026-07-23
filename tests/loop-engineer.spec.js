/**
 * Test suite for Loop Engineer System (loop-runner.js)
 * Path: tests/loop-engineer.spec.js
 *
 * Verifies state machine transitions, 3-loop cap, schema validation,
 * error handling, and persistent telemetry logging.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const assert = require('assert');
const {
  runLoop,
  validateQAFeedback,
  validateLoopLog,
  Status,
  Verdict,
  Severity
} = require('../plugins/loop-engineer/scripts/loop-runner.js');

async function runTests() {
  console.log('--- Starting Loop Engineer Unit & Integration Tests ---');
  let passedCount = 0;
  let failedCount = 0;

  async function test(name, fn) {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'loop-eng-test-'));
    try {
      await fn(tmpDir);
      console.log(`✓ PASS: ${name}`);
      passedCount++;
    } catch (err) {
      console.error(`✗ FAIL: ${name}`);
      console.error(err);
      failedCount++;
    } finally {
      try {
        fs.rmSync(tmpDir, { recursive: true, force: true });
      } catch (e) {}
    }
  }

  // ------------------------------------------------------------------------
  // Case 1: First-Pass Approval (GO on Loop 1 -> APPROVED)
  // ------------------------------------------------------------------------
  await test('Case 1: First-Pass Approval (GO on Loop 1)', async (tmpDir) => {
    const featureSlug = 'test-feature-1';

    let engCalls = 0;
    let qaCalls = 0;

    const res = await runLoop({
      featureSlug,
      baseDir: tmpDir,
      engineerRunner: async (input) => {
        engCalls++;
        return {
          status: 'DONE',
          engineer_summary: 'Initial clean code.',
          changed_files: ['index.js']
        };
      },
      qaRunner: async (input) => {
        qaCalls++;
        return {
          verdict: Verdict.GO,
          test_results: { total: 5, passed: 5, failed: 0, execution_time_ms: 500 },
          findings: []
        };
      }
    });

    assert.strictEqual(res.status, Status.APPROVED);
    assert.strictEqual(engCalls, 1);
    assert.strictEqual(qaCalls, 1);
    assert.strictEqual(res.log.iterations.length, 1);
    assert.strictEqual(res.log.iterations[0].qa_verdict, Verdict.GO);

    const logPath = path.join(tmpDir, '.sdd-docs', 'development', featureSlug, 'loop-log.json');
    assert.strictEqual(fs.existsSync(logPath), true);
    const savedLog = JSON.parse(fs.readFileSync(logPath, 'utf8'));
    assert.strictEqual(savedLog.status, Status.APPROVED);
    assert.strictEqual(validateLoopLog(savedLog).valid, true);
  });

  // ------------------------------------------------------------------------
  // Case 2: Iterative Remediation (NO-GO on Loop 1, GO on Loop 2 -> APPROVED)
  // ------------------------------------------------------------------------
  await test('Case 2: Iterative Remediation (NO-GO loop 1, GO loop 2)', async (tmpDir) => {
    const featureSlug = 'test-feature-2';

    let engCalls = 0;
    let qaCalls = 0;

    const res = await runLoop({
      featureSlug,
      baseDir: tmpDir,
      engineerRunner: async (input) => {
        engCalls++;
        if (input.iteration === 2) {
          assert.strictEqual(input.qa_findings_from_previous_loop.length, 1);
          assert.strictEqual(input.qa_findings_from_previous_loop[0].message, 'Syntax error on L10');
        }
        return {
          status: 'DONE',
          engineer_summary: `Summary for iter ${input.iteration}`,
          changed_files: ['app.js']
        };
      },
      qaRunner: async (input) => {
        qaCalls++;
        if (input.iteration === 1) {
          return {
            verdict: Verdict.NO_GO,
            test_results: { total: 5, passed: 4, failed: 1, execution_time_ms: 600 },
            findings: [
              {
                severity: Severity.MAJOR,
                file: 'app.js',
                line_range: 'L10',
                message: 'Syntax error on L10',
                test_context: 'unit test fail'
              }
            ]
          };
        }
        return {
          verdict: Verdict.GO,
          test_results: { total: 5, passed: 5, failed: 0, execution_time_ms: 400 },
          findings: []
        };
      }
    });

    assert.strictEqual(res.status, Status.APPROVED);
    assert.strictEqual(engCalls, 2);
    assert.strictEqual(qaCalls, 2);
    assert.strictEqual(res.log.iterations.length, 2);
    assert.strictEqual(res.log.iterations[0].qa_verdict, Verdict.NO_GO);
    assert.strictEqual(res.log.iterations[1].qa_verdict, Verdict.GO);
  });

  // ------------------------------------------------------------------------
  // Case 3: Maximum Iterations Capping (NO-GO on Loops 1..3 -> MAX_LOOPS_EXCEEDED)
  // ------------------------------------------------------------------------
  await test('Case 3: Maximum Iterations Cap (3 Loops Exceeded)', async (tmpDir) => {
    const featureSlug = 'test-feature-3';

    let engCalls = 0;
    let qaCalls = 0;

    const res = await runLoop({
      featureSlug,
      baseDir: tmpDir,
      engineerRunner: async () => {
        engCalls++;
        return { status: 'DONE', engineer_summary: 'Attempt fix', changed_files: ['lib.js'] };
      },
      qaRunner: async () => {
        qaCalls++;
        return {
          verdict: Verdict.NO_GO,
          test_results: { total: 5, passed: 3, failed: 2, execution_time_ms: 300 },
          findings: [
            {
              severity: Severity.BLOCKER,
              file: 'lib.js',
              line_range: 'L5-L10',
              message: 'Persistent defect',
              test_context: 'suite error'
            }
          ]
        };
      }
    });

    assert.strictEqual(res.status, Status.MAX_LOOPS_EXCEEDED);
    assert.strictEqual(engCalls, 3);
    assert.strictEqual(qaCalls, 3);
    assert.strictEqual(res.log.iterations.length, 3);
  });

  // ------------------------------------------------------------------------
  // Case 4: QA Protocol Error (Empty findings on NO-GO)
  // ------------------------------------------------------------------------
  await test('Case 4: QA Protocol Error (Invalid NO-GO payload)', async (tmpDir) => {
    const featureSlug = 'test-feature-4';

    const res = await runLoop({
      featureSlug,
      baseDir: tmpDir,
      engineerRunner: async () => ({ status: 'DONE', engineer_summary: 'OK', changed_files: [] }),
      qaRunner: async () => ({
        verdict: Verdict.NO_GO,
        test_results: { total: 2, passed: 1, failed: 1 },
        findings: [] // EMPTY findings on NO-GO!
      })
    });

    assert.strictEqual(res.status, Status.QA_PROTOCOL_ERROR);
    assert.strictEqual(res.log.status, Status.QA_PROTOCOL_ERROR);
  });

  // ------------------------------------------------------------------------
  // Case 5: Fatal Environment Failure / Timeout handling
  // ------------------------------------------------------------------------
  await test('Case 5: Fatal Error on Subagent Exception / Timeout', async (tmpDir) => {
    const featureSlug = 'test-feature-5';

    const res = await runLoop({
      featureSlug,
      baseDir: tmpDir,
      engineerRunner: async () => {
        throw new Error('Unrecoverable environment crash');
      },
      qaRunner: async () => ({
        verdict: Verdict.GO,
        test_results: { total: 1, passed: 1, failed: 0 },
        findings: []
      })
    });

    assert.strictEqual(res.status, Status.FATAL_ERROR);
    assert.strictEqual(res.log.status, Status.FATAL_ERROR);
  });

  // ------------------------------------------------------------------------
  // Case 6: Idempotent State Recovery (resume from checkpoint)
  // ------------------------------------------------------------------------
  await test('Case 6: Idempotent State Recovery', async (tmpDir) => {
    const featureSlug = 'test-feature-6';
    const docDir = path.join(tmpDir, '.sdd-docs', 'development', featureSlug);
    fs.mkdirSync(docDir, { recursive: true });

    // Seed existing loop-log.json with 1 completed iteration (NO-GO) in IN_PROGRESS status
    const initialLog = {
      id: 'existing-session-123',
      feature_slug: featureSlug,
      status: Status.IN_PROGRESS,
      max_loops: 3,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      iterations: [
        {
          iteration: 1,
          timestamp: new Date().toISOString(),
          engineer_summary: 'Iter 1 changes',
          changed_files: ['file1.js'],
          qa_verdict: Verdict.NO_GO,
          qa_findings: [
            {
              severity: Severity.MAJOR,
              file: 'file1.js',
              line_range: 'L1-L2',
              message: 'Fix needed',
              test_context: 'test 1'
            }
          ],
          test_results: { total: 2, passed: 1, failed: 1 }
        }
      ]
    };
    fs.writeFileSync(path.join(docDir, 'loop-log.json'), JSON.stringify(initialLog, null, 2));

    let engCalls = 0;
    const res = await runLoop({
      featureSlug,
      baseDir: tmpDir,
      engineerRunner: async (input) => {
        engCalls++;
        // Should resume at iteration 2!
        assert.strictEqual(input.iteration, 2);
        return { status: 'DONE', engineer_summary: 'Iter 2 fix', changed_files: ['file1.js'] };
      },
      qaRunner: async () => ({
        verdict: Verdict.GO,
        test_results: { total: 2, passed: 2, failed: 0 },
        findings: []
      })
    });

    assert.strictEqual(res.status, Status.APPROVED);
    assert.strictEqual(engCalls, 1); // Only iteration 2 ran
    assert.strictEqual(res.log.iterations.length, 2);
    assert.strictEqual(res.log.id, 'existing-session-123');
  });

  console.log(`\n--- Test Summary ---`);
  console.log(`Passed: ${passedCount}`);
  console.log(`Failed: ${failedCount}`);

  if (failedCount > 0) {
    process.exit(1);
  }
}

if (require.main === module) {
  runTests().catch((err) => {
    console.error('Unhandled test execution error:', err);
    process.exit(1);
  });
}

module.exports = { runTests };
