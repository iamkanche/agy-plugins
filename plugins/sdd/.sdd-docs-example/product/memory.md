# Product Memory

<!-- durable cross-feature memory; written by /sdd:preserve (NOT by sync-product) -->

- Sessions are cookie-based and shared by all auth flows (password + SSO).
- First SSO customer runs Okta (OIDC). SAML is deferred, not dropped.
- `sub` is the stable IdP identifier; email is optional and may be absent.
