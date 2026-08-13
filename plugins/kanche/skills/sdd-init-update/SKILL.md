---
name: sdd-init-update
description: Re-analyze this repository and refresh the guidelines merging new findings into existing docs.
model: flash
---

# /kanche:sdd-init-update

**Summary.** Re-analyze this repository and refresh the four steering docs under `.docs/guidelines/`, **merging** new findings into the existing docs rather than overwriting them. Applies the **steering** skill for the analysis and merge drafting.

This workflow runs in the main conversation context. The steering skill only returns document data; this workflow owns all writes to disk.

## Inputs

This workflow takes no arguments. It operates on the current repo.

## Steps

1. **Preconditions.** Confirm we are in a git repo and detect the default branch:
   ```bash
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "NOT_A_GIT_REPO"; exit 1; }
   DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
   DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
   DEFAULT=${DEFAULT:-main}
   ```
   If not a git repo, STOP.

2. **Require existing guidelines.** If `.docs/guidelines/` does not exist (or has none of the four docs), STOP and tell the user to run `/kanche:sdd-init` first — there is nothing to update. Read whichever of `product.md`, `tech.md`, `structure.md`, `rules.md` exist so the current content can be passed to the skill as the base to merge into.

3. **Survey the repo** for changes since the docs were written (read-only):
   ```bash
   git ls-files | head -400
   git ls-files | sed -n 's@.*\.@@p' | sort | uniq -c | sort -rn | head -30
   ```
   Read the top-level `README*` and any manifest/config that reveals the stack (`package.json`, `go.mod`, `pyproject.toml`, `Makefile`, `docker-compose*.yml`, CI config, `.tool-versions`). Focus on what may have drifted from the existing docs.

4. **Apply the steering skill** (skills/steering/SKILL.md) in **merge mode**: give it both the existing docs and the fresh survey. Ask it to update (merge, do not overwrite) the existing steering guidelines — pass the default branch, the existing product.md / tech.md / structure.md / rules.md verbatim, and the fresh survey (ls-files digest, extension histogram, and configs/READMEs you read). For each of the four docs it must return the FULL merged content: preserve hand-tuned content (especially rules.md), add what is new, correct what is now wrong, and flag removals rather than silently dropping them, grounding new claims in files and marking inferences. Then continue.

5. **Persist (merge).** Write each returned doc back to `.docs/guidelines/{product,tech,structure,rules}.md`. Because the skill returns the already-merged full text, a full write is correct — but never discard hand-tuned sections the skill preserved. If a doc came back unchanged, still write it (a no-op is safe).

6. **Report.** Print the changed paths and a short changelog: what was added, corrected, or flagged for removal per doc. Explicitly note if `rules.md` was left untouched.

## Failure cases

- Not a git repo → STOP (step 1).
- No existing guidelines → STOP, point to `/kanche:sdd-init` (step 2).
- Skill returns a doc that drops hand-tuned content → do NOT write it; report the conflict and ask the user how to reconcile rather than losing their edits.

## Done when

- The four guideline docs reflect the current repo, with prior hand-tuned content preserved.
- Each write came from the **steering** skill's merged output.
- The report lists changed paths and a per-doc changelog.
