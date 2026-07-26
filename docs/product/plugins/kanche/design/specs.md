# Design Workflows Specification

## 1. Overview
Provides systemic design, specification generation, adversarial design interrogation, and architectural reviews for features.

## 2. Included Skills & Commands
- `/kanche:design-grill`: Interrogates feature requests adversarially with a ranked list of clarifying questions.
- `/kanche:design-init`: Generates system design specifications (component boundaries, data model, user flow).
- `/kanche:design-specs`: Generates the functional specifications file (`specs.md`).
- `/kanche:design-specs-review`: Reviews functional specifications against rules and guidelines.
- `/kanche:design-review`: Reviews system design specifications and overall architecture.

## 3. Product Invariants
- Grounding in existing guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- Explicit documentation of trade-offs and key architectural decisions.
