# Design Workflows Design

## 1. Subagent Collaboration
Design workflows leverage specialized subagents:
- `@analyst`: Adversarial interrogation and requirement clarification.
- `@architect`: Component boundary definitions, data modeling, and architectural reviews.
- `@designer`: Visual UI screen layouts, wireframes, design tokens, and StitchMCP generation.

## 2. Review Protocol
- Design review skills emit universal `review-verdict` blocks (`verdict: GO` | `NO-GO`).
- Automated closed-loop iterations (≤3x) resolve architectural and specification findings before advancing.

## 3. Outputs
Artifact outputs feed directly into `.docs/development/{slug}/specs.md` and `design.md` during phase P1 and P2 of SDD workflows.
