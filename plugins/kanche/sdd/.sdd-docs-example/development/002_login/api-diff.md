# API delta — Login (SSO)

<!-- consumed by /sdd:sync-product → merged into product/api/openapi.yaml -->

## Added
```yaml
paths:
  /auth/sso/start:
    get:
      summary: Begin OIDC login (redirect to IdP)
      responses: { "302": { description: Redirect to IdP } }
  /auth/sso/callback:
    get:
      summary: OIDC callback — exchange code, issue session
      parameters:
        - { name: code,  in: query, required: true,  schema: { type: string } }
        - { name: state, in: query, required: true,  schema: { type: string } }
      responses:
        "302": { description: Session issued, redirect to / }
        "400": { description: Invalid or expired state }
```
