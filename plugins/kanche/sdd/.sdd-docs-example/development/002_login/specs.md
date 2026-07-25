# Login (SSO) — Specification

<!-- schema: specs | written by /sdd:specs -->

## Context
Users currently log in with email + password. Enterprise customers require SSO. This feature
adds OIDC-based single sign-on alongside the existing password flow.

## Scope
- **In scope:** OIDC authorization-code flow, callback handling, session issuance, "Sign in with SSO" button.
- **Out of scope:** SAML, SCIM provisioning, per-tenant IdP config UI (later feature).

## User stories
- As an enterprise user, I want to sign in with my company IdP, so that I don't manage a separate password.

## Acceptance criteria
1. Given a configured OIDC provider, when the user clicks "Sign in with SSO", then they are redirected to the IdP.
2. Given a valid IdP callback, when the code is exchanged, then a session cookie is issued and the user lands on the dashboard.
3. Given an invalid/expired `state`, when the callback arrives, then login is rejected with an error page.

## Data model
New `sso_identity` linking a `user` to an external `subject`. See `db-diff.md`.

## Non-functional requirements
- `state` and `nonce` are single-use, expire in 10 min.
- Tokens never logged.

## Open questions
_Resolved in grill-me: use existing session store; no new token cache._
