# Development Workflows Specification

## 1. Overview
Provides autonomous implementation and code modification workflows across frontend, backend, database, and full-stack layers.

## 2. Included Skills & Commands
- `/kanche:code-implement`: Implements target code changes incrementally against task manifests, executes closed-loop fixes from reviews, and executes verification tests.

## 3. Specialized Agent Orchestration
Implementation is delegated according to architectural domain:
- `@coder`: General full-stack and systems engineering tasks.
- `@frontend-expert`: React, TypeScript, modern web styling, client-side state, and UI component engineering.
- `@backend-expert`: API services, MSC architecture, server business logic, and routing.
- `@database-engineer`: Schema migrations, indexing, query optimizations, and data integrity.

## 4. Product Invariants
- Incremental, test-backed code modification preserving project conventions.
- Consumes structured `review-verdict` blocks (`verdict: GO` | `NO-GO`) in closed-loop cycles (≤3x) to address review findings.
- Standalone execution: `/kanche:code-implement` operates independently without orchestrator coupling.
- Safety: Code commits are gated by explicit interactive human confirmation via `/kanche:git-commit`.
- All implementation agents and skills are unified on `model: flash`.

