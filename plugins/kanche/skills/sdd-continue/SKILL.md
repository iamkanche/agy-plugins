---
name: sdd-continue
description: Resume the SDD workflow at the phase inferred from on-disk state instead of starting fresh.
model: flash
---

# /kanche:sdd-continue

**Summary.** Resume the SDD workflow at the phase inferred from on-disk state instead of starting fresh, then walk forward with the same mode and loop rules as `/kanche:sdd-run`. This body is the orchestration program you (the main-context model) execute directly: you detect the phase, then invoke each remaining phase's workflows by their slash names (`/sdd:*`, `/git:*`, `/gh-cli:*`) in this same context. State every workflow you run before running it.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **`--mode=auto|manual`** — default **auto** (also accept a bare `auto`/`manual` positional). Same semantics as `/kanche:sdd-run`: auto runs to P9; manual asks "Proceed to `<next phase>`? [Yes|No]" before each phase transition.
- **`--from=<phase>`** — override detection and force the resume point.
- **`--until=<phase>`** — stop after this phase (inclusive). If `--until` < `build` (P4), skip P5 validation, P6 deploy, and Level 2 entirely.
- **slug** (optional, positional) — disambiguates when several dev folders exist. If omitted, pick the most recently modified `.docs/development/{slug}/`; if that is ambiguous, list the candidates and ask the user.

## Steps

### 1. Detect current phase

Gather on-disk and repo signals, then map to the resume phase. Do NOT re-run completed phases.

```bash
# Steering
ls .docs/guidelines 2>/dev/null

# Feature folder + docs
FEAT=$(ls -dt .docs/development/*/ 2>/dev/null | head -1)
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
ls .docs/product/features/ 2>/dev/null                                      # consolidated yet?
```

Apply the detection rules **in order** and take the first match as the resume phase:

1. **No `.docs/guidelines/`** → steering missing. STOP; tell the user to run `/kanche:sdd-init` first. Do not resume.
2. **No feature folder** (or folder exists but empty) → resume at **P0/P1** (ensure branch, then specs).
3. **`specs.md` absent** → **P1**. **`specs.md` present, `design.md` absent** → **P2**. **`design.md` present, `tasks.md` absent** → **P3**.
4. **`tasks.md` present with unchecked `- [ ]` items** → **P4 build** (finish the checklist).
5. **All `tasks.md` items checked** → build is done → **P5** (if not yet validated) then **P6** (deploy & 3x review-respond loop).
6. **P6 deploy complete AND dev folder `development/{slug}/` present** → **P7** (`/kanche:sdd-sync` to promote docs to domain product directories).
7. **`sdd-sync` completed (dev folder consolidated) AND PR open** → **P8** (Gated human review checklist), then **P9** (PR merge `/kanche:gh-cli-pr-merge`).

`--from` overrides all of the above. Report the detected phase and the evidence for it before walking.

### 2. Ensure a feature branch (P0 guard)

Protected branches: **main, master, develop**. If detection lands at P1–P6 but `$CURRENT` is protected (or matches `$DEFAULT`), you MUST create a branch first:

> Run **/kanche:git-branch-create** with conventional branch name for the item before any generation or commit.

Never generate or commit on a protected branch. If already on a feature branch, keep it.

### 3. Resume the walk

From the detected (or `--from`) phase, execute forward exactly as `/kanche:sdd-run` does — following the **Loop Engineering Protocol (`plugins/kanche/rules/loop-engineering.md`)**, same inner-loop, gate, and bound rules. Summary of the walk:

- **P1–P4 inner loop (Loop Engineering Generator ↔ Reviewer Pairs)** — generate → review, parse the `sdd-review` `verdict:`; on **NO-GO** re-run generator with targeted delta fixes, up to **3×**.
  - P1: `/kanche:design-grill` (once, first cycle) → loop ≤3x (`/kanche:design-specs` ↔ `/kanche:design-specs-review`)
  - P2: loop ≤3x (`/kanche:design-init` ↔ `/kanche:design-review`)
  - P3: loop ≤3x (`/kanche:planner-tasks` ↔ `/kanche:planner-review`) → Docs Commit (`/kanche:git-commit` via HEREDOC)
  - P4: loop ≤3x (`/kanche:code-implement` ↔ `/kanche:code-review` / `/kanche:qa-review`) → Implementation Commit (`/kanche:git-commit` via HEREDOC)
- **P5** (only if `--until` ≥ build) — **/kanche:qa-validate** & fix loop (`/kanche:code-implement`, ≤3x loop).
- **P6** (only if `--until` ≥ build) — **/kanche:git-push** → **/kanche:gh-cli-pr-create** → **loop ≤3x (/kanche:gh-cli-pr-review ↔ /kanche:gh-cli-pr-respond → /kanche:git-commit → /kanche:git-push)**.
- **P7** (LEVEL 1 AI Final Step) — **/kanche:sdd-sync** (promotes `development/{slug}/` → `.docs/product/{domain}/`, commits via `/kanche:git-commit` HEREDOC & pushes to origin as separate step).
- **P8–P9 LEVEL 2 (Human)** —
  - P8: Gated human review checklist (`/kanche:qa-validate` displaying test/lint checklist)
  - P9: PR merge (`/kanche:gh-cli-pr-merge`)


In **manual** mode, ask "Proceed to `<next phase>`? [Yes|No]" before every phase transition; "No" stops cleanly and reports where it stopped. Respect `--from`/`--until` bounds throughout; if `--until` < build, stop after committing the last in-bounds P1–P4 phase.

## Failure handling

- Guidelines missing → stop, direct to `/kanche:sdd-init`.
- Detection ambiguous (multiple feature folders, no slug) → list and ask; do not guess.
- Protected branch at a commit/push point → stop, run P0.
- Review NO-GO after 3 cycles → gate, never silent.
- `gh` not authed (PR detection / P6) → treat PR state as unknown / relay `/kanche:gh-cli-pr-create`'s stop message.
- Any `/git:*` gate declined, merge conflict, or push rejection → surface and stop. Never force-push, never `--no-verify`, never amend a pushed commit, never `reset --hard`.

## Done when

- The resume phase was detected from on-disk state (or taken from `--from`) and reported with evidence; no completed phase was re-run.
- A feature branch exists before any generation/commit.
- The remaining in-bounds phases ran in order with the same loop/gate rules as `/kanche:sdd-run`.
- auto mode executed all remaining phases (P0→P9) to completion; manual mode stopped at declined gates.
- The walk respected `--from`/`--until`.
