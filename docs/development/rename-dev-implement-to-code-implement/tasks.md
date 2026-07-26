# Tasks: Rename dev-implement to code-implement & Update index.html

- [ ] 1. Move skill folder `plugins/kanche/skills/dev-implement` to `plugins/kanche/skills/code-implement` and update `SKILL.md` frontmatter & content.
- [ ] 2. Update `@coder` subagent definition in `plugins/kanche/agents/coder/agent.json`.
- [ ] 3. Update SDD orchestrators (`sdd-run/SKILL.md` and `sdd-continue/SKILL.md`) references from `dev-implement` to `code-implement`.
- [ ] 4. Update documentation files (`README.md`, `docs/guidelines/structure.md`, and product specs).
- [ ] 5. Update `index.html` dashboard registry:
  - Add `/kanche:code-review` and `/kanche:security-scan` to `qaCommands`.
  - Update `/kanche:dev-implement` to `/kanche:code-implement` in `devCommands`, `agentsData`, and `sddWorkflowPhases`.
