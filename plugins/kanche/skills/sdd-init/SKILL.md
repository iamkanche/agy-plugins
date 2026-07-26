---
name: sdd-init
description: Bootstrap the steering guidelines (product.md, tech.md, structure.md, rules.md) for this repository.
---

# /kanche:sdd-init

**Summary.** Analyze this repository and write the four steering docs under `docs/guidelines/`, applying the **steering** skill for the analysis and drafting.

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
   echo "default_branch=$DEFAULT"
   ```
   If not a git repo, STOP and tell the user to run this inside a repository.

2. **Idempotency check.** If `docs/guidelines/` already exists with any of `product.md`, `tech.md`, `structure.md`, `rules.md`, STOP and tell the user to run `/kanche:sdd-init-update` instead (that workflow merges into existing docs; this one bootstraps).

3. **Survey the repo** (read-only, keep it cheap — the skill will go deeper):
   ```bash
   git ls-files | head -400
   git ls-files | sed -n 's@.*\.@@p' | sort | uniq -c | sort -rn | head -30
   ```
   Read the top-level `README*`, and any manifest/config that reveals the stack (`package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, `Makefile`, `docker-compose*.yml`, `.tool-versions`, CI config). Read only what identifies the product, stack, and layout — do not read the whole tree.

4. **Apply the steering skill** (skills/steering/SKILL.md): give it the survey as context — bootstrap the steering guidelines for this repository (no existing guidelines), the default branch, the `ls-files` digest, the extension histogram, and the configs/READMEs you read. Ask it to return the full content of all four docs — product.md, tech.md, structure.md, rules.md — each as a separate fenced section, following the guidelines schema, grounding every claim in files it can point to and marking anything inferred as an assumption. The skill returns the four documents as data — it does not write files. Then continue.

5. **Persist.** Create the directory and write each returned document verbatim:
   ```bash
   mkdir -p docs/guidelines
   ```
   Then write each of `docs/guidelines/{product,tech,structure,rules}.md` from the skill's output. Do not invent content the skill did not return; if it returned a doc with open questions, keep them so the user can fill them in.

6. **Report.** Print the four written paths and a 2–3 line summary of what was captured (product one-liner, primary stack, notable structural boundaries). Note that `guidelines/rules.md` is meant to be hand-tuned by the team.

## Failure cases

- Not a git repo → STOP (step 1).
- Guidelines already exist → STOP, point to `/kanche:sdd-init-update` (step 2).
- Skill returns incomplete docs → write what came back, list the missing docs in the report, and suggest re-running rather than fabricating content.

## Done when

- `docs/guidelines/{product,tech,structure,rules}.md` all exist and are non-empty.
- Each was written from the **steering** skill's returned content.
- The report lists the four paths and the captured summary.
