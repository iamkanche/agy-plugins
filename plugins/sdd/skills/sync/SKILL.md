# doc-synchronizer (skill)

**Mission.** Detect drift — between the feature docs and each other, and between the docs and the
as-built code — and return a drift report plus concrete proposed edits. Never edit silently; the
calling workflow/human applies the edits.

## Read

- Feature docs: `.sdd-docs/development/{NNN}_{slug}/{specs,design,tasks,api-diff,db-diff}.md`.
- Consolidated docs when in scope: `.sdd-docs/product/api/openapi.yaml`,
  `.sdd-docs/product/database/er-diagram.md`, `.sdd-docs/product/features/{slug}/*`.
- `.sdd-docs/guidelines/{tech,structure,rules}.md`.
- The as-built code: use read-only git (`git diff`, `git log`, `git ls-files`) and
  glob/grep/read to compare the actual endpoints, schema, and behavior against what the
  docs claim.

Scope depends on the caller: `/sdd:sync-docs` reconciles the dev docs against each other;
`/sdd:sync-docs-code` reconciles the dev docs against as-built code. Only compare what the
caller asks for.

## Produce

Return a **drift report** (chat data, not a file) with two parts:

- **Drift findings** — one entry per discrepancy: what the doc says vs. what is true (in another
  doc or in code), the file(s)/location involved, and severity (blocker/major/nit). Cover:
  specs↔design↔tasks consistency (e.g. an acceptance criterion with no task, a design interface
  no longer matching code), `api-diff`/`db-diff` vs. actual routes/schema, and stale/obsolete
  statements. Explicitly state where docs and code already agree.
- **Proposed edits** — for each finding, a precise, ready-to-apply change: the target file and
  the exact old→new text (a `diff`-style or before/after snippet), so the workflow can apply it
  verbatim. Prefer editing docs to match as-built code; where the code looks wrong instead of the
  docs, flag it as a code issue rather than proposing a doc edit that hides a bug.

If there is no drift, say so explicitly with the evidence checked.

## Rules

- Returns DATA (drift report + proposed edits) to the calling workflow (`/sdd:sync-docs`,
  `/sdd:sync-docs-code`); does NOT edit files, commit, push, or orchestrate. Read-only —
  no writes/edits; bash for read-only git/inspection only.
- Never edit silently and never invent reconciliation: propose, with evidence, and let the
  workflow/human apply and commit.
- Ground every finding in a specific doc location and code location.
- Follow `.sdd-docs/guidelines/rules.md` and the project's output-language policy.
