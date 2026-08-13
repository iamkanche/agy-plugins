---
name: sdd-run
description: Drive a feature work item through the full SDD phase model (P0 to P9) using specifications, system designs, task check-lists, testing loops, and persistent /goal execution.
model: flash
---

# /kanche:sdd-run

**Summary.** Drive a work item through the full SDD phase model (P0→P9): verify/load settings and memory, present a feature receipt for user confirmation, ensure a feature branch, delegate phase-specific execution (P1-P5) to token-optimized specialized subagents, run inner review loops (≤3x), validate and fix implementation (≤3x), deploy and poll PR comments (≤3x) to automatically respond/fix issues, promote documentation to product directories, preserve memory files, and hand over the final PR review and merge to the user. Supports `/goal` long-running persistent mode.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description (e.g. `improve-sdd-plugins` or `login`). If absent, prompt the user for it to construct the folder path `.docs/development/{slug}/`.
- **`--mode=auto|manual`** — default **auto**. Also accept a bare `auto`/`manual` positional.
  - **auto:** run the entire workflow (P0→P9) straight through, executing Level 2 automatically (checks PR status, runs validation checklists, syncs docs, and cleans up folders) without per-phase prompt or interactive confirmation dialogs.
  - **manual:** before advancing to each next phase, ask "Proceed to `<next phase>`? [Yes|No]". "No" stops the walk cleanly (state where it stopped).
- **`--goal` / `/goal`** — enable goal-driven persistent execution mode for long-running or overnight tasks. The workflow continuously self-audits, automatically retries failed steps up to policy limits, and appends `<!-- GOAL_COMPLETE -->` upon full completion.
- **`--from=<phase>`** — start the walk at this phase instead of P0 (`P0`..`P9`, or a name like `design`/`build`). Phases before it are assumed already done; do not re-run them.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 AI-validation, P6 deploy, and Level 2 entirely. Bound both ends: never run outside `[from, until]`.

If `--from`/`--until` are inconsistent (from > until), stop and report.

## Phase model

```
LEVEL 1 (AI: P0 - P7)
P0 setup   Receipt → /kanche:git-branch-create
P1 specs   /kanche:design-grill → loop ≤3x (/kanche:design-specs → /kanche:design-specs-review)
P2 design  loop ≤3x (/kanche:design-init → /kanche:design-review)
P3 tasks   loop ≤3x (/kanche:planner-tasks → /kanche:planner-review) → Docs Commit (/kanche:git-commit)
P4 build   loop ≤3x (/kanche:code-implement → /kanche:qa-review) → Implementation Commit (/kanche:git-commit)
P5 valid.  /kanche:qa-validate & fix (≤3x loop)
P6 deploy  /kanche:git-push → /kanche:gh-cli-pr-create → loop ≤3x (/kanche:gh-cli-pr-review → /kanche:gh-cli-pr-respond → /kanche:git-commit → /kanche:git-push)
P7 align   /kanche:sdd-sync → /kanche:git-commit (Promote dev docs → product docs, commit & push)

LEVEL 2 (Human: P8 - P9)
P8 human review  gated human-review /kanche:qa-validate (show verification checklist)
P9 PR merge      /kanche:gh-cli-pr-merge (user merges PR)
```

## Goal Mode Protocol (`/goal`)

When `--goal` or `/goal` is passed:
1. **Persistent Execution:** Do not abort on transient errors; attempt up to 3 automatic remediation loops for failed validations or code reviews.
2. **Self-Auditing:** Audit all output files (`.docs/development/{slug}/*`, implementation diffs, test logs) before moving across phase boundaries.
3. **Completion Marker:** Upon successfully completing the workflow, append `<!-- GOAL_COMPLETE -->` to the final summary output.

## Steps

### 0. Preconditions & Setup (P0)

1. **Verify Git Repo.**
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "NOT_A_GIT_REPO"
   ```
2. **Load settings & memory.** Check if `.docs/settings.json` exists. If so, parse settings (e.g. loops, polling time, custom commands). Read `.docs/product/memory.md` to load project-specific rules and constraints.
3. **Present Feature Receipt.** Generate a structured receipt for the user. Ask for confirmation before creating the feature branch:
   - Feature Slug: `{slug}`
   - Feature Title: derived from description/backlog
   - Based Branch: default remote branch (e.g. `main`)
   - Target PR Branch: default remote branch (e.g. `main`)
   - Branch Name to Create: `feat/{slug}` or similar
   - Execution Mode: `auto` or `manual` (from settings or argument)
     In auto mode, log the feature receipt (slug, branch, execution mode) and proceed automatically without prompting. In manual mode, use `default_api:ask_question` to ask: "Do you approve checking out this feature branch and starting development?" with options `(Recommended) Yes, proceed` and `No, abort`.
4. **Detect remote default branch.**
   ```bash
   DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
   DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
   DEFAULT=${DEFAULT:-main}
   CURRENT=$(git rev-parse --abbrev-ref HEAD)
   ```
5. **Ensure guidelines exist.** If `.docs/guidelines/` does not exist, stop and instruct the user to run `/kanche:sdd-init`.
6. **Ensure feature branch.** If `$CURRENT` matches `$DEFAULT` or is a protected branch (`main`, `master`, `develop`), create a feature branch using `/kanche:git-branch-create` as `feat/{slug}`.

### 3. Commit Checkpoint Policy

All commits across the SDD workflow (Docs, Implementation, PR respond fixes, and Product Alignment Sync) MUST execute via the **/kanche:git-commit** skill to enforce standardized Conventional Commits formatting:
- **P3 Docs Commit:** `/kanche:git-commit` with message `docs({slug}): add specs, design, and task checklist`
- **P4 Implementation Commit:** `/kanche:git-commit` with message `feat({slug}): implement feature logic and unit tests`
- **P6 PR Respond Fix Commit:** `/kanche:git-commit` with message `fix({slug}): address PR review feedback`
- **P7 Product Alignment Sync Commit:** `/kanche:git-commit` with message `docs({domain}): promote feature docs and sync product knowledge`

> ⚠️ **Mandatory Commit Rules:**
> 1. All commits MUST use multi-line HEREDOC format carrying `## Overview`, `## Changes`, and `## Impact` sections as specified in `plugins/kanche/skills/git-commit/SKILL.md`.
> 2. ❌ **Prohibited:** Never execute inline single-line `git commit -m "..."` commands or merge commits into multi-command shell chains (e.g. `git commit -m ... && git push`). Every commit step MUST be an isolated invocation of `/kanche:git-commit`.

### P1–P4 — Inner Review Loops (Delegated to Token-Optimized Subagents & Loop Engineering Protocol)

To optimize token consumption and enforce continuous quality, the parent agent delegates Phase P1-P4 workflows to specialized subagents under the **Loop Engineering Framework (`plugins/kanche/rules/loop-engineering.md`)**. **Every phase review is FORCED and MANDATORY**: each generator phase MUST automatically execute its paired reviewer workflow immediately after generation, running a closed-loop retry cycle up to **3** times until a `GO` verdict is achieved.

| Phase | Subagent | Model | Generator Skill | Reviewer / Evaluator Skill (≤3x Loop) | Commit Gate (via `/kanche:git-commit`) |
|---|---|---|---|---|---|
| **P1 Specs** | `analyst` | `pro` | `/kanche:design-grill` (first cycle) then `/kanche:design-specs` | `/kanche:design-specs-review` | None |
| **P2 Design** | `architect` | `pro` | `/kanche:design-init` | `/kanche:design-review` | None |
| **P3 Tasks** | `planner` | `pro` | `/kanche:planner-tasks` | `/kanche:planner-review` | **Docs Commit** (`/kanche:git-commit -m "docs({slug}): ..."`) |
| **P4 Build** | `coder` | `flash` | `/kanche:code-implement` | `/kanche:code-review` / `/kanche:qa-review` | **Implementation Commit** (`/kanche:git-commit -m "feat({slug}): ..."`) |

For each phase:

1. **Delegate execution & mandatory review.** Spawn the corresponding subagent (`analyst`, `architect`, `planner`, or `coder`) with explicit instructions outlining the phase goal. **The subagent MUST invoke `view_file` on `plugins/kanche/skills/<skill>/SKILL.md` before executing any workflow or underlying command**, and automatically run both the generator skill AND the reviewer skill in sequence following `plugins/kanche/rules/loop-engineering.md`.
2. **Review verdict.** The subagent runs the review skill (P1: `/kanche:design-specs-review`, P2: `/kanche:design-review`, P3: `/kanche:planner-review`, P4: `/kanche:code-review` / `/kanche:qa-review`) and parses the `verdict:` output from:
   ```sdd-review
   verdict: GO            # or NO-GO
   loop_iteration: 1/3    # current iteration / max_loops
   findings:
     - severity: blocker  # blocker | major | nit
       msg: "..."
       file: "..."
       line: 123
       fix_suggestion: "..."
   ```

   - **GO** → Proceed to the next phase.
   - **NO-GO** and cycles remaining (up to 3x) → Re-run generator skill with targeted delta fixes addressing `findings`, then automatically re-run reviewer skill.
   - **NO-GO** on 3rd cycle → In `auto` mode, stop the workflow and report findings. In `manual` mode, ask via `default_api:ask_question` whether to `Proceed anyway` or `Stop`.
3. **Commit checkpoints.**
   - End of P3: Run `/kanche:git-commit` with conventional prefix `docs({slug}): ...` to commit all docs.
   - End of P4: Run `/kanche:git-commit` with conventional prefix `feat({slug}): ...` to commit all implementation changes.


### P5 — AI Validation & Fix Loop (Delegated to `validator`)

1. **Delegate validation.** Invoke the `validator` subagent to run `/kanche:qa-validate` (tests / lint / validations).
2. **Handle failures.** If validate fails:
   - **Under auto mode:** Re-enter P4 (build) automatically up to 3 times to apply fixes, and re-run validation. If still failing after 3 attempts, abort and report failures.
   - **Under manual mode:** Ask "Validation failed" via `default_api:ask_question` with options `Fix via build loop`, `Continue to deploy`, and `Stop`.

### P6 — Deploy & AI PR Review/Respond Loop

1. **Push branch.** Run `/kanche:git-push`.
2. **Create PR.** Run `/kanche:gh-cli-pr-create`.
3. **AI PR Review & Respond Loop (≤3x Loop).** Run `/kanche:gh-cli-pr-review` to audit the PR diff against project guidelines and post review comments on GitHub. If review feedback exists, automatically execute `/kanche:gh-cli-pr-respond` → `/kanche:git-commit` (with conventional message `fix({slug}): address PR review feedback`) → `/kanche:git-push` up to 3 times to parse feedback, apply code fixes, re-validate (P5), commit, and push updates to origin.

### P7 — Product Alignment & Doc Sync (LEVEL 1 AI Final Step)

1. **Promote documentation.** Run `/kanche:sdd-sync` locally on the feature branch (promotes dev docs to domain product directories under `.docs/product/{domain}/`, removes the dev folder `.docs/development/{slug}/`, commits via `/kanche:git-commit` with conventional message `docs({domain}): promote feature docs and sync product knowledge`, and pushes updates to origin feature branch).

### P8–P9 — Level 2 (Human Review & PR Merge)

In **auto** mode, LEVEL 1 (P0-P7) runs automatically end-to-end. LEVEL 2 begins at P8 where the user is presented with the interactive verification checklist and PR merge gate.

- **P8 Gated Human Review.**
  - Present the interactive verification checklist via `/kanche:qa-validate` (shows test results, lint checks, and checklist items) and ask for human review approval using `default_api:ask_question`.

- **P9 PR Merge.**
  - Execute PR merge via `/kanche:gh-cli-pr-merge` upon human confirmation, or hand over final merge to the user on GitHub.

### 10. Notify User (P10)

Upon completion or abortion, brief the user with a summary:

- Final status (e.g. Ready for Human Review & PR Merge, or Aborted)
- Summary of documentation and implementation edits made
- Direct link to the open PR and feature logs
- **Hand over to Level 2:** Present P8 human review checklist and prompt for P9 PR merge approval.
- **Ask for feedback:** Show a prompt requesting feedback on the automation run.
- **Ask for deployment:** Request if they want to deploy the feature further (e.g. production servers), saving preferences/instructions to memory if they want the agent to remember it.
- **Goal Mode Marker:** Include `<!-- GOAL_COMPLETE -->` if `/goal` was active.

## Done when

- All in-bounds phases ran in order.
- The feature receipt was presented and displayed to the user (confirmed in manual mode; logged in auto mode).
- Subagent delegation was performed to conserve tokens.
- LEVEL 1 AI (P0-P7) ran specs, design, tasks, build, validation, deploy, 3x PR review/respond loop, and sdd-sync.
- Product docs were promoted to domain directories in P7 (`.docs/product/{domain}/`).
- LEVEL 2 Human (P8-P9) presented gated human review checklist at P8 and PR merge at P9.
- Memory and settings files were preserved.
- If `/goal` mode was requested, `<!-- GOAL_COMPLETE -->` tag is appended to final response upon completion.
