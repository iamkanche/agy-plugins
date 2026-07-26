---
name: sdd-run
description: Drive a feature work item through the full SDD phase model (P0 to P9) using specifications, system designs, task check-lists, and testing loops.
---

# /kanche:sdd-run

**Summary.** Drive a work item through the full SDD phase model (P0→P9): verify/load settings and memory, present a feature receipt for user confirmation, ensure a feature branch, delegate phase-specific execution (P1-P5) to token-optimized specialized subagents, run inner review loops (≤3x), validate and fix implementation (≤3x), deploy and poll PR comments (≤3x) to automatically respond/fix issues, promote documentation to product directories, preserve memory files, and hand over the final PR review and merge to the user.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description (e.g. `improve-sdd-plugins` or `login`). If absent, prompt the user for it to construct the folder path `docs/development/{slug}/`.
- **`--mode=auto|manual`** — default **auto**. Also accept a bare `auto`/`manual` positional.
  - **auto:** run the entire workflow (P0→P9) straight through, executing Level 2 automatically (checks PR status, runs validation checklists, syncs docs, and cleans up folders) without per-phase prompt or interactive confirmation dialogs.
  - **manual:** before advancing to each next phase, ask "Proceed to `<next phase>`? [Yes|No]". "No" stops the walk cleanly (state where it stopped).
- **`--from=<phase>`** — start the walk at this phase instead of P0 (`P0`..`P9`, or a name like `design`/`build`). Phases before it are assumed already done; do not re-run them.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 AI-validation, P6 deploy, and Level 2 entirely. Bound both ends: never run outside `[from, until]`.

If `--from`/`--until` are inconsistent (from > until), stop and report.

## Phase model

```
LEVEL 1 (AI + Subagents)
P0 setup   Receipt → /kanche:git-branch-create
P1 specs   /kanche:design-grill → /kanche:design-specs → FORCED /kanche:design-specs-review (Analyst, ≤3x loop)
P2 design  /kanche:design-init → FORCED /kanche:design-review (Architect, ≤3x loop)
P3 tasks   /kanche:planner-tasks → FORCED /kanche:planner-review → Docs Commit (Planner, ≤3x loop)
P4 build   /kanche:dev-implement → FORCED /kanche:qa-review → Code Commit (Coder, ≤3x loop)
P5 valid.  /kanche:qa-validate & fix (Validator, ≤3x loop)
P6 deploy  /kanche:git-push → /kanche:gh-cli-pr-create → loop ≤3x (/kanche:gh-cli-pr-review → /kanche:gh-cli-pr-respond)

LEVEL 2 (Full AI Automation + Human Merge)
P9 alignment     /kanche:sdd-sync (Promote dev docs → product docs & push)
P7 human review  /kanche:qa-validate (Human review & verification checklist)
P8 PR merge      User merges the PR (or /kanche:gh-cli-pr-merge by user)
```

## Steps

### 0. Preconditions & Setup (P0)

1. **Verify Git Repo.**
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "NOT_A_GIT_REPO"
   ```
2. **Load settings & memory.** Check if `docs/settings.json` exists. If so, parse settings (e.g. loops, polling time, custom commands). Read `docs/product/memory.md` to load project-specific rules and constraints.
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
5. **Ensure guidelines exist.** If `docs/guidelines/` does not exist, stop and instruct the user to run `/kanche:sdd-init`.
6. **Ensure feature branch.** If `$CURRENT` matches `$DEFAULT` or is a protected branch (`main`, `master`, `develop`), create a feature branch using `/kanche:git-branch-create` as `feat/{slug}`.

### P1–P4 — Inner Review Loops (Delegated to Token-Optimized Subagents)

To optimize token consumption, the parent agent delegates Phase P1-P4 workflows to specialized subagents. **Every phase review is FORCED and MANDATORY**: each phase MUST automatically execute its paired review workflow immediately after generation, running a retry loop up to **3** times until a `GO` verdict is achieved.

| Phase | Subagent | Generate Workflow | Mandatory Review Workflow (Forced, ≤3x Loop) | Commit Gate |
|---|---|---|---|---|
| **P1 Specs** | `analyst` | `/kanche:design-grill` (first cycle) then `/kanche:design-specs` | `/kanche:design-specs-review` | None |
| **P2 Design** | `architect` | `/kanche:design-init` | `/kanche:design-review` | None |
| **P3 Tasks** | `planner` | `/kanche:planner-tasks` | `/kanche:planner-review` | **Docs Commit** (`/kanche:git-commit` for specs, design, tasks) |
| **P4 Build** | `coder` | `/kanche:dev-implement` | `/kanche:qa-review` | **Implementation Commit** (`/kanche:git-commit` for build/code) |

For each phase:

1. **Delegate execution & mandatory review.** Spawn the corresponding subagent (`analyst`, `architect`, `planner`, or `coder`) with explicit instructions outlining the phase goal. The subagent MUST automatically run both the generation workflow AND the review workflow in sequence without skipping review.
2. **Review verdict.** The subagent runs the review skill (P1: `/kanche:design-specs-review`, P2: `/kanche:design-review`, P3: `/kanche:planner-review`, P4: `/kanche:qa-review`) and parses the `verdict:` output from:
   ```sdd-review
   verdict: GO            # or NO-GO
   findings:
     - {severity: blocker|major|nit, msg: "..."}
   ```

   - **GO** → Proceed to the next phase.
   - **NO-GO** and cycles remaining (up to 3x) → Re-run generate, feeding `findings` to resolve, then automatically re-run review.
   - **NO-GO** on 3rd cycle → In `auto` mode, stop the workflow and report findings. In `manual` mode, ask via `default_api:ask_question` whether to `Proceed anyway` or `Stop`.
3. **Commit checkpoints.**
   - End of P3: Run `/kanche:git-commit` to commit all docs.
   - End of P4: Run `/kanche:git-commit` to commit all implementation changes.

### P5 — AI Validation & Fix Loop (Delegated to `validator`)

1. **Delegate validation.** Invoke the `validator` subagent to run `/kanche:qa-validate` (tests / lint / validations).
2. **Handle failures.** If validate fails:
   - **Under auto mode:** Re-enter P4 (build) automatically up to 3 times to apply fixes, and re-run validation. If still failing after 3 attempts, abort and report failures.
   - **Under manual mode:** Ask "Validation failed" via `default_api:ask_question` with options `Fix via build loop`, `Continue to deploy`, and `Stop`.

### P6 — Deploy & AI PR Review/Respond Loop

1. **Push branch.** Run `/kanche:git-push`.
2. **Create PR.** Run `/kanche:gh-cli-pr-create`.
3. **AI PR Review & Respond Loop (≤3x Loop).** Run `/kanche:gh-cli-pr-review` to audit the PR diff against project guidelines and post review comments on GitHub. If review feedback exists, automatically execute `/kanche:gh-cli-pr-respond` up to 3 times to parse feedback, apply code fixes, re-validate (P5), commit, and push updates.

### P9–P8 — Level 2 Automation (Alignment, Human Review & PR Merge)

In **auto** mode, LEVEL 2 phases execute P9 automatically to promote documentation, then present P7 human review checklist and P8 PR merge to the user. In **manual** mode, each step gates on user prompts.

- **P9 Product Alignment & Doc Sync.**
  - **auto:** Once P6 review/respond checks pass, run `/kanche:sdd-sync` locally on the feature branch (promotes dev docs to domain product directories under `docs/product/plugins/kanche/{domain}/`, removes the dev folder, commits and pushes updates to origin feature branch).
  - **manual:** Ask "Proceed with /kanche:sdd-sync to promote docs and push to feature branch?" using `default_api:ask_question`.

- **P7 Human Review & Checklist.**
  - **auto:** Present verification checklist (`/kanche:qa-validate`), test results, and synced product docs to the human user for review.
  - **manual:** Ask "Proceed to P7 human review checklist?" using `default_api:ask_question`.

- **P8 User PR Merge.**
  - **auto / manual:** Hand over PR merging to the user. The user reviews the PR and completes the merge on GitHub or via `/kanche:gh-cli-pr-merge`.

### 10. Notify User (P10)

Upon completion or abortion, brief the user with a summary:

- Final status (e.g. PR Ready for Human Merge, or Aborted)
- Summary of documentation and implementation edits made
- Direct link to the open PR and feature logs
- **Hand over merge:** Notify user that product docs are synced and the PR is ready for human review (P7) and merge (P8).
- **Ask for feedback:** Show a prompt requesting feedback on the automation run.
- **Ask for deployment:** Request if they want to deploy the feature further (e.g. production servers), saving preferences/instructions to memory if they want the agent to remember it.

## Done when

- All in-bounds phases ran in order.
- The feature receipt was presented and displayed to the user (confirmed in manual mode; logged in auto mode).
- Subagent delegation was performed to conserve tokens.
- Review loops, validation loops, P6 PR review-respond loop, and doc sync (P9) successfully executed.
- Product docs were promoted to domain directories in P9.
- Human review checklist ran at P7 and PR merge handed over to the user at P8.
- Memory and settings files were preserved.
- The user was briefed with a summary and optional feedback requests.
