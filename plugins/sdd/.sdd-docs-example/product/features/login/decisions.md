# Login — Decisions (ADR log)

<!-- ⭐⭐⭐⭐⭐ appended by /sdd:sync-product from design "Alternatives considered" -->

## ADR-001: OIDC before SAML
- **Context:** Enterprise customers need SSO; first customer is on Okta (OIDC).
- **Decision:** Ship OIDC authorization-code flow first; defer SAML.
- **Consequences:** Faster delivery for the initial customer; SAML remains a future feature.
- **Source:** 002_login/design.md → Alternatives considered.

## ADR-002: Reuse existing session store
- **Context:** SSO needs to issue a session after callback.
- **Decision:** Reuse `SessionIssuer`; no new token cache.
- **Consequences:** Less code; SSO and password sessions are identical downstream.
