---
name: test-data
description: Infer schemas from TypeScript types, database models, or OpenAPI specs to generate deterministic mock fixtures and test pattern tables.
---

# /kanche:test-data

**Mission.** Generate schema-grounded mock data (`json`, `csv`, `sql`, Laravel factories, TS fixtures) and boundary test pattern tables (`@tester`, `agents/tester.md`).

## Inputs

- `<target-schema>` — file path or symbol (e.g., `src/api/types.ts`, Prisma schema, Laravel Model/Migration, OpenAPI YAML).
- `--format=json|csv|sql|ts|factory|pattern` — output format (default: `json`).
- `--count=<N>` — record count (default: `10`).

## Steps

1. **Inspect Target Schema.** Read the referenced interface, model, migration, or `api-diff.md` / `db-diff.md`. Map field types, enums, nullable constraints, and foreign-key relations.
2. **Generate Boundary & Valid Cases.**
   - Include valid realistic records plus edge values (empty optional fields, min/max numeric/decimal boundaries, invalid format negatives for test cases).
   - For relational schemas, generate parent IDs before child records so foreign keys stay consistent.
   - If `--format=pattern`, emit a markdown matrix (`Case ID | Scenario | Input/Request | Expected Output/Status | Boundary Type`).
3. **Output or Save.** Write fixtures to the project's test fixture directory specified in `test-plan.md` / `.docs/guidelines/structure.md` (or return inline if no path given).

## Rules

- Never use real PII, production dumps, or live credentials in generated fixtures.
- Keep output deterministic and strictly matched to actual source types.
- Follow `rules/token-optimization.md`.
