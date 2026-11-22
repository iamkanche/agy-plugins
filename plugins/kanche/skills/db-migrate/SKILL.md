---
name: db-migrate
description: Verify database migrations against db-diff.md, check rollback reversibility, and gate destructive resets.
---

# /kanche:db-migrate

**Mission.** Author and safely verify database schema migrations (`@data-architect` / `@backend-expert`) across Laravel (`php artisan migrate`), Prisma, Go, Python/Alembic, or raw SQL against `.docs/development/{slug}/db-diff.md`.

## Inputs

- `--dry-run` — run pretend/SQL preview (`--pretend`, `migrate diff`, `--sql`) without mutating database state.
- `--rollback-check` — test `up` followed by `down` rollback on a non-production dev database to verify reversibility.

## Steps

1. **Inspect Schema Contract.** Read `.docs/development/{slug}/db-diff.md` and existing migrations/models. Verify indexes, foreign keys, nullability, and decimal/precision invariants (never float for money).
2. **Check Reversibility.** Confirm every migration implements a clean `down()` / rollback script without silent data loss.
3. **Preview & Validate:**
   - Run framework dry-run/status check (`php artisan migrate:status`, `npx prisma migrate status`, `alembic current`, etc.).
   - Execute non-destructive forward migration only after verifying target environment is local/dev (NEVER production).
4. **Destructive Gate (Mandatory):**
   - `migrate:fresh`, `migrate:reset`, `DROP TABLE`, `DROP DATABASE`, and `TRUNCATE` are **strictly forbidden** autonomously per `rules/destructive-safety.md` and blocked by `hooks/destructive_gate.py`.
   - Only prompt via `default_api:ask_question` if explicitly requested by the user on a local dev DB.

## Rules

- Never alter historical already-merged migrations; create a new incremental migration.
- Follow `rules/destructive-safety.md` and `rules/token-optimization.md`.
