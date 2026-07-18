# Notes — Login (SSO)

<!-- research / scratch; archive-only, never consolidated into product/ -->

- IdP for the first customer is Okta; discovery doc at `/.well-known/openid-configuration`.
- Reuse `SessionIssuer` from `/api/auth/session.go:41` — no new session store needed.
- Grill-me raised: what if the IdP returns no email? → require `sub`, email optional.
