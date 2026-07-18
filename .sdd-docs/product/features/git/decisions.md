# Git Plugin — Decisions (ADR log)

<!-- schema: decisions | written by /sdd:sync-product -->

## ADR-001: Secure Deletion of Tags
- **Context:** Deleting remote tags is a destructive action that should not be run automatically without verification.
- **Decision:** Gate the `/git:tag-delete` command behind explicit human confirmation. Verify the tag exists locally and remotely before attempting deletion.
- **Consequences:** Safe tag lifecycle management with reduced risk of accidental data loss.
