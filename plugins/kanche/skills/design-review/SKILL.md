---
name: design-review
description: Review system design specifications and architecture.
---

# /kanche:design-review

**Mission.** Critically review `design.md` and its `api-diff.md`/`db-diff.md` for technical soundness, spec coverage, and consistency, returning a GO/NO-GO verdict with findings for closed-loop iteration with `/kanche:design-init`.

## Loop Engineering Protocol (Reviewer Role — P2 Design Loop)

In the Loop Engineering Framework, `/kanche:design-review` acts as the **Reviewer Skill** paired with `/kanche:design-init`:
- Audits `design.md`, `api-diff.md`, and `db-diff.md` for technical feasibility, architecture alignment, and spec coverage.
- Emits structured `sdd-review` block consumed by `/kanche:design-init` during retry loops (up to 3x).

## Read

- `docs/development/{NNN}_{slug}/{design,api-diff,db-diff}.md` — the documents under review.
- `docs/development/{NNN}_{slug}/specs.md` — to verify the design satisfies every acceptance criterion.
- `docs/guidelines/{tech,structure,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — guidelines and loop rules.
- Consolidated context when present: `docs/product/api/openapi.yaml` + `docs/product/database/er-diagram.md`.
- The codebase to confirm cited files/symbols/patterns exist.

## Produce

Judge against these criteria and record every issue as a finding:

- **Spec coverage** — every acceptance criterion and applicable NFR is addressed.
- **Soundness** — the approach is implementable and fits existing architecture.
- **Interfaces** — signatures/contracts are complete and unambiguous.
- **Deltas** — `api-diff.md`/`db-diff.md` are correct and complete.
- **Risks & alternatives** — real risks are named with mitigations.
- **Grounding** — cited paths/patterns exist.

Return exactly one fenced `sdd-review` block plus a short prose rationale beneath it:

```sdd-review
verdict: GO            # or NO-GO
loop_iteration: 1/3    # current iteration / max_loops
findings:
  - severity: blocker  # blocker | major | nit
    msg: "Description of issue"
    file: "docs/development/{slug}/design.md"
    line: 14
    fix_suggestion: "Concrete guidance to refine technical design"
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`; `nit`-only ⇒ `GO`. Each `msg` is specific and fixable. If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/kanche:design-review`); does NOT edit the design, commit, push, or orchestrate. Read-only — no writes/edits.
- Review only; propose fixes as findings, do not apply them.
- Follow `docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.

