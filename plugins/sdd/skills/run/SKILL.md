---
name: run
description: Drive a feature work item through the full SDD phase model (P0 to P9) using specifications, system designs, task check-lists, and testing loops.
---

# /sdd:run

**Summary.** Drive a work item through the full SDD phase model (P0→P9): verify/load settings and memory, present a feature receipt for user confirmation, ensure a feature branch, delegate phase-specific execution (P1-P5) to token-optimized specialized subagents, run inner review loops (≤3x), validate and fix implementation (≤3x), deploy and poll PR comments (≤3x) to automatically respond/fix issues, automatically merge the PR, promote documentation, preserve memory files, and notify the user with a summary briefing and feedback options.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description (e.g. `improve-sdd-plugins` or `login`). If absent, prompt the user for it to construct the folder path `.sdd-docs/development/{slug}/`.
- **`--mode=auto|manual`** — default **auto**. Also accept a bare `auto`/`manual` positional.
  - **auto:** run the entire workflow (P0→P9) straight through, executing Level 2 automatically (checks PR status, runs validation checklists, syncs docs, and cleans up folders) without per-phase prompt or interactive confirmation dialogs.
  - **manual:** before advancing to each next phase, ask "Proceed to `<next phase>`? [Yes|No]". "No" stops the walk cleanly (state where it stopped).
- **`--from=<phase>`** — start the walk at this phase instead of P0 (`P0`..`P9`, or a name like `design`/`build`). Phases before it are assumed already done; do not re-run them.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 AI-validation, P6 deploy, and Level 2 entirely. Bound both ends: never run outside `[from, until]`.

If `--from`/`--until` are inconsistent (from > until), stop and report.

## Phase model

```
LEVEL 1 (AI + Subagents)                         LEVEL 2 (AI + human, auto/gated)
P0 setup   Receipt /git:branch-create            P7 human review  /sdd:human-validation
P1 specs   grill→specs→specs-review (Analyst)    P8 PR mods       /gh-cli:pr-respond & poll
P2 design  design→design-review (Architect)      P9 alignment     /sdd:sync -> /gh-cli:pr-merge & preserve
P3 tasks   tasks→tasks-review→Docs Commit        
           (Planner)
P4 build   build→build-review→Code Commit
           (Coder)
P5 valid.  /sdd:validate & fix (Validator)
P6 deploy  /git:push → /gh-cli:pr-create
```

## Steps

### 0. Preconditions & Setup (P0)

1. **Verify Git Repo.**
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "NOT_A_GIT_REPO"
   ```
2. **Load settings & memory.** Check if `.sdd-docs/settings.json` exists. If so, parse settings (e.g. loops, polling time, custom commands). Read `.sdd-docs/product/memory.md` to load project-specific rules and constraints.
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
5. **Ensure guidelines exist.** If `.sdd-docs/guidelines/` does not exist, stop and instruct the user to run `/sdd:init`.
6. **Ensure feature branch.** If `$CURRENT` matches `$DEFAULT` or is a protected branch (`main`, `master`, `develop`), create a feature branch using `/git:branch-create` as `feat/{slug}`.

### P1–P4 — Inner Review Loops (Delegated to Token-Optimized Subagents)

To optimize token consumption, the parent agent delegates Phase P1-P4 workflows to specialized subagents. Each loop runs up to **3** times.

| Phase | Subagent | Generate Workflow | Review Workflow | Commit Gate |
|---|---|---|---|---|
| **P1 Specs** | `sdd-analyst` | `/sdd:grill` (first cycle) then `/sdd:specs` | `/sdd:specs-review` | None |
| **P2 Design** | `sdd-architect` | `/sdd:design` | `/sdd:design-review` | None |
| **P3 Tasks** | `sdd-planner` | `/sdd:tasks` | `/sdd:tasks-review` | **Docs Commit** (`/git:commit` for specs, design, tasks) |
| **P4 Build** | `sdd-coder` | `/sdd:build` | `/sdd:build-review` | **Implementation Commit** (`/git:commit` for build/code) |

For each phase:
1. **Delegate execution.** Spawn the corresponding subagent (`sdd-analyst`, `sdd-architect`, `sdd-planner`, or `sdd-coder`) with a system prompt outlining the phase goal and feed it the relevant specs, designs, and tasks.
2. **Review verdict.** The subagent runs the review skill and parses the `verdict:` output from:
   ```sdd-review
   verdict: GO            # or NO-GO
   findings:
     - {severity: blocker|major|nit, msg: "..."}
   ```
   - **GO** → Proceed to the next phase.
   - **NO-GO** and cycles remaining → Re-run generate, feeding `findings` to resolve.
   - **NO-GO** on 3rd cycle → In `auto` mode, stop the workflow and report findings. In `manual` mode, ask via `default_api:ask_question` whether to `Proceed anyway` or `Stop`.
3. **Commit checkpoints.**
    - End of P3: Run `/git:commit` to commit all docs.
    - End of P4: Run `/git:commit` to commit all implementation changes.

### P5 — AI Validation & Fix Loop (Delegated to `sdd-validator`)

1. **Delegate validation.** Invoke the `sdd-validator` subagent to run `/sdd:validate` (tests / lint / validations).
2. **Handle failures.** If validate fails:
   - **Under auto mode:** Re-enter P4 (build) automatically up to 3 times to apply fixes, and re-run validation. If still failing after 3 attempts, abort and report failures.
   - **Under manual mode:** Ask "Validation failed" via `default_api:ask_question` with options `Fix via build loop`, `Continue to deploy`, and `Stop`.

### P6 — Deploy (Push & Create PR)

1. **Push branch.** Run `/git:push`.
2. **Create PR.** Run `/gh-cli:pr-create`.

### P7–P9 — Level 2 Automation (PR Review, Merging & Alignment)

In **auto** mode, LEVEL 2 phases run automatically. In **manual** mode, they gate on user question prompts.

- **P7 Human Review & Checklist.**
  - **auto:** Automatically check off verification checklists if local tests and validations passed.
  - **manual:** Ask "Proceed to P7?" using `default_api:ask_question`.

- **P8 PR Modifications & Polling.**
  - **auto:** Poll the pull request status and review comments using:
    ```bash
    gh pr view --json reviews,comments,state
    ```
    Poll up to 3 times (with sleep intervals configured in settings). If new review feedback or comments are found:
    - Automatically invoke `/gh-cli:pr-respond` to parse comments, fix files, run validations (P5), and commit/push updates.
    - Repeat checking until reviews are approved.
  - **manual:** Ask "Address PR feedback now?" using `default_api:ask_question`.

- **P9 Product Alignment & Merge.**
  - **auto:** Once the PR is approved, first run `/sdd:sync` locally on the feature branch (promotes dev docs to `product/`, removes the dev folder, commits and pushes to the feature branch). Poll CI/status checks on the new commit using `pr_polling` settings from `.sdd-docs/settings.json` (default 30s interval, 3 max attempts). Once checks pass, run `/gh-cli:pr-merge` (no `--keep-branch`) to merge the PR and delete both local and remote branches.
  - **manual:** Two separate gates: (1) `"Proceed with /sdd:sync to promote docs and push to feature branch? [Yes|No]"`, (2) `"Proceed with /gh-cli:pr-merge to merge the PR and clean up branches? [Yes|No]"`.

### 10. Notify User (P10)

Upon completion or abortion, brief the user with a summary:
- Final status (e.g. Success, Merged, or Aborted)
- Summary of documentation and implementation edits made
- Direct link to the merged PR and feature logs
- **Ask for feedback:** Show a prompt requesting feedback on the automation run.
- **Ask for deployment:** Request if they want to deploy the feature further (e.g. production servers), saving preferences/instructions to memory if they want the agent to remember it.

## Done when

- All in-bounds phases ran in order.
- The feature receipt was presented and displayed to the user (confirmed in manual mode; logged in auto mode).
- Subagent delegation was performed to conserve tokens.
- Review loops, validation loops, and PR response loops successfully executed.
- The PR was merged automatically on approval, and product docs synced.
- Memory and settings files were preserved.
- The user was briefed with a summary and optional feedback requests.
