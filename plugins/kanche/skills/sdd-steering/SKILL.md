---
name: sdd-steering
description: Analyze the repository and return the four steering guideline bodies.
---

# /kanche:sdd-steering

**Mission.** Analyze the repository and return the four steering guideline bodies —
`product.md`, `tech.md`, `structure.md`, `rules.md` — grounded in what the code actually
shows, so every later phase shares one project understanding.

## Read

Read only what is needed to characterize the project; do not read the whole tree.

- Existing `docs/guidelines/{product,tech,structure,rules}.md` if present (you are
  refreshing, not overwriting blindly — preserve intentional human edits, especially in
  `rules.md`).
- Manifests & config to fix the stack and versions: `package.json`, `go.mod`, `pyproject.toml`,
  `Cargo.toml`, `pom.xml`, `*.gradle`, lockfiles, `Dockerfile`, `docker-compose*.yml`, CI
  workflows (`.github/`, `.gitlab-ci.yml`), `Makefile`, `.editorconfig`, linter/formatter
  configs.
- Top-level directory layout (glob a few levels deep) to infer module boundaries and layers.
- README / docs / ADRs for stated vision, users, and constraints.
- A representative sample of source entry points to confirm conventions — do not read every file.

Prefer bash (`git ls-files`, `ls`, `wc -l`) and glob/grep to survey breadth cheaply;
read only the files whose content you must quote or characterize. Mark anything you infer but
cannot confirm from a file as **(inferred)**.

## Produce

Return the four bodies as four clearly labeled fenced/sectioned blocks — the calling workflow
writes them to disk. Each is the file body only (no frontmatter). Use the project's output
language for prose; keep identifiers, paths, commands, and versions verbatim.

- **`product.md`** — Vision (1–2 sentences), Target users / personas, Core value & primary use
  cases, In-scope vs. out-of-scope, Success signals. Source claims from README/docs; label
  gaps as open questions rather than inventing product intent.
- **`tech.md`** — Languages & runtimes (with versions), Frameworks & key libraries, Data
  stores, Build/test/lint/run commands (the exact invocations, e.g. `make test`, `npm run
  lint`), External services & integrations, Known technical constraints. This file is what
  `validate` and `build` rely on for commands — be precise and complete about them.
- **`structure.md`** — Top-level layout with the responsibility of each major directory,
  Module/layer boundaries and allowed dependency directions, Naming conventions, Where tests
  and fixtures live, Where new code of a given kind belongs.
- **`rules.md`** — Mandatory, checkable rules the AI must follow every generation step: coding
  standards, forbidden patterns, required patterns, security/privacy rules, branch/commit
  discipline. Keep each rule imperative and verifiable. Do not fabricate rules the repo does
  not evidence; flag suggested-but-unconfirmed rules distinctly.

End with a short **Confidence & gaps** note: which sections are well-grounded vs. inferred, and
the top unknowns the human should confirm.

## Rules

- Returns DATA to the calling workflow (`/kanche:sdd-init`, `/kanche:sdd-init-update`); does NOT write files,
  commit, push, or orchestrate.
- Read-only: never attempt to modify files.
- Ground every non-obvious claim in a file; label inferences as **(inferred)** and unknowns as
  open questions. Never present a guess as fact.
- Follow `docs/guidelines/rules.md` (when refreshing) and the project's output-language policy.
