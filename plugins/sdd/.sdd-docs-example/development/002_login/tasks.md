# Login (SSO) — Implementation Tasks

<!-- schema: tasks | written by /sdd:tasks, checked off by /sdd:build -->

## Phase A — Data
- [x] A1. Migration: create `sso_identity` table _(files: /db/migrations)_
- [x] A2. `sso_identity` repository _(files: /api/auth/sso_repo.go)_

## Phase B — Flow
- [x] B1. `GET /auth/sso/start` handler _(depends: A2)_
- [x] B2. `GET /auth/sso/callback` handler _(depends: B1)_
- [ ] B3. "Sign in with SSO" button _(files: /web/src/features/login)_

## Verification
- [x] Build passes
- [ ] Lint passes
- [ ] Tests pass (auth_test)
- [ ] Acceptance criteria in specs.md all satisfied
