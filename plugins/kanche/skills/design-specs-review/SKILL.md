---
name: design-specs-review
description: Review specifications against rules and guidelines.
---

# /kanche:design-specs-review

**Mission.** Critically review `specs.md` for completeness, testability, and consistency, and
return a GO/NO-GO verdict with actionable findings.

## Read

- `docs/development/{NNN}_{slug}/specs.md` — the document under review.
- The original feature request / grill Q&A passed in by the workflow — to check the specs answer
  what was asked and captured the resolved clarifications.
- `docs/guidelines/{product,tech,rules}.md` — for scope boundaries, constraints, and rules
  the specs must honor.
- The codebase only to sanity-check that data-model/integration claims are plausible against
  reality — do not review implementation.

## Produce

Judge against these criteria and record every issue as a finding:

- **Structure** — all required sections present (Context, Scope, User stories, Acceptance
  criteria, Data model, NFR, Open questions).
- **Testability** — every acceptance criterion is observable and verifiable; none leaks
  implementation detail. Flag vague/unmeasurable criteria.
- **Coverage** — every user story maps to ≥1 acceptance criterion; happy path, boundary/empty,
  and error behavior are all covered; non-goals are explicit.
- **NFR** — applicable non-functionals are present and measurable.
- **Consistency** — no internal contradictions; no conflict with guidelines; scope matches the
  request.
- **Open questions** — remaining unknowns are captured, not silently assumed.

Return exactly one fenced `sdd-review` block as the machine-readable verdict, plus a short prose
rationale beneath it:

```sdd-review
verdict: GO            # or NO-GO
findings:
  - {severity: blocker|major|nit, msg: "..."}
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`. `nit`-only ⇒ `GO`. Make each `msg` specific and
fixable (what's wrong + which section). If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/kanche:design-specs-review`); does NOT edit specs, commit, push,
  or orchestrate. Read-only — no writes/edits.
- Review only; propose fixes as findings, do not apply them.
- Follow `docs/guidelines/rules.md` and the project's output-language policy.
