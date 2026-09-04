---
name: code-review
description: Perform deep code review on staged/modified files with auto-fix capability and security checks.
model: flash
---

# /kanche:code-review

**Summary.** Perform deep static and functional code review on changed or staged files against guidelines, emitting a machine-readable `review-verdict` block for closed-loop iteration with `/kanche:code-implement`, with optional auto-application of minor refactors/nits when requested.

## Loop Engineering Protocol (Reviewer Role — Code Implementation Loop)

In the Loop Engineering Framework, `/kanche:code-review` acts as the **Reviewer & Auditor Skill** paired with `/kanche:code-implement`:
- Evaluates code diffs, security, style, and correctness against `tasks.md`, `specs.md`, and repository guidelines.
- Returns a structured `review-verdict` block with `verdict: GO` or `NO-GO`, iteration status, and actionable findings containing exact `file:line` pointers and fix suggestions.
- When `--auto-apply` is enabled, automatically applies minor formatting/nit fixes directly to files, resolving nit findings.

## Inputs

- `--auto-apply` — automatically apply minor formatting and lint fix suggestions directly to target files.
- `<target-path>` (optional) — specific file or directory to review. Defaults to modified branch diff (`git diff`).

## Steps

1. Inspect diff and touched paths (`git diff`, `git status`) against target branch or `tasks.md`.
2. Audit against code quality, security standards (no secrets, no SQL/command injection), test coverage, and style conventions.
3. Classify each finding by severity:
   - `blocker`: Critical bug, security flaw, or broken acceptance criterion. (Forces `NO-GO`)
   - `major`: Architecture violation, missing test, or correctness risk. (Forces `NO-GO`)
   - `nit`: Formatting, style, or minor clarity improvement. (Does not force `NO-GO`)
4. If `--auto-apply` is specified, apply nit/style fixes directly to files.
5. Return exactly one fenced `review-verdict` block as the machine-readable verdict, plus a concise summary:

```review-verdict
verdict: GO            # or NO-GO (NO-GO if any blocker or major exists)
loop_iteration: 1/3    # current iteration / max_loops
findings:
  - severity: blocker  # blocker | major | nit
    msg: "Description of issue"
    file: "src/example.ts"
    line: 42
    fix_suggestion: "Concrete fix recommendation"
```

## Rules

- Returns DATA (including the `review-verdict` block) to the calling workflow. Does NOT commit, push, or orchestrate.
- Read-only by default; only modifies files if `--auto-apply` is explicitly passed for minor nit fixes.
- Follow `.docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and project output-language policies.

