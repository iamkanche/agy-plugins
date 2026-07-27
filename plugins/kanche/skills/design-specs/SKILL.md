---
name: design-specs
description: Generate the functional specifications file based on feature description and guidelines.
---

# /kanche:design-specs

**Mission.** Turn the feature request plus the answered grill questions into a complete, testable `specs.md` body for `docs/development/{NNN}_{slug}/specs.md` — the WHAT, not the HOW — incorporating closed-loop feedback from `/kanche:design-specs-review`.

## Loop Engineering Protocol (Generator Role — P1 Specs Loop)

In the Loop Engineering Framework, `/kanche:design-specs` acts as the **Generator Skill** paired with `/kanche:design-specs-review`:
- **Iteration 1**: Generates initial `specs.md` based on feature request & grill Q&A.
- **Iteration 2..N (≤3x Loop)**: Receives `sdd-review` findings (`verdict: NO-GO`, `findings: [{severity, msg, fix_suggestion}]`). Applies targeted fixes to unresolved sections (e.g. testability, acceptance criteria, NFRs) without discarding existing human edits or valid criteria.

## Read

- The feature request / backlog text and the resolved grill Q&A passed in by the workflow.
- `docs/guidelines/{product,tech,structure,rules}.md` and `plugins/kanche/rules/loop-engineering.md` — scope boundaries, loop rules, terminology, and constraints.
- `sdd-review` findings from prior review iterations (when running in iteration 2..N).
- Any existing `docs/development/{NNN}_{slug}/{specs,notes}.md` for this feature (refine, don't discard human edits).
- The codebase only as needed (glob/grep/read) to ground data-model and integration claims in what exists — do not design the solution here.

## Produce

Return the `specs.md` body only (no frontmatter, no HOW/implementation detail), with these sections in order:

- **Context** — Why this work exists; the problem and the user/business value. Link the driving item id.
- **Scope** — In-scope bullets and an explicit **Out of scope / non-goals** list.
- **User stories** — `As a <role>, I want <capability>, so that <benefit>.` Grouped if several roles.
- **Acceptance criteria** — Numbered, each independently **testable** and observable. Prefer Given/When/Then. Cover happy path, boundary/empty inputs, and error/failure behavior. No criterion may depend on implementation internals. Every user story maps to ≥1 criterion.
- **Data model** — Entities, key fields & types, relationships, invariants/constraints, and states/transitions where relevant. Note new vs. changed vs. existing. (Detailed schema deltas are the design phase's job — keep this at the domain level.)
- **NFR (non-functional requirements)** — Performance, scale, security/authz, privacy/PII handling, accessibility, i18n, observability — only those that actually apply, each stated measurably.
- **Open questions** — Anything still unresolved, with the assumption you proceeded under so a reviewer can accept or correct it.

Keep acceptance criteria and NFRs concrete enough that `specs-review` can judge testability and `tasks`/`validate` can derive checks from them.

## Rules

- Returns DATA to the calling workflow (`/kanche:design-specs`); does NOT write files, commit, push, or orchestrate. Read-only — no writes/edits.
- Specify WHAT and WHY; leave HOW (components, interfaces, tech choices) to `design`.
- Every acceptance criterion must be testable and traceable to a user story or NFR; flag any that is not.
- Ground data-model/integration claims in real code or guidelines; label inferences. Never invent requirements the request or grill answers do not support — record them as open questions instead.
- Follow `docs/guidelines/rules.md`, `plugins/kanche/rules/loop-engineering.md`, and output-language policies.

