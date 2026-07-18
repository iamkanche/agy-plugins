---
name: run
description: Drive a feature work item through the full SDD phase model (P0 to P9) using specifications, system designs, task check-lists, and testing loops.
---

# /sdd:run

**Summary.** Drive a work item through the full SDD phase model (P0→P9): ensure a feature branch, then walk each phase, running the LEVEL-1 inner review loops (≤3×), committing between phases, and stopping at the human gate. This body is the orchestration program you (the main-context model) execute directly — you invoke each phase's workflows by their slash names (`/sdd:*`, `/git:*`) in this same context. State every workflow you run before running it.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **item_id** (required, positional) — the feature identifier, e.g. `002` or `002_login`. It selects/creates the dev folder `.sdd-docs/development/{NNN}_{slug}/`. If absent, ask the user (do NOT invent one).
- **`--mode=auto|manual`** — default **auto**. Also accept a bare `auto`/`manual` positional.
  - **auto:** run LEVEL 1 (P0→P6) straight through with no per-phase prompt, stopping at the P6 human gate.
  - **manual:** before advancing to each next phase, ask "Proceed to `<next phase>`? [Yes|No]". "No" stops the walk cleanly (state where it stopped).
- **`--from=<phase>`** — start the walk at this phase instead of P0 (`P0`..`P9`, or a name like `design`/`build`). Phases before it are assumed already done; do not re-run them.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 AI-validation and P6 deploy entirely. Bound both ends: never run outside `[from, until]`.

If `--from`/`--until` are inconsistent (from > until), stop and report.

## Phase model

```
LEVEL 1 (AI)                                    LEVEL 2 (AI + human, all gated)
P0 setup   /git:create-branch                   P7 human review  /sdd:human-validation
P1 specs   grill→specs→specs-review→commit      P8 PR mods       /git:respond-pr → …
P2 design  design→design-review→commit          P9 alignment     /sdd:sync-product
P3 tasks   tasks→tasks-review→commit
P4 build   build→build-review→commit
P5 valid.  /sdd:ai-validation
P6 deploy  /git:push → /git:create-pr  (HUMAN GATE)
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

### P0 — ensure a feature branch (`/git:create-branch`)

Protected branches: **main, master, develop**. If `$CURRENT` is one of those (or matches `$DEFAULT`), you MUST create a feature branch before any generation or commit:

> Run **/git:create-branch** for item `<item_id>` (it branches from the latest `$DEFAULT`).

If already on a feature branch, keep it. Never generate or commit on a protected branch.
Skip P0 if `--from` is past it AND a feature branch is already checked out.

For each phase transition in **manual** mode, ask "Proceed to `<phase>`? [Yes|No]" first; "No" → stop and report the current phase.

### P1–P4 — inner review loop (generate → review, ≤3×, then commit)

Each of these phases follows the SAME loop. Only the workflow trio differs:

| Phase | Generate | Review | Then |
|---|---|---|---|
| P1 specs | `/sdd:grill` then `/sdd:specs` | `/sdd:specs-review` | `/git:commit` |
| P2 design | `/sdd:design` | `/sdd:design-review` | `/git:commit` |
| P3 tasks | `/sdd:tasks` | `/sdd:tasks-review` | `/git:commit` |
| P4 build | `/sdd:build` | `/sdd:build-review` | `/git:commit` |

Loop for the current phase (max **3** generate→review cycles):

1. **Generate.** Run the phase's generate workflow(s) for `<item_id>`. For P1, run `/sdd:grill` once at the start of the first cycle only, then `/sdd:specs`.
2. **Review.** Run the phase's review workflow. It returns a fenced `sdd-review` block:
   ```sdd-review
   verdict: GO            # or NO-GO
   findings:
     - {severity: blocker|major|nit, msg: "..."}
   ```
   Parse the `verdict:` line.
   - **GO** → exit the loop, go to commit.
   - **NO-GO** and cycles remaining → re-run the generate workflow, explicitly feeding the `findings` list so it addresses them; then review again.
   - **NO-GO** on the 3rd cycle → do NOT silently proceed. Surface the remaining findings to the user and ask: "Specs/design/tasks/build still NO-GO after 3 attempts. [Commit anyway | Stop]". Honor the answer.
3. **Commit (gated).** Run **/git:commit**. It owns its own Yes/No confirmation and builds the Conventional-commit message — do not commit directly yourself and never pass `--no-verify`. If the user declines the commit gate, stop the walk and report.

Respect bounds: if a phase is outside `[from, until]`, skip it. If `--until` is one of P1–P4, commit that phase then STOP (do not enter P5/P6).

### P5 — AI validation (`/sdd:validate`)

Only if `--until` ≥ `build` (i.e. P4 completed and P5 within bounds).

> Run **/sdd:validate** for `<item_id>` (tests / lint / browser checks).

This is read-only verification; no commit. If it reports failures, surface them and ask "Validation failed. [Fix via build loop | Continue to deploy | Stop]".
"Fix via build loop" → re-enter P4 once with the failures as findings, then re-run P5.

### P6 — deploy (HUMAN GATE: `/git:push` → `/git:create-pr`)

Only if `--until` ≥ `build`. This is the LEVEL-1 stop point.

1. **Push (gated).** Run **/git:push** (it confirms before pushing; never force-push).
2. **Create PR (gated).** Run **/git:create-pr** (it requires `gh` auth and confirms before opening; if `gh` is not authed it stops and tells the user to `gh auth login`).

In **auto** mode: after P6, **STOP** — do not enter LEVEL 2. Report that the workflow reached the human gate and list P7–P9 as the human-driven next steps (`/sdd:continue` resumes them).

In **manual** mode with `--until` ≥ P7: ask "Proceed to P7 human review? [Yes|No]" and, only on Yes, continue into LEVEL 2 below.

### P7–P9 — LEVEL 2 (human-gated throughout)

Enter only if bounds allow AND (manual mode with an explicit Yes, or `--from` targets one of these phases for an intentional resume). **Gate — STOP.** Ask before EACH phase regardless of mode:

- **P7 human review** — ask "Proceed to P7? [Yes|No]" → **/sdd:human-validation** (produces a human checklist; no side effects).
- **P8 PR modifications** (loop) — "Address PR feedback now? [Yes|No]" → **/git:respond-pr**; if it changes code, optionally **/sdd:sync-docs-code**, then **/git:commit** and **/git:push** (each gated by its own workflow). Repeat while there is unresolved feedback and the user says Yes.
- **P9 product alignment** — "Promote dev docs to product/? [Yes|No]" → **/sdd:sync** (consolidates `development/{f}/` → `product/`; owns its own commit gate).

## Failure handling

- Protected branch reached at any commit/push point without a feature branch → stop, run P0.
- Review NO-GO after 3 cycles → gate as above, never silent.
- `gh` not authed at P6 → `/git:create-pr` stops; relay its instruction, do not auth for them.
- Merge conflict / push rejected → surface the error, stop; never force-push, never `--no-verify`, never `reset --hard`.
- Any `/git:*` gate declined → stop the walk, report the phase and reason.

## Done when

- A feature branch exists and all in-bounds phases ran in order.
- P1–P4 each reached GO (or an explicit "commit anyway") and were committed via `/git:commit`.
- If in bounds: P5 validation ran and P6 push + PR completed through their gates.
- auto mode stopped at the P6 human gate; manual/L2 phases ran only with explicit Yes answers.
- The walk respected `--from`/`--until`; nothing outside the bounds executed.
