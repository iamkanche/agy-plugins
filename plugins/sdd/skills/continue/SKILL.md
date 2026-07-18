---
name: continue
description: Resume the SDD workflow at the phase inferred from on-disk state instead of starting fresh.
---

# /sdd:continue

**Summary.** Resume the SDD workflow at the phase inferred from on-disk state instead of starting fresh, then walk forward with the same mode and loop rules as `/sdd:run`. This body is the orchestration program you (the main-context model) execute directly: you detect the phase, then invoke each remaining phase's workflows by their slash names (`/sdd:*`, `/git:*`) in this same context. State every workflow you run before running it.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **`--mode=auto|manual`** — default **auto** (also accept a bare `auto`/`manual` positional). Same semantics as `/sdd:run`: auto runs LEVEL 1 straight to the P6 gate; manual asks "Proceed to `<next phase>`? [Yes|No]" before each phase transition.
- **`--from=<phase>`** — override detection and force the resume point.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 validation and P6 deploy.
- **item_id** (optional, positional) — disambiguates when several dev folders exist. If omitted, pick the most recently modified `.sdd-docs/development/{NNN}_{slug}/`; if that is ambiguous, list the candidates and ask the user.

## Steps

### 1. Detect current phase

Gather on-disk and repo signals, then map to the resume phase. Do NOT re-run completed phases.

```bash
# Steering
ls .sdd-docs/guidelines 2>/dev/null

# Feature folder + docs
FEAT=$(ls -dt .sdd-docs/development/*/ 2>/dev/null | head -1)
echo "feature_dir=$FEAT"
[ -n "$FEAT" ] && ls "$FEAT"                        # specs.md? design.md? tasks.md?
# tasks completion: are any checkboxes still unchecked?
[ -f "$FEAT/tasks.md" ] && grep -c -- '- \[ \]' "$FEAT/tasks.md"   # >0 = tasks remain
[ -f "$FEAT/tasks.md" ] && grep -c -- '- \[x\]' "$FEAT/tasks.md"

# Branch / push / PR state
DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
DEFAULT=${DEFAULT:-main}
CURRENT=$(git rev-parse --abbrev-ref HEAD)
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "NO_UPSTREAM"
gh pr view --json state,number,mergedAt 2>/dev/null || echo "NO_PR"   # needs gh auth
ls .sdd-docs/product/features 2>/dev/null                              # consolidated yet?
```

Apply the detection rules **in order** and take the first match as the resume phase:

1. **No `.sdd-docs/guidelines/`** → steering missing. STOP; tell the user to run `/sdd:init` first. Do not resume.
2. **No feature folder** (or folder exists but empty) → resume at **P0/P1** (ensure branch, then specs).
3. **`specs.md` absent** → **P1**. **`specs.md` present, `design.md` absent** → **P2**. **`design.md` present, `tasks.md` absent** → **P3**.
4. **`tasks.md` present with unchecked `- [ ]` items** → **P4 build** (finish the checklist).
5. **All `tasks.md` items checked** → build is done → **P5** (if not yet validated) then **P6**. If the branch is **already pushed (has upstream) AND a PR is open** → **P7/P8** (human review / PR modifications).
6. **PR merged AND the dev folder `development/{f}/` still present** (no `product/features/{slug}/` consolidation) → **P9** (`sync` not yet run).

`--from` overrides all of the above. Report the detected phase and the evidence for it before walking.

### 2. Ensure a feature branch (P0 guard)

Protected branches: **main, master, develop**. If detection lands at P1–P6 but `$CURRENT` is protected (or matches `$DEFAULT`), you MUST create a branch first:

> Run **/git:create-branch** for the item before any generation or commit.

Never generate or commit on a protected branch. If already on a feature branch, keep it.

### 3. Resume the walk

From the detected (or `--from`) phase, execute forward exactly as `/sdd:run` does — same inner-loop, gate, and bound rules. Summary of the walk:

- **P1–P4 inner loop** — generate → review, parse the `sdd-review` `verdict:`; on **NO-GO** re-run generate with the findings, up to **3×**; on GO (or an explicit "commit anyway" after 3 failures) run **/git:commit** (its own Yes/No gate). Workflow trios:
  - P1: `/sdd:grill` (once, first cycle) → `/sdd:specs` → `/sdd:specs-review` → `/git:commit`
  - P2: `/sdd:design` → `/sdd:design-review` → `/git:commit`
  - P3: `/sdd:tasks` → `/sdd:tasks-review` → `/git:commit`
  - P4: `/sdd:build` → `/sdd:build-review` → `/git:commit`
- **P5** (only if `--until` ≥ build) — **/sdd:validate**; on failure ask "[Fix via build loop | Continue | Stop]".
- **P6** (only if `--until` ≥ build, HUMAN GATE) — **/git:push** then **/git:create-pr** (each self-gated; `gh` must be authed). In **auto** mode, STOP here and list P7–P9 as the human next steps. In **manual** mode, ask before entering P7.
- **P7–P9 LEVEL 2** — human-gated throughout; **Gate — STOP.** Ask "Proceed to `<phase>`? [Yes|No]" before EACH:
  - P7 **/sdd:human-validation** (checklist, no side effects)
  - P8 **/git:respond-pr** → optional **/sdd:sync-docs-code** → **/git:commit** → **/git:push** (loop while unresolved feedback and user says Yes)
  - P9 **/sdd:sync** (promotes `development/{f}/` → `product/`; own commit gate)

In **manual** mode, ask "Proceed to `<next phase>`? [Yes|No]" before every phase transition; "No" stops cleanly and reports where it stopped. Respect `--from`/`--until` bounds throughout; if `--until` < build, stop after committing the last in-bounds P1–P4 phase.

## Failure handling

- Guidelines missing → stop, direct to `/sdd:init`.
- Detection ambiguous (multiple feature folders, no item_id) → list and ask; do not guess.
- Protected branch at a commit/push point → stop, run P0.
- Review NO-GO after 3 cycles → gate, never silent.
- `gh` not authed (PR detection / P6) → treat PR state as unknown / relay `/git:create-pr`'s stop message; do not auth for the user.
- Any `/git:*` gate declined, merge conflict, or push rejection → surface and stop. Never force-push, never `--no-verify`, never amend a pushed commit, never `reset --hard`.

## Done when

- The resume phase was detected from on-disk state (or taken from `--from`) and reported with evidence; no completed phase was re-run.
- A feature branch exists before any generation/commit.
- The remaining in-bounds phases ran in order with the same loop/gate rules as `/sdd:run`.
- auto mode stopped at the P6 human gate; P7–P9 ran only with explicit Yes answers.
- The walk respected `--from`/`--until`.
