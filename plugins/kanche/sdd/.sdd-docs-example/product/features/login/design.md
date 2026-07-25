# Login — Consolidated Design (as-built)

<!-- schema: design | written by /sdd:sync-product -->

## Auth flows
- **Password:** existing email + password → `SessionIssuer`.
- **SSO (OIDC):** `/auth/sso/start` → IdP → `/auth/sso/callback` → `SessionIssuer`. _(002_login)_

## Components
| Component | Responsibility |
|---|---|
| `auth.SSOHandler` | OIDC start + callback |
| `auth.SessionIssuer` | issue session cookie (shared by both flows) |
| `sso_identity` repo | map IdP subject → user |

See `../../api/openapi.yaml` and `../../database/er-diagram.md`.
