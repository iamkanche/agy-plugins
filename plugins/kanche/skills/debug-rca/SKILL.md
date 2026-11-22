---
name: debug-rca
description: Perform autonomous root cause analysis on stack traces, failing tests, and logs using git history and minimal scratch repros.
---

# /kanche:debug-rca

**Mission.** Isolate the exact root cause of a failure before editing source files (`@debugger`, `agents/debugger.md`). Outputs a verified Root Cause Report and surgical fix spec for `/kanche:code-implement`.

## Inputs

- `<error-or-target>` — stack trace, failing test command, log snippet, or file path.
- `--repro` — write a minimal standalone reproduction script inside the conversation `scratch/` directory (never pollute the repo root).

## Steps

1. **Collect Evidence.** Read failing stack frames, error logs, and recent changes (`git log -n 10 --oneline`, `git diff`). Use `git bisect` only on read-only checkout if regression commit is unknown.
2. **Trace Execution Path.** Inspect call sites from crash line upstream; check nullability, concurrency races, state mutations, and schema mismatches.
3. **Verify Hypothesis.** Run targeted read-only checks or execute a minimal repro in `scratch/` (if `--repro`) to confirm reproduction before proposing a fix.
4. **Emit Root Cause Report:**
   - **Root Cause:** Exact `file:line` and faulty condition/assumption.
   - **Evidence:** Reproduction command + observed failure output.
   - **Surgical Fix Spec:** Minimal diff recommendation for `/kanche:code-implement` + regression test case to add.

## Rules

- Read-only to repository source files (repro scripts go in `scratch/` only).
- Never guess or apply blind patches before confirming root cause.
- Follow `rules/token-optimization.md` and `rules/output-language.md`.
