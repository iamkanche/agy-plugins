# Specs: SDD Workflow Structure & Governance Refactor

## Overview
This specification details the structural refactoring of SDD documentation paths, removal of legacy `/plugins/kanche` path nesting in product documentation and `sdd-sync`, renaming of `docs/` to `.docs/`, addition of explicit AI model declarations (`flash` vs `pro`/`claude`) to all skills, integration of `/goal` into `/sdd-run`, and the creation of a new Scrum PBI (Product Backlog Item) Creator skill.

## Requirements

### 1. Remove `/plugins/kanche` from `sdd-sync`
- Update `plugins/kanche/skills/sdd-sync/SKILL.md` so target product documentation path is `.docs/product/{domain}/` rather than `docs/product/plugins/kanche/{domain}/`.
- Ensure domain group mappings (`design`, `dev`, `gh-cli`, `git`, `planner`, `qa`, `sdd`, `scrum`) sync directly to `.docs/product/{domain}/`.

### 2. Rename `docs` to `.docs`
- Rename root `docs/` directory to `.docs/`.
- Update all path references across `plugins/kanche/skills/`, `plugins/kanche/agents/`, `plugins/kanche/rules/`, `plugin.json`, `index.html`, `README.md`, and steering docs from `docs/` to `.docs/`.

### 3. Simplify Product Docs Structure
- Product documentation structure is simplified to `.docs/product/{domain}/` (removing any `plugins/kanche/` nesting).
- Migrate existing domain folders (`design`, `dev`, `gh-cli`, `git`, `planner`, `qa`, `sdd`) into `.docs/product/{domain}/`.

### 4. Explicit AI Model Attribution for Skills
- Add a `model:` field to every skill's YAML frontmatter in `plugins/kanche/skills/*/SKILL.md`.
- **`model: flash`**: Assigned to simple, mechanical, CLI, execution, and validation tasks (`code-implement`, `gh-cli-pr-*`, `git-*`, `qa-validate`, `sdd-continue`, `sdd-init`, `sdd-init-update`, `sdd-run`, `sdd-sync`, `security-scan`).
- **`model: pro`**: Assigned to design, specification, architecture, planning, code review, QA review, and brainstorming tasks (`design-grill`, `design-specs`, `design-specs-review`, `design-init`, `design-review`, `planner-tasks`, `planner-review`, `code-review`, `qa-review`, `qa-test-plan`, `sdd-steering`, `ui-design-stitch`, `scrum-pbi-create`).

### 5. Goal Integration in `/sdd-run`
- Update `plugins/kanche/skills/sdd-run/SKILL.md` to incorporate `/goal` persistence mode, ensuring long-running, autonomous execution without stopping until `<!-- GOAL_COMPLETE -->` criteria are met.

### 6. Scrum PBI Creator Skill
- Add a new skill `scrum-pbi-create` in `plugins/kanche/skills/scrum-pbi-create/SKILL.md`.
- Domain: `scrum` (`.docs/product/scrum/`).
- Frontmatter: `name: scrum-pbi-create`, `description: Create structured Product Backlog Items (PBI) with user stories, acceptance criteria, priority, and story points under .docs/product/scrum/`, `model: pro`.
- Register command `/kanche:scrum-pbi-create` in `plugins/kanche/plugin.json` and `index.html`.

## Acceptance Criteria
- [ ] No references to `docs/product/plugins/kanche/` remain in any active skills, agents, or rules.
- [ ] `docs/` directory is renamed to `.docs/` and all references updated cleanly.
- [ ] All 40 skills have valid `model:` attributes in YAML frontmatter.
- [ ] `/kanche:sdd-run` incorporates `/goal` mode instructions and goal completion markers.
- [ ] `/kanche:scrum-pbi-create` skill is implemented, functional, and registered in `plugin.json` and `index.html`.
