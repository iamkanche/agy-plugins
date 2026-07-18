---
name: run
description: Drive a feature work item through the full SDD phase model (P0 to P9) using specifications, system designs, task check-lists, and testing loops.
---

# /sdd:run

**Summary.** Drive a work item through the full SDD phase model (P0→P9): ensure a feature branch, walk each phase, running the LEVEL-1 inner review loops (≤3×), committing at key checkpoints (docs commit after P3, implementation commit after P4), and progressing automatically in `auto` mode through LEVEL 2 (P7→P9). State every workflow you run before running it.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **slug** (optional, positional) — the feature slug/short description (e.g. `improve-sdd-plugins` or `login`). If absent, prompt the user for it to construct the folder path `.sdd-docs/development/{slug}/`.
- **`--mode=auto|manual`** — default **auto**. Also accept a bare `auto`/`manual` positional.
  - **auto:** run the entire workflow (P0→P9) straight through, executing Level 2 automatically (checks PR status, runs validation checklists, syncs docs, and cleans up folders) without per-phase prompt, stopping only for critical tool confirmations.
  - **manual:** before advancing to each next phase, ask "Proceed to `<next phase>`? [Yes|No]". "No" stops the walk cleanly (state where it stopped).
- **`--from=<phase>`** — start the walk at this phase instead of P0 (`P0`..`P9`, or a name like `design`/`build`). Phases before it are assumed already done; do not re-run them.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 AI-validation, P6 deploy, and Level 2 entirely. Bound both ends: never run outside `[from, until]`.

If `--from`/`--until` are inconsistent (from > until), stop and report.

## Phase model

```
LEVEL 1 (AI)                                    LEVEL 2 (AI + human, auto/gated)
P0 setup   /git:branch-create                   P7 human review  /sdd:human-validation
P1 specs   grill→specs→specs-review             P8 PR mods       /gh-cli:pr-respond → …
P2 design  design→design-review                 P9 alignment     /sdd:sync
P3 tasks   tasks→tasks-review→Docs Commit
P4 build   build→build-review→Implementation Commit
P5 valid.  /sdd:validate
P6 deploy  /git:push → /gh-cli:pr-create
```

## Steps

### 0. Preconditions

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "NOT_A_GIT_REPO"
DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
DEFAULT=${DEFAULT:-main}
CURRENT=$(git rev-parse --abbrev-ref HEAD)
echo "default=$DEFAULT current=$CURRENT"
ls .sdd-docs/guidelines 2>/dev/null
```

- Not a git repo → stop, tell the user.
- **No `.sdd-docs/guidelines/`** → steering is missing. Stop and tell the user to run `/sdd:init` first; do not proceed.

### P0 — ensure a feature branch (`/git:branch-create`)

Protected branches: **main, master, develop**. If `$CURRENT` is one of those (or matches `$DEFAULT`), you MUST create a feature branch before any generation or commit:

> Run **/git:branch-create** with a conventional name (e.g. `feat/{slug}`, `docs/{slug}`, or `refactor/{slug}`).

If already on a feature branch, keep it. Never generate or commit on a protected branch.
Skip P0 if `--from` is past it AND a feature branch is already checked out.

For each phase transition in **manual** mode, ask "Proceed to `<phase>`?" using the interactive `default_api:ask_question` tool with options `(Recommended) Yes, proceed` and `No, abort` first; selecting "No" → stop and report the current phase.

### P1–P4 — inner review loop (generate → review, ≤3×, then commit at key gates)

Each of these phases follows the SAME loop. Only the workflow trio differs:

| Phase | Generate | Review | Commit Gate |
|---|---|---|---|
| P1 specs | `/sdd:grill` then `/sdd:specs` | `/sdd:specs-review` | None |
| P2 design | `/sdd:design` | `/sdd:design-review` | None |
| P3 tasks | `/sdd:tasks` | `/sdd:tasks-review` | **Docs Commit** (`/git:commit` for specs, design, tasks) |
| P4 build | `/sdd:build` | `/sdd:build-review` | **Implementation Commit** (`/git:commit` for build/code) |

Loop for the current phase (max **3** generate→review cycles):

1. **Generate.** Run the phase's generate workflow(s) for `<slug>`. For P1, run `/sdd:grill` once at the start of the first cycle only, then `/sdd:specs`.
2. **Review.** Run the phase's review workflow. It returns a fenced `sdd-review` block:
   ```sdd-review
   verdict: GO            # or NO-GO
   findings:
     - {severity: blocker|major|nit, msg: "..."}
   ```
   Parse the `verdict:` line.
   - **GO** → exit the loop.
   - **NO-GO** and cycles remaining → re-run the generate workflow, explicitly feeding the `findings` list so it addresses them; then review again.
   - **NO-GO** on the 3rd cycle → do NOT silently proceed. Surface the remaining findings to the user and ask: "Specs/design/tasks/build still NO-GO after 3 attempts." using `default_api:ask_question` with options `Proceed anyway` and `Stop`. Honor the answer.
3. **Commit checkpoints.**
   - At the end of P3 (Tasks): run **/git:commit** to commit all documentation files (`specs.md`, `design.md`, `tasks.md`, `notes.md`) together with a conventional commit message (e.g. `docs(<slug>): specs, design, and task list`).
   - At the end of P4 (Build): run **/git:commit** to commit all implementation changes with a conventional commit message (e.g. `feat(<slug>): implementation`).
   - Confirmations are governed by the git workflow. If the user declines the commit, stop and report.

Respect bounds: if a phase is outside `[from, until]`, skip it. If `--until` is one of P1–P4, commit that checkpoint then STOP (do not enter P5/P6).

### P5 — AI validation (`/sdd:validate`)

Only if `--until` ≥ `build` (i.e. P4 completed and P5 within bounds).

> Run **/sdd:validate** for `<slug>` (tests / lint / browser checks).

This is read-only verification; no commit. If it reports failures, surface them and ask "Validation failed." using `default_api:ask_question` with options `Fix via build loop`, `Continue to deploy`, and `Stop`.
"Fix via build loop" → re-enter P4 once with the failures as findings, then re-run P5.

### P6 — deploy (HUMAN GATE: `/git:push` → `/gh-cli:pr-create`)

Only if `--until` ≥ `build`.

1. **Push (gated).** Run **/git:push** (it confirms before pushing; never force-push).
2. **Create PR (gated).** Run **/gh-cli:pr-create** (requires `gh` auth; if not authed, stop and request the user to run `gh auth login`).

In **auto** mode: after P6, automatically proceed to LEVEL 2 phases (P7→P9).
In **manual** mode with `--until` ≥ P7: ask "Proceed to P7 human review?" using `default_api:ask_question` with options `(Recommended) Yes, proceed` and `No, abort` and, only on Yes, continue into LEVEL 2.

### P7–P9 — LEVEL 2 (automatically walk in auto mode, gated in manual mode)

- **P7 human review** —
  - **auto:** Automatically run `/sdd:human-validation` (checklist).
  - **manual:** Ask "Proceed to P7?" using `default_api:ask_question` with options `(Recommended) Yes, proceed` and `No, abort` before running.
- **P8 PR modifications** (loop) —
  - **auto:** Automatically check PR status. If feedback is found, run `/gh-cli:pr-respond`, resolve conflicts/comments, run `/git:commit` and `/git:push`. Repeat until PR is merged or ready.
  - **manual:** Ask "Address PR feedback now?" using `default_api:ask_question` with options `(Recommended) Yes, proceed` and `No, abort` before running.
- **P9 product alignment** —
  - **auto:** Automatically run `/sdd:sync` to promote feature docs and clean up the development feature directory.
  - **manual:** Ask "Promote dev docs to product/?" using `default_api:ask_question` with options `(Recommended) Yes, proceed` and `No, abort` before running.

## Failure handling

- Protected branch reached at any commit/push point without a feature branch → stop, run P0.
- Review NO-GO after 3 cycles → gate as above, never silent.
- `gh` not authed at P6 → `/gh-cli:pr-create` stops; relay its instruction.
- Merge conflict / push rejected → surface the error, stop; never force-push, never `--no-verify`, never `reset --hard`.
- Any `/git:*` gate declined → stop the walk, report the phase and reason.

## Done when

- A feature branch exists and all in-bounds phases ran in order.
- Document and implementation checkpoints were committed via `/git:commit`.
- If in bounds: P5 validation ran and P6 push + PR completed through their gates.
- auto mode executed all phases (P0→P9) to completion; manual mode stopped at declined gates.
- The walk respected `--from`/`--until`; nothing outside the bounds executed.
