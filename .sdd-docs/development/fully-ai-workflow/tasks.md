# Tasks: Remove Ask-Question Gates from SDD Auto Mode

> Feature: `fully-ai-workflow`
> Design ref: `design.md` · Specs ref: `specs.md`
> AC traceability is noted per task as `→ AC-N`.

---

## Phase 1 — Policy Documents (4 files)

_Edit the authoritative steering guidelines to establish mode-conditional gate policy. These are the canonical source; all downstream files reference them. Must be done before Group 2–4 edits._

- [ ] **[T-1.1]** Edit `.sdd-docs/product/memory.md` L5–7: replace the three unconditional `ask_question` mandate bullets with the three mode-conditional bullets specified in `design.md §1`:
  - Bullet 1 (L5): manual mode gates on `default_api:ask_question`.
  - Bullet 2 (L6): auto mode suppresses the gate; action is logged and executed immediately.
  - Bullet 3 (L7): safety invariants (no force-push, no `--no-verify`, protected-branch refusal, secrets detection, self-approval prohibition) are unconditional in both modes.
  - Retain L8 (plugin enforcement rule) verbatim — no changes below L7.
  - _File_: `.sdd-docs/product/memory.md` · `→ AC-1`

- [ ] **[T-1.2]** Edit `.sdd-docs/guidelines/product.md`:
  - Remove L23 (`- Automatic execution of repository-modifying actions without human-gated confirmation.`) from the Out-of-Scope list.
  - Append to the In-Scope list: `- Auto-mode SDD workflow execution that runs P0–P9 end-to-end without interactive confirmation prompts, while preserving all safety invariants.`
  - _File_: `.sdd-docs/guidelines/product.md` · `→ AC-2`

- [ ] **[T-1.3]** Edit `.sdd-docs/guidelines/rules.md`:
  - L4 (`**Explicit Human Gates**`): replace unconditional mandate with mode-conditional text per `design.md §3` — manual mode requires gated confirmations; SDD auto mode suppresses them; safety invariants remain unconditional in both modes.
  - L14 (`**Interactive Question Gating**`): replace unconditional mandate with mode-conditional text — manual/standalone: `default_api:ask_question` fires; auto mode: gate suppressed, replaced by logged action record.
  - All other lines (L1–L3, L5–L13, L15–L16) remain verbatim.
  - _File_: `.sdd-docs/guidelines/rules.md` · `→ AC-3`

- [ ] **[T-1.4]** Edit `.sdd-docs/guidelines/tech.md` L28–29:
  - Replace two unconditional gate lines with two mode-conditional equivalents per `design.md §4`:
    - New L28: side effects are mode-gated (manual = `ask_question`, auto = logged automatically).
    - New L29: safety invariants are unconditional and enforced in both modes.
  - All other lines remain verbatim.
  - _File_: `.sdd-docs/guidelines/tech.md` · `→ AC-4`

---

## Phase 2 — Plugin Hard Rules (3 files)

_Update rule files that plugin skills directly cite. Depends on Phase 1 (authoritative policy must exist first). Each rule file must preserve all 7 safety invariant bullets unchanged._

- [ ] **[T-2.1]** Edit `plugins/sdd/rules/workflow-gating.md` L7 (`**Side Effect Confirmation**`):
  - Rewrite to mode-conditional using the Standard Clause from `design.md §Standard Clause`: auto mode → log the action (what will be written, exact command, target branch) and proceed; manual mode → STOP and ask using `default_api:ask_question` with `(Recommended) Yes, proceed` / `No, abort`.
  - Append to the clause: "Never commit or push on assumed consent in manual mode."
  - Lines 1–6 and L8–L11 remain verbatim.
  - _File_: `plugins/sdd/rules/workflow-gating.md` · `→ AC-5`

- [ ] **[T-2.2]** Edit `plugins/git/rules/git-hard-rules.md` L14 (`**Every side effect is human-gated.**`):
  - Replace heading and text with mode-conditional version: "**Side effects are mode-gated.**" Apply the Standard Clause (auto → log + proceed; manual → STOP + `ask_question` with Proceed/Abort options).
  - Lines 1–13 (all 7 safety invariants and supporting rules) remain verbatim and unconditional.
  - _File_: `plugins/git/rules/git-hard-rules.md` · `→ AC-6`

- [ ] **[T-2.3]** Edit `plugins/gh-cli/rules/gh-hard-rules.md` L9 (`**Every side effect is human-gated.**`):
  - Same pattern as T-2.2: replace heading with "**Side effects are mode-gated.**" and apply Standard Clause.
  - Lines 1–8 (self-approval prohibition, no-force-merge, COMMENT default, secrets rule) remain verbatim and unconditional.
  - _File_: `plugins/gh-cli/rules/gh-hard-rules.md` · `→ AC-7`

---

## Phase 3 — `run/SKILL.md` (7 targeted changes in one file)

_Seven discrete, line-targeted edits to `plugins/sdd/skills/run/SKILL.md`. Depends on Phase 2 (rule files updated). Apply all 7 edits in a single multi-replace operation to avoid intermediate-state conflicts._

- [ ] **[T-3.1]** L20 — Auto mode description: remove `stopping only for critical tool confirmations`. Replace the end of the auto-mode sentence with `without per-phase prompt or interactive confirmation dialogs.`
  - _File_: `plugins/sdd/skills/run/SKILL.md` L20 · `→ AC-8`

- [ ] **[T-3.2]** P0 receipt — Step 3 (L51–L58): make `ask_question` manual-mode-only.
  - Replace the blanket `Use default_api:ask_question to ask…` sentence (currently applies regardless of mode) with two-branch logic:
    - Auto mode: log the feature receipt (slug, branch, execution mode) and proceed automatically without prompting.
    - Manual mode: use `default_api:ask_question` to ask `"Do you approve checking out this feature branch and starting development?"` with options `(Recommended) Yes, proceed` and `No, abort`.
  - _File_: `plugins/sdd/skills/run/SKILL.md` L51–L58 · `→ AC-9`

- [ ] **[T-3.3]** P3 commit checkpoint (L92): remove `(ask for confirmation)`.
  - Change: `Run \`/git:commit\` (ask for confirmation) to commit all docs.` → `Run \`/git:commit\` to commit all docs.`
  - _File_: `plugins/sdd/skills/run/SKILL.md` L92 · `→ AC-10`

- [ ] **[T-3.4]** P4 commit checkpoint (L93): remove `(ask for confirmation)`.
  - Change: `Run \`/git:commit\` (ask for confirmation) to commit all implementation changes.` → `Run \`/git:commit\` to commit all implementation changes.`
  - _File_: `plugins/sdd/skills/run/SKILL.md` L93 · `→ AC-10`

- [ ] **[T-3.5]** P6 push (L104): remove `(request confirmation)`.
  - Change: `Run \`/git:push\` (request confirmation).` → `Run \`/git:push\`.`
  - _File_: `plugins/sdd/skills/run/SKILL.md` L104 · `→ AC-11`

- [ ] **[T-3.6]** P6 PR-create (L105): remove `(request confirmation)`.
  - Change: `Run \`/gh-cli:pr-create\` (request confirmation).` → `Run \`/gh-cli:pr-create\`.`
  - _File_: `plugins/sdd/skills/run/SKILL.md` L105 · `→ AC-11`

- [ ] **[T-3.7]** Done-when (L141): update confirmation language.
  - Change: `The feature receipt was presented and confirmed by the user.` → `The feature receipt was presented and displayed to the user (confirmed in manual mode; logged in auto mode).`
  - _File_: `plugins/sdd/skills/run/SKILL.md` L141 · `→ AC-12`

---

## Phase 4 — Skill Gate Steps (6 files)

_Apply the Standard Clause to individual skill gate steps. These depend on Phase 2 (hard rules) being updated first. Each change is independent of the others and may be applied in parallel `[P]`._

- [ ] **[T-4.1]** [P] Edit `plugins/git/skills/commit/SKILL.md`:
  - **Gate Step 7** (L63): replace the unconditional `STOP and ask the user to confirm…` text with the Standard Clause (auto → log + proceed; manual → show `default_api:ask_question` with `(Recommended) Yes, commit these changes` / `No, abort commit`).
  - **Done-when** (L118): change `The user explicitly confirmed the message via the gate before the commit ran.` → `The action was confirmed (manual mode) or logged (auto mode) before the commit ran.`
  - All other lines (steps 1–6, 8–9, commit message structure, hard rules section) remain verbatim.
  - _File_: `plugins/git/skills/commit/SKILL.md` · `→ AC-13`

- [ ] **[T-4.2]** [P] Edit `plugins/git/skills/push/SKILL.md`:
  - **Gate Step 5** (L50): replace the unconditional `STOP and ask the user to confirm pushing…` text with the Standard Clause (auto → log exact command + ahead/behind summary + proceed; manual → show `default_api:ask_question` with `(Recommended) Yes, proceed with push` / `No, abort push`).
  - **Done-when** (L67): change `The user explicitly confirmed the push via the gate.` → `The action was confirmed (manual mode) or logged (auto mode) before the push ran.`
  - All other lines remain verbatim.
  - _File_: `plugins/git/skills/push/SKILL.md` · `→ AC-14`

- [ ] **[T-4.3]** [P] Edit `plugins/git/skills/branch-delete/SKILL.md`:
  - **Gate Step 5** (L54): replace the unconditional `STOP and ask the user to confirm…` text with the Standard Clause (auto → log target branch + scope + proceed; manual → show `default_api:ask_question` with `(Recommended) Yes, proceed with deletion` / `No, abort`). Protected-branch refusal (Step 2) remains unconditional.
  - **git hard rules narrative** (L76): change `All deletions must be confirmed by the user.` → `All deletions must be confirmed by the user in manual mode, or logged before proceeding in auto mode.`
  - **Done-when** (L82): change `The action was explicitly confirmed via the gate.` → `The action was confirmed (manual mode) or logged (auto mode) before deletion ran.`
  - All other lines remain verbatim.
  - _File_: `plugins/git/skills/branch-delete/SKILL.md` · `→ AC-15`

- [ ] **[T-4.4]** [P] Edit `plugins/gh-cli/skills/pr-create/SKILL.md`:
  - **Gate Step 6** (L55): replace the unconditional `STOP and ask the user to confirm opening this pull request…` text with the Standard Clause (auto → log title + body + base branch + draft flag + proceed; manual → show `default_api:ask_question` with `(Recommended) Yes, create PR` / `No, abort`).
  - **Done-when** (L73): change `The user explicitly confirmed the title + body via the gate before creation.` → `The action was confirmed (manual mode) or logged (auto mode) before the PR was created.`
  - All other lines remain verbatim.
  - _File_: `plugins/gh-cli/skills/pr-create/SKILL.md` · `→ AC-16`

- [ ] **[T-4.5]** [P] Edit `plugins/gh-cli/skills/pr-merge/SKILL.md`:
  - **Gate Step 4** (L43): replace the unconditional `STOP and ask the user to confirm…` text with the Standard Clause (auto → log PR title + number + base branch + merge method + delete-branch flag + proceed; manual → show `default_api:ask_question` with `(Recommended) Yes, merge PR` / `No, abort`).
  - **Done-when** (L77): change `The action was explicitly confirmed via the gate.` → `The action was confirmed (manual mode) or logged (auto mode) before the merge ran.`
  - All other lines remain verbatim.
  - _File_: `plugins/gh-cli/skills/pr-merge/SKILL.md` · `→ AC-17`

- [ ] **[T-4.6]** [P] Edit `plugins/gh-cli/skills/pr-respond/SKILL.md`:
  - **Gate Step 5 — Triage Review** (L41): replace `STOP and show the user the list…` with Standard Clause (auto → log triage plan + proceed; manual → show `default_api:ask_question` with `(Recommended) Yes, proceed with response` / `No, abort`).
  - **Gate Step 8 — Reply Confirmation** (L53): replace `STOP and present the final text replies…` with Standard Clause (auto → log push status + reply content + proceed; manual → show `default_api:ask_question` with `(Recommended) Yes, post replies` / `No, abort`).
  - **Done-when** (L71): change `Proposed code changes and replies were reviewed and approved by the user.` → `Proposed code changes and replies were confirmed (manual mode) or logged (auto mode) before execution.`
  - All other lines remain verbatim.
  - _File_: `plugins/gh-cli/skills/pr-respond/SKILL.md` · `→ AC-18`

---

## Phase 5 — Verification Checkpoints

_Run after all 14 file edits in Phases 1–4 are committed. Each check is independent `[P]`._

- [ ] **[T-5.1]** [P] Grep all 14 edited files for the phrase `MUST use the interactive` without a mode qualifier (`manual` or `auto` appearing in the same sentence or bullet). Zero unqualified occurrences expected.
  - Command: `grep -rn "MUST use the interactive" .sdd-docs/product/memory.md .sdd-docs/guidelines/ plugins/sdd/rules/ plugins/git/rules/ plugins/gh-cli/rules/ plugins/sdd/skills/run/SKILL.md plugins/git/skills/commit/SKILL.md plugins/git/skills/push/SKILL.md plugins/git/skills/branch-delete/SKILL.md plugins/gh-cli/skills/pr-create/SKILL.md plugins/gh-cli/skills/pr-merge/SKILL.md plugins/gh-cli/skills/pr-respond/SKILL.md`
  - _Expected_: no unqualified matches. `→ AC-21, NFR-1`

- [ ] **[T-5.2]** [P] Verify all 7 safety invariants remain present and unconditional in `plugins/git/rules/git-hard-rules.md` and `plugins/gh-cli/rules/gh-hard-rules.md`:
  1. `Never force-push`
  2. `Never use --no-verify`
  3. `Never amend a pushed commit`
  4. `Never git reset --hard`
  5. `Never commit secrets`
  6. `Never work on a protected branch`
  7. `Never delete remote protected branches` (git) / `Never approve your own PR` + `Never force-merge` (gh-cli)
  - Command: `grep -n "Never" plugins/git/rules/git-hard-rules.md plugins/gh-cli/rules/gh-hard-rules.md`
  - _Expected_: all 7 invariant lines present, none surrounded by mode-conditional language. `→ AC-19, NFR-3`

- [ ] **[T-5.3]** [P] Verify `plugins/sdd/skills/run/SKILL.md` manual mode description still references `ask_question` gates.
  - Command: `grep -n "ask_question\|manual mode" plugins/sdd/skills/run/SKILL.md`
  - _Expected_: at least one line with manual-mode `ask_question` usage (e.g., P7–P9 manual gates). `→ AC-20`

- [ ] **[T-5.4]** [P] Verify `.sdd-docs/guidelines/product.md` no longer lists ungated auto-execution as Out-of-Scope, and new In-Scope entry is present.
  - Commands:
    - `grep -n "Automatic execution" .sdd-docs/guidelines/product.md` → _Expected_: no output.
    - `grep -n "Auto-mode SDD" .sdd-docs/guidelines/product.md` → _Expected_: one matching line. `→ AC-2`

- [ ] **[T-5.5]** [P] Verify `.sdd-docs/settings.json` is unchanged — still contains `"mode": "auto"` and no new keys were added.
  - Command: `cat .sdd-docs/settings.json`
  - _Expected_: identical content to the pre-change snapshot; `"mode": "auto"` present; no new keys. `→ specs Out-of-Scope`

---

## Verification Summary Table

> This feature modifies only Markdown policy and skill files. There is no compiled code, no build step, and no automated test suite in this repository (see `guidelines/tech.md`). Verification is performed via the grep/cat commands in Phase 5.

| Acceptance Criterion | Implementing Task(s) | Verification Task | Verification Command / Check |
|---|---|---|---|
| AC-1 memory.md mode-conditional | T-1.1 | T-5.1 | grep unqualified `ask_question` mandate → 0 |
| AC-2 product.md removal + addition | T-1.2 | T-5.4 | grep `"Automatic execution"` → 0; grep `"Auto-mode SDD"` → 1 |
| AC-3 rules.md L4, L14 updated | T-1.3 | T-5.1 | grep unqualified phrase → 0 |
| AC-4 tech.md L28-29 updated | T-1.4 | T-5.1 | grep unqualified phrase → 0 |
| AC-5 workflow-gating.md L7 updated | T-2.1 | T-5.1 | grep unqualified phrase → 0 |
| AC-6 git-hard-rules.md L14 updated | T-2.2 | T-5.2 | inspect invariant bullets present |
| AC-7 gh-hard-rules.md L9 updated | T-2.3 | T-5.2 | inspect invariant bullets present |
| AC-8 run/SKILL.md L20 no blocking phrase | T-3.1 | T-5.1 | grep `"stopping only for critical"` → 0 |
| AC-9 P0 receipt manual-only `ask_question` | T-3.2 | T-5.3 | grep `ask_question` in manual context |
| AC-10 P3/P4 `(ask for confirmation)` removed | T-3.3, T-3.4 | T-5.1 | grep `"ask for confirmation"` → 0 |
| AC-11 P6 `(request confirmation)` removed | T-3.5, T-3.6 | T-5.1 | grep `"request confirmation"` → 0 |
| AC-12 Done-when updated | T-3.7 | T-5.3 | grep `"displayed to the user"` in run/SKILL.md → 1 |
| AC-13 commit/SKILL.md gate conditionalized | T-4.1 | T-5.1 | grep across skill file |
| AC-14 push/SKILL.md gate conditionalized | T-4.2 | T-5.1 | grep across skill file |
| AC-15 branch-delete/SKILL.md gate conditionalized | T-4.3 | T-5.1 | grep across skill file |
| AC-16 pr-create/SKILL.md gate conditionalized | T-4.4 | T-5.1 | grep across skill file |
| AC-17 pr-merge/SKILL.md gate conditionalized | T-4.5 | T-5.1 | grep across skill file |
| AC-18 pr-respond/SKILL.md gates conditionalized | T-4.6 | T-5.1 | grep across skill file |
| AC-19 7 safety invariants unconditional | T-2.2, T-2.3 | T-5.2 | grep `Never` in hard rules |
| AC-20 Manual mode behavior unchanged | T-3.1–T-3.7, T-4.1–T-4.6 | T-5.3 | grep `ask_question` in manual branches |
| AC-21 Zero contradictory gate language | All Phase 1–4 | T-5.1 | no unqualified mandate phrases |
