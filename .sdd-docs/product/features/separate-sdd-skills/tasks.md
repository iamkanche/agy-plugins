# Task Manifest: Separate SDD Skills into Modular Domain Plugins

## Tasks

- [x] **Task 1: Setup `plugins/design` Plugin**
  - Create directory structure for `plugins/design` (`rules`, `agents`, `skills`).
  - Create `plugin.json` for `design`.
  - Copy output language rule `rules/output-language.md`.
  - Create agents `design-analyst` and `design-architect`.
  - Move/copy skills: `grill`, `specs`, `specs-review`, `design`, `design-review`.

- [x] **Task 2: Setup `plugins/qa` Plugin**
  - Create directory structure for `plugins/qa` (`rules`, `agents`, `skills`).
  - Create `plugin.json` for `qa`.
  - Copy output language rule `rules/output-language.md`.
  - Create agent `qa-validator`.
  - Move/copy skills: `validate`, `build-review`, and add `test-plan`.

- [x] **Task 3: Setup `plugins/planner` Plugin**
  - Create directory structure for `plugins/planner` (`rules`, `agents`, `skills`).
  - Create `plugin.json` for `planner`.
  - Copy output language rule `rules/output-language.md`.
  - Create agent `planner-agent`.
  - Move/copy skills: `tasks`, `tasks-review`.

- [x] **Task 4: Setup `plugins/dev` Plugin**
  - Create directory structure for `plugins/dev` (`rules`, `agents`, `skills`).
  - Create `plugin.json` for `dev`.
  - Copy output language rule `rules/output-language.md`.
  - Create agent `dev-coder`.
  - Move/copy skill: `build`.

- [x] **Task 5: Refactor `plugins/sdd` Core Orchestration**
  - Update `plugins/sdd/plugin.json`.
  - Retain core skills: `init`, `init-update`, `steering`, `sync`, `run`, `continue`.
  - Clean up moved skills from `plugins/sdd/skills/`.
  - Update `/sdd:run` skill to reference domain plugin skills (`/design:*`, `/planner:*`, `/dev:*`, `/qa:*`).
  - Update `plugins/sdd/README.md`.

- [x] **Task 6: Update Marketplace & Root Documentation**
  - Update `.agents/plugins/marketplace.json` to register `design`, `qa`, `planner`, `dev`, `sdd`, `git`, `gh-cli`.
  - Update root `README.md` to document all active plugins and their command namespaces.

- [x] **Task 7: Update `index.html` Marketplace Dashboard**
  - Add visual cards, badges, and skill descriptions for `design`, `qa`, `planner`, and `dev` plugins to `index.html`.
