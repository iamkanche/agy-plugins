---
name: design-adr
description: Generate numbered Architecture Decision Records (ADRs) documenting context, competing options, decision, and consequences.
---

# /kanche:design-adr

**Mission.** Record non-trivial architectural trade-offs (`@architect`, `agents/architect.md`) into `.docs/product/{domain}/decisions.md` (when `--domain` is known) or `.docs/adr/{NNNN}-{slug}.md`.

## Inputs

- `<title>` (required) — concise decision title (e.g. `Use Double-Entry Ledger Constraints`).
- `--domain=<domain>` (optional) — append numbered ADR entry to `.docs/product/{domain}/decisions.md`.

## Steps

1. **Analyze Context & Constraints.** Read `.docs/guidelines/{product,tech,structure}.md` and relevant design docs (`.docs/development/{slug}/design.md`).
2. **Compare ≥2 Competing Options.** For each option, list concrete Pros, Cons, and coupling/migration impact grounded in repo files.
3. **Draft ADR Entry:**
   - `## ADR-{NNNN}: {Title}`
   - **Status:** Accepted | Proposed | Superseded
   - **Context:** Problem statement and constraints.
   - **Options Considered:** Compact comparison table or bullets.
   - **Decision:** Chosen option and rationale ("Because..., accepting...").
   - **Consequences:** Positive/negative impacts and follow-ups.
4. **Persist.** Write to `.docs/product/{domain}/decisions.md` (appending sequentially) or `.docs/adr/{NNNN}-{slug}.md`.

## Rules

- Never commit or push autonomously.
- Ground claims in real file paths and observed constraints.
- Follow `rules/token-optimization.md` and `rules/output-language.md`.
