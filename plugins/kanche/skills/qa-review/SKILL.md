---
name: qa-review
description: Audit code quality, implementation diffs, and test coverage using static inspection and Playwright MCP browser verification.
---

# /kanche:qa-review

**Mission.** Review the implementation produced by `build` for correctness, spec/design conformance, code quality, and visual integrity — using read-only checks and Playwright MCP browser tools — and return a GO/NO-GO verdict with findings.

## Read

- The change under review: `git diff` / `git status` against the feature branch's base plus changed source files.
- `docs/development/{slug}/{tasks,design,specs,api-diff,db-diff}.md` — to verify the code matches specified design and checked-off tasks.
- `docs/guidelines/{tech,structure,rules}.md` — for conventions, mandatory rules, and build/test/lint commands.

## Produce

Assess and record every issue as a finding:

- **Correctness** — acceptance criteria met, edge cases handled, no race conditions or resource leaks.
- **Conformance** — matches `design.md`, `api-diff.md`, `db-diff.md`.
- **Quality & rules** — adheres to repo rules, minimal diff, no secrets committed.
- **Verification evidence (CLI & MCP Playwright)** — run read-only build/test/lint commands. For UI changes, launch dev server if needed and use Playwright MCP tools (`browser_navigate`, `browser_screenshot`, `browser_console`) to perform visual verification, capturing screenshots and console log evidence.

Return exactly one fenced `sdd-review` block plus short prose rationale:

```sdd-review
verdict: GO            # or NO-GO
findings:
  - {severity: blocker|major|nit, msg: "..."}
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`; `nit`-only ⇒ `GO`. Each `msg` is specific and fixable (`file:line` where possible). If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/kanche:qa-review`); does NOT edit code, commit, push, or orchestrate.
- Review only; propose fixes as findings, do not apply them.
- Follow `docs/guidelines/rules.md` and the project's output-language policy.
