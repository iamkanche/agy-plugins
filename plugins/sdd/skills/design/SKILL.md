# design-architect (skill)

**Mission.** Translate the approved `specs.md` into an implementable technical design — the HOW
— and return three bodies: `design.md`, `api-diff.md`, and `db-diff.md` for
`.sdd-docs/development/{NNN}_{slug}/`.

## Read

- `.sdd-docs/development/{NNN}_{slug}/specs.md` — the requirements this design must satisfy.
- `.sdd-docs/guidelines/{tech,structure,rules}.md` — stack, versions, module boundaries, allowed
  dependency directions, mandatory rules.
- Any existing `design.md`, `api-diff.md`, `db-diff.md` for this feature (refine, don't discard).
- Consolidated context when present: `.sdd-docs/product/api/openapi.yaml`,
  `.sdd-docs/product/database/er-diagram.md` — so deltas are expressed against the real
  current contract/schema.
- The codebase (glob/grep/read) to locate the actual files, symbols, and patterns the
  design will extend — cite exact paths so `tasks` and `build` can act without re-discovery.

## Produce

Return three clearly labeled bodies. Use the project output language for prose; keep code
identifiers, paths, types, routes, and SQL verbatim.

**`design.md`** — sections in order:

- **Approach** — The chosen strategy in a few sentences and why it fits the specs and guidelines.
- **Architecture context** — Where this lands in the existing structure; affected modules/layers
  and their boundaries. A small Mermaid diagram when it clarifies data/flow.
- **Components** — Each new/changed unit: responsibility, collaborators, and the source
  file(s) it lives in.
- **Interfaces** — Public signatures/contracts: function/method signatures, endpoints, events,
  CLI — enough for implementation, not full bodies.
- **Data changes** — Narrative of schema/state changes (the precise delta goes in `db-diff.md`).
- **Alternatives** — Options considered and why rejected (with a recommendation rating when the
  choice is non-obvious).
- **Risks** — Technical risks, breaking-change/migration concerns, and mitigations.

**`api-diff.md`** — the API delta for THIS feature only: added/changed/removed endpoints or
operations with method, path, request/response shape, status codes, and auth. Empty-but-explicit
("No API changes") if none. Expressed against `product/api/openapi.yaml` when it exists.

**`db-diff.md`** — the schema delta for THIS feature only: new/changed/removed tables, columns
(name, type, nullability, default), indexes, constraints, and any migration/backfill notes.
Empty-but-explicit if none. Expressed against `product/database/er-diagram.md` when it exists.

Trace each design decision back to a spec acceptance criterion or NFR; flag anything the specs
do not cover as an open question rather than silently expanding scope.

## Rules

- Returns DATA to the calling workflow (`/sdd:design`); does NOT write files, commit, push, or
  orchestrate. Read-only — no writes/edits.
- Design only within the approved specs and the guidelines' boundaries/versions; do not
  introduce new dependencies or scope without flagging them.
- Cite real file paths and existing patterns; label inferences. Keep `api-diff.md`/`db-diff.md`
  as per-feature deltas (not the whole contract) so consolidation stays tractable.
- Follow `.sdd-docs/guidelines/rules.md` and the project's output-language policy.
