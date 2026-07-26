---
name: code-review
description: Perform deep code review on staged/modified files with auto-fix capability and security checks.
---

# /kanche:code-review

**Summary.** Perform deep static and functional code review on changed or staged files against `AGENTS.md` and repository guidelines, with optional auto-application of non-breaking refactors/nits.

## Inputs

- `--auto-apply` — automatically apply minor formatting and lint fix suggestions.
- `<target-path>` (optional) — specific file or directory to review. Defaults to modified branch diff (`git diff`).

## Steps

1. Inspect diff and touched paths (`git diff`, `git status`).
2. Audit against code quality, security standards (no secrets, no SQL/command injection), and style conventions.
3. If `--auto-apply` is specified, apply nit/style fixes directly to files.
4. Report structured findings (Blocker / Major / Nit) with exact file:line pointers.
