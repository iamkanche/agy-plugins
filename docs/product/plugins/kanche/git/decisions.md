# Git Plugin — Decisions (ADR log)

<!-- schema: decisions | written by /kanche:sdd-sync -->

## ADR-001: Secure Deletion of Tags
- **Context:** Deleting remote tags is a destructive action that should not be run automatically without verification.
- **Decision:** Gate the `/kanche:git-tag-delete` command behind explicit human confirmation. Verify the tag exists locally and remotely before attempting deletion.
- **Consequences:** Safe tag lifecycle management with reduced risk of accidental data loss.

## ADR-002: Interactive Gating via AskQuestion
- **Context:** Command confirmations via text prompt (yes/no) interrupt execution flow and require manual typing in the terminal.
- **Decision:** Mandate using the `default_api:ask_question` tool for all human gates across all git side-effect commands.
- **Consequences:** Modal-driven, structured confirmations that prevent CLI disruption and reduce keystroke errors.
