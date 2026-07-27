---
name: design-init
description: Generate system design specifications including component boundaries, data model, and user flow.
---

# /kanche:design-init

**Mission.** Translate the approved `specs.md` into an implementable technical design — the HOW — returning three bodies (`design.md`, `api-diff.md`, `db-diff.md`), incorporating closed-loop feedback from `/kanche:design-review`.

## Loop Engineering Protocol (Generator Role — P2 Design Loop)

In the Loop Engineering Framework, `/kanche:design-init` acts as the **Generator Skill** paired with `/kanche:design-review`:
- **Iteration 1**: Generates initial `design.md`, `api-diff.md`, and `db-diff.md`.
- **Iteration 2..N (≤3x Loop)**: Receives `sdd-review` findings (`verdict: NO-GO`, `findings: [{severity, msg, fix_suggestion}]`). Applies targeted technical design refinements resolving reported blocker/major architectural issues.

## Read

- `docs/development/{NNN}_{slug}/specs.md` — the requirements this design must satisfy.
- `docs/guidelines/{tech,structure,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — stack, versions, module boundaries, allowed dependency directions, loop rules, and mandatory rules.
- `sdd-review` findings from prior review iterations (when running in iteration 2..N).
- Any existing `design.md`, `api-diff.md`, `db-diff.md` for this feature (refine, don't discard).
- Consolidated context when present: `docs/product/api/openapi.yaml`, `docs/product/database/er-diagram.md` — so deltas are expressed against the real current contract/schema.
- The codebase (glob/grep/read) to locate actual files, symbols, and patterns.

## Produce

Return three clearly labeled bodies (`design.md`, `api-diff.md`, `db-diff.md`).

**`design.md`** — sections in order:
- **Approach** — The chosen strategy in a few sentences and why it fits the specs and guidelines.
- **Architecture context** — Where this lands in the existing structure; affected modules/layers and their boundaries. Mermaid diagram when useful.
- **Components** — Each new/changed unit: responsibility, collaborators, and the source file(s) it lives in.
- **Interfaces** — Public signatures/contracts: function/method signatures, endpoints, events, CLI.
- **Data changes** — Narrative of schema/state changes.
- **Alternatives** — Options considered and why rejected.
- **Risks** — Technical risks, breaking-change/migration concerns, and mitigations.

**`api-diff.md`** — the API delta for THIS feature only.
**`db-diff.md`** — the schema delta for THIS feature only.

## Rules

- Returns DATA to the calling workflow (`/kanche:design-init`); does NOT write files, commit, push, or orchestrate. Read-only — no writes/edits.
- Design only within approved specs and guideline boundaries.
- Cite real file paths and existing patterns.
- Follow `docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.

