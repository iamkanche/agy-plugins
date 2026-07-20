# Specs: Remove Ask-Question Gates from SDD Auto Mode

## Context

The SDD workflow (`/sdd:run`) is designed to automate software delivery from P0 (setup) through P9 (merge). However, the current policy — encoded in `memory.md`, `rules.md`, `tech.md`, `workflow-gating.md`, and the `git`/`gh-cli` hard-rules — mandates `default_api:ask_question` interactive confirmation dialogs before every repository-modifying side effect (commits, pushes, PR creation, PR merge, branch deletion).

These confirmation gates defeat the purpose of the `auto` execution mode. The user wants the SDD workflow to run end-to-end without any interactive prompts when `mode=auto` — making it genuinely unattended.

This change updates the authoritative policy documents and the individual skill Gate steps to make confirmation dialogs mode-conditional: suppressed in `auto` mode, retained in `manual` mode. Safety invariants (no force-push, no secrets, protected-branch refusal, self-approval prohibition) remain unconditionally enforced regardless of mode.

## Scope

### In-Scope

- **`memory.md`**: Replace universal `ask_question` mandate with mode-conditional rule.
- **`product.md`**: Remove L23 out-of-scope entry; reflect auto-mode as a supported feature.
- **`rules.md`**: Make L4 and L14 mode-conditional.
- **`tech.md`**: Update Known Technical Constraints (L28-29) to reflect mode-conditional gating.
- **`workflow-gating.md`**: Rewrite L7 to be mode-conditional.
- **`git-hard-rules.md`**: Rewrite L14 to be mode-conditional.
- **`gh-hard-rules.md`**: Rewrite L9 to be mode-conditional.
- **`run/SKILL.md`**: Remove `(ask for confirmation)` / `(request confirmation)` from auto-mode descriptions at L20, L51-58, L92-93, L104-105, L141.
- **`git/skills/commit/SKILL.md`**: Gate step 7 conditionalized.
- **`git/skills/push/SKILL.md`**: Gate step 5 conditionalized.
- **`git/skills/branch-delete/SKILL.md`**: Gate step 5 conditionalized.
- **`gh-cli/skills/pr-create/SKILL.md`**: Gate step 6 conditionalized.
- **`gh-cli/skills/pr-merge/SKILL.md`**: Gate step 4 conditionalized.
- **`gh-cli/skills/pr-respond/SKILL.md`**: Gate steps 5 + 8 conditionalized.

### Out of Scope / Non-Goals

- `settings.json` — already `"mode": "auto"`, no new key needed.
- `git` skills not in SDD pipeline (rebase, tag-*, stash, fetch, pull, switch) — unchanged.
- `gh-cli` skills not in SDD pipeline (pr-approve, pr-review, pr-list) — unchanged.
- `git/skills/branch-create/SKILL.md` — already gate-free.
- P10 feedback prompts — post-run user interaction, not side-effect gates.
- Safety invariants — unconditional hard STOPs; never removed.
- `manual` mode behavior — all existing gate behavior preserved exactly.

## User Stories

- **US-1:** As a developer running `/sdd:run my-feature`, I want the entire P0–P9 pipeline to execute without any `ask_question` dialogs in auto mode.
- **US-2:** As a developer running `/sdd:run my-feature --mode=manual`, I want all existing confirmation gates to fire as before.
- **US-3:** As a developer in auto mode, I want the P0 feature receipt displayed as a plain log, not a blocking prompt.
- **US-4:** As a developer in auto mode, I want commits, pushes, PR creation, and PR merge to happen automatically.
- **US-5:** As a developer, when the pipeline fails in auto mode, I want a clean abort with a full action audit log.
- **US-6:** As a plugin user using git/gh-cli skills directly, I want the confirmation gate to still fire for standalone use.
- **US-7:** As an AI agent reading the policy documents, I want consistent, unambiguous rules across all files.

## Acceptance Criteria

### Policy Documents
- **AC-1:** `memory.md` — mode-conditional rule: auto mode = no gates; manual mode = ask_question fires.
- **AC-2:** `product.md` — remove L23 out-of-scope entry; add auto-mode as supported.
- **AC-3:** `rules.md` — L4 and L14 updated to be mode-conditional.
- **AC-4:** `tech.md` — L28-29 reflect mode-conditional gating.
- **AC-5:** `workflow-gating.md` — L7 Side Effect Confirmation is mode-conditional.
- **AC-6:** `git-hard-rules.md` — L14 mode-conditional; all other hard rules unconditional.
- **AC-7:** `gh-hard-rules.md` — L9 mode-conditional; self-approval/no-force-merge unconditional.

### `run/SKILL.md`
- **AC-8:** Auto mode description does NOT contain "stopping only for critical tool confirmations."
- **AC-9:** P0 receipt: displayed as plain log in auto mode; `ask_question` fires only in manual mode.
- **AC-10:** P3/P4 commit checkpoints: `(ask for confirmation)` removed from auto-mode text.
- **AC-11:** P6 push/PR-create: `(request confirmation)` removed from auto-mode text.
- **AC-12:** Done-when: "confirmed by the user" → "displayed to the user."

### Skill Gate Steps (AC-13 to AC-18)
Each skill's Gate step gains: "If called from SDD auto mode, proceed automatically. If invoked standalone or from manual mode, show this gate."
- **AC-13:** `git/skills/commit/SKILL.md` Gate step 7.
- **AC-14:** `git/skills/push/SKILL.md` Gate step 5.
- **AC-15:** `git/skills/branch-delete/SKILL.md` Gate step 5 (protected-branch check remains unconditional).
- **AC-16:** `gh-cli/skills/pr-create/SKILL.md` Gate step 6.
- **AC-17:** `gh-cli/skills/pr-merge/SKILL.md` Gate step 4.
- **AC-18:** `gh-cli/skills/pr-respond/SKILL.md` Gate steps 5 + 8.

### Safety & Regression
- **AC-19:** All 7 unconditional hard STOPs remain (protected-branch refusal, no force-push, no `--no-verify`, secrets detection, self-approval prohibition, no amend on pushed commits, no `reset --hard`).
- **AC-20:** Manual mode — all existing gate behavior fires identically to today.
- **AC-21:** After all 14 files updated, zero contradictory gate language across any two files.

## Data Model

| # | File | Change |
|---|---|---|
| 1 | `.sdd-docs/product/memory.md` | Replace L5-7 |
| 2 | `.sdd-docs/guidelines/product.md` | Remove L23; update In-Scope |
| 3 | `.sdd-docs/guidelines/rules.md` | Update L4, L14 |
| 4 | `.sdd-docs/guidelines/tech.md` | Update L28-29 |
| 5 | `plugins/sdd/skills/run/SKILL.md` | 7 targeted changes |
| 6 | `plugins/sdd/rules/workflow-gating.md` | Rewrite L7 |
| 7 | `plugins/git/rules/git-hard-rules.md` | Rewrite L14 |
| 8 | `plugins/gh-cli/rules/gh-hard-rules.md` | Rewrite L9 |
| 9 | `plugins/git/skills/commit/SKILL.md` | Gate step 7 conditionalized |
| 10 | `plugins/git/skills/push/SKILL.md` | Gate step 5 conditionalized |
| 11 | `plugins/git/skills/branch-delete/SKILL.md` | Gate step 5 conditionalized |
| 12 | `plugins/gh-cli/skills/pr-create/SKILL.md` | Gate step 6 conditionalized |
| 13 | `plugins/gh-cli/skills/pr-merge/SKILL.md` | Gate step 4 conditionalized |
| 14 | `plugins/gh-cli/skills/pr-respond/SKILL.md` | Gate steps 5 + 8 conditionalized |

## NFR

- **NFR-1 Consistency:** All 14 files derive a consistent, unambiguous auto/manual gate policy.
- **NFR-2 Backward Compatibility:** Manual mode behavior bit-for-bit identical to today.
- **NFR-3 Safety Invariant Preservation:** All 7 unconditional hard STOPs survive.
- **NFR-4 Auditability:** Auto mode logs every side-effect action; abort emits full action audit.
- **NFR-5 Minimal Diff:** Only gate-related lines changed; no unrelated prose changes.
