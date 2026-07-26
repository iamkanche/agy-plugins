---
feature: design
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# Design & Specs Plugin — Consolidated Specification

## Context
The `design` plugin packages requirements interrogation, functional specification drafting, system design architecture, and UI/UX wireframing skills for Google Antigravity agents.

## Capabilities
- `/kanche:design-grill` - Adversarially probe feature requests to extract ambiguities and rank clarifying questions.
- `/kanche:design-specs` - Draft functional specifications documenting target changes and acceptance criteria.
- `/kanche:design-specs-review` - Perform review on specs draft, returning a GO/NO-GO verdict with findings.
- `/kanche:design-init` - Draft system architecture design specifications including component details, API schemas, and DB models.
- `/kanche:design-review` - Perform review on design documents, returning a GO/NO-GO verdict with findings.

## Specialized Subagents
- `analyst`: Handles feature interrogation, specs drafting, and specs review (`grill`, `specs`, `specs-review`).
- `architect`: Handles system architecture design and design review (`init`, `review`).

## Acceptance Criteria (as-built)
1. Exposes `/kanche:design-grill`, `/kanche:design-specs`, `/kanche:design-specs-review`, `/kanche:design-init`, and `/kanche:design-review` slash commands.
2. Registers subagents `analyst` and `architect` in `plugins/design/plugin.json`.
3. Integrates with the master `/kanche:sdd-run` orchestrator for P1 (Specs) and P2 (Design) phases.
