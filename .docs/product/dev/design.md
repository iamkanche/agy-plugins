# Development Workflows Design

## 1. Architecture & Execution Loop
The development domain executes implementation tasks defined in task manifests (`tasks.md`), closing the loop with code reviews:
1. Task Parsing: Parses individual ordered tasks and target files.
2. Code Generation: Specialized agents apply surgical, minimal changes obeying project style rules.
3. Verification: Executes local test suites or linter checks.
4. Review Consumption: Consumes `review-verdict` blocks from `@reviewer` (`/kanche:code-review`) and applies targeted corrections up to 3 iterations.

## 2. Agent Roles
- `@coder`: Full-stack features, scripts, and multi-file orchestrations.
- `@frontend-expert`: Web components, responsive CSS, and state management.
- `@backend-expert`: Backend APIs, controllers, services, and middleware.
- `@database-engineer`: Data schema changes and query tuning.

## 3. Human Gating
All file modifications are verified through testing, but git commits require explicit user approval via `/kanche:git-commit` per `plugins/kanche/rules/destructive-safety.md`.

