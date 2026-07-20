# Design: Remove Ask-Question Gates from SDD Auto Mode

## Approach

Apply a **mode-conditional gate pattern** to every `default_api:ask_question` call that guards
a repository-modifying side effect. The mode is resolved once at skill-invocation time from
`settings.json` (`"mode": "auto"`) or from the `--mode` argument passed to `/sdd:run`. When
`mode=auto` the gate is bypassed and the action proceeds immediately after logging intent.
When `mode=manual` (or the skill is invoked standalone, outside of an SDD run) the existing
`default_api:ask_question` dialog fires exactly as it does today.

Safety invariants (no force-push, no `--no-verify`, protected-branch refusal, secrets
detection, self-approval prohibition, no amend on pushed commits, no `reset --hard`) are
unconditional hard STOPs that are **never** mode-gated.

## Standard Clause (Mode-Conditional Gate Pattern)

> **Gate — mode-conditional.** If this skill is invoked from SDD auto mode (`mode=auto` in
> `settings.json` or `--mode=auto` on `/sdd:run`), log the action (what will be written, the
> exact command, the target branch) and proceed automatically without prompting. If invoked
> standalone or from SDD manual mode, STOP and ask the user to confirm using the interactive
> `default_api:ask_question` tool with options `(Recommended) Yes, proceed` and `No, abort`.
> Proceed only on selecting Yes; on No, STOP.

## Mode Resolution Contract

```
resolve_mode(args, settings) → "auto" | "manual"
  1. --mode=auto|manual argument (highest priority)
  2. settings.json "mode" key
  3. default "auto" (SDD runner context) / "manual" (standalone invocation)
```

## Per-File Change Specifications

### 1. `.sdd-docs/product/memory.md` (L5–7)

**Before:**
```
- Human gating side-effect operations MUST use the interactive `default_api:ask_question` tool instead of raw text prompts.
- Gated operations include git commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges.
- Manual phase transitions, validation failures, and LEVEL 2 checkpoints in SDD workflow execution also use `default_api:ask_question`.
```

**After:**
```
- In **manual mode**, side-effect operations (git commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges) MUST gate on the interactive `default_api:ask_question` tool before proceeding.
- In **auto mode** (SDD `mode=auto`), the `default_api:ask_question` gate is suppressed for side-effect operations; the action is logged and executed immediately without a prompt.
- Safety invariants (no force-push, no `--no-verify`, protected-branch refusal, secrets detection, self-approval prohibition) are enforced unconditionally in both modes.
- Gated operations and commits MUST still be done using the formal slash command workflows from the `git` and `gh-cli` plugins (e.g. `/git:commit`, `/git:push`, `/gh-cli:pr-create`, `/gh-cli:pr-merge`) instead of raw shell commands.
```

### 2. `.sdd-docs/guidelines/product.md` (L23 removal + In-Scope addition)

- Remove L23: `- Automatic execution of repository-modifying actions without human-gated confirmation.`
- Append to In-Scope list: `- Auto-mode SDD workflow execution that runs P0–P9 end-to-end without interactive confirmation prompts, while preserving all safety invariants.`

### 3. `.sdd-docs/guidelines/rules.md` (L4, L14)

**L4 Before:**
```
- **Explicit Human Gates**: Gated confirmations are required for all repository-modifying actions (commits, pushes, pull request creations, and posting API reviews).
```
**L4 After:**
```
- **Explicit Human Gates**: In manual mode, gated confirmations are required for all repository-modifying actions (commits, pushes, pull request creations, and posting API reviews). In SDD auto mode, these gates are suppressed and actions proceed automatically; safety invariants remain unconditional in both modes.
```

**L14 Before:**
```
- **Interactive Question Gating**: Every side effect (commits, pushes, PR creation/approval/merge, tag creation/deletion) must use the interactive `default_api:ask_question` tool (grounded in `.sdd-docs/product/memory.md` and hard rules).
```
**L14 After:**
```
- **Interactive Question Gating**: In manual mode (or standalone skill invocation), every side effect (commits, pushes, PR creation/approval/merge, tag creation/deletion) must use the interactive `default_api:ask_question` tool. In SDD auto mode, the gate is suppressed and replaced by a logged action record. (Grounded in `.sdd-docs/product/memory.md` and hard rules.)
```

### 4. `.sdd-docs/guidelines/tech.md` (L28–29)

**Before:**
```
- Every side effect must be human-gated.
- Gated operations (commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges) MUST use the interactive `default_api:ask_question` tool (grounded in `.sdd-docs/product/memory.md`).
```
**After:**
```
- Side effects are mode-gated: in manual mode, every side effect MUST use the interactive `default_api:ask_question` tool; in SDD auto mode, the gate is suppressed and the action is logged automatically. (Grounded in `.sdd-docs/product/memory.md`.)
- Safety invariants (protected-branch refusal, no force-push, no `--no-verify`, secrets detection, self-approval prohibition) are unconditional and enforced in both modes.
```

### 5. `plugins/sdd/skills/run/SKILL.md` (7 targeted changes)

| Location | Before | After |
|---|---|---|
| L20 | `…stopping only for critical tool confirmations.` | `…without per-phase prompt or interactive confirmation dialogs.` |
| L51 (P0 receipt) | `Use \`default_api:ask_question\` to ask… with options…` | `In auto mode, log the feature receipt and proceed automatically. In manual mode, use \`default_api:ask_question\` to ask…` |
| L92 (P3 commit) | `Run \`/git:commit\` (ask for confirmation) to commit all docs.` | `Run \`/git:commit\` to commit all docs.` |
| L93 (P4 commit) | `Run \`/git:commit\` (ask for confirmation) to commit all implementation changes.` | `Run \`/git:commit\` to commit all implementation changes.` |
| L104 (P6 push) | `Run \`/git:push\` (request confirmation).` | `Run \`/git:push\`.` |
| L105 (P6 PR-create) | `Run \`/gh-cli:pr-create\` (request confirmation).` | `Run \`/gh-cli:pr-create\`.` |
| L141 (Done-when) | `The feature receipt was presented and confirmed by the user.` | `The feature receipt was presented and displayed to the user (confirmed in manual mode; logged in auto mode).` |

### 6. `plugins/sdd/rules/workflow-gating.md` (L7)

Apply standard clause replacing unconditional STOP with mode-conditional gate. Retain "Never commit or push on assumed consent in manual mode."

### 7. `plugins/git/rules/git-hard-rules.md` (L14)

Replace "Every side effect is human-gated" heading with "Side effects are mode-gated." Apply standard clause for auto/manual distinction. All other hard rules remain unconditional.

### 8. `plugins/gh-cli/rules/gh-hard-rules.md` (L9)

Same pattern as git-hard-rules.md L14. Self-approval prohibition, no-force-merge, secrets rules remain unconditional.

### 9–14. Skill Gate Steps (commit, push, branch-delete, pr-create, pr-merge, pr-respond)

Apply the standard clause to each gate step. Also update each skill's Done-when:
- Before: `The user explicitly confirmed… via the gate.`
- After: `The action was confirmed (manual mode) or logged (auto mode) before the operation ran.`

For `branch-delete`, also update the narrative line: `All deletions must be confirmed by the user.` → `All deletions must be confirmed by the user in manual mode, or logged before proceeding in auto mode.`

## Safety Invariants (Unconditional — Never Mode-Gated)

1. Protected-branch refusal (main/master/develop)
2. Force-push prohibition
3. `--no-verify` prohibition
4. Secrets detection before commit
5. Self-approval prohibition
6. No amend on pushed commits
7. No `reset --hard` on shared work

## Alternatives Considered

| Option | Verdict |
|---|---|
| New `--no-gate` flag per skill | Rejected — complexity; requires argument parser changes |
| Global env variable `SDD_MODE=auto` | Rejected — less portable than settings.json |
| Remove gates entirely | Rejected — breaks standalone use (US-6); violates NFR-2 |
| Separate auto-mode skill variants | Rejected — code duplication |
| **Context-propagation via settings.json (chosen)** | **Accepted** — zero new structures; minimal diff |

## Risks

| Risk | Mitigation |
|---|---|
| New gate added without mode-conditional clause | workflow-gating.md is canonical reference; AC-21 catches gaps |
| Standalone skill invoked in stale SDD context | Default-to-manual absent explicit SDD runner context |
| Safety invariant accidentally removed | Safety rules in separate bold-labelled bullets; never co-located with gate text |
