---
feature: login
module: auth
pbi: [002_login]
integrated_at: 2026-07-16
updated_at: 2026-07-16
---

# Login — Consolidated Specification

<!-- schema: specs | written by /sdd:sync-product (dev-only sections stripped) -->

## Context
Authentication for the app. Supports email + password (baseline) and OIDC SSO for enterprise.

## Capabilities
- Email + password sign-in (baseline).
- **SSO (OIDC)** — authorization-code flow; "Sign in with SSO" button. _(002_login)_

## Acceptance criteria (as-built)
1. Clicking "Sign in with SSO" redirects to the configured IdP.
2. A valid callback issues a session cookie and lands on the dashboard.
3. An invalid/expired `state` is rejected with an error page.

## Data model
`user`, `sso_identity`. See `../../database/er-diagram.md`.
