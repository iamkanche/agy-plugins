# Functional Specifications: Separate SDD Skills into Modular Plugins

## 1. Executive Summary
The goal of this refactoring is to modularize the monolithic `sdd` plugin in `agy-plugins` by extracting domain-specific skills and agents into dedicated plugins (`design`, `qa`, `planner`, `dev`), while keeping high-level workflow orchestration and steering in `sdd`.

## 2. Problem Statement
Currently, `plugins/sdd` contains 16 skills and 5 subagents handling specs, design, tasks, coding, QA, and workflow orchestration. This creates high coupling, making it harder for users to adopt individual capabilities (such as using *only* QA testing skills or *only* Design/Architecture skills).

## 3. Proposed Plugin Breakdown & Skill Mapping

### 3.1 `design` Plugin (`plugins/design`)
- **Skills**:
  - `grill` (`/design:grill`): Interrogate feature requests adversarially.
  - `specs` (`/design:specs`): Generate functional specifications & user stories.
  - `specs-review` (`/design:specs-review`): Audit functional specifications.
  - `design` (`/design:design`): System architecture, API, UI wireframes, and data models.
  - `design-review` (`/design:design-review`): Audit system architecture designs.
- **Agents**: `design-analyst`, `design-architect`

### 3.2 `qa` Plugin (`plugins/qa`)
- **Skills**:
  - `validate` (`/qa:validate`): Run test suites, linters, and verification checks.
  - `test-plan` (`/qa:test-plan`): Generate test plan and test cases.
  - `build-review` (`/qa:build-review`): Code quality & test diff review.
- **Agents**: `qa-validator`

### 3.3 `planner` Plugin (`plugins/planner`)
- **Skills**:
  - `tasks` (`/planner:tasks`): Generate structured task manifests.
  - `tasks-review` (`/planner:tasks-review`): Audit task breakdown & dependency ordering.
- **Agents**: `planner-agent`

### 3.4 `dev` Plugin (`plugins/dev`)
- **Skills**:
  - `build` (`/dev:build`): Implement code changes incrementally.
- **Agents**: `dev-coder`

### 3.5 `sdd` Core Plugin (`plugins/sdd`)
- **Skills**:
  - `init` (`/sdd:init`): Bootstrap steering guidelines.
  - `init-update` (`/sdd:init-update`): Refresh steering guidelines.
  - `steering` (`/sdd:steering`): Return steering guideline bodies.
  - `sync` (`/sdd:sync`): Promote development docs to product memory.
  - `run` (`/sdd:run`): Master orchestrator invoking sub-plugins (`/design:*`, `/planner:*`, `/dev:*`, `/qa:*`).
  - `continue` (`/sdd:continue`): Resume workflow from on-disk state.

## 4. Compatibility & Migration Strategy
- `sdd:run` will be updated to call domain plugin commands (`/design:specs`, `/design:design`, `/planner:tasks`, `/dev:build`, `/qa:validate`, etc.) seamlessly.
- `README.md`, `index.html`, and `.agents/plugins/marketplace.json` will be updated to register all domain plugins.

## 5. Acceptance Criteria
1. All domain plugins (`design`, `qa`, `planner`, `dev`, `sdd`) are created with valid `plugin.json` manifests, rules, agents, and skills.
2. `plugins/sdd` is focused on core orchestration and steering.
3. `marketplace.json` and root `README.md` are updated to register and describe all plugins.
4. `index.html` dashboard reflects the new plugins.
