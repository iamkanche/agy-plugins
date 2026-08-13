---
name: design-specs-review
description: Review specifications against rules and guidelines.
model: pro
---

# /kanche:design-specs-review

**Mission.** Critically review `specs.md` for completeness, testability, and consistency, returning a GO/NO-GO verdict with actionable findings for closed-loop iteration with `/kanche:design-specs`.

## Loop Engineering Protocol (Reviewer Role — P1 Specs Loop)

In the Loop Engineering Framework, `/kanche:design-specs-review` acts as the **Reviewer Skill** paired with `/kanche:design-specs`:
- Audits `specs.md` for testability, complete coverage, and rule adherence.
- Emits structured `sdd-review` block consumed by `/kanche:design-specs` during retry loops (up to 3x).

## Read

- `.docs/development/{NNN}_{slug}/specs.md` — the document under review.
- The original feature request / grill Q&A passed in by the workflow — to check the specs answer what was asked and captured the resolved clarifications.
- `.docs/guidelines/{product,tech,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — scope boundaries, constraints, loop rules, and guidelines.
- The codebase only to sanity-check that data-model/integration claims are plausible against reality — do not review implementation.

## Produce

Judge against these criteria and record every issue as a finding:

- **Structure** — all required sections present (Context, Scope, User stories, Acceptance criteria, Data model, NFR, Open questions).
- **Testability** — every acceptance criterion is observable and verifiable; none leaks implementation detail. Flag vague/unmeasurable criteria.
- **Coverage** — every user story maps to ≥1 acceptance criterion; happy path, boundary/empty, and error behavior are all covered; non-goals are explicit.
- **NFR** — applicable non-functionals are present and measurable.
- **Consistency** — no internal contradictions; no conflict with guidelines; scope matches the request.
- **Open questions** — remaining unknowns are captured, not silently assumed.

Return exactly one fenced `sdd-review` block as the machine-readable verdict, plus a short prose rationale beneath it:

```sdd-review
verdict: GO            # or NO-GO
loop_iteration: 1/3    # current iteration / max_loops
findings:
  - severity: blocker  # blocker | major | nit
    msg: "Description of issue"
    file: ".docs/development/{slug}/specs.md"
    line: 25
    fix_suggestion: "Concrete guidance to fix specs"
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`. `nit`-only ⇒ `GO`. Make each `msg` specific and fixable (what's wrong + which section). If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/kanche:design-specs-review`); does NOT edit specs, commit, push, or orchestrate. Read-only — no writes/edits.
- Review only; propose fixes as findings, do not apply them.
- Follow `.docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.

