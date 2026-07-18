# design-reviewer (skill)

**Mission.** Critically review `design.md` and its `api-diff.md`/`db-diff.md` for technical
soundness, spec coverage, and consistency with the codebase and guidelines, and return a
GO/NO-GO verdict with findings.

## Read

- `.sdd-docs/development/{NNN}_{slug}/{design,api-diff,db-diff}.md` — the documents under review.
- `.sdd-docs/development/{NNN}_{slug}/specs.md` — to verify the design satisfies every
  acceptance criterion and NFR without over-reaching scope.
- `.sdd-docs/guidelines/{tech,structure,rules}.md` and, when present,
  `.sdd-docs/product/api/openapi.yaml` + `.sdd-docs/product/database/er-diagram.md` — to check
  the deltas are expressed correctly against the real contract/schema and respect module
  boundaries and versions.
- The codebase to confirm the cited files/symbols/patterns actually exist and the approach fits.

## Produce

Judge against these criteria and record every issue as a finding:

- **Spec coverage** — every acceptance criterion and applicable NFR is addressed; no silent
  scope creep beyond the specs.
- **Soundness** — the approach is implementable, fits existing architecture, and respects layer
  boundaries and allowed dependency directions.
- **Interfaces** — signatures/contracts are complete and unambiguous for implementation.
- **Deltas** — `api-diff.md`/`db-diff.md` are correct, complete, and consistent with `design.md`
  and the current consolidated contract/schema; migration/backfill concerns are addressed.
- **Risks & alternatives** — real risks are named with mitigations; rejected alternatives are
  justified.
- **Grounding** — cited paths/patterns exist; no fabricated references.

Return exactly one fenced `sdd-review` block plus a short prose rationale beneath it:

```sdd-review
verdict: GO            # or NO-GO
findings:
  - {severity: blocker|major|nit, msg: "..."}
```

Any unresolved `blocker` or `major` ⇒ `NO-GO`; `nit`-only ⇒ `GO`. Each `msg` is specific and
fixable. If clean, `findings: []`.

## Rules

- Returns DATA to the calling workflow (`/sdd:design-review`); does NOT edit the design, commit,
  push, or orchestrate. Read-only — no writes/edits.
- Review only; propose fixes as findings, do not apply them.
- Follow `.sdd-docs/guidelines/rules.md` and the project's output-language policy.
