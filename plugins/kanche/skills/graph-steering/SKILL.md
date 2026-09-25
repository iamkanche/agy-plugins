---
name: graph-steering
description: Analyze the repository using Knowledge Graph extraction and return the four steering guideline bodies.
model: flash
---

# /kanche:graph-steering

**Mission.** Analyze the repository using Knowledge Graph extraction (AST + semantic entities, god nodes, community hubs, dependency boundaries) and return the four steering guideline bodies — `product.md`, `tech.md`, `structure.md`, `rules.md` — grounded in what the code graph actually shows, so every later phase shares one verified architectural understanding.

## Read

Read what is needed to characterize the project graph and stack; do not read the whole tree blindly.

- Existing `.docs/guidelines/{product,tech,structure,rules}.md` if present (preserve intentional human edits, especially in `rules.md`).
- Existing Knowledge Graph artifacts if present: `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md` — to inspect god nodes, community clusters, and module cohesion.
- If `graphify-out/` is missing, survey the AST structure and manifests cheaply:
  ```bash
  git ls-files | head -400
  git ls-files | sed -n 's@.*\.@@p' | sort | uniq -c | sort -rn | head -30
  ```
- Manifests & config to identify the stack and versions: `package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, `*.gradle`, lockfiles, `Dockerfile`, `docker-compose*.yml`, CI workflows (`.github/`, `.gitlab-ci.yml`), `Makefile`, `.editorconfig`, linter/formatter configs.
- Top-level directory layout to infer module boundaries, community clusters, and layer dependencies.
- README / docs / ADRs for stated vision, users, and constraints.
- A representative sample of source entry points to confirm conventions.

Ground every non-obvious claim in a file or graph node; mark anything inferred but cannot confirm as **(inferred)**.

## Produce

Return the four bodies as four clearly labeled fenced/sectioned blocks — the calling workflow writes them to disk. Each is the file body only (no frontmatter). Use the project's output language for prose; keep identifiers, paths, commands, and versions verbatim.

- **`product.md`** — Vision (1–2 sentences), Target users / personas, Core value & primary use cases, In-scope vs. out-of-scope, Success signals. Source claims from README/docs; label gaps as open questions.
- **`tech.md`** — Languages & runtimes (with versions), Frameworks & key libraries, Data stores, Build/test/lint/run commands (the exact invocations, e.g. `make test`, `npm run lint`), External services & integrations, Known technical constraints.
- **`structure.md`** — Top-level layout with the responsibility of each major directory, Knowledge Graph community clusters and god nodes, Module/layer boundaries and allowed dependency directions (DAG flow), Naming conventions, Where tests and fixtures live, Where new code of a given kind belongs.
- **`rules.md`** — Mandatory, checkable rules the AI must follow every generation step: coding standards, forbidden patterns, required patterns, security/privacy rules, branch/commit discipline. Keep each rule imperative and verifiable.

End with a short **Confidence & gaps** note: which sections are well-grounded vs. inferred, and the top unknowns the human should confirm.

## Rules

- Returns DATA to the calling workflow (`/kanche:graph-init`, `/kanche:graph-init-update`); does NOT write files, commit, push, or orchestrate.
- Read-only: never attempt to modify files.
- Ground every claim in code or graph structure; label inferences as **(inferred)** and unknowns as open questions.
- Follow `.docs/guidelines/rules.md` (when refreshing) and the project's output-language policy.
